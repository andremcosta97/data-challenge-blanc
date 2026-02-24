WITH source_count AS (
    SELECT COUNT(*) AS cnt
    FROM {{ ref('stg__orders') }}
),

fact_count AS (
    SELECT COUNT(*) AS cnt
    FROM {{ ref('fct__orders') }}
)

SELECT
    'Row count mismatch between stg__orders and fct__orders' AS error_message,
    source_count.cnt AS source_rows,
    fact_count.cnt AS fact_rows
FROM source_count ,fact_count 
where source_count.cnt != fact_count.cnt