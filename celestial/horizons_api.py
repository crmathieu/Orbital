# celestial/horizons_api.py
# -*- coding: utf-8 -*-

"""
This API provides:
- Raw data as a blob of ascii character (horizons_request)
- state vector (R, V) 
- State vector to osculating elements conversion (RV_to_elements)

"""
from __future__ import division

import json
import urllib
import urllib2
import math

#from constants import AU
from constants import *

from time_helper import TimeH   # unified time object
import collections
import numpy as np 

HORIZONS_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"
#HORIZONS_URL = "https://ssd.jpl.nasa.gov/horizons_batch.cgi"


# ------------------------------------------------------------
# 1. Low-level Horizons request
# ------------------------------------------------------------
def horizons_request(params, jsonFormat=True):
    query = urllib.urlencode(params)
    url = HORIZONS_URL + "?" + query

    response = urllib2.urlopen(url, timeout=20)
    if jsonFormat == True:
        data = json.loads(response.read())
    else:
        data = response.read()

    #if "error" in data:
    #    raise RuntimeError("Horizons error: %s" % data["error"])

    return data

"""
Use of REF_PLANE and REF_SYSTEM in horizons params block

To get this frame...    REF_PLANE   REF_SYSTEM
J2000 Ecliptic          ECLIPTIC    ICRF    
CRF (J2000 Equatorial)  FRAME       ICRF    
Mars Equator (IAU)      FRAME       IAU_MARS

To get Mars-Centered Ecliptic (specifically the Mars-centric version of the J2000 Earth Ecliptic), 
use the same frame parameters but change the CENTER code.

The Parameters

    CENTER: '500@499' (Mars Center)

    REF_PLANE: 'ECLIPTIC'

    REF_SYSTEM: 'ICRF' (or 'J2000')
"""

# ------------------------------------------------------------
# 2. Fetch state vector (VECTORS) in planet ecliptic frame
# ------------------------------------------------------------

def _get_ephemeris(id, center, epoch_str):
    """
    High-level helper: return position and velocity vectors in SI units.
    Parameters
    ----------
    id : str
        Horizons COMMAND (NAIF ID or quoted name, e.g. "301" or "'Phobos'").
    center : str
        Horizons CENTER string (e.g. "500@399").
    epoch_str : str
        Epoch as a Horizons-compatible calendar string (e.g. "2000-01-01").

    Returns
    -------
    r_m : (x, y, z) in meters
    v_m_s : (vx, vy, vz) in meters/second
    """    
    from datetime import datetime, timedelta 

    # Detect whether epoch_str has a time or not
    fmt = "%Y-%m-%d %H:%M" if " " in epoch_str else "%Y-%m-%d"
    start_dt = datetime.strptime(epoch_str, fmt)

    # STOP_TIME must be later than START_TIME
    stop_dt = start_dt + timedelta(minutes=1)

    start = start_dt.strftime("%Y-%m-%d %H:%M")
    stop  = stop_dt.strftime("%Y-%m-%d %H:%M")

    params = {
        "format": "json",
        "COMMAND": id,
        "OBJ_DATA": "NO", 
        "MAKE_EPHEM": "YES",
        "EPHEM_TYPE": "VECTORS",
        "CENTER": center,
        "START_TIME": "'%s'" % start,  # Note the '%s' wrapping 
        "STOP_TIME": "'%s'" % stop,    # Note the '%s' wrapping        
        "STEP_SIZE": "1",              # Simple integer for steps
        "OUT_UNITS": "KM-S",
        "REF_PLANE": "ECLIPTIC",
        "REF_SYSTEM": "ICRF",          # Modern standard for J2000-ecliptic
        "VEC_CORR": "NONE",            # MANDATORY: Ensures geometric consistency
        "VEC_LABELS": "YES",
        "VEC_TABLE": "2",              # Specifically requests the state vector table
    }

    data = horizons_request(params)
    text = data["result"]

    lines = text.splitlines()

    # Find $$SOE
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "$$SOE":
            start = i
            break
    if start is None:
        print "Object_id: ", id
        print text
        return (None, None, None),(None, None, None), ERR_CANTFIND_BLOCKMARKER
        #raise RuntimeError("No $$SOE block in Horizons result")

    x = y = z = vx = vy = vz = None

    for line in lines[start+1:]:
        L = line.strip()

        # Robust X/Y/Z parsing
        if L.startswith("X"):
            # Normalize formatting
            L = L.replace("=", " ")
            tokens = L.split()

            # tokens: ["X", "1.23E+05", "Y", "-2.34E+04", "Z", "3.45E+03"]
            x = float(tokens[1])
            y = float(tokens[3])
            z = float(tokens[5])

        # Robust VX/VY/VZ parsing
        if L.startswith("VX"):
            L = L.replace("=", " ")
            tokens = L.split()

            # tokens: ["VX", "1.23E-01", "VY", "-4.56E-02", "VZ", "7.89E-03"]
            vx = float(tokens[1])
            vy = float(tokens[3])
            vz = float(tokens[5])

        if x is not None and vx is not None:
            break

    if x is None or vx is None:
        return (None, None, None),(None, None, None), ERR_CANTPARSE_STATEVECTOR
        #raise RuntimeError("Could not parse state vector")

    # Convert km → m, km/s → m/s

    return (x*1000.0, y*1000.0, z*1000.0), (vx*1000.0, vy*1000.0, vz*1000.0), ERR_NOERR



