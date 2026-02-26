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

    total_revenue = total_metrics_df["overall_total_revenue"][0]
    total_profit = total_metrics_df["overall_total_profit"][0]
    total_cost = total_metrics_df["overall_total_cost"][0]
    gross_margin = total_metrics_df["overall_gross_margin"][0]
    total_returns = total_metrics_df["overall_total_returns"][0]

    st.metric(label="Total Revenue", value=f"${total_revenue:,}")
    st.metric(label="Total Profit", value=f"${total_profit:,}")
    st.metric(label="Total Cost", value=f"${total_cost:,}")
    st.metric(label="Total Returns", value=f"{total_returns:,}")
    st.metric(label="Gross Margin %", value=f"{gross_margin:.2f}%")


    ## BAR CHART: TOP 10 Total Return products
    top_returns_query = """
    SELECT 
        product_name,
        total_returns,
        return_rate_pct
    FROM analytics_marts.agg_returns_products
    LIMIT 10;
    """

    top_returns_df = pd.read_sql(top_returns_query, con=engine)

    # frist bar chart with total returns count
    fig_top_returns_value = px.bar(
        top_returns_df,
        x="total_returns",
        y="product_name",
        title="Top 10 Products by Total Returns (Count)"
    )

    st.plotly_chart(fig_top_returns_value, use_container_width=True)

    # second bar chart with return rate percentage
    fig_top_returns_value = px.bar(
        top_returns_df,
        x="return_rate_pct",
        y="product_name",
        title="Top 10 Products by Total Returns (Rate %)"
    )

    st.plotly_chart(fig_top_returns_value, use_container_width=True)

    ## LINE PLOT: Monthly Average Shipping Time
    monthly_query = """
    SELECT
        year_month,
        monthly_avg_shipping_time,
        monthly_total_revenue
    FROM analytics_marts.agg_year_month
    """

    monthly_agg_df = pd.read_sql(monthly_query, con=engine)

    fig_shipping = px.line(
        monthly_agg_df,
        x="year_month",
        y="monthly_avg_shipping_time",
        title="Monthly Average Shipping Time (Days)",
        markers=True
    )

    st.plotly_chart(fig_shipping, use_container_width=True)

    ## LINE PLOT: Monthly Sales Trend

    fig_monthly = px.line(
        monthly_agg_df,
        x="year_month",
        y="monthly_total_revenue",
        title="Monthly Sales Trend",
        markers=True
    )

    st.plotly_chart(fig_monthly, use_container_width=True)
    
    # BAR PLOT: Yearly Quarterly Revenue Trend by Category
    quarter_query = """
    SELECT
        year_quarter,
        category,
        year_quarter_total_revenue AS revenue
    FROM analytics_marts.agg_year_quarter_category
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

    ## BAR PLOT: Top 5 States + Others by Revenue by year
    top5_states_year_query = """
    SELECT 
        year,
        state,
        total_revenue
    FROM analytics_marts.top_5_state_sales_by_year
    """

    top5_states_year_df = pd.read_sql(top5_states_year_query, con=engine)

    # Plot grouped bar chart
    fig_top5_states_year = px.bar(
        top5_states_year_df,
        x="year",
        y="total_revenue",
        color="state",
        title="Top 5 States by Revenue per Year"
    )

    st.plotly_chart(fig_top5_states_year, use_container_width=True)

    

    # Dispose the engine when done
    engine.dispose()
