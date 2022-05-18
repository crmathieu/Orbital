import spiceypy as spice
from spiceypy.utils.support_types import SpiceyError
import numpy as np 
import sys
from math import pi
from visual import *

"""
def loadSpicePlanet(metaKernelName):
	# each obj is either the id of a planet, the sun or a barycenter
	ids = spice.spkobj(metaKernelName)
	names, tcs_sec, tcs_cal = [], [], [], []

	intervalNumber = 0

	for id in ids:
		# objDatas are cells made of various data structures containing intervals
		objData = spice.spkcov(metaKernelName, id)

		# time coverage in sec since J2000
		tc_sec = spice.wnfetd(objData, intervalNumber)
		tcs_sec.append(tc_sec)
"""

def getObjects(metaKernelName):
	# each obj is either the id of a planet, the sun or a barycenter
	obj = spice.spkobj(metaKernelName)
	ids, names, tcs_sec, tcs_cal = [], [], [], []
	n = 0
	interval2fetch = 0
	print str(obj)

	for o in obj:
		# ids
		ids.append(o) 

		# find the coverage window for a specific object given a meta kernel name and an object id
		winc = spice.spkcov(metaKernelName, ids[n])
		
		# get time coverage in sec since J2000 for interval interval2fetch (here it is 0)
		tc_sec = spice.wnfetd(winc, interval2fetch)

		tcs_sec.append(tc_sec)

		# convert it from J2000 to human readable
		tc_cal = [spice.timout(f, "YYYY MON DD HR:MN:SC.### (TDB) ::TDB") for f in tc_sec]
		tcs_cal.append(tc_cal)

		# get name of body
		try:
			names.append(id2body(o))

		except:
			names.append("unknown name")

		# print last elements processed ([-1] means last in array)
		print "id="+str(ids[-1])+", name="+names[-1]+", TC="+tc_cal[0]+ " -> "+tc_cal[1]
		n = n+1

	return ids, names, tcs_sec, tcs_cal


# returns name of a specific id
def id2body(id):
	return spice.bodc2n(id)


def tc2array(tcs, steps):
	# create a big array made of incremental epochs
	arr = np.zeros((steps, 1))

	# creates evenly spaced numbers (tcs[1]-tcs[0]/steps increments) over interval between tcs[0] and tcs[1] 
	arr[:, 0] = np.linspace(tcs[0], tcs[1], steps)
	return arr

def get_ephemeris_data(target, times, frame, observer):
	# spkezr returns an array of stateElements[6], and an array of lighttime float. Each element of the 
	# first array corresponds to a 3Dstate of the target (posx,posy,posz, velx,vely,velz) for a given epoch 
	# provided in the times parameters. Each element of the second array correspond to the lighttime between
	# the target and the observer at a given epoch.

#	return np.array(spice.spkezr(target, times, frame, 'NONE', observer)[0])
	state, lighttime = spice.spkezr(target, times, frame, 'NONE', observer)
	return state

STEPS = 10
FRAME = 'ECLIPJ2000'
OBSERVER = 'SUN'

SUN_M = 1.989e+30 # in Kg
SUN_R = 696e+3 # in km
G = 6.67384e-11	# Universal gravitational constant
#Mu = G * SUN_M 
#Mu = 2.9591309705483544E-04

Mu = 1.32712440018e20
Mu = 132742677600000000000


dicNames = {}
def rad2deg(rad):
	return rad * 180 / pi

