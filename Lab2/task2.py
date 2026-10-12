#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 02:04:34 2026

@author: saadali
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode


def competition(t, N, a=1, b=2, c=1, d=3):
    """Calculate population change for two competing species."""

    dNdt = np.zeros(2)

    dNdt[0] = a*N[0]*(1-N[0]) - b*N[0]*N[1]
    dNdt[1] = c*N[1]*(1-N[1]) - d*N[0]*N[1]

    return dNdt


def run_competition(Ninitial, a, b, c, d):
    """Run the competition model using RK45."""

    dt = 0.1
    t_end = 100

    solver = ode(competition).set_integrator("dopri5")

    solver.set_initial_value(Ninitial, 0)
    solver.set_f_params(a, b, c, d)

    time = [0]
    populations = [Ninitial]

    while solver.successful() and solver.t < t_end:

        solver.integrate(solver.t + dt)

        time.append(solver.t)
        populations.append(solver.y.copy())

    return np.array(time), np.array(populations)


# CASE 1: STRONG COMPETITION

Ninitial = np.array([0.3, 0.6])

time1, N1 = run_competition(
    Ninitial,
    a=1,
    b=2,
    c=1,
    d=3
)


# CASE 2: WEAKER COMPETITION

time2, N2 = run_competition(
    Ninitial,
    a=1,
    b=0.5,
    c=1,
    d=0.5
)


# PLOT CASE 1

plt.figure(figsize=(9, 6))

plt.plot(time1, N1[:, 0], label="Species 1")
plt.plot(time1, N1[:, 1], "--", label="Species 2")

plt.xlabel("Time (years)")
plt.ylabel("Population Density")
plt.title("Competition Model: Strong Competition")
plt.legend()
plt.grid()
plt.show()


# PLOT CASE 2

plt.figure(figsize=(9, 6))

plt.plot(time2, N2[:, 0], label="Species 1")
plt.plot(time2, N2[:, 1], "--", label="Species 2")

plt.xlabel("Time (years)")
plt.ylabel("Population Density")
plt.title("Competition Model: Weaker Competition")
plt.legend()
plt.grid()
plt.show()


# Print final populations
print("Strong competition final populations:")
print(N1[-1])

print("Weaker competition final populations:")
print(N2[-1])