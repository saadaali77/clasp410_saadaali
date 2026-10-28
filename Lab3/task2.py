#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 19:57:58 2026

@author: saadali
"""

import numpy as np
from energy_model import energy_balance, sigma


# DEFINE PARAMETERS

S0 = 1350
albedo = 0.33
emissivity = 1.0

# Calculate absorbed solar radiation
solar = S0 * (1 - albedo) / 4

# Expected temperature without an atmosphere
T0 = (solar / sigma) ** 0.25


# TEST 1: NO ATMOSPHERE

temperatures0, fluxes0 = energy_balance(
    nlayers=0,
    S0=S0,
    emissivity=emissivity,
    albedo=albedo,
    debug=True
)

print("\nTest 1: No Atmosphere")
print("Calculated:", temperatures0[0])
print("Expected:", T0)

# Expected: surface temperature equals T0
assert np.isclose(temperatures0[0], T0)


# TEST 2: ONE ATMOSPHERIC LAYER

temperatures1, fluxes1 = energy_balance(
    nlayers=1,
    S0=S0,
    emissivity=emissivity,
    albedo=albedo
)

# Expected temperature from the one-layer model
expected1 = (2 * solar / sigma) ** 0.25

print("\nTest 2: One Layer")
print("Calculated:", temperatures1[0])
print("Expected:", expected1)

# Expected: surface temperature is 2^(1/4) times T0
assert np.isclose(temperatures1[0], expected1)


# TEST 3: TWO ATMOSPHERIC LAYERS

temperatures2, fluxes2 = energy_balance(
    nlayers=2,
    S0=S0,
    emissivity=emissivity,
    albedo=albedo
)

# Expected temperature from the two-layer model
expected2 = (3 * solar / sigma) ** 0.25

print("\nTest 3: Two Layers")
print("Calculated:", temperatures2[0])
print("Expected:", expected2)

# Expected: surface temperature is 3^(1/4) times T0
assert np.isclose(temperatures2[0], expected2)


print("\nAll three validation tests passed!")