WITH customers AS (
    SELECT DISTINCT
        customer_id,
        customer_name,
        segment
    FROM {{ ref('stg__orders') }}
)
SELECT
    customer_id,
    customer_name,
    segment
FROM customers