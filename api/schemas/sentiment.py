"""Sentiment Analysis schemas."""
from pydantic import BaseModel, ConfigDict, Field


class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=3, max_length=2000, example="This product exceeded my expectations!")


class SentimentResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    text: str
    sentiment: str           # positive / neutral / negative
    confidence: float
    model_used: str
