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
#from vpython import *
import numpy as np
from random import *
import scipy.special as sp
import datetime
import time
import sys

class solarSystem:

	INNER_RING_COEF = 1.3
	OUTER_RING_COEF = 1.9
	RING_INCREMENT = 0.6

	bodies = []

	def __init__(self):
		self.Name = "Sun"
		self.JPL_designation = "SUN"
		self.nameIndex = {}
		self.BodyRadius = SUN_R
		self.Mass = SUN_M
		self.AbortSlideShow = False
		self.SlideShowInProgress = False
		self.currentSource = PHA
		self.JTrojansIndex = -1
		self.currentPOV = None
		self.LocalRef = False
		self.currentPOVselection = "SUN"
		self.Scene = display(title = 'Solar System', width = 1300, height = 740, range=3, center = (0,0,0))

		self.Scene.lights = []
		self.Scene.forward = (2,0,-1) #(0,0,-1)
		self.Scene.fov = math.pi/3
		self.Scene.userspin = True
		self.Scene.userzoom = True
		self.Scene.autoscale = 1
		self.Scene.autocenter = False
		self.Scene.up = (0,0,1)
		self.RefAxis = [0,0,0]
		self.RefAxisLabel = ["","",""]
		self.Axis = [0,0,0]
		self.AxisLabel = ["","",""]
		self.TimeIncrement = INITIAL_TIMEINCR
		self.CorrectionSize = self.BodyRadius*DIST_FACTOR/1.e-2
		self.Rotation = 25.05 # in days
		self.RotAngle = 0
		self.AxialTilt = 7.25
		self.Position = vector(0,0,0)
		self.EarthRef = None
		self.ShowFeatures = 0

		# make all light coming from origin
		self.sunLight = local_light(pos=(0,0,0), color=color.white)
		self.Scene.ambient = color.black

		if THREE_D:
			self.Scene.stereo='redcyan'
			self.Scene.stereodepth = 1

		self.TiltAngle = deg2rad(self.AxialTilt)
		self.Rotation_ObliquityAroundY = np.matrix([
			[cos(self.TiltAngle), 0, 	sin(self.TiltAngle)],
			[0, 		 1, 		     0],
			[-sin(self.TiltAngle), 0,	cos(self.TiltAngle)]]
		)

		self.Rotation_Obliquity = np.matrix([
			[1,			0,			 		  0],
			[0,			cos(self.TiltAngle),	-sin(self.TiltAngle)],
			[0,			sin(self.TiltAngle), cos(self.TiltAngle)]]
		)

		self.BodyShape = sphere(pos=vector(0,0,0), radius=self.BodyRadius/self.CorrectionSize, color=color.white)
		self.BodyShape.material = materials.emissive

		# make referential
		self.makeAxis(3*AU*DIST_FACTOR, (0,0,0))
		self.initRotation()
		if self.isFeatured(CELESTIAL_SPHERE):
			self.makeCelestialSphere()

		#self.Scene.scale = self.Scene.scale/100


	def makeCelestialSphere(self): # Unused
		import os.path
		CELESTIAL_RADIUS = 10000
		#file = "./img/stars_const.tga"
		file = "./img/stars.tga"
		if os.path.isfile(file):
			self.UniversRadius = CELESTIAL_RADIUS * AU * DIST_FACTOR
			self.Universe = sphere(pos=vector(0,0,0), radius=self.UniversRadius, color=color.white)
			self.Universe.material = materials.texture(data=materials.loadTGA(file), mapping="spherical", interpolate=False)
		else:
			print ("Could find "+file)
		#self.Scene.scale = self.Scene.scale / 1e10


	def animate(self, deltaT):
		self.setRotation()

	def setRotation(self):
		self.RotAngle = abs((2*pi/self.Rotation)*self.TimeIncrement)
		self.BodyShape.rotate(angle=self.RotAngle, axis=self.RotAxis, origine=(0,0,0))

	def initRotation(self):
		# this is necessary to align the planet's texture properly
		self.BodyShape.rotate(angle=pi/2+self.TiltAngle, axis=self.XdirectionUnit, origine=(0,0,0))
		self.RotAxis = self.ZdirectionUnit

	def isFeatured(self, type):
		return self.ShowFeatures & type

	def setFeature(self, type, value):
		if value == True:
			self.ShowFeatures |= type
		else:
			self.ShowFeatures = (self.ShowFeatures & ~type)

	def getTimeIncrement(self):
		return self.TimeIncrement

	def setTimeIncrement(self, value):
		self.TimeIncrement = value

	def setDefaultFeatures(self, flags):
		self.ShowFeatures = flags

	def makeAxis(self, size, position):
		refDirections = [vector(size,0,0), vector(0,size,0), vector(0,0,size/4)]
		relsize = 2 * (self.BodyRadius/self.CorrectionSize)
		relDirections = [vector(relsize,0,0), vector(0,relsize,0), vector(0,0,relsize)]
		refText = ["x (vernal eq.)","y","z"]
		relText = ["x","y","z"]
		pos = vector(position)
		for i in range (3): # Each direction
			self.RefAxis[i] = curve( frame = None, color = color.white, pos= [ pos, pos+refDirections[i]], visible=False)
			self.RefAxisLabel[i] = label( frame = None, color = color.white,  text = refText[i],
										pos = pos+refDirections[i], opacity = 0, box = False, visible=False )
			A = np.matrix([[relDirections[i][0]],[relDirections[i][1]],[relDirections[i][2]]], np.float64)
			relDirections[i] = self.Rotation_Obliquity * A

			self.Axis[i] = curve( frame = None, color = color.white, pos= [ pos, pos+relDirections[i]], visible=False)
			self.AxisLabel[i] = label( frame = None, color = color.white,  text = relText[i],
										pos = pos+relDirections[i], opacity = 0, box = False, visible=False )

		ZdirectionVec = self.Axis[2].pos[1]-self.Axis[2].pos[0]
		YdirectionVec = self.Axis[1].pos[1]-self.Axis[1].pos[0]
		XdirectionVec = self.Axis[0].pos[1]-self.Axis[0].pos[0]

		self.ZdirectionUnit = ZdirectionVec/mag(ZdirectionVec)
		self.YdirectionUnit = YdirectionVec/mag(YdirectionVec)
		self.XdirectionUnit = XdirectionVec/mag(XdirectionVec)

	def resetView(self):
		self.Scene.center = (0,0,0)

	def addTo(self, body):
		self.bodies.append(body)
		i = len(self.bodies) - 1
		self.nameIndex[body.JPL_designation] = i
		if body.JPL_designation == 'EARTH':
			self.EarthRef = body
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
			if body.BodyType in [OUTERPLANET, INNERPLANET, SATELLITE, DWARFPLANET, KUIPER_BELT, ASTEROID_BELT, INNER_OORT_CLOUD, ECLIPTIC_PLANE]:
				body.draw()

		self.Scene.autoscale = 0

	def getBodyFromName(self, jpl_designation):
		if jpl_designation in self.nameIndex:
			return self.bodies[self.nameIndex[jpl_designation]]
		return None

	def isRealsize(self):
		if self.ShowFeatures & REALSIZE != 0:
				return True
		return False

	def refresh(self, animationInProgress = False):
		orbitTrace = False
		if self.ShowFeatures & ORBITS != 0:
			orbitTrace = True

		labelVisible = False
		if self.ShowFeatures & LABELS != 0:
			labelVisible = True

		realisticSize = False
		if self.ShowFeatures & REALSIZE != 0:
			realisticSize = True

		for body in self.bodies:
			if body.BodyType in [OUTERPLANET, INNERPLANET, ASTEROID, COMET, SATELLITE, DWARFPLANET, PHA, BIG_ASTEROID, TRANS_NEPT]:
				body.toggleSize(realisticSize)

				if body.BodyShape.visible == True:
					body.Trail.visible = orbitTrace
					if body.isMoon == True:
						if body.sizeType == SCALE_NORMALIZED: # apply label on/off when moon in real size
							value = labelVisible
						else:	# otherwise do not show label
							value = False
					else:
						value = labelVisible
					for i in range(len(body.Labels)):
						body.Labels[i].visible = value
			else: # belts / rings
				if body.BodyShape.visible == True and animationInProgress == True:
					body.BodyShape.visible = False
					for i in range(len(body.Labels)):
						body.Labels[i].visible = False

		if self.ShowFeatures & LIT_SCENE != 0:
			self.Scene.ambient = color.white
			self.sunLight.visible = False
			self.BodyShape.material = materials.texture(data=materials.loadTGA("./img/sun"), mapping="spherical", interpolate=False)
		else:
			self.Scene.ambient = color.black
			self.sunLight.visible = True
			self.BodyShape.material = materials.emissive

		setRefTo = True if self.ShowFeatures & REFERENTIAL != 0 else False

		if 	self.currentPOVselection == self.JPL_designation and \
			self.ShowFeatures & LOCAL_REFERENTIAL:
			setRelTo = True
		else:
			setRelTo = False

		self.setAxisVisibility(setRefTo, setRelTo)

	def refreshSAVE(self, animationInProgress = False):
		orbitTrace = False
		if self.ShowFeatures & ORBITS != 0:
			orbitTrace = True

		labelVisible = False
		if self.ShowFeatures & LABELS != 0:
			labelVisible = True

		realisticSize = False
		if self.ShowFeatures & REALSIZE != 0:
			realisticSize = True

		for body in self.bodies:
			if body.BodyType in [OUTERPLANET, INNERPLANET, ASTEROID, COMET, SATELLITE, DWARFPLANET, PHA, BIG_ASTEROID, TRANS_NEPT]:
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

		if self.ShowFeatures & LIT_SCENE != 0:
			self.Scene.ambient = color.white
			self.sunLight.visible = False
			self.BodyShape.material = materials.texture(data=materials.loadTGA("./img/sun"), mapping="spherical", interpolate=False)
		else:
			self.Scene.ambient = color.black
			self.sunLight.visible = True
			self.BodyShape.material = materials.emissive

		setRefTo = True if self.ShowFeatures & REFERENTIAL != 0 else False

		if 	self.currentPOVselection == self.JPL_designation and \
			self.ShowFeatures & LOCAL_REFERENTIAL:
			setRelTo = True
		else:
			setRelTo = False

		self.setAxisVisibility(setRefTo, setRelTo)

	def setAxisVisibility(self, setRefTo, setRelTo):
		for i in range(3):
			self.Axis[i].visible = setRelTo
			self.AxisLabel[i].visible = setRelTo
			self.RefAxis[i].visible = setRefTo
			self.RefAxisLabel[i].visible = setRefTo

	def setRings(self, system, bodyName, colorArray):  # change default values during instantiation
		global objects_data
		self.SolarSystem = system
		planet = self.getBodyFromName(objects_data[bodyName]['jpl_designation'])
		if planet != None:
			planet.Ring = true
			planet.nRings = len(colorArray)
			planet.RingColors = colorArray
			self.makeRings(planet)

	def makeRings(self, planet): #, system, bodyName, numberOfRings, colorArray):  # change default values during instantiation
		#print planet.RingThickness
		for i in range(0, planet.nRings):
			curRadius = planet.BodyRadius * (self.INNER_RING_COEF + i * self.RING_INCREMENT) / planet.SizeCorrection[planet.sizeType]
			planet.Rings.insert(i, cylinder(pos=(planet.Position[0], planet.Position[1], planet.Position[2]), radius=curRadius, color=planet.RingColors[i][0], length=(planet.RingThickness-(i*planet.RingThickness/10)), opacity=planet.RingColors[i][1], axis=planet.RotAxis))
			if (self.SolarSystem.ShowFeatures & planet.BodyType) == 0:
				planet.Rings[i].visible = False

	def hideRings(self, planet):
		for i in range(0, planet.nRings):
			planet.Rings[i].visible = False

	def showRings(self, planet):
		for i in range(0, planet.nRings):
			planet.Rings[i].visible = True

	def setRingsPosition(self, planet):
		for i in range(0, planet.nRings):
			planet.Rings[i].pos = planet.BodyShape.pos #self.Position

	def makeRingsSAVE(self, planet): #, system, bodyName, numberOfRings, colorArray):  # change default values during instantiation
		for i in range(0, planet.nRings):
			curRadius = planet.BodyRadius * (self.INNER_RING_COEF + i * self.RING_INCREMENT) / planet.SizeCorrection[planet.sizeType]
			planet.Rings.insert(i, cylinder(pos=(planet.Position[0], planet.Position[1], planet.Position[2]), radius=curRadius, color=planet.RingColors[i][0], length=200-(i*20), opacity=planet.RingColors[i][1], axis=planet.RotAxis))
			if (self.SolarSystem.ShowFeatures & planet.BodyType) == 0:
				planet.Rings[i].visible = False
				planet.Rings[i].visible = False

	def makeRingsSAVE(self, system, bodyName):  # change default values during instantiation
		global objects_data
		self.SolarSystem = system
		planet = self.getBodyFromName(objects_data[bodyName]['jpl_designation'])
		if planet != None:
			InnerRadius = planet.BodyRadius * self.INNER_RING_COEF / planet.SizeCorrection[planet.sizeType]
			#DarkRadius = planet.BodyRadius * (self.INNER_RING_COEF+self.OUTER_RING_COEF)/ 1.5 / planet.SizeCorrection[planet.sizeType]
			OuterRadius = planet.BodyRadius * self.OUTER_RING_COEF / planet.SizeCorrection[planet.sizeType]
			planet.Ring = true

			planet.InnerRing = cylinder(pos=(planet.Position[0], planet.Position[1], planet.Position[2]), radius=InnerRadius, color=color.gray(0.7), length=100, opacity=1, axis=planet.RotAxis)
			#planet.DarkRing = cylinder(pos=(planet.Position[0], planet.Position[1], planet.Position[2]), radius=DarkRadius, color=color.black, length=80, opacity=1, axis=planet.RotAxis)
			planet.OuterRing = cylinder(pos=(planet.Position[0], planet.Position[1], planet.Position[2]), radius=OuterRadius, color=(0.5,0.5,0.5), length=60, opacity=0.5, axis=planet.RotAxis)

			if (self.SolarSystem.ShowFeatures & planet.BodyType) == 0:
				planet.InnerRing.visible = False
				planet.OuterRing.visible = False

	def makeRingsCircles(self, system, bodyName, density = 1):  # change default values during instantiation
		global objects_data
		self.SolarSystem = system
		planet = self.getBodyFromName(objects_data[bodyName]['jpl_designation'])
		if planet != None:
			InnerRadius = planet.BodyRadius * self.INNER_RING_COEF / planet.SizeCorrection[planet.sizeType]
			OuterRadius = planet.BodyRadius * self.OUTER_RING_COEF / planet.SizeCorrection[planet.sizeType]
			planet.Ring = true
			planet.InnerRing = curve(color=planet.Color)
			planet.OuterRing = curve(color=planet.Color)

			if (self.SolarSystem.ShowFeatures & planet.BodyType) == 0:
				planet.InnerRing.visible = false
				planet.OuterRing.visible = false

			Position = np.matrix([[0],[0],[0]])
			#angle = planet.Angle + pi/2
			angle = deg2rad(planet.AxialTilt)
			Rotation_3D = np.matrix([
				[1, 0, 					0],
				[0, cos(angle), 	-sin(angle)],
				[0, sin(angle), 	cos(angle)]]
			)

			for i in np.arange(0, 2*pi, pi/(180*density)):
				Position = [[(OuterRadius * cos(i))], [(OuterRadius * sin(i))], [0]]
				Position = Rotation_3D * Position + planet.Position
				planet.OuterRing.append(pos=(Position[X_COOR], Position[Y_COOR], Position[Z_COOR]), color=planet.Color) #radius=pointRadius/planet.SizeCorrection, size=1)

				Position = [[(InnerRadius * cos(i))], [(InnerRadius * sin(i))], [0]]
				Position = Rotation_3D * Position + planet.Position
				planet.InnerRing.append(pos=(Position[X_COOR], Position[Y_COOR], Position[Z_COOR]), color=planet.Color) #radius=pointRadius/planet.SizeCorrection, size=1)


