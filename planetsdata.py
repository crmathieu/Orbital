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

INNERPLANET = 0x01
OUTTERPLANET = 0x02
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

TYPE_MASK = 0xFFFFF

SATELLITE_M = 100
THREE_D = False
MAX_P_D = 1.1423e13
MIN_P_D = 46.0e9
LEGEND = True

SUN_M = 1.989e+30
SUN_R = 696e+6
G = 6.67384e-11	# Universal gravitational constant
Mu = G * SUN_M
DIST_FACTOR = 10e-7

# EPOCH constants
#JD2000_EPOCH = 2451543.5	# number of days ellapsed from 01-01-4713 BC GMT to 01-01-2000 AD GMT
EPOCH_2000_JD = 2451544.5	# number of days ellapsed from 01-01-4713 BC GMT to 01-01-2000 AD GMT
EPOCH_2000_MJD = 51544.0
EPOCH_1970_JD = 2440587.5 # number of days ellapsed from 01-01-4713 BC GMT to 01-01-1970 AD GMT

X_COOR = 0
Y_COOR = 1
Z_COOR = 2

TYPE_PLANET = 1
TYPE_ASTEROID = 2
TYPE_DWARF_PLANET = 3
TYPE_COMET = 4
TYPE_TRANS_N = 5

AU = 149597870691
DEFAULT_RADIUS = 2.78787878

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

