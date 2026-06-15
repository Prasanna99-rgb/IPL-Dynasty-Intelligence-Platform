import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="IPL Dynasty Intelligence Platform",
    page_icon="🏆",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    dynasty = pd.read_csv("data/ipl_dynasty_rankings.csv")

    franchise = pd.read_csv(
        "data/franchise_rankings.csv"
    )

    dna = pd.read_csv(
        "data/championship_dna_rankings.csv"
    )

    pressure = pd.read_csv(
        "data/pressure_performance_rankings.csv"
    )

    venue = pd.read_csv(
        "data/venue_dominance_rankings.csv"
    )

    return dynasty, franchise, dna, pressure, venue


try:

    dynasty, franchise, dna, pressure, venue = load_data()

except Exception as e:

    st.error(f"Data Loading Error: {e}")
    st.stop()

# --------------------------------------------------
# TEAM COLORS
# --------------------------------------------------

TEAM_COLORS = {
    "Chennai Super Kings": "#FFFF00",
    "Mumbai Indians": "#004BA0",
    "Royal Challengers Bengaluru": "#EC1C24",
    "Kolkata Knight Riders": "#3A225D",
    "Sunrisers Hyderabad": "#FF822A",
    "Delhi Capitals": "#17449B",
    "Rajasthan Royals": "#FF69B4",
    "Punjab Kings": "#D71920",
    "Gujarat Titans": "#1B2133",
    "Lucknow Super Giants": "#00AEEF",
    "Deccan Chargers": "#1E88E5",
    "Pune Warriors India": "#5E35B1",
    "Gujarat Lions": "#FF9800"
}

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🏆 IPL Dynasty Intelligence Platform")

st.markdown("""
### Franchise Analytics Dashboard

Analyze IPL teams using:

- Franchise Strength Score
- Championship DNA Score
- Pressure Performance Score
- Venue Dominance Score
- Dynasty Score™
""")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "🏆 Dynasty Rankings",
        "📊 Franchise Intelligence",
        "🧬 Championship DNA",
        "🔥 Pressure Performance",
        "🏟 Venue Dominance",
        "⚔ Team Comparison"
    ]
)

# --------------------------------------------------
# DYNASTY RANKINGS
# --------------------------------------------------

if page == "🏆 Dynasty Rankings":

    st.subheader("🏆 IPL Dynasty Rankings")

    st.dataframe(
        dynasty,
        use_container_width=True
    )

    colors = [
        TEAM_COLORS.get(team, "#808080")
        for team in dynasty["team"]
    ]

    fig, ax = plt.subplots(figsize=(12,6))

    bars = ax.bar(
        dynasty["team"],
        dynasty["dynasty_score"],
        color=colors
    )

    ax.set_title(
        "IPL Dynasty Rankings",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_ylabel("Dynasty Score")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height()+1,
            f"{bar.get_height():.1f}",
            ha="center"
        )

    plt.tight_layout()

    st.pyplot(fig)

# --------------------------------------------------
# FRANCHISE INTELLIGENCE
# --------------------------------------------------

elif page == "📊 Franchise Intelligence":

    st.subheader("📊 Franchise Intelligence")

    st.dataframe(
        franchise,
        use_container_width=True
    )

# --------------------------------------------------
# CHAMPIONSHIP DNA
# --------------------------------------------------

elif page == "🧬 Championship DNA":

    st.subheader("🧬 Championship DNA")

    st.dataframe(
        dna,
        use_container_width=True
    )

# --------------------------------------------------
# PRESSURE PERFORMANCE
# --------------------------------------------------

elif page == "🔥 Pressure Performance":

    st.subheader("🔥 Pressure Performance")

    st.dataframe(
        pressure,
        use_container_width=True
    )

# --------------------------------------------------
# VENUE DOMINANCE
# --------------------------------------------------

elif page == "🏟 Venue Dominance":

    st.subheader("🏟 Venue Dominance")

    st.dataframe(
        venue,
        use_container_width=True
    )

# --------------------------------------------------
# TEAM COMPARISON
# --------------------------------------------------

elif page == "⚔ Team Comparison":

    st.subheader("⚔ Team Comparison")

    teams = sorted(
        dynasty["team"].unique()
    )

    col1, col2 = st.columns(2)

    with col1:

        team1 = st.selectbox(
            "Select Team 1",
            teams
        )

    with col2:

        team2 = st.selectbox(
            "Select Team 2",
            teams,
            index=min(1, len(teams)-1)
        )

    compare = dynasty[
        dynasty["team"].isin(
            [team1, team2]
        )
    ]

    st.dataframe(
        compare,
        use_container_width=True
    )

    colors = [
        TEAM_COLORS.get(team, "#808080")
        for team in compare["team"]
    ]

    fig, ax = plt.subplots(figsize=(8,4))

    ax.bar(
        compare["team"],
        compare["dynasty_score"],
        color=colors
    )

    ax.set_title(
        "Dynasty Score Comparison"
    )

    ax.set_ylabel(
        "Dynasty Score"
    )

    st.pyplot(fig)

    st.markdown("---")

    selected_team = st.selectbox(
        "Franchise Report Card",
        teams
    )

    report = dynasty[
        dynasty["team"] == selected_team
    ]

    st.dataframe(
        report,
        use_container_width=True
    )

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

st.sidebar.markdown("---")

csv = dynasty.to_csv(index=False)

st.sidebar.download_button(
    label="📥 Download Dynasty Rankings",
    data=csv,
    file_name="ipl_dynasty_rankings.csv",
    mime="text/csv"
)