class makeEcliptic:

	def __init__(self, system, color):  # change default values during instantiation
		# draw a circle of 250 AU
		self.Labels = []
		self.Name = "Ecliptic Plane"
		self.Iau_name = "ecliptic"
		self.JPL_designation = "ecliptic"
		self.SolarSystem = system
		self.Color = color
		self.BodyType = ECLIPTIC_PLANE
		self.Labels.append(label(pos=(250*AU*DIST_FACTOR, 250*AU*DIST_FACTOR, 0), text=self.Name, xoffset=20, yoffset=12, space=0, height=10, border=6, box=false, font='sans', visible = False))

	def refresh(self):
		if self.SolarSystem.ShowFeatures & ECLIPTIC_PLANE != 0:
			self.BodyShape.visible = True
		else:
			self.BodyShape.visible = False

	def draw(self):
		self.BodyShape = cylinder(pos=vector(0,0,0), radius=250*AU*DIST_FACTOR, color=self.Color, length=10, opacity=0.1, axis=(0,0,1))
		self.BodyShape.visible = False


class makeBelt:

	def __init__(self, system, index, name, bodyType, color, size, density = 1, planetname = None):  # change default values during instantiation
		self.Labels = []
		self.Name = name
		self.Iau_name = name
		self.JPL_designation = name
		self.SolarSystem = system
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
		if self.SolarSystem.ShowFeatures & self.BodyType != 0:
			if self.BodyShape.visible == False:
				self.BodyShape.visible = True

			if self.SolarSystem.ShowFeatures & LABELS != 0:
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
		self.Planet = self.SolarSystem.getBodyFromName(objects_data[self.PlanetName]['jpl_designation'])
		if self.Planet != None:
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

	RING_BASE_THICKNESS = 2000
	def __init__(self, system, index, color, bodyType = INNERPLANET, sizeCorrectionType = INNERPLANET, RealisticCorrectionSize = SMALLBODY_SZ_CORRECTION, satelliteof = None):  # change default values during instantiation

		self.Labels = []
		self.SatelliteOf = satelliteof
		self.isMoon = False
		self.RealisticCorrectionSize = RealisticCorrectionSize

		#if satelliteof == None:
		#	self.Foci = vector(0,0,0)
		#else:
		self.Foci = vector(satelliteof.Position[X_COOR], satelliteof.Position[Y_COOR], satelliteof.Position[Z_COOR])

		self.ObjectIndex = index
		self.SolarSystem 			= system
		self.Ring 					= False
		self.AxialTilt				= objects_data[index]["axial_tilt"]
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
		self.Absolute_mag			= objects_data[index]["absolute_mag"]
		self.Axis 					= [None,None,None]
		self.AxisLabel 				= ["","",""]
		# for planets with rings
		self.Rings = []
		#w, h = 8, 2;
		#self.Rings = [[0 for x in range(w)] for y in range(h)]

		self.nRings = 0
		self.RingColors = []

		self.sizeCorrectionType = sizeCorrectionType
		self.BodyShape = None

		self.Rotation = objects_data[index]["rotation"] if "rotation" in objects_data[index] else 0
		self.RotAngle = 0

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
		self.directions = [vector(0,0,0),vector(0,0,0),vector(0,0,0)]
		self.Interval = 0
		self.SizeCorrection = [1] * 2
		self.sizeType = SCALE_OVERSIZED

		self.Position = np.matrix([[0],[0],[0]], np.float64)

		# 180 rotation so that vernal equinox points towards left
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
		self.i = deg2rad(self.Inclination)

		# convert polar to Cartesian in Sun referential
		self.setCartesianCoordinates()

		#sizeCorrection = { INNERPLANET: 1200, SATELLITE:1400, GASGIANT: 1900, DWARFPLANET: 100, ASTEROID:1, COMET:0.02, SMALL_ASTEROID: 0.1, BIG_ASTEROID:0.1, PHA: 0.0013, TRANS_NEPT: 0.001}[sizeCorrectionType]
		sizeCorrection = { INNERPLANET: 1200, SATELLITE:1400, GASGIANT: 3500, DWARFPLANET: 100, ASTEROID:1, COMET:0.02, SMALL_ASTEROID: 0.1, BIG_ASTEROID:0.1, PHA: 0.0013, TRANS_NEPT: 0.001}[sizeCorrectionType]
		self.shape = { INNERPLANET: "sphere", OUTERPLANET: "sphere", SATELLITE: "sphere", DWARFPLANET: "sphere", ASTEROID:"cube", COMET:"cone", SMALL_ASTEROID:"cube", BIG_ASTEROID:"sphere", PHA:"cube", TRANS_NEPT: "cube"}[bodyType]

		self.SizeCorrection[0] = getSigmoid(self.Perihelion, sizeCorrection)
		self.SizeCorrection[1] = self.RealisticCorrectionSize #self.getRealisticSizeCorrection()

		self.RingThickness = self.RING_BASE_THICKNESS / self.SizeCorrection[self.sizeType]

		if self.BodyRadius < DEFAULT_RADIUS:
			self.radiusToShow = DEFAULT_RADIUS
		else:
			self.radiusToShow = self.BodyRadius

		self.makeShape()

		# attach a curve to the object to display its orbit
		if self.BodyShape != None:
			self.Trail = curve(color=self.Color)
			self.Trail.append(pos=self.BodyShape.pos)
		else:
			return

		#angle = deg2rad(self.AxialTilt)
		self.TiltAngle = deg2rad(self.AxialTilt+self.Inclination) # in the ecliptic coordinates system
		#angle = deg2rad(45) #self.Inclination) # in the ecliptic coordinates system
		#angle = 0
		cosv = cos(self.TiltAngle)
		sinv = sin(self.TiltAngle)

		self.Rotation_ObliquityAroundY = np.matrix([
			[cosv, 		0, 		sinv],
			[0, 		1, 		0	],
			[-sinv, 	0,		cosv]]
		)
		self.Rotation_Obliquity = np.matrix([
			[1,			0,		0	],
			[0,			cosv,  -sinv],
			[0,			sinv, 	cosv]]
		)

		self.Rotation_Obliquity_SatCorrection = np.matrix([
			[1,			0,		0	],
			[0,			cosv,	sinv],
			[0,		   -sinv, 	cosv]]
		)

		# add LEGEND
		self.Labels.append(label(pos=(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]), text=self.Name, xoffset=20, yoffset=12, space=0, height=10, color=color, border=6, box=false, font='sans'))

		if (self.SolarSystem.ShowFeatures & bodyType) == 0:
			self.BodyShape.visible = False
			self.Labels[0].visible = False

		self.makeAxis(self.radiusToShow/self.SizeCorrection[self.sizeType], self.Position) #(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]))
		self.setAspect(index)
		self.initRotation()

	def setAspect(self, index):
		data = materials.loadTGA("./img/"+index) if objects_data[index]["material"] != 0 else materials.loadTGA("./img/asteroid")
		self.BodyShape.material = materials.texture(data=data, mapping="spherical", interpolate=False)

	def makeShape(self):
		self.BodyShape = sphere(pos=(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]), radius=self.radiusToShow/self.SizeCorrection[self.sizeType], make_trail=false)

	def makeAxis(self, size, position):
		self.directions = [vector(2*size,0,0), vector(0,2*size,0), vector(0,0,2*size)]
		texts = ["x","y","z"]
		pos = vector(position)
		for i in range (3): # Each direction
			A = np.matrix([[self.directions[i][0]],[self.directions[i][1]],[self.directions[i][2]]], np.float64)
			self.directions[i] = self.Rotation_Obliquity * A

			self.Axis[i] = curve( frame = None, color = color.white, pos= [ pos, pos+self.directions[i]], visible=False)
			self.AxisLabel[i] = label( frame = None, color = color.white,  text = texts[i],
										pos = pos+self.directions[i], opacity = 0, box = False, visible=False )

		ZdirectionVec = self.Axis[2].pos[1]-self.Axis[2].pos[0]
		YdirectionVec = self.Axis[1].pos[1]-self.Axis[1].pos[0]
		XdirectionVec = self.Axis[0].pos[1]-self.Axis[0].pos[0]

		self.ZdirectionUnit = ZdirectionVec/mag(ZdirectionVec)
		self.YdirectionUnit = YdirectionVec/mag(YdirectionVec)
		self.XdirectionUnit = XdirectionVec/mag(XdirectionVec)
		"""
		if self.Name == 'Earth':
			print "X="+str(self.XdirectionUnit)
			print "Y="+str(self.YdirectionUnit)
			print "Z="+str(self.ZdirectionUnit)
		"""

	def updateAxis(self):
		pos = vector(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR])
		for i in range (3): # Each direction
			self.Axis[i].pos = [ pos, pos+self.directions[i]]
			self.AxisLabel[i].pos = pos+self.directions[i]

	def getRealisticSizeCorrection(self):
		return self.RealisticCorrectionSize
		#SMALLBODY_SZ_CORRECTION = 1e-6/(DIST_FACTOR*5)
		#return 1e-6/(DIST_FACTOR*5)

	def setRealisticSizeCorrection(self, value):
		self.RealisticCorrectionSize = value

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x
		self.BodyShape.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]

	def setTraceAndLabelVisibility(self, value):
		if self.BodyShape.visible == True:
			self.Trail.visible = value
			for i in range(len(self.Labels)):
				self.Labels[i].visible = value

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
		self.i = deg2rad(self.Inclination)

		# convert polar to Cartesian in Sun referential
		self.setCartesianCoordinates()
		# update foci position
		#if self.SatelliteOf != None:
		self.Foci = self.SatelliteOf.Position
			#self.Trail.pos = self.Foci

		self.BodyShape.pos = vector(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR])
		self.Labels[0].pos = vector(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR])
		self.setRotation()
		if self.Ring == True:
			self.SolarSystem.setRingsPosition(self)
			#for i in range(0, self.nRings):
			#	self.Rings[i].pos = self.BodyShape.pos #self.Position
			#self.SolarSystem.makeRings(self) #self.SolarSystem, self.ObjectIndex)

		return self.getCurrentVelocity(), self.getCurrentDistanceFromEarth()

	def setOrbitalElements(self, index, timeincrement = 0):
		# For comets, asteroids or dwarf planets, data comes from data
		# files -or- predefined values. Orbital Position is calculated
		# from the last time of perihelion passage. This is the default
		# behavior
		self.setOrbitalFromPredefinedElements(objects_data[index], timeincrement) #-0.7)

	# unused
	def setEarthOrbitalFromKeplerianElements(self, elts, timeincrement):
		# get number of days since J2000 epoch and obtain the fraction of century
		# (the rate adjustment is given as a rate per century)
		days = daysSinceJ2000UTC() + timeincrement # what the hell was that thing - 1.5
		#T = (daysSinceJ2000UTC() + timeincrement)/36525. # T is in centuries
		T = days/36525. # T is in centuries

		#self.a = (elts["a"] + (elts["ar"] * T)) * AU
		self.a = 1.000001018 * AU

		#self.e = elts["e"] + (elts["er"] * T)
		self.e = 0.01670862 - (0.000042037 * T) - (0.0000001236 * T**2) + (0.00000000044 * T**3)

		#self.Inclination = elts["i"] + (elts["ir"] * T)
		self.Inclination = 0.0 + (0.0130546 * T) - (0.00000931 * T**2) - (0.000000034 * T**3)

		# compute mean Longitude with correction factors beyond jupiter M = L - W + bT^2 +ccos(ft) + ssin(ft)
		"""
		L = elts["L"] + (elts["Lr"] * T) + (elts["b"] * T**2  +
											elts["c"] * cos(elts["f"] * T) +
											elts["s"] * sin(elts["f"] * T))
		"""
		L = 100.466449 + (35999.3728519 * T) - (0.00000568 * T**2)

		#self.Longitude_of_perihelion = elts["W"] + (elts["Wr"] * T)
		self.Longitude_of_perihelion = 102.937348 + (0.3225557 * T) + (0.00015026 * T**2) + (0.000000478 * T**3)

		#self.Longitude_of_ascendingnode = elts["N"] + (elts["Nr"] * T)
		self.Longitude_of_ascendingnode =  0.0

		# compute Argument of perihelion w
		self.Argument_of_perihelion = self.Longitude_of_perihelion - self.Longitude_of_ascendingnode

		# compute mean Anomaly M = L - W
		M = toRange(L - self.Longitude_of_perihelion) #W)

		# Obtain ecc. Anomaly E (in degrees) from M using an approx method of resolution:
		success, self.E, dE, it = solveKepler(M, self.e, 12000)
		if success == False:
			print ("Could not converge for "+self.Name+", E = "+str(self.E)+", last precision = "+str(dE))



	# will calculate current value of approximate position of the major planets
	# including pluto. This won't work for Asteroid, Comets or Dwarf planets
	def setOrbitalFromKeplerianElements(self, elts, timeincrement):
		# get number of days since J2000 epoch and obtain the fraction of century
		# (the rate adjustment is given as a rate per century)
		days = daysSinceJ2000UTC() + timeincrement - ADJUSTMENT_FACTOR_PLANETS # - 1.43
		#T = (daysSinceJ2000UTC() + timeincrement)/36525. # T is in centuries
		T = days/36525. # T is in centuries

		self.a = (elts["a"] + (elts["ar"] * T)) * AU
		self.e = elts["e"] + (elts["er"] * T)
		self.Inclination = elts["i"] + (elts["ir"] * T)

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
			print ("Could not converge for "+self.Name+", E = "+str(self.E)+", last precision = "+str(dE))


	def setOrbitalFromPredefinedElements(self, elts, timeincrement):
		# data comes from data file or predefined values
		self.e 							= elts["e"]
		self.Longitude_of_perihelion 	= elts["longitude_of_perihelion"]
		self.Longitude_of_ascendingnode = elts["longitude_of_ascendingnode"]
		self.Argument_of_perihelion 	= self.Longitude_of_perihelion - self.Longitude_of_ascendingnode
		self.a 							= getSemiMajor(self.Perihelion, self.e)
		self.Inclination 				= elts["orbital_inclination"]
		self.Time_of_perihelion_passage = elts["Time_of_perihelion_passage_JD"]
		self.Mean_motion				= elts["mean_motion"]
		self.Epoch						= elts["epochJD"]
		self.Mean_anomaly				= elts["mean_anomaly"]
		self.revolution					= elts["revolution"]
		self.OrbitClass					= elts["orbit_class"]

		# calculate current position based on orbital elements
		#dT = daysSinceEpochJD(self.Epoch) + timeincrement # timeincrement comes in days
		dT = daysSinceEpochJD(self.Epoch) + timeincrement - ADJUSTMENT_FACTOR # - 0.6 # timeincrement comes in days
		# compute Longitude of Ascending node taking into account the time elapsed since epoch
		incrementYears = timeincrement / 365.25
		self.Longitude_of_ascendingnode +=  0.013967 * (2000.0 - (getCurrentYear() + incrementYears)) + 3.82394e-5 * dT

		# adjust Mean Anomaly with time elapsed since epoch
		M = toRange(self.Mean_anomaly + self.Mean_motion * dT)
		success, self.E, dE, it = solveKepler(M, self.e, 20000)
		if success == False:
			print (self.Name+" Warning Could not converge - E = "+str(self.E))

	def getIncrement(self):
		# provide 1 degree increment in radians
		return pi/180

	def draw(self):

		self.Trail.visible = False
		rad_E = deg2rad(self.E)
		increment = self.getIncrement()

		for E in np.arange(increment, 2*pi+increment, increment):
			self.setPolarCoordinates(E+rad_E)
			# from R and Nu, calculate 3D coordinates and update current position
			self.updatePosition(trace=True) #E*180/pi)
			rate(5000)

		if self.BodyShape.visible:
			self.Trail.visible = True

		self.hasRenderedOrbit = True


	def setPolarCoordinates(self, E_rad):
		X = self.a * (cos(E_rad) - self.e)
		Y = self.a * sqrt(1 - self.e**2) * sin(E_rad)
		# Now calculate current Radius and true Anomaly
		self.R = sqrt(X**2 + Y**2)
		self.Nu = atan2(Y, X)
		# Note that atan2 returns an angle in
		# radian, so Nu is always in radian

	# default initRotation behavior
	def initRotation(self):
		# this is necessary to align the planet's texture properly
		self.BodyShape.rotate(angle=(pi/2+self.TiltAngle), axis=self.XdirectionUnit, origine=(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]))
		self.RotAxis = self.ZdirectionUnit

		# calculate current RA, to position the obliquity properly:
		if "RA_1" in objects_data[self.ObjectIndex]:
			T = daysSinceJ2000UTC()/36525. # T is in centuries
			self.RA = objects_data[self.ObjectIndex]["RA_1"] + objects_data[self.ObjectIndex]["RA_2"] * T
			self.BodyShape.rotate(angle=deg2rad(self.RA), axis=self.ZdirectionUnit, origine=(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]))
		#else:
		#	print "No RA for " +self.Name



	# default
	def setRotation(self):
		ti = self.SolarSystem.getTimeIncrement()
		self.RotAngle = abs((2*pi/self.Rotation)*ti)
		if ti < 0:
			self.RotAngle *= -1

		self.updateAxis()
		self.BodyShape.rotate(angle=self.RotAngle, axis=self.RotAxis, origine=(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]))

	def updatePosition(self, trace = True):
		self.setCartesianCoordinates()
		self.BodyShape.pos = vector(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR])
		if trace:
			if self.Position[Z_COOR]+self.Foci[Z_COOR] < 0:
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

		if self.SolarSystem.ShowFeatures & ORBITS != 0:
			self.Trail.visible = True
		else:
			self.Trail.visible = False

		if self.SolarSystem.ShowFeatures & LABELS != 0:
			for i in range(len(self.Labels)):
				self.Labels[i].visible = True
		else:
			for i in range(len(self.Labels)):
				self.Labels[i].visible = False

		if self.Ring:
			self.SolarSystem.showRings(self)
			#for i in range(0, self.nRings):
			#	self.Rings[i].visible = True

	def hide(self):
		self.Details = False
		self.BodyShape.visible = False
		for i in range(len(self.Labels)):
			self.Labels[i].visible = False
		self.Trail.visible = False
		if self.Ring:
			#self.InnerRing.visible = False
			self.SolarSystem.hideRings(self)
			#self.OuterRing.visible = False

	def setAxisVisibility(self, setTo):
		for i in range(3):
			self.Axis[i].visible = setTo
			self.AxisLabel[i].visible = setTo

	def refresh(self):
		if self.SolarSystem.SlideShowInProgress and self.BodyType == self.SolarSystem.currentSource:
			return

		if self.BodyType & self.SolarSystem.ShowFeatures != 0 or self.Name == 'Earth' or self.Details == True:
			if self.BodyShape.visible == False:
				self.show()
			# if this is the currentPOV, check for local referential attribute
			if 	self.SolarSystem.currentPOVselection == self.JPL_designation and \
				self.SolarSystem.ShowFeatures & LOCAL_REFERENTIAL:
					setTo = True
			else:
					setTo = False

			self.setAxisVisibility(setTo)
		else:
			self.hide()
			self.setAxisVisibility(False)

	def getCurrentOrbitRadius(self, angle_in_rd):
		self.CurrRadius = (self.a * (1 - self.e**2))/(1 + cos(angle_in_rd))
		return self.CurrRadius

	def getCurrentVelocity(self):
		# the formulat is v^2 = GM(2/r - 1/a)
		return sqrt(G*SUN_M*((2/self.R) - (1/self.a)))

	def getCurrentDistanceFromEarth(self):
		return sqrt((self.Position[X_COOR] - self.SolarSystem.EarthRef.Position[X_COOR])**2 + \
					(self.Position[Y_COOR] - self.SolarSystem.EarthRef.Position[Y_COOR])**2 + \
					(self.Position[Z_COOR] - self.SolarSystem.EarthRef.Position[Z_COOR])**2)/DIST_FACTOR/AU

