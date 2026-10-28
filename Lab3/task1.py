#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 20:25:26 2026

@author: saadali
"""

import numpy as np
import matplotlib.pyplot as plt
from energy_model import energy_balance


# TASK 1: VISUALIZE THE N-LAYER ATMOSPHERE MODEL

# Define parameters
nlayers = 3
S0 = 1350
emissivity = 0.5
albedo = 0.33

# Calculate temperatures and fluxes
temperatures, fluxes = energy_balance(
    nlayers=nlayers,
    S0=S0,
    emissivity=emissivity,
    albedo=albedo,
    debug=True
)


# FIGURE 1: ENERGY BALANCE DIAGRAM

plt.figure(figsize=(8, 6))

# Draw Earth's surface and atmospheric layers
for i in range(nlayers + 1):

    if i == 0:
        label = "Earth's Surface"
    else:
        label = f"Atmospheric Layer {i}"

    plt.hlines(
        y=i,
        xmin=0,
        xmax=5,
        linewidth=3,
        color="blue"
    )

    plt.text(
        5.2,
        i,
        label,
        va="center"
    )


# Draw incoming solar radiation
plt.annotate(
    "",
    xy=(1, 0.1),
    xytext=(1, nlayers + 0.8),
    arrowprops=dict(
        arrowstyle="->",
        color="orange",
        lw=2
    )
)

plt.text(
    1.2,
    nlayers + 0.7,
    "Incoming Solar Radiation",
    fontsize=10
)


# Draw upward infrared radiation
for i in range(nlayers):

    plt.annotate(
        "",
        xy=(2.5, i + 0.9),
        xytext=(2.5, i + 0.1),
        arrowprops=dict(
            arrowstyle="->",
            color="red",
            lw=2
        )
    )


# Draw downward infrared radiation
for i in range(1, nlayers + 1):

    plt.annotate(
        "",
        xy=(3.5, i - 0.9),
        xytext=(3.5, i - 0.1),
        arrowprops=dict(
            arrowstyle="->",
            color="green",
            lw=2
        )
    )


plt.text(2.2, nlayers + 0.5, "Upward IR", color="red")
plt.text(3.5, nlayers + 0.5, "Downward IR", color="green")

plt.xlim(0, 8)
plt.ylim(-0.5, nlayers + 1)

plt.axis("off")
plt.title("N-Layer Atmospheric Energy Balance Model")

plt.tight_layout()
plt.show()


# FIGURE 2: COEFFICIENT MATRIX VISUALIZATION

# Reconstruct the matrix using the same equations
A = np.zeros((nlayers + 1, nlayers + 1))

# Surface equation
A[0, 0] = -1

for j in range(1, nlayers + 1):
    A[0, j] = (1 - emissivity) ** (j - 1)

# Atmospheric equations
for i in range(1, nlayers + 1):

    for j in range(nlayers + 1):

        if i == j:
            A[i, j] = -2

        elif j == 0:
            A[i, j] = emissivity * (
                (1 - emissivity) ** (i - 1)
            )

        else:
            A[i, j] = emissivity * (
                (1 - emissivity) ** (abs(i - j) - 1)
            )


# Plot the coefficient matrix
plt.figure(figsize=(7, 6))

plt.imshow(A, cmap="cividis")

plt.colorbar(label="Coefficient Value")

plt.xlabel("Flux Variable Index")
plt.ylabel("Energy Balance Equation Index")
plt.title("Coefficient Matrix A")

# Show numerical values in each cell
for i in range(nlayers + 1):
    for j in range(nlayers + 1):

        plt.text(
            j,
            i,
            f"{A[i, j]:.2f}",
            ha="center",
            va="center",
            color="black"
        )

plt.xticks(range(nlayers + 1))
plt.yticks(range(nlayers + 1))

plt.tight_layout()
plt.show()


# VALIDATION TEST

# Check that the matrix has the correct dimensions
assert A.shape == (nlayers + 1, nlayers + 1)

# Check that the model returns N+1 temperatures
assert len(temperatures) == nlayers + 1

# Check that all temperatures are positive
assert np.all(temperatures > 0)

print("All validation tests passed!")