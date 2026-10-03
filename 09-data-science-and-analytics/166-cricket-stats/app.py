import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Cricket Statistics Dashboard", page_icon="🏏", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

st.title("🏏 Cricket Statistics Dashboard")
st.markdown("Explore cricket player stats, team rankings, and match data")

# Sample cricket data
PLAYERS = [
    {"Name": "Virat Kohli", "Country": "India", "Role": "Batsman", "Matches": 280, "Runs": 21856, "Avg": 57.32, "SR": 80.2, "HS": 254, "100s": 75, "50s": 111},
    {"Name": "Rohit Sharma", "Country": "India", "Role": "Batsman", "Matches": 243, "Runs": 16578, "Avg": 49.32, "SR": 78.5, "HS": 264, "100s": 59, "50s": 88},
    {"Name": "Babar Azam", "Country": "Pakistan", "Role": "Batsman", "Matches": 115, "Runs": 9727, "Avg": 55.58, "SR": 74.8, "HS": 257, "100s": 34, "50s": 51},
    {"Name": "Joe Root", "Country": "England", "Role": "Batsman", "Matches": 265, "Runs": 19736, "Avg": 50.87, "SR": 72.8, "HS": 254, "100s": 64, "50s": 112},
    {"Name": "Steve Smith", "Country": "Australia", "Role": "Batsman", "Matches": 195, "Runs": 15146, "Avg": 59.32, "SR": 76.2, "HS": 239, "100s": 52, "50s": 80},
    {"Name": "Kane Williamson", "Country": "New Zealand", "Role": "Batsman", "Matches": 198, "Runs": 14438, "Avg": 54.27, "SR": 73.2, "HS": 251, "100s": 48, "50s": 78},
    {"Name": "Rohit Sharma", "Country": "India", "Role": "Batsman", "Matches": 259, "Runs": 11074, "Avg": 48.77, "SR": 85.0, "HS": 209, "100s": 29, "50s": 57},
    {"Name": "David Warner", "Country": "Australia", "Role": "Batsman", "Matches": 228, "Runs": 15945, "Avg": 47.32, "SR": 83.2, "HS": 209, "100s": 48, "50s": 86},
    {"Name": "AB de Villiers", "Country": "South Africa", "Role": "Batsman", "Matches": 228, "Runs": 12538, "Avg": 52.25, "SR": 100.5, "HS": 149, "100s": 47, "50s": 71},
    {"Name": "Chris Gayle", "Country": "West Indies", "Role": "Batsman", "Matches": 303, "Runs": 18465, "Avg": 40.26, "SR": 87.8, "HS": 215, "100s": 65, "50s": 104},
    {"Name": "Shakib Al Hasan", "Country": "Bangladesh", "Role": "All-rounder", "Matches": 223, "Runs": 10245, "Avg": 38.78, "SR": 78.5, "HS": 134, "100s": 26, "50s": 58},
    {"Name": "Ben Stokes", "Country": "England", "Role": "All-rounder", "Matches": 152, "Runs": 7235, "Avg": 42.56, "SR": 82.3, "HS": 182, "100s": 18, "50s": 42},
    {"Name": "Ravichandran Ashwin", "Country": "India", "Role": "Bowler", "Matches": 195, "Runs": 3856, "Avg": 25.42, "SR": 54.8, "HS": 124, "100s": 6, "50s": 23},
    {"Name": "Pat Cummins", "Country": "Australia", "Role": "Bowler", "Matches": 126, "Runs": 2156, "Avg": 28.18, "SR": 52.3, "HS": 63, "100s": 0, "50s": 8},
    {"Name": "Jasprit Bumrah", "Country": "India", "Role": "Bowler", "Matches": 115, "Runs": 1256, "Avg": 22.32, "SR": 48.5, "HS": 47, "100s": 0, "50s": 2},
]

TEAMS = [
    {"Team": "India", "Matches": 1045, "Wins": 612, "Losses": 398, "Draws": 35, "Win%": 58.56},
    {"Team": "Australia", "Matches": 986, "Wins": 569, "Losses": 376, "Draws": 41, "Win%": 57.71},
    {"Team": "England", "Matches": 1056, "Wins": 595, "Losses": 411, "Draws": 50, "Win%": 56.34},
    {"Team": "Pakistan", "Matches": 988, "Wins": 532, "Losses": 415, "Draws": 41, "Win%": 53.85},
    {"Team": "South Africa", "Matches": 845, "Wins": 447, "Losses": 358, "Draws": 40, "Win%": 52.90},
    {"Team": "New Zealand", "Matches": 782, "Wins": 392, "Losses": 352, "Draws": 38, "Win%": 50.13},
    {"Team": "West Indies", "Matches": 875, "Wins": 417, "Losses": 408, "Draws": 50, "Win%": 47.66},
    {"Team": "Sri Lanka", "Matches": 752, "Wins": 343, "Losses": 376, "Draws": 33, "Win%": 45.61},
    {"Team": "Bangladesh", "Matches": 456, "Wins": 157, "Losses": 285, "Draws": 14, "Win%": 34.43},
    {"Team": "Afghanistan", "Matches": 178, "Wins": 82, "Losses": 89, "Draws": 7, "Win%": 46.07},
]

