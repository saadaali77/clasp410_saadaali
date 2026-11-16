#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 19:08:09 2026

@author: saadali
"""


import numpy as np
import matplotlib.pyplot as plt
from snowball_functions import temp_warm
from snowball_model import snowball

# Define parameters
npoints = 18
dt = 1
years = 10000
diffusivity = 100
emissivity = 1.0

# Create latitude grid and initial temperatures
dlat = 180/npoints
lats = np.linspace(dlat/2, 180-dlat/2, npoints)
initial = temp_warm(lats)

# Experiment 1: Diffusion only

lats, T_diff = snowball(
    initial,
    diffusivity=diffusivity,
    emissivity=emissivity,
    dt_years=dt,
    years=years,
    spherical=False,
    radiation=False
)

# Experiment 2: Add spherical correction

lats, T_sphere = snowball(
    initial,
    diffusivity=diffusivity,
    emissivity=emissivity,
    dt_years=dt,
    years=years,
    spherical=True,
    radiation=False
)

# Experiment 3: Add radiative forcing

lats, T_full = snowball(
    initial,
    diffusivity=diffusivity,
    emissivity=emissivity,
    dt_years=dt,
    years=years,
    spherical=True,
    radiation=True
)

# Validation tests

# Test 1: Diffusion should leave a constant
# temperature unchanged when there is no forcing.

constant = np.full(npoints, 10.0)

_, T_constant = snowball(
    constant,
    dt_years=dt,
    years=100,
    spherical=False,
    radiation=False
)

assert np.allclose(T_constant, constant)

# Test 2: Diffusion should reduce temperature differences
assert np.ptp(T_diff) < np.ptp(initial)

# Test 3: Results should have the correct number of cells
assert len(T_full) == npoints

# Test 4: Calculated temperatures must be finite
assert np.all(np.isfinite(T_full))

print("All Task 1 validation tests passed!")

# Plot the three model stages

plt.figure(figsize=(9, 6))

plt.plot(
    lats, initial, "k:",
    label="Initial Warm Earth"
)

plt.plot(
    lats, T_diff, "--",
    label="Diffusion Only"
)

plt.plot(
    lats, T_sphere, "-.",
    label="Diffusion + Spherical Correction"
)

plt.plot(
    lats, T_full, "-",
    label="Full Model with Radiation"
)

plt.xlabel("Latitude (degrees from South Pole)")
plt.ylabel("Temperature (°C)")
plt.title("Task 1: Snowball Earth Model Validation")

plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
