import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import numpy as np
import os

# Define driver colors for consistency
color_norris = "orange"
color_leclerc = "red"

# Enable cache
cache = '/Users/arthavpatel/Desktop/project/f1_cache'
fastf1.Cache.enable_cache(cache)

# Load session
session = fastf1.get_session(2024, 'Spanish Grand Prix', 'Q')
session.load()

# Pick drivers' fastest laps
NOR = session.laps.pick_driver('NOR').pick_fastest()  # Lando Norris
LEC = session.laps.pick_driver('LEC').pick_fastest()  # Charles Leclerc

print(NOR)
print(LEC)

# Get telemetry data and add distance
telemetry_nor = NOR.get_car_data().add_distance()
telemetry_lec = LEC.get_car_data().add_distance()

# Set index to distance
telemetry_nor = telemetry_nor.set_index("Distance")
telemetry_lec = telemetry_lec.set_index("Distance")

# Align telemetry data
telemetry_lec = telemetry_lec.reindex(telemetry_nor.index, method="nearest")

# Time difference (optional for delta time graph later)
time_difference = (telemetry_nor["Time"] - telemetry_lec["Time"]).dt.total_seconds()

# ----- Sector split calculation (corrected cumulative times) -----
s1_time_seconds = NOR['Sector1Time'].total_seconds()
s2_time_seconds = s1_time_seconds + NOR['Sector2Time'].total_seconds()

sector_split_times = [s1_time_seconds, s2_time_seconds]

sector_distances = [
    telemetry_nor[telemetry_nor['Time'].dt.total_seconds() >= t].index[0]
    for t in sector_split_times
]

sector_labels = ['Sector 1', 'Sector 2']

# ====== Calculate car heading change (approximate steering angle) ======

def calculate_heading(pos_data):
    dx = pos_data['X'].diff()
    dy = pos_data['Y'].diff()
    heading = np.arctan2(dy, dx)
    heading_degrees = np.degrees(heading)
    return heading_degrees

# Get position data
position_nor = NOR.get_pos_data().set_index("SessionTime")
position_lec = LEC.get_pos_data().set_index("SessionTime")

# Calculate heading
heading_nor = calculate_heading(position_nor)
heading_lec = calculate_heading(position_lec)

# Interpolate heading to distance-based index
nor_time_to_distance = telemetry_nor.reset_index().set_index('SessionTime')['Distance']
lec_time_to_distance = telemetry_lec.reset_index().set_index('SessionTime')['Distance']

heading_nor_distance = heading_nor.reindex(nor_time_to_distance.index, method='nearest')
heading_lec_distance = heading_lec.reindex(lec_time_to_distance.index, method='nearest')

heading_nor_distance.index = nor_time_to_distance.values
heading_lec_distance.index = lec_time_to_distance.values

# ====== Plotting ======

fig, axes = plt.subplots(6, 1, figsize=(14, 18), sharex=True)

# Delta Time
axes[0].plot(telemetry_nor.index, time_difference, color="green", label="Delta Time (Norris vs Leclerc)")
axes[0].axhline(0, color='black', linestyle='--', linewidth=1)
axes[0].set_ylabel("Delta (s)")
axes[0].legend(loc="upper right")
axes[0].grid(True, linestyle='--', alpha=0.5)

# Speed
axes[1].plot(telemetry_nor.index, telemetry_nor["Speed"], color=color_norris, label="Norris Speed (km/h)")
axes[1].plot(telemetry_lec.index, telemetry_lec["Speed"], color=color_leclerc, label="Leclerc Speed (km/h)")
axes[1].set_ylabel("Speed (km/h)")
axes[1].legend(loc="upper right")
axes[1].grid(True, linestyle='--', alpha=0.5)

# Gear
axes[2].plot(telemetry_nor.index, telemetry_nor["nGear"], color="blue", label="Norris Gear")
axes[2].plot(telemetry_lec.index, telemetry_lec["nGear"], color="purple", label="Leclerc Gear")
axes[2].set_ylabel("Gear")
axes[2].legend(loc="upper right")
axes[2].grid(True, linestyle='--', alpha=0.5)

# Throttle
axes[3].plot(telemetry_nor.index, telemetry_nor["Throttle"], color=color_norris, label="Norris Throttle (%)")
axes[3].plot(telemetry_lec.index, telemetry_lec["Throttle"], color=color_leclerc, label="Leclerc Throttle (%)")
axes[3].set_ylabel("Throttle (%)")
axes[3].legend(loc="upper right")
axes[3].grid(True, linestyle='--', alpha=0.5)

# Brake
axes[4].plot(telemetry_nor.index, telemetry_nor["Brake"], color=color_norris, label="Norris Brake")
axes[4].plot(telemetry_lec.index, telemetry_lec["Brake"], color=color_leclerc, label="Leclerc Brake")
axes[4].set_ylabel("Brake")
axes[4].legend(loc="upper right")
axes[4].grid(True, linestyle='--', alpha=0.5)

# Heading change (approx. steering)
axes[5].plot(heading_nor_distance.index, heading_nor_distance, color=color_norris, label="Norris Heading Change (°)")
axes[5].plot(heading_lec_distance.index, heading_lec_distance, color=color_leclerc, label="Leclerc Heading Change (°)")
axes[5].set_ylabel("Heading Δ (°)")
axes[5].legend(loc="upper right")
axes[5].grid(True, linestyle='--', alpha=0.5)

# Add sector lines
for ax in axes:
    for dist, label in zip(sector_distances, sector_labels):
        ax.axvline(x=dist, color='red', linestyle='--', alpha=0.7)
        if ax == axes[0]:  # Add text only to top plot
            ax.text(dist, ax.get_ylim()[1], label, rotation=90,
                    verticalalignment='bottom', horizontalalignment='center',
                    fontsize=8, color='red')

# Final touches
fig.suptitle("Fastest Lap Comparison - Lando Norris vs Charles Leclerc\nSpanish GP 2024 Qualifying", fontsize=16, y=1.03)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.subplots_adjust(top=0.93)
plt.xlabel("Distance (m)")

plt.show()
