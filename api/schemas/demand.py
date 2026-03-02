"""Demand Forecasting schemas."""
from typing import List
from pydantic import BaseModel, ConfigDict, Field


class ForecastRequest(BaseModel):
    steps: int = Field(default=30, ge=1, le=365, example=30, description="Number of periods to forecast")
    product_id: str = Field(default="ALL", example="PROD_001")


class ForecastPoint(BaseModel):
    period: int
    forecast: float
    lower_bound: float = 0.0
    upper_bound: float = 0.0


class ForecastResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    product_id: str
    model_used: str
    steps: int
    forecasts: List[ForecastPoint]
    mape: float
