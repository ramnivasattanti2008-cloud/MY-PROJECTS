"""
Football Analysis App
A Streamlit application for analyzing football/soccer player statistics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Football Analysis",
    page_icon="⚽",
    layout="wide"
)

# Dark theme styling
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .css-1d391kg { padding: 2rem; }
    h1, h2, h3 { color: #ffffff; }
    .metric-card { background-color: #1e2530; padding: 1.5rem; border-radius: 10px; margin: 0.5rem 0; }
    .player-card { background-color: #1e2530; padding: 1rem; border-radius: 10px; border-left: 4px solid #00d4aa; }
</style>
""", unsafe_allow_html=True)

# Sample football player data
@st.cache_data
def load_player_data():
    """Load sample football player statistics"""
    data = {
        'player': [
            'Erling Haaland', 'Kylian Mbappe', 'Lionel Messi', 'Cristiano Ronaldo',
            'Mohamed Salah', 'Harry Kane', 'Robert Lewandowski', 'Kevin De Bruyne',
            'Vinicius Jr', 'Jude Bellingham', 'Phil Foden', 'Bukayo Saka',
            'Marcus Rashford', 'Ousmane Dembele', 'Jamal Musiala'
        ],
        'club': [
            'Manchester City', 'Real Madrid', 'Inter Miami', 'Al-Nassr',
            'Liverpool', 'Bayern Munich', 'Barcelona', 'Manchester City',
            'Real Madrid', 'Real Madrid', 'Manchester City', 'Arsenal',
            'Manchester United', 'Barcelona', 'Bayern Munich'
        ],
        'position': [
            'Forward', 'Forward', 'Forward', 'Forward',
            'Winger', 'Forward', 'Forward', 'Midfielder',
            'Winger', 'Midfielder', 'Midfielder', 'Winger',
            'Forward', 'Winger', 'Midfielder'
        ],
        'matches': [45, 48, 32, 41, 44, 45, 46, 38, 42, 43, 40, 47, 43, 44, 42],
        'goals': [42, 38, 25, 32, 24, 36, 33, 8, 18, 21, 15, 16, 14, 10, 12],
        'assists': [8, 12, 18, 5, 14, 8, 12, 22, 15, 10, 11, 13, 10, 8, 7],
        'yellow_cards': [4, 5, 2, 6, 3, 4, 5, 3, 6, 7, 2, 4, 5, 3, 4],
        'red_cards': [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        'minutes_played': [3600, 3800, 2500, 3200, 3500, 3600, 3700, 3000, 3300, 3400, 3200, 3700, 3400, 3500, 3300],
        'shots_per_game': [5.2, 4.8, 3.5, 4.2, 3.8, 4.5, 4.9, 2.1, 3.2, 3.0, 2.8, 2.5, 3.0, 2.4, 2.6],
        'pass_accuracy': [76, 82, 89, 81, 83, 85, 78, 92, 79, 88, 90, 84, 82, 85, 87],
        'dribble_success': [58, 65, 72, 61, 68, 62, 55, 78, 82, 75, 80, 73, 70, 78, 76],
        'rating': [8.5, 8.3, 8.1, 7.8, 8.0, 8.4, 8.2, 8.6, 8.1, 8.2, 8.0, 7.9, 7.6, 7.8, 7.9],
        'age': [23, 25, 36, 39, 31, 30, 35, 32, 23, 20, 23, 22, 26, 26, 21],
        'nationality': [
            'Norway', 'France', 'Argentina', 'Portugal',
            'Egypt', 'England', 'Poland', 'Belgium',
            'Brazil', 'England', 'England', 'England',
            'England', 'France', 'Germany'
        ]
    }
    return pd.DataFrame(data)

def calculate_goal_involvement(goals, assists, matches):
    """Calculate goal involvement per match"""
    return (goals + assists) / matches * 90

def main():
    st.title("⚽ Football Player Analysis")
    st.markdown("### Analyze football player statistics and compare performance")

    # Load data
    df = load_player_data()

    # Add calculated columns
    df['goal_involvement'] = df['goals'] + df['assists']
    df['goals_per_match'] = df['goals'] / df['matches']
    df['assists_per_match'] = df['assists'] / df['matches']

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Analysis",
        ["Overview", "Player Stats", "Compare Players", "Visual Analytics"]
    )

    if page == "Overview":
        show_overview(df)
    elif page == "Player Stats":
        show_player_stats(df)
    elif page == "Compare Players":
        show_comparison(df)
    elif page == "Visual Analytics":
        show_charts(df)

