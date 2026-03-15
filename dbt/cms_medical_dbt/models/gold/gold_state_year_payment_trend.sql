{{ config(materialized='table', schema='gold') }}

with s as (
  select *
  from {{ ref('silver_cms_prov_svc') }}
)

select
  reporting_year,
  provider_state,

  sum(total_services) as total_services,
  sum(total_beneficiaries) as total_beneficiaries,

  avg(avg_medicare_payment_amt) as avg_payment_amt,
  avg(avg_medicare_standardized_amt) as avg_standardized_amt

from s
group by 1,2