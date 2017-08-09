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

from planetsdata import *
from visual import *
import numpy as np
from random import *
import scipy.special as sp
import datetime
import time
import sys

class solarSystem:

	INNER_RING_COEF = 1.3
	OUTTER_RING_COEF = 1.9

	bodies = []

	def __init__(self):
		self.Name = "Sun"
		self.nameIndex = {}
		self.BodyRadius = SUN_R
		self.Mass = SUN_M
		self.AbortSlideShow = False
		self.SlideShowInProgress = False
		self.currentSource = PHA
		self.JTrojansIndex = -1

		self.Scene = display(title = 'Solar System', width = 1300, height = 740, center = (0,0,0))

		self.Scene.lights = []
		self.Scene.forward = (0,0,-1)
		self.Scene.fov = math.pi/3
		self.Scene.userspin = True
		self.Scene.userzoom = True
		self.Scene.autoscale = 1
		self.Scene.autocenter = False
		self.Scene.up = (0,0,1)
		self.Axis = [0,0,0]
		self.AxisLabel = ["","",""]
		self.CorrectionSize = self.BodyRadius*DIST_FACTOR/1.e-2

		# make all light coming from origin
		self.sunLight = local_light(pos=(0,0,0), color=color.white)
		self.Scene.ambient = color.black

		if THREE_D:
			self.Scene.stereo='redcyan'
			self.Scene.stereodepth = 1

		self.BodyShape = sphere(pos=vector(0,0,0), radius=self.BodyRadius/self.CorrectionSize, color=color.white)
		self.BodyShape.material = materials.emissive

		# make referential
		self.makeAxes(color.white, 3*AU*DIST_FACTOR, (0,0,0))

	def makeAxes(self, color, size, position):
	    directions = [vector(size,0,0), vector(0,size,0), vector(0,0,size/4)]
	    texts = ["x (vernal eq.)","y","z"]
	    pos = vector(position)
	    for i in range (3): # Each direction
	       self.Axis[i] = curve( frame = None, color = color, pos= [ pos, pos+directions[i]], visible=False)
	       self.AxisLabel[i] = label( frame = None, color = color,  text = texts[i],
		   							pos = pos+directions[i], opacity = 0, box = False, visible=False )

	def addTo(self, body):
		self.bodies.append(body)
		i = len(self.bodies) - 1
		self.nameIndex[body.JPL_designation] = i
		return i # this is the index of the added body in the collection

	def addJTrojans(self, body):
		if self.JTrojansIndex < 0:
			self.JTrojansIndex = self.addTo(body)
		else:
			for i in range(len(self.bodies[self.JTrojansIndex].Labels)):
				self.bodies[self.JTrojansIndex].Labels[i].visible = False
			self.bodies[self.JTrojansIndex].BodyShape.visible = False
			self.bodies[self.JTrojansIndex].Labels = []
			self.bodies[self.JTrojansIndex] = body

		body.draw()

	def getJTrojans(self):
		return self.bodies[self.JTrojansIndex]

	def drawAllBodiesTrajectory(self):
		for body in self.bodies:
			if body.BodyType in [OUTTERPLANET, INNERPLANET, DWARFPLANET, KUIPER_BELT, ASTEROID_BELT, INNER_OORT_CLOUD, ECLIPTIC_PLANE]:
				body.draw()

		self.Scene.autoscale = 1

	def getBodyFromName(self, jpl_designation):
		if jpl_designation in self.nameIndex:
			return self.bodies[self.nameIndex[jpl_designation]]
		return None

	def isRealsize(self):
		if self.ShowFeatures & REALSIZE <> 0:
				return True
		return False

	def refresh(self, animationInProgress = False):
		orbitTrace = False
		if self.ShowFeatures & ORBITS <> 0:
			orbitTrace = True

		labelVisible = False
		if self.ShowFeatures & LABELS <> 0:
			labelVisible = True

		realisticSize = False
		if self.ShowFeatures & REALSIZE <> 0:
			realisticSize = True

		for body in self.bodies:
			if body.BodyType in [OUTTERPLANET, INNERPLANET, ASTEROID, COMET, DWARFPLANET, PHA, BIG_ASTEROID, TRANS_NEPT]:
				body.toggleSize(realisticSize)

				if body.BodyShape.visible == True:
					body.Trail.visible = orbitTrace
					for i in range(len(body.Labels)):
						body.Labels[i].visible = labelVisible
			else: # belts / rings
				if body.BodyShape.visible == True and animationInProgress == True:
					body.BodyShape.visible = False
					for i in range(len(body.Labels)):
						body.Labels[i].visible = False

		if self.ShowFeatures & LIT_SCENE <> 0:
			self.Scene.ambient = color.white
			self.sunLight.visible = False
		else:
			self.Scene.ambient = color.black
			self.sunLight.visible = True

		if self.ShowFeatures & REFERENTIAL <> 0:
			for i in range(3):
				self.Axis[i].visible = True
				self.AxisLabel[i].visible = True
		else:
			for i in range(3):
				self.Axis[i].visible = False
				self.AxisLabel[i].visible = False

	def makeRings(self, system, bodyName, density = 1):  # change default values during instantiation
		global objects_data
		self.solarsystem = system
		planet = self.getBodyFromName(objects_data[bodyName]['jpl_designation'])
		if planet <> None:
			InnerRadius = planet.BodyRadius * self.INNER_RING_COEF / planet.SizeCorrection[planet.sizeType]
			OutterRadius = planet.BodyRadius * self.OUTTER_RING_COEF / planet.SizeCorrection[planet.sizeType]
			planet.Ring = true
			planet.InnerRing = curve(color=planet.Color)
			planet.OutterRing = curve(color=planet.Color)

			if (self.solarsystem.ShowFeatures & planet.BodyType) == 0:
				planet.InnerRing.visible = false
				planet.OutterRing.visible = false

			Position = np.matrix([[0],[0],[0]])
			angle = planet.Angle + pi/2
			Rotation_3D = np.matrix([
				[1, 0, 					0],
				[0, cos(angle), 	-sin(angle)],
				[0, sin(angle), 	cos(angle)]]
			)

			for i in np.arange(0, 2*pi, pi/(180*density)):
				Position = [[(OutterRadius * cos(i))], [(OutterRadius * sin(i))], [0]]
				Position = Rotation_3D * Position + planet.Position
				planet.OutterRing.append(pos=(Position[X_COOR], Position[Y_COOR], Position[Z_COOR]), color=planet.Color) #radius=pointRadius/planet.SizeCorrection, size=1)

				Position = [[(InnerRadius * cos(i))], [(InnerRadius * sin(i))], [0]]
				Position = Rotation_3D * Position + planet.Position
				planet.InnerRing.append(pos=(Position[X_COOR], Position[Y_COOR], Position[Z_COOR]), color=planet.Color) #radius=pointRadius/planet.SizeCorrection, size=1)


