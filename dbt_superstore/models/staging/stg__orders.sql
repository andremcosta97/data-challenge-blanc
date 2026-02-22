WITH orders AS (
    SELECT
        "Order ID"::TEXT AS "order_id",
        CAST("Order Date" AS DATE) AS "order_date",
        CAST("Ship Date" AS DATE) AS "ship_date",
        "Ship Mode"::TEXT AS "ship_mode",
        "Customer ID"::TEXT AS "customer_id",
        "Customer Name"::TEXT AS "customer_name",
        "Segment"::TEXT AS "segment",
        "Country/Region"::TEXT AS "country",
        "City"::TEXT AS "city",
        "State"::TEXT AS "state",
        "Postal Code"::INT AS "postal_code",
        "Region"::TEXT AS "region",
        "Product ID"::TEXT AS "product_id",
        "Category"::TEXT AS "category",
        "Sub-Category"::TEXT AS "sub_category",
        "Product Name"::TEXT AS "product_name",
        ROUND("Sales"::NUMERIC, 2) AS "sales",
        "Quantity"::INT AS "quantity",
        ROUND("Discount"::NUMERIC, 2) AS "discount",
        ROUND("Profit"::NUMERIC, 2) AS "profit"
    FROM {{ source('raw', 'orders') }}
)
SELECT
    ROW_NUMBER() OVER () AS order_sk,
   *
FROM orders

