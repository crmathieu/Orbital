# -*- coding: utf-8 -*-
# objects_loader.py

"""
This loader uses the horizons_api module to access horizons data

Minimal Horizons client for Python 2.7
Works for planets, moons, asteroids, comets, spacecraft.

Objects (asteroids, comets, dwarf planets, TNOs, etc.) fall into two categories:

Category 1 — Stable, long‑period objects:
    Ceres, Vesta, Makemake, Haumea, Eris, Sedna, etc.

    For these, the osculating elements at J2000 are perfectly valid and stable.
    Their orbital periods are decades to centuries.
    Their osculating elements barely change over short timescales.

Category 2 — Dynamic objects:
    NEOs, comets, short‑period asteroids, etc.

    For these, the osculating elements change significantly over months or years.
    Using J2000 would give you stale orbits.

So, 
    - If the object’s orbit evolves significantly → use epoch as “now” 
    - If the object’s orbit is stable → use J2000.

But you don’t want to manually classify objects.
So the simplest, most robust architecture is:   

Use “now” for all objects.
Why?
•   It matches what we already do for spacecraft and dynamic objects.
•   It ensures NEOs and comets are correct.
•   It doesn’t harm long‑period objects (Makemake, Eris, etc.).
•   It keeps the catalog consistent with our objects_loader’s purpose:
        “Give me the current osculating elements for all non‑moon objects.”

This is exactly what GMAT, Orekit, and STK do for dynamic catalogs. 


"""

import os
import json
import math
from datetime import datetime

from horizons_api import get_state_vectors, elements_from_state, make_empty_elements_block
from orbit3D import datetime_to_julian_date
from objects_resolver import OBJECTS
from planetary_constants import PLANET_CONSTANTS

from constants import *
import collections

