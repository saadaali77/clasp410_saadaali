#!/usr/bin/env python3

"""
CLaSP 410 Lab 1
Task 1 - Forest Fire Model

This code creates a forest fire model and tests it using a 3x3 grid and a 3x5 grid.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


# Cell values
BARE = 1    #cell is empty of burnable vegetation
FOREST = 2  #cell with happy trees, maybe maple
FIRE = 3    #cell that is actively burning


def spread_fire(forest, prob_spread): 
    # prob_spread is chance to spread to adjacent cells.
    
    """
    Move forest fire forward by one iteration. Fire can spread up, down, left, and right.
    """

    ny, nx = forest.shape   #nx,ny indicates number of cells in X and Y direction.

    # Copy the forest so all changes happen at the end of the iteration
    new_forest = forest.copy()

    for j in range(ny):
        for i in range(nx):

            if forest[j, i] == FIRE:

                # Check cell above
                if j > 0:
                    if forest[j-1, i] == FOREST:
                        if np.random.rand() < prob_spread:
                            new_forest[j-1, i] = FIRE

                # Check cell below
                if j < ny-1:
                    if forest[j+1, i] == FOREST:
                        if np.random.rand() < prob_spread:
                            new_forest[j+1, i] = FIRE

                # Check cell to the left
                if i > 0:
                    if forest[j, i-1] == FOREST:
                        if np.random.rand() < prob_spread:
                            new_forest[j, i-1] = FIRE

                # Check cell to the right
                if i < nx-1:
                    if forest[j, i+1] == FOREST:
                        if np.random.rand() < prob_spread:
                            new_forest[j, i+1] = FIRE

                # Current burning cell becomes burned
                new_forest[j, i] = BARE

    return new_forest


def plot_test(forest0, forest1, forest2, title):
    
    """Plot iterations 0, 1 and 2."""

    forest_cmap = ListedColormap(["tan", "darkgreen", "firebrick"])

    fig, axes = plt.subplots(1, 3, figsize=(10, 4))

    axes[0].imshow(forest0, cmap=forest_cmap, vmin=1, vmax=3)
    axes[0].set_title("Iteration 0")

    axes[1].imshow(forest1, cmap=forest_cmap, vmin=1, vmax=3)
    axes[1].set_title("Iteration 1")

    axes[2].imshow(forest2, cmap=forest_cmap, vmin=1, vmax=3)
    axes[2].set_title("Iteration 2")

    for ax in axes:
        ax.set_xlabel("x cell")
        ax.set_ylabel("y cell")

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()


# for 3x3 VALIDATION

nx = 3
ny = 3
prob_spread = 1.0

# Start with all forest
forest0 = 2 * np.ones([ny, nx], dtype=int)

# Set center cell on fire
forest0[1, 1] = FIRE

# Run two iterations
forest1 = spread_fire(forest0, prob_spread)
forest2 = spread_fire(forest1, prob_spread)

print("3x3 Iteration 0")
print(forest0)

print("3x3 Iteration 1")
print(forest1)

print("3x3 Iteration 2")
print(forest2)

plot_test(
    forest0,
    forest1,
    forest2,
    "3x3 Validation Test"
)


# for 3x5 VALIDATION

nx = 5
ny = 3

forest0 = 2 * np.ones([ny, nx], dtype=int)

# Center cell
forest0[1, 2] = FIRE

forest1 = spread_fire(forest0, prob_spread)
forest2 = spread_fire(forest1, prob_spread)

print("3x5 Iteration 0")
print(forest0)

print("3x5 Iteration 1")
print(forest1)

print("3x5 Iteration 2")
print(forest2)

plot_test(
    forest0,
    forest1,
    forest2,
    "3x5 Validation Test"
)