"""Fraud Detection schemas.

Field names match the 61-feature training set exactly
(fraud_scaler_20260220_202726.pkl  feature_names_in_).
Only the most actionable fields are required; all others default to 0.
"""
from pydantic import BaseModel, Field


class FraudFeatures(BaseModel):
    # --- Transaction-level (required) ---
    Amount: float = Field(..., example=249.99, description="Transaction amount ($)")
    Age: float = Field(default=35.0, example=35.0, description="Customer age")
    Total_Amount: float = Field(default=249.99, example=249.99)
    Ratings: float = Field(default=4.0, example=4.0)
    Hour: float = Field(default=12.0, ge=0, le=23, example=14.0)
    IsWeekend: int = Field(default=0, example=0)
    DayOfMonth: float = Field(default=15.0, example=15.0)
    DaysSinceFirstPurchase: float = Field(default=180.0, example=180.0)
    Quarter: float = Field(default=2.0, example=2.0)

    # --- Behavioural ratios ---
    Amount_vs_Avg_Ratio: float = Field(default=1.0, example=1.0)
    Cart_Size_vs_Avg_Ratio: float = Field(default=1.0, example=1.0)
    Purchase_Velocity_Ratio: float = Field(default=1.0, example=1.0)
    Spending_Velocity_Ratio: float = Field(default=1.0, example=1.0)

    # --- Order history aggregates ---
    Transaction_Count: float = Field(default=10.0, example=10.0)
    Avg_Order_Value: float = Field(default=80.0, example=80.0)
    Std_Order_Value: float = Field(default=20.0, example=20.0)
    Order_Value_CV: float = Field(default=0.25, example=0.25)
    Avg_Cart_Size: float = Field(default=2.0, example=2.0)
    Max_Cart_Size: float = Field(default=5.0, example=5.0)
    Std_Cart_Size: float = Field(default=1.0, example=1.0)
    Pct_Cancelled: float = Field(default=0.05, example=0.05)
    Pct_Shipped: float = Field(default=0.80, example=0.80)
    Pct_Processing: float = Field(default=0.15, example=0.15)
    Total_Purchases_numeric: float = Field(default=10.0, example=10.0)

    # --- Recency / frequency / tenure ---
    Frequency: float = Field(default=1.0, example=1.0)
    Recency_Days: float = Field(default=30.0, example=30.0)
    Customer_Tenure_Days: float = Field(default=365.0, example=365.0)
    Transactions_Per_Month: float = Field(default=1.0, example=1.0)
    Avg_Days_Between_Purchases: float = Field(default=30.0, example=30.0)
    Days_Since_Customer_Last_Purchase: float = Field(default=30.0, example=30.0)
    Transaction_Days_Since_First_Purchase: float = Field(default=180.0, example=180.0)
    Is_First_Transaction: int = Field(default=0, example=0)
    Recent_Txn_Count: float = Field(default=3.0, example=3.0)
    Historical_Txn_Count: float = Field(default=7.0, example=7.0)

    # --- RFM composite scores ---
    Recency_Score: float = Field(default=3.0, example=3.0)
    Frequency_Score: float = Field(default=3.0, example=3.0)
    RFM_Score: float = Field(default=9.0, example=9.0)

    # --- Ratings history ---
    Avg_Rating: float = Field(default=4.0, example=4.0)
    Std_Rating: float = Field(default=0.5, example=0.5)
    Min_Rating: float = Field(default=3.0, example=3.0)
    Max_Rating: float = Field(default=5.0, example=5.0)
    Rating_Consistency_Score: float = Field(default=0.8, example=0.8)
    Is_Satisfied_Customer: int = Field(default=1, example=1)
    Customer_Satisfaction_Flag: int = Field(default=1, example=1)

    # --- Category / brand diversity ---
    Unique_Categories: float = Field(default=3.0, example=3.0)
    Category_Entropy: float = Field(default=1.5, example=1.5)
    Unique_Brands: float = Field(default=3.0, example=3.0)
    High_Category_Diversity: int = Field(default=0, example=0)
    Brand_Diversity_Score: float = Field(default=0.5, example=0.5)
    Category_Exploration_Score: float = Field(default=0.5, example=0.5)

    # --- Payment / shipping behaviour ---
    Payment_Method_Changes: float = Field(default=0.0, example=0.0)
    Shipping_Method_Changes: float = Field(default=0.0, example=0.0)
    Is_Favorite_Category: int = Field(default=1, example=1)
    Is_Preferred_Payment: int = Field(default=1, example=1)
    Is_Preferred_Shipping: int = Field(default=1, example=1)
    Weekend_Preference_Match: int = Field(default=0, example=0)
    Weekend_Purchase_Pct: float = Field(default=0.25, example=0.25)
    Preferred_Hour: float = Field(default=14.0, example=14.0)
    Preferred_Day_Encoded: float = Field(default=2.0, example=2.0)

    # --- Engagement / loyalty ---
    Customer_Engagement_Score: float = Field(default=0.5, example=0.5)
    Repeat_Buyer_Score: float = Field(default=0.5, example=0.5)
