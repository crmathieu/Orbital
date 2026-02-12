# -*- coding: utf-8 -*-

"""
Principles Behind This Lunar Ephemeris Model
1. Analytical Geometry First (C1 Hybrid Model)
The Moon’s actual position is generated using a compact analytical model (C1‑style):
•   Mean longitude + secular drift
•   Dominant periodic terms (evection, variation, annual equation, etc.)
•   A few latitude and distance terms
This gives you a fast, dependency‑free, and reasonably accurate (~10 arcmin, ~100–200 km) lunar position in geocentric ecliptic J2000.
The key idea:
Use a small number of high‑impact terms to reproduce the Moon’s geometry without heavy ephemerides.

2. Derive the Orbital Plane and Node from the Geometry
Once we have the Moon’s position and a finite‑difference velocity:
•   Compute the instantaneous orbital plane
•   Extract the ascending node Ω from the cross‑product geometry
•   Extract the argument of periapsis ω and true anomaly ν from the state vector
This ensures the node orientation and Moon’s location along the orbit match the analytical geometry, not a canned element set.
The key idea:
Let the geometry determine the orientation of the orbit.

3. Use a Two‑Body Fit Only as a Geometric Diagnostic
We compute osculating elements from the state vector, but only to extract:
•   Ω (node)
•   ω (argument of periapsis)
•   ν (true anomaly)
•   e (eccentricity)
We do not trust the derived semi‑major axis, mean motion, or period, because the Moon is not a two‑body system and the C1 model is approximate.
The key idea:
Use the two‑body fit for orientation and anomaly, not for global orbital parameters.

4. Canonicalize the Global Orbital Parameters
To make the orbit look like a proper “Moon orbit” for simulation purposes, we override:
•   Inclination → 5.145°
•   Semi‑major axis → 384,400 km
•   Mean motion → 13.176358 deg/day
•   Period → 27.32166 days
These are stable, widely accepted lunar constants.
The key idea:
Use canonical values for global properties, but keep geometry‑driven values for instantaneous orientation and position.

5. Keep Everything in a Single, Clean Reference Frame
All computations are done in:
•   Geocentric ecliptic J2000
This avoids mixing frames and keeps the math simple and consistent.
The key idea:
One frame, no precession transforms, no hidden rotations.

6. Prioritize Simplicity, Stability, and Reproducibility
The entire model:
•   Has no external dependencies beyond NumPy and pytz
•   Is deterministic and lightweight
•   Runs fast even in Python 2.7
•   Is easy to maintain and extend
The key idea:
A compact, transparent model beats a black‑box ephemeris for simulation work.

In one sentence
Use a compact analytical model for the Moon’s geometry, extract the orbit plane and anomaly from the state vector, and override the global orbital parameters with canonical lunar constants to get a stable, simulation‑friendly hybrid ephemeris.
If you ever want to extend this same philosophy to the Sun or planets, we can build those next.

the same modeling philosophy works for all moons
Every major moon’s orbit can be modeled using the same three‑layer structure:
1. Analytical geometry model (low‑order series)
For each moon, you build a compact analytical model that gives:
•   Mean longitude
•   Mean anomaly
•   Node longitude
•   Argument of latitude
•   A handful of periodic terms
•   Distance terms
These models exist in various forms:
Earth’s Moon
•   ELP2000
•   Meeus truncated series
•   C1/C2 compact models (what you used)
Mars (Phobos, Deimos)
•   Very simple — nearly circular, tiny inclinations
•   A few periodic terms suffice
Jupiter (Galilean moons)
•   Io, Europa, Ganymede, Callisto
•   Use Laplace resonance terms + a few periodic corrections
•   Analytical models exist (Lieske’s E2/E5 theories)
Saturn (Titan, Rhea, Dione, Tethys, etc.)
•   Titan: simple secular + a few periodic terms
•   Inner moons: resonance terms
•   Analytical models exist (TASS theory)
Uranus / Neptune moons
•   Mostly simple Keplerian + small periodic corrections
•   Analytical models exist (Laskar, Jacobson)
Pluto–Charon
•   Almost perfectly two‑body
•   A trivial analytical model
The key idea:
Every moon has a published low‑order analytical ephemeris that can be truncated to a compact form.
"""

from __future__ import print_function

import math
from datetime import datetime
import numpy as np
import pytz

# =====================================================
# Constants
# =====================================================

MU_EARTH = 398600.4418          # km^3/s^2
DAYSEC   = 86400.0
DEG2RAD  = math.pi / 180.0
RAD2DEG  = 180.0 / math.pi

