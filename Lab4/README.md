# Lab 4: Snowball Earth

## Overview

This lab uses Python to model Earth's temperature at different latitudes. The model includes heat diffusion, spherical geometry, solar radiation, infrared cooling, and ice-albedo feedback.

## Required Libraries

- NumPy
- Matplotlib

## Code Organization

**snowball_functions.py** — Provided course file containing `temp_warm()` and `insolation()`.

**snowball_model.py** — Main numerical solver used by all four tasks. Also contains the area-weighted global temperature calculation.

**task1.py** — Builds the diffusion model, adds spherical correction and radiative forcing, and performs validation tests.

**task2.py** — Tests different values of diffusivity and emissivity, finds the best parameter combination, and compares the result with warm Earth.

**task3.py** — Tests hot Earth, cold Earth, and sustained ice-covered Earth initial conditions.

**task4.py** — Changes solar radiation from γ = 0.4 to 1.4 and back to investigate the stability of Snowball Earth.

## How to Run

1. Place all six Python files in the same folder.
2. Install NumPy and Matplotlib if needed.
3. Run `task1.py` to validate the model.
4. Run `task2.py` to tune the diffusivity and emissivity values.
5. Run `task3.py` to compare different initial temperatures.
6. Run `task4.py` to investigate solar forcing and climate stability.

**Important:** Run Task 2 before Tasks 3 and 4. It creates `best_parameters.npy`, which stores the tuned parameter values used by those tasks.

## Validation

Task 1 checks that constant temperature remains unchanged under pure diffusion, that diffusion reduces temperature differences, and that results are finite.

Task 2 checks the parameter fit and modeled temperature values.

Task 3 checks the numerical outputs and latitude-grid dimensions.

Task 4 checks the solar multiplier ranges, the number of simulations, and the numerical outputs.

## Reproducing Figures

Each task automatically displays its figures using Matplotlib. Run the task scripts in order to reproduce the figures and printed results. The scripts use the parameters stated in the code.

## Model Limitations

This is a simplified climate model. It represents Earth using latitude bands and does not include ocean currents, seasonal changes in temperature, or detailed atmospheric circulation. The flash-freeze test assumes that high surface albedo is maintained throughout the simulation.