class planet(makeBody):
	def __init__(self, system, index, color, type, sizeCorrectionType, defaultSizeCorrection):
		makeBody.__init__(self, system, index, color, type, sizeCorrectionType, defaultSizeCorrection, system)

	def getRealisticSizeCorrectionXX(self):
		#return 1/(DIST_FACTOR * 50)
		#PLANET_SZ_CORRECTION = 1/(DIST_FACTOR * 5)
		return 1/(DIST_FACTOR * 5)

	def toggleSize(self, realisticSize):

		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		self.BodyShape.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]
		self.RingThickness = self.RING_BASE_THICKNESS / self.SizeCorrection[self.sizeType]
		if self.Ring == True:
			for i in range(0, self.nRings):
				self.Rings[i].visible = False
				self.Rings[i] = None
			self.SolarSystem.makeRings(self) #self.SolarSystem, self.ObjectIndex)

	def setOrbitalElements(self, index, timeincrement = 0):
		# for the Major planets (default) includig Pluto, we have Keplerian
		# elements to calculate the body's current approximated position on orbit
		elt = objects_data[index]["kep_elt_1"] if "kep_elt_1" in objects_data[index] else objects_data[index]["kep_elt"]
		"""
		if self.Name == 'Earth':
			#print "EARTH ORBITAL ELTS"
			self.setEarthOrbitalFromKeplerianElements(elt, timeincrement) #)-0.75)
		else:
		"""
		self.setOrbitalFromKeplerianElements(elt, timeincrement) #-1.4) #0.7)
		#self.setOrbitalFromKeplerianElements(objects_data[index]["kep_elt"], timeincrement)

