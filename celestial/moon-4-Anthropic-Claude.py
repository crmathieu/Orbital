# Anthropic Claude
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Moon state & orbital elements in the geocentric ecliptic frame (J2000) - Python 2.7

Model:
- Two-body Keplerian with mean lunar element rates relative to Earth's center.
- Reference plane: Mean ecliptic of J2000.
- Outputs:
    * r_ecl (km), v_ecl (km/s) geocentric ecliptic Cartesian
    * classical orbital elements (a, e, i, Omega, omega, M) at the requested epoch

Accuracy:
- Educational/rough visualization quality only.
- Does not include lunar perturbation series; expect degree-level angular error.

Author: (you)
"""

from __future__ import division
import math
from datetime import datetime

# ----------------------------
# Utilities
# ----------------------------
def d2r(x): return x * math.pi / 180.0
def r2d(x): return x * 180.0 / math.pi
def wrap2pi(x):
    # wrap radians to [0, 2pi)
    twopi = 2.0 * math.pi
    x = math.fmod(x, twopi)
    if x < 0.0: x += twopi
    return x
def wrap360deg(x):
    x = x % 360.0
    if x < 0.0: x += 360.0
    return x

# ----------------------------
# Time: UTC -> Julian Day (TT corrections ignored for simplicity)
# ----------------------------
def julian_day(dt_utc):
    """Algorithm from Meeus; valid for Gregorian dates >= 1582-10-15."""
    y = dt_utc.year
    m = dt_utc.month
    D = dt_utc.day + (dt_utc.hour + (dt_utc.minute + dt_utc.second/60.0)/60.0)/24.0

    if m <= 2:
        y -= 1
        m += 12

    A = int(y/100)
    B = 2 - A + int(A/4)
    JD = int(365.25*(y + 4716)) + int(30.6001*(m + 1)) + D + B - 1524.5
    return JD

def centuries_since_j2000(JD):
    return (JD - 2451545.0) / 36525.0

# ----------------------------
# Kepler equation solver (elliptic)
# ----------------------------
def solve_kepler_E(M, e, tol=1e-12, itmax=50):
    """
    Solve E - e*sinE = M for E (radians). M wrapped to [0,2pi).
    Newton-Raphson with a Danby-style guard.
    """
    M = wrap2pi(M)
    # Initial guess: for small e, E ~ M; otherwise a better starter:
    if e < 0.8:
        E = M
    else:
        E = math.pi
    for _ in range(itmax):
        f = E - e*math.sin(E) - M
        fp = 1.0 - e*math.cos(E)
        dE = -f/fp
        E += dE
        if abs(dE) < tol:
            break
    return wrap2pi(E)

# ----------------------------
# Rotation helpers
# ----------------------------
def rot_z(vec, ang):
    c, s = math.cos(ang), math.sin(ang)
    x, y, z = vec
    return ( c*x - s*y, s*x + c*y, z )

def rot_x(vec, ang):
    c, s = math.cos(ang), math.sin(ang)
    x, y, z = vec
    return ( x, c*y - s*z, s*y + c*z )

# ----------------------------
# Elements <-> State conversions in ecliptic frame
# ----------------------------
MU_EARTH = 398600.4418  # km^3/s^2

def elements_to_state_ecliptic(a_km, e, inc_deg, raan_deg, argp_deg, M_deg, mu=MU_EARTH):
    """
    Classical elements (a,e,i,Omega,omega,M) -> r, v in the mean ecliptic of J2000.
    Angles in degrees, a in km.
    """
    i = d2r(inc_deg)
    Omega = d2r(raan_deg)
    omega = d2r(argp_deg)
    M = d2r(M_deg)

    # Solve Kepler for E
    E = solve_kepler_E(M, e)
    # True anomaly nu (v)
    sinv = (math.sqrt(1.0 - e*e) * math.sin(E)) / (1.0 - e*math.cos(E))
    cosv = (math.cos(E) - e) / (1.0 - e*math.cos(E))
    v = math.atan2(sinv, cosv)
    v = wrap2pi(v)

    # Distance and perifocal coordinates
    r_pf = a_km * (1.0 - e*math.cos(E))
    x_pf = r_pf * math.cos(v)
    y_pf = r_pf * math.sin(v)
    z_pf = 0.0

    # Perifocal velocity
    h = math.sqrt(mu * a_km * (1.0 - e*e))
    vx_pf = - (mu/h) * math.sin(v)
    vy_pf =   (mu/h) * (e + math.cos(v))
    vz_pf = 0.0

    # Rotate: perifocal -> ecliptic: Rz(Omega) * Rx(i) * Rz(omega)
    r_vec = (x_pf, y_pf, z_pf)
    v_vec = (vx_pf, vy_pf, vz_pf)

    r1 = rot_z(r_vec, omega)
    r2 = rot_x(r1, i)
    r3 = rot_z(r2, Omega)

    v1 = rot_z(v_vec, omega)
    v2 = rot_x(v1, i)
    v3 = rot_z(v2, Omega)

    return r3, v3

def state_to_elements_ecliptic(r, v, mu=MU_EARTH):
    """
    r, v in ecliptic J2000 -> classical elements (a,e,i,Omega,omega,M) with angles in degrees.
    """
    rx, ry, rz = r
    vx, vy, vz = v
    rmag = math.sqrt(rx*rx + ry*ry + rz*rz)
    vmag = math.sqrt(vx*vx + vy*vy + vz*vz)

    # Angular momentum
    hx = ry*vz - rz*vy
    hy = rz*vx - rx*vz
    hz = rx*vy - ry*vx
    hvec = (hx, hy, hz)
    h = math.sqrt(hx*hx + hy*hy + hz*hz)

    # Node vector (toward ecliptic ascending node)
    nx = -hz*0.0 - 0.0*hy   # cross(k,h)  where k=(0,0,1):  n = k * h = (-hy, hx, 0)
    ny =  hx
    nz =  0.0
    nx = -hy
    ny =  hx
    # magnitude
    n = math.sqrt(nx*nx + ny*ny)

    # Eccentricity vector
    rxv = ( (vy*hz - vz*hy), (vz*hx - vx*hz), (vx*hy - vy*hx) )
    evecx = (1.0/mu)*rxv[0] - rx/rmag
    evecy = (1.0/mu)*rxv[1] - ry/rmag
    evecz = (1.0/mu)*rxv[2] - rz/rmag
    e = math.sqrt(evecx*evecx + evecy*evecy + evecz*evecz)

    # Energy and a
    eps = vmag*vmag/2.0 - mu/rmag
    if abs(eps) > 0:
        a = -mu/(2.0*eps)
    else:
        a = float('inf')

    # Inclination
    inc = math.acos(hz / h)

    # RAAN Omega
    if n != 0.0:
        Omega = math.acos(nx / n)
        if ny < 0.0:
            Omega = 2.0*math.pi - Omega
    else:
        Omega = 0.0

    # Argument of perigee omega
    if n != 0.0 and e > 1e-12:
        cosw = (nx*evecx + ny*evecy + 0.0*evecz) / (n*e)
        cosw = max(-1.0, min(1.0, cosw))
        w = math.acos(cosw)
        # quadrant from e_z sign wrt node plane:
        if evecz < 0.0:
            w = 2.0*math.pi - w
    else:
        w = 0.0

    # True anomaly nu (v)
    if e > 1e-12:
        cosv = (evecx*rx + evecy*ry + evecz*rz) / (e*rmag)
        cosv = max(-1.0, min(1.0, cosv))
        v_true = math.acos(cosv)
        if (rx*vx + ry*vy + rz*vz) < 0.0:
            v_true = 2.0*math.pi - v_true
    else:
        v_true = 0.0

    # Mean anomaly M from E
    # tan(v/2) = sqrt((1+e)/(1-e)) * tan(E/2)  => E = 2*atan( ... )
    if e < 1.0 - 1e-12:
        # elliptic
        E = 2.0*math.atan2( math.tan(v_true/2.0), math.sqrt((1.0+e)/(1.0-e)) )
        E = wrap2pi(E)
        M = wrap2pi(E - e*math.sin(E))
    else:
        # fallback
        M = 0.0

    return (a, e, r2d(inc), r2d(Omega), r2d(w), r2d(M))

# ----------------------------
# Simplified mean-elements model for the Moon (about J2000)
# ----------------------------
def moon_mean_elements_approx(JD):
    """
    Returns a rough set of lunar orbital elements (a,e,i,Omega,omega,M) at JD,
    referenced to the mean ecliptic of J2000.

    WARNING: This is a simplified mean model. For precise work, replace with a
    proper lunar series to compute lambda, beta, delta, then derive elements/state.

    Sources (standard astro references; values are widely cited):
    - a  ~ 384400 km (mean)
    - e  ~ 0.0549 (mean)
    - i  ~ 5.145 deg (to ecliptic)
    - Omega0 ~ 125.044555 deg at J2000, Omega' ~ -0.0529539 deg/day (nodal regression)
    - omega0 ~ 318.0634   deg at J2000, omega' ~  0.1114041 deg/day (perigee advance)
    - M0 ~ 115.3654   deg at J2000, n  ~ 13.176358   deg/day (mean motion)

    These are approximate; small differences exist across sources.
    """
    # Epoch J2000.0
    JD0 = 2451545.0
    dt_days = JD - JD0

    a_km  = 384400.0
    e     = 0.0549
    inc   = 5.145

    # Rates (deg/day)
    Omega0 = 125.044555
    Omegad = -0.0529539

    omega0 = 318.0634
    omegad = 0.1114041

    M0     = 115.3654
    n      = 13.176358

    Omega = wrap360deg(Omega0 + Omegad * dt_days)
    omega = wrap360deg(omega0 + omegad * dt_days)
    M     = wrap360deg(M0     + n      * dt_days)

    return (a_km, e, inc, Omega, omega, M)

# ----------------------------
# Public API
# ----------------------------
def moon_state_geocentric_ecliptic(dt_utc):
    """
    Given a UTC datetime, compute geocentric ecliptic (J2000) r, v (km, km/s)
    along with the classical elements used, and the elements recovered from r,v.
    """
    JD = julian_day(dt_utc)
    elems = moon_mean_elements_approx(JD)   # (a,e,i,Omega,omega,M)
    r_ecl, v_ecl = elements_to_state_ecliptic(*elems)

    # also compute elements back from state for reference
    elems_from_rv = state_to_elements_ecliptic(r_ecl, v_ecl)

    out = {
        'datetime_utc': dt_utc.isoformat(),
        'JD': JD,
        'elements_used': {
            'a_km': elems[0], 'e': elems[1],
            'i_deg': elems[2], 'Omega_deg': elems[3],
            'omega_deg': elems[4], 'M_deg': elems[5],
            'frame': 'Geocentric mean ecliptic of J2000'
        },
        'r_ecliptic_km': {'x': r_ecl[0], 'y': r_ecl[1], 'z': r_ecl[2]},
        'v_ecliptic_km_s': {'x': v_ecl[0], 'y': v_ecl[1], 'z': v_ecl[2]},
        'elements_from_state': {
            'a_km': elems_from_rv[0], 'e': elems_from_rv[1],
            'i_deg': elems_from_rv[2], 'Omega_deg': elems_from_rv[3],
            'omega_deg': elems_from_rv[4], 'M_deg': elems_from_rv[5],
            'frame': 'Geocentric mean ecliptic of J2000'
        }
    }
    return out

# ----------------------------
# Example usage
# ----------------------------
if __name__ == '__main__':
    # Example: now (UTC)
    when_utc = datetime.utcnow()

    result = moon_state_geocentric_ecliptic(when_utc)

    print("UTC time:    %s" % result['datetime_utc'])
    print("Julian Day:  %.8f" % result['JD'])
    print("\nElements used (approx mean model, ecliptic J2000):")
    eu = result['elements_used']
    print("  a      = %.3f km" % eu['a_km'])
    print("  e      = %.6f" % eu['e'])
    print("  i      = %.6f deg" % eu['i_deg'])
    print("  Omega  = %.6f deg" % eu['Omega_deg'])
    print("  omega  = %.6f deg" % eu['omega_deg'])
    print("  M      = %.6f deg" % eu['M_deg'])

    r = result['r_ecliptic_km']
    v = result['v_ecliptic_km_s']
    print("\nGeocentric ecliptic state (J2000):")
    print("  r = [%.3f, %.3f, %.3f] km" % (r['x'], r['y'], r['z']))
    print("  v = [%.6f, %.6f, %.6f] km/s" % (v['x'], v['y'], v['z']))

    ef = result['elements_from_state']
    print("\nElements recovered from state (sanity check):")
    print("  a      = %.3f km" % ef['a_km'])
    print("  e      = %.6f" % ef['e'])
    print("  i      = %.6f deg" % ef['i_deg'])
    print("  Omega  = %.6f deg" % ef['Omega_deg'])
    print("  omega  = %.6f deg" % ef['omega_deg'])
    print("  M      = %.6f deg" % ef['M_deg'])