# ------------------------------------------------------------
# 2b. Public state-vector helper (preferred API)
# ------------------------------------------------------------

def get_state_vectors(object_id, center, epoch_str):
    # _get_ephemeris already returns SI units (meters, m/s)
    return _get_ephemeris(object_id, center, epoch_str)

# ------------------------------------------------------------
# 2c. Public state-vector helper (preferred API)
# ------------------------------------------------------------

def get_equatorial_elements(object_id, center, planet_name, epoch_str):
    # _get_ephemeris already returns SI units (meters, m/s)
    return _get_equatorial_elements(object_id, center, planet_name, epoch_str)

# ------------------------------------------------------------
# 2d. convert planet-centric ecliptic to CRF_J2000 ecliptic
# ------------------------------------------------------------

def rotate_body_ecl_to_sun_ecl(r, v, inc_deg, Omega_deg):
    """
    Rotate a state vector (r, v) from a planet-centric J2000 ecliptic frame
    into the Sun-centric J2000 ecliptic frame.

    Parameters:
        r, v       : 3-element numpy arrays (position in km, velocity in km/s)
        inc_deg    : orbital inclination of the central body (degrees)
        Omega_deg  : longitude of ascending node of the central body (degrees)

    Returns:
        r_sun, v_sun : rotated state vectors in Sun-centric J2000 ecliptic axes
                       (still planet-centric origin)
    """

    # Convert to radians
    inc  = np.radians(inc_deg)
    Omega = np.radians(Omega_deg)

    # Rotation about x-axis by +inc
    R_x = np.array([
        [1.0,       0.0,        0.0],
        [0.0,  np.cos(inc), -np.sin(inc)],
        [0.0,  np.sin(inc),  np.cos(inc)]
    ])

    # Rotation about z-axis by +Omega
    R_z = np.array([
        [ np.cos(Omega), -np.sin(Omega), 0.0],
        [ np.sin(Omega),  np.cos(Omega), 0.0],
        [ 0.0,            0.0,           1.0]
    ])

    # Combined rotation: R = R_z * R_x
    R = np.dot(R_z, R_x)

    # Apply rotation
    r_sun = np.dot(R, r)
    v_sun = np.dot(R, v)

    return r_sun, v_sun


# ------------------------------------------------------------
# 3. RV → Elements (TDB-aware, full dictionary)
# ------------------------------------------------------------

