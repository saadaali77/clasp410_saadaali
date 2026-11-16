#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 22:39:51 2026

@author: saadali
"""


import numpy as np
import matplotlib.pyplot as plt
from snowball_model import snowball, global_average

# Define parameters

npoints = 18
dt = 10
years = 20000

# Load parameters found in Task 2
diffusivity, emissivity = np.load(
    "best_parameters.npy"
)

# Start with a completely cold Earth
initial = np.full(npoints, -60.0)

# Solar multiplier values
gamma_up = np.linspace(0.4, 1.4, 21)
gamma_down = np.linspace(1.4, 0.4, 21)

warming_results = []
cooling_results = []

# Part A: Increase solar radiation

for gamma in gamma_up:

    # Run simulation with current solar multiplier
    lats, Temp = snowball(
        initial,
        diffusivity=diffusivity,
        emissivity=emissivity,
        gamma=gamma,
        dt_years=dt,
        years=years,
        albedo_mode="dynamic"
    )

    # Store average global temperature
    average = global_average(Temp, lats)
    warming_results.append(average)

    # Use the previous result for the next simulation
    initial = Temp.copy()

    print("Increasing gamma:", round(gamma, 2),
          "Average Temp:", round(average, 2))


# Part B: Decrease solar radiation

for gamma in gamma_down:

    # Continue from the previous final temperature
    lats, Temp = snowball(
        initial,
        diffusivity=diffusivity,
        emissivity=emissivity,
        gamma=gamma,
        dt_years=dt,
        years=years,
        albedo_mode="dynamic"
    )

    # Store average temperature
    average = global_average(Temp, lats)
    cooling_results.append(average)

    # Use previous result for next simulation
    initial = Temp.copy()

    print("Decreasing gamma:", round(gamma, 2),
          "Average Temp:", round(average, 2))


# Plot temperature vs. solar multiplier

plt.figure(figsize=(9, 6))

plt.plot(
    gamma_up,
    warming_results,
    marker="o",
    label="Increasing Solar Radiation"
)

plt.plot(
    gamma_down,
    cooling_results,
    marker="s",
    linestyle="--",
    label="Decreasing Solar Radiation"
)

plt.xlabel("Solar Multiplier (γ)")
plt.ylabel("Global Average Temperature (°C)")
plt.title("Task 4: Snowball Earth Solar Forcing")

plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# Validation tests

# Expected: 21 results in each direction
assert len(warming_results) == 21
assert len(cooling_results) == 21

# Expected: the multiplier reaches both endpoints
assert np.isclose(gamma_up[0], 0.4)
assert np.isclose(gamma_up[-1], 1.4)
assert np.isclose(gamma_down[-1], 0.4)

# Expected: no invalid temperatures
assert np.all(np.isfinite(warming_results))
assert np.all(np.isfinite(cooling_results))

print("Task 4 validation passed!")
