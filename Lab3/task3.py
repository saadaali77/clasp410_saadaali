#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 20:02:52 2026

@author: saadali
"""

import numpy as np
import matplotlib.pyplot as plt
from energy_model import energy_balance


# DEFINE PARAMETERS

S0 = 1350
albedo = 0.33
target_temperature = 288

# PART A: EFFECT OF EMISSIVITY

# Test emissivities from 0.01 to 1
emissivities = np.linspace(0.01, 1, 100)

surface_temperatures = []

# Calculate surface temperature for each emissivity
for e in emissivities:

    temperatures, fluxes = energy_balance(
        nlayers=1,
        S0=S0,
        emissivity=e,
        albedo=albedo
    )

    surface_temperatures.append(temperatures[0])

surface_temperatures = np.array(surface_temperatures)

# Find emissivity closest to 288 K
index = np.argmin(
    abs(surface_temperatures - target_temperature)
)

best_emissivity = emissivities[index]

print("Part A")
print("Emissivity closest to 288 K:", best_emissivity)
print("Surface temperature:", surface_temperatures[index])


# FIGURE 1: EMISSIVITY VS TEMPERATURE

plt.figure(figsize=(8, 5))

plt.plot(
    emissivities,
    surface_temperatures,
    color="blue",
    label="Modeled Surface Temperature"
)

plt.axhline(
    target_temperature,
    color="orange",
    linestyle="--",
    label="Target = 288 K"
)

plt.xlabel("Atmospheric Emissivity")
plt.ylabel("Surface Temperature (K)")
plt.title("Effect of Emissivity on Earth's Surface Temperature")

plt.legend()
plt.grid()
plt.tight_layout()
plt.show()


# PART B: EFFECT OF NUMBER OF LAYERS

emissivity = 0.255

# Test 1 to 20 atmospheric layers
layer_numbers = np.arange(1, 21)

surface_temperatures2 = []

for n in layer_numbers:

    temperatures, fluxes = energy_balance(
        nlayers=int(n),
        S0=S0,
        emissivity=emissivity,
        albedo=albedo
    )

    surface_temperatures2.append(temperatures[0])

surface_temperatures2 = np.array(surface_temperatures2)

# Find number of layers closest to 288 K
index2 = np.argmin(
    abs(surface_temperatures2 - target_temperature)
)

best_layers = layer_numbers[index2]

print("\nPart B")
print("Number of layers:", best_layers)
print("Surface temperature:", surface_temperatures2[index2])


# FIGURE 2: NUMBER OF LAYERS VS TEMPERATURE

plt.figure(figsize=(8, 5))

plt.plot(
    layer_numbers,
    surface_temperatures2,
    marker="o",
    color="blue",
    label="Surface Temperature"
)

plt.axhline(
    target_temperature,
    color="orange",
    linestyle="--",
    label="Target = 288 K"
)

plt.xlabel("Number of Atmospheric Layers")
plt.ylabel("Surface Temperature (K)")
plt.title("Effect of Atmospheric Layers on Surface Temperature")

plt.legend()
plt.grid()
plt.tight_layout()
plt.show()


# FIGURE 3: TEMPERATURE PROFILE

temperatures, fluxes = energy_balance(
    nlayers=int(best_layers),
    S0=S0,
    emissivity=emissivity,
    albedo=albedo
)

# Layer index represents relative altitude
altitude = np.arange(best_layers + 1)

plt.figure(figsize=(8, 5))

plt.plot(
    temperatures,
    altitude,
    marker="o",
    color="blue"
)

plt.xlabel("Temperature (K)")
plt.ylabel("Atmospheric Layer (relative altitude)")
plt.title("Earth Atmospheric Temperature Profile")

plt.grid()
plt.tight_layout()
plt.show()