def show_overview(df):
    """Display overview statistics"""
    st.header("📊 League Overview")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_goals = df['goals'].sum()
        st.metric("Total Goals", f"{total_goals}")

    with col2:
        total_assists = df['assists'].sum()
        st.metric("Total Assists", f"{total_assists}")

    with col3:
        avg_rating = df['rating'].mean()
        st.metric("Avg Rating", f"{avg_rating:.2f}")

    with col4:
        total_matches = df['matches'].sum()
        st.metric("Total Matches", f"{total_matches}")

    st.divider()

    # Top scorers
    st.subheader("🏆 Top Scorers")
    top_scorers = df.nlargest(10, 'goals')[['player', 'club', 'position', 'goals', 'assists', 'rating']]
    st.dataframe(
        top_scorers.style.background_gradient(subset=['goals'], cmap='Reds'),
        use_container_width=True
    )

    st.divider()

    # Top assists
    st.subheader("🎯 Top Playmakers (Assists)")
    top_assists = df.nlargest(10, 'assists')[['player', 'club', 'assists', 'goal_involvement', 'pass_accuracy']]
    st.dataframe(
        top_assists.style.background_gradient(subset=['assists'], cmap='Blues'),
        use_container_width=True
    )

    st.divider()

    # Best rated
    st.subheader("⭐ Highest Rated Players")
    best_rated = df.nlargest(10, 'rating')[['player', 'club', 'position', 'rating', 'goal_involvement']]
    st.dataframe(
        best_rated.style.background_gradient(subset=['rating'], cmap='Greens'),
        use_container_width=True
    )

def show_player_stats(df):
    """Display detailed player statistics"""
    st.header("👤 Player Statistics")

    # Player selector
    col1, col2 = st.columns([2, 1])

    with col1:
        player = st.selectbox("Select Player", df['player'].unique())

    with col2:
        position_filter = st.selectbox("Filter by Position", ['All'] + df['position'].unique().tolist())

    if position_filter != 'All':
        filtered_df = df[df['position'] == position_filter]
        player = st.selectbox("Select Player", filtered_df['player'].unique())

    player_data = df[df['player'] == player].iloc[0]

    # Player info cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00d4aa;">{player_data['goals']}</h3>
            <p>Goals</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00d4aa;">{player_data['assists']}</h3>
            <p>Assists</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00d4aa;">{player_data['rating']:.1f}</h3>
            <p>Rating</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00d4aa;">{player_data['goal_involvement']}</h3>
            <p>Goal Involvement</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Detailed stats
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Attack Statistics")
        attack_data = {
            'Metric': ['Matches', 'Goals', 'Assists', 'Goals per Match', 'Shots per Game', 'Dribble Success %'],
            'Value': [
                player_data['matches'],
                player_data['goals'],
                player_data['assists'],
                f"{player_data['goals_per_match']:.2f}",
                f"{player_data['shots_per_game']:.1f}",
                f"{player_data['dribble_success']}%"
            ]
        }
        st.table(pd.DataFrame(attack_data).set_index('Metric'))

    with col2:
        st.subheader("Discipline & Passing")
        discipline_data = {
            'Metric': ['Yellow Cards', 'Red Cards', 'Pass Accuracy %', 'Minutes Played', 'Age', 'Nationality'],
            'Value': [
                player_data['yellow_cards'],
                player_data['red_cards'],
                f"{player_data['pass_accuracy']}%",
                player_data['minutes_played'],
                player_data['age'],
                player_data['nationality']
            ]
        }
        st.table(pd.DataFrame(discipline_data).set_index('Metric'))

    # Performance gauge
    st.subheader("Performance Rating Breakdown")

    categories = ['Goals', 'Assists', 'Passing', 'Dribbling', 'Discipline']
    values = [
        player_data['goals_per_match'] * 25,
        player_data['assists_per_match'] * 30,
        player_data['pass_accuracy'],
        player_data['dribble_success'],
        max(0, 100 - player_data['yellow_cards'] * 10 - player_data['red_cards'] * 30)
    ]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=player_data['rating'] * 10,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#00d4aa"},
            'steps': [
                {'range': [0, 60], 'color': "#ff6b6b"},
                {'range': [60, 80], 'color': "#feca57"},
                {'range': [80, 100], 'color': "#00d4aa"}
            ]
        },
        title={'text': f"Overall Rating: {player_data['rating']}"}
    ))

    fig.update_layout(template='plotly_dark', height=300)
    st.plotly_chart(fig, use_container_width=True)

