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
INNERPLANET = 0x01
OUTERPLANET = 0x02
DWARFPLANET = 0x04
ASTEROID = 0x08
COMET = 0x10
SMALL_ASTEROID = 0x20
BIG_ASTEROID = 0x40
PHA = 0x80
ASTEROID_BELT = 0x100
KUIPER_BELT = 0x200
INNER_OORT_CLOUD = 0x400
ECLIPTIC_PLANE = 0x800
LIT_SCENE = 0x1000
REFERENTIAL = 0x2000
ORBITS = 0x4000
GASGIANT = 0x8000
TRANS_NEPT = 0x10000
LABELS = 0x20000
JTROJANS = 0x40000
REALSIZE = 0x80000
LOCAL_REFERENTIAL = 0x100000
SATELLITE = 0x200000
CELESTIAL_SPHERE = 0x400000
HYPERBOLIC = 0x800000
SPACECRAFT = 0x1000000
CONSTELLATIONS = 0x2000000

TYPE_MASK = 0xFFFFFFF


SATELLITE_M = 100
THREE_D = False
MAX_P_D = 1.1423e13
MIN_P_D = 46.0e9

LEGEND = True

SUN_M = 1.989e+30 # in Kg
SUN_R = 696e+3 # in km
G = 6.67384e-11	# Universal gravitational constant
Mu = G * SUN_M
DIST_FACTOR = 10e-7

# EPOCH constants
#EPOCH_2000_JD = 2451544.5	# number of days ellapsed from 01-01-4713 BC GMT to 01-01-2000 AD GMT
EPOCH_2000_JD = 2451545.0	# number of days ellapsed from 01-01-4713 BC GMT to 01-01-2000 AD @ 12pm GMT
EPOCH_2000_MJD = 51544.0
EPOCH_1970_JD = 2440587.5 # number of days ellapsed from 01-01-4713 BC GMT to 01-01-1970 AD GMT

#X_COOR = 0
#Y_COOR = 1
#Z_COOR = 2

TYPE_STAR = 0
TYPE_PLANET = 1
TYPE_ASTEROID = 2
TYPE_DWARF_PLANET = 3
TYPE_COMET = 4
TYPE_TRANS_N = 5
TYPE_SATELLITE = 6

CURRENT_BODY = "current_body"
EARTH_NAME = "earth"
SUN_NAME = "sun"

index_to_bodyname = {
	0: CURRENT_BODY, 	1: SUN_NAME, 	2: EARTH_NAME,	3: "mercury", 	4:"venus",		
	5:"mars", 			6:"jupiter",	7:"saturn", 	8:"uranus", 	9:"neptune",
	10:"pluto", 		11:"sedna",		12:"makemake", 	13:"haumea", 	14:"eris", 
	15:"charon",		16:"phobos",	17:"deimos", 	18:"moon"
}

