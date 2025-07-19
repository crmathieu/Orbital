import math

def calculate_planet_pole_direction(inclination_deg, node_longitude_deg):
    """
    Calculates the direction of a planet's north pole in heliocentric ecliptic
    coordinates (J2000 epoch).

    In this coordinate system:
    - The Sun is at the origin (0, 0, 0).
    - The XY-plane is the J2000 Ecliptic plane.
    - The X-axis points towards the J2000 Vernal Equinox.
    - The Z-axis points towards the J2000 North Ecliptic Pole.

    Args:
        inclination_deg (float): The inclination (I) of the planet's equator
                                 to the J2000 ecliptic, in degrees.
        node_longitude_deg (float): The longitude (Omega) of the ascending node
                                    of the planet's equator on the J2000 ecliptic,
                                    in degrees.

    Returns:
        list: A 3-element list [X, Y, Z] representing the unit vector
              of the planet's north pole in heliocentric ecliptic coordinates.
    """
    # Convert angles from degrees to radians for trigonometric functions
    inclination_rad = math.radians(inclination_deg)
    node_longitude_rad = math.radians(node_longitude_deg)

    # Calculate the components of the pole vector
    # These formulas are derived from spherical trigonometry, where:
    # X = sin(I) * sin(Omega)
    # Y = -sin(I) * cos(Omega)  (Note the negative sign due to coordinate system conventions)
    # Z = cos(I)
    x_pole = math.sin(inclination_rad) * math.sin(node_longitude_rad)
    y_pole = -math.sin(inclination_rad) * math.cos(node_longitude_rad)
    z_pole = math.cos(inclination_rad)

    # Return the normalized vector (it should already be a unit vector if I is an angle)
    # We can optionally normalize it to ensure it's a unit vector, though it should be.
    magnitude = math.sqrt(x_pole**2 + y_pole**2 + z_pole**2)
    if magnitude == 0:
        return [0.0, 0.0, 0.0] # Handle the edge case of zero magnitude
    return [x_pole / magnitude, y_pole / magnitude, z_pole / magnitude]

# --- Example Usage ---

# Example 1: Earth's North Pole (approximate J2000 values)
# For Earth, the inclination of its equator to the ecliptic is its obliquity.
# The longitude of the ascending node is often taken as 0 for Earth's pole
# if we align the X-axis with the vernal equinox.
# In a simplified view, Earth's pole is mostly along the Z-axis of the ecliptic system
# when considering its obliquity.
earth_inclination = 23.43928 # Earth's obliquity to the ecliptic (J2000)
earth_node_longitude = 0.0   # For Earth, this is often set to 0 for simplicity in this context

print("--- Earth's North Pole Direction (approximate J2000) ---")
earth_pole_vector = calculate_planet_pole_direction(earth_inclination, earth_node_longitude)
print(f"Inclination (I): {earth_inclination}°")
print(f"Node Longitude (Omega): {earth_node_longitude}°")
print(f"Pole Vector [X, Y, Z]: [{earth_pole_vector[0]:.6f}, {earth_pole_vector[1]:.6f}, {earth_pole_vector[2]:.6f}]")
print("\nNote: For Earth, the pole is primarily along the Z-axis of the ecliptic system,")
print("which makes sense as the ecliptic's Z-axis is normal to Earth's orbital plane.")


# Example 2: Mars's North Pole (approximate J2000 values)
# These values are more illustrative as Mars's pole is significantly tilted
# and its ascending node is not aligned with the vernal equinox.
# (These values are simplified and would typically be time-dependent in real applications)
mars_inclination = 25.19 # Inclination of Mars's equator to the ecliptic (approx. J2000)
mars_node_longitude = 49.56 # Longitude of ascending node of Mars's equator on ecliptic (approx. J2000)

print("\n--- Mars's North Pole Direction (approximate J2000) ---")
mars_pole_vector = calculate_planet_pole_direction(mars_inclination, mars_node_longitude)
print(f"Inclination (I): {mars_inclination}°")
print(f"Node Longitude (Omega): {mars_node_longitude}°")
print(f"Pole Vector [X, Y, Z]: [{mars_pole_vector[0]:.6f}, {mars_pole_vector[1]:.6f}, {mars_pole_vector[2]:.6f}]")

# Example 3: A hypothetical planet with different orientation
hypothetical_inclination = 60.0
hypothetical_node_longitude = 180.0

print("\n--- Hypothetical Planet's North Pole Direction ---")
hypothetical_pole_vector = calculate_planet_pole_direction(hypothetical_inclination, hypothetical_node_longitude)
print(f"Inclination (I): {hypothetical_inclination}°")
print(f"Node Longitude (Omega): {hypothetical_node_longitude}°")
print(f"Pole Vector [X, Y, Z]: [{hypothetical_pole_vector[0]:.6f}, {hypothetical_pole_vector[1]:.6f}, {hypothetical_pole_vector[2]:.6f}]")
