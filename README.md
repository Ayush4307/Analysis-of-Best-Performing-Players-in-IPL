<div align="center">
  <h1>🏏 IPL Player Performance Analyzer</h1>
  <p>An Interactive Streamlit Dashboard for analyzing IPL player and team performances from 2008–2024.</p>

  [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ipl-player-analyzer.streamlit.app/)
  [![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
</div>

<br />

## 🚀 Live Demo

**[Click here to view the live dashboard!](https://ipl-player-analyzer.streamlit.app/)**

---

## ✨ Features

- **📊 IPL Overview Dashboard:** Quick metrics on total matches, runs, wickets, and overall top performers.
- **🏏 Top Batsmen Analysis:** Filter top run-scorers by minimum runs and view interactive charts for Strike Rates and Boundaries.
- **🎯 Top Bowlers Analysis:** Explore the best wicket-takers, economy rates, and detailed bowling statistics.
- **🏟️ Venue Analysis:** *NEW!* Discover which stadiums host the most matches and how the toss decision (Bat vs. Field) impacts the win rate at top venues.
- **📅 Season Analysis:** Deep dive into specific IPL seasons to see top performers and winning teams.
- **🏆 Team Analysis:** Visualize the most successful IPL franchises over the years.
- **🔍 Player Search:** Search for any specific player to see their individual IPL career trajectory.

---

## 🛠️ Tech Stack

- **Python** (Core logic & Data pipelines)
- **Streamlit** (Interactive web app framework)
- **Pandas** (Data manipulation and analysis)
- **Plotly** (Dynamic, interactive data visualizations)

---

## ⚡ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ayush4307/Analysis-of-Best-Performing-Players-in-IPL.git
   ```

2. **Navigate to the project folder:**
   ```bash
   cd Analysis-of-Best-Performing-Players-in-IPL
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

---

## 📊 Standalone Data Pipelines

This project also includes standalone scripts for raw data analysis without the UI.

To run the Toss Impact Analysis pipeline:
```bash
python toss_analysis.py
```
This will output `toss_impact_summary.csv` containing detailed statistics on how winning the toss affects the match outcome across all venues.

---

## 🌐 Future Improvements

- [ ] Win probability prediction using Logistic Regression
- [ ] Machine Learning based player performance forecasting
- [ ] Advanced dynamic filtering
- [ ] Live IPL API integration for real-time updates
- [ ] Team vs Team Head-to-Head comparison dashboard

---

## 👨‍💻 Author

**Ayush Singh Pawar**  
B.Tech CSE (Full Stack)
