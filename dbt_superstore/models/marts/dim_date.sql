WITH date_series AS (
    SELECT 
        generate_series(
            '2018-01-01'::date,
            '2022-12-31'::date,
            interval '1 day'
        )::date AS full_date
)

SELECT
    TO_CHAR(full_date, 'YYYYMMDD')::int AS date_sk,
    full_date,
    EXTRACT(YEAR FROM full_date) AS year,
    EXTRACT(QUARTER FROM full_date) AS quarter,
    EXTRACT(MONTH FROM full_date) AS month,
    TO_CHAR(full_date, 'Month') AS month_name,
    EXTRACT(WEEK FROM full_date) AS week,
    EXTRACT(DAY FROM full_date) AS day,
    EXTRACT(DOW FROM full_date) AS day_of_week,
    TO_CHAR(full_date, 'Day') AS day_name,
    CASE 
        WHEN EXTRACT(DOW FROM full_date) IN (0,6) THEN TRUE
        ELSE FALSE
    END AS is_weekend
FROM date_series
ORDER BY full_date