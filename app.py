import streamlit as st
import pandas as pd

import plotly.express as px

st.set_page_config(
    page_title="COVID-19 India Vaccination Dashboard",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded"
)

excel = pd.ExcelFile("cleaned_covid_data 2.xlsx")

df = pd.read_excel("cleaned_covid_data 2.xlsx", sheet_name="cleaned")

# ==========================
# Professional UI
# ==========================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1 {
    color: #00D4FF;
    text-align: center;
    font-size: 42px;
}

h2, h3 {
    color: white;
}

[data-testid="stMetric"] {
    background-color: #1E1E1E;
    border: 1px solid #2E86C1;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

[data-testid="stMetricValue"] {
    color: #00FF99;
    font-size: 30px;
    font-weight: bold;
}

[data-testid="stSidebar"] {
    background-color: #1E1E1E;
}

</style>
""", unsafe_allow_html=True)



# ==========================
# Sidebar Filter
# ==========================

st.sidebar.header("📍 Filters")

state = st.sidebar.selectbox(
    "Select State",
    ["All States"] + list(df["State/UTs"])
)

if state != "All States":
    filtered_df = df[df["State/UTs"] == state]
else:
    filtered_df = df

# ==========================
# KPI Calculations
# ==========================

total_states = filtered_df["State/UTs"].nunique()
total_population = filtered_df["Population"].sum()
total_dose1 = filtered_df["Dose1"].sum()
total_dose2 = filtered_df["Dose2"].sum()
total_vaccination = filtered_df["Total Vaccination Doses"].sum()

# ==========================
# KPI Cards
# ==========================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("🏙️ States", total_states)

col2.metric(
    "👥 Population",
    f"{total_population/10000000:.1f} Cr"
)

col3.metric(
    "💉 Dose 1",
    f"{total_dose1/10000000:.1f} Cr"
)

col4.metric(
    "💉 Dose 2",
    f"{total_dose2/10000000:.1f} Cr"
)

col5.metric(
    "✅ Total Vaccination",
    f"{total_vaccination/10000000:.1f} Cr"
)

import plotly.express as px
st.markdown("---")

st.subheader("📊 Top 10 States by Total Vaccination")

top10 = (
    filtered_df
    .sort_values("Total Vaccination Doses", ascending=False)
    .head(10)
)

fig = px.bar(
    top10,
    x="Total Vaccination Doses",
    y="State/UTs",
    orientation="h",
    color="Total Vaccination Doses",
    color_continuous_scale="Blues",
    text="Total Vaccination Doses"
)

fig.update_layout(
    height=500,
    title="Top 10 States by Total Vaccination",
    yaxis=dict(autorange="reversed"),
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

#🚀 Phase 5 – 2 Charts Side by Side

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("💉 Dose 1 vs Dose 2")

    fig = px.bar(
        filtered_df,
        x="State/UTs",
        y=["Dose1", "Dose2"],
        barmode="group",
        title="Dose 1 vs Dose 2"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📈 Vaccination Percentage")

    fig = px.bar(
        filtered_df.sort_values(
            "Vaccination %",
            ascending=False
        ),
        x="State/UTs",
        y="Vaccination %",
        color="Vaccination %",
        title="Vaccination Percentage"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

#🚀 Phase 6 – Population Analysis + Precaution Dose
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 Population by State")

    top_population = filtered_df.sort_values(
        "Population",
        ascending=False
    ).head(10)

    fig = px.bar(
        top_population,
        x="Population",
        y="State/UTs",
        orientation="h",
        color="Population",
        color_continuous_scale="Greens",
        title="Top 10 Population States"
    )

    fig.update_layout(
        template="plotly_dark",
        yaxis=dict(autorange="reversed"),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🥧 Precaution Dose Distribution")

    top_precaution = filtered_df.sort_values(
        "Precaution 18-59",
        ascending=False
    ).head(10)

    fig = px.pie(
        top_precaution,
        names="State/UTs",
        values="Precaution 18-59",
        title="Precaution Dose Share"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

#🚀 Phase 7 – Business Insights

st.markdown("---")

st.header("📌 Business Insights")

st.info("""
✅ Uttar Pradesh recorded the highest vaccination doses.

✅ Vaccination is strongly related to population size.

✅ Most states achieved vaccination coverage above 150%.

✅ Precaution doses are much lower than Dose 1 and Dose 2.

✅ Larger states require higher vaccine allocation due to population demand.
""")

#🚀 Phase 8 – Download Button

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "filtered_covid_data.csv",
    "text/csv"
)

st.markdown("---")

st.markdown("""
<div style='text-align:center; color:gray;'>

Developed by <b>Tanmay Padole</b>

Python • Streamlit • Plotly • Pandas

</div>
""", unsafe_allow_html=True)