# Data Dictionary

This document describes the main analytical and ML-related fields used across the Databricks Gold layer and Power BI dashboard.

## gold_regression_features

| Column | Description |
|---|---|
| `reporting_year` | Reporting year of the aggregated CMS Medicare provider-service data |
| `provider_state` | U.S. state associated with the provider |
| `provider_type` | Provider specialty or provider classification |
| `place_of_service` | Place of service / service setting code |
| `provider_service_rows` | Number of provider-service level records contributing to the aggregation |
| `distinct_providers` | Count of distinct providers within the grouped segment |
| `distinct_hcpcs_codes` | Count of distinct HCPCS procedure codes within the grouped segment |
| `total_beneficiaries` | Total number of beneficiaries in the grouped segment |
| `total_services` | Total number of services in the grouped segment |
| `avg_submitted_charge_mean` | Mean submitted charge amount across the grouped segment |
| `avg_allowed_amt_mean` | Mean allowed amount across the grouped segment |
| `target_avg_payment_amt` | Actual average Medicare payment amount used as the regression target |

## gold_state_year_payment_trend

| Column | Description |
|---|---|
| `reporting_year` | Reporting year |
| `provider_state` | U.S. state associated with the provider |
| `total_services` | Total services for the state-year aggregation |
| `total_beneficiaries` | Total beneficiaries for the state-year aggregation |
| `avg_payment_amt` | Average payment amount for the state-year aggregation |
| `avg_standardized_amt` | Average standardized amount for the state-year aggregation |

## gold_regression_predictions

| Column | Description |
|---|---|
| `reporting_year` | Reporting year of the aggregated prediction row |
| `provider_state` | U.S. state associated with the prediction segment |
| `provider_type` | Provider specialty or provider classification |
| `place_of_service` | Place of service / service setting code |
| `provider_service_rows` | Number of provider-service records in the segment |
| `distinct_providers` | Count of distinct providers in the segment |
| `distinct_hcpcs_codes` | Count of distinct HCPCS codes in the segment |
| `total_beneficiaries` | Total beneficiaries in the segment |
| `total_services` | Total services in the segment |
| `avg_submitted_charge_mean` | Mean submitted charge amount in the segment |
| `avg_allowed_amt_mean` | Mean allowed amount in the segment |
| `target_avg_payment_amt` | Actual average payment amount |
| `predicted_payment` | Regression model predicted average payment amount |

## Power BI ML Evaluation Fields

| Field | Description |
|---|---|
| `Prediction Error` | Difference between actual payment and predicted payment |
| `MAE` | Mean Absolute Error across prediction rows |
| `MAPE` | Mean Absolute Percentage Error across prediction rows |
| `Prediction Bias` | Average signed prediction difference (predicted minus actual) |
| `Row Error` | Row-level actual minus predicted value |
| `Absolute Row Error` | Absolute row-level prediction error |