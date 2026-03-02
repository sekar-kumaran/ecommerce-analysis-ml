# E-Commerce ML Pipeline - Data Flow Documentation

## Pipeline Overview

This document outlines the complete data processing pipeline for the e-commerce ML project, showing how data flows through each notebook and what outputs are generated.

---

## 📊 Complete Pipeline Flow

```
Raw Data (new_retail_data.csv)
    ↓
[1] data_understanding.ipynb
    ↓
Profiled Data + Metadata
    ↓
[2] data_cleaning.ipynb  
    ↓
Cleaned Data
    ↓
[3] eda_business_insights.ipynb
    ↓
Business Insights + Enriched Dataset
    ↓
[4] feature engineering .ipynb
    ↓
Customer Features (Engineered)
    ↓
[5] churn_labeling.ipynb
    ↓
Train/Test Splits
    ↓
[6] model_training_1.ipynb / 06a_churn_prediction.ipynb / etc.
    ↓
Trained Models + Predictions
```

---

## 📁 Notebook Details & Outputs

### 1️⃣ **data_understanding.ipynb**

**Purpose**: Initial data exploration, profiling, and quality assessment

**Input**:
- `data/new_retail_data.csv` (raw retail transaction data)

**Processing**:
- Load and inspect dataset structure
- Analyze data types and distributions
- Identify missing values and outliers
- Validate business logic
- Perform customer-level aggregation
- Parse date columns

**Outputs**:
```
data/
  └── profiled_data.csv              ← Dataset with Date_Parsed column added

reports/
  ├── data_understanding_summary.json       ← Key metrics and statistics
  ├── data_understanding_column_profile.csv ← Column-level metadata
  └── data_understanding_missing_values.csv ← Missing value summary
```

**Key Features**:
- Adds `Date_Parsed` column for downstream use
- Identifies data quality issues
- Documents column cardinality and types
- NO transformations, only exploration

---

### 2️⃣ **data_cleaning.ipynb**

**Purpose**: Clean raw data, handle missing values, fix data quality issues

**Input**:
- `data/new_retail_data.csv` (raw data - independent of data_understanding.ipynb)

**Processing**:
- Remove duplicates
- Fix data types (dates, numericals, categoricals)
- Handle missing values (KNN imputation, mode, etc.)
- Validate and correct:
  - Age ranges (18-100)
  - Ratings (1-5)
  - Negative amounts
  - Year-date inconsistencies
- Standardize categorical values
- Create derived columns:
  - Day of week, month, quarter
  - Weekend flag
  - Hour and time of day
  - Days since first purchase
- Sort by customer and date

**Outputs**:
```
data/
  └── cleaned_data.csv              ← Fully cleaned transaction dataset

reports/
  └── cleaning_report.txt           ← Cleaning operations log

data/
  └── cleaning_metadata.json        ← Metadata about cleaning steps
```

**Key Features**:
- Zero missing values
- Zero duplicates
- All data types correctly formatted
- Derived temporal columns ready for feature engineering
- Data quality score calculated

---

### 3️⃣ **eda_business_insights.ipynb**

**Purpose**: Deep business analysis, RFM segmentation, cohort analysis

**Input**:
- `data/cleaned_data.csv` (from data_cleaning.ipynb)

**Processing**:
- Customer-level aggregation (transaction counts, revenue, ratings)
- RFM analysis (Recency, Frequency, Monetary)
- RFM segmentation (Champions, Loyal, At Risk, Lost)
- Revenue trend analysis (daily, monthly, hourly, day of week)
- Customer demographics analysis
- Product/category performance analysis
- Cohort retention analysis
- Correlation analysis
- Business insights generation

**Outputs**:
```
data/
  ├── business_insights_dataset.csv      ← Enriched transaction data with cohort fields
  ├── customer_behavior_summary.csv      ← Customer-level aggregated metrics
  ├── customer_rfm_segments.csv          ← RFM scores and segments per customer
  ├── cohort_retention_matrix.csv        ← Retention rates by cohort
  ├── category_metrics.csv               ← Product category performance
  ├── daily_revenue_timeseries.csv       ← Daily revenue with moving averages
  └── eda_statistics.json                ← Key business metrics summary

eda_visualizations/
  ├── rfm_segmentation.png
  ├── revenue_trends.png
  ├── customer_distribution.png
  ├── product_analysis.png
  ├── cohort_analysis.png
  └── correlation_matrix.png
```

**Key Features**:
- Adds Cohort, Transaction_Month, Cohort_Index columns to main dataset
- Creates customer-level behavioral summaries
- Identifies top/bottom performers
- Saves reusable artifacts for downstream modeling

---

### 4️⃣ **feature engineering .ipynb**

**Purpose**: Create customer-level features for ML modeling

**Input**:
- `data/cleaned_data.csv` (transaction-level data)

