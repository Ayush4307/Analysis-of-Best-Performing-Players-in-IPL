# Analysis-of-Best-Performing-Players-in-IPL
Analysis of Best Performing Players in IPL is a data analysis project that evaluates top IPL players using key performance metrics like runs, strike rate, wickets, and economy rate. It features cleaned data, visualizations, and insights on the best performers across seasons.
# Creating the basic file structure and code files for the Git repository

import os

# Directory structure
project_root = "/mnt/data/Analysis-of-Best-Performing-Players-in-IPL"
folders = [
    "data",
    "notebooks",
    "scripts",
    "visualizations"
]

# Create folders
os.makedirs(project_root, exist_ok=True)
for folder in folders:
    os.makedirs(os.path.join(project_root, folder), exist_ok=True)

# Create README.md
readme_content = """# Analysis of Best Performing Players in IPL

This project analyzes IPL (Indian Premier League) data to identify the best-performing players using Python, Pandas, and visualization libraries.

Tools Used
- Python
- Pandas
- Matplotlib
- Seaborn

Project Structure
- `data/` - Contains the IPL datasets (`matches.csv`, `deliveries.csv`)
- `notebooks/` - Jupyter notebooks for exploration and visualization
- `scripts/` - Python scripts for loading and analyzing the data
- `visualizations/` - Saved plots and charts

Outputs
- Top 10 Batsmen by Runs
- Top 10 Bowlers by Wickets
- Visualizations for key insights

## 📦 Dataset
Download the dataset from: [Kaggle - IPL Data Set](https://www.kaggle.com/datasets/ramjidoolla/ipl-data-set)
Place `matches.csv` and `deliveries.csv` in the `data/` folder.
"""

with open(os.path.join(project_root, "README.md"), "w") as f:
    f.write(readme_content)

# Create requirements.txt
requirements = "pandas\nmatplotlib\nseaborn\n"
with open(os.path.join(project_root, "requirements.txt"), "w") as f:
    f.write(requirements)

# Create analysis script
analysis_code = """import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data
data_path = os.path.join("..", "data")
matches = pd.read_csv(os.path.join(data_path, "matches.csv"))
deliveries = pd.read_csv(os.path.join(data_path, "deliveries.csv"))

# Top 10 Batsmen by Runs
top_batsmen = deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)
print("Top 10 Batsmen by Runs:")
print(top_batsmen)

# Top 10 Bowlers by Wickets
wickets = deliveries[deliveries['dismissal_kind'].notna()]
top_bowlers = wickets.groupby('bowler')['player_dismissed'].count().sort_values(ascending=False).head(10)
print("Top 10 Bowlers by Wickets:")
print(top_bowlers)

# Plot Top Batsmen
plt.figure(figsize=(10,6))
top_batsmen.plot(kind='bar', color='skyblue')
plt.title('Top 10 Batsmen by Runs')
plt.ylabel('Runs')
plt.xlabel('Batsman')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../visualizations/top_batsmen.png")
plt.show()

# Plot Top Bowlers
plt.figure(figsize=(10,6))
top_bowlers.plot(kind='bar', color='orange')
plt.title('Top 10 Bowlers by Wickets')
plt.ylabel('Wickets')
plt.xlabel('Bowler')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../visualizations/top_bowlers.png")
plt.show()
"""

with open(os.path.join(project_root, "scripts", "ipl_analysis.py"), "w") as f:
    f.write(analysis_code)
