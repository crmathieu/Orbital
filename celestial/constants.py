# constants.py

J2000_EPOCH = 2451545.0
AU = 149597870700.0


SUN_M = 1.989e+30 # in Kg
SUN_R = 6.957e8 # in m

G_universal = 6.67384e-11	# Universal gravitational constant
SUN_Mu = G_universal * SUN_M

ERR_NOERR 				 	= 0
ERR_CANTFIND_BLOCKMARKER 	= 1
ERR_CANTPARSE_STATEVECTOR 	= 2


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


# Body types
INNER_PLANET 		= 0x01
OUTER_PLANET 		= 0x02
MOON 				= 0x04
SPACECRAFT 			= 0x08
ASTEROID 			= 0x10
GAS_GIANT 			= 0x20
DWARF_PLANET 		= 0x40
TNO 				= 0x80
COMET 				= 0x100

SMALL_ASTEROID 		= 0x200
BIG_ASTEROID 		= 0x400
PHA 				= 0x800
ASTEROID_BELT 		= 0x1000
KUIPER_BELT 		= 0x2000
INNER_OORT_CLOUD 	= 0x4000
ECLIPTIC_PLANE 		= 0x8000

LIT_SCENE 			= 0x10000
REFERENTIAL 		= 0x20000
ORBITS 				= 0x40000
LABELS 				= 0x80000

JTROJANS 			= 0x100000
REALSIZE 			= 0x200000
LOCAL_REFERENTIAL 	= 0x400000
CELESTIAL_SPHERE 	= 0x800000
HYPERBOLIC 			= 0x1000000
CONSTELLATIONS 		= 0x2000000
SUN 				= 0x4000000
SMALL_MOON			= 0x8000000
TINY_MOON  			= 0x10000000

TYPE_MASK = 0xFFFFFFF

# texture:
DEFAULT_TEXTURE = "./img/asteroid"