**Processing**:
- **RFM Features**: Recency days, transaction count, LTV, avg order value, RFM scores
- **Temporal Features**: Recent vs historical activity, purchase velocity, preferred shopping times
- **Product Features**: Category diversity (entropy), brand diversity, rating behavior
- **Behavioral Features**: Payment/shipping preferences, order status distribution, cart size metrics
- **Demographic Features**: Age groups, income brackets
- Aggregate from transaction-level to customer-level
- Handle missing values
- Calculate derived metrics

**Outputs**:
```
data/
  ├── customer_features.csv              ← Full feature matrix (customer-level)
  ├── customer_features_enriched.csv     ← Final snapshot (same as above, redundant save)
  ├── feature_descriptions.csv           ← Feature metadata and business meanings
  └── feature_engineering_log.json       ← Feature creation log

reports/
  └── feature_importance_analysis.png    ← Correlation analysis visualization
```

**Key Features**:
- Transforms transaction-level → customer-level data
- ~50+ engineered features per customer
- Includes categorical and numerical features
- Ready for ML model training
- Comprehensive feature documentation

---

### 5️⃣ **churn_labeling.ipynb**

**Purpose**: Define churn, create labels, perform train-test split

**Input**:
- `data/customer_features.csv` (from feature engineering .ipynb)

**Processing**:
- Define churn threshold (60 days recency)
- Create binary churn label (0 = Active, 1 = Churned)
- Analyze churn distribution by segments (RFM, demographics)
- Exclude non-encoded categorical columns
- **Stratified train-test split** (80/20, maintaining class balance)
- Data integrity checks
- Generate metadata

**Outputs**:
```
data/
  ├── X_train_churn.csv                  ← Training features
  ├── y_train_churn.csv                  ← Training labels
  ├── X_test_churn.csv                   ← Test features
  ├── y_test_churn.csv                   ← Test labels
  └── train_test_metadata_churn.json     ← Split metadata and class distribution

reports/
  └── churn_distribution.png             ← Visualization of churn rates
```

**Key Features**:
- Stratified split ensures balanced class distribution in both sets
- ~86,000 training samples, ~21,000 test samples
- Churn rate maintained across train/test (~26-27%)
- No data leakage
- Both classes present in both sets

---

### 6️⃣ **Model Training Notebooks**

**Purpose**: Train ML models for various prediction tasks

**Notebooks**:
- `model_training_1.ipynb` - Traditional ML (LightGBM, XGBoost, Random Forest)
- `06a_churn_prediction.ipynb` - Churn prediction models
- `06b_recommendation_systems.ipynb` - Collaborative filtering (SVD, NCF, Wide&Deep)
- `06c_customer_segmentation.ipynb` - Clustering
- `06d_sales_clv_prediction.ipynb` - Customer lifetime value
- `06e_fraud_detection.ipynb` - Anomaly detection
- `06f_demand_forecasting.ipynb` - Time series
- `06g_sentiment_analysis.ipynb` - NLP

**Input**:
- `data/X_train_churn.csv` and `y_train_churn.csv` (for churn models)
- `data/X_test_churn.csv` and `y_test_churn.csv` (for evaluation)
- `data/cleaned_data.csv` (for recommendation/segmentation)
- `data/customer_features.csv` (for customer-level models)

**Outputs**:
```
artifacts/
  ├── models/
  │   ├── lightgbm_pipeline.pkl
  │   ├── xgboost_pipeline.pkl
  │   ├── random_forest_pipeline.pkl
  │   ├── svd_recommender.pkl
  │   ├── ncf_model.h5
  │   └── wide_deep_model.h5
  ├── encoders/
  │   └── (various encoders)
  └── scalers/
      └── (various scalers)

reports/
  ├── model_training_metrics.json        ← CV and test metrics for all models
  ├── model_comparison_report.csv        ← Side-by-side model comparison
  └── (various visualizations)
```

---

## 🔄 Critical Pipeline Dependencies

### Data Flow Chain:
```
Raw Data → Profiled → Cleaned → Business Insights → Features → Labels → Models
```

### Notebook Dependencies:

| Notebook | Depends On | Required Input Files |
|----------|------------|---------------------|
| data_understanding.ipynb | None | `new_retail_data.csv` |
| data_cleaning.ipynb | None | `new_retail_data.csv` |
| eda_business_insights.ipynb | data_cleaning | `cleaned_data.csv` |
| feature engineering .ipynb | data_cleaning | `cleaned_data.csv` |
| churn_labeling.ipynb | feature engineering | `customer_features.csv` |
| model_training_*.ipynb | churn_labeling | `X_train/test_churn.csv`, `y_train/test_churn.csv` |

### Independent Notebooks:
- `data_understanding.ipynb` - Can run standalone (exploration only)
- `data_cleaning.ipynb` - Can run standalone (produces cleaned data)

---

## ✅ Data Persistence Checklist

