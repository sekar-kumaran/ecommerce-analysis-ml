"""
Models Info Router — catalogue / registry of all saved models
Endpoints: /models/list, /models/{key}/info, /models/artifacts, /models/all-metrics
"""
from __future__ import annotations
import os
from datetime import datetime
from typing import Optional
from fastapi import APIRouter

from api.core.config import MODEL_REGISTRY, METADATA_REGISTRY, MODELS_DIR, SCALERS_DIR, ENCODERS_DIR
from api.core.model_loader import load_metadata, list_available_artifacts

router = APIRouter(prefix="/models", tags=["Model Registry"])

# Human-readable metadata for each model group
MODEL_CATALOGUE = [
    {
        "group": "churn",
        "title": "Churn Prediction",
        "models": ["churn_widedeep", "churn_xgboost", "churn_lightgbm"],
        "best_model": "Wide&Deep",
        "metrics": {"roc_auc": 0.896, "f1_score": 0.877},
        "framework": "TensorFlow / XGBoost / LightGBM",
        "n_features": 34,
        "training_date": "2026-02-18",
        "description": "Predicts 90-day customer churn probability.",
    },
    {
        "group": "clv",
        "title": "Customer Lifetime Value",
        "models": ["clv_lightgbm", "clv_xgboost", "clv_rf", "clv_ridge"],
        "best_model": "LightGBM",
        "metrics": {"r2": 0.998, "mape": 3.35},
        "framework": "LightGBM / XGBoost / sklearn",
        "n_features": 36,
        "training_date": "2026-02-18",
        "description": "Predicts total expected revenue per customer.",
    },
    {
        "group": "recommendations",
        "title": "Product Recommendations",
        "models": ["rec_svd", "rec_ncf"],
        "best_model": "SVD",
        "metrics": {"precision_at_5": 0.312, "ndcg_at_5": 0.334},
        "framework": "Surprise / TensorFlow NCF",
        "n_features": 0,
        "training_date": "2026-02-18",
        "description": "Collaborative-filtering personalised product recommendations.",
    },
    {
        "group": "fraud",
        "title": "Fraud Detection",
        "models": ["fraud_xgboost", "fraud_isoforest", "fraud_autoencoder"],
        "best_model": "XGBoost",
        "metrics": {"accuracy": 0.961, "auc": 0.947},
        "framework": "XGBoost / sklearn / Keras",
        "n_features": 10,
        "training_date": "2026-02-20",
        "description": "Real-time anomalous transaction detection.",
    },
    {
        "group": "segmentation",
        "title": "Customer Segmentation",
        "models": ["seg_kmeans", "seg_dbscan", "seg_gmm"],
        "best_model": "K-Means",
        "metrics": {"silhouette_score": 0.42, "n_clusters": 5},
        "framework": "scikit-learn",
        "n_features": 8,
        "training_date": "2026-02-18",
        "description": "RFM-based behavioural customer clustering.",
    },
    {
        "group": "demand",
        "title": "Demand Forecasting",
        "models": ["forecast_sarima", "forecast_holtwinters", "forecast_lightgbm", "forecast_lstm"],
        "best_model": "LightGBM",
        "metrics": {"mape": 8.93, "r2": 0.893},
        "framework": "statsmodels / LightGBM / TensorFlow",
        "n_features": 0,
        "training_date": "2026-02-20",
        "description": "Daily/weekly product demand time-series forecasting.",
    },
    {
        "group": "sentiment",
        "title": "Sentiment Analysis",
        "models": ["sentiment_lr", "sentiment_lstm"],
        "best_model": "LSTM",
        "metrics": {"accuracy": 0.91, "f1_macro": 0.89},
        "framework": "scikit-learn TF-IDF / TensorFlow LSTM",
        "n_features": 0,
        "training_date": "2026-02-20",
        "description": "Product review positive/neutral/negative classification.",
    },
]


@router.get("/list", summary="List all model groups")
async def list_models():
    """Return the full model catalogue with key metrics."""
    return {"models": MODEL_CATALOGUE, "total_groups": len(MODEL_CATALOGUE)}


@router.get("/artifacts", summary="List raw artifact files on disk")
async def list_artifacts():
    """Return file listings for models, scalers, and encoders directories."""
    return list_available_artifacts()


@router.get("/{group}/info", summary="Get info for a model group")
async def model_info(group: str):
    """Return detailed information for a specific model group."""
    entry = next((m for m in MODEL_CATALOGUE if m["group"] == group), None)
    if not entry:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Model group '{group}' not found")

    # Enrich with file metadata if files exist
    enriched_models = []
    for key in entry["models"]:
        filename = MODEL_REGISTRY.get(key, "")
        filepath = MODELS_DIR / filename
        file_info = {
            "key": key,
            "filename": filename,
            "exists": filepath.exists(),
            "size_kb": round(filepath.stat().st_size / 1024, 1) if filepath.exists() else 0,
            "last_modified": datetime.fromtimestamp(filepath.stat().st_mtime).isoformat() if filepath.exists() else None,
        }
        enriched_models.append(file_info)

    return {**entry, "model_files": enriched_models}


@router.get("/all-metrics", summary="Aggregate metrics across all models")
async def all_metrics():
    """Return a consolidated metrics summary for the entire platform."""
    return {
        "platform_summary": {
            "total_model_groups": len(MODEL_CATALOGUE),
            "total_model_files": len(MODEL_REGISTRY),
            "domains_covered": 7,
        },
        "model_metrics": {m["group"]: m["metrics"] for m in MODEL_CATALOGUE},
    }
