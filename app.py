import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="IPL Player Performance Analyzer",
    page_icon="🏏",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("🏏 IPL Player Performance Analyzer")
st.markdown(
    """
    Analyze IPL player performances across seasons (2008–2024).
    Explore batting, bowling, teams, season-wise statistics, and player insights.
    """
)

st.divider()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("📌 Navigation")

sections = st.sidebar.radio(
    "Select Analysis",
    [
        "Dashboard",
        "Top Batsmen",
        "Top Bowlers",
        "Season Analysis",
        "Team Analysis",
        "Venue Analysis",
        "Player Search"
    ]
)

# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------
if sections == "Dashboard":

    st.header("📊 IPL Overview Dashboard")

    total_matches = matches.shape[0]
    total_teams = pd.concat([matches['team1'], matches['team2']]).nunique()
    total_runs = deliveries['total_runs'].sum()
    total_wickets = deliveries['is_wicket'].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Matches", total_matches)
    col2.metric("Teams", total_teams)
    col3.metric("Runs", total_runs)
    col4.metric("Wickets", total_wickets)

    st.divider()

    # Top Run Scorers
    batting = deliveries.groupby("batter")["batsman_runs"].sum().reset_index()
    batting.columns = ["Player", "Runs"]
    batting = batting.sort_values("Runs", ascending=False).head(10)

    fig = px.bar(
        batting,
        x="Runs",
        y="Player",
        orientation="h",
        color="Runs",
        color_continuous_scale="oranges",
        title="Top 10 Run Scorers"
    )

    fig.update_layout(yaxis=dict(autorange="reversed"))

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# TOP BATSMEN
# ---------------------------------------------------
elif sections == "Top Batsmen":

    st.header("🏏 Top Batsmen")

    min_runs = st.slider("Minimum Runs", 500, 5000, 1000)

    batting = deliveries.groupby("batter").agg(
        runs=("batsman_runs", "sum"),
        balls=("ball", "count"),
        fours=("batsman_runs", lambda x: (x == 4).sum()),
        sixes=("batsman_runs", lambda x: (x == 6).sum())
    ).reset_index()

    batting["strike_rate"] = (
        batting["runs"] / batting["balls"] * 100
    ).round(2)

    batting = batting[batting["runs"] >= min_runs]
    batting = batting.sort_values("runs", ascending=False)

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Top Run Scorers")

        top10 = batting.head(10)

        fig = px.bar(
            top10,
            x="runs",
            y="batter",
            orientation="h",
            color="runs",
            color_continuous_scale="oranges"
        )

        fig.update_layout(yaxis=dict(autorange="reversed"))

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.subheader("Best Strike Rates")

        top_sr = batting.sort_values(
            "strike_rate",
            ascending=False
        ).head(10)

        fig2 = px.bar(
            top_sr,
            x="strike_rate",
            y="batter",
            orientation="h",
            color="strike_rate",
            color_continuous_scale="blues"
        )

        fig2.update_layout(yaxis=dict(autorange="reversed"))

        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📋 Full Batting Statistics")

    st.dataframe(
        batting.rename(columns={
            "batter": "Player",
            "runs": "Runs",
            "balls": "Balls",
            "strike_rate": "Strike Rate",
            "fours": "4s",
            "sixes": "6s"
        }),
        use_container_width=True
    )


# TOP BOWLERS

elif sections == "Top Bowlers":

    st.header("🎯 Top Bowlers")

    wicket_types = [
        "caught",
        "bowled",
        "lbw",
        "stumped",
        "caught and bowled",
        "hit wicket"
    ]

    wickets_df = deliveries[
        deliveries["dismissal_kind"].isin(wicket_types)
    ]

    bowling = wickets_df.groupby("bowler").agg(
        wickets=("dismissal_kind", "count")
    ).reset_index()

    balls = deliveries.groupby("bowler").agg(
        balls=("ball", "count"),
        runs_given=("total_runs", "sum")
    ).reset_index()

    bowling = bowling.merge(balls, on="bowler")

    bowling["economy"] = (
        bowling["runs_given"] / (bowling["balls"] / 6)
    ).round(2)

    bowling = bowling[bowling["wickets"] >= 20]
    bowling = bowling.sort_values("wickets", ascending=False)

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Top Wicket Takers")

        top10 = bowling.head(10)

        fig = px.bar(
            top10,
            x="wickets",
            y="bowler",
            orientation="h",
            color="wickets",
            color_continuous_scale="reds"
        )

        fig.update_layout(yaxis=dict(autorange="reversed"))

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.subheader("Best Economy Rates")

        top_eco = bowling.sort_values(
            "economy"
        ).head(10)

        fig2 = px.bar(
            top_eco,
            x="economy",
            y="bowler",
            orientation="h",
            color="economy",
            color_continuous_scale="greens"
        )

        fig2.update_layout(yaxis=dict(autorange="reversed"))

        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📋 Full Bowling Statistics")

    st.dataframe(
        bowling.rename(columns={
            "bowler": "Player",
            "wickets": "Wickets",
            "balls": "Balls",
            "runs_given": "Runs Given",
            "economy": "Economy"
        }),
        use_container_width=True
    )

