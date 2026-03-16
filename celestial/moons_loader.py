# -*- coding: utf-8 -*-

"""
moons_loader.py — Modern SI-native Horizons Moon Catalog Builder
This moons loader uses:
•   J2000 for all moons except Luna
•   “now” (current epoch) for Luna only
    because Luna is extremely sensitive to TT vs TDB and 
    you want fresh set of osculating elements.

This version:
- Uses ONLY the new horizons_api SI-native functions:
      get_state_vectors()
      elements_from_state()

- Doesn't try to parse for physical properties as the syntax they display is inconsistent
- Uses instead fallback physical properties for radius, mass, GM, rotation, axial tilt
- Computes J2 precession (rad/day → deg/day)
- Computes synchronous rotation
- Handles Luna using NOW (TT/TDB via TimeH)
- Handles all other moons using J2000
- Produces a clean SI-native catalog entry
- Supports subset loading via moons_list.txt
- Supports cache fallback
"""

import json
import math
import os

from horizons_api import get_state_vectors, elements_from_state, get_equatorial_elements
from time_helper import TimeH
from constants import *

import numpy as np 

from moons_resolver import (
    MOONS,
    
    #SYNCHRONOUS_MOONS,
    j2_precession_rates
)

from planetary_constants import PLANET_CONSTANTS


# ------------------------------------------------------------
# Load subset list (optional)
# ------------------------------------------------------------
def load_requested_moons(path="moons_list.txt"):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        names = [line.strip() for line in f if line.strip()]
    return set(names) if names else None



def build_moon_entry_equatorial(moon_name, cfg):
    import collections

    """
    Build a catalog entry for a single moon using:
      - SI-native Horizons state vectors
      - SI-native orbital elements
      - fallback physical properties
      - J2 precession
      - synchronous rotation logic
    """
    Id = cfg["Id"]
    Physical = cfg["physical"]
    Rotation = cfg["rotation"]

    planet = Id["orbiting"]
    command = Id["horizons_id"]
    center = Id["center"]

    # --------------------------------------------------------
    # 1. Determine epoch
    # --------------------------------------------------------
    if moon_name == "moon":
        # Luna uses NOW (TT/TDB via TimeH)
        t = TimeH()
        epoch_str = t.to_horizons_timestamp()
        epochJD = t.jd_tdb

    else:
        # All other moons use J2000
        epoch_str = "2000-01-01"
        epochJD = J2000_EPOCH

    # --------------------------------------------------------
    # 2. Fetch state vectors (SI units)
    # --------------------------------------------------------
