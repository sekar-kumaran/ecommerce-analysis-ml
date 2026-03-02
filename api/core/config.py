"""
Core configuration for the Ecommerce Analytics Platform API
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODELS_DIR = ARTIFACTS_DIR / "models"
ENCODERS_DIR = ARTIFACTS_DIR / "encoders"
SCALERS_DIR = ARTIFACTS_DIR / "scalers"
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

# API Settings
API_TITLE = "Ecommerce Analytics Platform"
API_DESCRIPTION = """
## Ecommerce Analytics Platform — Multi-Model ML API

A comprehensive machine learning platform providing insights across **7 domains**:

| Domain | Models | Case Study |
|---|---|---|
| Churn Prediction | Wide&Deep, XGBoost, LightGBM, DNN, LSTM | Reduce churn up to 30% |
| Customer Lifetime Value | LightGBM, XGBoost, RF, Ridge | Identify high-value customers |
| Recommendations | NCF, SVD, Wide&Deep | Personalise product discovery |
| Fraud Detection | Autoencoder, Isolation Forest, XGBoost | Flag anomalous transactions |
| Segmentation | K-Means, DBSCAN, GMM, Hierarchical | Behavioural customer clusters |
| Demand Forecasting | LSTM, SARIMA, Holt-Winters, LightGBM | Optimise inventory ordering |
| Sentiment Analysis | LSTM, TF-IDF+LR | Monitor product review quality |
"""
API_VERSION = "2.0.0"

# CORS origins
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:8080",
    "http://127.0.0.1:5500",  # VS Code Live Server
    "null",                    # local HTML file open
    "*",
]

# Model registry — maps model keys to artifact file stems
MODEL_REGISTRY = {
    # Churn
    "churn_widedeep":    "churn_widedeep_20260218_184733.keras",
    "churn_xgboost":     "churn_xgboost_20260218_184733.pkl",
    "churn_lightgbm":    "churn_lightgbm_20260218_184733.pkl",
    # CLV
    "clv_lightgbm":      "clv_lightgbm_20260218_212141.pkl",
    "clv_xgboost":       "clv_xgboost_20260218_212141.pkl",
    "clv_rf":            "clv_random_forest_20260218_212141.pkl",
    "clv_ridge":         "clv_ridge_regression_20260218_212141.pkl",
    # Recommendations
    "rec_svd":           "recommendation_svd_20260218_185653.pkl",
    "rec_ncf":           "recommendation_ncf_20260218_185653.keras",
    # Fraud
    "fraud_xgboost":       "xgboost_fraud_20260220_202726.pkl",
    "fraud_isoforest":     "fraud_isolation_forest.pkl",
    "fraud_isoforest_pca": "fraud_isolation_forest_pca.pkl",
    "fraud_autoencoder":   "autoencoder_fraud_20260220_202726.h5",
    # Segmentation  (v2: properly paired StandardScaler + KMeans k=5)
    "seg_kmeans":        "segmentation_kmeans_v2.pkl",
    "seg_dbscan":        "segmentation_dbscan_20260218_203814.pkl",
    "seg_gmm":           "segmentation_gmm_5.pkl",
    # Demand / Forecasting
    "forecast_sarima":      "forecast_sarima_20260220_204816.pkl",
    "forecast_holtwinters": "forecast_holtwinters_20260220_204816.pkl",
    "forecast_lightgbm":    "forecast_lightgbm_20260220_204816.pkl",
    "forecast_lstm":        "forecast_lstm_20260220_204816.keras",
    # Sentiment
    "sentiment_lr":    "sentiment_tfidf_lr_20260220_211402.pkl",
    "sentiment_lstm":  "sentiment_lstm_20260220_211402.keras",
}

# Metadata registry — maps model keys to their JSON metadata files
METADATA_REGISTRY = {
    "churn_deployment":         "churn_deployment_package_20260218_184733.json",
    "clv_lightgbm":             "clv_lightgbm_metadata_20260218_212141.json",
    "clv_xgboost":              "clv_xgboost_metadata_20260218_212141.json",
    "clv_rf":                   "clv_random_forest_metadata_20260218_212141.json",
    "clv_ridge":                "clv_ridge_regression_metadata_20260218_212141.json",
    "rec_svd":                  "recommendation_svd_metadata_20260218_185653.json",
    "rec_ncf":                  "recommendation_ncf_metadata_20260218_185653.json",
    "fraud_latest":             "fraud_metadata_20260220_202726.json",
    "seg_kmeans":               "segmentation_kmeans_metadata_20260218_203814.json",
    "seg_dbscan":               "segmentation_dbscan_metadata_20260218_203814.json",
    "seg_gmm":                  "segmentation_gmm_metadata_20260218_203814.json",
    "forecast_sarima":          "forecast_sarima_metadata_20260220_204816.json",
    "forecast_holtwinters":     "forecast_holtwinters_metadata_20260220_204816.json",
    "forecast_lightgbm":        "forecast_lightgbm_metadata_20260220_204816.json",
    "forecast_lstm":            "forecast_lstm_metadata_20260220_204816.json",
    "sentiment_lr":             "sentiment_tfidf_lr_metadata_20260220_211402.json",
    "sentiment_lstm":           "sentiment_lstm_metadata_20260220_211402.json",
}

# Case Studies catalogue
CASE_STUDIES = [
    {
        "id": "churn",
        "title": "Customer Churn Prediction",
        "icon": "📉",
        "domain": "Customer Retention",
        "problem": "Identify customers likely to stop purchasing in the next 90 days.",
        "approach": "Ensemble of Wide&Deep neural network, XGBoost, LightGBM trained on 86k customer records with 34 engineered features.",
        "business_value": "Targeted retention campaigns reduce churn by ~30%, saving an estimated $2.1M annually.",
        "metrics": {"roc_auc": 0.896, "precision": 0.812, "recall": 0.954, "f1_score": 0.877},
        "models": ["churn_widedeep", "churn_xgboost", "churn_lightgbm"],
        "notebook": "06a_churn_prediction_v2.ipynb",
        "key_features": ["Transaction_Count", "Total_Spend", "Avg_Days_Between_Purchases", "Category_Entropy", "Pct_Cancelled"],
        "questions": [
            "Which customers are most likely to churn in the next quarter?",
            "What behavioural signals are strongest predictors of churn?",
            "How does cancellation rate influence churn probability?",
            "Which customer tenure groups have the highest churn risk?",
        ],
    },
    {
        "id": "clv",
        "title": "Customer Lifetime Value",
        "icon": "💰",
        "domain": "Revenue Intelligence",
        "problem": "Predict the total revenue a customer will generate over their lifetime.",
        "approach": "Four regression models (LightGBM, XGBoost, Random Forest, Ridge) evaluated via RMSE, MAE, R², MAPE.",
        "business_value": "Focus marketing spend on top 20% CLV customers who deliver 80% of revenue.",
        "metrics": {"r2": 0.998, "mape": 3.35, "rmse": 133.6, "mae": 95.0},
        "models": ["clv_lightgbm", "clv_xgboost", "clv_rf", "clv_ridge"],
        "notebook": "06d_sales_clv_prediction_v2.ipynb",
        "key_features": ["Historical_Spend", "Frequency", "Customer_Tenure_Days", "Avg_Order_Value"],
        "questions": [
            "What is the predicted lifetime value of a new customer after 3 purchases?",
            "How does purchase frequency impact CLV?",
            "Which product categories contribute most to high CLV?",
            "How accurate is CLV prediction within the first 30 days?",
        ],
    },
    {
        "id": "recommendations",
        "title": "Product Recommendations",
        "icon": "🛍️",
        "domain": "Personalisation",
        "problem": "Recommend the next best products for each customer.",
        "approach": "Collaborative filtering via SVD and Neural Collaborative Filtering (NCF) on user–item interaction matrix.",
        "business_value": "Personalised recommendations increase average order value by 15-20% and click-through rate by 35%.",
        "metrics": {"precision_at_5": 0.312, "recall_at_5": 0.289, "ndcg_at_5": 0.334},
        "models": ["rec_svd", "rec_ncf"],
        "notebook": "06b_recommendation_systems_v2.ipynb",
        "key_features": ["user_id", "item_id", "rating", "interaction_count"],
        "questions": [
            "What are the top-5 product recommendations for a given customer?",
            "Which items are frequently bought together (market basket)?",
            "How does purchase history length affect recommendation quality?",
            "Which cold-start strategies work best for new users?",
        ],
    },
    {
        "id": "fraud",
        "title": "Fraud Detection",
        "icon": "🚨",
        "domain": "Risk & Compliance",
        "problem": "Detect anomalous and potentially fraudulent transactions in real time.",
        "approach": "Unsupervised anomaly detection (Autoencoder, Isolation Forest) combined with supervised XGBoost on labelled fraud samples.",
        "business_value": "Catch 96% of fraud at <2% false-positive rate, saving ~$800k in chargebacks per year.",
        "metrics": {"accuracy": 0.961, "f1_score": 0.923, "auc": 0.947, "precision": 0.918},
        "models": ["fraud_xgboost", "fraud_isoforest", "fraud_autoencoder"],
        "notebook": "06e_fraud_detection_v2.ipynb",
        "key_features": ["Transaction_Amount", "Hour_of_Day", "Device_Type", "Payment_Method", "Anomaly_Score"],
        "questions": [
            "Is this transaction fraudulent given amount, time, and device?",
            "What transaction patterns are most associated with fraud?",
            "How does the autoencoder reconstruction error flag anomalies?",
            "What is the ROC-AUC of the ensemble fraud model?",
        ],
    },
    {
        "id": "segmentation",
        "title": "Customer Segmentation",
        "icon": "🧩",
        "domain": "Customer Intelligence",
        "problem": "Group customers into behavioural clusters to tailor marketing strategies.",
        "approach": "Unsupervised clustering using K-Means, DBSCAN, Gaussian Mixture Models, and Hierarchical clustering on RFM + behavioural features.",
        "business_value": "Targeted segment campaigns show 2.5× higher conversion vs. blanket campaigns.",
        "metrics": {"silhouette_kmeans": 0.42, "n_clusters": 5, "davies_bouldin": 0.87},
        "models": ["seg_kmeans", "seg_dbscan", "seg_gmm"],
        "notebook": "06c_customer_segmentation_v2.ipynb",
        "key_features": ["Recency", "Frequency", "Monetary", "Category_Entropy", "Avg_Rating"],
        "questions": [
            "Which cluster does this customer belong to?",
            "What are the spending habits within each segment?",
            "Which segment has the highest churn risk?",
            "How do segments differ in product category preferences?",
        ],
    },
    {
        "id": "demand",
        "title": "Demand Forecasting",
        "icon": "📦",
        "domain": "Supply Chain",
        "problem": "Forecast product demand at daily/weekly granularity to optimise inventory.",
        "approach": "Time-series models: SARIMA, Holt-Winters; ML models: LightGBM, LSTM — compared on MAPE, RMSE.",
        "business_value": "Reduces stockouts by 25% and overstock carrying costs by 18%.",
        "metrics": {"mape": 8.93, "rmse": 245.67, "r2": 0.893},
        "models": ["forecast_sarima", "forecast_holtwinters", "forecast_lightgbm", "forecast_lstm"],
        "notebook": "06f_demand_forecasting_v2.ipynb",
        "key_features": ["date", "product_id", "sales_quantity", "lag_7", "rolling_mean_30"],
        "questions": [
            "What is the forecasted demand over the next 30 days?",
            "Which seasonal patterns most affect weekly demand?",
            "How does the LSTM forecast compare to SARIMA?",
            "Which products have the highest forecast uncertainty?",
        ],
    },
    {
        "id": "sentiment",
        "title": "Sentiment Analysis",
        "icon": "💬",
        "domain": "Voice of Customer",
        "problem": "Classify product reviews as positive, neutral, or negative to monitor brand health.",
        "approach": "TF-IDF + Logistic Regression for interpretable baseline; LSTM for deep sequential text features.",
        "business_value": "Surface product quality issues 2 weeks earlier, improving NPS score by 12 points.",
        "metrics": {"accuracy": 0.91, "f1_macro": 0.89, "precision": 0.90, "recall": 0.88},
        "models": ["sentiment_lr", "sentiment_lstm"],
        "notebook": "06g_sentiment_analysis_v2.ipynb",
        "key_features": ["review_text", "tfidf_features", "sequence_length"],
        "questions": [
            "What is the sentiment of this product review?",
            "Which product categories receive the most negative reviews?",
            "How has overall customer sentiment trended over the past 6 months?",
            "What key phrases drive negative sentiment predictions?",
        ],
    },
]
