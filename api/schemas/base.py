"""
Base Pydantic schemas shared across all routers.
"""
from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class PredictionResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    prediction: Any
    confidence: Optional[float] = None
    model_used: str
    model_version: str = "latest"
    timestamp: datetime = Field(default_factory=datetime.now)
    extra: Optional[Dict[str, Any]] = None


class BatchItem(BaseModel):
    features: Dict[str, Any]


class BatchPredictionResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    predictions: List[Dict[str, Any]]
    total: int
    model_used: str
    timestamp: datetime = Field(default_factory=datetime.now)


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)


class MetricsResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model_key: str
    model_name: str
    framework: str
    metrics: Dict[str, Any]
    metadata: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(BaseModel):
    detail: str
    timestamp: datetime = Field(default_factory=datetime.now)