class makeEcliptic:

	def __init__(self, system, color):  # change default values during instantiation
		# draw a circle of 250 AU
		self.Name = "Ecliptic Plane"
		self.Iau_name = "ecliptic"
		self.JPL_designation = "ecliptic"
		self.solarsystem = system
		self.Color = color
		self.BodyType = ECLIPTIC_PLANE

	def refresh(self):
		if self.solarsystem.ShowFeatures & ECLIPTIC_PLANE <> 0:
			self.BodyShape.visible = True
		else:
			self.BodyShape.visible = False

	def draw(self):
		self.BodyShape = cylinder(pos=vector(0,0,0), radius=250*AU*DIST_FACTOR, color=self.Color, length=100, opacity=0.2, axis=(0,0,1))
		self.BodyShape.visible = False


class makeBelt:

	def __init__(self, system, index, name, bodyType, color, size, density = 1, planetname = None):  # change default values during instantiation
		self.Labels = []
		self.Name = name
		self.Iau_name = name
		self.JPL_designation = name
		self.solarsystem = system
		self.Density = density		# body name
		self.RadiusMinAU = belt_data[index]["radius_min"]	# in AU
		self.RadiusMaxAU = belt_data[index]["radius_max"]	# in AU
		self.Thickness = belt_data[index]["thickness"]	# in AU
		self.ThicknessFactor = belt_data[index]["thickness_factor"]
		self.PlanetName = planetname
		self.Color = color
		self.BodyType = bodyType
		self.BodyShape = points(pos=(self.RadiusMinAU, 0, 0), size=size, color=color)
		self.BodyShape.visible = False
		if self.Thickness == 0:
			self.Thickness = (self.RadiusMinAU + self.RadiusMaxAU)/2 * math.tan(math.pi/6)
		shape = "cube"

	def getGaussian(self, position):
		mu = (self.RadiusMinAU + self.RadiusMaxAU)* AU * DIST_FACTOR/2
		sigma = (self.RadiusMaxAU - self.RadiusMinAU)* AU * DIST_FACTOR/3
		return float((1/(sigma*sqrt(math.pi*2)))*exp(-(((position-mu)/sigma)**2)/2))

	def draw(self):
		for i in np.arange(0, 2*math.pi, math.pi/(180*self.Density)):
			# generate random radius between Min and MAX
			RandomRadius = randint(round(self.RadiusMinAU * AU * DIST_FACTOR, 3) * 1000, round(self.RadiusMaxAU * AU * DIST_FACTOR, 3) * 1000) / 1000
			MAX = self.getGaussian(RandomRadius) * self.Thickness * AU * DIST_FACTOR * self.ThicknessFactor
			heightToEcliptic = {0: 0, 1:1, 2:-1}[randint(0,2)] * randint(0, int(round(MAX, 6)*1.e6))/1.e6
			self.BodyShape.append(pos=(RandomRadius * cos(i), RandomRadius * sin(i), heightToEcliptic))

		self.Labels.append(label(pos=(self.RadiusMaxAU * AU * DIST_FACTOR * cos(i), self.RadiusMaxAU * AU * DIST_FACTOR * sin(i), 0), text=self.Name, xoffset=20, yoffset=12, space=0, height=10, border=6, box=false, font='sans', visible = False))

	def refresh(self):
		if self.solarsystem.ShowFeatures & self.BodyType <> 0:
			if self.BodyShape.visible == False:
				self.BodyShape.visible = True

			if self.solarsystem.ShowFeatures & LABELS <> 0:
				labelVisible = True
			else:
				labelVisible = False

			for i in range(len(self.Labels)):
				self.Labels[i].visible = labelVisible

		else:
			if self.BodyShape.visible == true:
				self.BodyShape.visible = false
				for i in range(len(self.Labels)):
					self.Labels[i].visible = False

