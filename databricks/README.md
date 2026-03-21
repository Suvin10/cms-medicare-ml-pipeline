# Databricks Layer

## Workspace Notes

This project used a restricted Databricks environment with:

- serverless SQL / serverless notebook environment
- no all-purpose cluster creation
- no Unity Catalog External Data admin permissions

Because of that:

- Bronze ingestion used Databricks UI staging + SQL union
- Gold-to-S3 publishing used controlled CSV export + AWS CLI upload
- direct Databricks→S3 external location integration was not possible in this workspace

## Catalog / Schemas

- Catalog: `cms_medical_data`
- Schemas:
  - `bronze`
  - `silver`
  - `gold`
  - `default` (temporary staging)

## SQL Warehouse Connection (documentation only)

Used for:

- dbt profile setup
- Power BI DirectQuery connection

Document only:

- Hostname format: `dbc-<workspace>.cloud.databricks.com`
- HTTP Path format: `/sql/1.0/warehouses/<warehouse_id>`

Do not commit:

- real tokens
- real secrets
- user-specific connection files

## Final Tables

- `cms_medical_data.bronze.cms_prov_svc_raw`
- `cms_medical_data.silver.silver_cms_prov_svc`
- `cms_medical_data.gold.gold_regression_features`
- `cms_medical_data.gold.gold_state_year_payment_trend`
- `cms_medical_data.gold.gold_regression_predictions`