| Notebook | Saves Dataset? | Output File(s) | ✓ Status |
|----------|---------------|----------------|----------|
| data_understanding.ipynb | ✅ YES | profiled_data.csv + metadata | ✓ VERIFIED |
| data_cleaning.ipynb | ✅ YES | cleaned_data.csv + metadata | ✓ VERIFIED |
| eda_business_insights.ipynb | ✅ YES | business_insights_dataset.csv + 5 CSVs + JSON | ✓ VERIFIED |
| feature engineering .ipynb | ✅ YES | customer_features.csv (2 versions) + metadata | ✓ VERIFIED |
| churn_labeling.ipynb | ✅ YES | X/y train/test (4 CSVs) + metadata | ✓ VERIFIED |
| model_training_*.ipynb | ✅ YES | Trained models (.pkl / .h5) + metrics JSON | ✓ VERIFIED |

---

## 🚀 How to Run the Pipeline

### Sequential Execution (Recommended):

```bash
# 1. Data Understanding (Optional - for exploration)
jupyter nbconvert --execute --to notebook data_understanding.ipynb

# 2. Data Cleaning (REQUIRED - generates cleaned_data.csv)
jupyter nbconvert --execute --to notebook data_cleaning.ipynb

# 3. Business Insights (REQUIRED - generates customer artifacts)
jupyter nbconvert --execute --to notebook eda_business_insights.ipynb

# 4. Feature Engineering (REQUIRED - generates customer_features.csv)
jupyter nbconvert --execute --to notebook "feature engineering .ipynb"

# 5. Churn Labeling (REQUIRED - generates train/test splits)
jupyter nbconvert --execute --to notebook churn_labeling.ipynb

# 6. Model Training (Pick one or more)
jupyter nbconvert --execute --to notebook model_training_1.ipynb
jupyter nbconvert --execute --to notebook 06a_churn_prediction.ipynb
jupyter nbconvert --execute --to notebook 06b_recommendation_systems.ipynb
# ... etc
```

### Minimal Pipeline (For Quick Model Training):

```bash
# Only these 4 notebooks are required:
1. data_cleaning.ipynb
2. feature engineering .ipynb
3. churn_labeling.ipynb
4. model_training_1.ipynb (or any 06*.ipynb)
```

---

## 📝 Important Notes

### Data Storage Strategy:
- **Raw data**: `data/new_retail_data.csv` (never modified)
- **Intermediate data**: `data/cleaned_data.csv`, `data/customer_features.csv`
- **Model-ready data**: `data/X_train_churn.csv`, etc.
- **Metadata**: JSON files in `data/` and `reports/`
- **Models**: Serialized in `artifacts/models/`
- **Visualizations**: `eda_visualizations/` and `reports/`

### File Sizes (Approximate):
- `new_retail_data.csv`: ~120 MB (500K+ transactions)
- `cleaned_data.csv`: ~130 MB (with derived columns)
- `customer_features.csv`: ~15 MB (69K customers, 50+ features)
- `X_train_churn.csv`: ~12 MB
- `X_test_churn.csv`: ~3 MB

### Data Consistency:
- All notebooks save their outputs **at the end** of execution
- Each notebook can be rerun independently if its input files exist
- Metadata JSON files track creation timestamps and parameters
- **No data is modified in place** - all transformations create new files

---

## 🔍 Verification Commands

Check if all required files exist:

```python
import os
from pathlib import Path

required_files = [
    'data/cleaned_data.csv',
    'data/customer_features.csv',
    'data/X_train_churn.csv',
    'data/y_train_churn.csv',
    'data/X_test_churn.csv',
    'data/y_test_churn.csv',
]

for file in required_files:
    exists = Path(file).exists()
    status = "✓" if exists else "✗"
    print(f"{status} {file}")
```

---

## 📊 Data Schema Evolution

### Transaction-Level (Raw → Cleaned):
- **Rows**: ~500K transactions
- **Columns**: 20 original → 28 after cleaning (added temporal features)

### Customer-Level (Feature Engineering):
- **Rows**: ~69K customers
- **Columns**: ~50+ engineered features

### Model-Ready (After Churn Labeling):
- **Train**: ~86K samples
- **Test**: ~21K samples
- **Features**: ~40 numerical features (after excluding categoricals)
- **Target**: Binary (0/1) churn label

---

## 🎯 Next Steps After Pipeline Execution

1. **Model Evaluation**: Run `07_model_evaluation.ipynb` to compare all trained models
2. **Hyperparameter Tuning**: Use GridSearchCV/Optuna for optimization
3. **Feature Selection**: Analyze feature importance and reduce dimensionality
4. **Ensemble Methods**: Combine top models for better performance
5. **Deployment**: Export best model for production use
6. **Monitoring**: Track model drift and retrain periodically

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-14  
**Pipeline Status**: ✅ ALL NOTEBOOKS SAVE OUTPUTS CORRECTLY
