#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 02:07:30 2026

@author: saadali
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode


def predator_prey(t, N, a=1, b=2, c=1, d=3):
    """Calculate population change for predator and prey."""

    dNdt = np.zeros(2)

    # Prey population
    dNdt[0] = a*N[0] - b*N[0]*N[1]

    # Predator population
    dNdt[1] = -c*N[1] + d*N[0]*N[1]

    return dNdt


def run_predator_prey(Ninitial, a, b, c, d):
    """Run the predator-prey model using RK45."""

    dt = 0.05
    t_end = 100

    solver = ode(predator_prey).set_integrator("dopri5")

    solver.set_initial_value(Ninitial, 0)
    solver.set_f_params(a, b, c, d)

    time = [0]
    populations = [Ninitial]

    while solver.successful() and solver.t < t_end:

        solver.integrate(solver.t + dt)

        time.append(solver.t)
        populations.append(solver.y.copy())

    return np.array(time), np.array(populations)


# CASE 1

Ninitial1 = np.array([0.3, 0.6])

time1, N1 = run_predator_prey(
    Ninitial1,
    a=1,
    b=2,
    c=1,
    d=3
)


# CASE 2: DIFFERENT INITIAL CONDITIONS

Ninitial2 = np.array([0.6, 0.3])

time2, N2 = run_predator_prey(
    Ninitial2,
    a=1,
    b=2,
    c=1,
    d=3
)


# POPULATION VS. TIME

plt.figure(figsize=(9, 6))

plt.plot(time1, N1[:, 0], label="Prey")
plt.plot(time1, N1[:, 1], "--", label="Predator")

plt.xlabel("Time (years)")
plt.ylabel("Population Density")
plt.title("Predator-Prey Populations Over Time")
plt.legend()
plt.grid()
plt.show()


# PHASE DIAGRAM

plt.figure(figsize=(7, 6))

plt.plot(
    N1[:, 0],
    N1[:, 1],
    label="Initial: 0.3 prey, 0.6 predator"
)

plt.plot(
    N2[:, 0],
    N2[:, 1],
    "--",
    label="Initial: 0.6 prey, 0.3 predator"
)

plt.xlabel("Prey Population Density")
plt.ylabel("Predator Population Density")
plt.title("Predator-Prey Phase Diagram")
plt.legend()
plt.grid()
plt.show()