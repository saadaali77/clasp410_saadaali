#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 01:46:06 2026

@author: saadali
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode


# LOTKA-VOLTERRA EQUATIONS

def competition(t, N, a=1, b=2, c=1, d=3):
    """Calculate population change for competing species."""

    dNdt = np.zeros(2)

    dNdt[0] = a*N[0]*(1-N[0]) - b*N[0]*N[1]
    dNdt[1] = c*N[1]*(1-N[1]) - d*N[0]*N[1]

    return dNdt


def predator_prey(t, N, a=1, b=2, c=1, d=3):
    """Calculate population change for predator and prey."""

    dNdt = np.zeros(2)

    dNdt[0] = a*N[0] - b*N[0]*N[1]
    dNdt[1] = -c*N[1] + d*N[0]*N[1]

    return dNdt


# EULER SOLVER

def euler_solver(function, Ninitial, dt, t_end):
    """Solve two ODEs using Euler's method."""

    time = np.arange(0, t_end + dt, dt)

    populations = np.zeros((len(time), 2))

    # Starting populations
    populations[0] = Ninitial

    # Move forward one time step at a time
    for i in range(len(time) - 1):

        change = function(time[i], populations[i])

        populations[i + 1] = populations[i] + dt*change

    return time, populations


# RK45 SOLVER

def rk45_solver(function, Ninitial, dt, t_end):
    """Solve two ODEs using SciPy's RK45 method."""

    solver = ode(function).set_integrator("dopri5")
    solver.set_initial_value(Ninitial, 0)

    time = [0]
    populations = [Ninitial]

    while solver.successful() and solver.t < t_end:

        solver.integrate(solver.t + dt)

        time.append(solver.t)
        populations.append(solver.y.copy())

    return np.array(time), np.array(populations)


# INITIAL CONDITIONS

Ninitial = np.array([0.3, 0.6])
t_end = 100


# COMPETITION MODEL

# Required Euler time step
time_euler, N_euler = euler_solver(
    competition, Ninitial, 1, t_end
)

# Smaller Euler time step for comparison
time_small, N_small = euler_solver(
    competition, Ninitial, 0.1, t_end
)

# RK45 solution
time_rk, N_rk = rk45_solver(
    competition, Ninitial, 0.1, t_end
)


plt.figure(figsize=(9, 6))

plt.plot(time_euler, N_euler[:, 0],
         "--", label="Species 1 Euler, dt = 1")

plt.plot(time_euler, N_euler[:, 1],
         "--", label="Species 2 Euler, dt = 1")

plt.plot(time_rk, N_rk[:, 0],
         label="Species 1 RK45")

plt.plot(time_rk, N_rk[:, 1],
         label="Species 2 RK45")

plt.xlabel("Time (years)")
plt.ylabel("Population Density")
plt.title("Competition Model: Euler vs. RK45")
plt.legend()
plt.grid()
plt.show()


# PREDATOR-PREY MODEL

# Required Euler time step
time_euler, N_euler = euler_solver(
    predator_prey, Ninitial, 0.05, t_end
)

# Smaller Euler time step
time_small, N_small = euler_solver(
    predator_prey, Ninitial, 0.01, t_end
)

# RK45 solution
time_rk, N_rk = rk45_solver(
    predator_prey, Ninitial, 0.05, t_end
)


plt.figure(figsize=(9, 6))

plt.plot(time_euler, N_euler[:, 0],
         "--", label="Prey Euler, dt = 0.05")

plt.plot(time_euler, N_euler[:, 1],
         "--", label="Predator Euler, dt = 0.05")

plt.plot(time_rk, N_rk[:, 0],
         label="Prey RK45")

plt.plot(time_rk, N_rk[:, 1],
         label="Predator RK45")

plt.xlabel("Time (years)")
plt.ylabel("Population Density")
plt.title("Predator-Prey Model: Euler vs. RK45")
plt.legend()
plt.grid()
plt.show()