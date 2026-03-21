# Power BI Dashboard Notes

This document summarizes the Power BI dashboard built on top of Databricks Gold tables.

## Data Source

Power BI connects to Databricks using curated Gold tables:

- `gold_regression_features`
- `gold_state_year_payment_trend`
- `gold_regression_predictions`

## Dashboard Pages

### Page 1 — Executive Overview

Purpose:
- summarize Medicare payment and utilization metrics
- compare payment totals across states, provider types, and place of service

Main visuals:
- KPI cards for total actual payment, total services, total beneficiaries, total providers, average actual payment, and average allowed amount
- actual payment by state
- actual payment by provider type
- actual payment by place of service
- total services by state

Main slicers:
- reporting_year
- provider_state
- provider_type
- place_of_service

### Page 2 — State-Year Trends

Purpose:
- show time trends and state-level payment patterns

Main visuals:
- average payment by year
- average standardized amount by year
- average payment by state
- total services by state
- total beneficiaries by state

Main slicers:
- reporting_year
- provider_state

### Page 3 — Detailed Drilldown

Purpose:
- provide row-level inspection and filtering across the main analytical dimensions

Main visuals:
- detailed table with provider and service-level aggregate metrics
- slicers for year, state, provider type, and place of service

Table fields:
- reporting_year
- provider_state
- provider_type
- place_of_service
- provider_service_rows
- distinct_providers
- distinct_hcpcs_codes
- total_beneficiaries
- total_services
- avg_submitted_charge_mean
- avg_allowed_amt_mean
- target_avg_payment_amt

### Page 4 — ML Prediction Performance

Purpose:
- evaluate regression model performance using actual and predicted payment values

Main visuals:
- total actual payment
- total predicted payment
- prediction error
- MAE
- MAPE
- prediction bias
- actual vs predicted by state
- actual vs predicted by provider type
- scatter plot for actual vs predicted fit
- largest prediction errors table

Main slicers:
- reporting_year
- provider_state
- provider_type
- place_of_service

## Key DAX Measures

### Executive Overview

- `Total Actual Payment = SUM(gold_regression_features[target_avg_payment_amt])`
- `Total Services = SUM(gold_regression_features[total_services])`
- `Total Beneficiaries = SUM(gold_regression_features[total_beneficiaries])`
- `Total Providers = SUM(gold_regression_features[distinct_providers])`
- `Avg Actual Payment = AVERAGE(gold_regression_features[target_avg_payment_amt])`
- `Avg Allowed Amount = AVERAGE(gold_regression_features[avg_allowed_amt_mean])`

### State-Year Trends

- `Trend Avg Payment = AVERAGE(gold_state_year_payment_trend[avg_payment_amt])`
- `Trend Avg Standardized Amount = AVERAGE(gold_state_year_payment_trend[avg_standardized_amt])`
- `Trend Total Services = SUM(gold_state_year_payment_trend[total_services])`
- `Trend Total Beneficiaries = SUM(gold_state_year_payment_trend[total_beneficiaries])`

### ML Prediction Performance

- `Total Actual Payment = SUM(gold_regression_predictions[target_avg_payment_amt])`
- `Total Predicted Payment = SUM(gold_regression_predictions[predicted_payment])`
- `Prediction Error = [Total Actual Payment] - [Total Predicted Payment]`
- `Absolute Error = SUMX(gold_regression_predictions, ABS(gold_regression_predictions[target_avg_payment_amt] - gold_regression_predictions[predicted_payment]))`
- `MAE = DIVIDE([Absolute Error], COUNTROWS(gold_regression_predictions))`
- `MAPE = AVERAGEX(gold_regression_predictions, DIVIDE(ABS(gold_regression_predictions[target_avg_payment_amt] - gold_regression_predictions[predicted_payment]), gold_regression_predictions[target_avg_payment_amt]))`
- `Prediction Bias = AVERAGEX(gold_regression_predictions, gold_regression_predictions[predicted_payment] - gold_regression_predictions[target_avg_payment_amt])`

### Row-Level Calculated Columns

- `Row Error = gold_regression_predictions[target_avg_payment_amt] - gold_regression_predictions[predicted_payment]`
- `Absolute Row Error = ABS(gold_regression_predictions[target_avg_payment_amt] - gold_regression_predictions[predicted_payment])`

## Design Choices

Key dashboard design choices included:

- using Databricks Gold tables instead of raw files for cleaner BI consumption
- creating reusable DAX measures for consistent reporting logic
- preferring horizontal bar charts for long provider type and state labels
- separating descriptive analytics pages from the ML evaluation page
- keeping slicers consistent across pages for easier navigation
- using KPI cards at the top of each page for executive readability

## Visual Design Notes

- Page titles and metadata were standardized across all pages
- dashboard pages were designed for portfolio and interview presentation quality
- metric cards were formatted for readability using appropriate display units and decimal precision
- state and provider type visuals were converted to horizontal bar charts where necessary for label clarity
- the ML page was designed to show both business-facing summary metrics and row-level prediction inspection

## Future Enhancements

Potential Power BI improvements:
- publish dashboard to Power BI Service
- add drill-through navigation between summary and detail pages
- add model refresh timestamp metadata
- enable incremental refresh where appropriate
- add tooltips and richer annotations for executive users