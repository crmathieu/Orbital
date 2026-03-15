# -*- coding: utf-8 -*-
# moons.py

from orbit3D import *
import planetsdata as pd
from controls import *

"""
CLASS MAKEPLANETMOON -------------------------------------------------------
This class is used to create a moon with predictable behavior, moving in a 
keplerian way
"""
class makePlanetMoon(makeBody):
	def __init__(self, system, key, color, sizeCorrectionType, centralbody):

		makeBody.__init__(self, system, key, color, ptype=MOON, sizeCorrectionType=sizeCorrectionType, realisticCorrectionSize=MOON_SZ_CORRECTION, centralBody=centralbody)

		# register moon with planet's orbiting bodies set
		self.CentralBody.registerSatellite(key, self)

		# create a dictionary of orbiting bodies for this moon
		# (this is to be used for moon orbiting spacecrafts)
		self.moonOrbitingBodies = {}

		"""
		set up the Nodal regression rate (rad/day) for the longitutde of the 
		ascending node and the Periapsis precession rate (rad/day) for the 
		argument of periapsis. This is valid only for "good behaving moon", 
		whose orbit and position can be deternmined following the keplerian 
		model. It is the default behavior as many moons do follow a that model.
		"""
		self.Omega0 = self.Longitude_of_ascendingnode
		self.omega0 = self.Argument_of_periapsis


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


	def updateBodyPosition(self, timeIncrement):

		# calculate current position based on orbital 
		# elements (timeIncrement comes in days as a float)
		
		dT = daysSinceEpochJD(self.Epoch, self.locationInfo) + timeIncrement 

		# compute Longitude of Ascending node taking into account the 
		# precession due to J2 effect and time elapsed since epoch
		
		if hasattr(self, 'Omega_dot'):
			self.Longitude_of_ascendingnode = self.Omega0 + self.Omega_dot * dT
			self.Argument_of_periapsis = self.omega0 + self.omega_dot * dT
		

		# adjust Mean Anomaly with time elapsed since epoch
		M = toRange(self.Mean_anomaly + self.Mean_motion * dT)

		# since we can't solve Kepler's equation analytically,
		# we use an iterative numerical method

		return solveKepler(M, self.e, 20000)
	
"""
CLASS MAKENONKEPLERIANMOON --------------------------------------------------
the makeNonKeplerianMoon class is used for highly pertubed moons whose 
orbits and state vector can't be described with a keplerian model.
The most famous one is Luna, our moon
"""
class makeNonKeplerianMoon(makeBody):

	def __init__(self, system, key, color, sizeCorrectionType, centralbody):

		makeBody.__init__(self, system, key, color, ptype=MOON, sizeCorrectionType=sizeCorrectionType, realisticCorrectionSize=MOON_SZ_CORRECTION, centralBody=centralbody)

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

		# overwrite the moon information pulled from the moon_catalog with fresh 
		# osculating elements. The "physical", "rotation", and "id" fields are 
		# unchanged. Only "elements" is updated with fresh data  

		objects_data[name]["elements"]["distance_to_periapsis_m"] 			= elts["periapsis_m"]
		objects_data[name]["elements"]["eccentricity_EC"] 					= elts["eccentricity_EC"]
		objects_data[name]["elements"]["orbital_inclination_IN"] 			= elts["orbital_inclination_IN"]
		objects_data[name]["elements"]["longitude_of_ascendingnode_OM"] 	= elts["longitude_of_ascendingnode_OM"]
		objects_data[name]["elements"]["argument_of_periapsis_w"] 			= elts["argument_of_periapsis_w"]
		objects_data[name]["elements"]["longitude_of_periapsis_W"] 			= elts["longitude_of_periapsis_W"]
		objects_data[name]["elements"]["jd_time_of_periapsis_passage_Tp"] 	= elts["jd_time_of_periapsis_passage_Tp"]
		objects_data[name]["elements"]["mean_motion_N"] 					= elts["mean_motion_N_deg_per_day"]
		objects_data[name]["elements"]["mean_anomaly_MA"] 					= elts["mean_anomaly_MA"]
		objects_data[name]["elements"]["epochJD"] 							= elts["epochJD"] #EPOCH_2000_JD 
#		objects_data[name]["elements"]["utc"] = "" #utc_close_approach.strftime('%Y-%m-%d %H:%M:%S'),
#		objects_data[name]["elements"]["local"] = "" #orbit3D.datetime_from_utc_to_local(utc_close_approach)
		objects_data[name]["elements"]["aphelion_m"] 						= elts["apoapsis_m"]
		objects_data[name]["elements"]["revolution_PR"] 					= elts["revolution_PR"] #objects_data[name]["rotation"]["rotation_period_solar_d"]

		if hasattr(elts, "phase"):
			objects_data[name]["physical"]["phase"] 						= elts["phase"]
			objects_data[name]["physical"]["phase_angle_deg"] 				= elts["phase_angle_deg"]
			objects_data[name]["physical"]["illumination"] 					= elts["illumination"]

