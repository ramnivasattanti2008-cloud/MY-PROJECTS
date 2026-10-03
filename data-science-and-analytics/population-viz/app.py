import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="World Population Visualizer", page_icon="🌍", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: #ffffff !important; }
    .big-number { font-size: 3rem; font-weight: bold; color: #00d4ff; }
</style>
""", unsafe_allow_html=True)

st.title("🌍 World Population Visualizer")
st.markdown("Explore global population data with interactive visualizations")

# Embedded population data (World Bank style)
POPULATION_DATA = """
Country,Country_Code,Year,Population,Continent
China,CN,2023,1425887337,Asia
India,IN,2023,1428627663,Asia
United States,US,2023,339996563,North America
Indonesia,ID,2023,277534122,Asia
Pakistan,PK,2023,240485658,Asia
Brazil,BR,2023,216422446,South America
Nigeria,NG,2023,223804632,Africa
Bangladesh,BD,2023,172954319,Asia
Russia,RU,2023,144444359,Europe
Mexico,MX,2023,128456082,North America
Japan,JP,2023,123294513,Asia
Ethiopia,ET,2023,126527060,Africa
Philippines,PH,2023,117337368,Asia
Egypt,EG,2023,112716599,Africa
Vietnam,VN,2023,98858950,Asia
DR Congo,CD,2023,102262808,Africa
Turkey,TR,2023,85816199,Europe
Iran,IR,2023,87596853,Asia
Germany,DE,2023,83294633,Europe
Thailand,TH,2023,71801279,Asia
United Kingdom,GB,2023,67736802,Europe
France,FR,2023,64756584,Europe
South Africa,ZA,2023,60414495,Africa
Italy,IT,2023,58870762,Europe
Kenya,KE,2023,55100586,Africa
Myanmar,MM,2023,54577997,Asia
Colombia,CO,2023,52085168,South America
South Korea,KR,2023,51784059,Asia
Uganda,UG,2023,48582334,Africa
Spain,ES,2023,47558630,Europe
Argentina,AR,2023,45773884,South America
Sudan,SD,2023,48109006,Africa
Algeria,DZ,2023,45606480,Africa
Poland,PL,2023,41026067,Europe
Canada,CA,2023,38781292,North America
Morocco,MA,2023,37840044,Africa
Afghanistan,AF,2023,42239854,Asia
Saudi Arabia,SA,2023,36947025,Asia
Peru,PE,2023,34352719,South America
Angola,AO,2023,36684202,Africa
Malaysia,MY,2023,34308525,Asia
Mozambique,MZ,2023,33897354,Africa
Ghana,GH,2023,34121985,Africa
Nepal,NP,2023,30896590,Asia
Iraq,IQ,2023,45504600,Asia
Netherlands,NL,2023,17618299,Europe
Chile,CL,2023,19629590,South America
Ecuador,EC,2023,18190484,South America
"""

df = pd.read_csv(pd.io.common.StringIO(POPULATION_DATA))

# Continent colors
CONTINENT_COLORS = {
    "Asia": "#FF6B6B",
    "Africa": "#4ECDC4",
    "Europe": "#45B7D1",
    "North America": "#96CEB4",
    "South America": "#FFEAA7",
    "Oceania": "#DDA0DD"
}

# Total world population
total_pop = df["Population"].sum()
st.metric("🌎 Total World Population", f"{total_pop:,}")

# Filters
col1, col2 = st.columns([1, 3])
with col1:
    sort_by = st.selectbox("Sort by", ["Population", "Country"])
with col2:
    continents = st.multiselect("Filter by Continent",
                                options=df["Continent"].unique(),
                                default=df["Continent"].unique())

# Filter data
filtered_df = df[df["Continent"].isin(continents)]
if sort_by == "Country":
    filtered_df = filtered_df.sort_values("Country")
else:
    filtered_df = filtered_df.sort_values("Population", ascending=False)

# Charts
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["📊 Top Countries Bar Chart", "🥧 Continent Distribution", "🔍 Compare Countries"])

with tab1:
    fig = px.bar(filtered_df.head(20), x="Country", y="Population",
                 title="Top 20 Most Populous Countries",
                 color="Population", color_continuous_scale="Viridis",
                 labels={"Population": "Population"})
    fig.update_layout(template="plotly_dark", height=600)
    fig.update_yaxes(title_text="Population")
    fig.update_xaxes(title_text="Country")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    continent_pop = df.groupby("Continent")["Population"].sum().reset_index()
    continent_pop = continent_pop.sort_values("Population", ascending=False)

    fig = px.pie(continent_pop, values="Population", names="Continent",
                 title="Population by Continent",
                 color="Continent", color_discrete_map=CONTINENT_COLORS,
                 hole=0.4)
    fig.update_layout(template="plotly_dark", height=600)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

    # Bar chart for continents
    fig2 = px.bar(continent_pop, x="Continent", y="Population",
                  title="Population by Continent",
                  color="Continent", color_discrete_map=CONTINENT_COLORS)
    fig2.update_layout(template="plotly_dark", height=400, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    selected_countries = st.multiselect("Select countries to compare",
                                        options=df["Country"].tolist(),
                                        default=["India", "China", "United States", "Brazil", "Nigeria"])

    compare_df = df[df["Country"].isin(selected_countries)]

    if len(compare_df) > 0:
        fig = px.bar(compare_df, x="Country", y="Population",
                     title="Country Comparison",
                     color="Continent",
                     color_discrete_map=CONTINENT_COLORS,
                     text="Population")
        fig.update_layout(template="plotly_dark", height=500)
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

        # Horizontal bar for better readability
        fig2 = px.bar(compare_df.sort_values("Population"), x="Population", y="Country",
                     title="Population Comparison (Horizontal)",
                     color="Country", orientation="h")
        fig2.update_layout(template="plotly_dark", height=400, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

# Stats table
st.markdown("---")
st.subheader("📋 Detailed Statistics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Countries", len(df))
col2.metric("Most Populous", df.loc[df["Population"].idxmax(), "Country"])
col3.metric("Largest Region", continent_pop.iloc[0]["Continent"])
col4.metric("Avg Population", f"{df['Population'].mean():,.0f}")

st.dataframe(filtered_df[["Country", "Continent", "Population"]].reset_index(drop=True),
             use_container_width=True, height=400)

st.caption("Data source: World Bank Population Estimates (2023)")
