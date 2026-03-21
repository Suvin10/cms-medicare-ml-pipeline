# Model Metrics

This document summarizes the key machine learning evaluation metrics used in the CMS Medicare analytics and ML pipeline.

## Regression Model Metrics

### Baseline Linear Regression
- **MAE:** 3.131002673433983
- **RMSE:** 5.298360977462356
- **R²:** 0.9988458676376599

### XGBoost Regression
- **MAE:** 4.196263002397133
- **RMSE:** 28.56626555537998
- **R²:** 0.9664510084428551

## Time-Series / Time-Aware Model Metrics

### RandomForestRegressor on State-Year Trend Data
- **MAE:** 6.7296209424484035
- **RMSE:** 10.729275580483117
- **R²:** 0.31979331540390077

## Power BI Dashboard Monitoring Metrics

These metrics were surfaced in the final ML Prediction Performance dashboard page:

- **MAE:** 2.58
- **MAPE:** 2.81%
- **Prediction Bias:** -0.25

## Metric Definitions

### MAE
Mean Absolute Error measures the average magnitude of prediction error across rows.

- lower is better
- useful for understanding the typical size of mistakes

### RMSE
Root Mean Squared Error penalizes larger errors more heavily than MAE.

- lower is better
- useful when large prediction misses matter more

### R²
R-squared measures how much variance in the target is explained by the model.

- closer to 1 is better
- useful for overall fit assessment

### MAPE
Mean Absolute Percentage Error measures the average percentage difference between actual and predicted values.

- expressed as a percentage
- useful for understanding relative error

### Prediction Bias
Prediction Bias measures whether the model tends to systematically overpredict or underpredict.

- positive bias = model tends to overpredict
- negative bias = model tends to underpredict
- near zero = little directional bias on average

## Interpretation

The project showed:

- strong regression performance on the Gold feature dataset
- a strong linear relationship between predictors and target payment amount
- weaker time-series / time-aware performance due to the limited state-year panel depth
- business-facing ML monitoring through Power BI using actual vs predicted analysis and error KPIs