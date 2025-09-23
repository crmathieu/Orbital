#moon-3

# Import the necessary libraries. We are limited to numpy for this exercise.
import numpy as np
from datetime import datetime

# Gravitational parameter of the Earth (GM) in km^3/s^2.
# This value is essential for converting state vectors to orbital elements.
GM_EARTH = 3.986004418e5 

def calculate_moon_orbital_elements_simplified():
    """
    Calculates the Moon's approximate six orbital elements and its
    position and velocity vectors in ecliptic coordinates using only numpy.
    
    This function implements a simplified analytical model and then
    converts the resulting position and velocity vectors to orbital elements.
    
    Note: The results are approximate and do not account for all gravitational
    perturbations from the Sun, planets, and Earth's non-spherical shape.
    The coordinate transformation is also a simplified rotation.
    """
    try:
        # Get the current time in UTC
        current_utc_time = datetime.utcnow()
        
        # --- Step 1: Calculate the Julian Day (JD) and Julian Centuries (T) ---
        # JD is the standard time scale for astronomical calculations.
        # T is the number of Julian centuries from the J2000.0 epoch (2451545.0 JD).
        jd = 367 * current_utc_time.year - np.floor(7 * (current_utc_time.year + np.floor((current_utc_time.month + 9) / 12)) / 4) + np.floor(275 * current_utc_time.month / 9) + current_utc_time.day + 1721013.5 + (current_utc_time.hour + current_utc_time.minute / 60 + current_utc_time.second / 3600) / 24
        T = (jd - 2451545.0) / 36525.0
        
        print(f"Calculating approximate Moon's orbital elements for: {current_utc_time.isoformat()}Z\n")

        # --- Step 2: Calculate the simplified Mean Orbital Elements ---
        # These polynomial series give the mean position of the Moon.
        L0 = 218.3164477 + 481267.88123421 * T # Mean Longitude of the Moon
        M0 = 134.9629851 + 477198.8675338 * T  # Mean Anomaly of the Moon
        F0 = 93.2720993 + 483202.0175273 * T  # Argument of Latitude
        D0 = 297.8501921 + 445267.1115168 * T # Mean Elongation of the Moon
        
        # Convert degrees to radians for trigonometric functions.
        L0_rad, M0_rad, F0_rad, D0_rad = np.deg2rad([L0, M0, F0, D0])

        # --- Step 3: Compute simplified Geocentric Position and Velocity Vectors (x, y, z, vx, vy, vz) ---
        # These formulas approximate the state vectors in the geocentric equatorial frame.
        # Position vector components (in km)
        x = 384400 * np.cos(L0_rad)
        y = 384400 * np.sin(L0_rad) * np.cos(np.deg2rad(5.14)) # Use mean inclination
        z = 384400 * np.sin(L0_rad) * np.sin(np.deg2rad(5.14))

        # Velocity vector components (in km/s)
        # This is a simplified derivation for a circular orbit velocity.
        v_orbit = np.sqrt(GM_EARTH / 384400)
        vx = -v_orbit * np.sin(L0_rad)
        vy = v_orbit * np.cos(L0_rad) * np.cos(np.deg2rad(5.14))
        vz = v_orbit * np.cos(L0_rad) * np.sin(np.deg2rad(5.14))

        geocentric_position_vector = np.array([x, y, z])
        geocentric_velocity_vector = np.array([vx, vy, vz])
        
        # --- Step 4: Convert Geocentric Vectors to Ecliptic Vectors ---
        # We perform a rotation around the X-axis by the obliquity of the ecliptic.
        # This is a simplified method for a J2000 transformation.
        obliquity = np.deg2rad(23.439291) # Mean obliquity for J2000.0 epoch
        
        # Rotation matrix for a rotation around the X-axis
        R_x = np.array([
            [1, 0, 0],
            [0, np.cos(obliquity), np.sin(obliquity)],
            [0, -np.sin(obliquity), np.cos(obliquity)]
        ])
        
        # Apply the rotation to both position and velocity vectors.
        ecliptic_position_vector = np.dot(R_x, geocentric_position_vector)
        ecliptic_velocity_vector = np.dot(R_x, geocentric_velocity_vector)

        # --- Step 5: Convert Ecliptic State Vectors to Orbital Elements ---
        # Standard formulas to get orbital elements from position and velocity vectors.
        r = np.linalg.norm(ecliptic_position_vector)  # Magnitude of position vector (radius)
        v = np.linalg.norm(ecliptic_velocity_vector)  # Magnitude of velocity vector
        
        # Angular momentum vector (h = r x v)
        h_vector = np.cross(ecliptic_position_vector, ecliptic_velocity_vector)
        h = np.linalg.norm(h_vector)

        # Vector pointing to ascending node
        n_vector = np.cross(np.array([0, 0, 1]), h_vector)
        n = np.linalg.norm(n_vector)

        # Eccentricity vector (e = ((v^2 - GM/r)*r - (r.v)v)/GM)
        e_vector = ( (v**2 - GM_EARTH / r) * ecliptic_position_vector - np.dot(ecliptic_position_vector, ecliptic_velocity_vector) * ecliptic_velocity_vector ) / GM_EARTH
        eccentricity = np.linalg.norm(e_vector)

        # Semi-major axis (a = r^2 * v^2 / GM / (2GM/r - v^2))
        semi_major_axis = 1 / (2/r - v**2 / GM_EARTH)

        # Inclination (i)
        inclination = np.arccos(h_vector[2] / h)

        # Longitude of the Ascending Node (Ω)
        if n_vector[1] >= 0:
            ascending_node = np.arccos(n_vector[0] / n)
        else:
            ascending_node = 2 * np.pi - np.arccos(n_vector[0] / n)

        # Argument of Periapsis (ω)
        if e_vector[2] >= 0:
            argument_of_periapsis = np.arccos(np.dot(n_vector, e_vector) / (n * eccentricity))
        else:
            argument_of_periapsis = 2 * np.pi - np.arccos(np.dot(n_vector, e_vector) / (n * eccentricity))
            
        # True Anomaly (ν)
        if np.dot(ecliptic_position_vector, ecliptic_velocity_vector) >= 0:
            true_anomaly = np.arccos(np.dot(e_vector, ecliptic_position_vector) / (eccentricity * r))
        else:
            true_anomaly = 2 * np.pi - np.arccos(np.dot(e_vector, ecliptic_position_vector) / (eccentricity * r))
        
        # Print the calculated orbital elements.
        print("--- Six Orbital Elements (Ecliptic Coordinates) ---")
        print(f"1. Semi-major axis (a):   {semi_major_axis:.2f} km")
        print(f"2. Eccentricity (e):      {eccentricity:.6f}")
        print(f"3. Inclination (i):       {np.rad2deg(inclination):.4f}°")
        print(f"4. Ascending Node (Ω):    {np.rad2deg(ascending_node):.4f}°")
        print(f"5. Argument of Periapsis (ω): {np.rad2deg(argument_of_periapsis):.4f}°")
        print(f"6. True Anomaly (ν):      {np.rad2deg(true_anomaly):.4f}°")
        
        # --- NEW: Print the Ecliptic Position and Velocity Vectors ---
        print("\n--- Ecliptic Position and Velocity Vectors ---")
        print(f"Position (X, Y, Z):       [{ecliptic_position_vector[0]:.2f}, {ecliptic_position_vector[1]:.2f}, {ecliptic_position_vector[2]:.2f}] km")
        print(f"Velocity (Vx, Vy, Vz):    [{ecliptic_velocity_vector[0]:.6f}, {ecliptic_velocity_vector[1]:.6f}, {ecliptic_velocity_vector[2]:.6f}] km/s")


    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have numpy installed. You can install it with:")
        print("pip install numpy")

if __name__ == "__main__":
    calculate_moon_orbital_elements_simplified()
    