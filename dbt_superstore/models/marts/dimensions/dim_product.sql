WITH products AS (
    SELECT DISTINCT
        product_id,
        product_name,
        category,
        sub_category
    FROM {{ ref('stg__orders') }}
)
SELECT
    ROW_NUMBER() OVER (ORDER BY product_id) AS product_sk,
    product_id,
    product_name,
    category,
    sub_category
FROM products