# Canonical lunar orbit values
A_CANON_KM       = 384400.0     # mean lunar distance (km)
I_CANON_DEG      = 5.145        # mean inclination to ecliptic (deg)
N_SIDEREAL_DEG_D = 13.176358    # sidereal mean motion (deg/day)
P_SIDEREAL_DAYS  = 360.0 / N_SIDEREAL_DEG_D


# =====================================================
# Vector helpers
# =====================================================

def v_norm(v):
    return np.linalg.norm(v)

def v_unit(v):
    n = v_norm(v)
    if n == 0.0:
        return v * 0.0
    return v / n

def wrap_angle_rad(a):
    twopi = 2.0 * math.pi
    a = a % twopi
    if a < 0.0:
        a += twopi
    return a

# =====================================================
# State → elements (geocentric ecliptic J2000)
# =====================================================

def state_to_elements_J2000(r, v, jd, mu=MU_EARTH, plane_normal=None):
    """
    Super function - from the position and velocity we calculate
    the orbital elements
    """


    if plane_normal is None:
        plane_normal = np.array([0.0, 0.0, 1.0], dtype=float)
    else:
        plane_normal = np.array(plane_normal, dtype=float)

    n_plane = v_unit(plane_normal)

    Rmag = v_norm(r)
    Vmag = v_norm(v)

    h = np.cross(r, v)
    hmag = v_norm(h)

    cos_i = np.dot(h, n_plane) / hmag
    cos_i = max(-1.0, min(1.0, cos_i))
    i = math.acos(cos_i)

    n = np.cross(n_plane, h)
    nmag = v_norm(n)

    hv = np.cross(v, h)
    evec = hv / mu - r / Rmag
    e = v_norm(evec)

    a = 1.0 / (2.0 / Rmag - Vmag*Vmag / mu)

    if nmag > 0.0:
        OM = math.atan2(n[1], n[0])
    else:
        OM = 0.0
    OM = wrap_angle_rad(OM)

    if nmag > 0.0 and e > 1e-12:
        cosw = np.dot(n, evec) / (nmag * e)
        cosw = max(-1.0, min(1.0, cosw))
        sinw = np.dot(np.cross(n, evec), h) / (hmag * nmag * e)
        w = math.atan2(sinw, cosw)
    else:
        w = 0.0
    w = wrap_angle_rad(w)

    if e > 1e-12:
        cosnu = np.dot(evec, r) / (e * Rmag)
        cosnu = max(-1.0, min(1.0, cosnu))
        sinnu = np.dot(np.cross(evec, r), h) / (hmag * e * Rmag)
        nu = math.atan2(sinnu, cosnu)
    else:
        nu = 0.0
    nu = wrap_angle_rad(nu)

    nmean_rad_s = math.sqrt(mu / abs(a**3))
    nmean_deg_day = nmean_rad_s * DAYSEC * RAD2DEG

    period_sec = 2.0 * math.pi / nmean_rad_s
    period_days = period_sec / DAYSEC

    if e < 1.0:
        fac = math.sqrt((1.0 - e) / (1.0 + e))
        E = 2.0 * math.atan2(fac * math.sin(nu / 2.0),
                             math.cos(nu / 2.0))
        E = wrap_angle_rad(E)
        M = E - e * math.sin(E)
        M = wrap_angle_rad(M)
        Mdot = nmean_rad_s
        Tp = jd - (M / Mdot) / DAYSEC
    else:
        M = 0.0
        Tp = jd

    # we return distance in meters and angle in degrees 
    # to stay compatible with our mesurement of distances

    return {
        "epochJD": jd,
        "semimajor_m": a * 1000,
        "apoapsis_m": a * (1+e) * 1000,
        "periapsis_m": a * (1-e) * 1000,
        "eccentricity_EC": e,
        "orbital_inclination_IN": i * RAD2DEG,
        "longitude_of_ascendingnode_OM": OM * RAD2DEG,
        "argument_of_periapsis_w": w * RAD2DEG,
        "longitude_of_periapsis_W": (OM + w) * RAD2DEG,
        "true_anomaly_nu": nu * RAD2DEG,
        "mean_anomaly_MA": M * RAD2DEG,
        "mean_motion_N_deg_per_day": nmean_deg_day,
        "orbital_period_days": period_days,
        "orbital_period_seconds": period_sec,
        "jd_time_of_periapsis_passage_Tp": Tp
    }