class makeJtrojan(makeBelt):

	def __init__(self, system, index, name, bodyType, color, size, density = 1, planetname = None):
		makeBelt.__init__(self, system, index, name, bodyType, color, size, density, planetname)
		self.Planet = self.solarsystem.getBodyFromName(objects_data[self.PlanetName]['jpl_designation'])
		if self.Planet <> None:
			self.JupiterX = self.Planet.Position[X_COOR]
			self.JupiterY = self.Planet.Position[Y_COOR]
		else:
			self.JupiterX = 0
			self.JupiterY = 0

	def updateThickness(self, increment):
		self.RadiusMinAU = belt_data["jupiterTrojan"]["radius_min"]	- sqrt(increment) # in AU
		self.RadiusMaxAU = belt_data["jupiterTrojan"]["radius_max"]	+ sqrt(increment) # in AU
		self.Thickness = belt_data["jupiterTrojan"]["thickness"]	+ sqrt(increment)

	def draw(self):
		# determine where the body is
		if self.PlanetName == None:
			return

		# grab Jupiter's current True Anomaly and add the Long. of perihelion to capture
		# the current angle in the fixed referential
		Nu = deg2rad(toRange(rad2deg(self.Planet.Nu) + self.Planet.Longitude_of_perihelion))

		# get Lagrangian L4 and L5 based on body position
		L4 = (Nu + 4*pi/3 )
		L5 = (Nu + 2*pi/3)
		delta = deg2rad(25)

		for i in np.arange(pi/(180*self.Density), delta, pi/(180*self.Density)):
			self.updateThickness(i)
			RandomRadius = uniform(round(self.RadiusMinAU * AU * DIST_FACTOR, 3) * 1000, round(self.RadiusMaxAU * AU * DIST_FACTOR, 3) * 1000) / 1000
			RandomTail = uniform(round(belt_data["jupiterTrojan"]["radius_min"]  * AU * DIST_FACTOR, 3) * 1000, round(belt_data["jupiterTrojan"]["radius_max"] * AU * DIST_FACTOR, 3) * 1000) / 1000
			MAX = self.getGaussian(RandomRadius) * self.Thickness * AU * DIST_FACTOR * self.ThicknessFactor
			MAXTAIL = self.getGaussian(RandomTail) * self.Thickness * AU * DIST_FACTOR * self.ThicknessFactor

			heightToEcliptic = {0:1, 1:-1}[randint(0,1)] * uniform(1 * AU * DIST_FACTOR, int(round(MAX*sqrt(19*i), 6)*1.e6))/1e6
			heightToEclipticTail = {0:1, 1:-1}[randint(0,1)] * uniform(1 * AU * DIST_FACTOR, int(round(MAXTAIL*sqrt(delta-i), 6)*1.e6))/1e6
			# calculate positions on 1/2 values for small tail
			self.BodyShape.append(pos=(RandomTail * cos(L4+delta+i), RandomTail * sin(L4+delta+i), heightToEclipticTail))
			self.BodyShape.append(pos=(RandomTail * cos(L5-delta-i), RandomTail * sin(L5-delta-i), heightToEclipticTail))
			# calculate positions on 1/2 values and complete by symetry for the rest
			self.BodyShape.append(pos=(RandomRadius * cos(L4-delta+i), RandomRadius * sin(L4-delta+i), heightToEcliptic))
			self.BodyShape.append(pos=(RandomRadius * cos(L4+delta-i), RandomRadius * sin(L4+delta-i), heightToEcliptic))
			self.BodyShape.append(pos=(RandomRadius * cos(L5-delta+i), RandomRadius * sin(L5-delta+i), heightToEcliptic))
			self.BodyShape.append(pos=(RandomRadius * cos(L5+delta-i), RandomRadius * sin(L5+delta-i), heightToEcliptic))

		self.Labels.append(label(pos=(self.RadiusMaxAU * AU * DIST_FACTOR * cos(L4), self.RadiusMaxAU * AU * DIST_FACTOR * sin(L4), 0), text="L4 Trojans", xoffset=20, yoffset=12, space=0, height=10, border=6, box=false, font='sans', visible = False))
		self.Labels.append(label(pos=(self.RadiusMaxAU * AU * DIST_FACTOR * cos(L5), self.RadiusMaxAU * AU * DIST_FACTOR * sin(L5), 0), text="L5 Trojans", xoffset=20, yoffset=12, space=0, height=10, border=6, box=false, font='sans', visible = False))