class satellite(makeBody):
	def __init__(self, system, index, color, planetBody):
		#if planetBody != None:
		#	print objects_data[index]['name']+" is a satellite of: "+planetBody.Name
		makeBody.__init__(self, system, index, color, SATELLITE, SATELLITE, SATELLITE_SZ_CORRECTION, planetBody)
		self.isMoon = True

	def getRealisticSizeCorrectionXX(self):
		#SATELLITE_SZ_CORRECTION = 1/(DIST_FACTOR * 5)
		return 1/(DIST_FACTOR * 5)

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		if self.SolarSystem.isFeatured(self.SatelliteOf.BodyType):
			if self.sizeType == SCALE_OVERSIZED:
				self.Labels[0].visible = False
			else:
				self.Labels[0].visible = True

		self.BodyShape.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]

	def setCartesianCoordinatesXX(self):
		self.Position[X_COOR] = self.R * DIST_FACTOR * ( cos(self.N) * cos(self.Nu+self.w) - sin(self.N) * sin(self.Nu+self.w) * cos(self.i) )
		self.Position[Y_COOR] = self.R * DIST_FACTOR * ( sin(self.N) * cos(self.Nu+self.w) + cos(self.N) * sin(self.Nu+self.w) * cos(self.i) )
		self.Position[Z_COOR] = self.R * DIST_FACTOR * ( sin(self.Nu+self.w) * sin(self.i) )

		self.Position = self.Rotation_VernalEquinox * self.SatelliteOf.Rotation_Obliquity_SatCorrection * self.Position

	def draw(self):
		#print "drawing "+self.Name
		self.Trail.visible = False
		rad_E = deg2rad(self.E)
		increment = self.getIncrement()

		for E in np.arange(increment, 2*pi+increment, increment):
			self.setPolarCoordinates(E+rad_E)
			# from R and Nu, calculate 3D coordinates and update current position
			self.updatePosition(trace=false) #E*180/pi, False)
			#rate(5000)

		self.hasRenderedOrbit = True

