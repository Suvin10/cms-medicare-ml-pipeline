# Model Metrics

This document summarizes the key regression model evaluation metrics surfaced in the Power BI dashboard.

## Regression Evaluation Metrics

### MAE
**Mean Absolute Error** measures the average magnitude of prediction error across rows.

- Lower is better
- Helps quantify the average size of prediction mistakes

### MAPE
**Mean Absolute Percentage Error** measures the average percentage difference between actual and predicted values.

- Expressed as a percentage
- Useful for understanding relative error rather than absolute units

### Prediction Bias
Measures whether the model tends to systematically overpredict or underpredict.

- Positive bias = model tends to overpredict
- Negative bias = model tends to underpredict
- Value near zero = little directional bias on average

## Example Dashboard Values

These values are taken from the final Power BI dashboard:

- **MAE:** 2.58
- **MAPE:** 2.81%
- **Prediction Bias:** -0.25

## Interpretation

The regression model shows:

- low average prediction error
- low percentage error overall
- slight negative bias, indicating mild underprediction on average

These metrics are displayed alongside grouped visual comparisons in the Power BI ML Prediction Performance page.