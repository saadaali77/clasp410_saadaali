import numpy as np
from snowball_functions import insolation

# Parameters
S0 = 1370.0                  # Solar constant (W/m^2)
R = 6378e3                   # Earth radius (m)
C = 4.2e6                    # Heat capacity, as tabulated in lab
rho = 1020.0                # Seawater density (kg/m^3)
dz = 50.0                   # Mixed layer depth (m)
sigma = 5.67e-8             # Stefan-Boltzmann constant
seconds_year = 365 * 24 * 60 * 60
albedo_ground = 0.3
albedo_ice = 0.6
freezing_temp = -10.0


def build_matrices(npoints, diffusivity, dt_years):
    """Construct polar no-flux second- and first-difference matrices.

    Inputs: npoints (latitude cells), diffusivity (m^2/s), dt_years (years).
    Outputs: lats (degrees), B (1/m), K (1/m^2), L (dimensionless).
    """
    if npoints < 3:
        raise ValueError("Use at least three latitude cells")
    if diffusivity < 0 or dt_years <= 0:
        raise ValueError("Diffusivity must be nonnegative; time step positive")

    dlat = 180.0 / npoints
    lats = np.linspace(dlat / 2, 180 - dlat / 2, npoints)
    dy = R * np.deg2rad(dlat)
    dt = dt_years * seconds_year

    K = np.zeros((npoints, npoints))
    B = np.zeros((npoints, npoints))
    for i in range(1, npoints - 1):
        K[i, i - 1] = 1
        K[i, i] = -2
        K[i, i + 1] = 1
        B[i, i - 1] = -1 / (2 * dy)
        B[i, i + 1] = 1 / (2 * dy)

    # T[-1] = T[1], so the first row is [-2, 2, 0, ...].
    # Likewise the final row is [..., 2, -2].
    K[0, 0], K[0, 1] = -2, 2
    K[-1, -2], K[-1, -1] = 2, -2
    K = K / dy**2
    # B's polar rows remain zero: no first derivative at the poles.
    L = np.eye(npoints) - diffusivity * dt * K
    return lats, B, K, L

def snowball(initial, diffusivity=100, emissivity=1, gamma=1,
             dt_years=10, years=20000, spherical=True,
             radiation=True, albedo_mode="constant"):
    """Advance the zonal climate model to its final time.

    Inputs:
        initial: latitude-cell temperatures in degrees C (1D array)
        diffusivity: thermal diffusivity (m^2/s)
        emissivity: infrared emissivity, 0 through 1
        gamma: multiplier on latitude-dependent insolation
        dt_years: time step in years
        years: total simulated years (must be divisible by dt_years)
        spherical: include area-gradient correction
        radiation: include solar gain and longwave loss
        albedo_mode: 'constant', 'dynamic', or 'ice'
    Outputs:
        lats: cell-center latitudes from South Pole, degrees
        Temp: final temperature in each cell (degrees C)
    """
    Temp = np.array(initial, dtype=float, copy=True)
    if Temp.ndim != 1 or len(Temp) < 3 or not np.all(np.isfinite(Temp)):
        raise ValueError("Initial temperatures must be a finite 1D array of length >= 3")
    if not 0 <= emissivity <= 1 or gamma < 0 or years < 0:
        raise ValueError("Invalid emissivity, gamma, or years")
    if albedo_mode not in ("constant", "dynamic", "ice"):
        raise ValueError("Choose constant, dynamic, or ice albedo")
    steps = round(years / dt_years)
    if not np.isclose(steps * dt_years, years):
        raise ValueError("years must be a multiple of dt_years")

    lats, B, K, L = build_matrices(len(Temp), diffusivity, dt_years)
    dt = dt_years * seconds_year
    # Calculate the inverse once, not thousands of times in the loop.
    L_inv = np.linalg.inv(L)
    area = np.sin(np.deg2rad(lats))  # Spherical area, common factors cancel
    solar = gamma * insolation(S0, lats)

    for step in range(steps):
        # Implicit diffusion at the new time step.
        new_Temp = L_inv @ Temp

        # Explicit spherical correction, as illustrated in the lab equation.
        if spherical:
            new_Temp += diffusivity * dt * (B @ Temp) * (B @ area) / area

        # Explicit solar/infrared forcing at the current time step.
        if radiation:
            if albedo_mode == "dynamic":
                albedo = np.where(Temp <= freezing_temp, albedo_ice, albedo_ground)
            elif albedo_mode == "ice":
                albedo = np.full(len(Temp), albedo_ice)
            else:
                albedo = np.full(len(Temp), albedo_ground)
            kelvin = Temp + 273.15
            forcing = solar * (1 - albedo) - emissivity * sigma * kelvin**4
            new_Temp += dt * forcing / (rho * C * dz)

        Temp = new_Temp
        if not np.all(np.isfinite(Temp)):
            raise ArithmeticError("Nonfinite temperatures; reduce time step")
    return lats, Temp


def global_average(Temp, lats):
    """Area-weighted mean temperature (deg C); inputs in deg C and degrees."""
    weights = np.sin(np.deg2rad(lats))
    return np.sum(Temp * weights) / np.sum(weights)


def validation_tests():
    """Run key numerical tests; raises AssertionError if a test fails."""
    lats, B, K, L = build_matrices(18, 100, 1)
    dy = R * np.deg2rad(10)
    # Check lecture's polar stencil coefficients.
    assert np.isclose(K[0, 0] * dy**2, -2)
    assert np.isclose(K[0, 1] * dy**2, 2)
    assert np.isclose(K[-1, -2] * dy**2, 2)
    assert np.allclose(B[[0, -1]], 0)
    # With no flux, a constant profile must have zero second derivative.
    assert np.allclose(K @ np.ones(18), 0, atol=1e-18)
    # No forcing: a constant 10 C Earth must stay at 10 C.
    _, final = snowball(np.full(18, 10.0), dt_years=1,
                        years=100, spherical=True, radiation=False)
    assert np.allclose(final, 10.0)
    # With zero diffusivity and radiation disabled, any profile is unchanged.
    initial = np.linspace(-40, 25, 18)
    _, final = snowball(initial, diffusivity=0,
                        dt_years=1, years=10, radiation=False)
    assert np.allclose(initial, final)
    print("Validation tests passed")


if __name__ == "__main__":
    validation_tests()