#		print json.dumps(objects_data["moon"], sort_keys=True, indent=4)

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
		makeBody.draw(self)
		self.setCartesianCoordinates(0)


	# makeNonKeplerianMoon::
	def getMoonElements(key, timeIncrement):
		"""
		placeholder. Method should be provided by each moon's 
		to reflect its specific pertubation calculation
		"""
		print "getMoonElements MUST BE overriden by a subclass"
		exit()

	def updateBodyPosition(self, timeIncrement):

		# calculate current position based on orbital 
		# elements (timeIncrement comes in days as a float)
		
		dT = daysSinceEpochJD(self.Epoch, self.locationInfo) + timeIncrement 

		# compute Longitude of Ascending node taking 
		# into account the time elapsed since epoch

		# adjust Mean Anomaly with time elapsed since epoch
		M = toRange(self.Mean_anomaly + self.Mean_motion * dT)

		# since we can't solve Kepler's equation analytically,
		# we use an iterative numerical method

		return solveKepler(M, self.e, 20000)


"""
CLASS MAKELUNA ------------------------------------------------------------
Specific class for "luna", our moon, which is highly pertubed

"""
class makeLuna(makeNonKeplerianMoon):

	def __init__(self, system, color, centralbody):
		"""
		we need to calculate the most up to date orbital elements
		and state vector for the moon since dramatic perturbations
		prevent the use of normal kepler derivation
		"""
		print "MAKE LUNA CONSTRUCTOR"
		self.snapshot = {}
		self.snapshot = self.getMoonElements(0)

		# and update the object_data entry
		self.setMoonElements("moon", self.snapshot["elements"])

		# then call normal constructor with updated data
		makeNonKeplerianMoon.__init__(self, system, "moon", color, MOON, centralbody)

		#print json.dumps(objects_data["moon"], sort_keys=True, indent=4)

		#print "makeLuna: AFTER makePlanet::__init"
		
		#print "...........MOON OLD POSITION:", self.Position
		#self.Position = self.snapshot["position_vec"] * DIST_FACTOR
		#MOON_POS = self.Position
		#self.RefOrigin.pos = self.Position
		#print "...........MOON NEW POSITION:", MOON_POS
		#print self.snapshot["position_vec"] * DIST_FACTOR


	def initRotation(self):

		self.setTexturePosition()

	def to_helioPos(self):
		"""
		The reason we use to_helioPos instead if simply using the frame_to_world frame
		method is that planets and moons coordinates are not on the same distance 
		compression factor which generates disformation, in particular the Position of 
		the LocalEclipticRef is itself compressed by the planet factor, so it can't be 
		reliably used when the true value is required. So to_helioPos is required when
		calculating the true position of a moon in heliocentric ecliptic.
		"""
		# decompress coordinates in order to calculate accurate vectors

		moon_geo = self.Position * (1.0 / self.distanceFactor)
		planet_helio = self.CentralBody.Position * (1.0 / self.CentralBody.distanceFactor)
		moon_helio = moon_geo + planet_helio

		print "moon geo:", moon_geo, ", moon helio position:", moon_helio
		return moon_helio

	def setTexturePosition(self):

		# 1. Define the Vernal Equinox direction (your reference X-axis)
		vernal_equinox = vector(1, 0, 0)

		# 2. calculate true earth position

		earth_helio = vector()
		earth_helio = self.CentralBody.Position * (1/self.CentralBody.distanceFactor)

		# 3. calculate vector difference between moon_helio and earth_helio
		em_vec = self.to_helioPos() - earth_helio

		# 4. Calculate angle (using diff_angle for VPython vector convenience)
		print "Earth_moon vec:", em_vec, " vernal eq vec:", vernal_equinox
		angle_to_equinox = diff_angle(em_vec, vernal_equinox)

		# 4. Apply rotation
		# You want the face of the moon to look at the earth.
		# We rotate the moon around the orbital normal to match the equinox offset.

		self.RefOrigin.rotate(angle=-(np.pi/2 + abs(angle_to_equinox)), axis=self.RotAxis, origin=(0,0,0))


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
---------------------------------------------------------------------------------------------
CRF / ICRF			Earth Equator					EME2000, CRF J2000 (Equatorial)
Earth Ecliptic		Earth Orbit						J2000 Ecliptic
Mars Ecliptic		Mars Orbit						(The frame your data is currently in)
Frame Of Reference 	Earth Ecliptic					J2000		


Also, 2 different standards:

Frame				The "Floor" (Reference Plane)	Definition
---------------------------------------------------------------------------------------------
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
---------------------------

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
 we are talking about the earth's equatorial plane. But if I say: 
 	- CRF J2000 ecliptic 
 We are talking about the earth's orbital plane

"""