# ------------------------------------------------------------
# Build a single object entry (nested schema)
# ------------------------------------------------------------
def build_object_entry(name, cfg, epoch_str_now, epochJD_now):
    """
    Build a single catalog entry for one object using the nested schema.
    """

    horizons_rec_id = cfg["horizons_rec_id"]
    horizons_id = cfg["horizons_id"]
    jpl_designation = cfg["jpl_designation"]
    iau_name = cfg["iau_name"]

        
    primary = cfg["orbiting"]
    center = cfg["center"]
    physical = cfg["physical"]
    GM_object = 0.0
    if physical["mass_kg"] != None:
        GM_object = physical["mass_kg"] * G_universal

    planet_info = PLANET_CONSTANTS.get(name)

    # Determine epoch to use based on end_date
    end_date = cfg.get("end_date")

    if end_date:
        # Clamp to end_date (or end_date - 1 day if you prefer)
        epoch_str = end_date + " 00:00"
        # Convert to JD
        dt = datetime.strptime(end_date, "%Y-%m-%d")
        epochJD = datetime_to_julian_date(dt)
    else:
        # Use the "now" epoch passed in
        epoch_str = epoch_str_now
        epochJD = epochJD_now


    # ------------------------------------------------------------
    # 1. Fetch state vectors from Horizons
    # ------------------------------------------------------------
    r_vec, v_vec, status = get_state_vectors(
        object_id=horizons_id,
        center=center,
        epoch_str=epoch_str
    )
    if status == ERR_CANTFIND_BLOCKMARKER:
        print "TRYING WITH HORIZONS_RECID: ", horizons_rec_id
        # try with a numeric ID instead of horizons_id
        r_vec, v_vec, status = get_state_vectors(
            object_id=horizons_rec_id,
            center=center,
            epoch_str=epoch_str
        )
        if status != ERR_NOERR:
            raise("Can't parse data for ", name)

    # ------------------------------------------------------------
    # 2. GM of central body (planet name is the key)
    # ------------------------------------------------------------
    if primary != None:
        GM_central = PLANET_CONSTANTS[primary]["GM"]
    else:
        GM_central = SUN_Mu

    # ------------------------------------------------------------
    # 3. Convert RV → orbital elements (using horizons_api helper)
    # ------------------------------------------------------------

    if name == "sun":
        elements = make_empty_elements_block()
    else:
        elements = elements_from_state(
                        r_vec, v_vec,
                        GM_central,
                        epochJD
                    )

    # ------------------------------------------------------------
    # 4. Orbital period (days)
    # ------------------------------------------------------------
    #n = elements["mean_motion_rad_day"]
    #if n is not None:
    #    revolution_PR = (2.0 * math.pi) / n
    #else:
    #    # hyperbolic or parabolic trajectories
    #    revolution_PR = None


    # ------------------------------------------------------------
    # 5. Build nested catalog entry
    # ------------------------------------------------------------

    if "texture" in physical:
        texture = physical["texture"]
    else: 
        texture = DEFAULT_TEXTURE

    planet_info = PLANET_CONSTANTS.get(name)
    if planet_info:
        PHYS = collections.OrderedDict([
            ("texture", texture),
            ("mass_kg", physical.get("mass_kg")),
            ("radius_m", physical.get("radius_m")),
            ("GM", GM_object),
            ("J2", planet_info.get("J2")),
            ("drift_coef", planet_info["drift_coef"])
        ])

        precession = planet_info["precession"]
        # Rotation block
        ROTATION = collections.OrderedDict([
            ("axial_tilt", physical.get("axial_tilt_deg")),
            # the rotation is sidereal but expressed in # of solar days
            ("rotation_period_solar_d", physical.get("rotation_period_in_solar_d")),
            ("pole_RA_deg", precession.get("pole_ra_deg")),                     # in degrees
            ("pole_RA_dot_deg_day", precession.get("pole_ra_rate_deg_day")),    # in degrees/day
            ("pole_DEC_deg", precession.get("pole_dec_deg")),
            ("pole_DEC_dot_deg_day", precession.get("pole_ra_rate_deg_day")),
            ("prime_meridian_deg", precession.get("prime_meridian_deg")),
            ("prime_meridian_dot_deg_day", precession.get("prime_meridian_rate_deg_day"))             
        ])

    else:
        if cfg["object_class"] == SPACECRAFT:
            texture = None
            
        PHYS = collections.OrderedDict([
            ("texture", texture),
            ("mass_kg", physical.get("mass_kg")),
            ("radius_m", physical.get("radius_m")),
            ("GM", GM_object)
        ])

        ROTATION = collections.OrderedDict([
            ("axial_tilt", physical.get("axial_tilt_deg")),
            # the rotation is sidereal but expressed in # of solar days
            ("rotation_period_solar_d", physical.get("rotation_period_in_solar_d")) 
        ])

    # output the entry


    entry = collections.OrderedDict([

        # identification
        ("id", collections.OrderedDict([
            ("name", name),
            ("iau_name", cfg["iau_name"]),
            ("jpl_designation", cfg["jpl_designation"]),
            ("horizons_id",  cfg["horizons_id"]),
            ("horizons_rec_id",  cfg["horizons_rec_id"]),
            ("object_class", cfg["object_class"]),
            ("orbiting", primary)
        ])),
        
        
        # Orbital Elements block
        ("elements", elements), # If 'elements' is a dict, it will be unordered inside
        
        # Rotation block
        ("rotation", ROTATION),
        
        # Physical block
        ("physical", PHYS),

        # State vector block
        ("state_vector", collections.OrderedDict([
            ("r", r_vec),
            ("v", v_vec),
            ("epochJD", elements["epochJD"])
        ]))

    ])


    # Add the one extra derived field
    #entry["elements"]["revolution_PR"] = revolution_PR

    return entry


# ------------------------------------------------------------
# Build full catalog (Horizons calls for all objects)
# ------------------------------------------------------------
def build_full_catalog():
    catalog = {}

    # Use "now" as epoch (UTC)
    epoch_dt_now = datetime.utcnow()
    epoch_str_now = epoch_dt_now.strftime("%Y-%m-%d %H:%M")
    epochJD_now = datetime_to_julian_date(epoch_dt_now)

    print("Building full objects catalog at epoch:", epoch_str_now)

    for name, cfg in OBJECTS.items():
        print("Fetching:", name)

        entry = build_object_entry(name, cfg, epoch_str_now, epochJD_now)

        if entry is None:
            print("Skipping", name)
            continue

        catalog[name.lower()] = entry

    return catalog


# ------------------------------------------------------------
# Load or build catalog with cache fallback
# ------------------------------------------------------------

CACHE_FILE = "objects_catalog.json"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(BASE_DIR, CACHE_FILE)

def load_objects_catalog():
    """
    Mirrors the moons_loader fallback logic:
    - If catalog exists → load it
    - If not → build it
    - Save updated catalog
    """

    # CASE 1 — catalog exists
    if os.path.exists(CATALOG_PATH):
        print("Loading existing objects catalog from disk...")
        with open(CATALOG_PATH, "r") as f:
            catalog = json.load(f)
        return catalog

    # CASE 2 — catalog does not exist
    print("Rebuilding full objects catalog...")
    catalog = build_full_catalog()

    with open(CATALOG_PATH, "w") as f:
        json.dump(catalog, f, indent=4)

    return catalog

