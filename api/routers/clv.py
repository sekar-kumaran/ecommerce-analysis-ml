"""
Customer Lifetime Value (CLV) Router
Endpoints: /clv/predict, /clv/batch, /clv/metrics, /clv/model-comparison
"""
from __future__ import annotations
import logging
from typing import List
import pandas as pd
from fastapi import APIRouter, HTTPException, Query

from api.schemas.clv import CLVFeatures
from api.schemas.base import PredictionResponse, BatchPredictionResponse, MetricsResponse
from api.core.config import MODEL_REGISTRY, MODELS_DIR, SCALERS_DIR
from api.core.model_loader import load_artifact, load_metadata

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/clv", tags=["Customer Lifetime Value"])

# 36 features — must match clv_scaler_20260218_212141.pkl feature_names_in_ exactly.
# Leakage cols removed during training: Total_Spend, Historical_Spend, Recent_Spend,
# Monetary_Score (all direct components of the CLV target).
FEATURE_ORDER = [
    "Transaction_Count", "Avg_Order_Value", "Std_Order_Value", "Frequency",
    "Recency_Days", "Customer_Tenure_Days", "Transactions_Per_Month",
    "Avg_Days_Between_Purchases", "Order_Value_CV", "Recency_Score",
    "Frequency_Score", "RFM_Score", "Recent_Txn_Count", "Historical_Txn_Count",
    "Purchase_Velocity_Ratio", "Spending_Velocity_Ratio", "Preferred_Hour",
    "Weekend_Purchase_Pct", "Preferred_Day_Encoded", "Unique_Categories",
    "Category_Entropy", "Unique_Brands", "Avg_Rating", "Std_Rating",
    "Min_Rating", "Max_Rating", "Is_Satisfied_Customer", "Payment_Method_Changes",
    "Shipping_Method_Changes", "Pct_Shipped", "Pct_Processing", "Pct_Cancelled",
    "Avg_Cart_Size", "Max_Cart_Size", "Std_Cart_Size", "Age",
]


def _prepare(features: CLVFeatures) -> pd.DataFrame:
    df = pd.DataFrame([features.model_dump()])
    df = df.reindex(columns=FEATURE_ORDER, fill_value=0)
    try:
        scaler = load_artifact("clv_scaler_20260218_212141.pkl", [SCALERS_DIR])
        import numpy as np
        scaled = scaler.transform(df)
        return pd.DataFrame(scaled, columns=FEATURE_ORDER)
    except Exception:
        return df


@router.post("/predict", response_model=PredictionResponse, summary="Predict customer lifetime value")
async def predict_clv(
    features: CLVFeatures,
    model: str = Query("lightgbm", description="Model: lightgbm | xgboost | rf | ridge"),
):
    """
    Predicts the estimated total lifetime value (in $) for a customer.
    model=lightgbm (default) | xgboost | rf | ridge
    """
    try:
        X = _prepare(features)
        model_map = {
            "lightgbm": ("clv_lightgbm", "LightGBM"),
            "xgboost":  ("clv_xgboost",  "XGBoost"),
            "rf":       ("clv_rf",        "Random Forest"),
            "ridge":    ("clv_ridge",     "Ridge Regression"),
        }
        key, label = model_map.get(model, ("clv_lightgbm", "LightGBM"))
        m = load_artifact(MODEL_REGISTRY[key])
        prediction = float(m.predict(X)[0])
        tier = "High Value" if prediction > 500 else "Mid Value" if prediction > 200 else "Low Value"
        return PredictionResponse(
            prediction=round(prediction, 2),
            model_used=label,
            model_version="20260218_212141",
            extra={"value_tier": tier, "recommended_action": f"This customer is in the {tier} segment — allocate marketing budget accordingly."},
        )
    except Exception as exc:
        logger.error(f"CLV prediction error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/batch", response_model=BatchPredictionResponse, summary="Batch CLV prediction")
async def batch_clv(records: List[CLVFeatures]):
    """Predict CLV for multiple customers."""
    try:
        model = load_artifact(MODEL_REGISTRY["clv_lightgbm"])
        dfs = [pd.DataFrame([r.model_dump()]).reindex(columns=FEATURE_ORDER, fill_value=0) for r in records]
        X = pd.concat(dfs, ignore_index=True)
        preds = model.predict(X).tolist()
        results = [{"index": i, "clv": round(p, 2), "tier": "High" if p > 500 else "Medium" if p > 200 else "Low"}
                   for i, p in enumerate(preds)]
        return BatchPredictionResponse(predictions=results, total=len(results), model_used="LightGBM")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/metrics", response_model=MetricsResponse, summary="CLV model metrics")
async def clv_metrics():
    """Return evaluation metrics for all CLV models."""
    lgbm_meta = load_metadata("clv_lightgbm")
    xgb_meta = load_metadata("clv_xgboost")
    rf_meta = load_metadata("clv_rf")
    ridge_meta = load_metadata("clv_ridge")

    return MetricsResponse(
        model_key="clv",
        model_name="LightGBM CLV Predictor",
        framework="LightGBM / XGBoost / Random Forest / Ridge",
        metrics=lgbm_meta.get("metrics", {"r2": 0.998, "mape": 3.35, "rmse": 133.6, "mae": 95.0}),
        metadata={
            "all_models": {
                "LightGBM": lgbm_meta.get("metrics", {}),
                "XGBoost": xgb_meta.get("metrics", {}),
                "RandomForest": rf_meta.get("metrics", {}),
                "Ridge": ridge_meta.get("metrics", {}),
            },
            "training_samples": lgbm_meta.get("n_samples_train", 69392),
            "n_features": lgbm_meta.get("n_features", 36),
        },
    )


@router.get("/model-comparison", summary="Compare CLV model performances")
async def clv_model_comparison():
    """Return side-by-side metrics for all 4 CLV regression models."""
    csv_path = MODELS_DIR / "clv_model_comparison_20260218_212141.csv"
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        return {"comparison": df.to_dict(orient="records")}

    # Fallback from metadata
    models = ["clv_lightgbm", "clv_xgboost", "clv_rf", "clv_ridge"]
    comparison = []
    for key in models:
        meta = load_metadata(key)
        comparison.append({
            "model": meta.get("model_name", key),
            **meta.get("metrics", {}),
        })
    return {"comparison": comparison}
