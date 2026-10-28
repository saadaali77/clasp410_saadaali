Lab 3: Atmospheric Energy Balance Model

Overview

This lab uses Python to model how radiation affects the temperature of Earth’s surface and atmospheric layers. The model uses energy balance equations and the Stefan–Boltzmann law to calculate temperatures. It also explores Earth’s greenhouse effect, Venus’s atmosphere, and nuclear winter.

Required Libraries

* NumPy
* Matplotlib

Code Organization

The lab is divided into six Python files:

energy_model.py

* Contains the main energy_balance() function used by all tasks.
* Creates the coefficient matrix for an N-layer atmosphere.
* Uses np.linalg.solve() to calculate radiation fluxes.
* Converts fluxes into temperatures using the Stefan–Boltzmann law.
* Includes a debugging option to print matrices, fluxes, temperatures, and residuals.

task1(2).py — Model Design

* Generates a diagram showing incoming solar radiation and infrared radiation moving between atmospheric layers.
* Visualizes the coefficient matrix for a three-layer atmosphere.
* Tests matrix dimensions and checks that calculated temperatures are positive.

task2(2).py — Model Validation

* Tests the model with zero, one, and two atmospheric layers.
* Compares calculated temperatures with known analytical solutions.
* Uses assert statements to verify the results.

task3(2).py — Earth’s Surface Temperature

* Part A: Tests how atmospheric emissivity affects Earth’s surface temperature.
* Part B: Tests how the number of atmospheric layers affects surface temperature.
* Generates three figures showing emissivity, atmospheric layers, and temperature profiles.

task4(2).py — Venus Atmospheric Model

* Calculates how many atmospheric layers are needed to reach Venus’s approximate surface temperature of 700 K.
* Compares the numerical result with an analytical solution.
* Generates a graph showing surface temperature versus the number of atmospheric layers.

task5.py — Nuclear Winter

* Compares normal atmospheric conditions with nuclear winter.
* Models nuclear winter by allowing the top atmospheric layer to absorb incoming solar radiation.
* Calculates the surface temperature difference.
* Generates a graph comparing both atmospheric temperature profiles.

How to Run the Code

1. Download all six Python files into the same folder.
2. Open the folder in Spyder or another Python environment.
3. Make sure NumPy and Matplotlib are installed.
4. Run the task files separately in order, starting with task1(2).py.
5. Each script automatically displays its figures and prints numerical results where applicable.

Important: Keep energy_model.py in the same folder as the task files because they import the energy_balance() function from it.

Validation Tests

Several tests were included to check that the model works correctly.

Task 1: Checks that the coefficient matrix has the correct dimensions and that all calculated temperatures are positive. The matrix residuals are also printed to verify that the energy balance equations are satisfied.

Task 2: Compares numerical results with analytical solutions for zero, one, and two atmospheric layers. All three tests passed.

Task 4: Compares the calculated Venus surface temperature with the analytical solution. Both produced approximately 700.46 K.

Task 5: Checks that the nuclear winter model produces a lower surface temperature than the normal atmosphere model.
