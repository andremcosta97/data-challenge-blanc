SELECT
    CONCAT(dd.year, '-Q', dd.quarter) AS year_quarter,
    dp.category,
    {{ agg_global_metric(groupby='year_quarter_') }}
FROM analytics_marts.fct__orders f
LEFT JOIN analytics_marts.dim_date dd
    ON f.order_date_sk = dd.date_sk
LEFT JOIN analytics_marts.dim_product dp
    ON f.product_sk = dp.product_sk
GROUP BY 1,2
ORDER BY 1,2