SELECT
    sum(sales) AS total_revenue,
    sum(profit) AS total_profit,
    sum(sales) - sum(profit) AS total_cost,
    sum(profit) / nullif(sum(sales),0) * 100 AS gross_margin,
    sum(case when is_returned then 1 else 0 end) AS total_returns
FROM {{ ref('fct__orders') }}