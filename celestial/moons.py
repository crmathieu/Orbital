# moons.py

""" planets.py  """

from orbit3D import *
import planetsdata as pd
from controls import *
#from celestial.orbitalLIB import Api

class makePlanetMoon(makeBody):
	def __init__(self, system, key, color, centralBody):
		"""
		makeBody takes care of drawing the moon's orbit based on the pre-loaded
		orbital elements, when the moon's state_vector can't be directly solved 
		from the orbital elements. 
		"""
#		makeBody.__init__(self, system, key, color, SATELLITE, SATELLITE, SATELLITE_SZ_CORRECTION, centralBody)
		makeBody.__init__(self, system, key, color, MOON, MOON, MOON_SZ_CORRECTION, centralBody)
		self.isMoon = True

		"""
		set up the Nodal regression rate (rad/day) for the longitutde of the 
		ascending node and the Periapsis precession rate (rad/day) for the 
		argument of periapsis. This is valid only for "good behaving moon", 
		whose orbit and position can be deternmined following the keplerian 
		model. It is the default behavior as many moons do follow a that model.
		"""
		self.Omega0 = self.Longitude_of_ascendingnode
		self.omega0 = self.Argument_of_periapsis

		self.Omega_dot, self.omega_dot = self.j2_precession_rates(self.CentralBody.J2)


#	def j2_precession_rates(self, GM, R, J2, a, e, inc, period=None, n=None):

	def j2_precession_rates(self, J2):
		"""
		Compute secular J2 precession rates for a satellite orbiting an oblate planet.

		Parameters
		----------
		GM : float
		    Planet GM (km^3/s^2)
		R : float
		    Planet equatorial radius (km)
		J2 : float
		    Planet J2 coefficient
		a : float
		    Semi-major axis of the moon (km)
		e : float
		    Eccentricity
		inc : float
		    Inclination relative to the planet's equator (radians)
		period : float, optional
		    Orbital period (days). If provided, overrides n.
		n : float, optional
		    Mean motion (rad/day). If not provided, computed from GM and a.

		Returns
		-------
		Omega_dot : float
		    Nodal regression rate (rad/day)
		omega_dot : float
		    Periapsis precession rate (rad/day)
		"""
		"""
		# Compute mean motion if not provided
		if n is None:
		    # Convert GM from km^3/s^2 to km^3/day^2
		    GM_day = GM * (86400.0**2)
		    n = math.sqrt(GM_day / a**3)

		# Or compute from period if given
		if period is not None:
		    n = 2.0 * math.pi / period

		"""

		# calculate or retrieve n, p, a

		n = self.Mean_motion
		a = self.a
		e = self.e
		R = self.CentralBody.BodyRadius
		inc = self.i

		# Semi-latus rectum
		p = a * (1 - e**2)

		# Common J2 factor
		factor = (3.0/2.0) * n * J2 * (R**2 / p**2)

		# Secular rates
		Omega_dot = -factor * math.cos(inc)
		omega_dot = 0.5 * factor * (5.0 * math.cos(inc)**2 - 1.0)

		return Omega_dot, omega_dot

	# makePlanetMoon::
	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		if self.SolarSystem.isFeatured(self.CentralBody.BodyType):
			if self.sizeType == SCALE_OVERSIZED:
				self.Labels[0].visible = False
			else:
				self.Labels[0].visible = True

		self.BodyGeometry.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]

	def setCartesianCoordinates(self, timeIncrement):
			"""
			We need to call the default makeBody::setCartesianCoordinates with a moon distance
			factor
			"""
			return makeBody.setCartesianCoordinates(self, timeIncrement, DIST_FACTOR_MOON)

	def updateBodyPosition(self, timeIncrement):

		# calculate current position based on orbital 
		# elements (timeIncrement comes in days as a float)
		
		dT = daysSinceEpochJD(self.Epoch, self.locationInfo) + timeIncrement 
		print self.Name, ": DT=", dT


		# compute Longitude of Ascending node taking 
		# into account the time elapsed since epoch

		
		if hasattr(self, 'Omega_dot'):
			self.Longitude_of_ascendingnode = self.Omega0 + self.Omega_dot * dT
			self.Argument_of_periapsis = self.omega0 + self.omega_dot * dT
		

		# adjust Mean Anomaly with time elapsed since epoch
		M = toRange(self.Mean_anomaly + self.Mean_motion * dT)

		print "Advancing MOON"
		# since we can't solve Kepler's equation analytically,
		# we use an iterative numerical method

		return solveKepler(M, self.e, 20000)
	