class makeBody:

	def __init__(self, system, index, color, trueAnomaly, bodyType = INNERPLANET, sizeCorrectionType = INNERPLANET):  # change default values during instantiation


		self.Labels = []
		self.ObjectIndex = index
		self.solarsystem 			= system
		self.Ring 					= False
		self.OrbitalObliquity		= objects_data[index]["orbital_obliquity"]
		self.Name					= objects_data[index]["name"]		# body name
		self.Iau_name				= objects_data[index]["iau_name"]		# body iau name
		self.JPL_designation 		= objects_data[index]["jpl_designation"]
		self.Mass 					= objects_data[index]["mass"]		# body mass
		self.BodyRadius 			= objects_data[index]["radius"]		# body radius
		self.Color 					= color
		self.BodyType 				= bodyType
		self.Revolution 			= objects_data[index]["revolution"]
		self.Perihelion 			= objects_data[index]["perihelion"]	# body perhelion
		self.Distance 				= objects_data[index]["perihelion"]	# body distance at perige from focus
		self.Details				= False
		self.hasRenderedOrbit		= False

		self.Moid = objects_data[index]["earth_moid"] if "earth_moid" in objects_data[index] else 0
		self.setOrbitalElements(index)

		# generate 2d coordinates in the initial orbital plane, with +X pointing
		# towards periapsis. Make sure to convert degree to radians before using
		# any sin or cos function

		self.setPolarCoordinates(deg2rad(self.E))
		self.b = getSemiMinor(self.a, self.e)
		self.Aphelion = getAphelion(self.a, self.e)	# body aphelion

		# initial acceleration
		self.Acceleration = vector(0,0,0)
		self.Interval = 0
		self.SizeCorrection = [1] * 2
		self.sizeType = 0

		self.Position = np.matrix([[0],[0],[0]], np.float64)

		self.Rotation_VernalEquinox = np.matrix([
			[-1,	 0, 	0],
			[ 0,	-1,		0],
			[ 0,	 0,		1]]
		)

		# calculate current position of body on its orbit knowing
		# its current distance from Sun (R) and angle (Nu) that
		# were set up in setPolarCoordinates

		self.N = deg2rad(self.Longitude_of_ascendingnode)
		self.w = deg2rad(self.Argument_of_perihelion)
		self.i = deg2rad(self.Inclinaison)

		# convert polar to Cartesian in Sun referential
		self.setCartesianCoordinates()

		sizeCorrection = { INNERPLANET: 1200, GASGIANT: 1900, DWARFPLANET: 100, ASTEROID:1, COMET:0.02, SMALL_ASTEROID: 0.1, BIG_ASTEROID:0.1, PHA: 0.0013, TRANS_NEPT: 0.001}[sizeCorrectionType]
		self.shape = { INNERPLANET: "sphere", OUTTERPLANET: "sphere", DWARFPLANET: "sphere", ASTEROID:"cube", COMET:"cone", SMALL_ASTEROID:"cube", BIG_ASTEROID:"sphere", PHA:"cube", TRANS_NEPT: "cube"}[bodyType]

		self.SizeCorrection[0] = getSigmoid(self.Perihelion, sizeCorrection)
		self.SizeCorrection[1] = self.getRealisticSizeCorrection()

		if self.BodyRadius < DEFAULT_RADIUS:
			self.radiusToShow = DEFAULT_RADIUS
		else:
			self.radiusToShow = self.BodyRadius

		self.makeShape()

		# attach a curve to the object to display its orbit
		self.Trail = curve(color=self.Color)
		self.Trail.append(pos=self.BodyShape.pos)

		data = materials.loadTGA("./img/"+index) if objects_data[index]["material"] <> 0 else materials.loadTGA("./img/asteroid")

		self.BodyShape.material = materials.texture(data=data, mapping="spherical", interpolate=False)
		self.BodyShape.rotate(angle=self.Angle)

		# add LEGEND
		self.Labels.append(label(pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]), text=self.Name, xoffset=20, yoffset=12, space=0, height=10, color=color, border=6, box=false, font='sans'))
		if (self.solarsystem.ShowFeatures & bodyType) == 0:
			self.BodyShape.visible = False
			self.Labels[0].visible = False


	def makeShape(self):
		self.BodyShape = ellipsoid(	pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]),
									length=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType], make_trail=false)
		self.Angle = pi/randint(2,6)

	def getRealisticSizeCorrection(self):
		return 1e-7/(DIST_FACTOR*5)

	def toggleSize(self, realisticSize):

		x = 1 if realisticSize == True else 0
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		asteroidRandom = [(randint(10, 20)/10, randint(10, 20)/10, randint(10, 20)/10), (1,1,1)]
		self.BodyShape.length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyShape.height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyShape.width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

	def animate(self, timeIncrement):

		if self.hasRenderedOrbit == False:
			self.draw()
		# update position
		self.setOrbitalElements(self.ObjectIndex, timeIncrement)
		self.setPolarCoordinates(deg2rad(self.E))

		# initial acceleration
		self.Acceleration = vector(0,0,0)

		# calculate current body position on its orbit knowing
		# its current distance from Sun (R) and True anomaly (Nu)
		# that were set in setPolarCoordinates

		self.N = deg2rad(self.Longitude_of_ascendingnode)
		self.w = deg2rad(self.Argument_of_perihelion)
		self.i = deg2rad(self.Inclinaison)

		# convert polar to Cartesian in Sun referential
		self.setCartesianCoordinates()
		self.BodyShape.pos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])
		self.Labels[0].pos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])

		if self.Ring == True:
			self.InnerRing.visible = False
			self.OutterRing.visible = False
			self.InnerRing = None
			self.OutterRing = None
			self.solarsystem.makeRings(self.solarsystem, self.ObjectIndex)

		return self.getCurrentVelocity()


	def setOrbitalElements(self, index, timeincrement = 0):
		# For comets, asteroids or dwarf planets, data comes from data
		# files -or- predefined values. Orbital Position is calculated
		# from the last time of perihelion passage. This is the default
		# behavior
		self.setOrbitalFromPredefinedElements(objects_data[index], timeincrement)

	# will calculate current value of approximate position of the major planets
	# including pluto. This won't work for Asteroid, Comets or Dwarf planets
	def setOrbitalFromKeplerianElements(self, elts, timeincrement):
		# get number of days since J2000 epoch and obtain the fraction of century
		# (the rate adjustment is given as a rate per century)
		T = (daysSinceJ2000UTC() + timeincrement)/36525. # T is in centuries

		self.a = (elts["a"] + (elts["ar"] * T)) * AU
		self.e = elts["e"] + (elts["er"] * T)
		self.Inclinaison = elts["i"] + (elts["ir"] * T)

		# compute mean Longitude with correction factors beyond jupiter M = L - W + bT^2 +ccos(ft) + ssin(ft)
		L = elts["L"] + (elts["Lr"] * T) + (elts["b"] * T**2  +
											elts["c"] * cos(elts["f"] * T) +
											elts["s"] * sin(elts["f"] * T))
		self.Longitude_of_perihelion = elts["W"] + (elts["Wr"] * T)
		self.Longitude_of_ascendingnode = elts["N"] + (elts["Nr"] * T)

		# compute Argument of perihelion w
		self.Argument_of_perihelion = self.Longitude_of_perihelion - self.Longitude_of_ascendingnode

		# compute mean Anomaly M = L - W
		M = toRange(L - self.Longitude_of_perihelion) #W)

		# Obtain ecc. Anomaly E (in degrees) from M using an approx method of resolution:
		success, self.E, dE, it = solveKepler(M, self.e, 12000)
		if success == False:
			print "Could not converge for "+self.Name+", E = "+str(self.E)+", last precision = "+str(dE)

	def setOrbitalFromPredefinedElements(self, elts, timeincrement):
		# data comes from data file or predefined values
		self.e 							= elts["e"]
		self.Longitude_of_perihelion 	= elts["longitude_of_perihelion"]
		self.Longitude_of_ascendingnode = elts["longitude_of_ascendingnode"]
		self.Argument_of_perihelion 	= self.Longitude_of_perihelion - self.Longitude_of_ascendingnode
		self.a 							= getSemiMajor(self.Perihelion, self.e)
		self.Inclinaison 				= elts["orbital_inclination"]
		self.Time_of_perihelion_passage = elts["Time_of_perihelion_passage_JD"]
		self.Mean_motion				= elts["mean_motion"]
		self.Epoch						= elts["epochJD"]
		self.Mean_anomaly				= elts["mean_anomaly"]
		self.revolution					= elts["revolution"]
		self.OrbitClass					= elts["orbit_class"]

		# calculate current position based on orbital elements
		dT = daysSinceEpochJD(self.Epoch) + timeincrement # timeincrement comes in days
		# compute Longitude of Ascending node taking into account the time elapsed since epoch
		incrementYears = timeincrement / 365.25
		self.Longitude_of_ascendingnode +=  0.013967 * (2000.0 - (getCurrentYear() + incrementYears)) + 3.82394e-5 * dT

		# adjust Mean Anomaly with time elapsed since epoch
		M = toRange(self.Mean_anomaly + self.Mean_motion * dT)
		success, self.E, dE, it = solveKepler(M, self.e, 20000)
		if success == False:
			print self.Name+" Warning Could not converge - E = "+str(self.E)

	def getIncrement(self):
		# provide 1 degree increment in radians
		return pi/180

	def draw(self):
		self.Trail.visible = false
		rad_E = deg2rad(self.E)
		increment = self.getIncrement()

		for E in np.arange(increment, 2*pi+increment, increment):
			self.setPolarCoordinates(E+rad_E)
			# from R and Nu, calculate 3D coordinates and update current position
			self.updatePosition(E*180/pi)
			rate(5000)

		if self.BodyShape.visible:
			self.Trail.visible = true

		self.hasRenderedOrbit = True


	def setPolarCoordinates(self, E_rad):
		X = self.a * (cos(E_rad) - self.e)
		Y = self.a * sqrt(1 - self.e**2) * sin(E_rad)
		# Now calculate current Radius and true Anomaly
		self.R = sqrt(X**2 + Y**2)
		self.Nu = atan2(Y, X)
		# Note that atan2 returns an angle in
		# radian, so Nu is always in radian

	def updatePosition(self, trace = True):
		self.setCartesianCoordinates()
		self.BodyShape.pos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])
		if trace:
			if self.Position[Z_COOR] < 0:
				self.Interval += 1
				if self.Interval % 2 == 0:
					self.Trail.append(pos=self.BodyShape.pos, color=self.Color) #, interval=50)
				else:
					self.Trail.append(pos=self.BodyShape.pos, color=color.black) #, interval=50)
			else:
				self.Trail.append(pos=self.BodyShape.pos, color=self.Color)


	def setCartesianCoordinates(self):
		self.Position[X_COOR] = self.R * DIST_FACTOR * ( cos(self.N) * cos(self.Nu+self.w) - sin(self.N) * sin(self.Nu+self.w) * cos(self.i) )
		self.Position[Y_COOR] = self.R * DIST_FACTOR * ( sin(self.N) * cos(self.Nu+self.w) + cos(self.N) * sin(self.Nu+self.w) * cos(self.i) )
	 	self.Position[Z_COOR] = self.R * DIST_FACTOR * ( sin(self.Nu+self.w) * sin(self.i) )

		self.Position = self.Rotation_VernalEquinox * self.Position

	def show(self):
		if self.hasRenderedOrbit == False:
			self.draw()

		self.BodyShape.visible = True
		for i in range(len(self.Labels)):
			self.Labels[i].visible = True
		if self.solarsystem.ShowFeatures & ORBITS <> 0:
			self.Trail.visible = True
		else:
			self.Trail.visible = False
		if self.solarsystem.ShowFeatures & LABELS <> 0:
			for i in range(len(self.Labels)):
				self.Labels[i].visible = True
		else:
			for i in range(len(self.Labels)):
				self.Labels[i].visible = False
		if self.Ring:
			self.InnerRing.visible = True
			self.OutterRing.visible = True


	def hide(self):
		self.Details = False
		self.BodyShape.visible = False
		for i in range(len(self.Labels)):
			self.Labels[i].visible = False
		self.Trail.visible = False
		if self.Ring:
			self.InnerRing.visible = False
			self.OutterRing.visible = False


	def refresh(self):
		if self.solarsystem.SlideShowInProgress and self.BodyType == self.solarsystem.currentSource:
			return

		if self.BodyType & self.solarsystem.ShowFeatures <> 0 or self.Name == 'Earth' or self.Details == True:
			if self.BodyShape.visible == False:
				self.show()
		else:
			self.hide()

	def getCurrentOrbitRadius(self, angle_in_rd):
		self.CurrRadius = (self.a * (1 - self.e**2))/(1 + cos(angle_in_rd))
		return self.CurrRadius

	def getCurrentVelocity(self):
		# the formulat is v^2 = GM(2/r - 1/a)
		return sqrt(G*SUN_M*((2/self.R) - (1/self.a)))


