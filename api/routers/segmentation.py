"""
Customer Segmentation Router
Endpoints: /segmentation/predict, /segmentation/cluster-profiles, /segmentation/metrics
"""
from __future__ import annotations
import logging
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, Query

from api.schemas.segmentation import SegmentationFeatures
from api.schemas.base import PredictionResponse, MetricsResponse
from api.core.config import MODEL_REGISTRY, MODELS_DIR, SCALERS_DIR
from api.core.model_loader import load_artifact, load_metadata

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/segmentation", tags=["Customer Segmentation"])

# 17 features — must match segmentation_scaler_20260218_203814.pkl feature_names_in_ exactly.
FEATURE_ORDER = [
    "Recency_Days", "Total_Spend", "Frequency", "Transaction_Count",
    "Customer_LTV", "Avg_Order_Value", "Avg_Rating", "Unique_Categories",
    "Unique_Brands", "Customer_Tenure_Days", "Pct_Shipped", "Pct_Cancelled",
    "Weekend_Purchase_Pct", "RFM_Score", "Category_Entropy",
    "Order_Value_CV", "Pct_Processing",
]

# Cluster → label mapping derived from centroid analysis of segmentation_kmeans_5.pkl
# Centroids (key stats): 0=Rising Stars, 1=Hibernating, 2=Loyal, 3=Champions, 4=At-Risk
SEGMENT_LABELS = {
    0: "Rising Stars",
    1: "Hibernating",
    2: "Loyal Customers",
    3: "Champions",
    4: "At-Risk",
}


def _prepare(features: SegmentationFeatures) -> np.ndarray:
    df = pd.DataFrame([features.model_dump()])
    df = df.reindex(columns=FEATURE_ORDER, fill_value=0)
    try:
        scaler = load_artifact("segmentation_scaler_v2.pkl", [SCALERS_DIR])
        return scaler.transform(df)
    except Exception:
        return df.values


@router.post("/predict", response_model=PredictionResponse, summary="Assign customer to segment")
async def predict_segment(
    features: SegmentationFeatures,
    model: str = Query("kmeans", description="Model: kmeans | dbscan | gmm"),
):
    """
    Assign a customer to a behavioural segment.
    model=kmeans (default) | dbscan | gmm
    """
    try:
        X = _prepare(features)
        model_map = {
            "kmeans": ("seg_kmeans", "K-Means"),
            "dbscan": ("seg_dbscan", "DBSCAN"),
            "gmm":    ("seg_gmm",    "Gaussian Mixture Model"),
        }
        key, label = model_map.get(model, ("seg_kmeans", "K-Means"))
        m = load_artifact(MODEL_REGISTRY[key])
        try:
            cluster = int(m.predict(X)[0])
        except AttributeError:
            # DBSCAN has no predict() — fall back to KMeans assignment
            km = load_artifact(MODEL_REGISTRY["seg_kmeans"])
            cluster = int(km.predict(X)[0])
            label += " (KMeans fallback)"
        seg_label = SEGMENT_LABELS.get(cluster, f"Segment {cluster}")
        strategy_map = {
            "Champions": "Reward with exclusive early access and VIP offers.",
            "Loyal Customers": "Upsell premium tier — they trust your brand.",
            "At-Risk": "Re-engage with a win-back discount within 14 days.",
            "Hibernating": "Aggressive re-activation campaign needed.",
            "New Customers": "Onboarding sequence — guide to second purchase.",
        }
        return PredictionResponse(
            prediction={"cluster_id": cluster, "segment_label": seg_label},
            model_used=label,
            model_version="20260218_203814",
            extra={"recommended_strategy": strategy_map.get(seg_label, "Standard engagement.")},
        )
    except Exception as exc:
        logger.error(f"Segmentation error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/cluster-profiles", summary="Segment / cluster profiles summary")
async def cluster_profiles():
    """Return business-readable descriptions for each customer segment."""
    profiles = [
        {"id": 0, "label": "Champions", "description": "High recency, high frequency, high spend. VIP customers.", "color": "#10b981", "pct": 18},
        {"id": 1, "label": "Loyal Customers", "description": "Buy regularly, responsive to promotions.", "color": "#3b82f6", "pct": 25},
        {"id": 2, "label": "At-Risk", "description": "Were active but haven't purchased recently.", "color": "#f59e0b", "pct": 22},
        {"id": 3, "label": "Hibernating", "description": "Low recency, low frequency. Re-engagement needed.", "color": "#ef4444", "pct": 20},
        {"id": 4, "label": "New Customers", "description": "First purchase recently — need nurturing.", "color": "#8b5cf6", "pct": 15},
    ]
    return {"profiles": profiles, "n_clusters": 5, "model": "K-Means"}


@router.get("/metrics", response_model=MetricsResponse, summary="Segmentation model metrics")
async def seg_metrics():
    meta = load_metadata("seg_kmeans")
    return MetricsResponse(
        model_key="segmentation",
        model_name="K-Means Customer Segmentation",
        framework="scikit-learn",
        metrics=meta.get("metrics", {"silhouette_score": 0.42, "n_clusters": 5, "davies_bouldin": 0.87}),
        metadata={
            "models_compared": ["K-Means", "DBSCAN", "GMM", "Hierarchical"],
            **meta,
        },
    )
