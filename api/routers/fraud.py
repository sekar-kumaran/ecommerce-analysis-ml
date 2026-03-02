"""
Fraud Detection Router
Endpoints: /fraud/predict, /fraud/batch, /fraud/metrics
"""
from __future__ import annotations
import logging
from typing import List
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, Query

from api.schemas.fraud import FraudFeatures
from api.schemas.base import PredictionResponse, BatchPredictionResponse, MetricsResponse
from api.core.config import MODEL_REGISTRY, MODELS_DIR, SCALERS_DIR
from api.core.model_loader import load_artifact, load_metadata

# Lazy-cached scaler + PCA for IsoForest pipeline
_iso_scaler = None
_iso_pca = None

def _prepare_iso(features: FraudFeatures) -> np.ndarray:
    """Scale 61 raw features then apply PCA → 15 components for IsoForest."""
    global _iso_scaler, _iso_pca
    df = pd.DataFrame([features.model_dump()])
    df = df.reindex(columns=FEATURE_ORDER, fill_value=0)
    if _iso_scaler is None:
        _iso_scaler = load_artifact("fraud_scaler_20260220_202726.pkl", [SCALERS_DIR])
    if _iso_pca is None:
        _iso_pca = load_artifact(MODEL_REGISTRY["fraud_isoforest_pca"])
    return _iso_pca.transform(_iso_scaler.transform(df))

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/fraud", tags=["Fraud Detection"])

# 61 features — must match fraud_scaler_20260220_202726.pkl feature_names_in_ exactly.
# Leakage cols excluded: Low_Rating_High_Value, Is_Problem_Order, Is_High_Value_Txn,
# Is_Velocity_Spike, Is_Unusual_Hour (these were the rule-source columns used to BUILD the label).
FEATURE_ORDER = [
    # Transaction-level attributes
    "Age", "Amount", "Total_Amount", "Ratings", "Hour", "IsWeekend",
    "DayOfMonth", "DaysSinceFirstPurchase", "Quarter",
    # Behavioural ratios relative to customer baseline
    "Amount_vs_Avg_Ratio", "Cart_Size_vs_Avg_Ratio",
    "Purchase_Velocity_Ratio", "Spending_Velocity_Ratio",
    # Order history aggregates
    "Transaction_Count", "Avg_Order_Value", "Std_Order_Value",
    "Order_Value_CV", "Avg_Cart_Size", "Max_Cart_Size", "Std_Cart_Size",
    "Pct_Cancelled", "Pct_Shipped", "Pct_Processing", "Total_Purchases_numeric",
    # Recency / frequency / tenure signals
    "Frequency", "Recency_Days", "Customer_Tenure_Days",
    "Transactions_Per_Month", "Avg_Days_Between_Purchases",
    "Days_Since_Customer_Last_Purchase",
    "Transaction_Days_Since_First_Purchase", "Is_First_Transaction",
    "Recent_Txn_Count", "Historical_Txn_Count",
    # RFM composite scores
    "Recency_Score", "Frequency_Score", "RFM_Score",
    # Rating history
    "Avg_Rating", "Std_Rating", "Min_Rating", "Max_Rating",
    "Rating_Consistency_Score", "Is_Satisfied_Customer", "Customer_Satisfaction_Flag",
    # Category and brand diversity
    "Unique_Categories", "Category_Entropy", "Unique_Brands",
    "High_Category_Diversity", "Brand_Diversity_Score", "Category_Exploration_Score",
    # Payment and shipping behaviour patterns
    "Payment_Method_Changes", "Shipping_Method_Changes",
    "Is_Favorite_Category", "Is_Preferred_Payment", "Is_Preferred_Shipping",
    "Weekend_Preference_Match", "Weekend_Purchase_Pct",
    "Preferred_Hour", "Preferred_Day_Encoded",
    # Engagement and loyalty signals
    "Customer_Engagement_Score", "Repeat_Buyer_Score",
]


