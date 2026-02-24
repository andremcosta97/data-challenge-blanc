import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px


def create_engine_connection():
    try:
        # Define connection URL in the format: 'postgresql+psycopg2://user:password@host/database'
        engine = create_engine("postgresql+psycopg2://analytics:analytics@localhost/superstore")
        print("PostgreSQL connection engine created")
        return engine
    except Exception as e:
        print("Error creating engine:", e)
        return None


engine = create_engine_connection()
if engine:
    st.success("PostgreSQL connection engine created successfully")
    # Example query using pandas
    query_fact_orders = """
    SELECT
        f.order_id,
        d.full_date AS order_date,
        d2.full_date AS ship_date,
        f.shipping_time_days,
        f.product_sk,
        c.country,
        c.state,
        c.city,
        f.ship_mode,
        f.sales,
        f.quantity,
        f.discount,
        f.profit,
        f.is_returned
    FROM analytics_marts.fct__orders f
    LEFT JOIN analytics_marts.dim_date d
        ON f.order_date_sk = d.date_sk
    LEFT JOIN analytics_marts.dim_date d2
        ON f.ship_date_sk = d2.date_sk
    Left JOIN analytics_marts.dim_country c
        ON f.country_sk = c.country_sk
    """
    df = pd.read_sql(query_fact_orders, con=engine)
    st.write(df)

    # METRIC: TOTAL REVENUE
    total_metrics_query = """
    SELECT * 
    FROM analytics_marts.agg_overall_kpis;
    """

    total_metrics_df = pd.read_sql(total_metrics_query, con=engine)

    total_revenue = total_metrics_df["total_revenue"][0]
    total_profit = total_metrics_df["total_profit"][0]
    total_cost = total_metrics_df["total_cost"][0]
    gross_margin = total_metrics_df["gross_margin"][0]
    total_returns = total_metrics_df["total_returns"][0]

    st.metric(label="Total Revenue", value=f"${total_revenue:,}")
    st.metric(label="Total Profit", value=f"${total_profit:,}")
    st.metric(label="Total Cost", value=f"${total_cost:,}")
    st.metric(label="Total Returns", value=f"{total_returns:,}")
    st.metric(label="Gross Margin %", value=f"{gross_margin:.2f}%")


    ## BAR CHART: TOP 5 Return products
    top_returns_query = """
    SELECT
        p.product_name,
        SUM(f.quantity) AS total_returns
    FROM analytics_marts.fct__orders f
    LEFT JOIN analytics_marts.dim_product p
        ON f.product_sk = p.product_sk
    WHERE f.is_returned = TRUE
    GROUP BY p.product_name
    ORDER BY total_returns DESC
    LIMIT 5;
    """

    top_returns_df = pd.read_sql(top_returns_query, con=engine)

    # Horizontal bar chart
    fig_top_returns_value = px.bar(
        top_returns_df,
        x="total_returns",
        y="product_name",
        title="Top 5 Products by Returns (Count)"
    )

    st.plotly_chart(fig_top_returns_value, use_container_width=True)

    ## LINE PLOT: Monthly Average Shipping Time
    monthly_shipping_query = """
    SELECT
        d.year_month,
        AVG(f.shipping_time_days) AS avg_shipping_time
    FROM analytics_marts.fct__orders f
    LEFT JOIN analytics_marts.dim_date d
        ON f.order_date_sk = d.date_sk
    WHERE f.shipping_time_days IS NOT NULL
    GROUP BY 1
    ORDER BY 1
    """

    monthly_shipping_df = pd.read_sql(monthly_shipping_query, con=engine)

    fig_shipping = px.line(
        monthly_shipping_df,
        x="year_month",
        y="avg_shipping_time",
        title="Monthly Average Shipping Time (Days)",
        markers=True
    )

    st.plotly_chart(fig_shipping, use_container_width=True)

    ## LINE PLOT: Monthly Sales Trend
    monthly_sales_query = """
    SELECT
        d.year_month,
        SUM(f.sales) AS monthly_sales
    FROM analytics_marts.fct__orders f
    LEFT JOIN analytics_marts.dim_date d
        ON f.order_date_sk = d.date_sk
    GROUP BY 1
    ORDER BY 1
    """

    monthly_sales_df = pd.read_sql(monthly_sales_query, con=engine)

    fig_monthly = px.line(
        monthly_sales_df,
        x="year_month",
        y="monthly_sales",
        title="Monthly Sales Trend",
        markers=True
    )

    st.plotly_chart(fig_monthly, use_container_width=True)
    
    # BAR PLOT: Yearly Quarterly Revenue Trend by Category
    quarter_query = """
    SELECT
        CONCAT(dd.year, '-Q', dd.quarter) AS year_quarter,
        dp.category,
        SUM(f.sales) AS revenue
    FROM analytics_marts.fct__orders f
    LEFT JOIN analytics_marts.dim_date dd
        ON f.order_date_sk = dd.date_sk
    LEFT JOIN analytics_marts.dim_product dp
        ON f.product_sk = dp.product_sk
    GROUP BY 1,2
    ORDER BY 1,2
    """ 
    quarter_df = pd.read_sql(quarter_query, con=engine)

    fig_quarter = px.bar(
        quarter_df,
        x="year_quarter",
        y="revenue",
        color="category",
        barmode="group",
        title="Yearly Quarter Revenue Trend by Category"
    )

    st.plotly_chart(fig_quarter, use_container_width=True)

    ## BAR PLOT: Top 5 States by Revenue
    top_states_query = """
    SELECT
        c.state,
        SUM(f.sales) AS total_revenue
    FROM analytics_marts.fct__orders f
    JOIN analytics_marts.dim_country c
        ON f.country_sk = c.country_sk
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 5;
    """

    top_states_df = pd.read_sql(top_states_query, con=engine)

    fig_states = px.bar(
        top_states_df,
        x="total_revenue",
        y="state",
        orientation="h",
        title="Top 5 States by Revenue",
        text=top_states_df["total_revenue"].apply(lambda x: f"${x:,.0f}")
    )

    st.plotly_chart(fig_states, use_container_width=True)

    ## BAR PLOT: Top 5 States by Revenue by year
    top5_states_year_query = """
    WITH ranked_states AS (
        SELECT
            dd.year,
            dc.state,
            SUM(f.sales) AS revenue,
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
            SUM(revenue) AS revenue
        FROM ranked_states
        GROUP BY 1,2
    )
    SELECT *
    FROM clean_states
    ORDER BY year, revenue DESC;
    """

    top5_states_year_df = pd.read_sql(top5_states_year_query, con=engine)

    # Plot grouped bar chart
    fig_top5_states_year = px.bar(
        top5_states_year_df,
        x="year",
        y="revenue",
        color="state",
        title="Top 5 States by Revenue per Year"
    )

    st.plotly_chart(fig_top5_states_year, use_container_width=True)

    

    # Dispose the engine when done
    engine.dispose()