class hyperbolic(makeBody):
	def __init__(self, system, index, color, planetBody):
		makeBody.__init__(self, system, index, color, HYPERBOLIC, HYPERBOLIC, HYPERBOLIC_SZ_CORRECTION, planetBody)
		self.isMoon = false

	def getRealisticSizeCorrectionXX(self):
		#SATELLITE_SZ_CORRECTION = 1/(DIST_FACTOR * 5)
		return 1/(DIST_FACTOR * 5)

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		if self.SolarSystem.isFeatured(self.SatelliteOf.BodyType):
			if self.sizeType == SCALE_OVERSIZED:
				self.Labels[0].visible = False
			else:
				self.Labels[0].visible = True

		self.BodyShape.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]

	def setPolarCoordinates(self, E_rad):
		# calculate coordinates for an hyperbolic curve
		X = self.a * (cos(E_rad) - self.e)
		Y = self.a * sqrt(1 - self.e**2) * sin(E_rad)
		# Now calculate current Radius and true Anomaly
		self.R = sqrt(X**2 + Y**2)
		self.Nu = atan2(Y, X)
		# Note that atan2 returns an angle in
		# radian, so Nu is always in radian

	def draw(self):
		#print "drawing "+self.Name
		self.Trail.visible = False
		rad_E = deg2rad(self.E)
		increment = self.getIncrement()

		for E in np.arange(increment, 2*pi+increment, increment):
			self.setPolarCoordinates(E+rad_E)
			# from R and Nu, calculate 3D coordinates and update current position
			self.updatePosition(trace=False) #E*180/pi, False)
			#rate(5000)

		self.hasRenderedOrbit = True

