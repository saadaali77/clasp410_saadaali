#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 02:23:54 2026

@author: saadali
"""

#!/usr/bin/env python3

"""
CLaSP 410 Lab 1
Task 3 - Disease Model

This code modifies the forest fire model to study the spread of disease.
"""

import numpy as np
import matplotlib.pyplot as plt

#cell values
DEAD = 0    #dead person
IMMUNE = 1  #immune person
HEALTHY = 2 #healthy person
SICK = 3    #sick person


def make_population(nx, ny, prob_vaccine, prob_sick):
    
    # nx,ny indicates number of cells in X and Y direction.
    #prob_sick is chance people are sick
    
    """Create starting population."""

    population = 2 * np.ones([ny, nx], dtype=int)

    for j in range(ny):
        for i in range(nx):

            # Vaccinated people begin immune
            if np.random.rand() < prob_vaccine:  #prob_vaccine is chance people vaccinated
                population[j, i] = IMMUNE

            # Other people may begin sick
            elif np.random.rand() < prob_sick:
                population[j, i] = SICK

    return population


def spread_disease(population, prob_spread, prob_fatal):
    
    #prob_fatal is chance people die.
    
    """Move the disease forward one iteration."""

    ny, nx = population.shape
    new_population = population.copy()

    for j in range(ny):
        for i in range(nx):

            if population[j, i] == SICK:

                # Try to infect person above
                if j > 0:
                    if population[j-1, i] == HEALTHY:
                        if np.random.rand() < prob_spread:
                            new_population[j-1, i] = SICK

                # Try to infect person below
                if j < ny-1:
                    if population[j+1, i] == HEALTHY:
                        if np.random.rand() < prob_spread:
                            new_population[j+1, i] = SICK

                # Try to infect person to left
                if i > 0:
                    if population[j, i-1] == HEALTHY:
                        if np.random.rand() < prob_spread:
                            new_population[j, i-1] = SICK

                # Try to infect person to right
                if i < nx-1:
                    if population[j, i+1] == HEALTHY:
                        if np.random.rand() < prob_spread:
                            new_population[j, i+1] = SICK

                # Sick person either dies or becomes immune
                if np.random.rand() < prob_fatal:
                    new_population[j, i] = DEAD
                else:
                    new_population[j, i] = IMMUNE

    return new_population


def run_disease(prob_vaccine, prob_fatal):
    
    #prob_vaccine is chance that people are vaccinated.
    
    """Run one disease outbreak until nobody is sick."""

    nx = 50
    ny = 50

    prob_spread = 0.60    #prob_spread is chance to spread to adjacent cells
    prob_sick = 0.01

    population = make_population(
        nx,
        ny,
        prob_vaccine,
        prob_sick
    )

    # Keep track of how many people become infected
    total_infected = np.sum(population == SICK)

    while np.any(population == SICK):

        population = spread_disease(
            population,
            prob_spread,
            prob_fatal
        )

        total_infected = (
            total_infected
            + np.sum(population == SICK)
        )

    total_people = nx * ny

    infected_fraction = total_infected / total_people
    dead_fraction = np.sum(population == DEAD) / total_people

    return infected_fraction, dead_fraction


# Experiment 1: Change Fatality

fatal_values = np.linspace(0, 1, 11)

infected_values = []
dead_values = []

prob_vaccine = 0.10

for prob_fatal in fatal_values:

    infected, dead = run_disease(
        prob_vaccine,
        prob_fatal
    )

    infected_values.append(infected)
    dead_values.append(dead)


plt.figure()

plt.plot(
    fatal_values,
    infected_values,
    marker="o",
    label="Infected"
)

plt.plot(
    fatal_values,
    dead_values,
    marker="s",
    label="Died"
)

plt.xlabel("Probability of Death, P_fatal")
plt.ylabel("Fraction of Population")
plt.title("Effect of Fatality Rate on Disease")
plt.ylim(0, 1)

plt.legend()
plt.grid()

plt.show()


# Experiment 2: Change Vaccination

vaccine_values = np.linspace(0, 1, 11)

infected_values = []
dead_values = []

prob_fatal = 0.20

for prob_vaccine in vaccine_values:

    infected, dead = run_disease(
        prob_vaccine,
        prob_fatal
    )

    infected_values.append(infected)
    dead_values.append(dead)


plt.figure()

plt.plot(
    vaccine_values,
    infected_values,
    marker="o",
    label="Infected"
)

plt.plot(
    vaccine_values,
    dead_values,
    marker="s",
    label="Died"
)

plt.xlabel("Initial Vaccinated Fraction")
plt.ylabel("Fraction of Population")
plt.title("Effect of Vaccination on Disease Spread")
plt.ylim(0, 1)

plt.legend()
plt.grid()

plt.show()