def RV_to_elements(r, v, mu, epochJD_tdb):
    """
    Convert state vectors (SI units) into a full Keplerian element set.

    Parameters
    ----------
    r : tuple (meters)
        Position vector (x, y, z) in meters.
    v : tuple (m/s)
        Velocity vector (vx, vy, vz) in meters/second.
    mu : float (m^3/s^2)
        Gravitational parameter GM in SI units.
    epochJD_tdb : float
        Epoch in Julian Date (TDB).

    Returns
    -------
    dict
        Horizons-style orbital element dictionary.
    """

    # 1. Magnitudes
    R = math.sqrt(r[0]**2 + r[1]**2 + r[2]**2)
    V = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

    # 2. Angular momentum vector h = r × v
    hx = r[1]*v[2] - r[2]*v[1]
    hy = r[2]*v[0] - r[0]*v[2]
    hz = r[0]*v[1] - r[1]*v[0]
    h = math.sqrt(hx*hx + hy*hy + hz*hz)

    # 3. Node vector n = k × h
    nx = -hy
    ny = hx
    n = math.sqrt(nx*nx + ny*ny)

    # 4. Eccentricity vector
    # Calculate the Flight Path Angle (should be near 0 for Deimos since 
    # the orbit is quasi circular)

    dot_product = r[0]*v[0] + r[1]*v[1] + r[2]*v[2]
    angle_rad = math.asin(dot_product / (R * V))
    #print "Flight Path Angle (degrees):", math.degrees(angle_rad)


    rv = r[0]*v[0] + r[1]*v[1] + r[2]*v[2]
    ex = (1.0/mu)*((V*V - mu/R)*r[0] - rv*v[0])
    ey = (1.0/mu)*((V*V - mu/R)*r[1] - rv*v[1])
    ez = (1.0/mu)*((V*V - mu/R)*r[2] - rv*v[2])
    e = math.sqrt(ex*ex + ey*ey + ez*ez)

    # 5. Semi-major axis (meters)
    energy = V*V/2.0 - mu/R
    a_m = -mu/(2.0*energy)

    # 6. Inclination
    inc = math.acos(hz/h)

    # 7. Longitude of ascending node Ω
    if n < 1e-12: # Case for equatorial orbit
        Omega = 0.0
    else:
        Omega = math.atan2(ny, nx) # Corrected from (nx, ny)
        if Omega < 0.0: Omega += 2.0*math.pi

    #Omega = math.atan2(ny, nx)

    # 8. Argument of periapsis ω
    if n < 1e-12:
        # For equatorial, omega is Longitude of Periapsis
        omega = math.atan2(ey, ex)
    else:
        cos_omega = (nx*ex + ny*ey + 0*ez) / (n * e)
        # Clamp cos_omega to [-1, 1] to avoid float precision errors with acos
        omega = math.acos(max(-1.0, min(1.0, cos_omega)))
        if ez < 0:
            omega = 2.0*math.pi - omega


    # 9. True anomaly ν
    nu = math.atan2(rv/(e*h), (1.0/e)*((h*h)/(mu*R) - 1.0))
    if nu < 0.0:
        nu += 2.0*math.pi

    # 10–12. Anomalies, mean motion, period
    E = None
    H = None
    M = None
    n_rad_per_sec = None
    n_rad_per_day = None
    Tp_JD = None

    tol = 1e-6

    if e < 1.0 - tol and a_m > 0.0:
        # Elliptical case

        E = 2.0*math.atan(math.sqrt((1.0-e)/(1.0+e)) * math.tan(nu/2.0))
        if E < 0.0:
            E += 2.0*math.pi

        M = E - e*math.sin(E)
        if M < 0.0:
            M += 2.0*math.pi

        n_rad_per_sec = math.sqrt(mu / (a_m*a_m*a_m))
        n_rad_per_day = n_rad_per_sec * 86400.0
        Tp_JD = epochJD_tdb - (M / n_rad_per_day)

    elif abs(e - 1.0) < tol:

        # Parabolic case (not supported)
        # You can implement Barker’s equation here if you ever need it.

        n_rad_per_sec = None
        n_rad_per_day = None
        Tp_JD = None
        M = None

    else:

        # Hyperbolic case (e > 1)
        H = 2.0 * math.atanh(math.sqrt((e-1.0)/(e+1.0)) * math.tan(nu/2.0))
        M = e*math.sinh(H) - H

        # No bound period / mean motion in the elliptic sense
        n_rad_per_sec = None
        n_rad_per_day = None
        Tp_JD = None

    # 13. Return Horizons-style dictionary

    if n_rad_per_day != 0.0 and n_rad_per_day != None:
        revolution_days = (2.0 * math.pi) / n_rad_per_day
    else:
        revolution_days = None # hyperbolic or parabolic trajectories

    return collections.OrderedDict([
        ("semi_major_m", a_m),
        ("eccentricity_EC", e),
        ("orbital_inclination_IN", math.degrees(inc)),
        ("longitude_of_ascendingnode_OM", math.degrees(Omega)),
        ("argument_of_periapsis_w", math.degrees(omega)),
        ("longitude_of_periapsis_W", math.degrees(Omega + omega)),
        ("true_anomaly_nu", math.degrees(nu)),
        ("eccentric_anomaly_E", math.degrees(E) if E is not None else None),
        ("mean_anomaly_MA", math.degrees(M) if M is not None else None),
        ("mean_motion_rad_day", n_rad_per_day),
        ("mean_motion_N", math.degrees(n_rad_per_day) if n_rad_per_day is not None else None),
        ("revolution_PR", revolution_days),
        ("distance_to_periapsis_m", a_m * (1.0 - e)),
        ("aphelion_m", a_m * (1.0 + e)),
        ("jd_time_of_periapsis_passage_Tp", Tp_JD),
        ("epochJD", epochJD_tdb)
    ])



