# Project Runbook

This runbook describes the intended execution flow for the CMS Medicare analytics and machine learning pipeline.

## Prerequisites

Before running the project, ensure the following are available:

- Databricks workspace with SQL Warehouse access
- dbt configured for Databricks
- AWS S3 bucket for datasets, model artifacts, metrics, and predictions
- AWS SageMaker notebook or script environment
- Power BI Desktop connected to Databricks
- CMS Medicare public use source files for the selected reporting years

## End-to-End Execution Flow

### Step 1 — Ingest Raw CMS Data into Databricks Bronze

Load multi-year CMS Medicare source CSV files into the Bronze layer.

Expected Bronze table:
- `cms_medical_data.bronze.cms_prov_svc_raw`

Key task:
- append `reporting_year`
- preserve raw columns as close to source as possible

## Step 2 — Build Silver Layer with dbt

Run dbt to standardize and type the Bronze data into a validated Silver model.

Primary Silver table:
- `cms_medical_data.silver.silver_cms_prov_svc`

Key task:
- cast numeric fields
- clean column names
- standardize provider/service-level data

Example command:
```bash
dbt run --select silver_cms_prov_svc

### Step 3 — Build Gold Layer with dbt

Run dbt Gold models to create analytics-ready and ML-ready feature tables.

Primary Gold tables:
- `cms_medical_data.gold.gold_regression_features`
- `cms_medical_data.gold.gold_state_year_payment_trend`

Example command:

    dbt run --select gold_regression_features gold_state_year_payment_trend

### Step 4 — Run dbt Tests

Validate source, Silver, and Gold models.

Example command:

    dbt test

Focus areas:
- null checks
- accepted values
- schema consistency
- model integrity

### Step 5 — Export Gold Datasets for ML

Publish Gold datasets to S3 for SageMaker workflows.

Example feature paths:
- `s3://cms-medical-rwe-suvin-eu-west-2/ml/data/2026-03-03_v1/gold_regression_features.csv`
- `s3://cms-medical-rwe-suvin-eu-west-2/ml/data/2026-03-03_v1/gold_state_year_payment_trend.csv`

### Step 6 — Train Regression Model

Use the regression feature dataset to train a payment prediction model.

Target:
- `target_avg_payment_amt`

Output:
- trained model artifact
- metrics JSON
- optional feature importance output

Expected model artifact path:
- `s3://cms-medical-rwe-suvin-eu-west-2/ml/models/regression/2026-03-03_v1/model.joblib`

### Step 7 — Train Time-Series / Time-Aware Model

Use the state-year payment trend dataset to train a time-aware model.

Output:
- trained model artifact
- evaluation metrics

Expected model artifact path:
- `s3://cms-medical-rwe-suvin-eu-west-2/ml/models/timeseries/2026-03-03_v1/model.joblib`

### Step 8 — Run Batch Inference

Generate predictions from the regression model and write them to CSV.

Expected prediction output:
- `predictions.csv`

Expected S3 path:
- `s3://cms-medical-rwe-suvin-eu-west-2/ml/predictions/regression/2026-03-03_v1/predictions.csv`

### Step 9 — Load Predictions Back into Databricks

Create or refresh the Databricks prediction table used for BI reporting.

Target table:
- `cms_medical_data.gold.gold_regression_predictions`

Purpose:
- enable actual vs predicted reporting
- serve ML output to Power BI in the same semantic layer as Gold analytics tables

### Step 10 — Refresh Power BI Dashboard

Power BI consumes:
- `gold_regression_features`
- `gold_state_year_payment_trend`
- `gold_regression_predictions`

Final dashboard pages:
1. Executive Overview
2. State-Year Trends
3. Detailed Drilldown
4. ML Prediction Performance

## Validation Checklist

Before considering the project run complete, verify:

- Bronze table loaded successfully
- Silver table built successfully
- Gold tables built successfully
- dbt tests passed
- Gold datasets exported to S3
- model artifacts written to S3
- predictions.csv generated
- predictions loaded into Databricks
- Power BI visuals refresh successfully
- ML metrics visible on the final dashboard page

## Expected Outputs

### Databricks
- Bronze raw table
- Silver cleaned table
- Gold feature and trend tables
- Gold prediction table

### S3
- versioned feature CSV files
- model artifacts
- metrics files
- batch prediction CSV

### Power BI
- 4-page dashboard
- actual vs predicted comparisons
- error metrics
- trend and drilldown reporting

## Future Automation Opportunities

The current workflow can be extended with:

- orchestration via Airflow or AWS Step Functions
- CI/CD for dbt and ML workflows
- model registry and monitoring
- scheduled dashboard refresh and data publication