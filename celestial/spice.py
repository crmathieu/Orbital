import spiceypy as spice
import datetime
from math import pi

FRAME = 'ECLIPJ2000'

def rad2deg(rad):
	return rad * 180 / pi

def GetOcltx(objectId, timeincrement):
	print timeincrement

	# load spice files from meta kernel
	spice.furnsh("spice/spice-kernels/solarsys_metakernel.mk")

	_, GM_SUN_PRE = spice.bodvcd(bodyid=10, item='GM', maxn=1)
	print GM_SUN_PRE

	# odt contains the date (as string) we want to get ocultation info for
	et = spice.str2et(timeincrement) # 'Apr 13, 2021' );
	print et

# 	state, ltime = spice.spkezr( 'EARTH', et, 'ECLIPJ2000', 'LT+S', 'SUN' );
 	state, ltime = spice.spkezr( objectId, et, FRAME, 'LT+S', 'SUN' );
 	print state, " +++++++ ",  ltime

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
	return y

	#return y[0], y[1], rad2deg(y[2]), rad2deg(y[3]), rad2deg(y[4]), rad2deg(y[5]), y[6], y[7], rad2deg(y[8]), y[9], y[10]/86400
id = 50000001 #-143205
GetOcltx(str(id), datetime.datetime.today().strftime('%b %d, %Y'))

