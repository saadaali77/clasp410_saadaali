#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 00:53:51 2026

@author: saadali
"""

import numpy as np
import matplotlib.pyplot as plt


# Define variables

T0 = 90          # Initial coffee temperature (degrees C)
T_env = 20       # Room temperature (degrees C)
k = 0.01         # Cooling constant (1/s)
t_end = 300      # How long we run the model (seconds)


# Euler's method

def euler_coffee(dt):
    """
    Solve the coffee cooling problem using Euler's method.
    dt is the time step in seconds.
    """

    # Create time values
    time = np.arange(0, t_end + dt, dt)

    # Create an array to store temperature
    temperature = np.zeros(len(time))

    # Set first temperature to the initial temperature
    temperature[0] = T0

    # Use Euler's method to calculate each new temperature
    for i in range(len(time) - 1):

        temperature[i + 1] = (
            temperature[i]
            - k * dt * (temperature[i] - T_env)
        )

    return time, temperature


# Analytic solution

# Use small time spacing to make the analytic curve smooth
time_exact = np.linspace(0, t_end, 500)

temperature_exact = (
    T_env
    + (T0 - T_env) * np.exp(-k * time_exact)
)

# Try different time steps

time_1, temp_1 = euler_coffee(1)
time_10, temp_10 = euler_coffee(10)
time_30, temp_30 = euler_coffee(30)


# Plot the results

plt.figure(figsize=(9, 6))

# Analytic solution
plt.plot(
    time_exact,
    temperature_exact,
    label="Analytic Solution",
    linewidth=3
)

# Euler solutions
plt.plot(
    time_1,
    temp_1,
    "--",
    label="Euler: dt = 1 s"
)

plt.plot(
    time_10,
    temp_10,
    "-.",
    label="Euler: dt = 10 s"
)

plt.plot(
    time_30,
    temp_30,
    ":",
    label="Euler: dt = 30 s"
)

# Labels required for the figure
plt.xlabel("Time (s)")
plt.ylabel("Coffee Temperature (°C)")
plt.title("Coffee Cooling: Euler Method vs. Analytic Solution")

plt.legend()
plt.grid()

plt.show()