if __name__ == '__main__':

	scene.range = 20
	ball = sphere(color=color.cyan)
	v = vec(0,0,0)
	dv = 0.2
	dt = 0.01
	while True:
	    rate(30)
	    k = keysdown() # a list of keys that are down
	    if 'left' in k: v.x -= dv
	    if 'right' in k: v.x += dv
	    if 'down' in k: v.y -= dv
	    if 'up' in k: v.y += dv
	    ball.pos += v*dt

	sys.exit()

	# load spice files from meta kernel
	spice.furnsh("spice/spice-kernels/solarsys_metakernel.mk")

	_, GM_SUN_PRE = spice.bodvcd(bodyid=10, item='GM', maxn=1)
	print GM_SUN_PRE

	et = spice.str2et( 'Apr 13, 2021' );
	print et

 	state, ltime = spice.spkezr( 'EARTH', et, 'ECLIPJ2000', 'LT+S', 'SUN' );

	y = spice.oscltx( state, et, GM_SUN_PRE[0] );
	print "=========="
	print "Perifocal:" + str(y[0]) + " km"
	print "Eccentricity:"+str(y[1])
	
	print "Inclination:"+str(rad2deg(y[2])) + " deg"
	print "Long.Ascending Node:"+str(rad2deg(y[3])) + " deg"
	print "Argumt of periapsis:"+str(rad2deg(y[4])) + " deg"
	print "Mean anomaly:"+str(rad2deg(y[5]))
	print "Epoch:"+str(y[6])
	print "MU:"+str(y[7])
	print "NU:"+str(rad2deg(y[8])) + " deg/s"
	print "Semi-major:"+str(y[9])
	print "Period:"+str(y[10]/86400) + " d"

	sys.exit()

	# extract bodies info from d432s.bsp spk kernel which contains planets infos 
	ids, names, tcs_sec, tcs_cal = getObjects("./spice/spice-kernels/generic/spk/de432s.bsp")



#	names = [f for f in names if 'BARYCENTER' in f]
	for i in range (len(names)): 
		dicNames[names[i]] = ids[i]

	# create time array for ephemeris epoch data for all bodies (assuming they are the same for all bodies)
	times = tc2array(tcs_sec[0], STEPS)

	# create empty list for all ephemeris data
	rs = []
	#dic = {'name': ([np.array64[]], np.array64[])}
	dic = {}

	# collect ephemeris data for each barycenter
	for name in names:
		print "**** ",name," ****"
#		rs.append(get_ephemeris_data(name, times, FRAME, OBSERVER))
		rs.append([name, get_ephemeris_data(name, times, FRAME, OBSERVER)])
		dic[name] = get_ephemeris_data(name, times, FRAME, OBSERVER)

	TARGET = "EARTH"
	#print "=============> //?? ", dic[TARGET][0]
	print rs[len(rs)-1][1]
	print "++++++++++++++++++"
	print dic[TARGET]
	print "******************"
	elts = spice.oscelt(dic[TARGET][0], times[0], GM_SUN_PRE[0])
	print elts
	"""
	rp      Perifocal distance.
	ecc     Eccentricity.
	inc     Inclination.
	lnode   Longitude of the ascending node.
	argp    Argument of periapsis.
	m0      Mean anomaly at epoch.
	t0      Epoch.
	mu      Gravitational parameter.	
	"""
	print "========="
	elts = spice.oscltx(dic[TARGET][0], times[0], GM_SUN_PRE[0])
	#print elts.dtype
	#print elts.shape
	# convert ndarray into array of float
	y = elts #elts[()]
#	print y
#	print y[2]
	print elts
	print "=========="
	print "name:", name
	print "body id:" , dicNames[TARGET]
	print "body name:" , TARGET
	print 	"Perifocal:" + str(y[0]*1.495978707e8)
	print	"Eccentricity:"+str(y[1])
	
	print "Inclination:"+str(y[2])
	print "Long.Ascending Node:"+str(y[3])
	print "Argumt of periapsis:"+str(y[4])
	print "Mean anomaly:"+str(y[5])
	print "Epoch:"+str(y[6])
	print "MU:"+str(y[7])
	print "NU:"+str(y[8])
	print "Semi-major:"+str(y[9])
	print "Period:"+str(y[10])

	print rs[len(rs)-1]
	"""
	RP      Perifocal distance. 
	ECC     Eccentricity. 
	INC     Inclination. 
	LNODE   Longitude of the ascending node. 
	ARGP    Argument of periapsis. 
	M0      Mean anomaly at epoch. 
	T0      Epoch. 
	MU      Gravitational parameter. 
	NU      True anomaly at epoch. 
	A       Semi-major axis. A is set to zero if 
	      it is not computable. 
	TAU     Orbital period. Applicable only for 
	      elliptical orbits. Set to zero otherwise. 
	"""