MATCHES = [
    {"Match": "IND vs AUS", "Date": "2024-01-15", "Winner": "India", "Margin": "5 wickets", "Venue": "Sydney"},
    {"Match": "ENG vs SA", "Date": "2024-01-18", "Winner": "England", "Margin": "3 wickets", "Venue": "Johannesburg"},
    {"Match": "PAK vs NZ", "Date": "2024-01-20", "Winner": "New Zealand", "Margin": "7 wickets", "Venue": "Auckland"},
    {"Match": "AUS vs SA", "Date": "2024-01-22", "Winner": "Australia", "Margin": "62 runs", "Venue": "Perth"},
    {"Match": "IND vs ENG", "Date": "2024-01-25", "Winner": "India", "Margin": "4 wickets", "Venue": "Ahmedabad"},
    {"Match": "WI vs BAN", "Date": "2024-01-28", "Winner": "West Indies", "Margin": "8 wickets", "Venue": "Kingston"},
    {"Match": "SL vs AFG", "Date": "2024-02-01", "Winner": "Sri Lanka", "Margin": "45 runs", "Venue": "Colombo"},
    {"Match": "NZ vs PAK", "Date": "2024-02-03", "Winner": "Pakistan", "Margin": "6 wickets", "Venue": "Karachi"},
]

players_df = pd.DataFrame(PLAYERS)
teams_df = pd.DataFrame(TEAMS)
matches_df = pd.DataFrame(MATCHES)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏏 Top Players", "🏆 Team Rankings", "📅 Recent Matches", "📊 Analytics"])

with tab1:
    st.subheader("Top Cricketers by Runs")

    col1, col2 = st.columns([2, 1])
    with col2:
        role_filter = st.selectbox("Filter by Role", ["All", "Batsman", "Bowler", "All-rounder"])
        country_filter = st.selectbox("Filter by Country",
                                     ["All"] + sorted(players_df["Country"].unique().tolist()))

    filtered_players = players_df.copy()
    if role_filter != "All":
        filtered_players = filtered_players[filtered_players["Role"] == role_filter]
    if country_filter != "All":
        filtered_players = filtered_players[filtered_players["Country"] == country_filter]

    filtered_players = filtered_players.sort_values("Runs", ascending=False)

    fig = px.bar(filtered_players, x="Name", y="Runs",
                 title="Top Players by Total Runs",
                 color="Country", text="Runs",
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(template="plotly_dark", height=500)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Most Runs", f"{filtered_players.iloc[0]['Name']}")
    col2.metric("Highest Avg", f"{filtered_players.loc[filtered_players['Avg'].idxmax(), 'Name']}")
    col3.metric("Most 100s", f"{filtered_players.loc[filtered_players['100s'].idxmax(), 'Name']}")
    col4.metric("Highest SR", f"{filtered_players.loc[filtered_players['SR'].idxmax(), 'Name']}")

    st.dataframe(filtered_players, use_container_width=True)

with tab2:
    st.subheader("Team Rankings")

    fig = px.bar(teams_df.sort_values("Win%", ascending=True), x="Team", y="Win%",
                 title="Team Win Percentage",
                 color="Win%", color_continuous_scale="RdYlGn",
                 text="Win%")
    fig.update_layout(template="plotly_dark", height=600)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    # Pie chart for wins
    fig2 = px.pie(teams_df, values="Wins", names="Team",
                 title="Total Wins by Team",
                 hole=0.4)
    fig2.update_layout(template="plotly_dark", height=500)
    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(teams_df.sort_values("Win%", ascending=False), use_container_width=True)

with tab3:
    st.subheader("Recent Match Results")

    for _, match in matches_df.iterrows():
        st.markdown(f"""
        <div style="background: #161b22; padding: 15px; border-radius: 10px; margin: 10px 0;">
            <h4 style="color: #00d4ff; margin: 0;">{match['Match']}</h4>
            <p style="color: #888; margin: 5px 0;">📅 {match['Date']} | 📍 {match['Venue']}</p>
            <p style="color: #4ade80; margin: 0;">🏆 Winner: {match['Winner']}</p>
            <p style="color: #fff; margin: 5px 0;">Margin: {match['Margin']}</p>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.subheader("Performance Analytics")

    # Scatter: Runs vs Average
    fig = px.scatter(players_df, x="Runs", y="Avg", size="100s", color="Role",
                   title="Runs vs Average (Size = Centuries)",
                   hover_data=["Name", "Country"])
    fig.update_layout(template="plotly_dark", height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Strike Rate comparison
    fig2 = px.bar(players_df.sort_values("SR", ascending=False).head(10),
                 x="Name", y="SR", color="SR",
                 color_continuous_scale="Viridis",
                 title="Top 10 by Strike Rate")
    fig2.update_layout(template="plotly_dark", height=400, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

    # Role distribution
    role_counts = players_df["Role"].value_counts().reset_index()
    role_counts.columns = ["Role", "Count"]

    fig3 = px.pie(role_counts, values="Count", names="Role",
                 title="Player Role Distribution",
                 color_discrete_sequence=["#00d4ff", "#4ade80", "#f97316"])
    fig3.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig3, use_container_width=True)

st.caption("Cricket Statistics Dashboard | Sample data for demonstration")
