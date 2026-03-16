# SageMaker Workflow Notes

This folder documents the ML layer of the project.

## Components

### Regression Model
Used to predict:
- `target_avg_payment_amt`

### Time-Series Model
Used to analyze trend behavior across state-year payment aggregates.

## Workflow Summary

1. Gold analytical features prepared in Databricks
2. Feature data stored/exported for SageMaker workflows
3. Regression model trained for payment prediction
4. Time-series model trained for trend analysis
5. Batch inference pipeline generated `predictions.csv`
6. Prediction output loaded back into Databricks as `gold_regression_predictions`

## Planned Improvements

- add training scripts
- add batch inference script examples
- document model hyperparameters and validation approach
- add experiment tracking / registry notes