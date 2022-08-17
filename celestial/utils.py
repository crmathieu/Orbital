
import numpy as np
from visual import *

def deg2rad(deg):
	return deg * math.pi/180

def rad2deg(rad):
	return rad * 180/math.pi

def getAngleBetweenVectors(v1, v2):
	dotProduct = v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]
	print "getAngleBetweenVectors, cos(theta)=", dotProduct/(mag(v1)*mag(v2))
	theta = np.arccos(dotProduct/(mag(v1)*mag(v2)))
	return rad2deg(theta)

def getXYprojection(vec):
	return getVectorProjection(vec, [1,1,0])

def getXZprojection(vec):
	return getVectorProjection(vec, [1,0,1])

def getYZprojection(vec):
	return getVectorProjection(vec, [0,1,1])

def getVectorProjection(vec, plane):
	# plane can be either the (0,1,1), (1,0,1) or (1,1,0) planes
	return vec[0]*plane[0], vec[1]*plane[1], vec[2]*plane[2] 


def getOrthogonalVector(vec):
	# The set of all possible orthogonal vectors to a given vector is a Plane. Among 
	# all possible orthogonal vectors we choose the one that also lay on the (x,y) 
	# plane (with z=0) and whose x coordinate is arbitrary 1. Using these presets, we 
	# can deduct the y coordinate by applying a dot product between our vec and its 
	# orthogonal vector. The result of the dot product must be zero since the 
	# vectors are othogonal: 
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

def getVectorOrthogonalToPlane(A, B):
	# Vectors A and B defined a plane. To determined the unit vector that is
	# orthogonal to this plane, we need to calculate the cross product:
	# A X B = (a1b2 - b1a2, b0a2 - a0b2, a0b1 - b0a1) which comes from calculating 
	# the determinant:
	# 			    | i		j		k  |   
	#	P = A X B = | a0	a1		a2 | = i(a1b2 - b1a2) - j(a0b2 - b0a2) + k(a0b1 - b0a1)
	#			    | b0	b1		b2 |
	#

	x = A[1]*B[2] - A[2]*B[1]
	y = A[2]*B[0] - A[0]*B[2]
	z = A[0]*B[1] - B[0]*A[1]

	# return a unit vector
	norm = mag((x, y, z))
	return vector(x/norm, y/norm, z/norm)
