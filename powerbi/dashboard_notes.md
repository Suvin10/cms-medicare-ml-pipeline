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
- KPI cards for actual payment, services, beneficiaries, providers, and averages
- payment by state
- payment by provider type
- payment by place of service
- services by state

### Page 2 — State-Year Trends
Purpose:
- show time trends and state-level payment patterns

Main visuals:
- average payment by year
- average standardized amount by year
- state comparison for payment, services, and beneficiaries

### Page 3 — Detailed Drilldown
Purpose:
- provide row-level inspection and filtering across the main analytical dimensions

Main visuals:
- detailed table with provider/service-level aggregate metrics
- slicers for year, state, provider type, and place of service

### Page 4 — ML Prediction Performance
Purpose:
- evaluate regression model performance using actual and predicted payment values

Main visuals:
- total actual vs total predicted payment
- prediction error, MAE, MAPE, and prediction bias
- actual vs predicted by state
- actual vs predicted by provider type
- scatter plot for actual vs predicted relationship
- largest prediction errors table

## Design Choices

Key dashboard design choices included:

- using Databricks Gold tables instead of raw files for cleaner BI consumption
- creating reusable DAX measures for consistent reporting logic
- preferring horizontal bar charts for long provider type/state labels
- separating descriptive analytics pages from ML evaluation page
- keeping slicers consistent across pages for easier navigation

## Future Enhancements

Potential Power BI improvements:
- publish dashboard to Power BI Service
- add drill-through navigation between summary and detail pages
- add model refresh timestamp metadata
- enable incremental refresh where appropriate
- add tooltips and richer annotations for executive users