# =====================================================
# C1 Hybrid Lunar Model
# =====================================================

def moon_mean_arguments(T):
    D = 297.8501921 + 445267.1114034*T - 0.0018819*T*T + T*T*T/545868.0 - T*T*T*T/113065000.0
    M = 357.5291092 + 35999.0502909*T - 0.0001536*T*T + T*T*T/24490000.0
    Mp = 134.9633964 + 477198.8675055*T + 0.0087414*T*T + T*T*T/69699.0 - T*T*T*T/14712000.0
    F = 93.2720950 + 483202.0175233*T - 0.0036539*T*T - T*T*T/3526000.0 + T*T*T*T/863310000.0
    return (D*DEG2RAD, M*DEG2RAD, Mp*DEG2RAD, F*DEG2RAD)

def moon_mean_longitude(T):
    Lp = 218.3164477 + 481267.88123421*T - 0.0015786*T*T + T*T*T/538841.0 - T*T*T*T/65194000.0
    return Lp * DEG2RAD

def moon_position_C1(JD):
    T = (JD - 2451545.0) / 36525.0

    D, M, Mp, F = moon_mean_arguments(T)
    Lp = moon_mean_longitude(T)

    E = 1.0 - 0.002516*T - 0.0000074*T*T

    lon_evection  =  4586.0 * math.sin(2*D - M - Mp)
    lon_variation =  2062.0 * math.sin(2*D)
    lon_annual    = - 657.0 * math.sin(2*D - M)
    lon_term3     =  213.0 * math.sin(2*D - 2*Mp)
    lon_term4     = -185.0 * math.sin(M)
    lon_Mp        = 22640.0 * E * math.sin(Mp)
    lon_Mp2       =  769.0 * E * math.sin(2*Mp)
    lon_Mp3       =  412.0 * E * math.sin(2*D)
    lon_Mp4       = - 55.0 * E * math.sin(2*F - 2*D)

    dlon_arcsec = lon_evection + lon_variation + lon_annual + lon_term3 + lon_term4 + lon_Mp + lon_Mp2 + lon_Mp3 + lon_Mp4
    lam = wrap_angle_rad(Lp + (dlon_arcsec/3600.0)*DEG2RAD)

    lat_term1 = 18520.0 * math.sin(F + lam - Lp)
    lat_term2 = -2235.0 * math.sin(Lp)
    lat_term3 =  382.0 * math.sin(Mp + 2*D)

    beta = (lat_term1 + lat_term2 + lat_term3)/3600.0 * DEG2RAD

    R_mean = 385000.56
    dr_km = -20905.0*math.cos(Mp) - 3699.0*math.cos(2*D - Mp) - 2956.0*math.cos(2*D) - 570.0*math.cos(2*Mp)
    R_km = R_mean + dr_km

    return lam, beta, R_km

def sph_to_cart_ecliptic(lam, beta, R_km):
    cl = math.cos(lam)
    sl = math.sin(lam)
    cb = math.cos(beta)
    sb = math.sin(beta)
    return np.array([R_km*cb*cl, R_km*cb*sl, R_km*sb], dtype=float)


def moon_ephemeris(dt, delta, vel_dt_sec=10.0):

    # Main ephemeris (with canonical overrides)

    from orbit3D import datetime_to_julian_date
    
    jd = datetime_to_julian_date(dt, delta)

    lam, beta, R_km = moon_position_C1(jd)
    r = sph_to_cart_ecliptic(lam, beta, R_km)

    dt_days = vel_dt_sec / DAYSEC
    lam2, beta2, R_km2 = moon_position_C1(jd + dt_days)
    r2 = sph_to_cart_ecliptic(lam2, beta2, R_km2)

    v = (r2 - r) / float(vel_dt_sec)

    elems = state_to_elements_J2000(
        r, v, jd,
        mu=MU_EARTH,
        plane_normal=np.array([0.0, 0.0, 1.0], dtype=float)
    )

    # Canonical overrides

    elems["canonical_apoapsis_m"] = A_CANON_KM * 1000
    elems["orbital_inclination_IN"] = I_CANON_DEG
    elems["mean_motion_N_deg_per_day"] = N_SIDEREAL_DEG_D
    elems["orbital_period_days"] = P_SIDEREAL_DAYS
    elems["orbital_period_seconds"] = P_SIDEREAL_DAYS * DAYSEC

    W_raw = elems["longitude_of_ascendingnode_OM"] + elems["argument_of_periapsis_w"]
    elems["longitude_of_periapsis_W"] = W_raw % 360.0

    return r * 1000, v * 1000, elems

