import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Enterprise Sales Analytics",
    page_icon="",
    layout="wide"
)

# --------------------------------------------------
# DARK PROFESSIONAL THEME
# --------------------------------------------------
st.markdown("""
<style>
body { background-color: #0E1117; }

.card {
    background-color: #111827;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #1F2937;
}

.card-title {
    color: #9CA3AF;
    font-size: 14px;
    margin-bottom: 8px;
}

.card-value {
    color: white;
    font-size: 28px;
    font-weight: 700;
}

.section-title {
    color: #E5E7EB;
    font-size: 18px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("sales_data.csv")

df = load_data()

# --------------------------------------------------
# AUTO COLUMN DETECTION
# --------------------------------------------------
date_col = next(c for c in df.columns if "date" in c.lower())
sales_col = next(c for c in df.columns if "sales" in c.lower() or "revenue" in c.lower())
region_col = next(c for c in df.columns if "region" in c.lower() or "market" in c.lower() or "country" in c.lower())
product_col = next(c for c in df.columns if "category" in c.lower() or "product" in c.lower())

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df.dropna(subset=[date_col])
df["Month"] = df[date_col].dt.strftime("%b")

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.title("Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [df[date_col].min(), df[date_col].max()]
)

regions = st.sidebar.multiselect(
    "Region",
    sorted(df[region_col].unique()),
    default=list(df[region_col].unique())
)

products = st.sidebar.multiselect(
    "Product",
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
# HEADER
# --------------------------------------------------
st.title("Enterprise Sales Analytics Dashboard")

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
k1, k2, k3 = st.columns(3)

with k1:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Total Revenue</div>
        <div class="card-value">₹{filtered_df[sales_col].sum():,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Average Order Value</div>
        <div class="card-value">₹{filtered_df[sales_col].mean():,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Total Orders</div>
        <div class="card-value">{len(filtered_df):,}</div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# CHART GRID (LIKE YOUR IMAGE)
# --------------------------------------------------
c1, c2 = st.columns(2)

# -------- LINE CHART --------
with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Sales by Region</div>', unsafe_allow_html=True)

    region_trend = (
        filtered_df
        .groupby(["Month", region_col])[sales_col]
        .sum()
        .unstack()
        .fillna(0)
    )

    fig, ax = plt.subplots()
    for col in region_trend.columns:
        ax.plot(region_trend.index, region_trend[col], marker="o", label=col)

    ax.legend()
    ax.grid(alpha=0.3)
    st.pyplot(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------- DONUT CHART --------
with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Sales Distribution</div>', unsafe_allow_html=True)

    product_share = filtered_df.groupby(product_col)[sales_col].sum()

    fig, ax = plt.subplots()
    ax.pie(
        product_share,
        labels=product_share.index,
        autopct="%1.0f%%",
        startangle=90,
        wedgeprops=dict(width=0.4)
    )
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# SECOND ROW
# --------------------------------------------------
c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Revenue by Product</div>', unsafe_allow_html=True)

    product_rev = filtered_df.groupby(product_col)[sales_col].sum().sort_values()

    fig, ax = plt.subplots()
    ax.barh(product_rev.index, product_rev.values)
    st.pyplot(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Monthly Orders</div>', unsafe_allow_html=True)

    monthly_orders = filtered_df.groupby("Month").size()

    fig, ax = plt.subplots()
    ax.bar(monthly_orders.index, monthly_orders.values)
    st.pyplot(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

