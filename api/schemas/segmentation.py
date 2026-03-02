"""Segmentation schemas.

Field names match the 17-feature training set exactly
(segmentation_scaler_20260218_203814.pkl  feature_names_in_).
"""
from pydantic import BaseModel, Field


class SegmentationFeatures(BaseModel):
    # --- RFM core (required) ---
    Recency_Days: float = Field(..., example=30.0)
    Total_Spend: float = Field(..., example=850.0)
    Frequency: float = Field(..., example=5.0)

    # --- Volume & value ---
    Transaction_Count: float = Field(default=10.0, example=10.0)
    Customer_LTV: float = Field(default=850.0, example=850.0)
    Avg_Order_Value: float = Field(default=70.0, example=70.0)
    Order_Value_CV: float = Field(default=0.25, example=0.25)

    # --- Customer profile ---
    Avg_Rating: float = Field(default=4.0, example=4.0)
    Unique_Categories: float = Field(default=4.0, example=4.0)
    Unique_Brands: float = Field(default=3.0, example=3.0)
    Customer_Tenure_Days: float = Field(default=365.0, example=365.0)

    # --- Fulfilment stats ---
    Pct_Shipped: float = Field(default=0.80, example=0.80)
    Pct_Cancelled: float = Field(default=0.05, example=0.05)
    Pct_Processing: float = Field(default=0.15, example=0.15)

    # --- Behavioural ---
    Weekend_Purchase_Pct: float = Field(default=0.25, example=0.25)
    RFM_Score: float = Field(default=9.0, example=9.0)
    Category_Entropy: float = Field(default=1.5, example=1.5)
