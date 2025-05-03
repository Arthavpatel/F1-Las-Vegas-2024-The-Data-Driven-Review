import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import numpy as np
import os

# Enable cache
cache = '/Users/arthavpatel/Desktop/project/f1_cache'
fastf1.Cache.enable_cache(cache)

# Load session
session = fastf1.get_session(2024, 'Spanish Grand Prix', 'Q')
session.load()

# Pick drivers' fastest laps
NOR = session.laps.pick_driver('NOR').pick_fastest()  # Lando Norris
HAM = session.laps.pick_driver('HAM').pick_fastest()  # Lewis Hamilton

# Get telemetry data and add distance
telemetry_nor = NOR.get_car_data().add_distance()
telemetry_ham = HAM.get_car_data().add_distance()

# Set index for distance alignment
telemetry_nor = telemetry_nor.set_index("Distance")
telemetry_ham = telemetry_ham.set_index("Distance")

# Interpolate Hamilton's telemetry to match Norris's distance index
telemetry_ham = telemetry_ham.reindex(telemetry_nor.index, method="nearest")

# Calculate time delta between laps
time_difference = (telemetry_nor["Time"] - telemetry_ham["Time"]).dt.total_seconds()

# Get team colors
color_norris = fastf1.plotting.get_team_color(NOR['Team'], session)
color_hamilton = fastf1.plotting.get_team_color(HAM['Team'], session)

# ----- Sector split calculation -----
s1_time = NOR['Sector1Time']
s2_time = NOR['Sector2Time']

# Convert to total seconds
s1_time_seconds = s1_time.total_seconds()
s2_time_seconds = s1_time_seconds + s2_time.total_seconds()

# Find the closest distance for each sector end
sector1_distance = telemetry_nor[telemetry_nor['Time'].dt.total_seconds() >= s1_time_seconds].index[0]
sector2_distance = telemetry_nor[telemetry_nor['Time'].dt.total_seconds() >= s2_time_seconds].index[0]

# ----- Plotting -----

fig, axes = plt.subplots(5, 1, figsize=(14, 16), sharex=True)

# Delta Time
axes[0].plot(telemetry_nor.index, time_difference, color="green", label="Delta Time (Norris vs Hamilton)")
axes[0].axhline(0, color='black', linestyle='--', linewidth=1)
axes[0].set_ylabel("Delta (s)")
axes[0].legend(loc="upper right")
axes[0].grid(True, linestyle='--', alpha=0.5)

# Speed
axes[1].plot(telemetry_nor.index, telemetry_nor["Speed"], color=color_norris, label="Norris Speed (km/h)")
axes[1].plot(telemetry_ham.index, telemetry_ham["Speed"], color=color_hamilton, label="Hamilton Speed (km/h)")
axes[1].set_ylabel("Speed (km/h)")
axes[1].legend(loc="upper right")
axes[1].grid(True, linestyle='--', alpha=0.5)

# Gear
axes[2].plot(telemetry_nor.index, telemetry_nor["nGear"], color="blue", label="Norris Gear")
axes[2].plot(telemetry_ham.index, telemetry_ham["nGear"], color="purple", label="Hamilton Gear")
axes[2].set_ylabel("Gear")
axes[2].legend(loc="upper right")
axes[2].grid(True, linestyle='--', alpha=0.5)

# Throttle
axes[3].plot(telemetry_nor.index, telemetry_nor["Throttle"], color=color_norris, label="Norris Throttle (%)")
axes[3].plot(telemetry_ham.index, telemetry_ham["Throttle"], color=color_hamilton, label="Hamilton Throttle (%)")
axes[3].set_ylabel("Throttle (%)")
axes[3].legend(loc="upper right")
axes[3].grid(True, linestyle='--', alpha=0.5)

# Brake
axes[4].plot(telemetry_nor.index, telemetry_nor["Brake"], color=color_norris, label="Norris Brake")
axes[4].plot(telemetry_ham.index, telemetry_ham["Brake"], color=color_hamilton, label="Hamilton Brake")
axes[4].set_ylabel("Brake")
axes[4].legend(loc="upper right")
axes[4].grid(True, linestyle='--', alpha=0.5)

# Add sector lines
sector_distances = [sector1_distance, sector2_distance]
sector_labels = ['Sector 1', 'Sector 2']

for ax in axes:
    for dist, label in zip(sector_distances, sector_labels):
        ax.axvline(x=dist, color='red', linestyle='--', alpha=0.7)
        if ax == axes[0]:  # Add text only to top plot
            ax.text(dist, ax.get_ylim()[1], label, rotation=90,
                    verticalalignment='bottom', horizontalalignment='center',
                    fontsize=8, color='red')

# Final touches
fig.suptitle("Fastest Lap Comparison - Lando Norris vs Lewis Hamilton\nSpanish GP 2024 Qualifying", fontsize=16, y=1.03)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.subplots_adjust(top=0.93)
plt.xlabel("Distance (m)")

plt.show()
