"""Recommendation schemas."""
from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    user_id: int = Field(..., example=101, description="Numeric user ID")
    top_n: int = Field(default=5, ge=1, le=20, example=5)


class SVDRecommendationRequest(BaseModel):
    user_id: int = Field(..., example=101)
    top_n: int = Field(default=5, ge=1, le=20)
