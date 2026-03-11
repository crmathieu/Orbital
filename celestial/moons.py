# -*- coding: utf-8 -*-
# moons.py

""" planets.py  """

from orbit3D import *
import planetsdata as pd
from controls import *
#from celestial.orbitalLIB import Api

class makePlanetMoon(makeBody):
	def __init__(self, system, key, color, sizeCorrectionType, centralbody):
		"""
		makeBody takes care of drawing the moon's orbit based on the pre-loaded
		orbital elements, when the moon's state_vector can't be directly solved 
		from the orbital elements. 
		"""
#		makeBody.__init__(self, system, key, color, ptype=MOON, sizeCorrectionType=MOON, realisticCorrectionSize=MOON_SZ_CORRECTION, centralBody=centralbody)
		makeBody.__init__(self, system, key, color, ptype=MOON, sizeCorrectionType=sizeCorrectionType, realisticCorrectionSize=MOON_SZ_CORRECTION, centralBody=centralbody)

		# register moon with planet's orbiting bodies set
		self.CentralBody.registerSatellite(key, self)

		# create a dictionary of orbiting bodies for this moon
		self.moonOrbitingBodies = {}

		#self.isMoon = True

		"""
		set up the Nodal regression rate (rad/day) for the longitutde of the 
		ascending node and the Periapsis precession rate (rad/day) for the 
		argument of periapsis. This is valid only for "good behaving moon", 
		whose orbit and position can be deternmined following the keplerian 
		model. It is the default behavior as many moons do follow a that model.
		"""
		self.Omega0 = self.Longitude_of_ascendingnode
		self.omega0 = self.Argument_of_periapsis

		#self.Omega_dot, self.omega_dot = self.j2_precession_rates(self.CentralBody.J2)
		
#	def draw(self):
#		pass 

	def registerSpacecraft(self, key, body):
		self.moonOrbitingBodies[key] = body

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

	def setCartesianCoordinatesXX(self, timeIncrement):
			"""
			We need to call the default makeBody::setCartesianCoordinates with a moon distance
			factor
			"""
			return makeBody.setCartesianCoordinates(self, timeIncrement) #, DIST_FACTOR_MOON)

	def updateBodyPosition(self, timeIncrement):

		# calculate current position based on orbital 
		# elements (timeIncrement comes in days as a float)
		
		dT = daysSinceEpochJD(self.Epoch, self.locationInfo) + timeIncrement 
		#print self.Name, ": DT=", dT


		# compute Longitude of Ascending node taking 
		# into account the time elapsed since epoch

		
		if hasattr(self, 'Omega_dot'):
			self.Longitude_of_ascendingnode = self.Omega0 + self.Omega_dot * dT
			self.Argument_of_periapsis = self.omega0 + self.omega_dot * dT
		

		# adjust Mean Anomaly with time elapsed since epoch
		M = toRange(self.Mean_anomaly + self.Mean_motion * dT)

		#print "Advancing MOON"
		# since we can't solve Kepler's equation analytically,
		# we use an iterative numerical method

		return solveKepler(M, self.e, 20000)
	

class makeNonKeplerianMoon(makeBody):
	"""
	the makeNonKeplerianMoon class is used for highly pertubed moons whose 
	orbits and state vector can't be described with a keplerian model.
	The most famous one is Luna, our moon
	"""

	def __init__(self, system, key, color, sizeCorrectionType, centralbody):
		"""
		makeBody takes care of drawing the moon's orbit based on the pre-loaded
		orbital elements. When the state_vector of the moon can't be directly
		solved from the orbital elements, 
		"""
#		makeBody.__init__(self, system, key, color, SATELLITE, SATELLITE, SATELLITE_SZ_CORRECTION, centralBody)
		makeBody.__init__(self, system, key, color, ptype=MOON, sizeCorrectionType=sizeCorrectionType, realisticCorrectionSize=MOON_SZ_CORRECTION, centralBody=centralbody)
		#self.isMoon = True

		# register moon with planet's orbiting bodies set
		self.CentralBody.registerSatellite(key, self)		

		# create a dictionary of orbiting bodies for this moon
		self.moonOrbitingBodies = {}


	def registerSpacecraft(self, key, body):
		self.moonOrbitingBodies[key] = body

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
		#objects_data[name]["material"] = 0
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
			self.setMoonElements(self.Name, self.snapshot["elements"])
			self.Position = self.snapshot["position_vec"] * self.distanceFactor #DIST_FACTOR_MOON # DIST_FACTOR 
			self.RefOrigin.pos = self.Position
			return self.Position 
		else:
			return makeBody.setCartesianCoordinates(self, timeIncrement) #, DIST_FACTOR_MOON)

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

		#print "Advancing MOON"
		# since we can't solve Kepler's equation analytically,
		# we use an iterative numerical method

		return solveKepler(M, self.e, 20000)


# CLASS MAKELUNA ------------------------------------------------------------
class makeLuna(makeNonKeplerianMoon):

	def __init__(self, system, color, centralbody):
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
		makeNonKeplerianMoon.__init__(self, system, "moon", color, MOON, centralbody)
		objects_data["moon"]["tga_name"] = "moon"

