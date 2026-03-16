# CMS Medicare Analytics + ML Pipeline
**Databricks + dbt + AWS SageMaker + Power BI**

End-to-end analytics and machine learning project built on CMS Medicare public use data to create a modern data platform and reporting layer for reimbursement analysis, trend monitoring, and prediction performance evaluation.

## Project Overview

This project implements a full data-to-dashboard workflow using Databricks, dbt, AWS SageMaker, S3, and Power BI.

The pipeline ingests CMS Medicare public use data into Databricks, transforms it through a Bronze → Silver → Gold architecture, engineers analytics-ready features, trains machine learning models in SageMaker, generates batch predictions, loads prediction outputs back into Databricks, and exposes curated Gold tables to Power BI for executive dashboarding and model performance analysis.

## Results Snapshot

- Built Databricks Bronze → Silver → Gold analytical models using dbt
- Created Gold tables for regression features, state-year payment trends, and prediction outputs
- Trained AWS SageMaker regression and time-series models
- Generated batch predictions and loaded them back into Databricks for BI consumption
- Built a 4-page Power BI dashboard for executive analytics and ML performance reporting

### Example ML Metrics
- **MAE:** 2.58
- **MAPE:** 2.81%
- **Prediction Bias:** -0.25

## Business Goal

The objective of this project is to build a scalable analytics and ML workflow for Medicare provider service data that can:

- analyze reimbursement and utilization patterns
- monitor payment trends across states and provider types
- predict average payment amounts using regression
- support time-series trend analysis
- surface insights through an executive-style Power BI dashboard

## What I Built

In this project, I designed and implemented:

- a Databricks Medallion architecture for CMS Medicare data
- dbt transformations and schema tests for Silver and Gold analytical models
- Gold-layer feature tables for machine learning and reporting
- AWS SageMaker regression and time-series workflows
- a batch inference pipeline producing prediction outputs
- Power BI dashboards for Medicare payment analytics, utilization trends, and ML model evaluation

## Architecture Diagram

![Architecture Diagram](architecture/architecture_diagram.png)

## Architecture

### End-to-End Flow

1. CMS Medicare public use data ingested into Databricks Bronze layer  
2. Bronze data cleaned and standardized into Silver layer  
3. dbt transforms Silver tables into Gold analytics-ready models  
4. Gold features exported and stored for machine learning workflows  
5. AWS SageMaker trains:
   - a regression model for average payment prediction
   - a time-series model for trend analysis  
6. Batch inference pipeline generates prediction outputs  
7. Prediction outputs loaded back into Databricks Gold layer  
8. Power BI connects to Databricks and visualizes:
   - payment trends
   - provider and service patterns
   - actual vs predicted performance
   - model evaluation metrics

## Tech Stack

- **Databricks** for lakehouse storage and transformation
- **Delta Lake** for managed analytical tables
- **dbt** for SQL-based transformations, testing, and documentation
- **AWS S3** for intermediate storage and feature data
- **AWS SageMaker** for regression and time-series modeling
- **Python** for ML workflows and batch inference
- **SQL** for analytics models and transformations
- **Power BI** for executive dashboarding

## Data Model

### Bronze
Raw CMS Medicare provider and service data ingested into Databricks.

### Silver
Cleaned, standardized, and validated provider-service level dataset.

### Gold
Business-ready tables used for reporting and machine learning:

- `gold_regression_features`
- `gold_state_year_payment_trend`
- `gold_regression_predictions`

## Machine Learning Components

### 1. Regression Model
Used to predict:

- `target_avg_payment_amt`

Regression output includes:

- actual payment
- predicted payment
- evaluation metrics surfaced in Power BI

### 2. Time-Series / Trend Modeling
Used to analyze state-year payment trends and support forecasting-oriented reporting.

## Power BI Dashboard

The Power BI layer is built directly on curated Databricks Gold tables and includes 4 report pages.

### Page 1 — Executive Overview
Purpose:
- summarize Medicare payment and utilization metrics
- compare payment totals across states, provider types, and place of service

Main visuals:
- KPI cards for actual payment, services, beneficiaries, providers, and averages
- actual payment by state
- actual payment by provider type
- actual payment by place of service
- total services by state

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
- detailed table with provider and service-level aggregate metrics
- slicers for year, state, provider type, and place of service

### Page 4 — ML Prediction Performance
Purpose:
- evaluate regression model performance using actual and predicted payment values

Main visuals:
- total actual vs total predicted payment
- prediction error
- MAE
- MAPE
- prediction bias
- actual vs predicted by state
- actual vs predicted by provider type
- scatter plot for actual vs predicted fit
- largest prediction errors table

## Dashboard Screenshots

### Executive Overview
![Executive Overview](dashboard/screenshots/page1_executive_overview.png)

### State-Year Trends
![State-Year Trends](dashboard/screenshots/page2_state_year_trends.png)

### Detailed Drilldown
![Detailed Drilldown](dashboard/screenshots/page3_detailed_drilldown.png)

### ML Prediction Performance
![ML Prediction Performance](dashboard/screenshots/page4_ml_prediction_performance.png)

## Model Metrics

Model evaluation surfaced in the Power BI dashboard includes:

- **Prediction Error**
- **MAE (Mean Absolute Error)**
- **MAPE (Mean Absolute Percentage Error)**
- **Prediction Bias**

These metrics help assess:
- average magnitude of model error
- relative percentage error
- whether predictions systematically overpredict or underpredict

## Data Access

Raw CMS Medicare source data is not stored in this repository due to file size and repository hygiene.

Official source links:
- [CMS Data Portal](https://data.cms.gov/)
- [Medicare Provider Charge Data](https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data)

This project uses publicly available CMS Medicare data as the Bronze-layer source for downstream Databricks, dbt, SageMaker, and Power BI workflows.

## Repository Structure

```text
cms-medicare-ml-pipeline/
├── README.md
├── architecture/
│   └── architecture_diagram.png
├── dashboard/
│   └── screenshots/
│       ├── page1_executive_overview.png
│       ├── page2_state_year_trends.png
│       ├── page3_detailed_drilldown.png
│       └── page4_ml_prediction_performance.png
├── dbt/
│   └── cms_medical_dbt/
│       ├── dbt_project.yml
│       ├── models/
│       │   ├── bronze/
│       │   ├── silver/
│       │   └── gold/
│       ├── macros/
│       ├── tests/
│       └── packages.yml
├── docs/
│   ├── data_dictionary.md
│   └── model_metrics.md
├── powerbi/
│   └── dashboard_notes.md
├── sagemaker/
│   └── README.md