# SEASON ANALYSIS

elif sections == "Season Analysis":

    st.header("📅 Season Analysis")

    season = st.selectbox(
        "Select Season",
        sorted(matches["season"].unique(), reverse=True)
    )

    season_matches = matches[matches["season"] == season]

    season_deliveries = deliveries[
        deliveries["match_id"].isin(season_matches["id"])
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric("Matches", len(season_matches))
    col2.metric("Runs", season_deliveries["total_runs"].sum())

    if "winner" in season_matches.columns:
        winner = season_matches.iloc[-1]["winner"]
    else:
        winner = "N/A"

    col3.metric("Winner", winner)

    st.subheader(f"🏏 Top Run Scorers in {season}")

    batting = season_deliveries.groupby(
        "batter"
    )["batsman_runs"].sum().reset_index()

    batting.columns = ["Player", "Runs"]

    batting = batting.sort_values(
        "Runs",
        ascending=False
    ).head(10)

    fig = px.bar(
        batting,
        x="Runs",
        y="Player",
        orientation="h",
        color="Runs",
        color_continuous_scale="oranges"
    )

    fig.update_layout(yaxis=dict(autorange="reversed"))

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# TEAM ANALYSIS
# ---------------------------------------------------
elif sections == "Team Analysis":

    st.header("🏆 Team Analysis")

    winners = matches["winner"].value_counts().reset_index()

    winners.columns = ["Team", "Wins"]

    fig = px.pie(
        winners,
        names="Team",
        values="Wins",
        title="IPL Match Wins Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Most Successful Teams")

    fig2 = px.bar(
        winners.head(10),
        x="Wins",
        y="Team",
        orientation="h",
        color="Wins",
        color_continuous_scale="purples"
    )

    fig2.update_layout(yaxis=dict(autorange="reversed"))

    st.plotly_chart(fig2, use_container_width=True)


# ---------------------------------------------------
# VENUE ANALYSIS
# ---------------------------------------------------
elif sections == "Venue Analysis":

    st.header("🏟️ Venue Analysis")
    
    st.markdown("Discover which stadiums have hosted the most matches and how the toss impacts the game.")
    
    venue_counts = matches["venue"].value_counts().reset_index()
    venue_counts.columns = ["Venue", "Matches Hosted"]
    
    fig = px.bar(
        venue_counts.head(10),
        x="Matches Hosted",
        y="Venue",
        orientation="h",
        color="Matches Hosted",
        color_continuous_scale="teal",
        title="Top 10 Venues by Matches Hosted"
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.subheader("Toss Decision Impact at Top Venues")
    top_venues = venue_counts.head(10)["Venue"].tolist()
    top_venue_matches = matches[matches["venue"].isin(top_venues)]
    
    toss_decision = top_venue_matches.groupby(["venue", "toss_decision"]).size().reset_index(name="Count")
    
    fig2 = px.bar(
        toss_decision,
        x="venue",
        y="Count",
        color="toss_decision",
        barmode="group",
        title="Bat vs Field Decisions at Top Venues"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# PLAYER SEARCH
# ---------------------------------------------------

elif sections == "Player Search":

    st.header("🔍 Player Search")

    all_players = sorted(deliveries["batter"].dropna().unique())

    player = st.selectbox("Select Player", all_players)

    player_data = deliveries[
        deliveries["batter"] == player
    ]

    total_runs = player_data["batsman_runs"].sum()

    total_balls = len(player_data)

    strike_rate = round(
        (total_runs / total_balls) * 100,
        2
    ) if total_balls > 0 else 0

    fours = len(
        player_data[player_data["batsman_runs"] == 4]
    )

    sixes = len(
        player_data[player_data["batsman_runs"] == 6]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Runs", total_runs)
    col2.metric("Strike Rate", strike_rate)
    col3.metric("Fours", fours)
    col4.metric("Sixes", sixes)

    st.divider()

    st.subheader(f"📈 {player} - Season Wise Runs")

    player_matches = player_data.merge(
        matches[["id", "season"]],
        left_on="match_id",
        right_on="id"
    )

    season_runs = player_matches.groupby(
        "season"
    )["batsman_runs"].sum().reset_index()

    season_runs.columns = ["Season", "Runs"]

    fig = px.line(
        season_runs,
        x="Season",
        y="Runs",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.markdown(
    """
    <center>
    Built with ❤️ using Streamlit, Pandas, and Plotly
    </center>
    """,
    unsafe_allow_html=True
)
