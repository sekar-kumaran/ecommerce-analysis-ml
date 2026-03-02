"""
Churn Prediction Router
Endpoints: /churn/predict, /churn/batch, /churn/metrics, /churn/feature-importance
"""
from __future__ import annotations
import logging
from typing import List
from datetime import datetime

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, Query

from api.schemas.churn import ChurnFeatures
from api.schemas.base import PredictionResponse, BatchPredictionResponse, MetricsResponse
from api.core.config import MODEL_REGISTRY, MODELS_DIR, SCALERS_DIR
from api.core.model_loader import load_artifact, load_metadata, load_json_report

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/churn", tags=["Churn Prediction"])

FEATURE_ORDER = [
    "Transaction_Count", "Total_Spend", "Avg_Order_Value", "Std_Order_Value",
    "Frequency", "Customer_Tenure_Days", "Transactions_Per_Month", "Customer_LTV",
    "Avg_Days_Between_Purchases", "Order_Value_CV", "Frequency_Score", "Monetary_Score",
    "Historical_Txn_Count", "Historical_Spend", "Preferred_Hour", "Weekend_Purchase_Pct",
    "Preferred_Day_Encoded", "Unique_Categories", "Category_Entropy", "Unique_Brands",
    "Avg_Rating", "Std_Rating", "Min_Rating", "Max_Rating", "Is_Satisfied_Customer",
    "Payment_Method_Changes", "Shipping_Method_Changes", "Pct_Shipped", "Pct_Processing",
    "Pct_Cancelled", "Avg_Cart_Size", "Max_Cart_Size", "Std_Cart_Size", "Age",
]


def _prepare(features: ChurnFeatures) -> np.ndarray:
    """Scale input features using the saved churn scaler.

    The scaler was saved as a dict:
        {'scaler': RobustScaler, 'feature_names': [...], 'removed_features': [...]}
    We must unwrap the 'scaler' key before calling .transform().
    """
    df = pd.DataFrame([features.model_dump()])
    df = df.reindex(columns=FEATURE_ORDER, fill_value=0)
    try:
        scaler_pkg = load_artifact("churn_scaler_20260218_184733.pkl", [SCALERS_DIR])
        # Saved as a dict — unwrap the actual scaler object
        scaler = scaler_pkg['scaler'] if isinstance(scaler_pkg, dict) else scaler_pkg
        return scaler.transform(df)
    except Exception as e:
        logger.warning(f"Churn scaler transform failed ({e}), using raw values")
        return df.values


@router.post("/predict", response_model=PredictionResponse, summary="Predict churn probability")
async def predict_churn(
    features: ChurnFeatures,
    model: str = Query("xgboost", description="Model to use: xgboost | lightgbm | widedeep"),
):
    """
    Returns a churn probability score [0–1].
    model=xgboost (default) | lightgbm | widedeep
    """
    try:
        X = _prepare(features)
        proba: float
        model_used: str

        if model == "widedeep":
            try:
                m = load_artifact(MODEL_REGISTRY["churn_widedeep"])
                proba = float(m.predict(X)[0][0])
                model_used = "Wide & Deep Neural Net"
            except Exception:
                m = load_artifact(MODEL_REGISTRY["churn_xgboost"])
                proba = float(m.predict_proba(X)[0][1])
                model_used = "XGBoost (fallback)"
        elif model == "lightgbm":
            m = load_artifact(MODEL_REGISTRY["churn_lightgbm"])
            proba = float(m.predict_proba(X)[0][1])
            model_used = "LightGBM"
        else:  # default: xgboost
            m = load_artifact(MODEL_REGISTRY["churn_xgboost"])
            proba = float(m.predict_proba(X)[0][1])
            model_used = "XGBoost"

        risk = "HIGH" if proba >= 0.7 else "MEDIUM" if proba >= 0.4 else "LOW"
        action = (
            "Send personalised retention offer within 7 days — high urgency."
            if risk == "HIGH"
            else "Monitor engagement; consider a loyalty incentive next campaign."
            if risk == "MEDIUM"
            else "Customer is stable — maintain standard engagement."
        )

        return PredictionResponse(
            prediction=round(proba, 4),
            confidence=round(max(proba, 1 - proba), 4),
            model_used=model_used,
            model_version="20260218_184733",
            extra={"risk_level": risk, "recommended_action": action},
        )
    except Exception as exc:
        logger.error(f"Churn prediction error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/batch", response_model=BatchPredictionResponse, summary="Batch churn prediction")
async def batch_churn(records: List[ChurnFeatures]):
    """Predict churn probability for multiple customers at once."""
    try:
        results = []
        for i, rec in enumerate(records):
            X = _prepare(rec)
            try:
                model = load_artifact(MODEL_REGISTRY["churn_xgboost"])
                proba = float(model.predict_proba(X)[0][1])
            except Exception:
                proba = 0.5
            results.append({"index": i, "churn_probability": round(proba, 4), "at_risk": proba >= 0.5})

        return BatchPredictionResponse(predictions=results, total=len(results), model_used="XGBoost")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/metrics", response_model=MetricsResponse, summary="Churn model performance metrics")
async def churn_metrics():
    """Return evaluation metrics for the deployed churn models."""
    meta = load_metadata("churn_deployment")
    return MetricsResponse(
        model_key="churn",
        model_name="Wide&Deep Churn Predictor",
        framework="TensorFlow/Keras + XGBoost",
        metrics=meta.get("expected_performance", {
            "roc_auc": 0.896, "precision": 0.812, "recall": 0.954, "f1_score": 0.877,
        }),
        metadata={
            "threshold": meta.get("threshold", 0.5),
            "n_features": len(FEATURE_ORDER),
            "training_date": "2026-02-18",
            "best_model": meta.get("best_model", "Wide_Deep"),
        },
    )


@router.get("/feature-importance", summary="Churn feature importance")
async def churn_feature_importance():
    """Return feature importance from the XGBoost churn model."""
    try:
        model = load_artifact(MODEL_REGISTRY["churn_xgboost"])
        if hasattr(model, "feature_importances_"):
            importance = dict(zip(FEATURE_ORDER, model.feature_importances_.tolist()))
            sorted_imp = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
            return {"feature_importance": sorted_imp, "model": "XGBoost"}
    except Exception:
        pass

    # Fallback: load from CSV if available
    csv_path = MODELS_DIR / "churn_feature_importance_20260218_184733.csv"
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        return {"feature_importance": df.set_index(df.columns[0])[df.columns[1]].to_dict(), "model": "XGBoost (CSV)"}

    return {"feature_importance": {}, "model": "unavailable"}
