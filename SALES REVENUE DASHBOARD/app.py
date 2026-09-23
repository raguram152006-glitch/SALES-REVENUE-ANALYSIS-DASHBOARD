"""
Sales & Revenue Analysis Dashboard
Streamlit Application
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

# Import custom modules
from data_generator import get_or_create_dataset
from utils import load_sales_data, apply_filters, calculate_kpis, format_currency, format_number
from styles import get_custom_css, apply_plotly_theme, PALETTE, PRIMARY_COLOR, SUCCESS_COLOR, WARNING_COLOR, DANGER_COLOR, INFO_COLOR, PURPLE_COLOR

# ------------------------------------------------------------------------------
# 1. Page Configuration & Theme
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Sales & Revenue Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. Data Loading & Initialization
# ------------------------------------------------------------------------------
if "force_recreate" not in st.session_state:
    st.session_state.force_recreate = False

df_raw = load_sales_data(force_recreate=st.session_state.force_recreate)

if st.session_state.force_recreate:
    st.session_state.force_recreate = False

# Min/Max dates for filter controls
min_date = df_raw["Order Date"].min().date()
max_date = df_raw["Order Date"].max().date()

# ------------------------------------------------------------------------------
# 3. Sidebar Controls & Interactive Filters
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 0.5rem 0 1.5rem 0;'>
            <h2 style='color: #6366F1; margin: 0; font-weight: 800; font-size: 1.5rem;'>⚡ Sales Intelligence</h2>
            <p style='color: #64748B; font-size: 0.8rem; margin-top: 0.2rem;'>Executive Dashboard v2.5</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎛️ Filter Panel")

    # Date Range Presets
    date_preset = st.selectbox(
        "Date Quick Presets",
        ["All Time", "Year 2025", "Year 2024", "Last 12 Months", "Custom Range"]
    )

    if date_preset == "All Time":
        start_date_val, end_date_val = min_date, max_date
    elif date_preset == "Year 2025":
        start_date_val = date(2025, 1, 1)
        end_date_val = date(2025, 12, 31)
    elif date_preset == "Year 2024":
        start_date_val = date(2024, 1, 1)
        end_date_val = date(2024, 12, 31)
    elif date_preset == "Last 12 Months":
        end_date_val = max_date
        start_date_val = max_date - pd.Timedelta(days=365)
    else:
        date_range = st.date_input(
            "Select Custom Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date_val, end_date_val = date_range[0], date_range[1]
        else:
            start_date_val, end_date_val = min_date, max_date

    st.divider()

    # Region Filter
    all_regions = sorted(df_raw["Region"].unique().tolist())
    selected_regions = st.multiselect(
        "Region",
        options=all_regions,
        default=all_regions,
        help="Filter sales by geographic region"
    )

    # Category Filter
    all_categories = sorted(df_raw["Category"].unique().tolist())
    selected_categories = st.multiselect(
        "Category",
        options=all_categories,
        default=all_categories,
        help="Filter by product category"
    )

    # Dynamic Sub-Category / Product Filter
    available_products = sorted(
        df_raw[
            df_raw["Region"].isin(selected_regions if selected_regions else all_regions) &
            df_raw["Category"].isin(selected_categories if selected_categories else all_categories)
        ]["Product Name"].unique().tolist()
    )

    selected_products = st.multiselect(
        "Product Name (Optional)",
        options=available_products,
        default=[],
        help="Leave empty to select all products"
    )

    # Customer Segment Filter
    all_segments = sorted(df_raw["Customer Type"].unique().tolist())
    selected_segments = st.multiselect(
        "Customer Segment",
        options=all_segments,
        default=all_segments
    )

    st.divider()

    # Data Actions
    st.markdown("### ⚙️ Data Actions")
    col_act1, col_act2 = st.columns(2)
    with col_act1:
        if st.button("🔄 Reset Filters", use_container_width=True):
            st.rerun()
    with col_act2:
        if st.button("🎲 Re-Gen Dataset", use_container_width=True):
            st.session_state.force_recreate = True
            st.rerun()

    st.markdown("""
        <div style='margin-top: 2rem; font-size: 0.75rem; color: #475569; text-align: center;'>
            Built with Streamlit & Plotly • Antigravity AI
        </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 4. Data Processing & Filter Execution
