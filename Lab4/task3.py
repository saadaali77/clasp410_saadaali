#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 22:39:18 2026

@author: saadali
"""


import numpy as np
import matplotlib.pyplot as plt
from snowball_functions import temp_warm
from snowball_model import snowball, global_average

# Define parameters

npoints = 18
dlat = 180/npoints
lats = np.linspace(dlat/2, 180-dlat/2, npoints)

dt = 10
years = 20000

# Load tuned parameters from Task 2
diffusivity, emissivity = np.load(
    "best_parameters.npy"
)

# Define initial temperatures

hot_initial = np.full(npoints, 60.0)
cold_initial = np.full(npoints, -60.0)
warm_initial = temp_warm(lats)


# Case 1: Hot Earth

lats, hot_Temp = snowball(
    hot_initial,
    diffusivity=diffusivity,
    emissivity=emissivity,
    dt_years=dt,
    years=years,
    albedo_mode="dynamic"
)


# Case 2: Cold Earth

lats, cold_Temp = snowball(
    cold_initial,
    diffusivity=diffusivity,
    emissivity=emissivity,
    dt_years=dt,
    years=years,
    albedo_mode="dynamic"
)


# Case 3: Flash-frozen Earth

# Start with warm Earth but keep the ice albedo
# at 0.6 to represent a sustained ice-covered planet.

lats, frozen_Temp = snowball(
    warm_initial,
    diffusivity=diffusivity,
    emissivity=emissivity,
    dt_years=dt,
    years=years,
    albedo_mode="ice"
)


# Print global average temperatures

print("Hot Earth final average:",
      global_average(hot_Temp, lats))

print("Cold Earth final average:",
      global_average(cold_Temp, lats))

print("Flash Freeze final average:",
      global_average(frozen_Temp, lats))


# Plot the three cases

plt.figure(figsize=(9, 6))

plt.plot(
    lats, hot_Temp,
    marker="o", label="Hot Earth (60°C start)"
)

plt.plot(
    lats, cold_Temp,
    "--", label="Cold Earth (-60°C start)"
)

plt.plot(
    lats, frozen_Temp,
    "-.", label="Flash Freeze (Albedo = 0.6)"
)

plt.axhline(
    -10, color="black", linestyle=":",
    label="Freezing Threshold (-10°C)"
)

plt.xlabel("Latitude (degrees from South Pole)")
plt.ylabel("Temperature (°C)")
plt.title("Task 3: Effect of Initial Conditions")

plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# Validation tests

# Expected: all three simulations return valid temperatures
assert np.all(np.isfinite(hot_Temp))
assert np.all(np.isfinite(cold_Temp))
assert np.all(np.isfinite(frozen_Temp))

# Expected: all three simulations use 18 latitude bands
assert len(hot_Temp) == npoints
assert len(cold_Temp) == npoints
assert len(frozen_Temp) == npoints

print("Task 3 validation passed!")
