"""
Custom CSS Styles and Plotly Visual Themes for Sales Dashboard
Provides glassmorphism layout, vibrant KPI metric card HTML/CSS, and consistent color palettes.
"""

# Color Palette Definitions
PRIMARY_COLOR = "#6366F1"    # Indigo Accent
SUCCESS_COLOR = "#10B981"    # Emerald Green
WARNING_COLOR = "#F59E0B"    # Amber Gold
DANGER_COLOR = "#EF4444"     # Rose Red
INFO_COLOR = "#3B82F6"       # Sky Blue
PURPLE_COLOR = "#8B5CF6"     # Deep Violet
BG_DARK = "#0F172A"          # Slate Dark 900
CARD_BG = "#1E293B"          # Slate Dark 800

PALETTE = [PRIMARY_COLOR, SUCCESS_COLOR, WARNING_COLOR, DANGER_COLOR, INFO_COLOR, PURPLE_COLOR, "#EC4899", "#14B8A6"]

def get_custom_css() -> str:
    """Return custom CSS to inject into Streamlit dashboard."""
    return """
    <style>
    /* Global Container Adjustments */
    .stApp {
        background-color: #0B0F17;
        color: #F8FAFC;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Remove default header padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }

    /* Modern Card Layout */
    .kpi-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px -5px rgba(99, 102, 241, 0.25);
        border-color: rgba(99, 102, 241, 0.3);
    }

    .kpi-title {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .kpi-value {
        color: #F8FAFC;
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.35rem;
    }

    .kpi-badge-positive {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.6rem;
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .kpi-badge-negative {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.6rem;
        background-color: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .kpi-badge-neutral {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.6rem;
        background-color: rgba(148, 163, 184, 0.15);
        color: #CBD5E1;
        border: 1px solid rgba(148, 163, 184, 0.3);
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    /* Subtitle & Header styling */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(90deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.6) 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1.75rem;
    }

    .header-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #CBD5E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .header-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        margin-top: 0.25rem;
    }

    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0.85rem;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.4);
        border-radius: 9999px;
        color: #818CF8;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10B981;
    }

    /* Customizing Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #090D14;
        border-right: 1px solid rgba(255, 255, 255, 0.07);
    }

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stDateInput label {
        color: #E2E8F0 !important;
        font-weight: 600;
    }

    /* Tab navigation style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: transparent;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(30, 41, 59, 0.4);
        border-radius: 10px;
        padding: 0.5rem 1.25rem;
        color: #94A3B8;
        font-weight: 600;
        border: 1px solid transparent;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(139, 92, 246, 0.25) 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(99, 102, 241, 0.5) !important;
    }

    /* Metric Cards Grid Wrapper */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
    }

    /* Table styling */
    .dataframe {
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    </style>
    """

def apply_plotly_theme(fig):
    """Apply unified dark modern glass theme to Plotly figures."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.4)",
        font=dict(family="Inter, sans-serif", color="#CBD5E1", size=12),
        margin=dict(l=30, r=30, t=50, b=30),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)",
            zerolinecolor="rgba(255, 255, 255, 0.1)",
            tickfont=dict(color="#94A3B8"),
            title=dict(font=dict(color="#CBD5E1"))
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)",
            zerolinecolor="rgba(255, 255, 255, 0.1)",
            tickfont=dict(color="#94A3B8"),
            title=dict(font=dict(color="#CBD5E1"))
        ),
        legend=dict(
            font=dict(color="#CBD5E1"),
            bgcolor="rgba(15, 23, 42, 0.6)",
            bordercolor="rgba(255, 255, 255, 0.1)",
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="#1E293B",
            font_size=13,
            font_family="Inter, sans-serif"
        )
    )
    return fig
