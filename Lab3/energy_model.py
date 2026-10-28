#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 19:53:48 2026

@author: saadali
"""

import numpy as np

# Stefan-Boltzmann constant (W/m^2/K^4)
sigma = 5.6703e-8


def energy_balance(nlayers, S0, emissivity, albedo,
                   nuclear_winter=False, debug=False):
    """
    Calculate surface and atmospheric temperatures.

    Inputs:
        nlayers: Number of atmospheric layers
        S0: Solar irradiance (W/m^2)
        emissivity: Atmospheric emissivity (0 to 1)
        albedo: Planetary albedo (0 to 1)
        nuclear_winter: If True, sunlight is absorbed
                        by the top atmospheric layer
        debug: If True, print matrices and results

    Outputs:
        temperatures: Surface and layer temperatures (K)
        fluxes: Emitted radiation fluxes (W/m^2)
    """

    # Check that inputs are valid
    if nlayers < 0 or not isinstance(nlayers, int):
        raise ValueError("nlayers must be a nonnegative integer")

    if not 0 <= emissivity <= 1:
        raise ValueError("Emissivity must be between 0 and 1")

    if not 0 <= albedo <= 1:
        raise ValueError("Albedo must be between 0 and 1")

    if nuclear_winter and nlayers < 1:
        raise ValueError("Nuclear winter requires an atmosphere")

    # Create the coefficient matrix and constant vector
    A = np.zeros((nlayers + 1, nlayers + 1))
    b = np.zeros(nlayers + 1)

    # Solar radiation absorbed by the planet
    solar = S0 * (1 - albedo) / 4

    # Surface energy balance

    A[0, 0] = -1

    for j in range(1, nlayers + 1):
        A[0, j] = (1 - emissivity) ** (j - 1)

    # Normal case: sunlight reaches the surface
    if not nuclear_winter:
        b[0] = -solar

    # Atmospheric energy balance

    for i in range(1, nlayers + 1):

        for j in range(nlayers + 1):

            if i == j:
                # Each layer emits upward and downward
                A[i, j] = -2

            elif j == 0:
                # Radiation from the surface
                A[i, j] = emissivity * (
                    (1 - emissivity) ** (i - 1)
                )

            else:
                # Radiation from another atmospheric layer
                A[i, j] = emissivity * (
                    (1 - emissivity) ** (abs(i - j) - 1)
                )

    # Nuclear winter modification


    if nuclear_winter:
        # All incoming sunlight is absorbed at the top
        b[nlayers] = -solar / emissivity

    # Solve Ax = b


    fluxes = np.linalg.solve(A, b)

    # Convert fluxes into temperatures
    temperatures = np.zeros(nlayers + 1)

    # Surface emissivity is 1
    temperatures[0] = (fluxes[0] / sigma) ** 0.25

    # Atmospheric layers have specified emissivity
    if emissivity > 0:
        for i in range(1, nlayers + 1):
            temperatures[i] = (
                fluxes[i] / (emissivity * sigma)
            ) ** 0.25

    # Print detailed information when debugging
    if debug:
        print("Coefficient matrix A:")
        print(A)

        print("\nConstant vector b:")
        print(b)

        print("\nFluxes:")
        print(fluxes)

        print("\nTemperatures:")
        print(temperatures)

        print("\nMatrix residual:")
        print(A @ fluxes - b)

    return temperatures, fluxes