class planet(makeBody):
	def __init__(self, system, index, color, trueAnomaly, type, sizeCorrectionType):
		makeBody.__init__(self, system, index, color, trueAnomaly, type, sizeCorrectionType)

	def makeShape(self):
		self.BodyShape = sphere(pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]), radius=self.radiusToShow/self.SizeCorrection[self.sizeType], make_trail=false)
		self.Angle = pi/2 + deg2rad(self.OrbitalObliquity)

	def getRealisticSizeCorrection(self):
		return 1/(DIST_FACTOR * 50)

	def toggleSize(self, realisticSize):
		x = 1 if realisticSize == True else 0
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		self.BodyShape.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]

		if self.Ring == True:
			self.InnerRing.visible = False
			self.OutterRing.visible = False
			self.InnerRing = None
			self.OutterRing = None
			self.solarsystem.makeRings(self.solarsystem, self.ObjectIndex)


	def setOrbitalElements(self, index, timeincrement = 0):
		# for the Major planets (default) includig Pluto, we have Keplerian
		# elements to calculate the body's current approximated position on orbit
		self.setOrbitalFromKeplerianElements(objects_data[index]["kep_elt"], timeincrement)


class comet(makeBody):
	def __init__(self, system, index, color, trueAnomaly):
		makeBody.__init__(self, system, index, color, trueAnomaly, COMET, COMET)

	def getIncrement(self):
		# for comets, due to their sometimes high eccentricity, an increment of 1 deg may not be small enough
		# to insure a smooth curve, hence we need to take smaller increments of 12.5 arcminutes or less in radians
		return pi/(180 * 4)

