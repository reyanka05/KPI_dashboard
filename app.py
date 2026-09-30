import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Customer Churn KPI Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* =====================================================
   MAIN APPLICATION
===================================================== */

.stApp {
    background-color: #0e1117;
}


/* =====================================================
   MAIN HEADINGS
===================================================== */

h1, h2, h3 {
    color: #ffffff !important;
}


/* =====================================================
   NORMAL TEXT
===================================================== */

.stMarkdown p {
    color: #e5e7eb !important;
}


/* =====================================================
   METRIC / KPI CARDS
===================================================== */

/* White card */

[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border-radius: 14px !important;
    padding: 18px !important;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.25) !important;

    /* Important */
    color: #111827 !important;
}


/* KPI LABEL */

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] div,
[data-testid="stMetricLabel"] span {
    color: #111827 !important;
    opacity: 1 !important;
}


/* KPI VALUE */

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stMetricValue"] div,
[data-testid="stMetricValue"] span {
    color: #000000 !important;
    opacity: 1 !important;
}


/* KPI DELTA */

[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] *,
[data-testid="stMetricDelta"] div,
[data-testid="stMetricDelta"] span {
    color: #111827 !important;
    opacity: 1 !important;
}


/* =====================================================
   SIDEBAR
===================================================== */

[data-testid="stSidebar"] {
    background-color: #171a21 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #ffffff !important;
}


/* =====================================================
   EXPANDER
===================================================== */

[data-testid="stExpander"] {
    border: 1px solid #3a3f4b !important;
    border-radius: 12px !important;
}


/* =====================================================
   DATASET INFORMATION METRIC CARDS
===================================================== */

/*
   These are the Rows / Columns / Missing Values
   cards inside the expander.
*/

[data-testid="stExpander"] [data-testid="stMetric"] {
    background-color: #ffffff !important;
    color: #111827 !important;
}


[data-testid="stExpander"] [data-testid="stMetricLabel"],
[data-testid="stExpander"] [data-testid="stMetricLabel"] *,
[data-testid="stExpander"] [data-testid="stMetricLabel"] p,
[data-testid="stExpander"] [data-testid="stMetricLabel"] div,
[data-testid="stExpander"] [data-testid="stMetricLabel"] span {
    color: #111827 !important;
    opacity: 1 !important;
}


[data-testid="stExpander"] [data-testid="stMetricValue"],
[data-testid="stExpander"] [data-testid="stMetricValue"] *,
[data-testid="stExpander"] [data-testid="stMetricValue"] div,
[data-testid="stExpander"] [data-testid="stMetricValue"] span {
    color: #000000 !important;
    opacity: 1 !important;
}


/* =====================================================
   DATAFRAME
===================================================== */

[data-testid="stDataFrame"] {
    border-radius: 10px !important;
}


/* =====================================================
   DIVIDER
===================================================== */

hr {
    border-color: #343943 !important;
}


/* =====================================================
   CHART TITLES / TEXT
===================================================== */

.js-plotly-plot .plotly text {
    font-family: Arial, sans-serif !important;
}


/* =====================================================
   FOOTER
===================================================== */

