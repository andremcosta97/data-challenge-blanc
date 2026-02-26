SELECT
    {{ agg_global_metric(groupby='overall_') }},
    SUM(f.sales) - SUM(f.profit) AS overall_total_cost,
    SUM(f.profit) / nullif(SUM(f.sales),0) * 100 AS overall_gross_margin
FROM {{ ref('fct__orders') }} f