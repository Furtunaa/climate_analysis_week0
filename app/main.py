"""
main.py
--------
Streamlit dashboard for African Climate Trend Analysis.
10 Academy Week 0 Challenge — April 2026

Run with:
    streamlit run app/main.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Allow imports from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.utils import (
    load_all_countries, filter_data, compute_monthly_avg,
    compute_annual_extreme_heat, compute_vulnerability_scores,
    COLORS, VARIABLE_LABELS, COUNTRIES
)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="African Climate Dashboard | COP32",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8f9fa;
        border-left: 4px solid #E45756;
        padding: 1rem;
        border-radius: 6px;
    }
    .insight-box {
        background: #eef6ff;
        border-left: 4px solid #4C9BE8;
        padding: 1rem;
        border-radius: 6px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_all_countries()

df_all = get_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Flag_of_Ethiopia.svg/120px-Flag_of_Ethiopia.svg.png", width=80)
    st.markdown("### 🌍 Climate Explorer")
    st.markdown("**10 Academy Week 0 | COP32 Prep**")
    st.divider()

    # Country multi-select
    selected_countries = st.multiselect(
        "🗺️ Select Countries",
        options=COUNTRIES,
        default=COUNTRIES,
        help="Choose one or more countries to display"
    )

    # Year range slider
    st.markdown("**📅 Year Range**")
    if not df_all.empty:
        min_year = int(df_all['Year'].min())
        max_year = int(df_all['Year'].max())
    else:
        min_year, max_year = 2015, 2026

    year_range = st.slider(
        "Select period",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )

    # Variable selector
    selected_var = st.selectbox(
        "📊 Climate Variable",
        options=list(VARIABLE_LABELS.keys()),
        format_func=lambda x: VARIABLE_LABELS[x],
        index=0
    )

    # Heat threshold
    heat_threshold = st.slider(
        "🌡️ Extreme Heat Threshold (°C)",
        min_value=30,
        max_value=45,
        value=35,
        step=1
    )

    st.divider()
    st.markdown("**Data Source:** NASA POWER")
    st.markdown("**Period:** 2015–2026")
    st.markdown("**Countries:** Ethiopia, Kenya, Sudan, Tanzania, Nigeria")

# ── Filter data ────────────────────────────────────────────────────────────────
if df_all.empty:
    st.error("⚠️ No data files found. Please run the EDA notebooks first to generate cleaned CSV files in the `data/` directory.")
    st.info("Expected files: `data/ethiopia_clean.csv`, `data/kenya_clean.csv`, etc.")
    st.stop()

if not selected_countries:
    st.warning("Please select at least one country.")
    st.stop()

df = filter_data(df_all, selected_countries, year_range)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">🌍 African Climate Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="sub-header">Historical climate analysis across {len(selected_countries)} African nations '
    f'({year_range[0]}–{year_range[1]}) — supporting Ethiopia\'s COP32 preparation</div>',
    unsafe_allow_html=True
)

# ── KPI Metrics ────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Countries Selected", len(selected_countries))
with col2:
    st.metric("Total Observations", f"{len(df):,}")
with col3:
    if 'T2M' in df.columns:
        st.metric("Mean Temperature", f"{df['T2M'].mean():.1f}°C")
with col4:
    if 'T2M_MAX' in df.columns:
        extreme_days = (df['T2M_MAX'] > heat_threshold).sum()
        st.metric(f"Extreme Heat Days (>{heat_threshold}°C)", f"{extreme_days:,}")

st.divider()

# ── Tab layout ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🌡️ Temperature Trends",
    "🌧️ Precipitation",
    "⚡ Extreme Events",
    "🏆 Vulnerability Ranking"
])

# ── Tab 1: Temperature Trends ──────────────────────────────────────────────────
with tab1:
    st.subheader(f"Monthly {VARIABLE_LABELS.get(selected_var, selected_var)} Over Time")

    if selected_var in df.columns:
        monthly = compute_monthly_avg(df, selected_var)

        fig_line = px.line(
            monthly, x='Date', y=selected_var, color='Country',
            color_discrete_map=COLORS,
            labels={selected_var: VARIABLE_LABELS.get(selected_var, selected_var), 'Date': 'Date'},
            title=f"Monthly Average {VARIABLE_LABELS.get(selected_var, selected_var)} ({year_range[0]}–{year_range[1]})"
        )
        fig_line.update_layout(
            height=420,
            legend=dict(orientation='h', y=-0.15),
            hovermode='x unified'
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Summary stats
        st.subheader("Summary Statistics")
        summary = df.groupby('Country')[selected_var].agg(['mean', 'median', 'std']).round(3)
        summary.columns = ['Mean', 'Median', 'Std Dev']
        summary = summary.sort_values('Mean', ascending=False)
        st.dataframe(summary, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        📌 <strong>COP32 Insight:</strong> Sudan records the highest mean temperatures, 
        reflecting Saharan heat amplification. Ethiopia and Kenya both show a visible 
        warming trend of ~0.3°C/decade — directly threatening rainfed agriculture that 
        supports 80%+ of the population.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(f"Variable {selected_var} not available in the dataset.")

# ── Tab 2: Precipitation ───────────────────────────────────────────────────────
with tab2:
    st.subheader("Precipitation Distribution — Country Comparison")

    if 'PRECTOTCORR' in df.columns:
        col_a, col_b = st.columns(2)

        with col_a:
            # Boxplot
            fig_box = px.box(
                df, x='Country', y='PRECTOTCORR',
                color='Country', color_discrete_map=COLORS,
                title="Daily Precipitation Distribution",
                labels={'PRECTOTCORR': 'Precipitation (mm/day)'},
                points=False
            )
            fig_box.update_layout(height=420, showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)

        with col_b:
            # Monthly precipitation line
            monthly_p = compute_monthly_avg(df, 'PRECTOTCORR')
            monthly_p['PRECTOTCORR_monthly'] = monthly_p['PRECTOTCORR'] * 30

            fig_precip = px.area(
                monthly_p, x='Date', y='PRECTOTCORR', color='Country',
                color_discrete_map=COLORS,
                title="Monthly Average Daily Precipitation",
                labels={'PRECTOTCORR': 'mm/day'},
            )
            fig_precip.update_layout(height=420, legend=dict(orientation='h', y=-0.15))
            st.plotly_chart(fig_precip, use_container_width=True)

        # Precip summary
        prec_stats = df.groupby('Country')['PRECTOTCORR'].agg(['mean', 'median', 'std']).round(3)
        prec_stats.columns = ['Mean (mm/day)', 'Median (mm/day)', 'Std Dev']
        prec_stats = prec_stats.sort_values('Std Dev', ascending=False)
        st.subheader("Precipitation Variability (sorted by Std Dev)")
        st.dataframe(prec_stats, use_container_width=True)

# ── Tab 3: Extreme Events ──────────────────────────────────────────────────────
with tab3:
    st.subheader(f"Extreme Heat Days per Year (T2M_MAX > {heat_threshold}°C)")

    if 'T2M_MAX' in df.columns:
        heat_df = df[df['T2M_MAX'] > heat_threshold].groupby(['Country', 'Year']).size().reset_index(name='Days')

        fig_heat = px.bar(
            heat_df, x='Year', y='Days', color='Country',
            color_discrete_map=COLORS, barmode='group',
            title=f"Extreme Heat Days per Year (T2M_MAX > {heat_threshold}°C)",
            labels={'Days': 'Number of Days'}
        )
        fig_heat.update_layout(height=420)
        st.plotly_chart(fig_heat, use_container_width=True)

    st.subheader("Max Consecutive Dry Days per Year")

    if 'PRECTOTCORR' in df.columns:
        def max_dry(s):
            max_run, cur = 0, 0
            for v in s:
                if pd.isna(v) or v < 1.0:
                    cur += 1
                    max_run = max(max_run, cur)
                else:
                    cur = 0
            return max_run

        dry_df = df.groupby(['Country', 'Year'])['PRECTOTCORR'].apply(max_dry).reset_index()
        dry_df.columns = ['Country', 'Year', 'Max Dry Days']

        fig_dry = px.bar(
            dry_df, x='Year', y='Max Dry Days', color='Country',
            color_discrete_map=COLORS, barmode='group',
            title="Maximum Consecutive Dry Days per Year",
        )
        fig_dry.update_layout(height=420)
        st.plotly_chart(fig_dry, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        📌 <strong>COP32 Insight:</strong> The 2020–2023 Horn of Africa drought is visible 
        as elevated consecutive dry day counts in Ethiopia and Kenya — the worst multi-year 
        drought in 40 years, displacing 2.3M people and costing $9.5B USD in livestock losses 
        (FAO, 2023). This demands funded early warning systems and pastoral adaptation finance.
        </div>
        """, unsafe_allow_html=True)

