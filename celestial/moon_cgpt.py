# moon-chatGPT
import numpy as np
from math import floor

# -----------------------------
# Utilities
# -----------------------------
def jd_from_calendar(year, month, day, hour=0, minute=0, second=0.0):
    y = year
    m = month
    if m <= 2:
        y -= 1
        m += 12
    A = int(y/100)
    B = 2 - A + int(A/4)
    frac_day = (hour + (minute + second/60.0)/60.0)/24.0
    JD = int(365.25*(y + 4716)) + int(30.6001*(m + 1)) + day + B - 1524.5 + frac_day
    return JD

def centuries_since_J2000(JD):
    return (JD - 2451545.0)/36525.0

def wrap_deg(x):
    return x % 360.0

# -----------------------------
# Mean lunar element polynomials
# -----------------------------
def lunar_mean_elements(T):
    L = (218.3164477
         + 481267.88123421*T
         - 0.0015786*T**2
         + (1/538841.0)*T**3
         - (1/65194000.0)*T**4)

    pi_lon = (83.3532465
              + 4069.0137287*T
              - 0.0103200*T**2
              - (1/80053.0)*T**3
              + (1/18999000.0)*T**4)

    Omega = (125.0445550
             - 1934.1361849*T
             + 0.0020762*T**2
             + (1/467410.0)*T**3
             - (1/60616000.0)*T**4)

    return wrap_deg(L), wrap_deg(pi_lon), wrap_deg(Omega)

# -----------------------------
# Solve Kepler's equation
# -----------------------------
def solve_kepler(M, e, tol=1e-10, maxiter=50):
    M = np.radians(M)
    E = M if e < 0.8 else np.pi  # first guess
    for _ in range(maxiter):
        dE = (E - e*np.sin(E) - M) / (1 - e*np.cos(E))
        E -= dE
        if abs(dE) < tol:
            break
    return E

# -----------------------------
# Moon position in ecliptic coordinates with perturbations + orbital elements
# -----------------------------
#def moon_position_ecliptic(year, month, day, hour=0, minute=0, second=0.0):
def moon_orbital_elements(year, month, day, hour=0, minute=0, second=0.0):
    JD = jd_from_calendar(year, month, day, hour, minute, second)
    T  = centuries_since_J2000(JD)

    # Mean orbital elements
    L, pi_lon, Omega = lunar_mean_elements(T)
    i = 5.1453964   # inclination (deg)
    e = 0.0549      # eccentricity
    a = 384400.0    # km semi-major axis

    omega = wrap_deg(pi_lon - Omega)
    M = wrap_deg(L - pi_lon)

    # -----------------------------
    # Perturbation corrections (simplified ELP2000 truncation)
    # -----------------------------
    D = wrap_deg(L - 297.8501921 - 445267.1114034*T)
    Mm = M
    Ms = wrap_deg(357.5291092 + 35999.0502909*T)  # Sun's mean anomaly
    F  = wrap_deg(L - Omega)

    lon_corr = (-1.274 * np.sin(np.radians(Mm - 2*D))
                +0.658 * np.sin(np.radians(2*D))
                -0.186 * np.sin(np.radians(Ms))
                -0.059 * np.sin(np.radians(2*Mm - 2*D))
                -0.057 * np.sin(np.radians(Mm - 2*D + Ms))
                +0.053 * np.sin(np.radians(Mm + 2*D))
                +0.046 * np.sin(np.radians(2*D - Ms))
                +0.041 * np.sin(np.radians(Mm - Ms)))

    lat_corr = (-0.173 * np.sin(np.radians(F - 2*D))
                -0.055 * np.sin(np.radians(Mm - F - 2*D))
                -0.046 * np.sin(np.radians(Mm + F - 2*D))
                +0.033 * np.sin(np.radians(F + 2*D))
                +0.017 * np.sin(np.radians(2*Mm + F)))

    # Corrected orbital elements
    L_refined = L + lon_corr
    omega_refined = omega + lon_corr
    i_refined = i + lat_corr
    e_refined = e

    # Solve Kepler with refined elements
    M_refined = wrap_deg(L_refined - (omega_refined + Omega))
    E = solve_kepler(M_refined, e_refined)

    # True anomaly
    nu = 2*np.arctan2(np.sqrt(1+e_refined)*np.sin(E/2),
                      np.sqrt(1-e_refined)*np.cos(E/2))

    # Distance
    r = a*(1 - e_refined*np.cos(E))

    # Position in orbital plane
    x_orb = r * np.cos(nu)
    y_orb = r * np.sin(nu)
    z_orb = 0.0

    # Rotate into ecliptic frame
    cosO = np.cos(np.radians(Omega))
    sinO = np.sin(np.radians(Omega))
    cosi = np.cos(np.radians(i_refined))
    sini = np.sin(np.radians(i_refined))
    cosw = np.cos(np.radians(omega_refined))
    sinw = np.sin(np.radians(omega_refined))

    R = np.array([
        [cosO*cosw - sinO*sinw*cosi, -cosO*sinw - sinO*cosw*cosi, sinO*sini],
        [sinO*cosw + cosO*sinw*cosi, -sinO*sinw + cosO*cosw*cosi, -cosO*sini],
        [sinw*sini,                  cosw*sini,                  cosi]
    ])

    vec_orb = np.array([x_orb, y_orb, z_orb])
    vec_ecl = np.dot(R, vec_orb) #  @ vec_orb

    # -----------------------------
    # Epoch + Time of Periapsis
    # -----------------------------
    # Mean motion n (rad/day), using Kepler's 3rd law with mu (Earth+Moon GM)
    mu = 398600.4418  # km^3/s^2, Earth GM
    n = np.sqrt(mu / a**3) * 86400.0  # rad/day

    M_rad = np.radians(M_refined)
    Tp = JD - M_rad / n  # Julian date of periapsis passage

    return {
        "epochJD": JD,
        "x_km": vec_ecl[0],
        "y_km": vec_ecl[1],
        "z_km": vec_ecl[2],
        "distance_km": r,
        "Tp_Time_of_perihelion_passage_JD": Tp,
        "orbital_elements": {
	        "aphelion": a,
	        "EC_e": e_refined,
	        "IN_orbital_inclination": i_refined,
	        "OM_longitude_of_the_ascendingnode": Omega,
	        "longitude_of_perihelion": omega_refined,
	        "MA_mean_anomaly": M_refined,
	        "L_mean_longitude": L_refined,
	        "N_mean_motion": n
        }
    }

