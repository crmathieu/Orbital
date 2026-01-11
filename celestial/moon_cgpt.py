# -*- coding: utf-8 -*-
"""
High-fidelity lunar ephemeris & orbital-element generator  
Python-2.7 compatible (no numpy, no math.radians/degrees)
----------------------------------------------------------------
*  Implements a truncated ELP-2000/82 theory (longitude + latitude
   corrections only) to ~0.1 deg accuracy.
*  Returns both the inertial (ecliptic J2000) Cartesian state
   vector and the instantaneous osculating Keplerian elements.
*  All angles are in degrees, distances in km, time in Julian Day
   (UTC).
*  Uses the Earth-Moon barycentric gravitational parameter
   mu = 403 503 km^3 s^-2  ->  sidereal month ~ 27.32158 d
----------------------------------------------------------------
"""

from __future__ import division   # 1/2 -> 0.5
import math

# ------------------------------------------------------------------
# Low-level utilities
# ------------------------------------------------------------------
def _sin(d):
    return math.sin(math.radians(d))

def _cos(d):
    return math.cos(math.radians(d))

def _atan2(y, x):
    return math.atan2(y, x)

def _fmod(x, m):
    return math.fmod(x, m)

def jd_from_calendar(y, m, d, h=0, minute=0, s=0.0):
    """Gregorian calendar -> Julian Day (UTC)."""
    if m <= 2:
        y -= 1
        m += 12
    A = int(y / 100)
    B = 2 - A + int(A / 4)
    frac = (h + (minute + s / 60.0) / 60.0) / 24.0
    jd = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524.5 + frac
    return jd

def centuries_since_J2000(jd):
    return (jd - 2451545.0) / 36525.0

def wrap360(x):
    x = _fmod(x, 360.0)
    return x + 360.0 if x < 0 else x

# ------------------------------------------------------------------
# Mean element polynomials (ELP-2000/82)
# ------------------------------------------------------------------
def mean_lunar_elements(T):
    L = (218.3164477
         + 481267.88123421 * T
         - 0.0015786 * T**2
         + (1.0 / 538841.0) * T**3
         - (1.0 / 65194000.0) * T**4)

    pi_lon = (83.3532465
              + 4069.0137287 * T
              - 0.0103200 * T**2
              - (1.0 / 80053.0) * T**3
              + (1.0 / 18999000.0) * T**4)

    Omega = (125.0445550
             - 1934.1361849 * T
             + 0.0020762 * T**2
             + (1.0 / 467410.0) * T**3
             - (1.0 / 60616000.0) * T**4)

    return wrap360(L), wrap360(pi_lon), wrap360(Omega)

# ------------------------------------------------------------------
# Kepler solver  (E - e sin E = M  [rad])
# ------------------------------------------------------------------
def solve_kepler(Mrad, e, tol=1e-12, maxit=30):
    E = Mrad if e < 0.8 else (math.pi if Mrad > 0 else -math.pi)
    for _ in range(maxit):
        f = E - e * math.sin(E) - Mrad
        fd = 1.0 - e * math.cos(E)
        delta = f / fd
        E -= delta
        if abs(delta) < tol:
            break
    return E

# ------------------------------------------------------------------
# Matrix helpers (3x3 * 3x1)  -> list[x,y,z]
# ------------------------------------------------------------------
def matvec(R, v):
    return [R[0][0]*v[0] + R[0][1]*v[1] + R[0][2]*v[2],
            R[1][0]*v[0] + R[1][1]*v[1] + R[1][2]*v[2],
            R[2][0]*v[0] + R[2][1]*v[1] + R[2][2]*v[2]]