class asteroid(makeBody):
	def __init__(self, system, index, color, trueAnomaly):
		makeBody.__init__(self, system, index, color, trueAnomaly, BIG_ASTEROID, BIG_ASTEROID)

	def makeShape(self):
		self.BodyShape = sphere(pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]), radius=self.radiusToShow/self.SizeCorrection[self.sizeType], make_trail=false)
		self.Angle = pi/2 + deg2rad(self.OrbitalObliquity)

	def getRealisticSizeCorrection(self):
		return 1e-2/(DIST_FACTOR*5)

	def toggleSize(self, realisticSize):
		x = 1 if realisticSize == True else 0
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		self.BodyShape.radius = self.radiusToShow / self.SizeCorrection[self.sizeType]


class pha(makeBody):
	def __init__(self, system, index, color, trueAnomaly):
		makeBody.__init__(self, system, index, color, trueAnomaly, PHA, PHA)


class smallAsteroid(makeBody):
	def __init__(self, system, index, color, trueAnomaly):
		makeBody.__init__(self, system, index, color, trueAnomaly, SMALL_ASTEROID, SMALL_ASTEROID)


class dwarfPlanet(makeBody):
	def __init__(self, system, index, color, trueAnomaly):
		makeBody.__init__(self, system, index, color, trueAnomaly, DWARFPLANET, DWARFPLANET)

	def getRealisticSizeCorrection(self):
		return 1e-2/(DIST_FACTOR*5)

	def toggleSize(self, realisticSize):
		x = 1 if realisticSize == True else 0
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		self.BodyShape.radius = self.BodyRadius / self.SizeCorrection[self.sizeType]

	def makeShape(self):
		self.BodyShape = sphere(pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]), radius=self.radiusToShow/self.SizeCorrection[self.sizeType], make_trail=false)
		self.Angle = pi/2 + deg2rad(self.OrbitalObliquity)


