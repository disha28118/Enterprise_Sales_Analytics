import streamlit as st
import pandas as pd
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Enterprise Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# POWER BI STYLE
# --------------------------------------------------
st.markdown("""
<style>
body { background-color: #0E1117; }
.kpi {
    background: linear-gradient(135deg, #1f2937, #020617);
    padding: 22px;
    border-radius: 14px;
    text-align: center;
}
.kpi-title {
    color: #9CA3AF;
    font-size: 13px;
}
.kpi-value {
    color: white;
    font-size: 30px;
    font-weight: 700;
}
.section {
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    return df

df = load_data()

# --------------------------------------------------
# AUTO COLUMN DETECTION (SAFE)
# --------------------------------------------------
date_col = next(c for c in df.columns if "date" in c.lower())
sales_col = next(c for c in df.columns if "sales" in c.lower() or "revenue" in c.lower())
region_col = next(c for c in df.columns if "region" in c.lower() or "market" in c.lower() or "country" in c.lower())
product_col = next(c for c in df.columns if "category" in c.lower() or "product" in c.lower())

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df.dropna(subset=[date_col])

df["YearMonth"] = df[date_col].dt.to_period("M").astype(str)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.title(" Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [df[date_col].min(), df[date_col].max()]
)

regions = st.sidebar.multiselect(
    "Select Region",
    sorted(df[region_col].unique()),
    default=list(df[region_col].unique())
)

products = st.sidebar.multiselect(
    "Select Product",
    sorted(df[product_col].unique()),
    default=list(df[product_col].unique())
)

filtered_df = df[
    (df[date_col] >= pd.to_datetime(date_range[0])) &
    (df[date_col] <= pd.to_datetime(date_range[1])) &
    (df[region_col].isin(regions)) &
    (df[product_col].isin(products))
]

# --------------------------------------------------
# KPIs
# --------------------------------------------------
total_revenue = filtered_df[sales_col].sum()
avg_order = filtered_df[sales_col].mean()
total_orders = len(filtered_df)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("Enterprise Sales Analytics Dashboard")

k1, k2, k3 = st.columns(3)

with k1:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">Total Revenue</div>
        <div class="kpi-value">₹{total_revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">Average Order Value</div>
        <div class="kpi-value">₹{avg_order:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">Total Orders</div>
        <div class="kpi-value">{total_orders:,}</div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# REVENUE TREND (FIXED)
# --------------------------------------------------
st.markdown("##  Revenue Trend Over Time")

trend_df = (
    filtered_df
    .groupby("YearMonth")[sales_col]
    .sum()
    .reset_index()
)

st.line_chart(trend_df.set_index("YearMonth"))

# --------------------------------------------------
# BREAKDOWNS
# --------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.markdown("##  Revenue by Region")
    st.bar_chart(
        filtered_df.groupby(region_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

with c2:
    st.markdown("##  Revenue by Product")
    st.bar_chart(
        filtered_df.groupby(product_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

# --------------------------------------------------
# EXECUTIVE INSIGHTS
# --------------------------------------------------
top_region = filtered_df.groupby(region_col)[sales_col].sum().idxmax()
top_product = filtered_df.groupby(product_col)[sales_col].sum().idxmax()

st.success(
    f"""
    🔹 **Top Region:** {top_region}  
    🔹 **Top Product:** {top_product}  
    🔹 **Records Analyzed:** {len(filtered_df):,}
    """
)

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------
with st.expander("View Filtered Data"):
    st.dataframe(filtered_df.head(100), use_container_width=True)


