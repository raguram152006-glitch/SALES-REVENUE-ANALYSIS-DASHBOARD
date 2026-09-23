"""
Automated Comprehensive Test Suite for Sales & Revenue Dashboard
Tests data loading, filter variations, KPI calculations, Plotly figures generation, and export utilities.
"""

import os
import sys
import pandas as pd
import numpy as np
import io
from datetime import date, datetime

# Add project root to sys.path
sys.path.insert(0, os.path.abspath("."))

from data_generator import generate_sales_data, get_or_create_dataset
from utils import load_sales_data, apply_filters, calculate_kpis, format_currency, format_number
from styles import get_custom_css, apply_plotly_theme, PALETTE, PRIMARY_COLOR, SUCCESS_COLOR, WARNING_COLOR, DANGER_COLOR, INFO_COLOR, PURPLE_COLOR
import plotly.express as px
import plotly.graph_objects as go

def run_all_tests():
    print("==================================================")
    print("[+] Running Comprehensive Dashboard Test Suite...")
    print("==================================================")

    # -------------------------------------------------------------------------
    # TEST 1: Synthetic Dataset Generation & Schema Validation
    # -------------------------------------------------------------------------
    print("\n[TEST 1] Testing Data Generator & CSV Loading...")
    df = get_or_create_dataset(force_recreate=True)
    assert not df.empty, "Dataset should not be empty!"
    assert len(df) == 5000, f"Expected 5000 records, got {len(df)}"
    
    required_cols = [
        "Order ID", "Order Date", "Year", "Month", "Quarter", "Customer Type",
        "Region", "Country", "City", "Category", "Sub-Category", "Product Name",
        "Unit Price", "Quantity", "Gross Sales", "Discount %", "Discount Amount",
        "Sales Revenue", "Unit Cost", "Total Cost", "Profit", "Profit Margin %",
        "Payment Method", "Order Status"
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing required column: {col}"
    print("  [PASS] Data Generator Test Passed! (5000 records, 24 columns)")

    # -------------------------------------------------------------------------
    # TEST 2: Filter Logic Tests
    # -------------------------------------------------------------------------
    print("\n[TEST 2] Testing Interactive Sidebar Filter Logic...")
    
    # 2a. Date Range Filter
    df_filtered_date = apply_filters(
        df,
        start_date=date(2024, 6, 1),
        end_date=date(2024, 12, 31)
    )
    assert not df_filtered_date.empty, "Filtered date range should have records"
    assert (df_filtered_date["Order Date"].dt.date >= date(2024, 6, 1)).all(), "Date start bound broken"
    assert (df_filtered_date["Order Date"].dt.date <= date(2024, 12, 31)).all(), "Date end bound broken"
    print(f"  [PASS] Date filter test passed ({len(df_filtered_date)} records matched).")

    # 2b. Region & Category Multi-select Filter
    regions_test = ["North America", "Europe"]
    categories_test = ["Electronics"]
    df_filtered_rc = apply_filters(
        df,
        regions=regions_test,
        categories=categories_test
    )
    assert set(df_filtered_rc["Region"].unique()).issubset(set(regions_test)), "Region filter leak!"
    assert set(df_filtered_rc["Category"].unique()).issubset(set(categories_test)), "Category filter leak!"
    print(f"  [PASS] Region & Category filter test passed ({len(df_filtered_rc)} records matched).")

    # 2c. Product Filter
    sample_prod = df["Product Name"].iloc[0]
    df_filtered_prod = apply_filters(df, products=[sample_prod])
    assert (df_filtered_prod["Product Name"] == sample_prod).all(), "Product filter failed"
    print(f"  [PASS] Product filter test passed ({len(df_filtered_prod)} records matched).")

    # -------------------------------------------------------------------------
    # TEST 3: KPI Metrics Calculation & Growth Deltas
    # -------------------------------------------------------------------------
    print("\n[TEST 3] Testing KPI Metrics Calculation...")
    kpis = calculate_kpis(df_filtered_date, df_baseline=df)
    
    assert kpis["total_sales"] > 0, "Total sales should be > 0"
    assert kpis["total_profit"] != 0, "Total profit should not be 0"
    assert kpis["total_orders"] > 0, "Total orders should be > 0"
    assert kpis["aov"] > 0, "AOV should be > 0"
    assert isinstance(kpis["profit_margin"], float), "Profit margin should be float"
    
    # Test Empty Dataframe Safety
    empty_kpis = calculate_kpis(pd.DataFrame(), pd.DataFrame())
    assert empty_kpis["total_sales"] == 0.0, "Empty total sales should be 0.0"
    assert empty_kpis["total_orders"] == 0, "Empty total orders should be 0"
    print("  [PASS] KPI metric calculations & empty safety test passed.")

    # -------------------------------------------------------------------------
    # TEST 4: Plotly Visual Charts Rendering
    # -------------------------------------------------------------------------
    print("\n[TEST 4] Testing Plotly Charts Generation...")
    
    # Chart 1: Monthly Sales Trend
    monthly_df = df.groupby("Month").agg(
        Sales_Revenue=("Sales Revenue", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=monthly_df["Month"], y=monthly_df["Sales_Revenue"]))
    fig1.add_trace(go.Scatter(x=monthly_df["Month"], y=monthly_df["Profit"]))
    apply_plotly_theme(fig1)
    print("  [PASS] Monthly Trend Chart generated successfully.")

    # Chart 2: Category Donut Chart
    cat_df = df.groupby("Category")["Sales Revenue"].sum().reset_index()
    fig2 = px.pie(cat_df, values="Sales Revenue", names="Category", hole=0.55)
    apply_plotly_theme(fig2)
    print("  [PASS] Category Donut Chart generated successfully.")

    # Chart 3: Sales vs Profit Scatter Analysis
    fig3 = px.scatter(df, x="Sales Revenue", y="Profit", color="Category", size="Quantity")
    apply_plotly_theme(fig3)
    print("  [PASS] Sales vs Profit Scatter plot generated successfully.")

    # Chart 4: Profit Margin Heatmap
    heatmap_df = df.pivot_table(index="Category", columns="Region", values="Profit Margin %", aggfunc="mean").round(1)
    fig4 = px.imshow(heatmap_df, text_auto=True)
    apply_plotly_theme(fig4)
    print("  [PASS] Profit Margin Heatmap generated successfully.")

    # Chart 5: Regional Bar Chart
    region_summary = df.groupby("Region").agg(
        Sales_Revenue=("Sales Revenue", "sum")
    ).reset_index().sort_values(by="Sales_Revenue", ascending=True)
    fig5 = px.bar(region_summary, y="Region", x="Sales_Revenue", orientation="h")
    apply_plotly_theme(fig5)
    print("  [PASS] Regional Bar Chart generated successfully.")

    # Chart 6: Top 10 Products Chart
    top_products = df.groupby(["Product Name", "Category"]).agg(
        Sales_Revenue=("Sales Revenue", "sum")
    ).reset_index().sort_values(by="Sales_Revenue", ascending=False).head(10)
    fig6 = px.bar(top_products, x="Sales_Revenue", y="Product Name", orientation="h")
    apply_plotly_theme(fig6)
    print("  [PASS] Top 10 Products Chart generated successfully.")

    # -------------------------------------------------------------------------
    # TEST 5: Data Export Utilities (CSV & Excel)
    # -------------------------------------------------------------------------
    print("\n[TEST 5] Testing Data Export (CSV & Excel)...")
    
    # CSV Export test
    csv_bytes = df.head(100).to_csv(index=False).encode("utf-8")
    assert len(csv_bytes) > 0, "CSV bytes should not be empty"
    print("  [PASS] CSV export test passed.")

    # Excel Export test using openpyxl
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.head(100).to_excel(writer, index=False, sheet_name="Sales_Data")
    excel_bytes = buffer.getvalue()
    assert len(excel_bytes) > 0, "Excel bytes should not be empty"
    print("  [PASS] Excel export test passed.")

    print("\n==================================================")
    print("[SUCCESS] ALL 5 DASHBOARD TEST SUITES PASSED PERFECTLY!")
    print("==================================================")

if __name__ == "__main__":
    run_all_tests()
