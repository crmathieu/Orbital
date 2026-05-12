# -*- coding: utf-8 -*-
"""
	Copyright (c) 2017 Charles Mathieu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
# Body types
INNER_PLANET 			= 0x01
OUTER_PLANET 			= 0x02

MOON 					= 0x04
#BARYCENTER_MEMBER 		= 0x04
 	
SPACECRAFT 				= 0x08
ASTEROID 				= 0x10
GAS_GIANT 				= 0x20
DWARF_PLANET 			= 0x40
TNO 					= 0x80
COMET 					= 0x100

SMALL_ASTEROID 			= 0x200
BIG_ASTEROID 			= 0x400
PHA 					= 0x800
ASTEROID_BELT 			= 0x1000
KUIPER_BELT 			= 0x2000
INNER_OORT_CLOUD 		= 0x4000
ECLIPTIC_PLANE 			= 0x8000

LIT_SCENE 				= 0x10000
REFERENTIAL 			= 0x20000
ORBITS 					= 0x40000
LABELS 					= 0x80000

JTROJANS 				= 0x100000
REALSIZE 				= 0x200000
LOCAL_REFERENTIAL 		= 0x400000
CELESTIAL_SPHERE 		= 0x800000
HYPERBOLIC 				= 0x1000000
CONSTELLATIONS 			= 0x2000000

STAR 					= 0x4000000
SUN 					= 0x4000000

SMALL_MOON				= 0x8000000
SMALLER_MOON			= 0x10000000
TINY_MOON  				= 0x20000000
BIG_MOON				= 0x40000000
BARYCENTER				= 0x80000000
BARYCENTER_MEMBER		= 0x100000000


TYPE_MASK = 0xFFFFFFFFF

# Pluto-Charon barycenter as the reference center
# 500@9 = Pluto system barycenter (same as Pluto-Charon barycenter)
PLUTO_BARYCENTER = "500@9"
SUN_BARYCENTER = "500@0"

SPACECRAFT_M = 100
THREE_D = False
MAX_P_D = 1.1423e13
MIN_P_D = 46.0e9

LEGEND = True

SUN_M = 1.989e+30 # in Kg
SUN_R = 6.957e8 # in m

G = 6.67384e-11	# Universal gravitational constant
Mu = G * SUN_M


# EPOCH constants
#EPOCH_2000_JD = 2451544.5	# number of days ellapsed from 01-01-4713 BC GMT to 01-01-2000 AD GMT
EPOCH_2000_JD = 2451545.0	# number of days ellapsed from 01-01-4713 BC GMT to 01-01-2000 AD @ 12pm GMT
EPOCH_2000_MJD = 51544.0
EPOCH_1970_JD = 2440587.5 # number of days ellapsed from 01-01-4713 BC GMT to 01-01-1970 AD GMT

J2000_TDB = 2451545.0


TYPE_STAR = 0
TYPE_PLANET = 1
TYPE_ASTEROID = 2
TYPE_DWARF_PLANET = 3
TYPE_COMET = 4
TYPE_TRANS_N = 5
#TYPE_SATELLITE = 6
TYPE_MOON = 7

CURRENT_BODY = "current_body"
EARTH_NAME = "earth"
SUN_NAME = "sun"
JUPITER_PERIHELION = 740.52e9
DEFAULT_FRAMERATE = 20.0

index_to_month = {
	1: "Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"
}

index_to_bodyname = {
	0: CURRENT_BODY,	1: SUN_NAME,	2: EARTH_NAME,	3: "mercury",	4:"venus",		
	5:"mars",       	6:"jupiter",	7:"saturn",   	8:"uranus", 	9:"neptune",
	10:"pluto",     	11:"sedna", 	12:"makemake",	13:"haumea",	14:"eris", 
	15:"charon",    	16:"phobos",	17:"adrastea",	18:"mimas",     19:"moon"
}

bodyname_to_index = {
	index_to_bodyname[0]: 0, 	index_to_bodyname[1]: 1, 	index_to_bodyname[2]: 2, 	index_to_bodyname[3]: 3, 	
	index_to_bodyname[4]: 4,	index_to_bodyname[5]: 5, 	index_to_bodyname[6]: 6, 	index_to_bodyname[7]: 7, 	
	index_to_bodyname[8]: 8, 	index_to_bodyname[9]: 9,	index_to_bodyname[10]: 10, 	index_to_bodyname[11]: 11, 	
	index_to_bodyname[12]: 12, 	index_to_bodyname[13]: 13, 	index_to_bodyname[14]: 14, 	index_to_bodyname[15]: 15, 		
	index_to_bodyname[16]: 16, 	index_to_bodyname[17]: 17, 	index_to_bodyname[18]: 18,  index_to_bodyname[19]: 19 
}

AU = 149597870691
DEFAULT_RADIUS = 2.0

LOOKUP_SPKID = 0
LOOKUP_NAME = 1
LOOKUP_JPL_DESIGNATION = 2
LOOKUP_IAU_NAME = 3
LOOKUP_DIAMETER = 5


JPL_FULLNAME = 0
JPL_DESIGNATION = 1
JPL_IAU_NAME = 2
JPL_PREFIX = 3
JPL_NEAR_EARTH_ORBIT = 4
JPL_PHA = 5
JPL_MAG_H = 6
JPL_MAG_G = 7
JPL_MAG_M1 = 8
JPL_MAG_M2 = 9
JPL_MAG_K1 = 10
JPL_MAG_K2 = 11
JPL_MAG_PC = 12
JPL_DIAMETER = 13
JPL_EXTENT = 14
JPL_ALBEDO = 15
JPL_ROT_PER = 16
JPL_GM = 17
JPL_MAG_BV = 18
JPL_MAG_UB = 19
JPL_MAG_IR = 20
JPL_SPEC_1 = 21
JPL_SPEC_2 = 22
JPL_H_SIGMA = 23
JPL_DIAMETER_SIGMA = 24
JPL_ORBIT_ID = 25
JPL_EPOCH_JD = 26
JPL_EPOCH_MJD = 27
JPL_EPOCH_ET = 28
JPL_EQUINOX = 29

JPL_OE_e = 30
JPL_OE_a = 31
JPL_OE_q = 32
JPL_OE_i = 33
JPL_OE_N = 34
JPL_OE_w = 35
JPL_OE_M = 36
JPL_OE_Q = 37
JPL_OE_n = 38
JPL_OE_tp_JD = 39
JPL_OE_tp_ET = 40
JPL_OE_Pd = 41
JPL_OE_Py = 42
JPL_EARTH_MOID_AU = 43
JPL_EARTH_MOID_LD = 44
JPL_JUPITER_MOID_AU = 45
JPL_ORBIT_CLASS = 58

# a few facts about earth rotation:
# - A sidereal period is the time required for a given body to return to the same position
#   relative to the stars. It is 86164.0905 seconds (23 h 56 min 4.0905 s or 23.9344696 h)
# - A synodic period, the time required for a body within the solar system, such as a planet, 
#   the Moon, or an artificial Earth satellite, to return to the same or approximately the same 
#   position relative to the Sun as seen by an observer on the Earth. It is 86400 seconds (24h)
#
# The Earth rotation angle (ERA) measures the rotation of the Earth from an origin on the celestial 
# equator, the Celestial Intermediate Origin (CIO), that has no instantaneous motion along the equator; 
# it was originally referred to as the non-rotating origin.
#
# ERA, measured in radians, is related to UT1 by a simple linear polynomial:
#
# Theta (tU) = 2 PI (0.779 057 273 2640 + 1.002 737 811 911 354 48 x tU) 
# where tU=JD-J2000 is the Julian UT1 date (JD) relative to the J2000 epoch (JD 2451545.0). The linear 
# coefficient represents the Earth's rotation speed. 

# time increments in day unit


TI_SOLAR_DAY				 = 86400.0			# in mean solar seconds
TI_SIDEREAL_DAY 			 = 86164.0905	# in mean solar secs
SOLAR_DAY_RATIO 			 = TI_SIDEREAL_DAY/TI_SOLAR_DAY 	# as a ratio of MEAN solar day. It's almost one,
															# 0.997269565972222, but not completely. This is the ratio
															# set for the earth rotation
TI_SOLAR_YEAR				 = 365.24 		# in solar days
TI_SIDEREAL_YEAR			 = 366.24		# in sidereal days

TI_ONE_MEAN_SOLAR_SECOND 	 = 1.0 / TI_SOLAR_DAY 	# in mean solar days #1.157407e-5 : 1d -> 86400 sec => 1sec = 1/86400 day
TI_ONE_SIDEREAL_SOLAR_SECOND = 365.25/366.25 # in UT1 seconds     # 1 / TI_SIDEREAL_DAY


# analemma special value for visualization
TI_ONE_SECOND_ANA 			 = 1.160585e-5	# normally, it should be 1.160576284e-5 since it is 1/86164.0905 sec 
											# but rounding to this value gives a more stable rotation.

#TI_24_HOURS_ANA 	= TI_ONE_SECOND_ANA * TI_SIDEREAL_DAY

#TI_24_HOURS_ANA 	= 1 #TI_ONE_SECOND_ANA * TI_SOLAR_DAY			# 1.00274544 solar day

#TI_ONE_SECOND 	= 1.160576e-5 # 1d -> 86164.0905 sec => 1 sec = 1/86164.0905 day

# values used in Time Slider
TI_ONE_SECOND		= TI_ONE_MEAN_SOLAR_SECOND # 1.1574074074074074074074074074074e-5 in  mean solar day
TI_10_SECONDS 		= TI_ONE_SECOND * 10
TI_30_SECONDS 		= TI_ONE_SECOND * 30
TI_ONE_MINUTE 		= TI_ONE_SECOND * 60
TI_FIVE_MINUTES 	= TI_ONE_MINUTE * 5 
TI_TEN_MINUTES 		= TI_ONE_MINUTE * 10 

TI_ONE_HOUR 		= TI_TEN_MINUTES * 6
TI_SIX_HOURS 		= TI_TEN_MINUTES * 36
TI_TWELVE_HOURS 	= TI_TEN_MINUTES * 72
TI_24_HOURS 		= TI_TEN_MINUTES * 144
TI_FULL_YEAR		= TI_24_HOURS  * 365.25

print "=========================>>>>>>>>>>>>> 1 SEC=", TI_ONE_SECOND, ", 24H = ", TI_24_HOURS

#TI_ONE_HOUR 	= 0.0416666666
#TI_SIX_HOURS 	= 0.25
#TI_TWELVE_HOURS = 0.5
#TI_24_HOURS 	= 1

"""
Frame_IntervalsXX = { 
	TI_ONE_SECOND 	: { "value": 1, "label": "1", "unit": "s"},
	TI_10_SECONDS 	: { "value": 10, "label": "10", "unit": "s"},
	TI_30_SECONDS 	: { "value": 30, "label": "30", "unit": "s"},

	TI_ONE_MINUTE 	: { "value": 1, "label": "1", "unit": "m"},
	TI_FIVE_MINUTES : { "value": 5, "label": "5", "unit": "m"},
	TI_TEN_MINUTES 	: { "value": 10, "label": "10", "unit": "m"}, 
	TI_ONE_HOUR 	: { "value": 60, "label": "1", "unit": "h"}, 
	TI_SIX_HOURS 	: { "value": 360, "label": "6", "unit": "h"},
	TI_TWELVE_HOURS : { "value": 720, "label": "12", "unit": "h"}
}
"""

# the following handles time interval values based on the dialer's position
Frame_Intervals = { # incr values are always expressed in (fraction of a) day...
	1: { "incr": TI_ONE_SECOND,  "value": 1, 		"label": "1", 	"unit": "s"},
	2: { "incr": TI_10_SECONDS,  "value": 10, 		"label": "10", 	"unit": "s"},
	3: { "incr": TI_30_SECONDS,  "value": 30, 		"label": "30", 	"unit": "s"},
	4: { "incr": TI_ONE_MINUTE,  "value": 1,  		"label": "1", 	"unit": "m"},
	5: { "incr": TI_FIVE_MINUTES,"value": 5, 		"label": "5", 	"unit": "m"},
	6: { "incr": TI_TEN_MINUTES, "value": 10, 		"label": "10", 	"unit": "m"}, 
	7: { "incr": TI_ONE_HOUR,    "value": 1, 		"label": "1", 	"unit": "h"}, 
	8: { "incr": TI_SIX_HOURS, 	 "value": 6, 		"label": "6", 	"unit": "h"},
	9: { "incr": TI_TWELVE_HOURS,"value": 12, 		"label": "12", 	"unit": "h"},
   10: { "incr": TI_24_HOURS,	 "value": 1, 		"label": "24", 	"unit": "d"}
}


INITIAL_INCREMENT_KEY = 1
#TimeIncrementKey = 1
INITIAL_TIMEINCR = Frame_Intervals[INITIAL_INCREMENT_KEY]["incr"] #TI_ONE_SECOND #TI_TEN_MINUTES # 
#BaseTimeIncrement = INITIAL_TIMEINCR

"""
SCALING
"""

# scale toggling:
# toggles between in "inflated" view of planets, and a more up-to-scale view
# where planets are more in relation to their real dimension. THIS MAY GO AWAY
SCALE_OVERSIZED = 0
SCALE_NORMALIZED = 1

# size and distance corrections...
# we apply a coefficient to reduce distances which are vastly too big for a 
# practical use in a simulation.
# 
# The SMALLER the number in DIST_FACTOR, the MORE compressed distances will be. 
#
# For MOONS, we need to compress less so 
# that we can see them around their central body. If we'd compress with the 
# same ratio, they would be all inside their central body, as their semi-major
# axis is very small compared to interplanetary distances. On the opposite side
# we want to make the planets and their moons visible, so we want to boost their
# size that pales in comparison to the distances separating them.

#DIST_FACTOR = 10e-7 # <--- The original distance factor
DIST_FACTOR = 0.6e-5 # <--- New distance factor

#DIST_FACTOR_MOON = DIST_FACTOR * 8 # <--- distance factor to use for a moon orbit around its central body
DIST_FACTOR_MOON = DIST_FACTOR * 15 # <--- distance factor to use for a moon orbit around its central body


planet_moon_dist_factor = {
	"earth": DIST_FACTOR * 18,
	"mars" : DIST_FACTOR * 80,
	"pluto": DIST_FACTOR * 80,
	"pluto-barycenter": DIST_FACTOR * 150,
	"jupiter": DIST_FACTOR * 75,
	"saturn": DIST_FACTOR * 75,
	"uranus": DIST_FACTOR * 30,
	"neptune": DIST_FACTOR * 70,
	"mercury": DIST_FACTOR,
	"venus": DIST_FACTOR,
}


# original SZ correction:
# The following are default sizes used when objects are 
# displayed in a more realistic way, instead of their
# inflated version

SUN_SZ_CORRECTION 			= 1/(DIST_FACTOR * 5)
PLANET_SZ_CORRECTION 		= 1/(DIST_FACTOR * 5)
#SATELLITE_SZ_CORRECTION 	= 1/(DIST_FACTOR * 5)
MOON_SZ_CORRECTION 			= 1/(DIST_FACTOR * 5)
HYPERBOLIC_SZ_CORRECTION 	= 1/(DIST_FACTOR * 5)
### ASTEROID_SZ_CORRECTION = 1e-2/(DIST_FACTOR * 5)

#DWARF_PLANET_SZ_CORRECTION 	= 1e-2/(DIST_FACTOR * 5)
DWARF_PLANET_SZ_CORRECTION 	= 1/(DIST_FACTOR * 5)

SMALLBODY_SZ_CORRECTION 	= 1e-6/(DIST_FACTOR*5) #(default)
ASTEROID_SZ_CORRECTION 		= SMALLBODY_SZ_CORRECTION

# scale per body type. We need to apply a coefficient to increase
# the size of the planets and moons, so that we can see them more
# easily in the simulation. The bodyScaler dictionary tells what
# coefficeint to use in relation to a particular type of object.
# The LOWER the number, the MORE "inflated" the object will be.

#bodyScaler = { SUN: 55000, SPACECRAFT: 1, INNER_PLANET: 1200, SATELLITE:1400, GAS_GIANT: 3500, DWARF_PLANET: 100, ASTEROID:1, COMET:0.02, SMALL_ASTEROID: 0.1, BIG_ASTEROID:0.1, PHA: 0.007, TNO: 0.001}

# original bodyscaler
bodyScaler = { 	SUN: 			15000, 
				SPACECRAFT: 	1, 
				INNER_PLANET: 	1400, 
				BIG_MOON: 		2000, 
				MOON: 			1400, 
				SMALLER_MOON:	300,
				SMALL_MOON:		100, 
				TINY_MOON: 		30, 
				GAS_GIANT: 		1300, 
				DWARF_PLANET: 	35, 
				ASTEROID:		1, 
				COMET:			0.02, 
				SMALL_ASTEROID: 0.1, 
				BIG_ASTEROID:	0.1, 
				PHA: 			0.04, 
				TNO: 			20 #50
}

#bodyScaler = { SUN: 120000, SPACECRAFT: 1, INNER_PLANET: 2400, MOON: 2400, GAS_GIANT: 4500, DWARF_PLANET: 100, ASTEROID:1, COMET:0.02, SMALL_ASTEROID: 0.1, BIG_ASTEROID:0.1, PHA: 0.007, TNO: 0.001}

# new bodyscaler
#bodyScaler = { SUN: 5000, SPACECRAFT: 1, INNER_PLANET: 1800, SATELLITE:1400, GAS_GIANT: 2200, DWARF_PLANET: 100, ASTEROID:1, COMET:0.02, SMALL_ASTEROID: 0.1, BIG_ASTEROID:0.1, PHA: 0.007, TNO: 0.001}

# body shapes
BodyGeometryTypes = { SUN: "sphere", SPACECRAFT: "cylinder", INNER_PLANET: "sphere", MOON: "sphere", OUTER_PLANET: "sphere", DWARF_PLANET: "sphere", ASTEROID:"cube", COMET:"cone", SMALL_ASTEROID:"cube", BIG_ASTEROID:"sphere", PHA:"cube", TNO: "sphere"}
#BodyGeometryTypes = { SUN: "sphere", SPACECRAFT: "cylinder", INNER_PLANET: "sphere", OUTER_PLANET: "sphere", SATELLITE: "sphere", DWARF_PLANET: "sphere", ASTEROID:"cube", COMET:"cone", SMALL_ASTEROID:"cube", BIG_ASTEROID:"sphere", PHA:"cube", TNO: "cube"}



# sun synchronous precession rate per second (calculated using
# the 360 deg per sidereal year) using the formula:
# rate = 360 /(SIDEREAL_YEAR * EPHEMERIS_DAY)) degrees/s -or- 
#        (PI * 2) / (SIDEREAL_YEAR * EPHEMERIS_DAY) rad/s
#  

EPHEMERIS_DAY = 86400 # in seconds
MEAN_SOLARDAY = 86400 # in seconds
SIDEREAL_DAY = 86164.0905 # in seconds

SIDEREAL_YEAR = 365.256363004  # in ephemeris days

"""
The value of 365.2425 days is an exact value; it is the average number of days per year per the Gregorian calendar. 
The Gregorian calendar repeats over a 400 span. In any 400 span, there will be 97 leap years (96 non-century leap 
years, plus one century leap year) with 366 days and 303 years with 365 days. That results in 146097/400 days in a 
year on average, or exactly 365.2425 days.
"""
TROPICAL_YEAR 			= 365.2421871    # in ephemeris days
EARTH_PERIOD 			= 365.25 #TROPICAL_YEAR #SIDEREAL_YEAR
EARTH_CENTURY 			= 36525
EARTH_MEAN_MOTION_WIKI 	= 1.99096871e-7  	# in rad/s according to wikipedia
								 	# but = 1.9909865927683785320224459427387e-7 rd/s according to calculation
EARTH_DAILY_MEAN_MOTION = 0.01720212416151879051667393294526 # in rd/day
EARTH_MEAN_MOTION 		= 1.9909865927683785320224459427387e-7 # in rd/s

def getEarthMeanMotion2():
	return (pi * 2)/(SIDEREAL_YEAR * EPHEMERIS_DAY)

	
#from visual import color
from vpython_interface import Color


"""2
# Coefficients (alpha0_J2000, alpha0_dot, delta0_J2000, delta0_dot)
# alpha0_dot and delta0_dot are per Julian century
# Periodic terms are added where applicable.
# Data from IAU 2009 WGCCRE Report (Archinal et al. 2010), Table 2.
# Note: For Earth, these simplified formulas are for comparison, IERS data is more precise.
planet_data = {
    "Sun":       (286.13,    0.0,     63.87,    0.0),
    "Mercury":   (281.0097, -0.0328,  61.4143, -0.0049),
    "Venus":     (272.76,    0.0,     67.16,    0.0), 	# Retrograde rotation, but pole is defined by north of invariable plane
    "Earth":     (0.00,     -0.641,   90.00,   -0.557),
    "Mars":      (317.68143, -0.1061,  52.88650, -0.0609),
    # Jupiter includes periodic terms
    "Jupiter":   (268.056595, -0.006499, 64.495303, 0.008391),
    "Saturn":    (40.589,   -0.036,   83.537,  -0.004),
    "Uranus":    (257.31,    0.0,    -15.18,    0.0), 	# Retrograde rotation, but pole is defined by north of invariable plane
    "Neptune":   (299.36,    0.70,    43.46,    0.0),
    # Pluto's pole model in IAU 2009 is linear, no periodic terms listed.
    "Pluto":     (313.02,   -0.001,    9.09,    0.005)
}
"""

# Note: the "rotationalElts" structure contains the information relevant to a planet's rotation axis 
# direction. Each planet has its own algorithm to determine its orientation and therefore must have
# a different "rotationalElts" structure, as well as a custom "setRightAscensionAngle" method to 
# handle its specific content. These methods are defined in each planet class in planets.py.
# see document: doc/"method to determine north Pole orientation"

"""
Jupiter 	Io 	501 	JUP365 	Laplace 	2000-01-01.5 	421800. 	0.004 	49.1 	330.9 	0.0 	0.0 	1.762732 	1.333 	0.000 	268.1 	64.5 	0.0 	28
Jupiter 	Europa 	502 	JUP365 	Laplace 	2000-01-01.5 	671100. 	0.009 	45.0 	345.4 	0.5 	184.0 	3.525463 	1.394 	30.202 	268.1 	64.5 	0.0 	28
Jupiter 	Ganymede 	503 	JUP365 	Laplace 	2000-01-01.5 	1070400. 	0.001 	198.3 	324.8 	0.2 	58.5 	7.155588 	68.301 	137.812 	268.2 	64.6 	0.1 	28
Jupiter 	Callisto 	504 	JUP365 	Laplace 	2000-01-01.5 	1882700. 	0.007 	43.8 	87.4 	0.3 	309.1 	16.690440 	277.921 	577.264 	268.7 	64.8 	0.4 	28

	"io": {
		"type": TYPE_SATELLITE,
		"material":1,
		"name": "Io",
		"symbol": "",
		"iau_name": "Io",
		"jpl_designation": "io",
		"mass": 7.342e+22,
		"radius": 1738.1e+3,
		"distance_to_periapsis":0.00237529455014751*AU,
		"aphelion":0.00270352798850*AU,
		"eccentricity_EC":6.462786125327587e-02,
		"revolution_PR":27.321582,
		"rotation":27.321582 * SOLAR_DAY_RATIO, # in days
		"orbital_inclination_IN":5.27749841723057, #23.44, # to earth eq.
		"longitude_of_ascendingnode_OM":143.9091328687446,
		"longitude_of_periapsis_W":296.9775666926365+143.9091328687446,
		"mean_anomaly_MA": 158.3907159645461,
		"mean_motion_N":13.42988221368860,
		"epochJD": 2457994.50,
		"jd_time_of_periapsis_passage_Tp": 2457982.706097905825,

		"axial_tilt": 6.67, # to its own orbital plane1.263=
		"absolute_mag": 0.0,
		"orbit_class": "E-SAT",
		"tga_name": "Moon"
	},
		"Moon": {
		"M_deg": 140.14966404910976, 
		"e": 0.053574743523550905, 
		"omega_dot_deg_day": 1.1487795987460944e-05, 
		"Omega_deg": 123.95805543719277, 
		"revolution_days": 27.63832883056322, 
		"epochJD": 2461086.1573032406, 
		"Omega_dot_deg_day": -5.780161074447413e-06, 
		"planet": "Earth", 
		"n_deg_day": 13.025389567038589, 
		"mass_kg": 5.0098137632410894e+19, 
		"i_deg": 5.240273000309319, 
		"omega_deg": 315.4342061988724, 
		"rotation_days": 27.321661, 
		"a_m": 386138429.0737721, 
		"Tp_JD": 2451534.240270832, 
		"radius_m": 4902800.066
	"""			
all_objects = {}


texture = {
	"mercury": 	"mercury",
	"venus":	"venus",
	"earth": 	"highres-earth-8192x4096-clouds",
	"mars": 	"mars",
	"jupiter": 	"source/2k_jupiter-PM-normalized",
	"saturn": 	"saturn",
	"uranus": 	"uranus",
	"neptune": 	"source/2k_neptune-PM-normalized",
}

objects_data = {}
objects_data2 = {


	# highly pertubed Moons
	"moon" :{

		# Note:
		# For moons, and since orbital elements are always expressed in term 
		# of the ecliptic plane, the GeoEcliptic must also have its x,y
		# plane in the ecliptic 

		"type": TYPE_MOON,
		"material":1,
		"name": "Moon",
		"symbol": u"\u263D ",
		"iau_name": "Moon",
		"jpl_designation": "moon",
		"mass": 7.342e+22,
		"radius": 1738.1e+3,
		"distance_to_periapsis":0.00237529455014751*AU,
		"aphelion":0.00270352798850*AU,
		"eccentricity_EC":6.462786125327587e-02,
		"revolution_PR":27.321582,
		"rotation":27.321582 * SOLAR_DAY_RATIO, # in days
		"orbital_inclination_IN":5.27749841723057,# to earth ecliptic #23.44, # to earth eq.
		"longitude_of_ascendingnode_OM":143.9091328687446,
		"longitude_of_periapsis_W":296.9775666926365+143.9091328687446,
		"mean_anomaly_MA": 158.3907159645461,
		"mean_motion_N":13.21247237789748,
		"epochJD": 2457994.50,
		"jd_time_of_periapsis_passage_Tp": 2457982.706097905825,

		"axial_tilt": 6.67, # to its own orbital plane1.263=
		"absolute_mag": 0.0,
		"orbit_class": "E-SAT",
		"tga_name": "Moon"
		},


	# keplerian Moons
	"phobos" :{
		"type": TYPE_MOON,
		"material":0,
		"name": "Phobos",
		"iau_name": "Phobos",
		"jpl_designation": "phobos",
		"mass": 1.1e+16,
		"radius": 15*11.1e+3,
		"distance_to_periapsis":4*9.236397056433352E+06, #4*9234.42e+3,
		"aphelion":4*9.519289172301515E+06, #4*9517.58e+3,
		"eccentricity_EC":1.508300535731693E-02,
		"revolution_PR":0.3191794301882109,
		"rotation":0.3191794301882109 * SOLAR_DAY_RATIO, # in days
		"orbital_inclination_IN":2.566118935798619E+01, # to ecliptic, #1.093, # to mars eq #
		"longitude_of_ascendingnode_OM":8.223772856123789E+01,
		"longitude_of_periapsis_W":2.762475522960488E+02+8.223772856123789E+01,
		"mean_anomaly_MA": 8.524147919084433E+01,
		"mean_motion_N":1.128100327597539E+03,
		"epochJD": 2458001.50,
		"jd_time_of_periapsis_passage_Tp": -0.075561966525,

		"axial_tilt": 0.046, # to its own orbital plane
		"absolute_mag": 0.0,
		"orbit_class": "M-SAT",
		"tga_name": "Phobos"
		},
	"deimos" :{
		"type": TYPE_MOON,
		"material":0,
		"name": "Deimos",
		"iau_name": "Deimos",
		"jpl_designation": "deimos",
		"mass": 1.4762e+15,
		"radius": 15*6.2e+3,
		"distance_to_periapsis":4*2.345311353009123E+07, #4*23455.5e+3,
		"aphelion":4*2.346540189020549E+07, #4*23470.9e+3,
		"eccentricity_EC":2.619085451484923E-04,
		"revolution_PR":1.262540567604984,
		"rotation":1.262540567604984 * SOLAR_DAY_RATIO, # in days
		"orbital_inclination_IN":2.544419693842261E+01, # to ecliptic, 0.93, # to mars eq. #
		"longitude_of_ascendingnode_OM":7.875346643344125E+01,
		"longitude_of_periapsis_W":3.353099851925172E+02+7.875346643344125E+01,
		"mean_anomaly_MA": 3.541134423740633E+02,
		"mean_motion_N":2.851220253841971E+02,
		"epochJD": 2458001.50,
		"jd_time_of_periapsis_passage_Tp": 0.020645748493,

		"axial_tilt": 0.897, # to its own orbital plane
		"absolute_mag": 0.0,
		"orbit_class": "M-SAT",
		"tga_name": "Deimos"
		},
	"charon" :{
		"type": TYPE_MOON,
		"material":0,
		"name": "Charon",
		"iau_name": "Charon",
		"jpl_designation": "charon",
		"mass": 1.586e+21,
		"radius": 15*606e+3,
		"distance_to_periapsis":100*1.959394328352395E+07, # 19596e+3, we multiply by 100 since pluto is bigger than it should
		"aphelion":100*1.959976480409748E+07, # 19596e+3, we multiply by 100 since pluto is bigger than it should
		"eccentricity_EC":1.485320184688916E-04,
		"revolution_PR":6.387221715378253,
		"rotation":6.387221715378253 * SOLAR_DAY_RATIO, # in days
		"orbital_inclination_IN":1.128960563495295E+02, # to ecliptic
		"longitude_of_ascendingnode_OM":2.274019157345203E+02,
		"longitude_of_periapsis_W":1.895323185981683E+02+2.274019157345203E+02,
		"mean_anomaly_MA": 7.639225900405658E+01,
		"mean_motion_N":5.636253382800892E+01,
		"epochJD": 2458001.50,
		"jd_time_of_periapsis_passage_Tp": -1.355373043326,

		"axial_tilt": 0, # to its own orbital plane
		"absolute_mag": 1.0,
		"orbit_class": "M-SAT",
		"tga_name": "Charon"
		},

	"sunZob" :{
		"type": TYPE_STAR,
		"material":1,
		"name": "Sun",
		"symbol": u"\u2609 ",
		"iau_name": "SUN",
		"jpl_designation": "sun",
		"mass":1.98855e+30,
		"radius":3.47850e+8,
		"distance_to_periapsis":0,
		"eccentricity_EC":0,
		"revolution_PR":0,
		"rotation":25.38,
		"orbital_inclination_IN":67.23, # to the galactic plane
		"longitude_of_ascendingnode_OM":0,
		"longitude_of_periapsis_W":0,
		"axial_tilt": 7.25,
		"absolute_mag": 0.0,
		"tga_name": "Sun"
	},



	"sun" : {
		"type": TYPE_STAR,
		"material":1,
		"name": "Sun",
		"symbol": u"\u2609 ",
		"iau_name": "SUN",
		"jpl_designation": SUN_NAME,
		"mass":SUN_M,
		"radius":SUN_R,
		"distance_to_periapsis":0.0,
		"eccentricity_EC":0.0,
		"revolution_PR": 0,
		"rotation":	25.05 * SOLAR_DAY_RATIO,
		"orbital_inclination_IN":0,
		"longitude_of_ascendingnode_OM":0.0,
		"longitude_of_periapsis_W":0.0,
		"axial_tilt": 7.25,
		"absolute_mag": 0.0,
		"rotationalElts": {
			"W_1": 0.00,
			"W_2": -0.641,
			"W_C": 0
		},
		"drift_coef":{
			'a' : 1.00000018, 
			'ar': -3e-08, 
			'e' : 0.01673163, 
			'er':-3.661e-05, 
			'i' :-0.00054346, 
			'ir':-0.01337178, 
			'L' :100.46691572, 
			'Lr':35999.3730633, 
			'W' :102.93005885, 
			'Wr':0.3179526, 
			'N' :-5.11260389, 
			'Nr':-0.24123856, 
			'b' :0.0, 
			'c' :0.0, 
			's': 0.0, 
			'f' :0.0
		},
		"tga_name": "sun"
#		"tga_name": "source/2k_sun"
	},

	"neptune" :{
		"type": TYPE_PLANET,
		"material":1,
		"name": "Neptune",
		"symbol": u"\u2646 ",
		"iau_name": "NEPTUNE",
		"jpl_designation": "neptune",
		"mass":102e+24,
		"radius":24.622e+6,
		"distance_to_periapsis":4444.45e+9,
		"eccentricity_EC":0.00858587,
		"revolution_PR":60182,
		"rotation":0.6713 * SOLAR_DAY_RATIO,
		"orbital_inclination_IN":1.769,
		"longitude_of_ascendingnode_OM":131.72169,
		"longitude_of_periapsis_W":44.97135,
		"axial_tilt": 28.32,
		"absolute_mag": 0.0,
		"rotationalElts": {
			"""
			N=357.85 + 52.316T			
			a0=299.36 + 0.70 sinN
			d0=43.46 - 0.51 cosN
			W=253.18 + 536.3128492d - 0.48 sinN 
			"""
			"a0_1": 299.36,
			"a0_2": 0.70,
			"d0_1": 43.46,
			"d0_2":	-0.51,
			"N_1": 357.85,
			"N_2": 52.316,
			"W_1": 253.18, 
			"W_2": 536.3128492,#0, # requires special treatment: 299.36 + 0.70 sin N where N=357.85 + 52.316*T, T= interval in Julian centuries (of 36525 days) from the standard epoch
			"W_3": -0.48,
			"W_C": 200
		},
		"drift_coef": {
			"a" : 30.06952752, 
			"ar": 0.00006447,
			"e" : 0.00895439,
			"er": 0.00000818,
			"i" : 1.77005520,
			"ir": 0.00022400,
			"L" : 304.22289287,
			"Lr": 218.46515314,
			"W" : 46.68158724,
			"Wr": 0.01009938,
			"N" : 131.78635853,
			"Nr": -0.00606302,
			"b" : -0.00041348,
			"c" : 0.68346318,
			"s" : -0.10162547,
			"f" : 7.67025000
		},
#		"tga_name":"Neptune",
		"tga_name":"source/2k_neptune-PM-normalized",
		"J2": 3536.3e-6		
	},

	"uranus" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Uranus",
		"symbol": u"\u26E2 ",
		"iau_name": "URANUS",
		"jpl_designation": "uranus",
		"mass":86.8e24,
		"radius":25362e3,
		"distance_to_periapsis":2741.30e9,
		"eccentricity_EC":0.04716771,
		"revolution_PR":30688.5,
		"rotation": -0.71833 * SOLAR_DAY_RATIO, # retrograde
		"orbital_inclination_IN":0.770,
		"longitude_of_ascendingnode_OM":74.22988,
		"longitude_of_periapsis_W":170.96424,
		"axial_tilt": 97.8,
		"absolute_mag": 0.0,
		"rotationalElts": {
			"W_1": 203.81, #257.311,
			"W_2": -501.1600928, #0,
			"W_C": 70
		},
		"drift_coef":{
			"a" : 19.18797948, 
			"ar": -0.00020455, 
			"e" : 0.04685740, 
			"er": -0.00001550, 
			"i" : 0.77298127, 
			"ir": -0.00180155, 
			"L" : 314.20276625, 
			"Lr": 428.49512595, 
			"W" : 172.43404441, 
			"Wr": 0.09266985, 
			"N": 73.96250215, 
			"Nr": 0.05739699, 
			"b" : 0.00058331, 
			"c" : -0.97731848, 
			"s" : 0.17689245, 
			"f" : 7.67025000
		},
		"tga_name": "Uranus",
		"J2": 3510.7e-6
	},

	"saturn" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Saturn",
		"symbol": u"\u2644 ",
		"iau_name": "SATURN",
		"jpl_designation": "saturn",
		"mass":568e24,
		"radius":58232e3,
		"distance_to_periapsis":1352.55e9,
		"eccentricity_EC":0.05415060,
		"revolution_PR":10759.22,
		"rotation":0.4407868753677 * SOLAR_DAY_RATIO,
		"orbital_inclination_IN":2.484,
		"longitude_of_ascendingnode_OM":113.71504,
		"longitude_of_periapsis_W":92.43194,
		"axial_tilt": 26.7,
		"absolute_mag": 0.0,
		
		"rotationalElts": {
			"a0_1": 40.589,
			"a0_2": -0.036,
			"d0_1": 83.537,
			"d0_2":	-0.004,
			"W_1": 38.90, #40.589,
			"W_2": 810.7939024, #-0.036,
			"W_C": -30

		},
		"drift_coef":{
			"a" : 9.54149883, 
			"ar": -0.00003065, 
			"e" : 0.05550825, 
			"er": -0.00032044, 
			"i" : 2.49424102, 
			"ir": 0.00451969, 
			"L" : 50.07571329, 
			"Lr": 1222.11494724, 
			"W" : 92.86136063, 
			"Wr": 0.54179478, 
			"N": 113.63998702, 
			"Nr": -0.25015002, 
			"b" : 0.00025899, 
			"c" : -0.13434469, 
			"s" : 0.87320147, 
			"f" : 38.35125
		},
		"tga_name": "Saturn",
		"J2": 16290.6e-6		
	},

	"jupiter" :{
		"type": TYPE_PLANET,
		"material":1,
		"name": "Jupiter",
		"symbol": u"\u2643 ",
		"iau_name": "JUPITER",
		"jpl_designation": "jupiter",
		"mass":1898e24,
		"radius":69911e3,
		"distance_to_periapsis":740.52e9,
		"eccentricity_EC":0.04839266,
		"revolution_PR":11.862 * 365.25,
		"rotation": 0.4146722375876 * SOLAR_DAY_RATIO,
		"orbital_inclination_IN":1.305,
		"longitude_of_ascendingnode_OM":100.55615,
		"longitude_of_periapsis_W":14.75385,
		"axial_tilt": 3.1,
		"absolute_mag": 0.0,
		"rotationalElts": {
			"W_1": 284.95,
			"W_2": 870.5360000,
			"W_C": 0
		},
		"drift_coef":{
			'a' : 5.20248019, 
			'ar': -0.00002864, 
			"e" : 0.04853590, 
			"er": 0.00018026, 
			"i" : 1.29861416, 
			"ir": -0.00322699, 
			"L" : 34.33479152, 
			"Lr": 3034.90371757, 
			"W" : 14.27495244, 
			"Wr": 0.18199196, 
			"N": 100.29282654, 
			"Nr": 0.13024619, 
			"b" : -0.00012452, 
			"c" : 0.06064060, 
			"s" : -0.35635438, 
			"f" : 38.35125
		},
		#"tga_name": "Jupiter",
		"tga_name": "source/2k_jupiter-PM-normalized",
		"J2": 14696.5e-6
	},

	"mars" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Mars",
		"symbol": u"\u2642 ",
		"iau_name": "MARS",
		"jpl_designation": "mars",
		"mass":0.642e24,
		"radius":3389e3,
		"distance_to_periapsis":206.62e9,
		"eccentricity_EC":0.09341233,
		"revolution_PR":686.98,
		"rotation": 1.027806363417 * SOLAR_DAY_RATIO,
		"orbital_inclination_IN":1.851,
		"longitude_of_ascendingnode_OM":49.57854,
		"longitude_of_periapsis_W":336.04084,
		"axial_tilt": 25.2,
		"absolute_mag": 0.0,
		"rotationalElts": {
			"a0_1": 317.68143,
			"a0_2": -0.1061,
			"d0_1": 52.88650,
			"d0_2": -0.0609,
			"W_1": 176.630, #317.681,
			"W_2": 350.89198226, #-0.106,
			"W_C": 0
		},
		"drift_coef":{
			'a' : 1.52371243, 
			'ar': 9.7e-07, 
			'e' : 0.09336511, 
			'er':9.149e-05, 
			'i' :1.85181869, 
			'ir':-0.00724757, 
			'L' :-4.56813164, 
			'Lr':19140.2993424, 
			'W' :-23.91744784, 
			'Wr':0.45223625, 
			'N' :49.71320984, 
			'Nr':-0.26852431, 
			'b' :0.0, 
			'c' :0.0, 
			's' :0.0, 
			'f' :0.0
		},

		"tga_name": "Mars",
#		"tga_name": "source/2k_mars-PM-normalized",
		"J2": 1956.6e-6
	},

	"mercury" :{
		"type": TYPE_PLANET,
		"material":1,
		"name": "Mercury",
		"symbol": u"\u263F ",
		"iau_name": "MERCURY",
		"jpl_designation": "mercury",
		"mass":0.330e24,
		"radius":2439e3,
		"distance_to_periapsis":46.0e9,
		"eccentricity_EC":0.20563069,
		"revolution_PR":87.969,
		"rotation": 58.81057874574 * SOLAR_DAY_RATIO,
		"orbital_inclination_IN":7.005,
		"longitude_of_ascendingnode_OM":48.33167,
		"longitude_of_periapsis_W":77.45645,
		"axial_tilt": 0.034,
		"absolute_mag": 0.0,
		"rotationalElts": {
			"W_1": 281.010,
			"W_2": -0.033,
			"W_C": 0
		},
		"drift_coef":{
			'a' : 0.38709843, 
			'ar': 0.0, 
			'e' : 0.20563661, 
			'er':0.00002123, 
			'i' :7.00559432, 
			'ir':-0.00590158, 
			'L' :252.25166724, 
			'Lr':149472.674866, 
			'W' :77.45771895, 
			'Wr':0.15940013, 
			'N' :48.33961819, 
			'Nr':-0.12214182, 
			'b' :0.0, 
			'c' :0.0, 
			's' :0.0, 
			'f' :0.0
		},
		"tga_name": "Mercury",
		"J2": 0
	},

	"venus" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Venus",
		"symbol": u"\u2640 ",
		"iau_name": "VENUS",
		"jpl_designation": "venus",
		"mass":4.87e24,
		"radius":6052e3,
		"distance_to_periapsis":107.48e9,
		"eccentricity_EC":0.00677323,
		"revolution_PR":224.701,
		"rotation": -243.6862038466 * SOLAR_DAY_RATIO, # retrograde
		"orbital_inclination_IN":3.3947,
		"longitude_of_ascendingnode_OM":76.68069,
		"longitude_of_periapsis_W":131.53298,
		"axial_tilt": 177.4,
		"absolute_mag": 0.0,
		"rotationalElts": {
			"a0": 272.76,
			"d0": 67.16,
			"W_1": 160.20, #272.76,
			"W_2": -1.4813688, #0,
			"W_C": 0
		},
		"drift_coef":{
			'a' : 0.72332102, 
			'ar': -2.6e-07, 
			'e' : 0.00676399, 
			'er':-5.107e-05, 
			'i' :3.39777545, 
			'ir':0.00043494, 
			'L' :181.9797085, 
			'Lr':58517.8156026, 
			'W' :131.76755713, 
			'Wr':0.05679648, 
			'N' :76.67261496, 
			'Nr':-0.27274174, 
			'b' :0.0, 
			'c' :0.0, 
			's' :0.0, 
			'f' :0.0
		},

		#"drift_coef_1":{'a' : 0.72333566, 'ar':0.00000390, 'eccentricity_EC' : 0.00677672, 'er':-0.00004107, 'i' :3.39467605, 'ir':-0.00078890, 'L' :181.97909950, 'Lr':58517.81538729, 'W' :131.60246718, 'Wr':0.00268329, 'N' :76.67984255, 'Nr':-0.27769418, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
		"tga_name": "Venus",
		"J2": 0
	},

	"earth" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Earth",
		"symbol": u"\u2641 ",
		"iau_name": "EARTH",
		"jpl_designation": EARTH_NAME,
		"mass":5.972e24,
		"radius":6371e3,
		"distance_to_periapsis":147.09e9,
		"eccentricity_EC":0.01671022,
		"revolution_PR": EARTH_PERIOD, #365.256,
		"rotation": 1 * SOLAR_DAY_RATIO,	# = 0.99726956597222 expressed in mean solar day
		"orbital_inclination_IN":0,
		"longitude_of_ascendingnode_OM":-11.26064,
		"longitude_of_periapsis_W":102.94719,
		"axial_tilt": 23.4,
		"absolute_mag": 0.0,
		"drift_coef":{
			'a' : 1.00000018, 
			'ar': -3e-08, 
			'e' : 0.01673163, 
			'er':-3.661e-05, 
			'i' :-0.00054346, 
			'ir':-0.01337178, 
			'L' :100.46691572, 
			'Lr':35999.3730633, 
			'W' :102.93005885, 
			'Wr':0.3179526, 
			'N' :-5.11260389, 
			'Nr':-0.24123856, 
			'b' :0.0, 
			'c' :0.0, 
			's' :0.0, 
			'f' :0.0
		},
	
		#"drift_coef_1":{'a' : 1.00000261, 'ar': 0.00000562, 'eccentricity_EC' : 0.01671123, 'er':-0.00004392, 'i' :-0.00001531, 'ir':-0.01294668, 'L' :100.46457166, 'Lr':35999.37244981, 'W' :102.93768193, 'Wr':0.32327364, 'N' :0.0, 'Nr':0.0, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
		"tga_name": "highres-earth-8192x4096-clouds", #"EarthClouds"
#		"tga_name": "source/4k-earth-with-clouds-PM-normalized",
#		"tga_name": "source/2k_earth_daymap-PM-normalized",
		#"tga_name": "land_shallow_topo_16384x8192"
		"J2": 9.01e-4
	},

	"pluto" : {
		"type": TYPE_DWARF_PLANET,
		"material":1,
		"name": "Pluto",
		"symbol": u"\u2647 ",
		"iau_name": "PLUTO",
		"jpl_designation": "pluto",
		"mass":0.0146e24,
		"radius":1195e3,
		"distance_to_periapsis":4436.82e+9,
		"eccentricity_EC":0.24880766,
		"revolution_PR":90560,
		"rotation": -6.404988435438 * SOLAR_DAY_RATIO, # retrograde
		"orbital_inclination_IN":17.142,
		"longitude_of_ascendingnode_OM":110.30347,
		"longitude_of_periapsis_W":224.06676,
		"axial_tilt": 122.5,
		"absolute_mag": -0.7,
		"rotationalElts": {
			"W_1": 132.99,
			"W_2": 0,
			"W_C": 0
		},
		"drift_coef":{
			'a' : 39.48686035, 
			'ar': 0.00449751, 
			'e' : 0.24885238, 
			'er':6.016e-05, 
			'i' :17.1410426, 
			'ir':5.01e-06, 
			'L' :238.96535011, 
			'Lr':145.18042903, 
			'W' :224.09702598, 
			'Wr':-0.00968827, 
			'N' :110.30167986, 
			'Nr':-0.00809981, 
			'b' :-0.01262724, 
			'c' :0.0, 
			's' :0.0, 
			'f' :0.0
		},
		#"drift_coef_1":{'a' : 39.48211675, 'ar':-0.00031596, 'eccentricity_EC' : 0.24882730, 'er':0.00005170, 'i' :17.14001206, 'ir':0.00004818, 'L' :238.92903833, 'Lr':145.20780515, 'W' :224.06891629, 'Wr':-0.04062942, 'N' :110.30393684, 'Nr':-0.01183482, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
		"tga_name": "Pluto3",
		"J2": 9.01e-4

	},

	"eris" : {
		"type": TYPE_DWARF_PLANET,
		"material":1,
		"name": "Eris",
#		"symbol": u'\u2BF0',		
		"iau_name": "ERIS",
		#"jpl_designation": 136199,
		"jpl_designation": "eris",
		"mass":1.66e22,
		"radius":1163e3,
		"distance_to_periapsis":5.723e12,
		"eccentricity_EC":0.4417142619088136,
		"revolution_PR": 203830,
		"rotation": 1.082121333841 * SOLAR_DAY_RATIO,
		"orbital_inclination_IN":44.0445,
		"longitude_of_ascendingnode_OM": 35.87791199490014,
		"longitude_of_periapsis_W":186.9301,

		"jd_time_of_periapsis_passage_Tp": 2545575.799683113451,
		"mean_motion_N":.001771354370292503, # in deg/day
		"epochJD": 2458000.5,
		"mean_anomaly_MA": 204.8731101766414,
		"orbit_class" : "TNO",
		"absolute_mag": -1.17,
		"axial_tilt": 0,
		"tga_name": "Eris"
		},

	"makemake":{
		"type": TYPE_DWARF_PLANET,
		"material":1,
		"name": "Makemake",
#		"symbol": u'\U0001F77C',
		"iau_name": "MAKEMAKE",
		#"jpl_designation": 136472,
		"jpl_designation": "makemake",
		"mass":4.4e21,
		"radius":739e3,
		"distance_to_periapsis":5.77298e12,
		"eccentricity_EC":.154682767507142,
		"revolution_PR": 112897.9710682497,
		"rotation": 0.3246781808988 * SOLAR_DAY_RATIO,
		"orbital_inclination_IN":29.00685,
		"longitude_of_ascendingnode_OM": 79.3659,
		"longitude_of_periapsis_W":376.6059,

		"jd_time_of_periapsis_passage_Tp": 2407499.827534289027,
		"mean_motion_N":.003188719837864677, # in deg/day
		"epochJD": 2458000.5,
		"mean_anomaly_MA": 161.032496116919,
		"orbit_class" : "TNO",
		"absolute_mag": -0.3,
		"axial_tilt": 0,
		"tga_name": "Makemake"
		},

	"sedna":   {
		"type": TYPE_DWARF_PLANET,
		"material":1,
		"name": "Sedna",
#		"symbol": u"\u2BF2",
		"iau_name": "SEDNA",
		#"jpl_designation": 90377,
		"jpl_designation": "sedna",
		"mass":4.4e21, # mass is undetermined
		"radius":995e3,
		"distance_to_periapsis":1.1423e13,
		"eccentricity_EC":0.85491,
		"revolution_PR": 3934726.687924069,
		"rotation": 0.4303416887476 * SOLAR_DAY_RATIO,
		"orbital_inclination_IN":11.92872,
		"longitude_of_ascendingnode_OM":144.546,
		"longitude_of_periapsis_W":455.836,

		"jd_time_of_periapsis_passage_Tp": 2479566.507375652123,
		"mean_motion_N":9.149301299753888e-5,  # in deg/day
		"epochJD": 2458000.5,
		"mean_anomaly_MA": 358.0268610068745,
		"orbit_class" : "TNO",
		"absolute_mag": 1.83,
		"axial_tilt": 0,
		"tga_name": "Sedna"

		},

	"haumea":  {
		"type": TYPE_DWARF_PLANET,
		"material":1,
		"name": "Haumea",
#		"symbol": u'\U0001F77B',
		"iau_name": "HAUMEA",
		#"jpl_designation": 136108,
		"jpl_designation": "haumea",
		"mass":4.006e21,
		"radius":620e3,
		"distance_to_periapsis":35.14529440338772*AU,
		"eccentricity_EC":0.1893662787361186,
		"revolution_PR": 104270.6801862633,
		"rotation": 0.163146 * SOLAR_DAY_RATIO,
		"orbital_inclination_IN":28.20363151617822,
		"longitude_of_ascendingnode_OM":121.9702799705751,
		"longitude_of_periapsis_W":360.8407349965672,

		"jd_time_of_periapsis_passage_Tp": 2500269.703252029540,
		"mean_motion_N":0.003452552523460249, # in deg/day
		"epochJD": 2458000.5,
		"mean_anomaly_MA": 214.0633556475513,
		"orbit_class" : "TNO",
		"absolute_mag": 0.2,
		"axial_tilt": 0,
		"tga_name": "Haumea"
		},

}

belt_data = {
	"jupitertrojans": {
		"radius_min":5.05,
		"radius_max":5.65, #5.35,
		"thickness": 0.6,
		"thickness_factor":15.e4},
	"asteroid":	{
		"radius_min":2.06,
		"radius_max":3.27,
		"thickness": 0,
		"thickness_factor":5.e4},
	"kuiper":   {
		"radius_min":30,
		"radius_max":50,
		"thickness": 10,
		"thickness_factor":1.e6},
	"inneroort":	{
		"radius_min":2000,
		"radius_max":20000,
		"thickness": 0,
		"thickness_factor":1.e9},
}

"""
		"radius":58232e3,
		"distance_to_periapsis":1352.55e9,
		"eccentricity_EC":0.05415060,
		"revolution_PR":10759.22,
		"rotation":0.4407868753677,

		SATURN
Name(1)	Distance from Saturn's
            center (km)				Width (km)		Thickness

D ring 		66,900  -  74,510		7,500	 	
C Ring 		74,658  -   92,000		17,500
B Ring		92,000  -  117,580		25,500	 	*
A ring		122,170 -   136,775		14,600	 	*
F Ring		140,180 (3)				30 - 500	* 
G Ring		166,000  -  175,000		9,000	 
E Ring		180,000 - 480,000		300,000	 

		URANUS

Mu			86 000 - 103 000		17000				0.14			
Nu			66 100 - 69 900			3800				0.012
Tau			37 850 - 41 350			3500				1
"""
rings_data = {
	"neptune": {
		"rings":[
			{	"name"		: "Galle",
				"radius"	: 41000e3,
				"width"		: 2000e3,
				"color"		: Color.darkgrey,
				"opacity"	: 1.0
			},
			{	"name"		: "LeVerrier",
				"radius"	: 53200e3,
				"width"		: 113e3,
				"color"		: Color.grey,
				"opacity"	: 1.0
			},
			{	"name"		: "Lassell",
				"radius"	: 55000e3,
				"width"		: 4000e3,
				"color"		: Color.darkgrey, #Color.blueish,
				"opacity"	: 0.9
			},
			{	"name"		: "Arago",
				"radius"	: 57200e3,
				"width"		: 100e3,
				"color"		: Color.darkgrey, #Color.blueish,
				"opacity"	: 0.8
			},
			{	"name"		: "Adams",
				"radius"	: 62932e3,
				"width"		: 50e3,
				"color"		: Color.grey, #Color.blueish,
				"opacity"	: 0.2
			}
		]
	},
	"uranus": {
		"rings":[
			{	"name"		: "cos-1",
				"radius"	: 103000e3,
				"width"		: 50e3,
				"color"		: Color.grey, #Color.blueish,
				"opacity"	: 1.0
			},
			{	"name"		: "Mu",
				"radius"	: 102950e3,
				"width"		: 17000e3,
				"color"		: Color.darkgrey,
				"opacity"	: 0.6
			},
			{	"name"		: "Nu",
				"radius"	: 69900e3,
				"width"		: 3800e3,
				"color"		: Color.darkgrey,
				"opacity"	: 0.3
			},
			{	"name"		: "cos-2",
				"radius"	: 41350e3,
				"width"		: 50e3,
				"color"		: Color.grey, #Color.blueish,
				"opacity"	: 0.4
			},
			{	"name"		: "Tau",
				"radius"	: 41300e3,
				"width"		: 3500e3,
				"color"		: Color.darkgrey, #Color.blueish,
				"opacity"	: 0.2
			}
		]
	},
	"saturn": {
		"rings": [
			{	"name"		: "F",
				"radius"	: 140180e3,
				"width"		:100e3,
				"color"		: Color.whiteish,
				"opacity"	: 1.0
			},
			{	"name"		: "A",
				"radius"	: 136775e3,
				"width"		: 14600e3,
				"color"		: Color.lightgrey,
				"opacity"	: 1.0
			},
			{	"name"		: "B",
				"radius"	: 117580e3,
				"width"		: 25300e3, #25500e3,
				"color"		: Color.whiteish,
				"opacity"	: 1.0
			},
			{	"name"		: "C",
				"radius"	: 92000e3,
				"width"		: 17200e3, #17500e3,
				"color"		: Color.grey,
				"opacity"	: 1.0
			},
			{	"name"		: "D",
				"radius"	: 74510e3,
				"width"		: 7500e3,
				"color"		: Color.deepgrey,
				"opacity"	: 1.0
			}		
		]
	}
}

europa_omega_dot = -0.025 # degrees / day

"""

2. Architectural pattern for any regular moon
For each regular moon:

- Collect constants (once):
- planet equatorial radius R
- planet J_2
- moon’s a,e,i (planet‐centric, planet‐equator frame)
- moon’s period P → n=2.pi/P

- Compute:

- p=a(1-e^2)
- Omega_dot = -3/2 *n*J_2(R^2/p^2)*cos i
- Freeze those into a DriftModel for that moon:
- a,e,i: constants
- Omega _0,omega _0,M_0: from a reference epoch (e.g. J2000)
- Omega _dot : from the formula above
- omega _dot : optional, from the analogous J2 formula if you want

- Use in your ephemeris:
- dT= JD - JD_0 (days since reference epoch)
- Omega (t) = Omega _0 + Omega _dot * dT
- omega (t) = omega _0 + omega _dot * dT (if used)
- M(t) = M_0 + n*dT

This is identical to what we did conceptually for Europa; you just plug in the appropriate constants per moon.



1. The J_2 formula for omega_dot
For a point mass orbiting an oblate primary with J_2, the secular periapsis precession rate is:
omega_dot = 3/4 * n * J_2 * (R^2/p^2) * (5 * cos ^2(i) -1) 

Side‑by‑side with Omega_dot:
Omega_dot  = -3/2 *n*J_2(R^2/p^2)*cos i

So the pair you want is:
- Node regression:
Omega_dot  = -3/2 *n*J_2(R^2/p^2)*cos i
- Periapsis precession:
omega_dot = 3/4 * n * J_2 * (R^2/p^2) * (5 * cos ^2(i) -1)

This is the standard textbook result (e.g., Vallado, Bate, Curtis, etc.) for a J_2‑only perturbation, averaged over an orbit.

2. How to implement this in your DriftModel
Given:
- planet constants: R,J_2,GM_planet
- moon’s elements: a,e,i (in planet‑equator frame)
- moon’s period P or mean motion n

You do:

- Compute mean motion (if not already given):
n = 2 * pi/P  or n = sqrt(mu/a^3) 

- Compute semi‑latus rectum:
p = a(1-e^2)

- Compute:
Omega_dot  = -3/2 *n*J_2(R^2/p^2)*cos i 
omega_dot = 3/4 * n * J_2 * (R^2/p^2) * (5 * cos ^2(i) -1)

- Plug into your DriftModel:
Omega = Omega0 + Omega_dot * dT
omega = omega0 + omega_dot * dT
M     = M0     + n        * dT



3. A couple of practical notes
- For regular moons:
- e is small → p ~ a
- i is small → cos i ~ 1, cos ^2i ~ 1

- So you often get:
- Omega_dot ~ - 3/2 * n * J_2 * (R/a)^2
- omega_dot ~ 3/4 * n * J_2 * (R/a)^2 * (5-1) = 3 * n * J_2*(R/a)^2

- Signs:
- Omega_dot is usually negative (node regresses).
- omega_dot can be positive or negative depending on i; for small i, it’s typically positive (prograde periapsis precession).
- Frame:
- These formulas assume i is measured w.r.t. the planet’s equatorial plane, not ecliptic.
"""