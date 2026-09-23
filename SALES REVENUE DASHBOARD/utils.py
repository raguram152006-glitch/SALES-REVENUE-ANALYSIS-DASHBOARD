"""
Utility & Data Processing Module for Streamlit Sales & Revenue Dashboard
Contains caching, data filtering, KPI metric calculations, growth deltas, and helper functions.
"""

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
from data_generator import get_or_create_dataset

@st.cache_data(show_spinner="Loading Sales Dataset...")
def load_sales_data(filepath: str = "data/sales_data.csv", force_recreate: bool = False) -> pd.DataFrame:
    """Load sales data with caching."""
    df = get_or_create_dataset(filepath=filepath, force_recreate=force_recreate)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

def apply_filters(
    df: pd.DataFrame,
    start_date: datetime.date = None,
    end_date: datetime.date = None,
    regions: list = None,
    categories: list = None,
    products: list = None,
    customer_types: list = None,
    order_statuses: list = None
) -> pd.DataFrame:
    """Apply interactive sidebar filters to dataframe."""
    filtered_df = df.copy()

    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df["Order Date"].dt.date >= start_date) &
            (filtered_df["Order Date"].dt.date <= end_date)
        ]

    if regions:
        filtered_df = filtered_df[filtered_df["Region"].isin(regions)]

    if categories:
        filtered_df = filtered_df[filtered_df["Category"].isin(categories)]

    if products:
        filtered_df = filtered_df[filtered_df["Product Name"].isin(products)]

    if customer_types:
        filtered_df = filtered_df[filtered_df["Customer Type"].isin(customer_types)]

    if order_statuses:
        filtered_df = filtered_df[filtered_df["Order Status"].isin(order_statuses)]

    return filtered_df

def calculate_kpis(df_current: pd.DataFrame, df_baseline: pd.DataFrame = None):
    """
    Calculate core KPI metrics and growth percentage compared to baseline dataframe.
    Returns dictionary with raw values, formatted values, and percentage deltas.
    """
    if df_current.empty:
        return {
            "total_sales": 0.0,
            "total_profit": 0.0,
            "total_orders": 0,
            "aov": 0.0,
            "profit_margin": 0.0,
            "sales_delta": 0.0,
            "profit_delta": 0.0,
            "orders_delta": 0.0,
            "aov_delta": 0.0,
            "margin_delta": 0.0,
        }

    total_sales = df_current["Sales Revenue"].sum()
    total_profit = df_current["Profit"].sum()
    total_orders = df_current["Order ID"].nunique()
    aov = total_sales / total_orders if total_orders > 0 else 0.0
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0.0

    # Baseline comparison metrics
    sales_delta = 0.0
    profit_delta = 0.0
    orders_delta = 0.0
    aov_delta = 0.0
    margin_delta = 0.0

    if df_baseline is not None and not df_baseline.empty:
        b_sales = df_baseline["Sales Revenue"].sum()
        b_profit = df_baseline["Profit"].sum()
        b_orders = df_baseline["Order ID"].nunique()
        b_aov = b_sales / b_orders if b_orders > 0 else 0.0
        b_margin = (b_profit / b_sales * 100) if b_sales > 0 else 0.0

        sales_delta = ((total_sales - b_sales) / b_sales * 100) if b_sales > 0 else 0.0
        profit_delta = ((total_profit - b_profit) / abs(b_profit) * 100) if b_profit != 0 else 0.0
        orders_delta = ((total_orders - b_orders) / b_orders * 100) if b_orders > 0 else 0.0
        aov_delta = ((aov - b_aov) / b_aov * 100) if b_aov > 0 else 0.0
        margin_delta = profit_margin - b_margin

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "total_orders": total_orders,
        "aov": aov,
        "profit_margin": profit_margin,
        "sales_delta": sales_delta,
        "profit_delta": profit_delta,
        "orders_delta": orders_delta,
        "aov_delta": aov_delta,
        "margin_delta": margin_delta,
    }

def format_currency(val: float) -> str:
    """Format numeric values as concise readable currency string."""
    if abs(val) >= 1_000_000:
        return f"${val / 1_000_000:,.2f}M"
    elif abs(val) >= 1_000:
        return f"${val / 1_000:,.1f}K"
    else:
        return f"${val:,.2f}"

def format_number(val: int) -> str:
    """Format integer counts with thousand separators."""
    if abs(val) >= 1_000_000:
        return f"{val / 1_000_000:,.2f}M"
    elif abs(val) >= 1_000:
        return f"{val / 1_000:,.1f}K"
    else:
        return f"{val:,}"
