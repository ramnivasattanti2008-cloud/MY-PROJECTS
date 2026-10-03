"""
Cricket Analysis App
A Streamlit application for analyzing cricket player statistics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Cricket Analysis",
    page_icon="🏏",
    layout="wide"
)

# Dark theme styling
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .css-1d391kg { padding: 2rem; }
    h1, h2, h3 { color: #ffffff; }
    .stats-card { background-color: #1e2530; padding: 1rem; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# Sample cricket player data
@st.cache_data
def load_player_data():
    """Load sample cricket player statistics"""
    data = {
        'player': [
            'Virat Kohli', 'Rohit Sharma', 'Steve Smith', 'Kane Williamson',
            'Joe Root', 'Babar Azam', 'David Warner', 'Ben Stokes',
            'Chris Gayle', 'AB de Villiers', 'Rahul Dravid', 'Sachin Tendulkar'
        ],
        'matches': [280, 240, 138, 159, 256, 123, 161, 192, 465, 424, 509, 664],
        'innings': [251, 220, 126, 147, 238, 113, 154, 176, 450, 408, 490, 630],
        'runs': [21847, 16186, 11520, 12364, 18279, 8654, 12424, 12556, 10476, 12376, 24237, 34357],
        'not_out': [42, 45, 30, 31, 62, 19, 25, 34, 78, 87, 68, 115],
        'highest_score': [254, 264, 239, 251, 254, 225, 335, 192, 400, 149, 270, 200],
        'average': [87.4, 73.6, 91.4, 84.1, 76.8, 76.6, 81.0, 71.5, 68.2, 72.4, 49.5, 53.8],
        'strike_rate': [138.2, 132.4, 129.4, 126.8, 124.6, 128.4, 134.6, 126.2, 142.8, 121.0, 119.0, 116.2],
        'hundreds': [71, 40, 41, 35, 52, 25, 38, 40, 32, 33, 70, 100],
        'fifties': [107, 75, 52, 58, 105, 42, 50, 72, 88, 73, 146, 164],
        'wickets': [4, 8, 0, 22, 5, 26, 0, 105, 268, 1, 1, 46],
        'catches': [156, 128, 124, 140, 182, 78, 142, 156, 201, 232, 120, 115],
        'role': ['Batsman', 'Batsman', 'Batsman', 'Batsman', 'Batsman', 'Batsman',
                 'Batsman', 'All-rounder', 'Batsman', 'Batsman', 'Batsman', 'Batsman']
    }
    return pd.DataFrame(data)

def calculate_batting_average(runs, dismissals):
    """Calculate batting average"""
    with np.errstate(divide='ignore', invalid='ignore'):
        avg = runs / dismissals
        avg = np.where(np.isinf(avg), 0, avg)
        return np.nan_to_num(avg, nan=0)

def main():
    st.title("🏏 Cricket Player Analysis")
    st.markdown("### Analyze cricket player statistics and compare performance")

    # Load data
    df = load_player_data()

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Analysis",
        ["Overview", "Career Stats", "Player Comparison", "Performance Charts"]
    )

    if page == "Overview":
        show_overview(df)
    elif page == "Career Stats":
        show_career_stats(df)
    elif page == "Player Comparison":
        show_comparison(df)
    elif page == "Performance Charts":
        show_charts(df)

def show_overview(df):
    """Display overview statistics"""
    st.header("📊 Overview Statistics")

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_matches = df['matches'].sum()
        st.metric("Total Matches", f"{total_matches:,}")

    with col2:
        total_runs = df['runs'].sum()
        st.metric("Total Runs", f"{total_runs:,}")

    with col3:
        total_hundreds = df['hundreds'].sum()
        st.metric("Total Centuries", f"{total_hundreds}")

    with col4:
        avg_strike_rate = df['strike_rate'].mean()
        st.metric("Avg Strike Rate", f"{avg_strike_rate:.1f}")

    st.divider()

    # Top performers table
    st.subheader("🏆 Top Run Scorers")
    top_scorers = df.nlargest(10, 'runs')[['player', 'matches', 'runs', 'average', 'hundreds', 'strike_rate']]
    st.dataframe(
        top_scorers.style.background_gradient(subset=['runs', 'average'], cmap='Greens'),
        use_container_width=True
    )

def show_career_stats(df):
    """Display detailed career statistics"""
    st.header("📈 Career Statistics")

    # Player selector
    player = st.selectbox("Select Player", df['player'].unique())
    player_data = df[df['player'] == player].iloc[0]

    # Player info cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <h4>Batting Stats</h4>
            <p>Matches: {player_data['matches']}</p>
            <p>Innings: {player_data['innings']}</p>
            <p>Runs: {player_data['runs']:,}</p>
            <p>Average: {player_data['average']:.2f}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <h4>Milestones</h4>
            <p>Highest Score: {player_data['highest_score']}</p>
            <p>Centuries: {player_data['hundreds']}</p>
            <p>Fifties: {player_data['fifties']}</p>
            <p>Not Outs: {player_data['not_out']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stats-card">
            <h4>Performance</h4>
            <p>Strike Rate: {player_data['strike_rate']:.1f}</p>
            <p>Wickets: {player_data['wickets']}</p>
            <p>Catches: {player_data['catches']}</p>
            <p>Role: {player_data['role']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Career chart
    st.subheader(f"Career Performance - {player}")

    # Create mock timeline data
    years = list(range(2010, 2025))
    mock_runs = np.random.randint(400, 1500, len(years))
    mock_runs = np.cumsum(mock_runs)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=mock_runs,
        mode='lines+markers',
        name='Career Runs',
        line=dict(color='#00d4aa', width=3),
        marker=dict(size=8)
    ))

    fig.update_layout(
        template='plotly_dark',
        xaxis_title='Year',
        yaxis_title='Total Runs',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

def show_comparison(df):
    """Compare multiple players"""
    st.header("🔍 Player Comparison")

    # Multi-select for players
    players = st.multiselect(
        "Select Players to Compare",
        df['player'].unique(),
        default=['Virat Kohli', 'Steve Smith', 'Kane Williamson']
    )

    if len(players) < 2:
        st.warning("Please select at least 2 players for comparison")
        return

    compare_df = df[df['player'].isin(players)]

    # Comparison metrics
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Batting Average Comparison")
        fig = px.bar(
            compare_df,
            x='player',
            y='average',
            color='average',
            color_continuous_scale='Viridis',
            labels={'average': 'Batting Average', 'player': 'Player'}
        )
        fig.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Strike Rate Comparison")
        fig = px.bar(
            compare_df,
            x='player',
            y='strike_rate',
            color='strike_rate',
            color_continuous_scale='Plasma',
            labels={'strike_rate': 'Strike Rate', 'player': 'Player'}
        )
        fig.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Radar chart comparison
    st.subheader("Complete Performance Radar")

    categories = ['runs', 'average', 'hundreds', 'fifties', 'strike_rate', 'catches']

    fig = go.Figure()

    for player in players:
        player_data = df[df['player'] == player].iloc[0]
        values = [player_data[cat] for cat in categories]

        # Normalize values
        max_values = [df[cat].max() for cat in categories]
        normalized = [v/m*100 for v, m in zip(values, max_values)]

        fig.add_trace(go.Scatterpolar(
            r=normalized + [normalized[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=player
        ))

    fig.update_layout(
        polar=dict(bgcolor='#1e2530'),
        showlegend=True,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # Side by side stats
    st.subheader("Detailed Comparison Table")
    display_cols = ['player', 'matches', 'runs', 'average', 'strike_rate', 'hundreds', 'fifties']
    st.dataframe(compare_df[display_cols], use_container_width=True)

def show_charts(df):
    """Display various performance charts"""
    st.header("📊 Performance Charts")

    # Scatter plot: Runs vs Average
    st.subheader("Runs vs Batting Average")
    fig = px.scatter(
        df,
        x='runs',
        y='average',
        size='hundreds',
        color='player',
        hover_data=['matches', 'strike_rate'],
        labels={'runs': 'Total Runs', 'average': 'Batting Average'}
    )
    fig.update_layout(template='plotly_dark', height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Pie chart: Centuries distribution
    st.subheader("Centuries Distribution")
    top_centurions = df.nlargest(8, 'hundreds')
    fig = px.pie(
        top_centurions,
        values='hundreds',
        names='player',
        hole=0.4
    )
    fig.update_layout(template='plotly_dark', height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Line chart: Runs progression
    st.subheader("Top Run Scorers Comparison")
    top5 = df.nlargest(5, 'runs')

    fig = go.Figure()
    for _, player in top5.iterrows():
        years = list(range(2010, 2025))
        mock_runs = np.random.randint(300, 1200, len(years))
        mock_cumulative = np.cumsum(mock_runs)

        fig.add_trace(go.Scatter(
            x=years,
            y=mock_cumulative,
            mode='lines',
            name=player['player']
        ))

    fig.update_layout(
        template='plotly_dark',
        xaxis_title='Year',
        yaxis_title='Career Runs',
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap of correlations
    st.subheader("Statistics Correlation Heatmap")
    numeric_cols = ['matches', 'runs', 'average', 'strike_rate', 'hundreds', 'fifties', 'catches']
    corr_matrix = df[numeric_cols].corr()

    fig = px.imshow(
        corr_matrix,
        labels=dict(color="Correlation"),
        x=numeric_cols,
        y=numeric_cols,
        color_continuous_scale='RdBu'
    )
    fig.update_layout(template='plotly_dark', height=500)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
