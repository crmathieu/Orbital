#moon-1

import numpy as np

def moon_position_cartesian(T):
    """
    Calculate the geocentric position of the Moon in Cartesian coordinates (equatorial frame),
    taking into account the obliquity of the ecliptic.

    Parameters:
    T : float
        Julian centuries since J2000.0

    Returns:
    (xe, ye, ze) : tuple of floats
        Cartesian coordinates of the Moon in the geocentric equatorial frame (in Earth radii)
    """
    rads = np.pi / 180.0

    # Fundamental lunar arguments (simplified, from Jean Meeus)
    D = 297.8501921 + 445267.1114034*T - 0.0018819*T*T + T*T*T/545868 - T*T*T*T/113065000
    M = 357.5291092 + 35999.0502909*T - 0.0001536*T*T + T*T*T/24490000
    Mprime = 134.9633964 + 477198.8675055*T + 0.0087414*T*T + T*T*T/69699 - T*T*T*T/14712000
    F = 93.2720950 + 483202.0175233*T - 0.0036539*T*T - T*T*T/3526000 + T*T*T*T/863310000

    # Normalize angles
    D = np.mod(D, 360.0)
    M = np.mod(M, 360.0)
    Mprime = np.mod(Mprime, 360.0)
    F = np.mod(F, 360.0)

    D_r = D * rads
    M_r = M * rads
    Mprime_r = Mprime * rads
    F_r = F * rads

    # Ecliptic longitude and latitude (approximate formulas)
    lon = 218.3164591 + 481267.88134236*T
    lon += 6.289 * np.sin(Mprime_r)           # Evection
    lon += 1.274 * np.sin(2*D_r - Mprime_r)   # Variation
    lon += 0.658 * np.sin(2*D_r)              # Yearly equation
    lon += 0.214 * np.sin(2*Mprime_r)         # Correction term
    lon += 0.110 * np.sin(D_r)                # Correction term

    lat = 5.128 * np.sin(F_r)
    lat += 0.280 * np.sin(Mprime_r + F_r)
    lat += 0.277 * np.sin(Mprime_r - F_r)
    lat += 0.173 * np.sin(2*D_r - F_r)

    # Convert to radians
    lon_r = lon * rads
    lat_r = lat * rads

    # Cartesian coordinates in ecliptic frame
    x_ecl = np.cos(lat_r) * np.cos(lon_r)
    y_ecl = np.cos(lat_r) * np.sin(lon_r)
    z_ecl = np.sin(lat_r)

    # Obliquity of the ecliptic (J2000.0 approx)
    epsilon = 23.439291 * rads

    # Convert to equatorial frame (rotate by obliquity)
    xe = x_ecl
    ye = y_ecl * np.cos(epsilon) - z_ecl * np.sin(epsilon)
    ze = y_ecl * np.sin(epsilon) + z_ecl * np.cos(epsilon)

    return xe, ye, ze

# Example for J2000.0 (T=0)
moon_pos = moon_position_cartesian(0)
print("Cartesian geocentric coordinates (J2000.0):", moon_pos)