#    r_planet, v_planet, status = get_state_vectors(command, center, epoch_str)
    elements = get_equatorial_elements(command, center, planet, epoch_str)
    if r_planet is None:
        print("ERROR: No state vectors for {}, skipping".format(moon_name))
        return None

    # ----------------------------------------------------------------
    # 2b. Convert from planet-centric ecliptic to sun-centric ecliptic
    # ----------------------------------------------------------------
    #inc_deg = PLANET_CONSTANTS[planet]["orbital_plane"]["inclination"]
    #Omega_deg = PLANET_CONSTANTS[planet]["orbital_plane"]["inclination"]
    #r_sun, v_sun = rotate_body_ecl_to_sun_ecl(r_planet, v_planet, inc_deg, Omega_deg)


    r_sun = r_planet
    v_sun = v_planet


    # --------------------------------------------------------
    # 3. Physical properties from fallback
    # --------------------------------------------------------
    #fb = FALLBACK_PROPERTIES.get(moon_name, {})
    #fb = MOONS[moon_name]["physical"]
    fb = Physical

    radius_m = fb.get("radius_m")
    #mass_kg = fb.get("mass_kg")
    mass_kg = fb["mass_kg"]

    GM_moon_m3_s2 = fb.get("GM", 0.0)
    rotation_days = fb.get("rotation_period_in_solar_d")
    axial_tilt_deg = fb.get("axial_tilt_deg", 0.0)

    # Convert radius to meters
    #radius_m = radius_km * 1000.0 if radius_km is not None else None

    # Convert GM to SI (m^3/s^2)
    #GM_moon = GM_moon_km3_s2 * 1e9 if GM_moon_km3_s2 is not None else 0.0
    GM_moon = GM_moon_m3_s2 if GM_moon_m3_s2 is not None else 0.0

    # --------------------------------------------------------
    # 4. Gravitational parameter μ = GM_planet + GM_moon (SI)
    # --------------------------------------------------------
    GM_planet_m3_s2 = PLANET_CONSTANTS[planet]["GM"]
    #mu = (GM_planet_km3_s2 * 1e9) + GM_moon  # m^3/s^2
    mu = GM_planet_m3_s2 + GM_moon  # m^3/s^2


    # --------------------------------------------------------
    # 5. Orbital elements (SI-native)
    # --------------------------------------------------------
    #elements = elements_from_state(r_sun, v_sun, mu, epochJD)

    # Extract needed values for J2 and revolution period
    a_m = elements["semi_major_m"]
    #if a_m < 0:
    #    print("Proteus center:", center)

    e = elements["eccentricity_EC"]
    inc_rad = math.radians(elements["orbital_inclination_IN"])

    # --------------------------------------------------------
    # 6. J2 precession (rad/day → deg/day)
    # --------------------------------------------------------
    #a_km = a_m / 1000.0
    #print "a_m=", a_m, ", e=", e,", planet=", planet
    Omega_dot_rad_day, omega_dot_rad_day = j2_precession_rates(
        a_m,
        e,
        inc_rad,
        planet
    )

    # --------------------------------------------------------
    # 7. Revolution period (days)
    # --------------------------------------------------------
    n_rad_day = elements["mean_motion_rad_day"]
    revolution_days = (2.0 * math.pi) / n_rad_day

    # --------------------------------------------------------
    # 8. Synchronous rotation logic
    # --------------------------------------------------------
    if Id.get("moon_class") == "SYNCHRONOUS":
        rotation_days = revolution_days

    if "texture" in Physical:
        texture = Physical["texture"]
    else: 
        texture = DEFAULT_TEXTURE

    # output the entry
    
    entry = collections.OrderedDict([

        # identification
        ("id", collections.OrderedDict([
            ("name", moon_name),
            ("iau_name", Id["iau_name"]),
            ("jpl_designation", Id["jpl_designation"]),
            ("horizons_id",  Id["horizons_id"]),
            ("horizons_rec_id",  Id["horizons_rec_id"]),
            ("object_class", Id["object_class"]),
            ("moon_class", Id["moon_class"]),
            ("orbiting", Id["orbiting"])
        ])),
        
        
        # Orbital Elements block
        ("elements", elements), # If 'elements' is a dict, it will be unordered inside
        
        # Rotation block
        ("rotation", collections.OrderedDict([
            ("axial_tilt", Physical.get("axial_tilt_deg")),
            # the rotation is sidereal but expressed in # of solar days
            ("rotation_period_solar_d", Physical.get("rotation_period_in_solar_d")),
            ("pole_RA_deg", Rotation.get("pole_ra")),                     # in degrees
            ("pole_DEC_deg", Rotation.get("pole_dec")),
            ("prime_meridian_deg", Rotation.get("prime_meridian"))

        ])),
        
        # Physical block
        ("physical", collections.OrderedDict([
            ("texture", texture),
            ("mass_kg", Physical.get("mass_kg")),
            ("radius_m", Physical.get("radius_m")),
            ("GM", GM_moon),
            ("Omega_dot_deg_day", Omega_dot_rad_day * 180.0 / math.pi),
            ("omega_dot_deg_day", omega_dot_rad_day * 180.0 / math.pi)

        ])),

       # State vector block
        ("state_vector", collections.OrderedDict([
            ("r", r_sun),
            ("v", v_sun),
            ("epochJD", elements["epochJD"])
        ]))

    ])

    return entry

