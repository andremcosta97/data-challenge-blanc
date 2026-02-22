WITH countries AS (
    SELECT DISTINCT
        country,
        region,
        state,
        city,
        COALESCE(postal_code, -99) AS postal_code
    FROM {{ ref('stg__orders') }}
)
SELECT
    ROW_NUMBER() OVER (
        ORDER BY country, state, city, postal_code
    ) AS country_sk,
    country,
    region,
    state,
    city,
    postal_code
FROM countries