class comet(makeBody):
	def __init__(self, system, index, color):
		makeBody.__init__(self, system, index, color, COMET, COMET, SMALLBODY_SZ_CORRECTION, system)

	def makeShape(self):
		self.BodyShape = ellipsoid(	pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]),
									length=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType], make_trail=false)
	def setAspect(self, index):
		# we don't need index for comets
		#self.BodyShape.material = materials.marble
		data = materials.loadTGA("./img/comet")
		self.BodyShape.material = materials.texture(data=data, mapping="spherical", interpolate=False)


	def initRotation(self):
		self.RotAngle = pi/6
		self.RotAxis = (1,1,1)

	def setRotation(self):
		#self.updateAxis()
		self.BodyShape.rotate(angle=self.RotAngle, axis=self.RotAxis, origine=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])) #-sin(alpha), cos(alpha)))

	def makeAxis(self, size, position):
		return

	def setAxisVisibility(self, setTo):
		return

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		asteroidRandom = [(randint(10, 20)/10, randint(10, 20)/10, randint(10, 20)/10), (1,1,1)]
		self.BodyShape.length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyShape.height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyShape.width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

	def getIncrement(self):
		# for comets, due to their sometimes high eccentricity, an increment of 1 deg may not be small enough
		# to insure a smooth curve, hence we need to take smaller increments of 12.5 arcminutes or less in radians
		return pi/(180 * 4)