# ------------------------------------------------------------
# Build a single moon entry
# ------------------------------------------------------------
def build_moon_entry_Ecliptic(moon_name, cfg):
    import collections

    """
    Build a catalog entry for a single moon using:
      - SI-native Horizons state vectors
      - SI-native orbital elements
      - fallback physical properties
      - J2 precession
      - synchronous rotation logic
    """
    Id = cfg["Id"]
    Physical = cfg["physical"]
    Rotation = cfg["rotation"]

    planet = Id["orbiting"]
    command = Id["horizons_id"]
    center = Id["center"]


    # --------------------------------------------------------
    # 1. Determine epoch
    # --------------------------------------------------------
    if moon_name == "moon":
        # Luna uses NOW (TT/TDB via TimeH)
        t = TimeH()
        epoch_str = t.to_horizons_timestamp()
        epochJD = t.jd_tdb

    else:
        # All other moons use J2000
        epoch_str = "2000-01-01"
        epochJD = J2000_EPOCH

    # --------------------------------------------------------
    # 2. Fetch state vectors (SI units)
    # --------------------------------------------------------
    r_planet, v_planet, status = get_state_vectors(command, center, epoch_str)
    if r_planet is None:
        print("ERROR: No state vectors for {}, skipping".format(moon_name))
        return None

    # ----------------------------------------------------------------
    # 2b. Convert from planet-centric ecliptic to sun-centric ecliptic
    # ----------------------------------------------------------------
    #inc_deg = PLANET_CONSTANTS[planet]["orbital_plane"]["inclination"]
    #Omega_deg = PLANET_CONSTANTS[planet]["orbital_plane"]["inclination"]
    #r_sun, v_sun = rotate_body_ecl_to_sun_ecl(r_planet, v_planet, inc_deg, Omega_deg)


    r_sun = r_planet
    v_sun = v_planet


    # --------------------------------------------------------
    # 3. Physical properties from fallback
    # --------------------------------------------------------
    #fb = FALLBACK_PROPERTIES.get(moon_name, {})
    #fb = MOONS[moon_name]["physical"]
    fb = Physical

    radius_m = Physical.get("radius_m")
    #mass_kg = fb.get("mass_kg")
    mass_kg = Physical["mass_kg"]

    GM_moon_m3_s2 = Physical.get("GM", 0.0)
    rotation_days = Physical.get("rotation_period_in_solar_d")
    axial_tilt_deg = Physical.get("axial_tilt_deg", 0.0)

    # Convert radius to meters
    #radius_m = radius_km * 1000.0 if radius_km is not None else None

    # Convert GM to SI (m^3/s^2)
    #GM_moon = GM_moon_km3_s2 * 1e9 if GM_moon_km3_s2 is not None else 0.0
    GM_moon = GM_moon_m3_s2 if GM_moon_m3_s2 is not None else 0.0

    # --------------------------------------------------------
    # 4. Gravitational parameter μ = GM_planet + GM_moon (SI)
    # --------------------------------------------------------
    GM_planet_m3_s2 = PLANET_CONSTANTS[planet]["GM"]
    #mu = (GM_planet_km3_s2 * 1e9) + GM_moon  # m^3/s^2
    mu = GM_planet_m3_s2 + GM_moon  # m^3/s^2


    # --------------------------------------------------------
    # 5. Orbital elements (SI-native)
    # --------------------------------------------------------
    elements = elements_from_state(r_sun, v_sun, mu, epochJD)

    # Extract needed values for J2 and revolution period
    a_m = elements["semi_major_m"]
    #if a_m < 0:
    #    print("Proteus center:", center)

    e = elements["eccentricity_EC"]
    inc_rad = math.radians(elements["orbital_inclination_IN"])

    # --------------------------------------------------------
    # 6. J2 precession (rad/day → deg/day)
    # --------------------------------------------------------
    #a_km = a_m / 1000.0
    #print "a_m=", a_m, ", e=", e,", planet=", planet
    Omega_dot_rad_day, omega_dot_rad_day = j2_precession_rates(
        a_m,
        e,
        inc_rad,
        planet
    )

    # --------------------------------------------------------
    # 7. Revolution period (days)
    # --------------------------------------------------------
    n_rad_day = elements["mean_motion_rad_day"]
    revolution_days = (2.0 * math.pi) / n_rad_day

    # --------------------------------------------------------
    # 8. Synchronous rotation logic
    # --------------------------------------------------------
    if Id.get("moon_class") == "SYNCHRONOUS":
        rotation_days = revolution_days

    if "texture" in Physical:
        texture = Physical["texture"]
    else: 
        texture = DEFAULT_TEXTURE

    # output the entry
    
    entry = collections.OrderedDict([

        # identification
        ("id", collections.OrderedDict([
            ("name", moon_name),
            ("iau_name", Id["iau_name"]),
            ("jpl_designation", Id["jpl_designation"]),
            ("horizons_id",  Id["horizons_id"]),
            ("horizons_rec_id",  Id["horizons_rec_id"]),
            ("object_class", Id["object_class"]),
            ("moon_class", Id["moon_class"]),
            ("orbiting", Id["orbiting"])
        ])),
        
        
        # Orbital Elements block
        ("elements", elements), # If 'elements' is a dict, it will be unordered inside
        
        # Rotation block
        ("rotation", collections.OrderedDict([
            ("axial_tilt", Physical.get("axial_tilt_deg")),
            # the rotation is sidereal but expressed in # of solar days
            ("rotation_period_solar_d", Physical.get("rotation_period_in_solar_d")),
            ("pole_RA_deg", Rotation.get("pole_ra")),                     # in degrees
            ("pole_DEC_deg", Rotation.get("pole_dec")),
            ("prime_meridian_deg", Rotation.get("prime_meridian"))

        ])),
        
        # Physical block
        ("physical", collections.OrderedDict([
            ("texture", texture),
            ("mass_kg", Physical.get("mass_kg")),
            ("radius_m", Physical.get("radius_m")),
            ("GM", GM_moon),
            ("Omega_dot_deg_day", Omega_dot_rad_day * 180.0 / math.pi),
            ("omega_dot_deg_day", omega_dot_rad_day * 180.0 / math.pi)

        ])),

       # State vector block
        ("state_vector", collections.OrderedDict([
            ("r", r_sun),
            ("v", v_sun),
            ("epochJD", elements["epochJD"])
        ]))

    ])

    return entry


