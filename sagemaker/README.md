# SageMaker Workflow Notes

This folder documents the machine learning layer of the CMS Medicare analytics and ML pipeline.

## Purpose

SageMaker was used to:

- train a regression model for average Medicare payment prediction
- train a time-aware model using state-year payment trend data
- generate batch predictions for downstream BI reporting
- store models, metrics, and predictions in versioned S3 paths

## Input Datasets

### Regression Dataset
Source:
- `gold_regression_features.csv`

Typical S3 path:
- `s3://cms-medical-rwe-suvin-eu-west-2/ml/data/2026-03-03_v1/gold_regression_features.csv`

Target:
- `target_avg_payment_amt`

### Time-Series / Time-Aware Dataset
Source:
- `gold_state_year_payment_trend.csv`

Typical S3 path:
- `s3://cms-medical-rwe-suvin-eu-west-2/ml/data/2026-03-03_v1/gold_state_year_payment_trend.csv`

## Output Artifacts

### Regression Model
Example S3 path:
- `s3://cms-medical-rwe-suvin-eu-west-2/ml/models/regression/2026-03-03_v1/model.joblib`

### Time-Series Model
Example S3 path:
- `s3://cms-medical-rwe-suvin-eu-west-2/ml/models/timeseries/2026-03-03_v1/model.joblib`

### Metrics
Metrics were stored alongside model outputs and surfaced in documentation and Power BI.

### Predictions
Batch inference produced:
- `predictions.csv`

Example S3 path:
- `s3://cms-medical-rwe-suvin-eu-west-2/ml/predictions/regression/2026-03-03_v1/predictions.csv`

## Workflow Summary

1. Gold analytical datasets were prepared in Databricks
2. Gold datasets were exported to S3
3. SageMaker loaded the regression dataset and trained candidate models
4. Regression metrics were compared across baseline linear regression and XGBoost
5. A time-aware model was trained on the state-year trend dataset
6. Batch inference generated predictions for BI and reporting use
7. Predictions were loaded back into Databricks for Power BI consumption

## Regression Results

### Baseline Linear Regression
- **MAE:** 3.131002673433983
- **RMSE:** 5.298360977462356
- **R²:** 0.9988458676376599

### XGBoost Regression
- **MAE:** 4.196263002397133
- **RMSE:** 28.56626555537998
- **R²:** 0.9664510084428551

## Time-Aware Model Results

### RandomForestRegressor
- **MAE:** 6.7296209424484035
- **RMSE:** 10.729275580483117
- **R²:** 0.31979331540390077

## Files in This Folder

- `train_regression.py` — training workflow for regression modeling
- `train_timeseries.py` — time-aware / trend-model training workflow
- `batch_inference.py` — prediction generation workflow for regression outputs

## Notes

- S3 was used as the storage handoff between Databricks and SageMaker
- versioned paths were used for datasets, models, and predictions
- predictions were later consumed by Power BI via Databricks Gold tables