.stCaption {
    color: #9ca3af !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("customer_churn_sample.csv")

    # Remove unwanted spaces from column names
    df.columns = df.columns.str.strip()

    return df


df = load_data()


# =========================================================
# TITLE
# =========================================================

st.title("📊 Customer Churn KPI Dashboard")

st.write(
    "Interactive dashboard for analyzing customer churn, "
    "retention, revenue risk, tenure and customer segments."
)

st.divider()


# =========================================================
# DATASET INFORMATION
# =========================================================

with st.expander("🔍 View Dataset Information"):

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Rows",
        df.shape[0]
    )

    col2.metric(
        "Columns",
        df.shape[1]
    )

    col3.metric(
        "Missing Values",
        int(df.isnull().sum().sum())
    )

    st.subheader("Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )


# =========================================================
# FIND COLUMN FUNCTION
# =========================================================

def find_column(possible_names):

    for name in possible_names:

        if name in df.columns:
            return name

    return None


# =========================================================
# IDENTIFY IMPORTANT COLUMNS
# =========================================================

churn_col = find_column([
    "Churn",
    "churn",
    "Exited",
    "Status"
])

contract_col = find_column([
    "ContractType",
    "Contract",
    "contract",
    "contract_type"
])

payment_col = find_column([
    "PaymentMethod",
    "Payment Method",
    "payment_method"
])

tenure_col = find_column([
    "TenureMonths",
    "Tenure",
    "tenure",
    "tenure_months"
])

monthly_charge_col = find_column([
    "MonthlyCharges",
    "MonthlyCharge",
    "Monthly Charges",
    "monthly_charges"
])

total_charge_col = find_column([
    "TotalCharges",
    "TotalCharge",
    "Total Charges",
    "total_charges"
])


# =========================================================
# CHECK CHURN COLUMN
# =========================================================

if churn_col is None:

    st.error(
        "Churn column was not found in the dataset."
    )

    st.write(
        "Available columns:",
        list(df.columns)
    )

    st.stop()


# =========================================================
# NORMALIZE CHURN VALUES
# =========================================================

def is_churned(value):

    value = str(value).strip().lower()

    return value in [
        "yes",
        "y",
        "churned",
        "true",
        "1",
        "left",
        "exited"
    ]


df["ChurnFlag"] = df[churn_col].apply(is_churned)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🎯 Dashboard Filters")


# =========================================================
# CONTRACT FILTER
# =========================================================

if contract_col:

    contract_values = sorted(
        df[contract_col]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_contract = st.sidebar.multiselect(
        "Contract Type",
        contract_values,
        default=contract_values
    )

else:

    selected_contract = None


# =========================================================
# PAYMENT METHOD FILTER
# =========================================================

if payment_col:

    payment_values = sorted(
        df[payment_col]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_payment = st.sidebar.multiselect(
        "Payment Method",
        payment_values,
        default=payment_values
    )

else:

    selected_payment = None


# =========================================================
# TENURE FILTER
# =========================================================

if tenure_col:

    df[tenure_col] = pd.to_numeric(
        df[tenure_col],
        errors="coerce"
    )

    min_tenure = int(df[tenure_col].min())
    max_tenure = int(df[tenure_col].max())

    selected_tenure = st.sidebar.slider(
        "Tenure (Months)",
        min_value=min_tenure,
        max_value=max_tenure,
        value=(min_tenure, max_tenure)
    )

else:

    selected_tenure = None


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


if contract_col:

    filtered_df = filtered_df[
        filtered_df[contract_col]
        .astype(str)
        .isin(selected_contract)
    ]


if payment_col:

    filtered_df = filtered_df[
        filtered_df[payment_col]
        .astype(str)
        .isin(selected_payment)
    ]


if tenure_col:

    filtered_df = filtered_df[
        filtered_df[tenure_col].between(
            selected_tenure[0],
            selected_tenure[1]
        )
    ]


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_customers = len(filtered_df)


if total_customers > 0:

    churned_customers = int(
        filtered_df["ChurnFlag"].sum()
    )

    retained_customers = (
        total_customers - churned_customers
    )

    churn_rate = (
        churned_customers /
        total_customers
    ) * 100

    retention_rate = (
        retained_customers /
        total_customers
    ) * 100

else:

    churned_customers = 0
    retained_customers = 0
    churn_rate = 0
    retention_rate = 0


# =========================================================
# REVENUE AT RISK
# =========================================================

revenue_at_risk = 0


if monthly_charge_col:

    filtered_df[monthly_charge_col] = pd.to_numeric(
        filtered_df[monthly_charge_col],
        errors="coerce"
    )

    revenue_at_risk = filtered_df.loc[
        filtered_df["ChurnFlag"],
        monthly_charge_col
    ].sum()


# =========================================================
# AVERAGE TENURE
# =========================================================

average_tenure = 0


if tenure_col:

    average_tenure = filtered_df[
        tenure_col
    ].mean()


# =========================================================
# KPI SECTION
# =========================================================

st.subheader("📌 Key Performance Indicators")


k1, k2, k3, k4, k5 = st.columns(5)


k1.metric(
    "Total Customers",
    f"{total_customers:,}"
)

k2.metric(
    "Churn Rate",
    f"{churn_rate:.2f}%"
)

k3.metric(
    "Retention Rate",
    f"{retention_rate:.2f}%"
)

k4.metric(
    "Revenue at Risk",
    f"₹{revenue_at_risk:,.2f}"
)

k5.metric(
    "Avg Tenure",
    f"{average_tenure:.1f} months"
)


st.divider()


# =========================================================
# CHURN VS RETENTION
# =========================================================

st.subheader("📉 Churn vs Retention")


col1, col2 = st.columns(2)


# =========================================================
# PIE CHART
# =========================================================

with col1:

    status_data = pd.DataFrame({

        "Status": [
            "Retained",
            "Churned"
        ],

        "Customers": [
            retained_customers,
            churned_customers
        ]
    })


    fig = px.pie(
        status_data,
        names="Status",
        values="Customers",
        hole=0.45,
        title="Customer Churn Distribution"
    )


    fig.update_layout(
        margin=dict(
            t=50,
            l=20,
            r=20,
            b=20
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# BAR CHART
# =========================================================

with col2:

    churn_data = pd.DataFrame({

        "Status": [
            "Retained",
            "Churned"
        ],

        "Customers": [
            retained_customers,
            churned_customers
        ]
    })


    fig2 = px.bar(
        churn_data,
        x="Status",
        y="Customers",
        text="Customers",
        title="Customer Status"
    )


    fig2.update_traces(
        textposition="outside"
    )


    fig2.update_layout(
        margin=dict(
            t=50,
            l=20,
            r=20,
            b=20
        )
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# =========================================================
# CONTRACT ANALYSIS
# =========================================================

if contract_col:

    st.subheader("📄 Churn by Contract Type")


    contract_analysis = (
        filtered_df
        .groupby(contract_col)["ChurnFlag"]
        .agg(["count", "sum"])
        .reset_index()
    )


    contract_analysis["ChurnRate"] = (
        contract_analysis["sum"] /
        contract_analysis["count"]
    ) * 100


    fig3 = px.bar(
        contract_analysis,
        x=contract_col,
        y="ChurnRate",
        text="ChurnRate",
        title="Churn Rate by Contract"
    )


    fig3.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )


    fig3.update_layout(
        yaxis_title="Churn Rate (%)",
        xaxis_title="Contract Type"
    )


    st.plotly_chart(
        fig3,
        use_container_width=True
    )


# =========================================================
# TENURE ANALYSIS
# =========================================================

if tenure_col:

    st.subheader("⏳ Churn by Tenure")


    tenure_df = filtered_df.copy()


    tenure_df["TenureGroup"] = pd.cut(

        tenure_df[tenure_col],

        bins=[
            -1,
            6,
            12,
            24,
            48,
            float("inf")
        ],

        labels=[
            "0-6 months",
            "7-12 months",
            "13-24 months",
            "25-48 months",
            "49+ months"
        ]
    )


    tenure_analysis = (
        tenure_df
        .groupby(
            "TenureGroup",
            observed=False
        )["ChurnFlag"]
        .agg(["count", "sum"])
        .reset_index()
    )


    tenure_analysis["ChurnRate"] = (
        tenure_analysis["sum"] /
        tenure_analysis["count"]
    ) * 100


    fig4 = px.bar(
        tenure_analysis,
        x="TenureGroup",
        y="ChurnRate",
        text="ChurnRate",
        title="Churn Rate by Tenure Group"
    )


    fig4.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )


    fig4.update_layout(
        xaxis_title="Tenure",
        yaxis_title="Churn Rate (%)"
    )


    st.plotly_chart(
        fig4,
        use_container_width=True
    )


# =========================================================
# PAYMENT METHOD ANALYSIS
# =========================================================

if payment_col:

    st.subheader("💳 Churn by Payment Method")


    payment_analysis = (
        filtered_df
        .groupby(payment_col)["ChurnFlag"]
        .agg(["count", "sum"])
        .reset_index()
    )


    payment_analysis["ChurnRate"] = (
        payment_analysis["sum"] /
        payment_analysis["count"]
    ) * 100


    fig5 = px.bar(
        payment_analysis,
        x=payment_col,
        y="ChurnRate",
        text="ChurnRate",
        title="Churn Rate by Payment Method"
    )


    fig5.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )


    fig5.update_layout(
        xaxis_title="Payment Method",
        yaxis_title="Churn Rate (%)"
    )


    st.plotly_chart(
        fig5,
        use_container_width=True
    )


# =========================================================
# CUSTOMER SEGMENTS
# =========================================================

st.subheader("👥 Customer Segments")


def create_segment(row):

    if row["ChurnFlag"]:

        return "High Risk"


    if tenure_col:

        tenure = row[tenure_col]


        if pd.isna(tenure):

            return "Medium Risk"


        if tenure < 12:

            return "High Risk"


        elif tenure < 24:

            return "Medium Risk"


        else:

            return "Low Risk"


    return "Medium Risk"


filtered_df["CustomerSegment"] = filtered_df.apply(
    create_segment,
    axis=1
)


segment_counts = (
    filtered_df["CustomerSegment"]
    .value_counts()
    .reset_index()
)


segment_counts.columns = [
    "CustomerSegment",
    "Customers"
]


col1, col2 = st.columns(2)


# =========================================================
# SEGMENT BAR CHART
# =========================================================

with col1:

    fig6 = px.bar(
        segment_counts,
        x="CustomerSegment",
        y="Customers",
        text="Customers",
        title="Customer Segments"
    )


    fig6.update_traces(
        textposition="outside"
    )


    st.plotly_chart(
        fig6,
        use_container_width=True
    )


# =========================================================
# SEGMENT PIE CHART
# =========================================================

with col2:

    fig7 = px.pie(
        segment_counts,
        names="CustomerSegment",
        values="Customers",
        hole=0.4,
        title="Customer Segment Distribution"
    )


    st.plotly_chart(
        fig7,
        use_container_width=True
    )


# =========================================================
# KEY INSIGHTS
# =========================================================

st.subheader("💡 Key Insights")


st.write(
    f"• The current filtered customer base contains "
    f"**{total_customers:,} customers**."
)


st.write(
    f"• The churn rate is "
    f"**{churn_rate:.2f}%**, while the retention rate is "
    f"**{retention_rate:.2f}%**."
)


st.write(
    f"• Monthly revenue associated with churned customers "
    f"is approximately "
    f"**₹{revenue_at_risk:,.2f}**."
)


if tenure_col:

    st.write(
        f"• The average customer tenure is "
        f"**{average_tenure:.1f} months**."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Customer Churn KPI Dashboard | Data Analytics Project"
)