# --------------------------------------------------------------
# Helper that takes care of serializing json before file dumping
# --------------------------------------------------------------

def to_serializable(x):
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, dict):
        return {k: to_serializable(v) for k, v in x.iteritems()}
    if isinstance(x, (list, tuple)):
        return [to_serializable(v) for v in x]
    return x

# ------------------------------------------------------------
# Build full catalog
# ------------------------------------------------------------

def build_full_catalog():
    catalog = {}
    requested = load_requested_moons()

    """
    print("REQUESTED MOONS =", requested)
    ##############
    cfg = MOONS["deimos"]
    entry = build_moon_entry("deimos", cfg)
    ##############
    exit()
    """

    if False:
        print "TEST TEST TEST "

        """
         X =-1.921010950537068E+04 Y = 3.628376001633492E+03 Z = 1.297071778297925E+04
         VX=-4.637998704622034E-01 VY=-1.220877800089562E+00 VZ=-3.459024989304397E-01

        """
        Mu = PLANET_CONSTANTS['mars']["GM"] + 96150.0
        print "Mu = ", Mu
        r = 1000 * np.array([-1.921010950537068E+04, 3.628376001633492E+03, 1.297071778297925E+04])
        v = 1000 * np.array([-4.637998704622034E-01, -1.220877800089562E+00, 3.459024989304397E-01])
        
        elements_from_state(r, v, Mu, J2000_EPOCH)
        exit()
        ########################


    for moon_name, cfg in MOONS.items():

        if requested is not None and moon_name not in requested:
            continue

        print("Fetching:", moon_name)
        entry = build_moon_entry_Ecliptic(moon_name, cfg)

        if entry is None:
            print("Skipping", moon_name)
            continue

        catalog[moon_name.lower()] = entry #to_serializable(entry)

    return catalog



# ------------------------------------------------------------
# Load or build catalog with cache fallback
# ------------------------------------------------------------

CACHE_FILE = "moons_catalog.json"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(BASE_DIR, CACHE_FILE)

def load_moon_catalog():
    # CASE 1 — catalog exists
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, "r") as f:
            catalog = json.load(f)

        print "Loading fresh osculating elements for LUNA only ..."
        # Refresh Luna only
        luna = build_moon_entry_Ecliptic("moon", MOONS["moon"])

        catalog["Moon"] = luna
        return catalog
    else:
        # CASE 2 — catalog does not exist
        print "Rebuilding Full moon catalog ..."
        catalog = build_full_catalog()  # Horizons calls for all moons

    with open(CATALOG_PATH, "w") as f:
        json.dump(catalog, f, indent=4)

    return catalog

