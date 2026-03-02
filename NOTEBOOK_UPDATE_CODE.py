# Key Updates for 06b-06g ML Notebooks
# This file contains the critical code changes needed for each notebook

"""
=============================================================================
06b - RECOMMENDATION SYSTEMS
=============================================================================
Dataset: transaction_level_enriched.csv (301,006 transactions)
Models: SVD, LightFM, Neural Collaborative Filtering
"""

# --- DATA LOADING UPDATE ---
# REPLACE:
df = pd.read_csv('../data/cleaned_data.csv')
interaction_df = df[['Customer_ID', 'Product_Category', 'Ratings', 'Amount']].copy()

# WITH:
df = pd.read_csv('../data/transaction_level_enriched.csv')
# Use enriched features for better recommendations
interaction_df = df[['Customer_ID', 'Product_Category', 'Ratings', 'Amount',
                     'Customer_Engagement_Score', 'Category_Exploration_Score',
                     'Brand_Diversity_Score', 'Repeat_Buyer_Score']].copy()

# --- MODEL SAVING UPDATE ---
# ADD at end of notebook:
MODEL_VERSION = datetime.now().strftime('%Y%m%d_%H%M%S')

# Save SVD model
svd_model_path = f'../artifacts/models/recommendation_svd_{MODEL_VERSION}.pkl'
pickle.dump(svd_model, open(svd_model_path, 'wb'))

# Save NCF model
ncf_model_path = f'../artifacts/models/recommendation_ncf_{MODEL_VERSION}.keras'
ncf_model.save(ncf_model_path)