# ------------------------------------------------------------
# 3b. Public elements helper (preferred API)
# ------------------------------------------------------------
def elements_from_state(r, v, mu, epochJD_tdb):
    """
    High-level helper: convert state vectors to a full Keplerian element set.

    Parameters
    ----------
    r : tuple
        Position vector (x, y, z) in AU.
    v : tuple
        Velocity vector (vx, vy, vz) in AU/day.
    mu : float
        Gravitational parameter (GM) in AU^3/day^2 (consistent with r, v units).
    epochJD_tdb : float
        Epoch in Julian Date (TDB).

    Returns
    -------
    dict
        Dictionary with semi-major axis, eccentricity, angles, anomalies,
        mean motion, periapsis distance, aphelion, Tp, and epochJD.
    """
    return RV_to_elements(r, v, mu, epochJD_tdb)


# ------------------------------------------------------------
# 4. RV → Empty Elements (mostly for the edge case of the sun)
# ------------------------------------------------------------

def make_empty_elements_block():
    return collections.OrderedDict([
    ("semi_major_m", 0.0),
    ("eccentricity_EC", 0.0),
    ("orbital_inclination_IN", 0.0),
    ("longitude_of_ascendingnode_OM", 0.0),
    ("argument_of_periapsis_w", 0.0),
    ("longitude_of_periapsis_W", 0.0),
    ("true_anomaly_nu", 0.0),
    ("eccentric_anomaly_E", None),
    ("mean_anomaly_MA", None),
    ("mean_motion_rad_day", 0.0),
    ("mean_motion_N", 0.0),
    ("revolution_PR", 0.0),
    ("distance_to_periapsis_m", 0.0),
    ("aphelion_m", 0.0),
    ("jd_time_of_periapsis_passage_Tp", 0.0),
    ("epochJD", J2000_EPOCH)
])