class transNeptunian(makeBody):
	def __init__(self, system, index, color, trueAnomaly):
		makeBody.__init__(self, system, index, color, trueAnomaly, TRANS_NEPT, TRANS_NEPT)

#
# various functions
#
def getSigmoid(distance, correction):
	sigmoid = 1/(1+exp(-MAX_P_D/distance))
	return correction * sigmoid

# independent functions
def getSemiMajor(perihelion, eccentricity):
	# knowing the perihelion, the formula is given by rp = a(1-e)
	return perihelion /(1 - eccentricity)

def getSemiMinor(semimajor, eccentricity):
	# knowing the perihelion, the formula is given by rp = a(1-e)
	return semimajor * sqrt(1 - eccentricity**2)

def getAphelion(semimajor, eccentricity):
	# knowing the semi major, the formulat is ra = a(1+e)
	return semimajor * (1 + eccentricity)

def getOrbitalPeriod(semimajor):
	# knowing the semi major, the formulat is T = 2 pi sqrt(a^3/Mu)
	return 2*math.pi*sqrt((semimajor**3)/Mu)

def glbRefresh(solarSystem, animationInProgress):
	solarSystem.refresh(animationInProgress)
	for body in solarSystem.bodies:
		body.refresh()

def hideBelt(beltname):
	beltname.BodyShape.visible = false
	beltname.Labels[0].visible = false

def showBelt(beltname):
	beltname.BodyShape.visible = true
	beltname.Labels[0].visible = true

def getColor():
	return { 0: color.white, 1: color.red, 2: color.orange, 3: color.yellow, 4: color.cyan, 5: color.magenta, 6: color.green}[randint(0,6)]

# Calculates Eccentric Anomaly (E) given the mean anomaly (M) and the depth of the Bessel first kind functions
def bessel_E(M, e, depth):
    return (M + sum(2.0 / n * sp.jv(n, n * e) * np.sin(n * M)
                    for n in range(1, depth, 1)))

# Calculates Eccentric Anomaly (E) given the mean anomaly (M), the depth and the
# precision required using an iterative method. If the precision has been reached
# within the maximum iteration depth, returns (True, E, precision, #it) or
# (False, E, precision, #it) otherwise

def solveKepler(M, e, depth, precision = 1.e-8):
	M = deg2rad(M)
	threshold = deg2rad(precision)
	E0 = M
	it = 0
	while True:
		E1 = M + e*sin(E0)
		if abs(E1-E0) < threshold:
			return True, rad2deg(E0), rad2deg(E1-E0), it
		it = it + 1
		if it > depth:
			return False, rad2deg(E0), rad2deg(E1-E0), it
		E0 = E1

def toRange (angle):
	n = angle % 360
	if n < 0:
		n = n + 360
	return n

# Calculates the true anomaly (NU) and Radius given the Eccentric
# Anomaly (E), the orbit eccentricity and the semi-majour axis

def getTrueAnomalyAndRadius(E, e, a):
	ta = 2 * atan(sqrt((1+e)/(1-e)) * tan(E/2))
	R = a * (1 - e*cos(E))
	if ta < 0:
		ta = ta + 2*pi
	return ta, R

