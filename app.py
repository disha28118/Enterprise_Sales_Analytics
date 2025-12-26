import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Enterprise Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# SAFE, SCOPED STYLING (NO GHOST BOXES)
# --------------------------------------------------
st.markdown("""
<style>
body { background-color: #0B0F19; }

.kpi-box {
    background: rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.08);
}

.kpi-title {
    color: #9CA3AF;
    font-size: 13px;
}

.kpi-value {
    color: #F9FAFB;
    font-size: 32px;
    font-weight: 700;
}

.section-title {
    color: #E5E7EB;
    font-size: 18px;
    margin-bottom: 8px;
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
region_col = next(
    c for c in df.columns
    if "region" in c.lower() or "market" in c.lower() or "country" in c.lower()
)
product_col = next(c for c in df.columns if "category" in c.lower() or "product" in c.lower())

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df.dropna(subset=[date_col])
df["YearMonth"] = df[date_col].dt.to_period("M").astype(str)

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
st.title("Enterprise Sales Analytics")
st.caption("Modern • Interactive • Executive BI Dashboard")

# --------------------------------------------------
# KPI ROW
# --------------------------------------------------
k1, k2, k3 = st.columns(3)

with k1:
    st.markdown(
        f"""
        <div class="kpi-box">
            <div class="kpi-title">Total Revenue</div>
            <div class="kpi-value">₹{filtered_df[sales_col].sum():,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-box">
            <div class="kpi-title">Avg Order Value</div>
            <div class="kpi-value">₹{filtered_df[sales_col].mean():,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-box">
            <div class="kpi-title">Total Orders</div>
            <div class="kpi-value">{len(filtered_df):,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# SALES BY REGION (LINE WITH DOTS)
# --------------------------------------------------
st.markdown('<div class="section-title">Sales by Region</div>', unsafe_allow_html=True)

line_df = (
    filtered_df
    .groupby(["YearMonth", region_col])[sales_col]
    .sum()
    .reset_index()
)

fig = px.line(
    line_df,
    x="YearMonth",
    y=sales_col,
    color=region_col,
    markers=True,
    template="plotly_dark"
)
fig.update_layout(height=350)
st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# SALES DISTRIBUTION (DONUT)
# --------------------------------------------------
st.markdown('<div class="section-title">Sales Distribution</div>', unsafe_allow_html=True)

donut_df = filtered_df.groupby(product_col)[sales_col].sum().reset_index()

fig = go.Figure(go.Pie(
    labels=donut_df[product_col],
    values=donut_df[sales_col],
    hole=0.65
))
fig.update_layout(
    annotations=[dict(text="Share", x=0.5, y=0.5, showarrow=False)],
    template="plotly_dark",
    height=350
)
st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# REVENUE BY PRODUCT (ROUNDED BARS)
# --------------------------------------------------
st.markdown('<div class="section-title">Revenue by Product</div>', unsafe_allow_html=True)

prod_df = filtered_df.groupby(product_col)[sales_col].sum().reset_index()

fig = px.bar(
    prod_df,
    x=sales_col,
    y=product_col,
    orientation="h",
    template="plotly_dark",
    text_auto=".2s"
)

fig.update_traces(
    marker=dict(
        color="#6D7CFF",
        line=dict(width=0),
        cornerradius=12
    )
)

fig.update_layout(
    height=300,
    bargap=0.35,
    xaxis_title="Sales",
    yaxis_title="Category",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# MONTHLY ORDERS (ROUNDED BARS)
# --------------------------------------------------
st.markdown('<div class="section-title">Monthly Orders</div>', unsafe_allow_html=True)

orders_df = filtered_df.groupby("YearMonth").size().reset_index(name="Orders")

fig = px.bar(
    orders_df,
    x="YearMonth",
    y="Orders",
    template="plotly_dark"
)

fig.update_traces(
    marker=dict(
        color="#6D7CFF",
        line=dict(width=0),
        cornerradius=10
    )
)

fig.update_layout(
    height=300,
    bargap=0.45,
    xaxis_title="Month",
    yaxis_title="Orders",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