# ------------------------------------------------------------------------------
df_filtered = apply_filters(
    df_raw,
    start_date=start_date_val,
    end_date=end_date_val,
    regions=selected_regions,
    categories=selected_categories,
    products=selected_products,
    customer_types=selected_segments
)

# Calculate baseline (previous matching time window or full set for growth deltas)
date_days = (end_date_val - start_date_val).days + 1
prev_start = start_date_val - pd.Timedelta(days=date_days)
prev_end = start_date_val - pd.Timedelta(days=1)

df_baseline = apply_filters(
    df_raw,
    start_date=prev_start,
    end_date=prev_end,
    regions=selected_regions,
    categories=selected_categories,
    products=selected_products,
    customer_types=selected_segments
)

kpis = calculate_kpis(df_filtered, df_baseline)

# ------------------------------------------------------------------------------
# 5. Header Section
# ------------------------------------------------------------------------------
st.markdown("""
    <div class="header-container">
        <div>
            <h1 class="header-title">Sales & Revenue Analytics</h1>
            <div class="header-subtitle">Real-time financial performance, product trends & margin insights</div>
        </div>
        <div class="live-badge">
            <div class="pulse-dot"></div>
            <span>LIVE DATA ENGINE</span>
        </div>
    </div>
""", unsafe_allow_html=True)

if df_filtered.empty:
    st.warning("⚠️ No records match the selected filter criteria. Please broaden your sidebar filters.")
    st.stop()

# ------------------------------------------------------------------------------
# 6. KPI Cards Section (5 Required Metrics)
# ------------------------------------------------------------------------------
kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