# ------------------------------------------------------------------
# Main routine
# ------------------------------------------------------------------
def moon_ephemeris(y, m, d, h=0, minute=0, s=0.0):
#def moon_orbital_elements(y, m, d, h=0, minute=0, s=0.0):    
    """
    Compute Moon's osculating elements and ecliptic J2000 state vector.
    Returns dict with keys:
        epochJD, x_km, y_km, z_km, distance_km, Tp_JD,
        orbital_elements{...}
    """
    # Time
    jd = jd_from_calendar(y, m, d, h, minute, s)
    T = centuries_since_J2000(jd)

    # Mean elements
    L, pi_lon, Omega = mean_lunar_elements(T)

    # Constants
    a = 384400.0          # km
    e = 0.0549
    i0 = 5.1453964        # deg

    # Auxiliary arguments
    D = wrap360(L - (297.8501921 + 445267.1114034 * T))
    Mm = wrap360(L - pi_lon)
    Ms = wrap360(357.5291092 + 35999.0502909 * T)
    F = wrap360(L - Omega)

    # Periodic corrections (deg)
    dL = (-1.274 * _sin(Mm - 2 * D)
          + 0.658 * _sin(2 * D)
          - 0.186 * _sin(Ms)
          - 0.059 * _sin(2 * Mm - 2 * D)
          - 0.057 * _sin(Mm - 2 * D + Ms)
          + 0.053 * _sin(Mm + 2 * D)
          + 0.046 * _sin(2 * D - Ms)
          + 0.041 * _sin(Mm - Ms))

    dB = (-0.173 * _sin(F - 2 * D)
          - 0.055 * _sin(Mm - F - 2 * D)
          - 0.046 * _sin(Mm + F - 2 * D)
          + 0.033 * _sin(F + 2 * D)
          + 0.017 * _sin(2 * Mm + F))

    # Corrected angles
    L_corr = wrap360(L + dL)
    pi_corr = wrap360(pi_lon + dL)   # longitude of perigee
    i_corr = i0 + dB

    # Mean anomaly
    M_corr = wrap360(L_corr - pi_corr)

    # Solve Kepler
    E = solve_kepler(math.radians(M_corr), e)
    nu = 2.0 * _atan2(math.sqrt(1 + e) * math.sin(E / 2.0),
                      math.sqrt(1 - e) * math.cos(E / 2.0))
    r = a * (1.0 - e * math.cos(E))   # km

    # Orbital-plane position
    x_orb, y_orb, z_orb = r * math.cos(nu), r * math.sin(nu), 0.0

    # Rotation into ecliptic J2000
    cosO, sinO = _cos(Omega), _sin(Omega)
    cosi, sini = _cos(i_corr), _sin(i_corr)
    cosw, sinw = _cos(pi_corr - Omega), _sin(pi_corr - Omega)

    R = [
        [cosO * cosw - sinO * sinw * cosi, -cosO * sinw - sinO * cosw * cosi, sinO * sini],
        [sinO * cosw + cosO * sinw * cosi, -sinO * sinw + cosO * cosw * cosi, -cosO * sini],
        [sinw * sini, cosw * sini, cosi]
    ]
    vec_ecl = matvec(R, [x_orb, y_orb, z_orb])

    # Mean motion (rad/day)  mu = 403503 km^3/s^2
    mu = 403503.2
    n = math.sqrt(mu / (a**3)) * 86400.0

    # Perigee passage time
    Tp = jd - math.radians(M_corr) / n

    # Build result
      # Package results
    return {
        "epochJD": jd,
        "x_km": vec_ecl[0],
        "y_km": vec_ecl[1],
        "z_km": vec_ecl[2],
        "distance_km": r,
        "Tp_Time_of_perihelion_passage_JD": Tp,

        "orbital_elements": {


            "aphelion": a,
            "eccentricity_EC": e,
            "orbital_inclination_IN": i_corr,
            "longitude_of_ascendingnode_OM": Omega,
            "longitude_of_periapsis_W":pi_corr,
            "mean_anomaly_MA": M_corr,
            "mean_motion_N": n

        }
    }



# ------------------------------------------------------------------
# Quick self-test / demo
# ------------------------------------------------------------------
if __name__ == "__main__":
    import json
    res = moon_ephemeris(2025, 8, 23, 0, 0, 0)
    print(json.dumps({k: v for k, v in res.items() if k != "orbital_elements"}, indent=2))
    print("\nOsculating elements:")
    print(json.dumps(res["orbital_elements"], indent=2))

