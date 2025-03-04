import fastf1 as ff1
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Cache directory setup
cache_dir = '/Users/arthavpatel/Desktop/project/f1_cache'
os.makedirs(cache_dir, exist_ok=True)
ff1.Cache.enable_cache(cache_dir)

# Load the race session for the Spanish GP 2024
session = ff1.get_session(2024, 'Spanish Grand Prix', 'Q')
session.load()

# Get all laps
laps = session.laps
laps['LapTime(min)'] = laps['LapTime'].dt.total_seconds() / 60  # Convert LapTime to minutes

# Find the fastest lap overall
fastest_lap = laps.loc[laps['LapTime(min)'].idxmin()]

# Find the fastest lap per team and retain LapTime for proper annotation
# Find the fastest lap per team and retain LapTime and Driver for proper annotation
fastest_team_lap = laps.loc[laps.groupby('Team')['LapTime(min)'].idxmin(), ['Team', 'Driver', 'LapTime(min)']]
fastest_team_lap = fastest_team_lap.sort_values(by='LapTime(min)')
print(fastest_team_lap)

# Define custom colors for each team
team_colors = {
    'Ferrari': 'red',
    'Red Bull Racing': 'darkblue',
    'McLaren': 'orange',
    'RB': 'blue',
    'Mercedes': 'lightblue',
    'Kick Sauber': 'lime',
    'Haas F1 Team': 'black',
    'Alpine': 'pink',
    'Aston Martin': 'green',
    'Williams': 'yellow'
}

# Apply Seaborn theme for better visualization
sns.set_theme(style="darkgrid")

# Ensure correct order for teams
team_order = fastest_team_lap["Team"]  

# Plotting the bar graph
plt.figure(figsize=(7, 4))
ax = sns.barplot(
    data=fastest_team_lap, 
    x="LapTime(min)", 
    y="Team", 
    hue="Team", 
    dodge=False, 
    palette=team_colors, 
    order=team_order  # Ensures the order is correct
)

# Labels and title
plt.xlabel("Fastest Lap Time (minutes)", fontsize=14)
plt.ylabel("Team", fontsize=14)
plt.title(f"Fastest Lap by Team - Spanish GP 2024 Race \nFastest Lap: {fastest_lap['LapTime']}", 
          fontsize=16, fontweight='bold')

# Hide legend (redundant since colors indicate teams)
plt.legend([],[], frameon=False) 

# Add grid lines
plt.grid(axis='both', linestyle='--', alpha=0.7)

# Show the plot
plt.show()
