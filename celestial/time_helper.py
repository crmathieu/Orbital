# celestial/time_helper.py
# -*- coding: utf-8 -*-


import math
from datetime import datetime, timedelta
import pytz

"""
UTC — Civil Time (Human Time)
-----------------------------
UTC is the time you and I live in. It’s tied to:
•   Earth’s rotation
•   Leap seconds
•   Time zones (UTC is the base)
•   Clocks on your wall and in your OS

Key properties
•   Not uniform — Earth’s rotation slows down, so leap seconds are added irregularly.
•   Jumps — When a leap second occurs, UTC goes:
        23:59:59 → 23:59:60 → 00:00:00

•   Good for humans, terrible for physics.

UTC is NOT suitable for orbital mechanics
Because orbital propagation requires a smooth, uniform time scale.

TDB — Barycentric Dynamical Time (Physics Time)
-----------------------------------------------
TDB is a relativistic, uniform time scale used for:
- ephemerides
- spacecraft navigation
- Horizons state vectors
- SPICE kernels
- orbital propagation

Key properties
- Uniform — no leap seconds
- Defined at the Solar System barycenter
- Corrected for relativistic effects
- gravitational potential differences
- velocity of Earth around the Sun
- Runs slightly faster than TT/UTC
(~1.6 milliseconds per day)
TDB is the time scale Horizons uses internally
When you request VECTORS or ELEMENTS, Horizons computes them at a TDB epoch.

TT — Terrestrial Time
---------------------
TT (Terrestrial Time) is a uniform, non‑relativistic time scale used as the baseline for all Earth‑based astronomical calculations.
It is:
- smooth
- continuous
- free of leap seconds
- defined at the surface of the Earth
- the successor to the old Ephemeris Time (ET)
Think of TT as “the ideal clock on Earth” — the one you would use if you wanted perfect, uniform seconds that never jump or drift.

-> How TT relates to UTC
UTC is messy because of leap seconds.
TT is clean because it has none.
The relationship is:

    TT = UTC + ΔT

Where:
- ΔT = 32.184 seconds + (TAI − UTC)
- TAI − UTC is the accumulated leap seconds
- 32.184 seconds is a historical offset from Ephemeris Time
So TT is always ahead of UTC by about:
- ~69 seconds today (varies as leap seconds accumulate)
This is why TT is used for ephemerides:
you can’t propagate orbits across a time scale that jumps.

-> How TT relates to TDB
TDB (Barycentric Dynamical Time) is the time scale used for:
- Horizons internal computations
- SPICE kernels
- orbital propagation
- barycentric ephemerides
TDB is basically:

    TDB = TT + (small peridoci relativistic correction)

The correction is:
- periodic
- amplitude ≈ 1.6 milliseconds
- caused by Earth’s varying gravitational potential and velocity in its orbit
So:
- TT is the uniform Earth‑based time scale
- TDB is the uniform barycentric time scale

Both are smooth and leap‑second‑free.

Why this matters for this simulation

- Horizons VECTORS and ELEMENTS are computed at TDB
Even if you request them using a UTC timestamp.

- Your Julian Date function gives you UTC JD
Which is fine for cataloging, but not identical to TDB JD.

- If you want perfect alignment with Horizons
You eventually want:
    
    UTC → TT → TDB


TAI — International Atomic Time
-------------------------------
TAI (Temps Atomique International) is the master clock of the modern world.

TAI is one of those time scales that quietly sits underneath everything else, 
and once you understand it, the whole UTC → TAI → TT → TDB chain becomes 
beautifully clear. 

It is:
•   continuous
•   uniform
•   never has leap seconds
•   defined by an ensemble of atomic clocks around the world
•   the foundation for all precise timekeeping

Think of TAI as the perfect, uninterrupted atomic time scale.
It is the reference from which UTC and TT are derived.

-> How TAI relates to UTC
This is the part that matters most for your engine.
UTC is the civil time scale — the one your computer gives you.
But UTC has leap seconds, so it jumps occasionally.
TAI does not.
The relationship is:

    TAI = UTC + (TAI - UTC)

Where:
•   TAI − UTC is the accumulated leap seconds
•   As of 2026, TAI − UTC = 37 seconds
So:
•   UTC is “atomic time with leap seconds removed”
•   TAI is “pure atomic time with no jumps”

-> How TAI relates to TT
TT (Terrestrial Time) is defined as:

    TT = TAI + 32.184 seconds

That 32.184 seconds is a historical offset from Ephemeris Time.
So:
•   TAI → TT is a fixed offset
•   UTC → TT is leap‑seconds + 32.184 seconds
This is why TT is smooth and uniform.

-> How TAI relates to TDB
TDB (Barycentric Dynamical Time) is:
•   TT plus a small periodic relativistic correction
•   amplitude ≈ 1.6 milliseconds
•   caused by Earth’s varying gravitational potential and orbital velocity
So the chain is:

    UTC -> TAI -> TT -> TDB

Why TAI matters in this simulation
Because:
- UTC is not uniform (leap seconds)
- TAI is uniform (atomic)
- TT is uniform (atomic + fixed offset)
- TDB is uniform (relativistic dynamical time)

Horizons uses TDB internally.
Our Moon model uses TT.
Your computer gives you UTC.
TAI is the bridge that makes the conversions consistent.

SUMMARY TABLE

Time scales     Purpose                 Uniform?    Leap Seconds?   Defined At 
----------------------------------------------------------------------------------        
UTC             Civil Time              NO          YES             Earth Surface
----------------------------------------------------------------------------------
TAI             Atomic Ref. Time        YES         NO              Atomic clocks
----------------------------------------------------------------------------------
TT              Astronomical Earth-     YES         NO              Earth Surface
                based time
----------------------------------------------------------------------------------                
TDB             Barycentric Dynamical   YES         NO              Solar System
                time                                                barycenter
----------------------------------------------------------------------------------

Why you kept seeing TAI in this documentation
Because:
- TT is defined relative to TAI
- UTC is defined relative to TAI
- TDB is defined relative to TT
- Horizons uses TDB
- Our Moon model uses TT
- Your computer gives you UTC
So TAI is the anchor that ties all these together.
Even if you never explicitly compute TAI, it’s always in the background.

"""