# ── Tab 4: Vulnerability Ranking ───────────────────────────────────────────────
with tab4:
    st.subheader("🏆 Climate Vulnerability Ranking")

    vuln = compute_vulnerability_scores(df)

    col_l, col_r = st.columns([2, 1])

    with col_l:
        fig_rank = px.bar(
            vuln.reset_index(), x='Composite Score', y='index',
            orientation='h',
            color='index', color_discrete_map=COLORS,
            title="Composite Climate Vulnerability Score\n(Normalized: Temperature + Precipitation + Extremes)",
            labels={'index': 'Country', 'Composite Score': 'Score'}
        )
        fig_rank.update_layout(height=380, showlegend=False, yaxis={'autorange': 'reversed'})
        st.plotly_chart(fig_rank, use_container_width=True)

    with col_r:
        st.dataframe(
            vuln[['Rank', 'Composite Score']],
            use_container_width=True
        )

    st.subheader("📋 COP32 Position Paper Observations")
    st.markdown("""
    1. **Fastest warming:** Sudan — Saharan amplification means it warms 1.5–2× faster than the global average, threatening water security for 46M people.
    2. **Most unstable precipitation:** Nigeria — high variance between Sahel droughts and Niger Delta flooding demands integrated basin-level water management.
    3. **Extreme heat & drought:** Sudan leads extreme heat days; Ethiopia & Kenya dominate consecutive dry days — both require climate adaptation investment now.
    4. **Ethiopia's profile:** Bimodal rainfall system makes it uniquely vulnerable — one failed rainy season equals a food crisis. +0.3°C/decade trend demands investment in drought-resilient agriculture.
    5. **Champion for finance:** Sudan should be Ethiopia's priority coalition partner at COP32 — it presents the strongest data case for urgent, large-scale adaptation finance.
    """)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "**Data:** NASA POWER | **Analysis:** 10 Academy Week 0 Challenge | "
    "**Purpose:** Supporting Ethiopia's COP32 preparation, Addis Ababa 2027"
)