class asteroid(makeBody):
	def __init__(self, system, index, color):
		makeBody.__init__(self, system, index, color, BIG_ASTEROID, BIG_ASTEROID, ASTEROID_SZ_CORRECTION, system)

	def initRotation(self):
		self.RotAngle = pi/6
		self.RotAxis = (1,1,1)

	def setRotation(self):
		self.BodyShape.rotate(angle=self.RotAngle, axis=self.RotAxis, origine=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])) #-sin(alpha), cos(alpha)))

	def makeAxis(self, size, position):
		return

	def setAxisVisibility(self, setTo):
		return

	def getRealisticSizeCorrectionXX(self):
		#ASTEROID_SZ_CORRECTION = 1e-2/(DIST_FACTOR*5)
		return 1e-2/(DIST_FACTOR*5)


class pha(makeBody):
	def __init__(self, system, index, color):
		makeBody.__init__(self, system, index, color, PHA, PHA, SMALLBODY_SZ_CORRECTION, system)

	def makeShape(self):
		"""
		self.BodyShape = ellipsoid(	pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]),
									length=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType], make_trail=false)
		"""
		asteroidRandom = [(1.5, 2, 1), (1.5, 2, 1)]
		self.BodyShape = ellipsoid(	pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]),
									length=(self.radiusToShow * asteroidRandom[self.sizeType][0])/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * asteroidRandom[self.sizeType][1])/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * asteroidRandom[self.sizeType][2])/self.SizeCorrection[self.sizeType], make_trail=false)

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		#asteroidRandom = [(randint(10, 20)/10, randint(10, 20)/10, randint(10, 20)/10), (1,1,1)]
		asteroidRandom = [(1.5, 2, 1), (1.5, 2, 1)]
		self.BodyShape.length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyShape.height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyShape.width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

	def initRotation(self):
		self.RotAngle = pi/6
		self.RotAxis = (1,1,1)

	def setRotation(self):
		#self.updateAxis()
		self.BodyShape.rotate(angle=self.RotAngle, axis=self.RotAxis, origine=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])) #-sin(alpha), cos(alpha)))

	def makeAxis(self, size, position):
		return

	def setAxisVisibility(self, setTo):
		return