# -----------------------------
# Example
# -----------------------------
#if __name__ == "__main__":
#    pos = moon_position_ecliptic(2025, 8, 23, 0, 0, 0.0)
#    for k, v in pos.items():
#        if k != "orbital_elements":
#            print(f"{k:>20s}: {v}")
#    print("\nRefined Orbital Elements:")
#    for k, v in pos["orbital_elements"].items():
#        print(f"{k:>20s}: {v}")


"""
What's new:

    Perturbation corrections are added to longitude and latitude (simplified ELP terms).

    The function now also returns the refined orbital elements:

        a (semi-major axis, km)

        e (eccentricity)

        i (inclination, deg)

        Omega (longitude of ascending node, deg)

        omega (argument of perigee, deg)

        M (mean anomaly, deg)

        L (mean longitude, deg, corrected)
"""


# Explanation:
"""
1. JD

The Julian Day number for the given calendar date/time. Continuous day count used in 
astronomy, starting from January 1, 4713 BCE.
Example: 2460910.5 corresponds to 2025-08-23 00:00:00 UTC.

2. a_km

Semi-major axis of the Moon's mean orbit. Average Earth-Moon distance: 384,400 km. 
It's the "size" of the Moon's elliptical orbit.

3. e

Orbital eccentricity (dimensionless). Measures how "stretched" the ellipse is.
For the Moon: 0.0549, meaning the orbit is slightly elliptical but close to circular.

4. i_deg

Orbital inclination (degrees). Tilt of the Moon's orbital plane relative to the 
ecliptic plane. Around 5.15 deg - this is why eclipses don't happen every month (the 
orbit is tilted relative to Earth's orbit around the Sun).

5. Omega_deg

Longitude of the ascending node (degrees). Angle along the ecliptic from the vernal 
equinox to the point where the Moon crosses the ecliptic northward. Defines the 
orientation of the orbit plane in space.

6. omega_deg

Argument of perigee (degrees). Angle measured in the Moon's orbital plane, from the 
ascending node to the perigee (closest point to Earth). Defines where the "closest 
approach" happens within the orbit.

7. M_deg

Mean anomaly (degrees). An angular measure of where the Moon is along its orbit, 
assuming it moves at uniform speed. Related to the time since perigee passage.
From M, you can calculate the true anomaly (actual position along the ellipse).

8. Tp_JD

Julian Day of the last perigee passage before the given time. Found from:

Tp = t - (M/n)

where 
M = mean anomaly and 
n = mean motion.

9. Tp_calendar

The same perigee passage time, but converted into a human-readable Gregorian 
date and time:
{"year": ..., "month": ..., "day": ..., "hour": ..., "minute": ..., "second": ...}

"""

# -----------------------------
# Example usage
# -----------------------------
#if __name__ == "__main__":
#    # Example: 2025-08-23 00:00:00 UTC
#    elems = moon_orbital_elements(2025, 8, 23, 0, 0, 0.0)
#    for k, v in elems.items():
#        print(f"{k:>10s}: {v}")
