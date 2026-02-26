SELECT
    p.product_name,
    {{ agg_global_metric() }}
FROM {{ ref('fct__orders') }} f
LEFT JOIN {{ ref('dim_product') }} p
    ON f.product_sk = p.product_sk
GROUP BY p.product_name
ORDER BY total_returns DESC