class makeNonKeplerianMoon(makeBody):
	"""
	the makeNonKeplerianMoon class is used for highly pertubed moons whose 
	orbits and state vector can't be described with a keplerian model.
	The most famous one is Luna, our moon
	"""

	def __init__(self, system, key, color, centralBody):
		"""
		makeBody takes care of drawing the moon's orbit based on the pre-loaded
		orbital elements. When the state_vector of the moon can't be directly
		solved from the orbital elements, 
		"""
#		makeBody.__init__(self, system, key, color, SATELLITE, SATELLITE, SATELLITE_SZ_CORRECTION, centralBody)
		makeBody.__init__(self, system, key, color, MOON, MOON, MOON_SZ_CORRECTION, centralBody)
		self.isMoon = True


	# makeNonKeplerianMoon::
	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		if self.SolarSystem.isFeatured(self.CentralBody.BodyType):
			if self.sizeType == SCALE_OVERSIZED:
				self.Labels[0].visible = False
			else:
				self.Labels[0].visible = True

		self.BodyGeometry.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]

	# makeNonKeplerianMoon::
	def setMoonElements(self, name, elts):
		objects_data[name]["profile"] = ""
		objects_data[name]["material"] = 0
		objects_data[name]["name"] = name
		objects_data[name]["iau_name"] = name
		#objects_data[name]["jpl_designation"] = target
		objects_data[name]["distance_to_periapsis"] = elts["periapsis_m"]
		objects_data[name]["eccentricity_EC"] = elts["eccentricity_EC"]
			
		#objects_data[name]["revolution_PR"] = float(arr[PR_SIDERAL_ORBIT].strip()) / SIDEREAL_DAY
			
		objects_data[name]["orbital_inclination_IN"] = elts["orbital_inclination_IN"]

		objects_data[name]["longitude_of_ascendingnode_OM"] = elts["longitude_of_ascendingnode_OM"]
		objects_data[name]["argument_of_periapsis_w"] = elts["argument_of_periapsis_w"]
		objects_data[name]["longitude_of_periapsis_W"] = elts["longitude_of_periapsis_W"]

		objects_data[name]["jd_time_of_periapsis_passage_Tp"] = elts["jd_time_of_periapsis_passage_Tp"]
		objects_data[name]["mean_motion_N"] = elts["mean_motion_N_deg_per_day"]
		objects_data[name]["mean_anomaly_MA"] = elts["mean_anomaly_MA"]

		objects_data[name]["epochJD"] = EPOCH_2000_JD 

		objects_data[name]["earth_moid"] = 0 #float(entry["orbital_data"]["minimum_orbit_intersection"]) * AU,
		objects_data[name]["orbit_class"] = "N/A"
		objects_data[name]["axial_tilt"] = 0.0
		objects_data[name]["utc"] = "" #utc_close_approach.strftime('%Y-%m-%d %H:%M:%S'),
		objects_data[name]["local"] = "" #orbit3D.datetime_from_utc_to_local(utc_close_approach)

		objects_data[name]["albedo"] = 0.0
		objects_data[name]["aphelion"] = elts["apoapsis_m"]
		objects_data[name]["absolute_mag"] = 0 #float(entry["absolute_magnitude_h"]),

	# makeNonKeplerianMoon::
	def setCartesianCoordinates(self, timeIncrement):
		"""
		We need to override the default makeBody::setCartesianCoordinates
		since these cartesian coordinates are normally derived from the body's 
		orbital elements. Because orbital elements for highly pertubed moons are 
		osculating, they can't be trusted to generate the position of the moon 
		with an acceptable precision, hence we need a special function to replace 
		the default method. 

		But, we still need the default setCartesianCoordinate using the canonical
		(constant) orbital elements from data to trace the orbit. Hence we use the 
		new code only after the orbit has been rendered.

		The consequence is that the position of the moon may not always be following
		its orbit right in its trajectory, but may be slightly off. 

		So to recap, the position of the moon is accurate, but its orbit is a mean orbit.
		"""

		if self.hasRenderedOrbit == True:
			self.snapshot = self.getMoonElements(timeIncrement)
			self.setMoonElements("moon", self.snapshot["elements"])
			self.Position = self.snapshot["position_vec"] * DIST_FACTOR_MOON # DIST_FACTOR 
			self.RefOrigin.pos = self.Position
			return self.Position 
		else:
			return makeBody.setCartesianCoordinates(self, timeIncrement, DIST_FACTOR_MOON)

	# makeNonKeplerianMoon::
	def draw(self):
		"""
		since the position can't be directly derived from the body's orbital 
		elements, we need to override the default makeBody::draw by adding a 
		call to the makeLuna::setCartesianCoordinates to reflect the current 
		position of the moon, which doesn't derive its state_vector from the 
		orbital elements.

		"""
		#print "NO DRAW FOR THE MOON!!!!!!!!!!"
		#pass
		makeBody.draw(self)
		self.setCartesianCoordinates(0)


	# makeNonKeplerianMoon::
	def getMoonElements(key, timeIncrement):
		"""
		placeholder. Method should be provided by each moon's 
		to reflect its specific pertubation calculation
		"""
		pass
        #raise NotImplementedError("Subclasses must implement getMoonElements")

	def updateBodyPosition(self, timeIncrement):

		# calculate current position based on orbital 
		# elements (timeIncrement comes in days as a float)
		
		dT = daysSinceEpochJD(self.Epoch, self.locationInfo) + timeIncrement 

		# compute Longitude of Ascending node taking 
		# into account the time elapsed since epoch

		# adjust Mean Anomaly with time elapsed since epoch
		M = toRange(self.Mean_anomaly + self.Mean_motion * dT)

		print "Advancing MOON"
		# since we can't solve Kepler's equation analytically,
		# we use an iterative numerical method

		return solveKepler(M, self.e, 20000)


