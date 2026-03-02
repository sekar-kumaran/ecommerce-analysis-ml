# Ecommerce Analytics Platform — Model Training Details

> Source of truth for every saved artifact, its exact feature contract, scaler format, and known API bugs.  
> Used by the FastAPI routers to align inference with training.

---

## Table of Contents
1. [Churn Prediction](#1-churn-prediction)
2. [Customer Lifetime Value (CLV)](#2-customer-lifetime-value-clv)
3. [Fraud Detection](#3-fraud-detection)
4. [Customer Segmentation](#4-customer-segmentation)
5. [Demand Forecasting](#5-demand-forecasting)
6. [Sentiment Analysis](#6-sentiment-analysis)
7. [Recommendation Systems](#7-recommendation-systems)
8. [Bug Registry & Fixes](#8-bug-registry--fixes)

---

## 1. Churn Prediction

**Notebook:** `notebooks/06a_churn_prediction_v2.ipynb`

### Training Summary
| Item | Value |
|------|-------|
| Target | Binary — `Churn` (1 = churned in next 90 days) |
| Definition | `Recency_Days > 60` |
| Algorithm | LightGBM, XGBoost, Wide & Deep neural net |
| Train/test split | 80/20 stratified |
| Imbalance handling | SMOTE (minority → 80% of majority) + `class_weight='balanced'` |
| Scaler | `RobustScaler` (median-centred, IQR-scaled) |
| CV folds | 5-fold StratifiedKFold |
| Performance | ROC-AUC ≈ 0.896, F1 ≈ 0.877 |

### Leakage Features Removed Before Training
The following are **excluded** from model input because they directly encode `Recency_Days` (the label definition):
- `Recency_Days`, `Recency_Score`, `RFM_Score`
- `Purchase_Velocity_Ratio`, `Spending_Velocity_Ratio`
- All columns matching keywords: `Recency`, `Recent`, `Last_Purchase`, `Days_Since`

### Exact Feature Order (34 features)
```python
CHURN_FEATURE_ORDER = [
    "Transaction_Count", "Total_Spend", "Avg_Order_Value", "Std_Order_Value",
    "Frequency", "Customer_Tenure_Days", "Transactions_Per_Month", "Customer_LTV",
    "Avg_Days_Between_Purchases", "Order_Value_CV", "Frequency_Score", "Monetary_Score",
    "Historical_Txn_Count", "Historical_Spend", "Preferred_Hour", "Weekend_Purchase_Pct",
    "Preferred_Day_Encoded", "Unique_Categories", "Category_Entropy", "Unique_Brands",
    "Avg_Rating", "Std_Rating", "Min_Rating", "Max_Rating", "Is_Satisfied_Customer",
    "Payment_Method_Changes", "Shipping_Method_Changes", "Pct_Shipped", "Pct_Processing",
    "Pct_Cancelled", "Avg_Cart_Size", "Max_Cart_Size", "Std_Cart_Size", "Age",
]
```

### Saved Artifacts
| File | Location | Format | Note |
|------|----------|--------|------|
| `churn_lightgbm_20260218_184733.pkl` | `artifacts/models/` | joblib | LGBMClassifier |
| `churn_xgboost_20260218_184733.pkl` | `artifacts/models/` | joblib | XGBClassifier |
| `churn_widedeep_20260218_184733.keras` | `artifacts/models/` | Keras | Wide & Deep NN |
| `churn_scaler_20260218_184733.pkl` | `artifacts/scalers/` | joblib | **DICT** `{'scaler': RobustScaler, 'feature_names': [...], 'removed_features': [...]}` |
| `churn_deployment_package_20260218_184733.json` | `artifacts/models/` | JSON | Full deployment spec |

### ⚠️ Critical Bug — Scaler is a Dict
The scaler was saved as:
```python
joblib.dump({'scaler': scaler, 'feature_names': feature_names,
             'removed_features': leakage_features}, scaler_path)
```
**The router MUST unwrap it:**
```python
scaler_pkg = load_artifact("churn_scaler_20260218_184733.pkl", [SCALERS_DIR])
scaler = scaler_pkg['scaler'] if isinstance(scaler_pkg, dict) else scaler_pkg
X_scaled = scaler.transform(df)
```

---

## 2. Customer Lifetime Value (CLV)

**Notebook:** `notebooks/06d_sales_clv_prediction_v2.ipynb`

### Training Summary
| Item | Value |
|------|-------|
| Target | `Customer_LTV` — predicted total lifetime revenue ($) |
| Algorithms | Ridge Regression, Random Forest, XGBoost, LightGBM |
| Train/test split | 80/20 stratified by LTV decile |
| Imbalance handling | N/A (regression task) |
| Scaler | `StandardScaler` — **plain sklearn object, NOT a dict** |
| Best model | LightGBM (R² ≈ 0.998, MAPE ≈ 3.35%) |

### Leakage Features Removed Before Training
| Column | Reason |
|--------|--------|
| `Total_Spend` | IS the target — perfect leakage |
| `Historical_Spend` | Subset of total spend |
| `Recent_Spend` | Subset of total spend |
| `Monetary_Score` | RFM score derived purely from spend |
| `Customer_ID` | Identifier |
| `Customer_LTV` | Target column |
| Date/text columns | Non-numeric, not encoded |

### Exact Feature Order (36 features)
```python
CLV_FEATURE_ORDER = [
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
```

### Saved Artifacts
| File | Location | Format |
|------|----------|--------|
| `clv_lightgbm_20260218_212141.pkl` | `artifacts/models/` | joblib |
| `clv_xgboost_20260218_212141.pkl` | `artifacts/models/` | joblib |
| `clv_random_forest_20260218_212141.pkl` | `artifacts/models/` | joblib |
| `clv_ridge_regression_20260218_212141.pkl` | `artifacts/models/` | joblib |
| `clv_scaler_20260218_212141.pkl` | `artifacts/scalers/` | joblib | Plain `StandardScaler` |
| `clv_features.json` | `artifacts/models/` | JSON | 36-feature list |

### ⚠️ Critical Bug — Wrong FEATURE_ORDER in Router
Router `clv.py` had only 12 features. Models expect **36**. All missing features were zero-filled BUT the zero-filled df was passed directly to the model without correcting FEATURE_ORDER → `ValueError: X has 12 features, expected 36`.

---

## 3. Fraud Detection

**Notebook:** `notebooks/06e_fraud_detection_v2.ipynb`

### Training Summary
| Item | Value |
|------|-------|
| Target | Binary — `Is_Fraud` (1 = fraudulent transaction) |
| Label method | Rule-based: low-rating+high-value, problem-order+high-value, velocity-spike+unusual-hour |
| Algorithms | Isolation Forest (unsupervised), XGBoost + SMOTE, Autoencoder (deep learning) |
| Train/test split | 80/20 stratified |
| Imbalance handling | SMOTE for XGBoost; contamination tuning for Isolation Forest |
| Scaler | `StandardScaler` — **plain sklearn object** |
| Performance | XGBoost: Precision ≈ 0.918, Recall ≈ 0.xxx, F1 ≈ 0.923 |

### Leakage Features Excluded (rule-source columns)
- `Low_Rating_High_Value` (Rule 1 source)
- `Is_Problem_Order`, `Is_High_Value_Txn` (Rule 2 sources)
- `Is_Velocity_Spike`, `Is_Unusual_Hour` (Rule 3 sources)

### Exact Feature Order (61 features)
```python
FRAUD_FEATURE_ORDER = [
    # Transaction-level
    "Age", "Amount", "Total_Amount", "Ratings", "Hour", "IsWeekend",
    "DayOfMonth", "DaysSinceFirstPurchase", "Quarter",
    # Behavioural ratios
    "Amount_vs_Avg_Ratio", "Cart_Size_vs_Avg_Ratio",
    "Purchase_Velocity_Ratio", "Spending_Velocity_Ratio",
    # Order history aggregates
    "Transaction_Count", "Avg_Order_Value", "Std_Order_Value",
    "Order_Value_CV", "Avg_Cart_Size", "Max_Cart_Size", "Std_Cart_Size",
    "Pct_Cancelled", "Pct_Shipped", "Pct_Processing", "Total_Purchases_numeric",
    # RFM / recency / frequency
    "Frequency", "Recency_Days", "Customer_Tenure_Days",
    "Transactions_Per_Month", "Avg_Days_Between_Purchases",
    "Days_Since_Customer_Last_Purchase",
    "Transaction_Days_Since_First_Purchase", "Is_First_Transaction",
    "Recent_Txn_Count", "Historical_Txn_Count",
    "Recency_Score", "Frequency_Score", "RFM_Score",
    # Ratings
    "Avg_Rating", "Std_Rating", "Min_Rating", "Max_Rating",
    "Rating_Consistency_Score", "Is_Satisfied_Customer", "Customer_Satisfaction_Flag",
    # Category/brand diversity
    "Unique_Categories", "Category_Entropy", "Unique_Brands",
    "High_Category_Diversity", "Brand_Diversity_Score", "Category_Exploration_Score",
    # Payment/shipping patterns
    "Payment_Method_Changes", "Shipping_Method_Changes",
    "Is_Favorite_Category", "Is_Preferred_Payment", "Is_Preferred_Shipping",
    "Weekend_Preference_Match", "Weekend_Purchase_Pct",
    "Preferred_Hour", "Preferred_Day_Encoded",
    # Engagement
    "Customer_Engagement_Score", "Repeat_Buyer_Score",
]
```

### Saved Artifacts
| File | Location | Format |
|------|----------|--------|
| `xgboost_fraud_20260220_202726.pkl` | `artifacts/models/` | joblib |
| `isolation_forest_20260220_202726.pkl` | `artifacts/models/` | joblib |
| `autoencoder_fraud_20260220_202726.h5` | `artifacts/models/` | Keras h5 |
| `autoencoder_threshold_20260220_202726.pkl` | `artifacts/models/` | joblib |
| `fraud_scaler_20260220_202726.pkl` | `artifacts/scalers/` | joblib | Plain `StandardScaler` with 61 features |

### ⚠️ Critical Bug — Wrong FEATURE_ORDER in Router
Router `fraud.py` had only 10 features. Model expects **61**. The reindex produced a 10-column DataFrame and then scaler raised a mismatch error silently caught by the fallback → wrong predictions.

---

## 4. Customer Segmentation

**Notebook:** `notebooks/06c_customer_segmentation_v2.ipynb`

### Training Summary
| Item | Value |
|------|-------|
| Task | Unsupervised clustering (no target label) |
| Algorithms | K-Means, DBSCAN, GMM (Gaussian Mixture Model), Hierarchical |
| Optimal K | Selected by silhouette score across K=2..10 |
| Scaler | `StandardScaler` — **plain sklearn object** |
| Input data | `customer_features_enriched.csv` (1 row per customer) |

### Exact Feature Order (17 features)
```python
SEG_FEATURE_ORDER = [
    "Recency_Days", "Total_Spend", "Frequency", "Transaction_Count",
    "Customer_LTV", "Avg_Order_Value", "Avg_Rating", "Unique_Categories",
    "Unique_Brands", "Customer_Tenure_Days", "Pct_Shipped", "Pct_Cancelled",
    "Weekend_Purchase_Pct", "RFM_Score", "Category_Entropy",
    "Order_Value_CV", "Pct_Processing",
]
```

### Saved Artifacts
| File | Location | Format |
|------|----------|--------|
| `segmentation_kmeans_20260218_203814.pkl` | `artifacts/models/` | joblib |
| `segmentation_dbscan_20260218_203814.pkl` | `artifacts/models/` | joblib |
| `segmentation_gmm_20260218_203814.pkl` | `artifacts/models/` | joblib |
| `segmentation_hierarchical_20260218_203814.pkl` | `artifacts/models/` | joblib |
| `segmentation_scaler_20260218_203814.pkl` | `artifacts/scalers/` | joblib | Plain `StandardScaler` with 17 features |

### ⚠️ Critical Bug — Wrong FEATURE_ORDER in Router
Router `segmentation.py` had only 8 features. Model expects **17**. `reindex` filled the missing 9 with zeros which distorted cluster assignments.

---

## 5. Demand Forecasting

**Notebook:** `notebooks/06f_demand_forecasting_v2.ipynb`

### Training Summary
| Item | Value |
|------|-------|
| Task | Time-series regression — daily order count |
| Algorithms | Holt-Winters (ETS), SARIMA (1,1,1)×(1,1,1,7), LSTM, LightGBM |
| Split method | Temporal — first 80% of dates train, last 20% test |
| Scaler (LSTM only) | `StandardScaler` for order series normalisation |
| Primary metric | MAPE (scale-independent) |

### LightGBM Feature Order (9 features)
```python
DEMAND_LGBM_FEATURES = [
    "IsWeekend", "DayOfWeek", "Month",
    "Avg_Engagement", "High_Value_Txns",
    "Lag_1", "Lag_3", "Lag_7", "Lag_14",
]
```
**Note:** `Lag_*` = previous day/3-day/7-day/14-day order counts. At inference time with no history, lag values can be filled from the last known demand value or default to 100 (median).

### SARIMA Configuration
- Order: `(1,1,1)` (non-seasonal), `(1,1,1,7)` (seasonal, period=7 days)
- Uses `statsmodels` fitted model — call `.forecast(steps=N)` directly

### Holt-Winters Configuration
- Multiplicative seasonality to capture amplitude-scaling weekly peaks
- Call `.forecast(N)` directly on the fitted model

### LSTM Architecture
- 2 stacked LSTM layers: 64 units → dropout(0.2) → 32 units → dropout(0.2) → Dense(16) → Dense(1)
- Lookback window: **14 days**
- Input scaler: `forecast_lstm_scaler.pkl` (StandardScaler on order series)
- Must inverse_transform outputs before returning

### Saved Artifacts
| File | Location |
|------|----------|
| `forecast_sarima_20260220_204816.pkl` | `artifacts/models/` |
| `forecast_holtwinters_20260220_204816.pkl` | `artifacts/models/` |
| `forecast_lightgbm_20260220_204816.pkl` | `artifacts/models/` |
| `forecast_lstm_20260220_204816.keras` | `artifacts/models/` |
| `forecast_lstm_scaler_20260220_204816.pkl` | `artifacts/scalers/` |

### ⚠️ Critical Bug — LightGBM Sent Wrong Features
Router `demand.py` built `pd.DataFrame({"period": range(1, steps+1)})` but LightGBM expects 9 calendar+lag columns.  
Fix: build a proper feature frame using `datetime.now()` + a default lag value.

---

## 6. Sentiment Analysis

**Notebook:** `notebooks/06g_sentiment_analysis_v2.ipynb`

### Training Summary
| Item | Value |
|------|-------|
| Task | 3-class text classification: Negative / Neutral / Positive |
| Label mapping | Rating 1-2 → Negative (0), Rating 3 → Neutral (1), Rating 4-5 → Positive (2) |
| Algorithms | TF-IDF + Logistic Regression, Bidirectional LSTM |
| Train/test split | 80/20 stratified with class weights for Neutral minority |
| Input | Review text (generated from transaction features + 5% noise) |

### TF-IDF + LR Model (Primary)
- Saved as a **single pipeline object** containing: `TfidfVectorizer` + `LogisticRegression` + `LabelEncoder`
- Call `model.predict_proba([text])[0]` → returns 3-class probabilities
- Class order: `{0: "negative", 1: "neutral", 2: "positive"}`

### LSTM Model
- Bidirectional LSTM, embedding-based
- Requires separate tokenizer: `sentiment_tokenizer.pkl` (in `artifacts/encoders/`)
- Lookback: sequences padded to `MAX_LEN`

### Saved Artifacts
| File | Location | Note |
|------|----------|------|
| `sentiment_tfidf_lr_20260220_211402.pkl` | `artifacts/models/` | Pipeline with vectorizer+LR |
| `sentiment_lstm_20260220_211402.keras` | `artifacts/models/` | Keras LSTM |
| `sentiment_tokenizer_20260220_211402.pkl` | `artifacts/encoders/` | Keras tokenizer for LSTM |

### No Feature Bugs
Sentiment router takes raw text; the saved pipeline handles vectorization internally. ✅

---

## 7. Recommendation Systems

**Notebook:** `notebooks/06b_recommendation_systems_v2.ipynb`

### Training Summary
| Item | Value |
|------|-------|
| Task | Collaborative filtering — top-N item recommendations per user |
| Algorithms | SVD (matrix factorisation), Neural Collaborative Filtering (NCF), Wide & Deep |
| Library (SVD) | `surprise` — SVD object with `.trainset` |
| Inference | `model.predict(user_id, item_id)` → `.est` score |

### Saved Artifacts
| File | Location |
|------|----------|
| `recommendation_svd_20260218_185653.pkl` | `artifacts/models/` |
| `recommendation_ncf_20260218_185653.keras` | `artifacts/models/` |
| `recommendation_item_encoder_20260218_185653.pkl` | `artifacts/encoders/` |
| `recommendation_user_encoder_20260218_185653.pkl` | `artifacts/encoders/` |
| `recommendation_feature_scaler_20260218_185653.pkl` | `artifacts/scalers/` |

### No Feature Bugs
SVD uses user/item IDs directly from the trainset. Router already handles unknown user fallback. ✅

---

## 8. Bug Registry & Fixes

| # | Router | Bug | Fix |
|---|--------|-----|-----|
| 1 | `churn.py` | Scaler saved as `dict` — calling `.transform()` on it crashes silently → predictions are from unscaled data | Unwrap: `pkg['scaler'] if isinstance(pkg, dict)` |
| 2 | `clv.py` | `FEATURE_ORDER` has 12 features; model expects 36 → `ValueError` | Replace FEATURE_ORDER with 36-feature list from scaler |
| 3 | `clv.py` | CLV schema only has 12 fields; missing 24 derived features default to 0 after reindex | Added all 36 fields with `default=0.0` |
| 4 | `fraud.py` | `FEATURE_ORDER` has 10 features; model expects 61 → scaler mismatch caught silently → always predicts 0 | Replace FEATURE_ORDER with 61-feature list |
| 5 | `fraud.py` | Fraud schema only has 10 fields | Added all 61 fields with `default=0.0` |
| 6 | `segmentation.py` | `FEATURE_ORDER` has 8 features; model expects 17 → wrong cluster assignments | Replace FEATURE_ORDER with 17-feature list |
| 7 | `segmentation.py` | Segmentation schema only has 8 fields | Added all 17 fields with `default=0.0` |
| 8 | `demand.py` | LightGBM predict called with `{"period": [...]}` but needs 9 lag+calendar features | Build proper feature frame from `datetime.now()` |
| 9 | `model_loader.py` | No automatic dict-scaler unwrapping | Added `load_scaler()` helper that unwraps dict scalers |

---

## Scaler Save Format Reference

| Model | Scaler File | Format | How to Load |
|-------|------------|--------|-------------|
| Churn | `churn_scaler_*.pkl` | `dict {scaler, feature_names, removed_features}` | `pkg = joblib.load(...); scaler = pkg['scaler']` |
| CLV | `clv_scaler_*.pkl` | Plain `StandardScaler` | `scaler = joblib.load(...)` |
| Fraud | `fraud_scaler_*.pkl` | Plain `StandardScaler` | `scaler = joblib.load(...)` |
| Segmentation | `segmentation_scaler_*.pkl` | Plain `StandardScaler` | `scaler = joblib.load(...)` |
| Demand LSTM | `forecast_lstm_scaler_*.pkl` | Plain `StandardScaler` | `scaler = joblib.load(...)` |
