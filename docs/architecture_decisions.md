# Architecture Decisions

## 1. Multi-Year Dataset Strategy
Decision:
- use 2021, 2022, 2023 files
- add `reporting_year` at ingestion time

Why:
- supports time-aware analysis
- stronger than a single-year regression-only project

## 2. Medallion Architecture
Decision:
- Bronze = raw multi-year CMS samples
- Silver = cleaned, typed, standardized dataset
- Gold = aggregated ML/BI feature layer

Why:
- reproducibility
- easier debugging
- clean separation of concerns

## 3. Databricks / dbt Schema Handling
Decision:
- use `cms_medical_data` catalog
- override dbt schema concatenation with `generate_schema_name` macro

Why:
- avoid generated schemas like `bronze_silver`
- preserve clean `silver` and `gold` schema names

## 4. Export-to-S3 Design Under Workspace Constraints
Observed constraints:
- serverless only
- no all-purpose clusters
- no Unity Catalog external data permissions

Decision:
- publish Gold datasets via controlled CSV export + AWS CLI upload

Why:
- direct Databricks→S3 external location pattern was not possible in this workspace
- CSV handoff still preserved reproducibility and versioning

## 5. Regression Target Selection
Decision:
- target = `target_avg_payment_amt`

Why:
- strong business relevance
- stable label at Gold layer
- easy to explain in healthcare reimbursement terms

## 6. Why Linear Regression Outperformed XGBoost
Observation:
- Linear regression strongly outperformed XGBoost

Why:
- payment is highly driven by allowed amount
- reimbursement logic is largely linear
- interpretability is valuable in healthcare

## 7. Time-Aware Model Selection
Decision:
- use RandomForestRegressor over a tiny 3-year state-year panel

Why:
- only 3 annual observations per state
- insufficient sequence depth for robust classical or deep forecasting claims
- still supports valid time-aware prediction use case

## 8. S3 as Feature Store + Model Registry
Decision:
- store datasets, models, metrics, predictions in versioned S3 prefixes

Why:
- reproducibility
- simple registry pattern
- auditable ML lifecycle

## 9. Power BI DirectQuery
Decision:
- use DirectQuery to Databricks SQL Warehouse

Why:
- more enterprise-aligned than import mode
- supports warehouse-backed analytics
- avoids stale local copies

## 10. Prediction Table for BI
Decision:
- serve predictions as a Databricks-facing table when possible

Why:
- makes ML outputs available to BI users in same semantic layer as Gold tables