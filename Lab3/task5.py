#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 20:06:50 2026

@author: saadali
"""

import numpy as np
import matplotlib.pyplot as plt
from energy_model import energy_balance


# DEFINE PARAMETERS

S0 = 1350
albedo = 0.33
emissivity = 0.5
nlayers = 5


# NORMAL ATMOSPHERE

normal_temperatures, normal_fluxes = energy_balance(
    nlayers=nlayers,
    S0=S0,
    emissivity=emissivity,
    albedo=albedo
)


# NUCLEAR WINTER ATMOSPHERE

winter_temperatures, winter_fluxes = energy_balance(
    nlayers=nlayers,
    S0=S0,
    emissivity=emissivity,
    albedo=albedo,
    nuclear_winter=True,
    debug=True
)


# PRINT RESULTS

print("Normal surface temperature:")
print(normal_temperatures[0])

print("\nNuclear winter surface temperature:")
print(winter_temperatures[0])

print("\nTemperature difference:")
print(normal_temperatures[0] - winter_temperatures[0])


# VALIDATION TEST

# Expected: nuclear winter should cool the surface

assert winter_temperatures[0] < normal_temperatures[0]

print("\nValidation passed: nuclear winter cools the surface.")


# PLOT TEMPERATURE PROFILES

altitude = np.arange(nlayers + 1)

plt.figure(figsize=(8, 5))

plt.plot(
    normal_temperatures,
    altitude,
    marker="o",
    color="blue",
    label="Normal Atmosphere"
)

plt.plot(
    winter_temperatures,
    altitude,
    marker="s",
    linestyle="--",
    color="orange",
    label="Nuclear Winter"
)

plt.xlabel("Temperature (K)")
plt.ylabel("Atmospheric Layer (relative altitude)")
plt.title("Earth Temperature Profile: Nuclear Winter")

plt.legend()
plt.grid()
plt.tight_layout()
plt.show()