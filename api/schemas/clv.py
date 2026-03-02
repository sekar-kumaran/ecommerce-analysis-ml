"""CLV Prediction schemas.

Field names match the 36-feature training set exactly
(clv_scaler_20260218_212141.pkl  feature_names_in_).
Leakage columns excluded from training: Total_Spend, Historical_Spend,
Recent_Spend, Monetary_Score (all direct components of Customer_LTV).
"""
from pydantic import BaseModel, Field


class CLVFeatures(BaseModel):
    # --- Core order metrics (required) ---
    Transaction_Count: float = Field(..., example=12.0)
    Avg_Order_Value: float = Field(..., example=70.87)
    Frequency: float = Field(..., example=1.2)
    Customer_Tenure_Days: float = Field(..., example=365.0)

    # --- Order value stats ---
    Std_Order_Value: float = Field(default=20.0, example=20.0)
    Order_Value_CV: float = Field(default=0.28, example=0.28)
    Avg_Cart_Size: float = Field(default=2.0, example=2.0)
    Max_Cart_Size: float = Field(default=5.0, example=5.0)
    Std_Cart_Size: float = Field(default=1.0, example=1.0)

    # --- Recency / time signals ---
    Recency_Days: float = Field(default=30.0, example=30.0)
    Transactions_Per_Month: float = Field(default=1.0, example=1.0)
    Avg_Days_Between_Purchases: float = Field(default=30.0, example=30.0)
    Recency_Score: float = Field(default=3.0, example=3.0)
    Frequency_Score: float = Field(default=3.0, example=3.0)
    RFM_Score: float = Field(default=9.0, example=9.0)
    Recent_Txn_Count: float = Field(default=3.0, example=3.0)
    Historical_Txn_Count: float = Field(default=9.0, example=9.0)
    Purchase_Velocity_Ratio: float = Field(default=1.0, example=1.0)
    Spending_Velocity_Ratio: float = Field(default=1.0, example=1.0)

    # --- Time-of-purchase preferences ---
    Preferred_Hour: float = Field(default=14.0, example=14.0)
    Weekend_Purchase_Pct: float = Field(default=0.25, example=0.25)
    Preferred_Day_Encoded: float = Field(default=2.0, example=2.0)

    # --- Product diversity ---
    Unique_Categories: float = Field(default=4.0, example=4.0)
    Category_Entropy: float = Field(default=1.5, example=1.5)
    Unique_Brands: float = Field(default=3.0, example=3.0)

    # --- Rating history ---
    Avg_Rating: float = Field(default=4.0, example=4.0)
    Std_Rating: float = Field(default=0.5, example=0.5)
    Min_Rating: float = Field(default=3.0, example=3.0)
    Max_Rating: float = Field(default=5.0, example=5.0)
    Is_Satisfied_Customer: int = Field(default=1, example=1)

    # --- Behaviour changes ---
    Payment_Method_Changes: float = Field(default=0.0, example=0.0)
    Shipping_Method_Changes: float = Field(default=0.0, example=0.0)
    Pct_Shipped: float = Field(default=0.80, example=0.80)
    Pct_Processing: float = Field(default=0.15, example=0.15)
    Pct_Cancelled: float = Field(default=0.05, example=0.05)

    # --- Demographics ---
    Age: float = Field(default=35.0, example=35.0)
