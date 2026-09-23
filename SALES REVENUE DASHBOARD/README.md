# 📊 Sales & Revenue Analysis Dashboard

A modern, executive-grade Sales & Revenue Analytics Dashboard built using **Python**, **Streamlit**, and **Plotly**. 

Features real-time interactive KPI metric cards, multi-dimensional filtering, dark-mode glassmorphism visual styling, trend predictions, regional breakdowns, profit margin heatmaps, top product rankings, and custom report export engines (CSV & Excel).

---

## 🌟 Key Features

### 1. Executive KPI Cards
- **Total Sales Revenue**: Overall revenue with period-over-period % growth delta.
- **Total Net Profit**: Net bottom-line profit with growth delta.
- **Total Orders**: Total unique transactions completed.
- **Average Order Value (AOV)**: Average revenue generated per order.
- **Profit Margin (%)**: Overall margin with target health status.

### 2. Multi-Tab Visual Analytics
- **📈 Revenue Trends**: Monthly & quarterly revenue vs. profit dual-axis interactive charts, category share donut chart, and customer segment matrix.
- **💰 Profitability & Margins**: Sales vs. Profit scatter plot, discount impact curves, Category vs. Region profit margin heatmap, and low margin order alerts.
- **🌍 Regional Performance**: Horizontal regional revenue rank, top 10 global cities chart, and regional metrics summary.
- **🏆 Top Products**: Top 10 best-selling products leaderboard, units sold vs profit margin matrix, and category breakdown.
- **📄 Data Explorer & Exporter**: Full searchable dataset viewer with column visibility selection and instant export to CSV or Excel (.xlsx).

### 3. Interactive Sidebar Filters
- **Date Quick Presets**: All Time, Year 2025, Year 2024, Last 12 Months, or Custom Date Picker.
- **Geographic Region**: Multi-select filter across North America, Europe, Asia Pacific, Latin America, Middle East & Africa.
- **Product Categories & Sub-Categories**: Multi-select filtering.
- **Product Name Search**: Dynamic product filter.
- **Customer Segment Filter**: Corporate, Small Business, Consumer.
- **Actions**: Reset Filters & Re-generate synthetic dataset buttons.

---

## 📁 Project Structure

```text
SALES REVENUE DASHBOARD/
│
├── app.py                # Main Streamlit dashboard application
├── data_generator.py     # Synthetic sales dataset generator module
├── utils.py              # Data caching, filter logic, & KPI calculator
├── styles.py             # Glassmorphism CSS design system & Plotly visual themes
├── requirements.txt      # Required Python packages
└── data/
    └── sales_data.csv    # Generated sales dataset (created automatically)
```

---

## 🚀 How to Run the Application

### 1. Install Dependencies
Open your terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

### 2. Launch Streamlit App
Run the following command to start the local web application:

```bash
streamlit run app.py
```

The app will open automatically in your default web browser at:
`http://localhost:8501`

---

## ⚙️ Custom Dataset Generation
If no dataset exists, the dashboard automatically generates a 5,000-record realistic synthetic sales dataset upon launch. You can also re-generate new dataset samples at any time by clicking the **"🎲 Re-Gen Dataset"** button in the sidebar.
