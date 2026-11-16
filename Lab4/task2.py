#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 22:38:07 2026

@author: saadali
"""


import numpy as np
import matplotlib.pyplot as plt
from snowball_functions import temp_warm
from snowball_model import snowball

# Define parameters

npoints = 18
dlat = 180/npoints
lats = np.linspace(dlat/2, 180-dlat/2, npoints)

warm = temp_warm(lats)

dt = 10
years = 20000

# Starting parameter values
diffusivity = 100
emissivity = 0.8


def calculate_error(model, target):
    """
    Calculate the average temperature error.

    Inputs:
        model: Modeled temperatures (C)
        target: Warm-Earth temperatures (C)

    Output:
        RMSE: Root mean square error (C)
    """
    return np.sqrt(np.mean((model-target)**2))


# Part A: Change diffusivity

diffusivities = np.linspace(0, 150, 7)
diff_errors = []

for lam in diffusivities:

    _, Temp = snowball(
        warm,
        diffusivity=lam,
        emissivity=emissivity,
        dt_years=dt,
        years=years
    )

    error = calculate_error(Temp, warm)
    diff_errors.append(error)

# Plot diffusivity against model error
plt.figure(figsize=(8, 5))

plt.plot(
    diffusivities, diff_errors,
    marker="o", label="Temperature Error"
)

plt.xlabel("Thermal Diffusivity (m²/s)")
plt.ylabel("RMSE (°C)")
plt.title("Task 2A: Effect of Diffusivity")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Part B: Change emissivity

emissivities = np.linspace(0, 1, 11)
emiss_errors = []

for e in emissivities:

    _, Temp = snowball(
        warm,
        diffusivity=diffusivity,
        emissivity=e,
        dt_years=dt,
        years=years
    )

    error = calculate_error(Temp, warm)
    emiss_errors.append(error)

# Plot emissivity against model error
plt.figure(figsize=(8, 5))

plt.plot(
    emissivities, emiss_errors,
    marker="s", label="Temperature Error"
)

plt.xlabel("Emissivity")
plt.ylabel("RMSE (°C)")
plt.title("Task 2B: Effect of Emissivity")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# Part C: Find the best combination

best_error = np.inf
best_diffusivity = 0
best_emissivity = 0

# Test both parameters together
for lam in diffusivities:

    for e in np.linspace(0.4, 1.0, 13):

        _, Temp = snowball(
            warm,
            diffusivity=lam,
            emissivity=e,
            dt_years=dt,
            years=years
        )

        error = calculate_error(Temp, warm)

        # Keep the combination with smallest error
        if error < best_error:
            best_error = error
            best_diffusivity = lam
            best_emissivity = e

print("Best diffusivity:", best_diffusivity)
print("Best emissivity:", best_emissivity)
print("Smallest RMSE:", best_error)

# Save these values for Tasks 3 and 4
np.save(
    "best_parameters.npy",
    [best_diffusivity, best_emissivity]
)

# Run model using best parameters
lats, best_Temp = snowball(
    warm,
    diffusivity=best_diffusivity,
    emissivity=best_emissivity,
    dt_years=dt,
    years=years
)

# Plot modeled vs. warm Earth temperatures

plt.figure(figsize=(9, 6))

plt.plot(
    lats, warm,
    "k--", label="Target Warm Earth"
)

plt.plot(
    lats, best_Temp,
    marker="o", label="Tuned Model"
)

plt.xlabel("Latitude (degrees from South Pole)")
plt.ylabel("Temperature (°C)")
plt.title("Task 2: Tuned Warm Earth Model")

plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# Validation

# Expected: every model value is finite
assert np.all(np.isfinite(best_Temp))

# Expected: best fit is at least as good as the
# original parameter pair tested in Part A
_, original_Temp = snowball(
    warm,
    diffusivity=diffusivity,
    emissivity=emissivity,
    dt_years=dt,
    years=years
)

assert best_error <= calculate_error(original_Temp, warm) + 1e-8

print("Task 2 validation passed!")