class smallAsteroid(makeBody):
	def __init__(self, system, index, color):
		makeBody.__init__(self, system, index, color, SMALL_ASTEROID, SMALL_ASTEROID, SMALLBODY_SZ_CORRECTION, system)

	def makeShape(self):
		self.BodyShape = ellipsoid(	pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]),
									length=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType], make_trail=false)

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		asteroidRandom = [(randint(10, 20)/10, randint(10, 20)/10, randint(10, 20)/10), (1,1,1)]
		self.BodyShape.length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyShape.height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyShape.width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

	def initRotation(self):
		self.RotAngle = pi/6
		self.RotAxis = (1,1,1)

	def setRotation(self):
		self.BodyShape.rotate(angle=self.RotAngle, axis=self.RotAxis, origine=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])) #-sin(alpha), cos(alpha)))

	def makeAxis(self, size, position):
		return

	def setAxisVisibility(self, setTo):
		return

class dwarfPlanet(makeBody):
	def __init__(self, system, index, color):
		makeBody.__init__(self, system, index, color, DWARFPLANET, DWARFPLANET, DWARFPLANET_SZ_CORRECTION, system)

	def getRealisticSizeCorrectionXX(self):
		#DWARFPLANET_SZ_CORRECTION = 1e-2/(DIST_FACTOR*5)
		return 1e-2/(DIST_FACTOR*5)


class transNeptunian(makeBody):
	def __init__(self, system, index, color):
		makeBody.__init__(self, system, index, color, TRANS_NEPT, TRANS_NEPT, SMALLBODY_SZ_CORRECTION, system)

	def makeShape(self):
		self.BodyShape = ellipsoid(	pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]),
									length=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType], make_trail=false)

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		asteroidRandom = [(randint(10, 20)/10, randint(10, 20)/10, randint(10, 20)/10), (1,1,1)]
		self.BodyShape.length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyShape.height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyShape.width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

	def initRotation(self):
		self.RotAngle = pi/6
		self.RotAxis = (1,1,1)

	def setRotation(self):
		self.BodyShape.rotate(angle=self.RotAngle, axis=self.RotAxis, origine=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])) #-sin(alpha), cos(alpha)))

	def makeAxis(self, size, position):
		return

	def setAxisVisibility(self, setTo):
		return

#
# various functions
#
def getSigmoid(distance, correction):
	sigmoid = 1/(1+exp(-MAX_P_D/distance))
	return correction * sigmoid

# independent functions
def getPerihelion(semimajor, eccentricity):
	# knowing the semi major, the formulat is rp = a(1-e)
	return semimajor * (1 - eccentricity)

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
		#print "Refreshed "+body.Name
	#print "End glbRefresh() ..."

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
# Anomaly (E), the orbit eccentricity and the semi-major axis

def getTrueAnomalyAndRadius(E, e, a):
	ta = 2 * atan(sqrt((1+e)/(1-e)) * tan(E/2))
	R = a * (1 - e*cos(E))
	if ta < 0:
		ta = ta + 2*pi
	return ta, R


# load orbital parameters stored in a file
def loadBodies(SolarSystem, type, filename, maxentries = 0):
	fo  = open(filename, "r")
	token = []
	maxentries = 1000 if maxentries == 0 else maxentries
	for line in fo:
		if line[0] == '#': # skip comments
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
					"absolute_mag": float(token[JPL_MAG_H]) if token[JPL_MAG_H] else 0,
					"axial_tilt": 0 # in deg
				}
				body = {COMET: 			comet,
						BIG_ASTEROID: 	asteroid,
						PHA:			pha,
						TRANS_NEPT:		transNeptunian,
						SATELLITE:		satellite,
						SMALL_ASTEROID:	smallAsteroid,
						}[type](SolarSystem, token[JPL_DESIGNATION], getColor())

				SolarSystem.addTo(body)
				#if body.Name == "Moon":
				#	print body.JPL_designation
				#	print "Satellite was added to solar system"
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
	return EPOCH_2000_JD #2451545.0

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
	return delta + 367*utc.year - (7*(utc.year + ((utc.month+9)/12)))/4 + (275*utc.month)/9 + utc.day - 730530 + (utc.hour/24.0)
	#return delta + julian(utc.day, utc.month, utc.year)

def julian(d,m,y):
	temp1 = m - 14
	temp2 = d - 32075 + 1461 * (y + 4800 + int(temp1 / 12.0)) / 4
	temp3 = int(temp1 / 12.0) * 12
	temp4 = ((y + 4900 + int(temp1 / 12.0)) / 100)
	return temp2 + 367 * (m - 2 - temp3) / 12 - 3 * temp4 / 4

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