# ------------------------------------------------------------
# 1. Julian Date from UTC datetime (+ optional fractional days)
# ------------------------------------------------------------
def julian_day(dt_utc, day_increment=0.0):
    """
    Convert a UTC datetime to Julian Date.
    Optionally add a fractional-day increment (float, in days).
    """

    if day_increment != 0.0:
        dt_utc = dt_utc + timedelta(days=day_increment)

    year = dt_utc.year
    month = dt_utc.month
    day = dt_utc.day + (dt_utc.hour +
                        (dt_utc.minute + dt_utc.second/60.0)/60.0)/24.0

    if month <= 2:
        year -= 1
        month += 12

    A = math.floor(year/100)
    B = 2 - A + math.floor(A/4)

    JD = (math.floor(365.25*(year + 4716)) +
          math.floor(30.6001*(month + 1)) +
          day + B - 1524.5)

    return JD


# ------------------------------------------------------------
# 2. UTC → TT
# ------------------------------------------------------------
def utc_to_tt(dt_utc):
    """
    Convert UTC datetime to TT datetime.
    TT = UTC + (TAI-UTC) + 32.184 seconds.
    """

    # As of 2026, TAI-UTC = 37 seconds.
    TAI_minus_UTC = 37.0

    offset = TAI_minus_UTC + 32.184  # seconds

    return dt_utc + timedelta(seconds=offset)


# ------------------------------------------------------------
# 3. TT → TDB (IAU 2006 approximation)
# ------------------------------------------------------------
def tt_to_tdb(jd_tt):
    """
    Convert TT Julian Date to TDB Julian Date.
    IAU 2006 approximation:
    TDB - TT = 0.001657*sin(g) + 0.000022*sin(2g)
    where g = 357.53° + 0.9856003° * (JD_TT - 2451545.0)
    """

    T = jd_tt - 2451545.0

    g = math.radians(357.53 + 0.9856003 * T)

    delta = 0.001657 * math.sin(g) + 0.000022 * math.sin(2*g)

    return jd_tt + delta / 86400.0


# ------------------------------------------------------------
# 4. UTC → TDB (full chain)
# ------------------------------------------------------------
def utc_to_tdb(dt_utc):
    """
    Convert UTC datetime to TDB Julian Date.
    Performs:
        UTC → TT → JD(TT) → TDB
    """

    dt_tt = utc_to_tt(dt_utc)
    jd_tt_val = julian_day(dt_tt)
    jd_tdb_val = tt_to_tdb(jd_tt_val)

    return jd_tdb_val


# ------------------------------------------------------------
# 5. Convenience wrappers
# ------------------------------------------------------------
def jd_tt(dt_utc):
    """Return TT Julian Date from UTC datetime."""
    return julian_day(utc_to_tt(dt_utc))


def jd_tdb(dt_utc):
    """Return TDB Julian Date from UTC datetime."""
    return utc_to_tdb(dt_utc)


# ------------------------------------------------------------
# 6. Unified Time Object
# ------------------------------------------------------------
class TimeH:
    """
    Unified time object storing:
    - UTC datetime
    - JD(UTC)
    - JD(TT)
    - JD(TDB)
    """

    def __init__(self, dt_utc=None):
        if dt_utc is None:
            dt_utc = datetime.now(pytz.utc)

        self.utc = dt_utc
        self.jd_utc = julian_day(dt_utc)

        self.tt = utc_to_tt(dt_utc)
        self.jd_tt = julian_day(self.tt)

        self.jd_tdb = tt_to_tdb(self.jd_tt)

    def to_horizons_timestamp(self):
        return self.utc.strftime("%Y-%m-%d %H:%M")

    def as_dict(self):
        return {
            "epoch_utc_iso": self.utc.isoformat(),
            "jd_utc": self.jd_utc,
            "jd_tt": self.jd_tt,
            "jd_tdb": self.jd_tdb
        }
