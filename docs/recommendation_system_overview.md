# Recommendation System Modeling Strategy

## Data & Problem Definition
- Source: `project_ecommerce/data/cleaned_data.csv` containing 301k transaction-level rows across 86,740 customers and 5 product categories.
- Target signal: Explicit product ratings on a 1-5 scale aggregated to unique customer-product pairs (217,644 interactions).
- Goal: Predict the next rating for a given `(user, product)` pair to support top-N personalized recommendations inside the ecommerce dashboard.

## Models & Algorithms
1. **Matrix Factorization (SVD, Surprise library)**
   - Learns latent user and item factors with tuned hyperparameters (`n_factors`, `n_epochs`, `lr_all`, `reg_all`).
   - Forms the classical collaborative filtering baseline with fast inference and interpretable embeddings.
2. **Neural Collaborative Filtering (NCF)**
   - Uses learned user/item embeddings (64 dims) followed by dense ReLU blocks with batch normalization, dropout, and L2 regularization.
   - Optimized with Adam (lr=7e-4, gradient clipping) to capture higher-order user-item interactions.
3. **Wide & Deep Recommender**
   - Deep tower identical to NCF plus a wide component with explicit element-wise user-item interactions.
   - Balances memorization (wide) and generalization (deep) for production-grade performance.

## Training & Evaluation Pipeline
- **Encoding**: Label encoding converts `Customer_ID` and `Product_Category` into contiguous integer ids consumed by all models.
- **Hold-out Strategy**: Custom stratified split keeps at least one interaction per user in train and allocates 20% to test, preventing cold-start leakage.
- **Baselines**: Global-mean and per-user mean predictors are computed first (RMSE 1.213 / MAE 1.033 and RMSE 1.563 / MAE 1.259 respectively) to gauge gains.
- **Hyperparameter Search**:
  - SVD: 3-fold cross-validated grid search on latent factors, epochs, learning rate, and regularization.
  - Deep models: EarlyStopping + ReduceLROnPlateau tune effective epochs while monitoring validation loss.
- **Metrics**: Root Mean Squared Error (RMSE) and Mean Absolute Error (MAE) on the untouched test fold; models also persist metrics JSON for dashboards.

## Leakage & Overfitting Controls
- Train/test split never mixes interactions from the same customer, so user history in test is unseen during training.
- Aggregation only uses historical ratings before splitting, so no future leakage.
- NCF and Wide & Deep include L2 regularization, dropout, batch normalization, and gradient clipping to mitigate overfitting on dense embeddings.
- Early stopping restores the best weights, and ReduceLROnPlateau lowers learning rates instead of overfitting.
- Saving encoders and models separately prevents accidental overriding when re-training in different sessions.

## Target KPIs & Acceptance Criteria
- **Baseline to beat**: RMSE 1.213 / MAE 1.033 (global mean predictor).
- **SVD expectation**: RMSE ~ 1.23, MAE ~ 1.04 - provides a strong baseline and should at least match global-mean RMSE despite sparse catalog.
- **NCF / Wide & Deep target**: Push RMSE <= 1.20 and MAE <= 1.00 by leveraging nonlinear interaction modeling.
- Performance within +/- 0.02 of these thresholds is acceptable given only five item categories; larger gains will likely require richer content features.

## Next Steps
- Finish fine-tuning deep models (shorter epochs + stratified mini-batches) and log their best metrics.
- Investigate top-N recommendation quality (precision@K / recall@K) once regression accuracy stabilizes.
- Explore hybrid signals (spend, recency) to enrich the current user-item-only interaction matrix.
