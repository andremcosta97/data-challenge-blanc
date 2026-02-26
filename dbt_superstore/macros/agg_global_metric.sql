{% macro agg_global_metric(groupby = '') %}

ROUND(AVG(f.shipping_time_days), 2) AS {{ groupby }}avg_shipping_time,
SUM(f.sales) AS {{ groupby }}total_revenue,
SUM(f.profit) AS {{ groupby }}total_profit,
SUM(f.quantity) AS {{ groupby }}total_quantity,
SUM(
    CASE
        WHEN f.is_returned = TRUE
        THEN f.quantity 
        ELSE 0
    END
) AS {{ groupby }}total_returns,
ROUND(
    SUM(
        CASE
            WHEN f.is_returned = TRUE
            THEN f.quantity  
            ELSE 0
        END
    ) * 100.0 / NULLIF(SUM(f.quantity), 0), 2
) AS {{ groupby }}return_rate_pct

{% endmacro %}