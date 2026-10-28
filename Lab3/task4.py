#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 20:04:32 2026

@author: saadali
"""

import numpy as np
import matplotlib.pyplot as plt
from energy_model import energy_balance


# DEFINE PARAMETERS

S0 = 2600
albedo = 0.75
emissivity = 1.0

target_temperature = 700

# Test 2 to 150 atmospheric layers
layer_numbers = np.arange(2, 151)

surface_temperatures = []


# CALCULATE TEMPERATURES

for n in layer_numbers:

    temperatures, fluxes = energy_balance(
        nlayers=int(n),
        S0=S0,
        emissivity=emissivity,
        albedo=albedo
    )

    surface_temperatures.append(temperatures[0])

surface_temperatures = np.array(surface_temperatures)


# FIND BEST NUMBER OF LAYERS

index = np.argmin(
    abs(surface_temperatures - target_temperature)
)

best_layers = layer_numbers[index]

# Validate numerical result against analytical solution

solar = S0 * (1 - albedo) / 4
sigma = 5.6703e-8

expected_temperature = (
    (best_layers + 1) * solar / sigma
) ** 0.25

print("Analytical temperature:", expected_temperature)

assert np.isclose(
    surface_temperatures[index],
    expected_temperature
)

print("Validation passed!")

print("Venus Atmospheric Model")
print("Best number of layers:", best_layers)
print("Surface temperature:", surface_temperatures[index])


# PLOT RESULTS

plt.figure(figsize=(8, 5))

plt.plot(
    layer_numbers,
    surface_temperatures,
    color="blue",
    label="Modeled Surface Temperature"
)

plt.axhline(
    target_temperature,
    color="orange",
    linestyle="--",
    label="Target = 700 K"
)

plt.xlabel("Number of Atmospheric Layers")
plt.ylabel("Surface Temperature (K)")
plt.title("Venus: Effect of Atmospheric Layers")

plt.legend()
plt.grid()
plt.tight_layout()
plt.show()