# CLASS MAKELUNA ------------------------------------------------------------
class makeLuna(makeNonKeplerianMoon):

	def __init__(self, system, color, planet):
		"""
		we need to calculate the most up to date orbital elements
		and state vector for the moon since dramatic perturbations
		prevent the use of normal kepler derivation
		"""

		self.snapshot = {}
		self.snapshot = self.getMoonElements(0)

		# and update the object_data entry
		self.setMoonElements("moon", self.snapshot["elements"])

#		print "makeLuna: before makePlanet::__init"
		makeNonKeplerianMoon.__init__(self, system, "moon", color, planet)
		objects_data["moon"]["tga_name"] = "moon"

#		print "makeLuna: AFTER makePlanet::__init"
		
		#print "...........MOON OLD POSITION:", self.Position
		#self.Position = self.snapshot["position_vec"] * DIST_FACTOR
		#MOON_POS = self.Position
		#self.RefOrigin.pos = self.Position

		#print "...........MOON NEW POSITION:", MOON_POS
		print self.snapshot["position_vec"] * DIST_FACTOR

	def getMoonElements(self, timeIncrement):

		from moon_luna import moon_ephemeris
		from orbit3D import System_utc

		# System_utc is the dateTime reference to estimate all
		# positions in our solare system

		r, v, elems = moon_ephemeris(System_utc, timeIncrement)
		return {
			"position_vec": r, # in meters
			"velocity_vec": v, # in meters/sec
			"elements": elems
		}