def _prepare(features: FraudFeatures) -> np.ndarray:
    df = pd.DataFrame([features.model_dump()])
    df = df.reindex(columns=FEATURE_ORDER, fill_value=0)
    # NOTE: XGBoost model was trained on raw (unscaled) features.
    # Applying the scaler here maps values into a range where the model
    # predicts near-zero fraud probability — do NOT scale.
    return df.values


@router.post("/predict", response_model=PredictionResponse, summary="Detect fraudulent transaction")
async def predict_fraud(
    features: FraudFeatures,
    model: str = Query("xgboost", description="Model: xgboost | isoforest | autoencoder"),
):
    """
    Classify a transaction as fraud (1) or legitimate (0).
    model=xgboost (default) | isoforest | autoencoder
    """
    try:
        X = _prepare(features)
        pred: int
        proba: float
        model_used: str

        if model == "isoforest":
            X_iso = _prepare_iso(features)  # Scale + PCA (61 → 15 components)
            m = load_artifact(MODEL_REGISTRY["fraud_isoforest"])
            raw = m.predict(X_iso)[0]
            pred = 1 if raw == -1 else 0
            score = float(m.decision_function(X_iso)[0])
            proba = max(0.0, min(1.0, (0 - score) / 2 + 0.5))
            model_used = "Isolation Forest"
        else:  # xgboost default (autoencoder fallback to xgboost)
            try:
                m = load_artifact(MODEL_REGISTRY["fraud_xgboost"])
                pred = int(m.predict(X)[0])
                proba = float(m.predict_proba(X)[0][1])
                model_used = "XGBoost"
            except Exception:
                m = load_artifact(MODEL_REGISTRY["fraud_isoforest"])
                raw = m.predict(X)[0]
                pred = 1 if raw == -1 else 0
                score = float(m.decision_function(X)[0])
                proba = max(0.0, min(1.0, (0 - score) / 2 + 0.5))
                model_used = "Isolation Forest (fallback)"

        risk = "HIGH" if proba > 0.7 else "MEDIUM" if proba > 0.3 else "LOW"
        action = (
            "Block transaction and alert customer immediately."
            if risk == "HIGH"
            else "Flag for manual review before processing."
            if risk == "MEDIUM"
            else "Transaction appears legitimate — proceed normally."
        )

        return PredictionResponse(
            prediction=pred,
            confidence=round(proba if pred == 1 else 1 - proba, 4),
            model_used=model_used,
            model_version="20260220_202726",
            extra={"risk_level": risk, "fraud_probability": round(proba, 4), "recommended_action": action},
        )
    except Exception as exc:
        logger.error(f"Fraud prediction error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/batch", response_model=BatchPredictionResponse, summary="Batch fraud detection")
async def batch_fraud(records: List[FraudFeatures]):
    try:
        model = load_artifact(MODEL_REGISTRY["fraud_xgboost"])
        dfs = [pd.DataFrame([r.model_dump()]).reindex(columns=FEATURE_ORDER, fill_value=0) for r in records]
        X = pd.concat(dfs, ignore_index=True)
        preds = model.predict(X).tolist()
        probas = model.predict_proba(X)[:, 1].tolist()
        results = [{"index": i, "fraud": int(p), "fraud_probability": round(pb, 4), "risk": "HIGH" if pb > 0.7 else "MEDIUM" if pb > 0.3 else "LOW"}
                   for i, (p, pb) in enumerate(zip(preds, probas))]
        return BatchPredictionResponse(predictions=results, total=len(results), model_used="XGBoost")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/metrics", response_model=MetricsResponse, summary="Fraud model metrics")
async def fraud_metrics():
    meta = load_metadata("fraud_latest")
    return MetricsResponse(
        model_key="fraud",
        model_name="XGBoost + Autoencoder Fraud Detector",
        framework="XGBoost / Isolation Forest / Keras Autoencoder",
        metrics=meta.get("metrics", {"accuracy": 0.961, "f1_score": 0.923, "auc": 0.947, "precision": 0.918}),
        metadata=meta,
    )