# load orbital parameters stored in a file
def loadBodies(solarsystem, type, filename, maxentries = 0):
	fo  = open(filename, "r")
	token = []
	maxentries = 1000 if maxentries == 0 else maxentries
	for line in fo:
		if line[0] == '#':
			continue
		else:
			token = line.split('|')
			if len(token) > 0:
				objects_data[token[JPL_DESIGNATION]] = {
					"material": 0,
					"name": token[JPL_FULLNAME],
					"iau_name": token[JPL_IAU_NAME],
					"jpl_designation": token[JPL_DESIGNATION],
					"mass": (float(token[JPL_GM])/G)*1.e+9 if token[JPL_GM] else 0, # convert km3 to m3
					"radius": float(token[JPL_DIAMETER])/2 if token[JPL_DIAMETER] else 0, #DEFAULT_RADIUS,
					"perihelion": float(token[JPL_OE_q]) * AU,
					"e": float(token[JPL_OE_e]),
					"revolution": float(token[JPL_OE_Pd]),
					"orbital_inclination": 	float(token[JPL_OE_i]),
					"longitude_of_ascendingnode":float(token[JPL_OE_N]),
					"argument_of_perihelion": float(token[JPL_OE_w]),
					"longitude_of_perihelion":float(token[JPL_OE_N])+float(token[JPL_OE_w]),
					"Time_of_perihelion_passage_JD":float(token[JPL_OE_tp_JD]),
					"mean_motion": float(token[JPL_OE_n]) if token[JPL_OE_n] else 0,
					"mean_anomaly": float(token[JPL_OE_M]) if token[JPL_OE_M] else 0,
					"epochJD": float(token[JPL_EPOCH_JD]),
					"earth_moid": (float(token[JPL_EARTH_MOID_AU])*AU) if token[JPL_EARTH_MOID_AU] else 0,
					"orbit_class":token[JPL_ORBIT_CLASS],
					"orbital_obliquity": 0 # in deg
				}
				body = {COMET: 			comet,
						BIG_ASTEROID: 	asteroid,
						PHA:			pha,
						TRANS_NEPT:		transNeptunian,
						SMALL_ASTEROID:	smallAsteroid,
						}[type](solarsystem, token[JPL_DESIGNATION], getColor(), 0)

				solarsystem.addTo(body)
				maxentries -= 1
				if maxentries <= 0:
					break
	fo.close()

def deg2rad(deg):
	return deg * math.pi/180

def rad2deg(rad):
	return rad * 180/math.pi

# ----------------
# TIME MANAGEMENT
# ----------------
def getJ2000():
	return 2451545.0

def getCurrentYear(year = 0):
	if year == 0:
		utc = datetime.datetime.utcnow()
		y = utc.year
	else:
		y = year
	return float(y)

def JDdaydiff(jd):
	# note that if jd corresponds to a date before 2000
	# jd - EPOCH_2000_JD will be a negative value
	return float(jd - EPOCH_2000_JD)

def MJDdaydiff(mjd):
	return float(mjd - EPOCH_2000_MJD)

# returns number of days since J2000 from current JDE
def JDE2day(jde):
	return float(jde - EPOCH_2000_JD)

# calculate the number of days since epoch
def currentdate2JDE():
	utc = datetime.datetime.utcnow()
	if utc.month <= 2:
		utc.year = utc.year-1
		utc.month = utc.month + 12
	return int(365.25*(utc.year+4716)) + int(30.6001*(utc.month+1)) + utc.day - 1524.5

def gregoriandate2JDE(year, month, day):
	if month <= 2:
		year = year-1
		month = month + 12
	A = int(year/100)
	B = 2 - A + int(A/4)
	return int(365.25*(year+4716)) + int(30.6001*(month+1)) + day + B - 1524.5

def JDEtoJulian(jdediff_indays):
	Y = jdediff_indays / 365.25
	years = int(Y)
	days = (Y - years)*365.25
	return days

def makeJulianDate(utc, delta):
	# Fliegel / Van Flandern Formula - "delta" is in days
	return delta + 367*utc.year - (7*(utc.year + ((utc.month+9)/12)))/4 + (275*utc.month)/9 + utc.day - 730530 + (utc.hour + utc.minute/60)/24

# will compute the number of days since J2000 UTC
def daysSinceJ2000UTC(delta = 0):
	utc = datetime.datetime.utcnow()
	return makeJulianDate(utc, delta)

def daysSinceEpochJD(julianDate):
	if julianDate == 0:
		# when epoch is not known, epoch is set to zero
		return 0
	# otherwise determine number of days since epoch
	days = daysSinceJ2000UTC() # days from 2000
	return days - (julianDate - EPOCH_2000_JD)

def daysSinceEpochJDfromUnixTimeStamp(UnixTimestamp):
	# Unix timestamp are the number of seconds since 01-01-1970 GMT.
	# first let's convert that number in a number of days, by a)
	# calculating the number of days since 1970 and b) add the number
	# of JULIAN DAYS corresponding to 01-01-1970
	ndays = (UnixTimeStamp / 86400.0) + EPOCH_1970_JD

	# second convert that number of days into the number of days since
	# 01-01-2000
	return daysSinceEpochJD(ndays)