def show_comparison(df):
    """Compare multiple players"""
    st.header("🔍 Player Comparison")

    # Multi-select
    players = st.multiselect(
        "Select Players to Compare",
        df['player'].unique(),
        default=['Erling Haaland', 'Kylian Mbappe', 'Harry Kane']
    )

    if len(players) < 2:
        st.warning("Please select at least 2 players for comparison")
        return

    compare_df = df[df['player'].isin(players)]

    # Key comparison metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Goals Comparison")
        fig = px.bar(
            compare_df,
            x='player',
            y='goals',
            color='goals',
            color_continuous_scale='Reds',
            text='goals'
        )
        fig.update_layout(template='plotly_dark', height=400)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Assists Comparison")
        fig = px.bar(
            compare_df,
            x='player',
            y='assists',
            color='assists',
            color_continuous_scale='Blues',
            text='assists'
        )
        fig.update_layout(template='plotly_dark', height=400)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.subheader("Rating Comparison")
        fig = px.bar(
            compare_df,
            x='player',
            y='rating',
            color='rating',
            color_continuous_scale='Greens',
            text='rating'
        )
        fig.update_layout(template='plotly_dark', height=400)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Radar chart
    st.subheader("Complete Performance Comparison")

    categories = ['goals_per_match', 'assists_per_match', 'pass_accuracy', 'dribble_success', 'rating']
    category_labels = ['Goals/Match', 'Assists/Match', 'Pass %', 'Dribble %', 'Rating']

    fig = go.Figure()

    colors = ['#00d4aa', '#ff6b6b', '#feca57', '#54a0ff', '#9b59b6']

    for i, player in enumerate(players):
        player_data = df[df['player'] == player].iloc[0]
        values = [player_data[cat] * 10 if cat in ['goals_per_match', 'assists_per_match'] else player_data[cat] for cat in categories]

        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=category_labels + [category_labels[0]],
            fill='toself',
            name=player,
            line_color=colors[i % len(colors)]
        ))

    fig.update_layout(
        polar=dict(bgcolor='#1e2530'),
        showlegend=True,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # Detailed comparison table
    st.subheader("Detailed Comparison")
    display_cols = ['player', 'club', 'position', 'goals', 'assists', 'rating', 'pass_accuracy', 'dribble_success']
    st.dataframe(compare_df[display_cols], use_container_width=True)

def show_charts(df):
    """Display various analytics charts"""
    st.header("📊 Visual Analytics")

    # Scatter: Goals vs Assists
    st.subheader("Goals vs Assists")
    fig = px.scatter(
        df,
        x='goals',
        y='assists',
        size='rating',
        color='position',
        hover_data=['player', 'club'],
        labels={'goals': 'Goals', 'assists': 'Assists'}
    )
    fig.update_layout(template='plotly_dark', height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Goals by club
    st.subheader("Goals by Club")
    club_goals = df.groupby('club')['goals'].sum().sort_values(ascending=True)
    fig = px.bar(
        x=club_goals.values,
        y=club_goals.index,
        orientation='h',
        color=club_goals.values,
        color_continuous_scale='Reds'
    )
    fig.update_layout(template='plotly_dark', height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Position distribution
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Position Distribution")
        position_counts = df['position'].value_counts()
        fig = px.pie(
            values=position_counts.values,
            names=position_counts.index,
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Goals by Position")
        position_goals = df.groupby('position')['goals'].sum()
        fig = px.bar(
            x=position_goals.index,
            y=position_goals.values,
            color=position_goals.values,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Rating distribution
    st.subheader("Player Rating Distribution")
    fig = px.histogram(
        df,
        x='rating',
        nbins=10,
        color_discrete_sequence=['#00d4aa']
    )
    fig.update_layout(template='plotly_dark', height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Correlation heatmap
    st.subheader("Statistics Correlation")
    numeric_cols = ['goals', 'assists', 'rating', 'pass_accuracy', 'dribble_success', 'shots_per_game']
    corr_matrix = df[numeric_cols].corr()

    fig = px.imshow(
        corr_matrix,
        labels=dict(color="Correlation"),
        x=['Goals', 'Assists', 'Rating', 'Pass %', 'Dribble %', 'Shots/Game'],
        y=['Goals', 'Assists', 'Rating', 'Pass %', 'Dribble %', 'Shots/Game'],
        color_continuous_scale='RdBu'
    )
    fig.update_layout(template='plotly_dark', height=500)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