bodyname_to_index = {
	index_to_bodyname[0]: 0, 	index_to_bodyname[1]: 1, 	index_to_bodyname[2]: 2, 	index_to_bodyname[3]: 3, 	
	index_to_bodyname[4]: 4,	index_to_bodyname[5]: 5, 	index_to_bodyname[6]: 6, 	index_to_bodyname[7]: 7, 	
	index_to_bodyname[8]: 8, 	index_to_bodyname[9]: 9,	index_to_bodyname[10]: 10, 	index_to_bodyname[11]: 11, 	
	index_to_bodyname[12]: 12, 	index_to_bodyname[13]: 13, 	index_to_bodyname[14]: 14, 	index_to_bodyname[15]: 15, 		
	index_to_bodyname[16]: 16, 	index_to_bodyname[17]: 17, 	index_to_bodyname[18]: 18
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

# time increments in day unit

TI_ONE_SECOND 	= 1.157407e-5			# 1d -> 86400 sec => 1sec = 1/86400 day
TI_10_SECONDS 	= TI_ONE_SECOND * 10
TI_30_SECONDS 	= TI_ONE_SECOND * 30
TI_ONE_MINUTE 	= TI_ONE_SECOND * 60
TI_FIVE_MINUTES = TI_ONE_MINUTE * 5 
TI_TEN_MINUTES 	= TI_ONE_MINUTE * 10 
TI_ONE_HOUR 	= 0.0416666666
TI_SIX_HOURS 	= 0.25
TI_TWELVE_HOURS = 0.5
TI_24_HOURS 	= 1


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

# scale toggling
SCALE_OVERSIZED = 0
SCALE_NORMALIZED = 1

# size corrections...
SMALLBODY_SZ_CORRECTION = 1e-6/(DIST_FACTOR*5) #(default)
#SMALLBODY_SZ_CORRECTION = 5e-5/(DIST_FACTOR * 5) #(default)

SUN_SZ_CORRECTION = 1e-2/(DIST_FACTOR * 20)
PLANET_SZ_CORRECTION = 1/(DIST_FACTOR * 5)
SATELLITE_SZ_CORRECTION = 1/(DIST_FACTOR * 5)
HYPERBOLIC_SZ_CORRECTION = 1/(DIST_FACTOR * 5)
### ASTEROID_SZ_CORRECTION = 1e-2/(DIST_FACTOR * 5)
ASTEROID_SZ_CORRECTION = SMALLBODY_SZ_CORRECTION
DWARFPLANET_SZ_CORRECTION = 1e-2/(DIST_FACTOR * 5)

# adjustment factor
#Adjustment_cte = 1.85
ADJUSTMENT_FACTOR_PLANETS = 0 # 1.95
ADJUSTMENT_FACTOR = 0 #1.72 #1.80

#from visual import color
from vpython_interface import Color

objects_data = {
	"moon" :{
		"type": TYPE_SATELLITE,
		"material":1,
		"name": "Moon",
		"iau_name": "Moon",
		"jpl_designation": "moon",
		"mass": 7.342e+22,
		"radius": 1738.1e+3,
		"QR_perihelion":0.00237529455014751*AU,
		"aphelion":0.00270352798850*AU,
		"EC_e":6.462786125327587e-02,
		"PR_revolution":27.321582,
		"rotation":27.321582, # in days
		"IN_orbital_inclination":5.27749841723057, #+23.44, # to earth eq.
		"OM_longitude_of_ascendingnode":143.9091328687446,
		"longitude_of_perihelion":296.9775666926365+143.9091328687446,
		"MA_mean_anomaly": 158.3907159645461,
		"N_mean_motion":13.42988221368860,
		"epochJD": 2457994.50,
		"Tp_Time_of_perihelion_passage_JD": 2457982.706097905825,

		"axial_tilt": 6.67, # to its own orbital plane1.263=
		"absolute_mag": 0.0,
		"orbit_class": "E-SAT",
		"tga_name": "Moon"
		},
	"phobos" :{
		"type": TYPE_SATELLITE,
		"material":0,
		"name": "Phobos",
		"iau_name": "Phobos",
		"jpl_designation": "phobos",
		"mass": 1.1e+16,
		"radius": 15*11.1e+3,
		"QR_perihelion":4*9.236397056433352E+06, #4*9234.42e+3,
		"aphelion":4*9.519289172301515E+06, #4*9517.58e+3,
		"EC_e":1.508300535731693E-02,
		"PR_revolution":0.3191794301882109,
		"rotation":0.3191794301882109, # in days
		"IN_orbital_inclination":2.566118935798619E+01, # to ecliptic, #1.093, # to mars eq #
		"OM_longitude_of_ascendingnode":8.223772856123789E+01,
		"longitude_of_perihelion":2.762475522960488E+02+8.223772856123789E+01,
		"MA_mean_anomaly": 8.524147919084433E+01,
		"N_mean_motion":1.128100327597539E+03,
		"epochJD": 2458001.50,
		"Tp_Time_of_perihelion_passage_JD": -0.075561966525,

		"axial_tilt": 0.046, # to its own orbital plane
		"absolute_mag": 0.0,
		"orbit_class": "M-SAT",
		"tga_name": "Phobos"
		},
	"deimos" :{
		"type": TYPE_SATELLITE,
		"material":0,
		"name": "Deimos",
		"iau_name": "Deimos",
		"jpl_designation": "deimos",
		"mass": 1.4762e+15,
		"radius": 15*6.2e+3,
		"QR_perihelion":4*2.345311353009123E+07, #4*23455.5e+3,
		"aphelion":4*2.346540189020549E+07, #4*23470.9e+3,
		"EC_e":2.619085451484923E-04,
		"PR_revolution":1.262540567604984,
		"rotation":1.262540567604984, # in days
		"IN_orbital_inclination":2.544419693842261E+01, # to ecliptic, 0.93, # to mars eq. #
		"OM_longitude_of_ascendingnode":7.875346643344125E+01,
		"longitude_of_perihelion":3.353099851925172E+02+7.875346643344125E+01,
		"MA_mean_anomaly": 3.541134423740633E+02,
		"N_mean_motion":2.851220253841971E+02,
		"epochJD": 2458001.50,
		"Tp_Time_of_perihelion_passage_JD": 0.020645748493,

		"axial_tilt": 0.897, # to its own orbital plane
		"absolute_mag": 0.0,
		"orbit_class": "M-SAT",
		"tga_name": "Deimos"
		},
	"charon" :{
		"type": TYPE_SATELLITE,
		"material":0,
		"name": "Charon",
		"iau_name": "Charon",
		"jpl_designation": "charon",
		"mass": 1.586e+21,
		"radius": 15*606e+3,
		"QR_perihelion":100*1.959394328352395E+07, # 19596e+3, we multiply by 100 since pluto is bigger than it should
		"aphelion":100*1.959976480409748E+07, # 19596e+3, we multiply by 100 since pluto is bigger than it should
		"EC_e":1.485320184688916E-04,
		"PR_revolution":6.387221715378253,
		"rotation":6.387221715378253, # in days
		"IN_orbital_inclination":1.128960563495295E+02, # to ecliptic
		"OM_longitude_of_ascendingnode":2.274019157345203E+02,
		"longitude_of_perihelion":1.895323185981683E+02+2.274019157345203E+02,
		"MA_mean_anomaly": 7.639225900405658E+01,
		"N_mean_motion":5.636253382800892E+01,
		"epochJD": 2458001.50,
		"Tp_Time_of_perihelion_passage_JD": -1.355373043326,

		"axial_tilt": 0, # to its own orbital plane
		"absolute_mag": 1.0,
		"orbit_class": "M-SAT",
		"tga_name": "Charon"
		},

	"sun" :{
		"type": TYPE_STAR,
		"material":1,
		"name": "Sun",
		"iau_name": "SUN",
		"jpl_designation": "sun",
		"mass":1.98855e+30,
		"radius":3.47850e+8,
		"QR_perihelion":0,
		"EC_e":0,
		"PR_revolution":0,
		"rotation":25.38,
		"IN_orbital_inclination":67.23, # to the galactic plane
		"OM_longitude_of_ascendingnode":0,
		"longitude_of_perihelion":0,
		"axial_tilt": 7.25,
		"absolute_mag": 0.0,
		"tga_name": "Sun"

		},

	"neptune" :{
		"type": TYPE_PLANET,
		"material":1,
		"name": "Neptune",
		"iau_name": "NEPTUNE",
		"jpl_designation": "neptune",
		"mass":102e+24,
		"radius":24.622e+6,
		"QR_perihelion":4444.45e+9,
		"EC_e":0.00858587,
		"PR_revolution":60182,
		"rotation":0.6713,
		"IN_orbital_inclination":1.769,
		"OM_longitude_of_ascendingnode":131.72169,
		"longitude_of_perihelion":44.97135,
		"axial_tilt": 28.32,
		"absolute_mag": 0.0,
		"RA_1": 299.36,
		"RA_2": 0, # requires special treatment: 299.36 + 0.70 sin N where N=357.85 + 52.316*T, T=Julian century from epoch
		"kep_elt":{"a" : 30.06952752, "ar": 0.00006447,"EC_e" : 0.00895439,"er": 0.00000818,"i" : 1.77005520,"ir": 0.00022400,"L" : 304.22289287,"Lr": 218.46515314,"W" : 46.68158724,"Wr": 0.01009938,"N" : 131.78635853,"Nr": -0.00606302,"b" : -0.00041348,"c" : 0.68346318,"s" : -0.10162547,"f" : 7.67025000},
		"tga_name": "Neptune"
		},

	"uranus" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Uranus",
		"iau_name": "URANUS",
		"jpl_designation": "uranus",
		"mass":86.8e24,
		"radius":25362e3,
		"QR_perihelion":2741.30e9,
		"EC_e":0.04716771,
		"PR_revolution":30688.5,
		"rotation": -0.71833, # retrograde
		"IN_orbital_inclination":0.770,
		"OM_longitude_of_ascendingnode":74.22988,
		"longitude_of_perihelion":170.96424,
		"axial_tilt": 97.8,
		"absolute_mag": 0.0,
		"RA_1": 257.311,
		"RA_2": 0,
		"kep_elt":{"a" : 19.18797948, "ar": -0.00020455, "EC_e" : 0.04685740, "er": -0.00001550, "i" : 0.77298127, "ir": -0.00180155, "L" : 314.20276625, "Lr": 428.49512595, "W" : 172.43404441, "Wr": 0.09266985, "N": 73.96250215, "Nr": 0.05739699, "b" : 0.00058331, "c" : -0.97731848, "s" : 0.17689245, "f" : 7.67025000},
		"tga_name": "Uranus"
		},

	"saturn" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Saturn",
		"iau_name": "SATURN",
		"jpl_designation": "saturn",
		"mass":568e24,
		"radius":58232e3,
		"QR_perihelion":1352.55e9,
		"EC_e":0.05415060,
		"PR_revolution":10759.22,
		"rotation":0.4407868753677,
		"IN_orbital_inclination":2.484,
		"OM_longitude_of_ascendingnode":113.71504,
		"longitude_of_perihelion":92.43194,
		"axial_tilt": 26.7,
		"absolute_mag": 0.0,
		"RA_1": 40.589,
		"RA_2": -0.036,
		"kep_elt":{"a" : 9.54149883, "ar": -0.00003065, "EC_e" : 0.05550825, "er": -0.00032044, "i" : 2.49424102, "ir": 0.00451969, "L" : 50.07571329, "Lr": 1222.11494724, "W" : 92.86136063, "Wr": 0.54179478, "N": 113.63998702, "Nr": -0.25015002, "b" : 0.00025899, "c" : -0.13434469, "s" : 0.87320147, "f" : 38.35125},
		"tga_name": "Saturn"
		},

	"jupiter" :{
		"type": TYPE_PLANET,
		"material":1,
		"name": "Jupiter",
		"iau_name": "JUPITER",
		"jpl_designation": "jupiter",
		"mass":1898e24,
		"radius":69911e3,
		"QR_perihelion":740.52e9,
		"EC_e":0.04839266,
		"PR_revolution":11.862 * 365.25,
		"rotation": 0.4146722375876,
		"IN_orbital_inclination":1.305,
		"OM_longitude_of_ascendingnode":100.55615,
		"longitude_of_perihelion":14.75385,
		"axial_tilt": 3.1,
		"absolute_mag": 0.0,
		"RA_1": 268.057,
		"RA_2": -0.006,

		"kep_elt":{'a' : 5.20248019, 'ar': -0.00002864, "EC_e" : 0.04853590, "er": 0.00018026, "i" : 1.29861416, "ir": -0.00322699, "L" : 34.33479152, "Lr": 3034.90371757, "W" : 14.27495244, "Wr": 0.18199196, "N": 100.29282654, "Nr": 0.13024619, "b" : -0.00012452, "c" : 0.06064060, "s" : -0.35635438, "f" : 38.35125},
		"tga_name": "Jupiter"

		},

	"mars" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Mars",
		"iau_name": "MARS",
		"jpl_designation": "mars",
		"mass":0.642e24,
		"radius":3389e3,
		"QR_perihelion":206.62e9,
		"EC_e":0.09341233,
		"PR_revolution":686.98,
		"rotation": 1.027806363417,
		"IN_orbital_inclination":1.851,
		"OM_longitude_of_ascendingnode":49.57854,
		"longitude_of_perihelion":336.04084,
		"axial_tilt": 25.2,
		"absolute_mag": 0.0,
		"RA_1": 317.681,
		"RA_2": -0.106,

		"kep_elt":{'a' : 1.52371243, 'ar': 9.7e-07, 'EC_e' : 0.09336511, 'er':9.149e-05, 'i' :1.85181869, 'ir':-0.00724757, 'L' :-4.56813164, 'Lr':19140.2993424, 'W' :-23.91744784, 'Wr':0.45223625, 'N' :49.71320984, 'Nr':-0.26852431, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
		"tga_name": "Mars"
		},

	"mercury" :{
		"type": TYPE_PLANET,
		"material":1,
		"name": "Mercury",
		"iau_name": "MERCURY",
		"jpl_designation": "mercury",
		"mass":0.330e24,
		"radius":2439e3,
		"QR_perihelion":46.0e9,
		"EC_e":0.20563069,
		"PR_revolution":87.969,
		"rotation": 58.81057874574,
		"IN_orbital_inclination":7.005,
		"OM_longitude_of_ascendingnode":48.33167,
		"longitude_of_perihelion":77.45645,
		"axial_tilt": 0.034,
		"absolute_mag": 0.0,
		"RA_1": 281.010,
		"RA_2": -0.033,

		"kep_elt":{'a' : 0.38709843, 'ar': 0.0, 'EC_e' : 0.20563661, 'er':0.00002123, 'i' :7.00559432, 'ir':-0.00590158, 'L' :252.25166724, 'Lr':149472.674866, 'W' :77.45771895, 'Wr':0.15940013, 'N' :48.33961819, 'Nr':-0.12214182, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
		"tga_name": "Mercury"
		},

	"venus" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Venus",
		"iau_name": "VENUS",
		"jpl_designation": "venus",
		"mass":4.87e24,
		"radius":6052e3,
		"QR_perihelion":107.48e9,
		"EC_e":0.00677323,
		"PR_revolution":224.701,
		"rotation": -243.6862038466, # retrograde
		"IN_orbital_inclination":3.3947,
		"OM_longitude_of_ascendingnode":76.68069,
		"longitude_of_perihelion":131.53298,
		"axial_tilt": 177.4,
		"absolute_mag": 0.0,
		"RA_1": 272.76,
		"RA_2": 0,
		"kep_elt":{'a' : 0.72332102, 'ar': -2.6e-07, 'EC_e' : 0.00676399, 'er':-5.107e-05, 'i' :3.39777545, 'ir':0.00043494, 'L' :181.9797085, 'Lr':58517.8156026, 'W' :131.76755713, 'Wr':0.05679648, 'N' :76.67261496, 'Nr':-0.27274174, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
		#"kep_elt_1":{'a' : 0.72333566, 'ar':0.00000390, 'EC_e' : 0.00677672, 'er':-0.00004107, 'i' :3.39467605, 'ir':-0.00078890, 'L' :181.97909950, 'Lr':58517.81538729, 'W' :131.60246718, 'Wr':0.00268329, 'N' :76.67984255, 'Nr':-0.27769418, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
		"tga_name": "Venus"
		},

	"earth" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Earth",
		"iau_name": "EARTH",
		"jpl_designation": "earth",
		"mass":5.972e24,
		"radius":6371e3,
		"QR_perihelion":147.09e9,
		"EC_e":0.01671022,
		"PR_revolution":365.256,
		"rotation":	1,
		"IN_orbital_inclination":0,
		"OM_longitude_of_ascendingnode":-11.26064,
		"longitude_of_perihelion":102.94719,
		"axial_tilt": 23.4,
		"absolute_mag": 0.0,
		"RA_1": 0.00,
		"RA_2": -0.641,
		"kep_elt":{'a' : 1.00000018, 'ar': -3e-08, 'EC_e' : 0.01673163, 'er':-3.661e-05, 'i' :-0.00054346, 'ir':-0.01337178, 'L' :100.46691572, 'Lr':35999.3730633, 'W' :102.93005885, 'Wr':0.3179526, 'N' :-5.11260389, 'Nr':-0.24123856, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
		#"kep_elt_1":{'a' : 1.00000261, 'ar': 0.00000562, 'EC_e' : 0.01671123, 'er':-0.00004392, 'i' :-0.00001531, 'ir':-0.01294668, 'L' :100.46457166, 'Lr':35999.37244981, 'W' :102.93768193, 'Wr':0.32327364, 'N' :0.0, 'Nr':0.0, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
		"tga_name": "highres-earth-8192x4096-clouds" #"EarthClouds"
		#"tga_name": "land_shallow_topo_16384x8192"
		},

	"pluto" : {
		"type": TYPE_DWARF_PLANET,
		"material":1,
		"name": "Pluto",
		"iau_name": "PLUTO",
		"jpl_designation": "pluto",
		"mass":0.0146e24,
		"radius":1195e3,
		"QR_perihelion":4436.82e+9,
		"EC_e":0.24880766,
		"PR_revolution":90560,
		"rotation": -6.404988435438, # retrograde
		"IN_orbital_inclination":17.142,
		"OM_longitude_of_ascendingnode":110.30347,
		"longitude_of_perihelion":224.06676,
		"axial_tilt": 122.5,
		"absolute_mag": -0.7,
		"RA_1": 132.99,
		"RA_2": 0,
		"kep_elt":{'a' : 39.48686035, 'ar': 0.00449751, 'EC_e' : 0.24885238, 'er':6.016e-05, 'i' :17.1410426, 'ir':5.01e-06, 'L' :238.96535011, 'Lr':145.18042903, 'W' :224.09702598, 'Wr':-0.00968827, 'N' :110.30167986, 'Nr':-0.00809981, 'b' :-0.01262724, 'c' :0.0, 's':0.0, 'f' :0.0},
		#"kep_elt_1":{'a' : 39.48211675, 'ar':-0.00031596, 'EC_e' : 0.24882730, 'er':0.00005170, 'i' :17.14001206, 'ir':0.00004818, 'L' :238.92903833, 'Lr':145.20780515, 'W' :224.06891629, 'Wr':-0.04062942, 'N' :110.30393684, 'Nr':-0.01183482, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
		"tga_name": "Pluto"
#		"tga_name": "highres-earth-8192x4096-clouds" #"EarthClouds"

		},

	"eris" : {
		"type": TYPE_DWARF_PLANET,
		"material":1,
		"name": "Eris",
		"iau_name": "ERIS",
		#"jpl_designation": 136199,
		"jpl_designation": "eris",
		"mass":1.66e22,
		"radius":1163e3,
		"QR_perihelion":5.723e12,
		"EC_e":0.4417142619088136,
		"PR_revolution": 203830,
		"rotation": 1.082121333841,
		"IN_orbital_inclination":44.0445,
		"OM_longitude_of_ascendingnode": 35.87791199490014,
		"longitude_of_perihelion":186.9301,

		"Tp_Time_of_perihelion_passage_JD": 2545575.799683113451,
		"N_mean_motion":.001771354370292503,
		"epochJD": 2458000.5,
		"MA_mean_anomaly": 204.8731101766414,
		"orbit_class" : "TNO",
		"absolute_mag": -1.17,
		"axial_tilt": 0,
		"tga_name": "Eris"
		},

	"makemake":{
		"type": TYPE_DWARF_PLANET,
		"material":1,
		"name": "Makemake",
		"iau_name": "MAKEMAKE",
		#"jpl_designation": 136472,
		"jpl_designation": "makemake",
		"mass":4.4e21,
		"radius":739e3,
		"QR_perihelion":5.77298e12,
		"EC_e":.154682767507142,
		"PR_revolution": 112897.9710682497,
		"rotation": 0.3246781808988,
		"IN_orbital_inclination":29.00685,
		"OM_longitude_of_ascendingnode": 79.3659,
		"longitude_of_perihelion":376.6059,

		"Tp_Time_of_perihelion_passage_JD": 2407499.827534289027,
		"N_mean_motion":.003188719837864677,
		"epochJD": 2458000.5,
		"MA_mean_anomaly": 161.032496116919,
		"orbit_class" : "TNO",
		"absolute_mag": -0.3,
		"axial_tilt": 0,
		"tga_name": "Makemake"
		},

	"sedna":   {
		"type": TYPE_DWARF_PLANET,
		"material":1,
		"name": "Sedna",
		"iau_name": "SEDNA",
		#"jpl_designation": 90377,
		"jpl_designation": "sedna",
		"mass":4.4e21, # mass is undetermined
		"radius":995e3,
		"QR_perihelion":1.1423e13,
		"EC_e":0.85491,
		"PR_revolution": 3934726.687924069,
		"rotation": 0.4303416887476,
		"IN_orbital_inclination":11.92872,
		"OM_longitude_of_ascendingnode":144.546,
		"longitude_of_perihelion":455.836,

		"Tp_Time_of_perihelion_passage_JD": 2479566.507375652123,
		"N_mean_motion":9.149301299753888e-5,
		"epochJD": 2458000.5,
		"MA_mean_anomaly": 358.0268610068745,
		"orbit_class" : "TNO",
		"absolute_mag": 1.83,
		"axial_tilt": 0,
		"tga_name": "Sedna"

		},

	"haumea":  {
		"type": TYPE_DWARF_PLANET,
		"material":1,
		"name": "Haumea",
		"iau_name": "HAUMEA",
		#"jpl_designation": 136108,
		"jpl_designation": "haumea",
		"mass":4.006e21,
		"radius":620e3,
		"QR_perihelion":35.14529440338772*AU,
		"EC_e":0.1893662787361186,
		"PR_revolution": 104270.6801862633,
		"rotation": 0.163146,
		"IN_orbital_inclination":28.20363151617822,
		"OM_longitude_of_ascendingnode":121.9702799705751,
		"longitude_of_perihelion":360.8407349965672,

		"Tp_Time_of_perihelion_passage_JD": 2500269.703252029540,
		"N_mean_motion":.003452552523460249,
		"epochJD": 2458000.5,
		"MA_mean_anomaly": 214.0633556475513,
		"orbit_class" : "TNO",
		"absolute_mag": 0.2,
		"axial_tilt": 0,
		"tga_name": "Haumea"
		},
}

belt_data = {
	"jupiterTrojan": {
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
		"QR_perihelion":1352.55e9,
		"EC_e":0.05415060,
		"PR_revolution":10759.22,
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
	"uranus": {
		"rings":[
			{	"name"		: "Mu",
				"radius"	: 103000e3,
				"width"		: 17000e3,
				"color"		: Color.darkgrey,
				"opacity"	: 1.0
			},
			{	"name"		: "Nu",
				"radius"	: 69900e3,
				"width"		: 3800e3,
				"color"		: Color.darkgrey,
				"opacity"	: 1.0
			},
			{	"name"		: "Tau",
				"radius"	: 41350e3,
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