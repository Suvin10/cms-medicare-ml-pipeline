{{ config(materialized='view', schema='silver') }}

with src as (
    select *
    from {{ source('cms_bronze', 'cms_prov_svc_raw') }}
),

cleaned as (
    select
        cast(reporting_year as int) as reporting_year,

        cast(Rndrng_NPI as bigint) as rendering_npi,
        trim(Rndrng_Prvdr_Last_Org_Name) as provider_last_or_org_name,
        trim(Rndrng_Prvdr_First_Name) as provider_first_name,
        trim(Rndrng_Prvdr_MI) as provider_middle_initial,
        trim(Rndrng_Prvdr_Crdntls) as provider_credentials,
        trim(Rndrng_Prvdr_Ent_Cd) as provider_entity_code,
        trim(Rndrng_Prvdr_City) as provider_city,
        trim(Rndrng_Prvdr_State_Abrvtn) as provider_state,
        cast(Rndrng_Prvdr_Zip5 as string) as provider_zip5,
        trim(Rndrng_Prvdr_Cntry) as provider_country,
        trim(Rndrng_Prvdr_Type) as provider_type,

        trim(HCPCS_Cd) as hcpcs_code,
        trim(HCPCS_Desc) as hcpcs_description,
        trim(Place_Of_Srvc) as place_of_service,

        cast(Tot_Benes as bigint) as total_beneficiaries,
        cast(Tot_Srvcs as double) as total_services,

        -- money columns: strip $ and commas then cast
        cast(regexp_replace(Avg_Sbmtd_Chrg, '[$,]', '') as double) as avg_submitted_charge,
        cast(regexp_replace(Avg_Mdcr_Alowd_Amt, '[$,]', '') as double) as avg_medicare_allowed_amt,
        cast(regexp_replace(Avg_Mdcr_Pymt_Amt, '[$,]', '') as double) as avg_medicare_payment_amt,
        cast(regexp_replace(Avg_Mdcr_Stdzd_Amt, '[$,]', '') as double) as avg_medicare_standardized_amt
    from src
)

select * from cleaned