# Save metadata
metadata = {
    'model_version': MODEL_VERSION,
    'created_at': datetime.now().isoformat(),
    'n_interactions': len(interaction_df),
    'n_users': interaction_df['Customer_ID'].nunique(),
    'n_items': interaction_df['Product_Category'].nunique(),
    'metrics': {
        'rmse_svd': rmse_svd,
        'mae_svd': mae_svd,
        'ndcg@10': ndcg_10  # Add if implemented
    }
}
with open(f'../artifacts/models/recommendation_metadata_{MODEL_VERSION}.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"✓ Models saved with version: {MODEL_VERSION}")


"""
=============================================================================
06c - CUSTOMER SEGMENTATION  
=============================================================================
Dataset: customer_features_enriched.csv (86,740 customers)
Models: K-Means, DBSCAN, Hierarchical, GMM
"""

# --- DATA LOADING UPDATE ---
# REPLACE:
df = pd.read_csv('../data/cleaned_data.csv')
customer_agg = df.groupby('Customer_ID').agg({
    'Total_Amount': ['sum', 'mean', 'std', 'count'],
    ...
}).reset_index()

# WITH:
customer_df = pd.read_csv('../data/customer_features_enriched.csv')
# Already has 54 engineered features - no aggregation needed!

# Select features for clustering
feature_cols = ['Transaction_Count', 'Customer_LTV', 'Avg_Order_Value',
                'Avg_Rating', 'Unique_Categories', 'Unique_Brands',
                'Customer_Tenure_Days', 'Pct_Shipped', 'Weekend_Purchase_Pct']
X = customer_df[feature_cols].fillna(0)

# --- ADD SILHOUETTE ANALYSIS ---
from sklearn.metrics import silhouette_score, davies_bouldin_score

silhouette_scores = []
k_range = range(2, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    silhouette_scores.append(score)

# Plot
plt.plot(k_range, silhouette_scores, marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Analysis for Optimal K')
plt.savefig('../reports/segmentation_silhouette.png', dpi=300)

# --- MODEL SAVING UPDATE ---
MODEL_VERSION = datetime.now().strftime('%Y%m%d_%H%M%S')

# Save K-Means model
kmeans_path = f'../artifacts/models/segmentation_kmeans_{MODEL_VERSION}.pkl'
joblib.dump(kmeans_final, kmeans_path)

# Save cluster labels
customer_df['Cluster'] = kmeans_final.labels_
customer_df[[' Customer_ID', 'Cluster']].to_csv(
    f'../data/customer_segments_{MODEL_VERSION}.csv', index=False
)

# Save cluster profiles
cluster_profiles = customer_df.groupby('Cluster')[feature_cols].mean()
cluster_profiles.to_csv(f'../reports/cluster_profiles_{MODEL_VERSION}.csv')

print(f"✓ Segmentation models and profiles saved with version: {MODEL_VERSION}")


"""
=============================================================================
06d - CLV / SALES PREDICTION
=============================================================================
Dataset: customer_features_enriched.csv (86,740 customers)
Models: Linear Regression, Random Forest, XGBoost, LightGBM
"""

# --- DATA LOADING UPDATE ---
# REPLACE:
df = pd.read_csv('../data/cleaned_data.csv')
clv_df = df.groupby('Customer_ID').agg({
    'Total_Amount': 'sum',
    'Transaction_ID': 'count',
    ...
}).reset_index()

# WITH:
customer_df = pd.read_csv('../data/customer_features_enriched.csv')
# Target: Customer_LTV (already calculated)
# Features: All other customer features

# Prepare features and target
target = 'Customer_LTV'
exclude_cols = ['Customer_ID', target, 'First_Purchase_Date', 'Last_Purchase_Date',
                'Preferred_Day', 'Favorite_Category']
feature_cols = [col for col in customer_df.columns if col not in exclude_cols]

X = customer_df[feature_cols]
y = customer_df[target]

# --- ADD TRAIN/TEST SPLIT ---
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- ADD MULTIPLE MODELS ---
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
import lightgbm as lgb

models = {
    'Ridge': Ridge(alpha=1.0),
    'RandomForest': RandomForestRegressor(n_estimators=200, random_state=42),
    'LightGBM': lgb.LGBMRegressor(n_estimators=500, learning_rate=0.05, random_state=42)
}

results = []
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    results.append({
        'Model': name,
        'RMSE': rmse,
        'MAE': mae,
        'R2': r2
    })
    print(f"{name} - RMSE: {rmse:.2f}, MAE: {mae:.2f}, R2: {r2:.4f}")

results_df = pd.DataFrame(results)

# --- MODEL SAVING ---
MODEL_VERSION = datetime.now().strftime('%Y%m%d_%H%M%S')

# Save best model (by R2)
best_model_name = results_df.loc[results_df['R2'].idxmax(), 'Model']
best_model = models[best_model_name]

model_path = f'../artifacts/models/clv_{best_model_name.lower()}_{MODEL_VERSION}.pkl'
joblib.dump(best_model, model_path)

scaler_path = f'../artifacts/scalers/clv_scaler_{MODEL_VERSION}.pkl'
joblib.dump(scaler, scaler_path)

print(f"✓ CLV models saved with version: {MODEL_VERSION}")


"""
=============================================================================
06e - FRAUD DETECTION
=============================================================================
Dataset: transaction_level_enriched.csv (301,006 transactions)
Models: Isolation Forest, XGBoost with SMOTE, Autoencoder
"""

# --- DATA LOADING UPDATE ---
# REPLACE:
df = pd.read_csv('../data/cleaned_data.csv')
# Create synthetic fraud labels
df['is_fraud'] = 0
df.loc[(df['Ratings'] == 1) & (df['Total_Amount'] > df['Total_Amount'].quantile(0.95)), 'is_fraud'] = 1

# WITH:
df = pd.read_csv('../data/transaction_level_enriched.csv')

# Use enriched fraud-specific features
fraud_features = [
    'Total_Amount', 'Ratings', 'Age', 'Hour', 'IsWeekend',
    'Is_High_Value_Txn', 'Is_First_Transaction', 'Is_Velocity_Spike',
    'Low_Rating_High_Value', 'Is_Problem_Order', 'Amount_vs_Avg_Ratio',
    'Cart_Size_vs_Avg_Ratio', 'Is_Unusual_Hour', 'Transaction_Count',
    'Customer_Tenure_Days', 'Pct_Cancelled'
]

# Create fraud label (improved logic)
df['is_fraud'] = 0
# High-value + low rating
df.loc[(df['Low_Rating_High_Value'] == 1), 'is_fraud'] = 1
# Cancelled orders + high value
df.loc[(df['Is_Problem_Order'] == 1) & (df['Is_High_Value_Txn'] == 1), 'is_fraud'] = 1
# Velocity spike + unusual hour
df.loc[(df['Is_Velocity_Spike'] == 1) & (df['Is_Unusual_Hour'] == 1), 'is_fraud'] = 1

fraud_rate = df['is_fraud'].mean()
print(f"Fraud rate: {fraud_rate:.2%}")

# --- ADD SMOTE FOR SEVERE IMBALANCE ---
from imblearn.over_sampling import SMOTE

X = df[fraud_features].fillna(0)
y = df['is_fraud']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Apply SMOTE
smote = SMOTE(sampling_strategy=0.5, random_state=42)  # Minority = 50% of majority
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)

print(f"After SMOTE - Fraud samples: {y_train_resampled.sum()}, Normal: {(1-y_train_resampled).sum()}")

# --- TRAIN WITH PROPER METRICS ---
# For fraud, focus on Precision and Recall
from sklearn.metrics import precision_recall_curve, average_precision_score

xgb_model = xgb.XGBClassifier(
    scale_pos_weight=10,  # Emphasis on fraud class
    max_depth=6,
    learning_rate=0.05,
    n_estimators=500,
    random_state=42
)
xgb_model.fit(X_train_resampled, y_train_resampled)

y_pred_proba = xgb_model.predict_proba(X_test_scaled)[:, 1]
y_pred = (y_pred_proba >= 0.3).astype(int)  # Lower threshold for fraud detection

# Calculate metrics
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
pr_auc = average_precision_score(y_test, y_pred_proba)

print(f"Fraud Detection Metrics:")
print(f"  Precision: {precision:.4f}")
print(f"  Recall: {recall:.4f}")
print(f"  F1-Score: {f1:.4f}")
print(f"  PR-AUC: {pr_auc:.4f}")

# --- MODEL SAVING ---
MODEL_VERSION = datetime.now().strftime('%Y%m%d_%H%M%S')

model_path = f'../artifacts/models/fraud_xgboost_{MODEL_VERSION}.pkl'
joblib.dump(xgb_model, model_path)

scaler_path = f'../artifacts/scalers/fraud_scaler_{MODEL_VERSION}.pkl'
joblib.dump({'scaler': scaler, 'features': fraud_features}, scaler_path)

print(f"✓ Fraud detection models saved with version: {MODEL_VERSION}")


"""
=============================================================================
06f - DEMAND FORECASTING
=============================================================================
Dataset: transaction_level_enriched.csv (301,006 transactions)
Models: Prophet, SARIMA, LSTM, TCN
"""

# --- DATA LOADING UPDATE ---
# REPLACE:
df = pd.read_csv('../data/cleaned_data.csv')

# WITH:
df = pd.read_csv('../data/transaction_level_enriched.csv')
df['Transaction_DateTime'] = pd.to_datetime(df['Transaction_DateTime'])

# Aggregate by date (use enriched features for better forecasting)
daily_demand = df.groupby(df['Transaction_DateTime'].dt.date).agg({
    'Transaction_ID': 'count',
    'Total_Amount': 'sum',
    'Customer_Engagement_Score': 'mean',  # Average engagement
    'Is_High_Value_Txn': 'sum',  # High-value transaction count
    'IsWeekend': 'first'  # Weekend indicator
}).reset_index()

daily_demand.columns = ['Date', 'Orders', 'Revenue', 'Avg_Engagement', 
                        'High_Value_Txns', 'IsWeekend']
daily_demand['Date'] = pd.to_datetime(daily_demand['Date'])
daily_demand = daily_demand.sort_values('Date')

# --- ADD PROPER TRAIN/TEST SPLIT (TEMPORAL) ---
# Use last 30 days as test set
test_days = 30
train_size = len(daily_demand) - test_days

train_data = daily_demand.iloc[:train_size]
test_data = daily_demand.iloc[train_size:]

print(f"Train: {len(train_data)} days, Test: {len(test_data)} days")

# --- PROPHET MODEL ---
from prophet import Prophet

# Prepare data for Prophet
prophet_train = train_data[['Date', 'Orders']].copy()
prophet_train.columns = ['ds', 'y']

# Add regressors
prophet_model = Prophet(
    seasonality_mode='multiplicative',
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)
prophet_model.add_regressor('IsWeekend')
prophet_model.add_regressor('Avg_Engagement')

# Prepare training data with regressors
prophet_train = train_data[['Date', 'Orders', 'IsWeekend', 'Avg_Engagement']].copy()
prophet_train.columns = ['ds', 'y', 'IsWeekend', 'Avg_Engagement']

# Fit
prophet_model.fit(prophet_train)

# Predict
future = test_data[['Date', 'IsWeekend', 'Avg_Engagement']].copy()
future.columns = ['ds', 'IsWeekend', 'Avg_Engagement']
forecast = prophet_model.predict(future)

# Evaluate
y_true = test_data['Orders'].values
y_pred = forecast['yhat'].values

from sklearn.metrics import mean_absolute_error, mean_squared_error
mae = mean_absolute_error(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

print(f"Prophet Forecast Metrics:")
print(f"  MAE: {mae:.2f}")
print(f"  RMSE: {rmse:.2f}")
print(f"  MAPE: {mape:.2f}%")

# --- MODEL SAVING ---
MODEL_VERSION = datetime.now().strftime('%Y%m%d_%H%M%S')

model_path = f'../artifacts/models/forecast_prophet_{MODEL_VERSION}.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(prophet_model, f)

print(f"✓ Forecasting models saved with version: {MODEL_VERSION}")


"""
=============================================================================
06g - SENTIMENT ANALYSIS
=============================================================================
Dataset: transaction_level_enriched.csv (301,006 transactions)
Models: TF-IDF + Logistic, LSTM, BERT
"""

# --- DATA LOADING UPDATE ---
# REPLACE:
df = pd.read_csv('../data/cleaned_data.csv')

# WITH:
df = pd.read_csv('../data/transaction_level_enriched.csv')

# Use Customer_Satisfaction_Flag and ratings
df['Sentiment'] = pd.cut(df['Ratings'], bins=[0, 2, 3, 5], 
                          labels=['Negative', 'Neutral', 'Positive'])

# Create synthetic feedback if not exists (based on enriched features)
if 'Feedback' not in df.columns:
    def generate_feedback(row):
        if row['Customer_Satisfaction_Flag'] == 1:
            return f"Great product from {row.get('Product_Category', 'shop')}. Very satisfied with my purchase."
        elif row['Ratings'] <= 2:
            return f"Not happy with {row.get('Product_Category', 'this')}. Poor quality and service."
        else:
            return f"Average experience with {row.get('Product_Category', 'product')}. It's okay."
    
    df['Feedback'] = df.apply(generate_feedback, axis=1)

# Filter out null feedback
df = df.dropna(subset=['Feedback', 'Sentiment'])

print(f"Total samples: {len(df)}")
print(f"Sentiment distribution:\n{df['Sentiment'].value_counts()}")

# --- ADD TEXT PREPROCESSING ---
import re
from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

df['Feedback_Clean'] = df['Feedback'].apply(preprocess_text)

# --- TRAIN/TEST SPLIT ---
from sklearn.model_selection import train_test_split

X = df['Feedback_Clean']
y = df['Sentiment']

# Encode labels
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_encoded = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# --- TF-IDF + LOGISTIC REGRESSION ---
tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

from sklearn.linear_model import LogisticRegression

lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train_tfidf, y_train)

y_pred = lr_model.predict(X_test_tfidf)

from sklearn.metrics import classification_report, accuracy_score
accuracy = accuracy_score(y_test, y_pred)
print(f"\nLogistic Regression Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# --- MODEL SAVING ---
MODEL_VERSION = datetime.now().strftime('%Y%m%d_%H%M%S')

# Save TF-IDF model
model_path = f'../artifacts/models/sentiment_tfidf_lr_{MODEL_VERSION}.pkl'
joblib.dump({
    'vectorizer': tfidf,
    'model': lr_model,
    'label_encoder': le
}, model_path)

print(f"✓ Sentiment models saved with version: {MODEL_VERSION}")


"""
=============================================================================
SUMMARY OF KEY CHANGES
=============================================================================

1. DATA LOADING:
   - Customer-level: customer_features_enriched.csv (06a, 06c, 06d)
   - Transaction-level: transaction_level_enriched.csv (06b, 06e, 06f, 06g)

2. FEATURE USAGE:
   - Use pre-computed enriched features instead of aggregating
   - Leverage fraud-specific, recommendation-specific features

3. MODEL SAVING:
   - Add timestamp versioning: MODEL_VERSION = datetime.now().strftime('%Y%m%d_%H%M%S')
   - Save models with version suffix
   - Save scalers, encoders separately
   - Save metadata JSON with metrics

4. CLASS IMBALANCE:
   - Use SMOTE for severe imbalance (fraud, churn)
   - Set appropriate sampling_strategy
   - Apply only to training data
   - Use class_weight parameter

5. EVALUATION:
   - Add comprehensive metrics (not just accuracy)
   - For classification: Precision, Recall, F1, ROC-AUC, PR-AUC
   - For regression: RMSE, MAE, R2, MAPE
   - For clustering: Silhouette, Davies-Bouldin

6. PRODUCTION READY:
   - Proper train/test splits
   - Feature scaling (fit on train only)
   - Model versioning
   - Metadata logging
   - Deployment artifacts
"""

print("\n" + "="*70)
print("ML NOTEBOOK UPDATES - IMPLEMENTATION GUIDE")
print("="*70)
print("\nThis file contains all critical code changes for notebooks 06b-06g")
print("\nFor each notebook:")
print("1. Update data loading to use enriched datasets")
print("2. Add model versioning with timestamps")
print("3. Save models with metadata")
print("4. Add comprehensive evaluation metrics")
print("5. Test with actual data")
print("\nRefer to ML_NOTEBOOKS_PRODUCTION_GUIDE.md for detailed instructions")
print("="*70)
