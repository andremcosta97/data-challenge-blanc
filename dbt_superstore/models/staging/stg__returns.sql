WITH returns AS (
    SELECT 
        "Order ID"::TEXT AS "order_id",
        "Returned"::BOOLEAN AS is_returned
    FROM {{ source('raw', 'returns') }}
)
SELECT 
    distinct
    *
FROM returns