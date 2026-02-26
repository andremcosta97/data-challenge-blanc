SELECT
    o.order_sk,
    o.order_id,
    c.customer_id,
    country.country_sk,
    p.product_sk,
    d_order.date_sk AS order_date_sk,
    d_ship.date_sk AS ship_date_sk,
    o.ship_date - o.order_date AS shipping_time_days,
    o.ship_mode,
    o.sales,
    o.profit,
    o.quantity,
    o.discount,
    r.is_returned
FROM {{ ref('stg__orders') }} o
LEFT JOIN {{ ref('dim_customer') }} c
    ON o.customer_id = c.customer_id
LEFT JOIN {{ ref('dim_product') }} p
    ON o.product_id = p.product_id
    AND o.category = p.category
    AND o.sub_category = p.sub_category
    AND o.product_name = p.product_name
LEFT JOIN {{ ref('stg__returns') }} r
    ON o.order_id = r.order_id
LEFT JOIN {{ ref('dim_country') }} country
    ON o.country = country.country
   AND o.state = country.state
   AND o.city = country.city
   AND COALESCE(o.postal_code, -99) = country.postal_code
   and o.region = country.region
LEFT JOIN {{ ref('dim_date') }} d_order
    ON o.order_date = d_order.full_date
LEFT JOIN {{ ref('dim_date') }} d_ship
    ON o.ship_date = d_ship.full_date
