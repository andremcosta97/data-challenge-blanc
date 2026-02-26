SELECT
    d.year_month,
    {{ agg_global_metric(groupby='monthly_') }}
FROM {{ ref('fct__orders') }} f
LEFT JOIN {{ ref('dim_date') }} d
    ON f.order_date_sk = d.date_sk
WHERE f.shipping_time_days IS NOT NULL
GROUP BY 1
ORDER BY 1