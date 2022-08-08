
import numpy as np
from visual import *

def deg2rad(deg):
	return deg * math.pi/180

def rad2deg(rad):
	return rad * 180/math.pi

def getAngleBetweenVectors(v1, v2):
	dotProduct = v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]
	theta = np.arccos(dotProduct/(mag(v1)*mag(v2)))
	return rad2deg(theta)

def getOrthogonalVector(vec):
	# The set of all possible orthogonal vectors is a Plane. Among all possible 
	# orthogonal vectors we choose the one that also lay on the (x,y) plane (with z=0) 
	# and whose x coordinate is arbitrary 1. Using these presets, we can deduct the 
	# y coordinate by applying a dot product between our vec and the orthogonal vector. 
	# Its results must be zero since the vectors are othogonal. 
	# (x.x1 + y.y1 + z.z1 = 0)  => y = -(z.z1 + x.x1)/y1 
	z = 0
	x, y = 0, 0
	if vec[1] != 0:
		x = 1
		y = -vec[0]*x/vec[1]
	else:
		
		y = 1
		x = 0

	# return a unit vector
	norm = mag((x, y, z))
	return vector(x/norm, y/norm, z/norm)