objects_data = {
	"neptune" :{
		"type": TYPE_PLANET,
		"material":1,
		"name": "Neptune",
		"iau_name": "NEPTUNE",
		"jpl_designation": "NEPTUNE",
		"mass":102e24,
		"radius":24622e3,
		"perihelion":4444.45e9,
		"e":0.00858587,
		"revolution":164.179 * 365,
		"orbital_inclination":1.769,
		"longitude_of_ascendingnode":131.72169,
		"longitude_of_perihelion":44.97135,
		"orbital_obliquity": 28.3,
		"kep_elt":{"a" : 30.06952752, "ar": 0.00006447,"e" : 0.00895439,"er": 0.00000818,"i" : 1.77005520,"ir": 0.00022400,"L" : 304.22289287,"Lr": 218.46515314,"W" : 46.68158724,"Wr": 0.01009938,"N" : 131.78635853,"Nr": -0.00606302,"b" : -0.00041348,"c" : 0.68346318,"s" : -0.10162547,"f" : 7.67025000}
		},

	"uranus" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Uranus",
		"iau_name": "URANUS",
		"jpl_designation": "URANUS",
		"mass":86.8e24,
		"radius":25362e3,
		"perihelion":2741.30e9,
		"e":0.04716771,
		"revolution":84.011 * 365,
		"orbital_inclination":0.770,
		"longitude_of_ascendingnode":74.22988,
		"longitude_of_perihelion":170.96424,
		"orbital_obliquity": 97.8,
		"kep_elt":{"a" : 19.18797948, "ar": -0.00020455, "e" : 0.04685740, "er": -0.00001550, "i" : 0.77298127, "ir": -0.00180155, "L" : 314.20276625, "Lr": 428.49512595, "W" : 172.43404441, "Wr": 0.09266985, "N": 73.96250215, "Nr": 0.05739699, "b" : 0.00058331, "c" : -0.97731848, "s" : 0.17689245, "f" : 7.67025000}
		},

	"saturn" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Saturn",
		"iau_name": "SATURN",
		"jpl_designation": "SATURN",
		"mass":568e24,
		"radius":58232e3,
		"perihelion":1352.55e9,
		"e":0.05415060,
		"revolution":29.457 * 365,
		"orbital_inclination":2.484,
		"longitude_of_ascendingnode":113.71504,
		"longitude_of_perihelion":92.43194,
		"orbital_obliquity": 26.7,
		"kep_elt":{"a" : 9.54149883, "ar": -0.00003065, "e" : 0.05550825, "er": -0.00032044, "i" : 2.49424102, "ir": 0.00451969, "L" : 50.07571329, "Lr": 1222.11494724, "W" : 92.86136063, "Wr": 0.54179478, "N": 113.63998702, "Nr": -0.25015002, "b" : 0.00025899, "c" : -0.13434469, "s" : 0.87320147, "f" : 38.35125}
		},

	"jupiter" :{
		"type": TYPE_PLANET,
		"material":1,
		"name": "Jupiter",
		"iau_name": "JUPITER",
		"jpl_designation": "JUPITER",
		"mass":1898e24,
		"radius":69911e3,
		"perihelion":740.52e9,
		"e":0.04839266,
		"revolution":11.862 * 365,
		"orbital_inclination":1.305,
		"longitude_of_ascendingnode":100.55615,
		"longitude_of_perihelion":14.75385,
		"orbital_obliquity": 3.1,
		"kep_elt":{"a" : 5.20248019, "ar": -0.00002864, "e" : 0.04853590, "er": 0.00018026, "i" : 1.29861416, "ir": -0.00322699, "L" : 34.33479152, "Lr": 3034.90371757, "W" : 14.27495244, "Wr": 0.18199196, "N": 100.29282654, "Nr": 0.13024619, "b" : -0.00012452, "c" : 0.06064060, "s" : -0.35635438, "f" : 38.35125}
		},

	"mars" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Mars",
		"iau_name": "MARS",
		"jpl_designation": "MARS",
		"mass":0.642e24,
		"radius":3389e3,
		"perihelion":206.62e9,
		"e":0.09341233,
		"revolution":686.98,
		"orbital_inclination":1.851,
		"longitude_of_ascendingnode":49.57854,
		"longitude_of_perihelion":336.04084,
		"orbital_obliquity": 25.2,
		"kep_elt":{'a' : 1.52371243, 'ar': 9.7e-07, 'e' : 0.09336511, 'er':9.149e-05, 'i' :1.85181869, 'ir':-0.00724757, 'L' :-4.56813164, 'Lr':19140.2993424, 'W' :-23.91744784, 'Wr':0.45223625, 'N' :49.71320984, 'Nr':-0.26852431, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0}
		},

	"mercury" :{
		"type": TYPE_PLANET,
		"material":1,
		"name": "Mercury",
		"iau_name": "MERCURY",
		"jpl_designation": "MERCURY",
		"mass":0.330e24,
		"radius":2439e3,
		"perihelion":46.0e9,
		"e":0.20563069,
		"revolution":87.969,
		"orbital_inclination":7.005,
		"longitude_of_ascendingnode":48.33167,
		"longitude_of_perihelion":77.45645,
		"orbital_obliquity": 0.034,
		"kep_elt":{'a' : 0.38709843, 'ar': 0.0, 'e' : 0.20563661, 'er':0.00002123, 'i' :7.00559432, 'ir':-0.00590158, 'L' :252.25166724, 'Lr':149472.674866, 'W' :77.45771895, 'Wr':0.15940013, 'N' :48.33961819, 'Nr':-0.12214182, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
		},

	"venus" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Venus",
		"iau_name": "VENUS",
		"jpl_designation": "VENUS",
		"mass":4.87e24,
		"radius":6052e3,
		"perihelion":107.48e9,
		"e":0.00677323,
		"revolution":224.701,
		"orbital_inclination":3.3947,
		"longitude_of_ascendingnode":76.68069,
		"longitude_of_perihelion":131.53298,
		"orbital_obliquity": 177.4,
		"kep_elt":{'a' : 0.72332102, 'ar': -2.6e-07, 'e' : 0.00676399, 'er':-5.107e-05, 'i' :3.39777545, 'ir':0.00043494, 'L' :181.9797085, 'Lr':58517.8156026, 'W' :131.76755713, 'Wr':0.05679648, 'N' :76.67261496, 'Nr':-0.27274174, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
		},

	"earth" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Earth",
		"iau_name": "EARTH",
		"jpl_designation": "EARTH",
		"mass":5.972e24,
		"radius":6371e3,
		"perihelion":147.09e9,
		"e":0.01671022,
		"revolution":365.256,
		"orbital_inclination":0,
		"longitude_of_ascendingnode":-11.26064,
		"longitude_of_perihelion":102.94719,
		"orbital_obliquity": 23.4,
		"kep_elt":{'a' : 1.00000018, 'ar': -3e-08, 'e' : 0.01673163, 'er':-3.661e-05, 'i' :-0.00054346, 'ir':-0.01337178, 'L' :100.46691572, 'Lr':35999.3730633, 'W' :102.93005885, 'Wr':0.3179526, 'N' :-5.11260389, 'Nr':-0.24123856, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
		},

	"pluto" : {
		"type": TYPE_PLANET,
		"material":1,
		"name": "Pluto",
		"iau_name": "PLUTO",
		"jpl_designation": "PLUTO",
		"mass":0.0146e24,
		"radius":1195e3,
		"perihelion":4436.82e+9,
		"e":0.24880766,
		"revolution":247.68 * 365,
		"orbital_inclination":17.142,
		"longitude_of_ascendingnode":110.30347,
		"longitude_of_perihelion":224.06676,
		"orbital_obliquity": 122.5,
		"kep_elt":{'a' : 39.48686035, 'ar': 0.00449751, 'e' : 0.24885238, 'er':6.016e-05, 'i' :17.1410426, 'ir':5.01e-06, 'L' :238.96535011, 'Lr':145.18042903, 'W' :224.09702598, 'Wr':-0.00968827, 'N' :110.30167986, 'Nr':-0.00809981, 'b' :-0.01262724, 'c' :0.0, 's':0.0, 'f' :0.0}
		},

	"eris" : {
		"type": TYPE_DWARF_PLANET,
		"material":1,
		"name": "Eris",
		"iau_name": "ERIS",
		"jpl_designation": 136199,
		"mass":1.66e22,
		"radius":1163e3,
		"perihelion":5.723e12,
		"e":0.4417142619088136,
		"revolution": 203830,
		"orbital_inclination":44.0445,
		"longitude_of_ascendingnode": 35.87791199490014,
		"longitude_of_perihelion":186.9301,

		"Time_of_perihelion_passage_JD": 2545575.799683113451,
		"mean_motion":.001771354370292503,
		"epochJD": 2458000.5,
		"mean_anomaly": 204.8731101766414,
		"orbit_class" : "TNO",
		"orbital_obliquity": 0
		},

	"makemake":{
		"type": TYPE_DWARF_PLANET,
		"material":1,
		"name": "Makemake",
		"iau_name": "MAKEMAKE",
		"jpl_designation": 136472,
		"mass":4.4e21,
		"radius":739e3,
		"perihelion":5.77298e12,
		"e":.154682767507142,
		"revolution": 112897.9710682497,
		"orbital_inclination":29.00685,
		"longitude_of_ascendingnode": 79.3659,
		"longitude_of_perihelion":376.6059,

		"Time_of_perihelion_passage_JD": 2407499.827534289027,
		"mean_motion":.003188719837864677,
		"epochJD": 2458000.5,
		"mean_anomaly": 161.032496116919,
		"orbit_class" : "TNO",
		"orbital_obliquity": 0
		},

	"sedna":   {
		"type": TYPE_DWARF_PLANET,
		"material":0,
		"name": "Sedna",
		"iau_name": "SEDNA",
		"jpl_designation": 90377,
		"mass":4.4e21, # mass is undetermined
		"radius":995e3,
		"perihelion":1.1423e13,
		"e":0.85491,
		"revolution": 3934726.687924069,
		"orbital_inclination":11.92872,
		"longitude_of_ascendingnode":144.546,
		"longitude_of_perihelion":455.836,

		"Time_of_perihelion_passage_JD": 2479566.507375652123,
		"mean_motion":9.149301299753888e-5,
		"epochJD": 2458000.5,
		"mean_anomaly": 358.0268610068745,
		"orbit_class" : "TNO",
		"orbital_obliquity": 0
		},

	"haumea":  {
		"type": TYPE_DWARF_PLANET,
		"material":1,
		"name": "Haumea",
		"iau_name": "HAUMEA",
		"jpl_designation": 136108,
		"mass":4.006e21,
		"radius":620e3,
		"perihelion":35.14529440338772*AU,
		"e":0.1893662787361186,
		"revolution": 104270.6801862633,
		"orbital_inclination":28.20363151617822,
		"longitude_of_ascendingnode":121.9702799705751,
		"longitude_of_perihelion":360.8407349965672,

		"Time_of_perihelion_passage_JD": 2500269.703252029540,
		"mean_motion":.003452552523460249,
		"epochJD": 2458000.5,
		"mean_anomaly": 214.0633556475513,
		"orbit_class" : "TNO",
		"orbital_obliquity": 0
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