#		print "makeLuna: AFTER makePlanet::__init"
		
		#print "...........MOON OLD POSITION:", self.Position
		#self.Position = self.snapshot["position_vec"] * DIST_FACTOR
		#MOON_POS = self.Position
		#self.RefOrigin.pos = self.Position

		#print "...........MOON NEW POSITION:", MOON_POS
		print self.snapshot["position_vec"] * DIST_FACTOR

	def initRotation(self):
			self.setTextureFromSolarTime(None)

	def setTextureFromSolarTime(self, localDatetime):

		# This will position the Moon texture to match the 
		# face observed from the earth surface

		# calculate the angle the moon is making in the earth geocentric ecliptic
		Theta = math.atan2(self.Position[1], self.Position[0])
		print "MOON THETA=", rad2deg(Theta)
		alpha = deg2rad(5)
		self.RefOrigin.rotate(angle=(Theta - alpha), axis=self.RotAxis, origin=(0,0,0))
		return

	def getMoonElements(self, timeIncrement):

		from moon_luna import moon_ephemeris
		from orbit3D import System_utc

		# System_utc is the dateTime reference to estimate all
		# positions in our solare system

		r, v, elems = moon_ephemeris(System_utc, timeIncrement)
		#print "Moon's elements", elems
		return {
			"position_vec": r, # in meters
			"velocity_vec": v, # in meters/sec
			"elements": elems
		}


"""
Some terminology:
Term				Floor (Reference Plane)			Also Known As...
CRF / ICRF			Earth Equator					EME2000, CRF J2000 (Equatorial)
Earth Ecliptic		Earth Orbit						J2000 Ecliptic
Mars Ecliptic		Mars Orbit						(The frame your data is currently in)
Frame Of Reference 	Earth Ecliptic					J2000		


Also, 2 different standards:

Frame				The "Floor" (Reference Plane)	Definition
J2000 / CRF			Earth's Mean Equator			Based entirely on Earth's orientation on Jan 1, 2000.
Invariable Plane	The Solar System's Angular 		The "average" plane of the planets you were thinking of.
					Momentum	

1. The Invariable Plane (The "Average")

In astronomy, we are a bit "Earth-centric":

If you treated the solar system like a spinning top and found its 
true "waist," that would be the Invariable Plane.

    Jupiter has the most mass and momentum, so the Invariable Plane is 
    tilted very closely to Jupiter's orbit.

    The Earth's orbit (Ecliptic) is tilted about 1.57° away from 
    this "average" plane.

2. Why we don't use it as the "Standard"

	Even though the Invariable Plane is more "fair" to all the planets, 
	it’s very hard to measure from a telescope on the ground.

	For centuries, astronomers used the Earth's Equator and Earth's 
	Orbit because those were the "level" and "plumb line" we could 
	actually see. The CRF (J2000) is essentially the modernized, 
	high-precision version of those Earth-based measurements.

SYNONYMS for J2000 Ecliptic:

In the world of orbital mechanics, the "J2000 Ecliptic" has several names depending on whether you are 
talking to a software engineer, a navigator, or an astrophysicist.

Because it refers to a plane (Earth's orbit) at a specific time (January 1, 2000), these are the most 
common synonyms:
1. Technical & Mathematical Synonyms

    Mean Ecliptic of J2000.0: This is the most formal name. "Mean" indicates that 
    short-term "wobbles" (nutation) have been averaged out.

    EME2000 Ecliptic: (Earth Mean Ecliptic 2000). Often used in 
    aerospace codebases.

    Heliocentric Ecliptic (J2000): Frequently used when the coordinate 
    system is centered on the Sun.

    Barycentric Ecliptic (J2000): Used when the center of the coordinate 
    system is the Solar System's center of mass (Barycenter).

2. General Reference Synonyms

    Standard Ecliptic: In most modern textbooks, unless stated otherwise, 
    "the ecliptic" refers to the J2000 standard.

    Earth's Orbital Plane (J2000): The physical description of the frame.

    J2K Ecliptic: Common shorthand in programming (C++, Python, etc.).

3. Contextual "Near-Synonyms" (Caution Required)

	These are often used interchangeably in casual conversation, but they have subtle differences:

    	ICRS Ecliptic: Technically, the ICRS (International Celestial Reference System) is a 
    	set of fixed stars, but "ICRS Ecliptic" is often used to describe the plane derived 
    	from those stars that matches the J2000 ecliptic.

    	Inertial Ecliptic: This distinguishes it from a "rotating" or "of-date" frame that 
    	moves with the Earth's current wobbles.

Crucial Distinction: What is NOT a synonym

	The following are not synonyms for the J2000 Ecliptic:

    	CRF / ICRF / J2000 Equatorial: These refer to the Earth's Equator, which is 
    	tilted 23.44° away from the Ecliptic.

    	Ecliptic of Date: This refers to the Earth's orbit as it exists right now, 
    	which changes slightly every year due to the gravity of other planets.

    	Invariable Plane: This is the "average" plane of the solar system, tilted 
    	about 1.57° away from the J2000 Ecliptic.

SO, just to be clear, If we say:
 	- CRF J2000 
 we am talking about the earth's equatorial plane. But if I say: 
 	- CRF J2000 ecliptic 
 We am talking about the earth's orbital plane

"""
