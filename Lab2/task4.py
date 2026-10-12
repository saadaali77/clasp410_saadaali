#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 02:10:14 2026

@author: saadali
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode


# LORENZ EQUATIONS

def lorenz(t, values, sigma=10, r=23, b=8/3):
    """Calculate the rates of change for x, y, and z."""

    x = values[0]
    y = values[1]
    z = values[2]

    dvalues = np.zeros(3)

    dvalues[0] = -sigma*x + sigma*y
    dvalues[1] = -x*z + r*x - y
    dvalues[2] = x*y - b*z

    return dvalues


# RUN LORENZ MODEL

def run_lorenz(initial, r):
    """Run the Lorenz model using RK45."""

    dt = 0.01
    t_end = 100

    solver = ode(lorenz).set_integrator("dopri5")

    solver.set_initial_value(initial, 0)
    solver.set_f_params(10, r, 8/3)

    time = [0]
    results = [initial]

    while solver.successful() and solver.t < t_end:

        solver.integrate(solver.t + dt)

        time.append(solver.t)
        results.append(solver.y.copy())

    return np.array(time), np.array(results)


# INITIAL CONDITIONS

initial1 = np.array([1.0, 1.0, 1.0])

# Add 10^-5 to each initial value
initial2 = np.array([
    1.00001,
    1.00001,
    1.00001
])


# R = 23

time1, result1 = run_lorenz(initial1, 23)
time2, result2 = run_lorenz(initial2, 23)


plt.figure(figsize=(9, 6))

plt.plot(
    time1,
    result1[:, 0],
    label="Original"
)

plt.plot(
    time2,
    result2[:, 0],
    "--",
    label="Perturbed"
)

plt.xlabel("Time")
plt.ylabel("x")
plt.title("Lorenz Model: r = 23")
plt.legend()
plt.grid()
plt.show()


# R = 25

time1, result1 = run_lorenz(initial1, 25)
time2, result2 = run_lorenz(initial2, 25)


plt.figure(figsize=(9, 6))

plt.plot(
    time1,
    result1[:, 0],
    label="Original"
)

plt.plot(
    time2,
    result2[:, 0],
    "--",
    label="Perturbed"
)

plt.xlabel("Time")
plt.ylabel("x")
plt.title("Lorenz Model: r = 25")
plt.legend()
plt.grid()
plt.show()


# PRINT FINAL VALUES

# r = 23
time1_23, result1_23 = run_lorenz(initial1, 23)
time2_23, result2_23 = run_lorenz(initial2, 23)

print("r = 23 original final values:")
print(result1_23[-1])

print("r = 23 perturbed final values:")
print(result2_23[-1])

#r=25
print("r = 25 original final values:")
print(result1[-1])

print("r = 25 perturbed final values:")
print(result2[-1])