def render_kpi_card(column, title, value_str, delta_val, is_percentage_points=False, suffix="vs prev period"):
    if delta_val > 0:
        badge_class = "kpi-badge-positive"
        icon = "▲"
        sign = "+"
    elif delta_val < 0:
        badge_class = "kpi-badge-negative"
        icon = "▼"
        sign = ""
    else:
        badge_class = "kpi-badge-neutral"
        icon = "•"
        sign = ""
    
    delta_formatted = f"{sign}{delta_val:.1f}%" if not is_percentage_points else f"{sign}{delta_val:.1f} pts"

    html_content = f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value_str}</div>
        <div>
            <span class="{badge_class}">{icon} {delta_formatted}</span>
            <span style="font-size: 0.7rem; color: #64748B; margin-left: 0.3rem;">{suffix}</span>
        </div>
    </div>
    """
    column.markdown(html_content, unsafe_allow_html=True)

render_kpi_card(kpi_col1, "Total Sales", format_currency(kpis["total_sales"]), kpis["sales_delta"])
render_kpi_card(kpi_col2, "Total Profit", format_currency(kpis["total_profit"]), kpis["profit_delta"])
render_kpi_card(kpi_col3, "Total Orders", format_number(kpis["total_orders"]), kpis["orders_delta"])
render_kpi_card(kpi_col4, "Avg Order Value", format_currency(kpis["aov"]), kpis["aov_delta"])
render_kpi_card(kpi_col5, "Profit Margin", f"{kpis['profit_margin']:.1f}%", kpis["margin_delta"], is_percentage_points=True)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 7. Main Dashboard Tabs
# ------------------------------------------------------------------------------
tab_overview, tab_profit, tab_region, tab_products, tab_raw_data = st.tabs([
    "📈 Revenue Trends",
    "💰 Profitability & Margins",
    "🌍 Regional Performance",
    "🏆 Top Products",
    "📄 Data Explorer"
])

# ------------------------------------------------------------------------------
# TAB 1: Revenue & Monthly Sales Trends
# ------------------------------------------------------------------------------
with tab_overview:
    col_t1, col_t2 = st.columns([7, 5])

    with col_t1:
        st.markdown("### 📅 Monthly Sales & Revenue Trend")
        
        # Aggregate Monthly
        monthly_df = df_filtered.groupby("Month").agg(
            Sales_Revenue=("Sales Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique")
        ).reset_index()

        fig_trend = go.Figure()
        
        # Bar for Sales Revenue
        fig_trend.add_trace(go.Bar(
            x=monthly_df["Month"],
            y=monthly_df["Sales_Revenue"],
            name="Sales Revenue",
            marker_color=PRIMARY_COLOR,
            opacity=0.85
        ))
        
        # Line for Net Profit
        fig_trend.add_trace(go.Scatter(
            x=monthly_df["Month"],
            y=monthly_df["Profit"],
            name="Net Profit",
            mode="lines+markers",
            line=dict(color=SUCCESS_COLOR, width=3),
            marker=dict(size=7, color=SUCCESS_COLOR)
        ))

        fig_trend.update_layout(
            title="Monthly Sales Revenue vs. Net Profit ($)",
            barmode="group",
            height=380,
            hovermode="x unified"
        )
        st.plotly_chart(apply_plotly_theme(fig_trend), use_container_width=True)

    with col_t2:
        st.markdown("### 📦 Sales by Category")
        
        cat_df = df_filtered.groupby("Category")["Sales Revenue"].sum().reset_index()
        
        fig_donut = px.pie(
            cat_df,
            values="Sales Revenue",
            names="Category",
            hole=0.55,
            color_discrete_sequence=PALETTE,
            title="Revenue Share by Product Category"
        )
        fig_donut.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#0F172A", width=2))
        )
        fig_donut.update_layout(height=380, showlegend=False)
        st.plotly_chart(apply_plotly_theme(fig_donut), use_container_width=True)

    st.markdown("---")

    # Quarterly Performance Breakdown
    col_q1, col_q2 = st.columns(2)
    
    with col_q1:
        st.markdown("### 📊 Quarterly Revenue & Profit Matrix")
        q_df = df_filtered.groupby("Quarter").agg(
            Sales_Revenue=("Sales Revenue", "sum"),
            Profit=("Profit", "sum"),
            Margin=("Profit Margin %", "mean")
        ).reset_index()

        fig_q = px.bar(
            q_df,
            x="Quarter",
            y=["Sales_Revenue", "Profit"],
            barmode="group",
            labels={"value": "Amount ($)", "variable": "Metric"},
            color_discrete_map={"Sales_Revenue": PRIMARY_COLOR, "Profit": SUCCESS_COLOR},
            title="Quarterly Sales vs Profit Comparison"
        )
        fig_q.update_layout(height=340)
        st.plotly_chart(apply_plotly_theme(fig_q), use_container_width=True)

    with col_q2:
        st.markdown("### 🏬 Sales by Customer Segment")
        segment_df = df_filtered.groupby("Customer Type").agg(
            Sales_Revenue=("Sales Revenue", "sum"),
            Orders=("Order ID", "nunique"),
            AOV=("Sales Revenue", lambda x: x.sum() / len(x))
        ).reset_index()

        fig_segment = px.bar(
            segment_df,
            x="Customer Type",
            y="Sales_Revenue",
            color="Customer Type",
            color_discrete_sequence=[PRIMARY_COLOR, INFO_COLOR, PURPLE_COLOR],
            text_auto=".2s",
            title="Revenue Distribution by Customer Type"
        )
        fig_segment.update_layout(height=340, showlegend=False)
        st.plotly_chart(apply_plotly_theme(fig_segment), use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 2: Profitability & Margins Analysis
# ------------------------------------------------------------------------------
with tab_profit:
    st.markdown("### 💡 Financial Profitability Insights")

    col_p1, col_p2 = st.columns([6, 6])

    with col_p1:
        st.markdown("#### 🎯 Sales vs. Profit Relationship (Scatter Analysis)")
        fig_scatter = px.scatter(
            df_filtered,
            x="Sales Revenue",
            y="Profit",
            color="Category",
            size="Quantity",
            hover_data=["Product Name", "Discount %", "Region"],
            color_discrete_sequence=PALETTE,
            title="Order Sales vs Net Profit (Bubble Size = Quantity)"
        )
        # Add reference line for 0 profit
        fig_scatter.add_hline(y=0, line_dash="dash", line_color=DANGER_COLOR, opacity=0.7)
        fig_scatter.update_layout(height=380)
        st.plotly_chart(apply_plotly_theme(fig_scatter), use_container_width=True)

    with col_p2:
        st.markdown("#### 📉 Discount Impact on Profit Margin (%)")
        disc_df = df_filtered.groupby("Discount %").agg(
            Avg_Margin=("Profit Margin %", "mean"),
            Total_Sales=("Sales Revenue", "sum"),
            Total_Profit=("Profit", "sum")
        ).reset_index()

        fig_disc = px.line(
            disc_df,
            x="Discount %",
            y="Avg_Margin",
            markers=True,
            line_shape="spline",
            title="Average Profit Margin (%) vs. Applied Discount Rate (%)",
            labels={"Avg_Margin": "Avg Profit Margin (%)"}
        )
        fig_disc.update_traces(line_color=WARNING_COLOR, line_width=3, marker=dict(size=8))
        fig_disc.update_layout(height=380)
        st.plotly_chart(apply_plotly_theme(fig_disc), use_container_width=True)

    st.markdown("---")

    # Heatmap: Profit Margin by Category & Region
    st.markdown("#### 🌡️ Profit Margin Heatmap (Category vs Region)")
    heatmap_df = df_filtered.pivot_table(
        index="Category",
        columns="Region",
        values="Profit Margin %",
        aggfunc="mean"
    ).round(1)

    fig_heat = px.imshow(
        heatmap_df,
        labels=dict(x="Region", y="Category", color="Profit Margin %"),
        x=heatmap_df.columns,
        y=heatmap_df.index,
        color_continuous_scale="Viridis",
        aspect="auto",
        text_auto=True,
        title="Average Profit Margin (%) Matrix"
    )
    fig_heat.update_layout(height=320)
    st.plotly_chart(apply_plotly_theme(fig_heat), use_container_width=True)

    # Low Profit Margin Alerts Table
    st.markdown("#### ⚠️ Low Margin Orders (< 10% Profit Margin)")
    low_margin_df = df_filtered[df_filtered["Profit Margin %"] < 10][
        ["Order ID", "Order Date", "Customer Type", "Region", "Category", "Product Name", "Sales Revenue", "Discount %", "Profit", "Profit Margin %"]
    ].sort_values(by="Profit Margin %", ascending=True)

    if not low_margin_df.empty:
        st.dataframe(
            low_margin_df.head(15).style.format({
                "Sales Revenue": "${:,.2f}",
                "Profit": "${:,.2f}",
                "Discount %": "{:.1f}%",
                "Profit Margin %": "{:.1f}%"
            }).background_gradient(subset=["Profit Margin %"], cmap="Reds_r"),
            use_container_width=True,
            height=280
        )
    else:
        st.success("✨ All orders maintain high healthy profit margins above 10%!")

# ------------------------------------------------------------------------------
# TAB 3: Regional Performance
# ------------------------------------------------------------------------------
with tab_region:
    st.markdown("### 🌍 Geographic & Regional Sales Analysis")

    col_r1, col_r2 = st.columns([6, 6])

    with col_r1:
        st.markdown("#### 🗺️ Total Sales Revenue by Region")
        region_summary = df_filtered.groupby("Region").agg(
            Sales_Revenue=("Sales Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique"),
            Avg_Order_Value=("Sales Revenue", lambda x: x.sum() / len(x))
        ).reset_index().sort_values(by="Sales_Revenue", ascending=True)

        fig_region_bar = px.bar(
            region_summary,
            y="Region",
            x="Sales_Revenue",
            orientation="h",
            color="Sales_Revenue",
            color_continuous_scale="Blues",
            text_auto=".3s",
            title="Regional Sales Revenue Comparison"
        )
        fig_region_bar.update_layout(height=380, showlegend=False)
        st.plotly_chart(apply_plotly_theme(fig_region_bar), use_container_width=True)

    with col_r2:
        st.markdown("#### 🏙️ Top 10 Cities by Revenue")
        city_summary = df_filtered.groupby(["City", "Country", "Region"])["Sales Revenue"].sum().reset_index()
        top_cities = city_summary.sort_values(by="Sales Revenue", ascending=False).head(10)

        fig_city = px.bar(
            top_cities,
            x="Sales Revenue",
            y="City",
            color="Region",
            orientation="h",
            color_discrete_sequence=PALETTE,
            title="Top Performing Cities Globally",
            text_auto=".2s"
        )
        fig_city.update_layout(height=380, yaxis=dict(autorange="reversed"))
        st.plotly_chart(apply_plotly_theme(fig_city), use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📋 Regional Performance Summary Table")
    region_summary["Sales Revenue"] = region_summary["Sales_Revenue"].apply(format_currency)
    region_summary["Total Profit"] = region_summary["Profit"].apply(format_currency)
    region_summary["Avg Order Value"] = region_summary["Avg_Order_Value"].apply(format_currency)
    region_table = region_summary[["Region", "Orders", "Sales Revenue", "Total Profit", "Avg Order Value"]]
    st.dataframe(region_table, use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# TAB 4: Top Products Performance
# ------------------------------------------------------------------------------
with tab_products:
    st.markdown("### 🏆 Top 10 Products Analysis")

    col_p_top1, col_p_top2 = st.columns([7, 5])

    with col_p_top1:
        st.markdown("#### 🥇 Top 10 Best-Selling Products by Revenue")
        top_products = df_filtered.groupby(["Product Name", "Category"]).agg(
            Sales_Revenue=("Sales Revenue", "sum"),
            Units_Sold=("Quantity", "sum"),
            Total_Profit=("Profit", "sum"),
            Avg_Margin=("Profit Margin %", "mean")
        ).reset_index().sort_values(by="Sales_Revenue", ascending=False).head(10)

        fig_top_prod = px.bar(
            top_products,
            x="Sales_Revenue",
            y="Product Name",
            orientation="h",
            color="Category",
            color_discrete_sequence=PALETTE,
            text_auto=".3s",
            title="Top 10 Products Revenue Breakdown"
        )
        fig_top_prod.update_layout(height=420, yaxis=dict(autorange="reversed"))
        st.plotly_chart(apply_plotly_theme(fig_top_prod), use_container_width=True)

    with col_p_top2:
        st.markdown("#### 📦 Units Sold vs Profit Margin")
        fig_prod_scatter = px.scatter(
            top_products,
            x="Units_Sold",
            y="Avg_Margin",
            color="Category",
            size="Sales_Revenue",
            text="Product Name",
            color_discrete_sequence=PALETTE,
            title="Units Sold vs Profit Margin (%)"
        )
        fig_prod_scatter.update_traces(textposition="top center")
        fig_prod_scatter.update_layout(height=420)
        st.plotly_chart(apply_plotly_theme(fig_prod_scatter), use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📊 Top 10 Product Leaderboard Detail")
    top_prod_table = top_products.copy()
    top_prod_table["Sales Revenue"] = top_prod_table["Sales_Revenue"].apply(format_currency)
    top_prod_table["Total Profit"] = top_prod_table["Total_Profit"].apply(format_currency)
    top_prod_table["Avg Margin %"] = top_prod_table["Avg_Margin"].apply(lambda x: f"{x:.1f}%")
    top_prod_table = top_prod_table[["Product Name", "Category", "Units_Sold", "Sales Revenue", "Total Profit", "Avg Margin %"]]
    st.dataframe(top_prod_table, use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# TAB 5: Raw Data Explorer & Custom Exporter
# ------------------------------------------------------------------------------
with tab_raw_data:
    st.markdown("### 📄 Sales Data Explorer & Export Engine")
    st.write(f"Displaying **{len(df_filtered):,}** matching transaction records.")

    # Column selection
    all_cols = df_filtered.columns.tolist()
    selected_cols = st.multiselect(
        "Choose Columns to Display",
        options=all_cols,
        default=["Order ID", "Order Date", "Customer Type", "Region", "Category", "Product Name", "Quantity", "Sales Revenue", "Profit", "Profit Margin %", "Order Status"]
    )

    st.dataframe(
        df_filtered[selected_cols] if selected_cols else df_filtered,
        use_container_width=True,
        height=420
    )

    st.markdown("### 📥 Download Filtered Data Report")
    col_dl1, col_dl2 = st.columns(2)

    with col_dl1:
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Download Report as CSV",
            data=csv_data,
            file_name=f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_dl2:
        import io
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_filtered.to_excel(writer, index=False, sheet_name='Sales_Data')
        excel_data = buffer.getvalue()
        
        st.download_button(
            label="📊 Download Report as Excel (.xlsx)",
            data=excel_data,
            file_name=f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
