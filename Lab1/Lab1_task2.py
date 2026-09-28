#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 01:39:43 2026

@author: saadali
"""

#!/usr/bin/env python3

"""
CLaSP 410 Lab 1
Task 2 - Wildfire Experiments

This code tests how P_spread and P_bare affect the amount of forest that burns.
"""

import numpy as np
import matplotlib.pyplot as plt

# Cell values
BARE = 1    #cell is empty of burnable vegetation
FOREST = 2  #cell with happy trees, maybe maple
FIRE = 3    #cell that is actively burning


def make_forest(nx, ny, prob_bare, prob_ignite):
    #prob_ignite is chance of cell to catch fire at start
    #prob_bare is chance of cell to start as bare patch.
    
    """Create starting forest."""

    forest = 2 * np.ones([ny, nx], dtype=int)
        # nx,ny indicates number of cells in X and Y direction.

    for j in range(ny):
        for i in range(nx):

            # Decide if the cell starts bare
            if np.random.rand() < prob_bare:
                forest[j, i] = BARE

            # If it is forest, decide if it starts on fire
            elif np.random.rand() < prob_ignite:
                forest[j, i] = FIRE

    return forest


def spread_fire(forest, prob_spread):
    #prob_spread is chance to spread to adjacent cells
    
    """Move fire forward one iteration."""

    ny, nx = forest.shape
    new_forest = forest.copy()

    for j in range(ny):
        for i in range(nx):

            if forest[j, i] == FIRE:

                if j > 0:
                    if forest[j-1, i] == FOREST:
                        if np.random.rand() < prob_spread:
                            new_forest[j-1, i] = FIRE

                if j < ny-1:
                    if forest[j+1, i] == FOREST:
                        if np.random.rand() < prob_spread:
                            new_forest[j+1, i] = FIRE

                if i > 0:
                    if forest[j, i-1] == FOREST:
                        if np.random.rand() < prob_spread:
                            new_forest[j, i-1] = FIRE

                if i < nx-1:
                    if forest[j, i+1] == FOREST:
                        if np.random.rand() < prob_spread:
                            new_forest[j, i+1] = FIRE

                new_forest[j, i] = BARE

    return new_forest


def run_fire(prob_spread, prob_bare, prob_ignite):
    
    """Run one complete forest fire."""

    nx = 50
    ny = 50
    
    forest = make_forest(
        nx,
        ny,
        prob_bare,
        prob_ignite
    )

    # Number of cells containing trees at the beginning
    initial_forest = np.sum(
        (forest == FOREST) | (forest == FIRE)
    )

    # Count cells that start on fire
    total_burned = np.sum(forest == FIRE)

    # Continue until there is no fire
    while np.any(forest == FIRE):

        forest = spread_fire(
            forest,
            prob_spread
        )

        # Add newly burning cells to total
        total_burned = total_burned + np.sum(forest == FIRE)

    if initial_forest == 0:
        return 0

    fraction_burned = total_burned / initial_forest

    return fraction_burned


# Experiment 1: Change P_spread


spread_values = np.linspace(0, 1, 11)
burned_values = []

prob_bare = 0.10
prob_ignite = 0.01

for prob_spread in spread_values:

    burned = run_fire(
        prob_spread,
        prob_bare,
        prob_ignite
    )

    burned_values.append(burned)


plt.figure()

plt.plot(
    spread_values,
    burned_values,
    marker="o"
)

plt.xlabel("Probability of Spread, P_spread")
plt.ylabel("Fraction of Forest Burned")
plt.title("Effect of P_spread on Wildfire Spread")
plt.ylim(0, 1)

plt.grid()

plt.show()


# Experiment 2: Change P_bare

bare_values = np.linspace(0, 1, 11)
burned_values = []

prob_spread = 0.60
prob_ignite = 0.01

for prob_bare in bare_values:

    burned = run_fire(
        prob_spread,
        prob_bare,
        prob_ignite
    )

    burned_values.append(burned)


plt.figure()

plt.plot(
    bare_values,
    burned_values,
    marker="o"
)

plt.xlabel("Probability of Bare Ground, P_bare")
plt.ylabel("Fraction of Forest Burned")
plt.title("Effect of P_bare on Wildfire Spread")
plt.ylim(0, 1)

plt.grid()

plt.show()