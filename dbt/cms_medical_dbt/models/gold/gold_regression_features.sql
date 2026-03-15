{{ config(materialized='table', schema='gold') }}

with s as (
  select *
  from {{ ref('silver_cms_prov_svc') }}
)

select
  reporting_year,
  provider_state,
  provider_type,
  place_of_service,

  count(*) as provider_service_rows,
  count(distinct rendering_npi) as distinct_providers,
  count(distinct hcpcs_code) as distinct_hcpcs_codes,

  sum(total_beneficiaries) as total_beneficiaries,
  sum(total_services) as total_services,

  avg(avg_submitted_charge) as avg_submitted_charge_mean,
  avg(avg_medicare_allowed_amt) as avg_allowed_amt_mean,

  -- TARGET for regression
  avg(avg_medicare_payment_amt) as target_avg_payment_amt

from s
group by 1,2,3,4