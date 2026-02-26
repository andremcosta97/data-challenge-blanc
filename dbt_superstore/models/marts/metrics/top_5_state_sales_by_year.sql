WITH ranked_states AS (
    SELECT
        dd.year,
        dc.state,
        SUM(f.sales) AS total_revenue,
        ROW_NUMBER() OVER (PARTITION BY dd.year ORDER BY SUM(f.sales) DESC) AS rank
    FROM analytics_marts.fct__orders f
    JOIN analytics_marts.dim_country dc
        ON f.country_sk = dc.country_sk
    JOIN analytics_marts.dim_date dd
        ON f.order_date_sk = dd.date_sk
    GROUP BY 1, 2
),
clean_states AS (
    SELECT
        year,
        CASE
            WHEN rank <= 5
                THEN state 
                ELSE 'Others'
        END AS state,
        SUM(total_revenue) AS total_revenue
    FROM ranked_states
    GROUP BY 1,2
)
SELECT 
    year,
    state,
    total_revenue
FROM clean_states
ORDER BY year, total_revenue DESC