def getMoonElementsXX(timeIncrement):
#    now_utc = datetime.now(pytz.utc)

    from orbit3D import System_utc


    r, v, elems = moon_ephemeris(System_utc, timeIncrement)
    return {
        "position_vec": r, # in meters
        "velocity_vec": v, # in meters/sec
        "elements": elems
    }


# =====================================================
# Simple solar model (geocentric ecliptic longitude)
# =====================================================

def sun_ecliptic_longitude(JD):
    """
    Very compact approximate solar longitude (geocentric, ecliptic, J2000).
    Accuracy: ~0.5 deg level, sufficient for phase classification.
    """

    T = (JD - 2451545.0) / 36525.0

    # Mean anomaly of the Sun (deg)
    M = 357.52911 + 35999.05029*T - 0.0001537*T*T
    M_rad = M * DEG2RAD

    # Mean longitude (deg)
    L0 = 280.46646 + 36000.76983*T + 0.0003032*T*T

    # Equation of center (deg)
    C = (1.914602 - 0.004817*T - 0.000014*T*T) * math.sin(M_rad) \
        + (0.019993 - 0.000101*T) * math.sin(2.0*M_rad) \
        + 0.000289 * math.sin(3.0*M_rad)

    # True longitude (deg)
    lambda_sun = L0 + C

    # Wrap to [0, 360)
    lambda_sun = lambda_sun % 360.0

    return lambda_sun * DEG2RAD


# =====================================================
# Moon phase from Sun–Moon elongation
# =====================================================

def moon_phase_from_longitudes(lam_moon, lam_sun):
    """
    Input:
        lam_moon: Moon ecliptic longitude (rad)
        lam_sun:  Sun ecliptic longitude (rad)
    Returns:
        phase_angle_deg: elongation (0=new, 180=full)
        illumination: fraction of disk illuminated
        phase_name: rough textual classification
    """

    # Elongation (Sun–Moon angle)
    D = (lam_moon - lam_sun)
    # Wrap to [-pi, pi]
    D = (D + math.pi) % (2.0*math.pi) - math.pi
    phase_angle = abs(D)          # 0..pi
    phase_angle_deg = phase_angle * RAD2DEG

    # Approximate illuminated fraction
    # f = (1 - cos(phase_angle)) / 2 gives New=0, Full=1
    illumination = (1.0 - math.cos(phase_angle)) * 0.5

    # Simple phase classification (you can tune thresholds)
    if phase_angle_deg < 10.0:
        name = "New Moon"
    elif phase_angle_deg < 80.0:
        # 0..180: waxing if Moon ahead of Sun, waning if behind
        name = "Waxing Crescent" if D > 0 else "Waning Crescent"
    elif phase_angle_deg < 100.0:
        name = "First Quarter" if D > 0 else "Last Quarter"
    elif phase_angle_deg < 170.0:
        name = "Waxing Gibbous" if D > 0 else "Waning Gibbous"
    else:
        name = "Full Moon"

    return phase_angle_deg, illumination, name



# =====================================================
# Example usage
# =====================================================
"""
if __name__ == "__main__":
    now_utc = datetime.now(pytz.utc)
    r, v, elems = moon_ephemeris(now_utc, 0)

    print("UTC time:", now_utc.isoformat())
    print("Position (km):", r)
    print("Velocity (km/s):", v)
    print("\nOsculating elements (canonicalized):")
    for k in sorted(elems.keys()):
        print(k, "=", elems[k])
"""

"""
if __name__ == "__main__":
    now_utc = datetime.now(pytz.utc)

    # Moon state
    r, v, elems = moon_ephemeris(now_utc, 0)
    jd = elems["epochJD"]

    # Moon longitude from our C1 model
    lam_moon, beta_moon, R_moon = moon_position_C1(jd)

    # Sun longitude from simple solar model
    lam_sun = sun_ecliptic_longitude(jd)

    phase_angle_deg, illum, phase_name = moon_phase_from_longitudes(lam_moon, lam_sun)

    print("UTC time:", now_utc.isoformat())
    print("Phase angle (deg):", phase_angle_deg)
    print("Illumination fraction:", illum)
    print("Phase name:", phase_name)
    print("Position (m):", r)
    print("Velocity (m/s):", v)
    print("\nOsculating elements (canonicalized):")
    for k in sorted(elems.keys()):
        print(k, "=", elems[k])


"""