#moon-2
import math
from datetime import datetime

def get_moon_position_precise(dt: datetime):
    """
    Calculates the more precise geocentric Cartesian coordinates (x, y, z)
    of the Moon for a given datetime object.

    This function uses a more detailed astronomical model, including
    more terms for the Moon's orbital elements. The output is in a
    geocentric equatorial reference frame.

    Args:
        dt (datetime): The date and time for which to calculate the position.

    Returns:
        tuple: A tuple (x, y, z) of the Moon's Cartesian coordinates in kilometers.
    """
    # === Step 1: Calculate Julian Day and Epoch Time ===
    year = dt.year
    month = dt.month
    day = dt.day + dt.hour / 24.0 + dt.minute / (24.0 * 60.0) + dt.second / (24.0 * 3600.0)

    if month <= 2:
        year -= 1
        month += 12

    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5

    # Time since J2000.0 epoch in Julian centuries
    t = (jd - 2451545.0) / 36525.0

    # === Step 2: More Precise Lunar Orbital Calculations (Simplified Ecliptic Coordinates) ===
    # Using more terms for a more accurate result.
    
    # Mean longitude of the Moon (degrees)
    L0 = 218.3164477 + 481267.88123421 * t - 0.00157864 * t**2 + t**3 / 189474.0 - t**4 / 189474000.0
    L0 = math.fmod(L0, 360)

    # Mean anomaly of the Moon (degrees)
    M = 134.9634114 + 477198.86763 * t + 0.008997 * t**2 + t**3 / 69699.0 - t**4 / 14712000.0
    M = math.fmod(M, 360)

    # Elongation of the Moon from the Sun (degrees)
    D = 297.8501921 + 445267.11152 * t - 0.00163004 * t**2 + t**3 / 545860.0 - t**4 / 153300000.0
    D = math.fmod(D, 360)

    # Mean anomaly of the Sun (degrees)
    M_sun = 357.5291092 + 35999.05029 * t - 0.0001536 * t**2 + t**3 / 24490000.0
    M_sun = math.fmod(M_sun, 360)

    # Longitude of the Moon's ascending node (degrees)
    F = 93.2720993 + 483202.01753 * t - 0.00368257 * t**2 + t**3 / 327270.0 + t**4 / 4300000.0
    F = math.fmod(F, 360)
    
    # Arguments in radians for trigonometric functions
    M_rad = math.radians(M)
    M_sun_rad = math.radians(M_sun)
    D_rad = math.radians(D)
    F_rad = math.radians(F)

    # Ecliptic longitude terms (degrees)
    ecliptic_longitude = L0 + (6.289 * math.sin(M_rad)) + (1.274 * math.sin(2 * D_rad - M_rad)) + \
                         (0.658 * math.sin(2 * D_rad)) + (0.214 * math.sin(2 * M_rad))
    ecliptic_longitude = math.fmod(ecliptic_longitude, 360)
    if ecliptic_longitude < 0:
        ecliptic_longitude += 360

    # Ecliptic latitude terms (degrees)
    ecliptic_latitude = (5.128 * math.sin(F_rad)) + (0.280 * math.sin(M_rad + F_rad))
    
    # Distance terms (kilometers)
    distance_km = 384400.0 * (1 - 0.0549 * math.cos(M_rad) - 0.00412 * math.cos(2*M_rad) - 0.00282 * math.cos(2*D_rad-M_rad))
    
    # === Step 3: Convert from Ecliptic to Cartesian Equatorial Coordinates ===
    lambda_rad = math.radians(ecliptic_longitude)
    beta_rad = math.radians(ecliptic_latitude)
    
    # Obliquity of the Ecliptic (tilt of the Earth's axis) in degrees
    epsilon_degrees = 23.439 - 0.013 * t
    epsilon_rad = math.radians(epsilon_degrees)

    # Calculate x, y, z in geocentric ecliptic coordinates
    x_ecliptic = distance_km * math.cos(beta_rad) * math.cos(lambda_rad)
    y_ecliptic = distance_km * math.cos(beta_rad) * math.sin(lambda_rad)
    z_ecliptic = distance_km * math.sin(beta_rad)

    # Convert from ecliptic to equatorial Cartesian coordinates using the obliquity
    x_eq = x_ecliptic
    y_eq = y_ecliptic * math.cos(epsilon_rad) - z_ecliptic * math.sin(epsilon_rad)
    z_eq = y_ecliptic * math.sin(epsilon_rad) + z_ecliptic * math.cos(epsilon_rad)

    return x_eq, y_eq, z_eq
