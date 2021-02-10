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
import datetime
import sys
import time
from random import *

#from vpython import *
import numpy as np
import scipy.special as sp
from pynput.mouse import Button, Controller
from visual import *

from location import *
from planetsdata import *

mouse = mouseTracker()
locationInfo = Timeloc() 
mouse = Controller()
print "Mouse position", mouse.position


class solarSystem:

	INNER_RING_COEF = 1.3
	OUTER_RING_COEF = 1.9
	RING_INCREMENT = 0.6
	SCENE_WIDTH = 1920
	SCENE_HEIGHT = 1080
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
		self.Scene = display(title = 'Solar System', width = self.SCENE_WIDTH, height =self.SCENE_HEIGHT, range=3, center = (0,0,0))
		self.MT = self.Scene.getMouseTracker()
		self.MT.SetMouseStateReporter(self.Scene)

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
		self.BodyShape = []

		# make all light coming from origin
		self.sunLight = local_light(pos=(0,0,0), color=color.white)
		self.Scene.ambient = color.black

		if THREE_D:
			self.Scene.stereo='redcyan'
			self.Scene.stereodepth = 1

		self.TiltAngle = deg2rad(self.AxialTilt)
		cosv = cos(self.TiltAngle)
		sinv = sin(self.TiltAngle)
		self.Rotation_ObliquityAroundY = np.matrix([
			[cosv, 	0, 	sinv],
			[0, 	1, 	   0],
			[-sinv, 0,	cosv]]
		)

		self.Rotation_Obliquity = np.matrix([
			[1,		0,	      0],
			[0,		cosv, -sinv],
			[0,		sinv,  cosv]]
		)

		self.BodyShape.append(sphere(pos=vector(0,0,0), radius=self.BodyRadius/self.CorrectionSize, color=color.white))
		self.BodyShape[0].material = materials.emissive

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
			print ("Could not find "+file)
		#self.Scene.scale = self.Scene.scale / 1e10


	def animate(self, deltaT):
		self.setRotation()

	def setRotation(self):
		self.RotAngle = abs((2*pi/self.Rotation)*self.TimeIncrement)
		self.BodyShape[0].rotate(angle=self.RotAngle, axis=self.RotAxis, origine=(0,0,0))

	def initRotation(self):
		# this is necessary to align the planet's texture properly
		self.BodyShape[0].rotate(angle=pi/2+self.TiltAngle, axis=self.XdirectionUnit, origine=(0,0,0))
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
			self.RefAxis[i] = curve( frame = None, color = color.dirtyYellow, pos= [ pos, pos+refDirections[i]], visible=False)
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

	def updateCameraPOV(self, body):

		# the following values will do the following
		# (0,-1,-1): freezes rotation and looks down towards the left
		# (0,-1, 1): freezes rotation and looks up towards the left
		# (0, 1, 1): freezes rotation and looks up towards the right
		# (0, 1,-1): freezes rotation and looks down towards the right

		#self.SolarSystem.Scene.forward = (0, 0, -1)
		# For a planet, Foci(x, y, z) is (0,0,0). For a moon, Foci represents the position of the planet the moon orbits around
		self.currentPOV = body
		self.currentPOVselection = body.Name.upper()
		self.Scene.center = (self.currentPOV.Position[X_COOR]+self.currentPOV.Foci[X_COOR],
							 self.currentPOV.Position[Y_COOR]+self.currentPOV.Foci[Y_COOR],
							 self.currentPOV.Position[Z_COOR]+self.currentPOV.Foci[Z_COOR])
		print self.Scene.center

	def addTo(self, body):
		self.bodies.append(body)
		i = len(self.bodies) - 1
		self.nameIndex[body.JPL_designation] = i
		if body.JPL_designation == 'earth':
			self.EarthRef = body
		return i # this is the index of the added body in the collection

	def addJTrojans(self, body):
		if self.JTrojansIndex < 0:
			self.JTrojansIndex = self.addTo(body)
		else:
			for i in range(len(self.bodies[self.JTrojansIndex].Labels)):
				self.bodies[self.JTrojansIndex].Labels[i].visible = False
			self.bodies[self.JTrojansIndex].BodyShape[0].visible = False
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
			if body.BodyType in [SPACECRAFT, OUTERPLANET, INNERPLANET, ASTEROID, COMET, SATELLITE, DWARFPLANET, PHA, BIG_ASTEROID, TRANS_NEPT]:
				body.toggleSize(realisticSize)

				if body.BodyShape[0].visible == True:
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
				if body.BodyShape[0].visible == True and animationInProgress == True:
					for i in range(len(body.BodyShape)):
						body.BodyShape[i].visible = False
					for i in range(len(body.Labels)):
						body.Labels[i].visible = False

		if self.ShowFeatures & LIT_SCENE != 0:
			self.Scene.ambient = color.white
			self.sunLight.visible = False
			self.BodyShape[0].material = materials.texture(data=materials.loadTGA("./img/sun"), mapping="spherical", interpolate=False)
		else:
			self.Scene.ambient = color.nightshade #color.black
			self.sunLight.visible = True
			self.BodyShape[0].material = materials.emissive

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
			planet.Rings[i].pos = planet.BodyShape[0].pos #self.Position

	def makeRingsV2(self, planet): #, system, bodyName, numberOfRings, colorArray):  # change default values during instantiation
		for i in range(0, planet.nRings):
			curRadius = planet.BodyRadius * (self.INNER_RING_COEF + i * self.RING_INCREMENT) / planet.SizeCorrection[planet.sizeType]
			planet.Rings.insert(i, cylinder(pos=(planet.Position[0], planet.Position[1], planet.Position[2]), radius=curRadius, color=planet.RingColors[i][0], length=200-(i*20), opacity=planet.RingColors[i][1], axis=planet.RotAxis))
			if (self.SolarSystem.ShowFeatures & planet.BodyType) == 0:
				planet.Rings[i].visible = False
				planet.Rings[i].visible = False

	def makeRingsV3(self, system, bodyName):  # change default values during instantiation
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
				cosv = cos(i)
				sinv = sin(i)
				Position = [[OuterRadius * cosv], [OuterRadius * sinv], [0]]
				Position = Rotation_3D * Position + planet.Position
				planet.OuterRing.append(pos=(Position[X_COOR], Position[Y_COOR], Position[Z_COOR]), color=planet.Color) #radius=pointRadius/planet.SizeCorrection, size=1)

				Position = [[InnerRadius * cosv], [InnerRadius * sinv], [0]]
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
		self.BodyShape = []
		self.Labels.append(label(pos=(250*AU*DIST_FACTOR, 250*AU*DIST_FACTOR, 0), text=self.Name, xoffset=20, yoffset=12, space=0, height=10, border=6, box=false, font='sans', visible = False))

	def refresh(self):
		if self.SolarSystem.ShowFeatures & ECLIPTIC_PLANE != 0:
			self.BodyShape[0].visible = True
		else:
			self.BodyShape[0].visible = False

	def draw(self):
		self.BodyShape.append(cylinder(pos=vector(0,0,0), radius=250*AU*DIST_FACTOR, color=self.Color, length=10, opacity=0.1, axis=(0,0,1)))
		self.BodyShape[0].visible = False


class makeBelt:

	def __init__(self, system, key, name, bodyType, color, size, density = 1, planetname = None):  # change default values during instantiation
		self.Labels = []
		self.Name = name
		self.Iau_name = name
		self.JPL_designation = name
		self.SolarSystem = system
		self.Density = density		# body name
		self.RadiusMinAU = belt_data[key]["radius_min"]	# in AU
		self.RadiusMaxAU = belt_data[key]["radius_max"]	# in AU
		self.Thickness = belt_data[key]["thickness"]	# in AU
		self.ThicknessFactor = belt_data[key]["thickness_factor"]
		self.PlanetName = planetname
		self.Color = color
		self.BodyType = bodyType
		self.BodyShape = []
		self.BodyShape.append(points(pos=(self.RadiusMinAU, 0, 0), size=size, color=color))

		self.BodyShape[0].visible = False
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
			self.BodyShape[0].append(pos=(RandomRadius * cos(i), RandomRadius * sin(i), heightToEcliptic))

		self.Labels.append(label(pos=(self.RadiusMaxAU * AU * DIST_FACTOR * cos(i), self.RadiusMaxAU * AU * DIST_FACTOR * sin(i), 0), text=self.Name, xoffset=20, yoffset=12, space=0, height=10, border=6, box=false, font='sans', visible = False))

	def refresh(self):
		if self.SolarSystem.ShowFeatures & self.BodyType != 0:
			if self.BodyShape[0].visible == False:
				self.BodyShape[0].visible = True

			if self.SolarSystem.ShowFeatures & LABELS != 0:
				labelVisible = True
			else:
				labelVisible = False

			for i in range(len(self.Labels)):
				self.Labels[i].visible = labelVisible

		else:
			if self.BodyShape[0].visible == true:
				self.BodyShape[0].visible = false
				for i in range(len(self.Labels)):
					self.Labels[i].visible = False

class makeJtrojan(makeBelt):

	def __init__(self, system, key, name, bodyType, color, size, density = 1, planetname = None):
		makeBelt.__init__(self, system, key, name, bodyType, color, size, density, planetname)
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
			self.BodyShape[0].append(pos=(RandomTail * cos(L4+delta+i), RandomTail * sin(L4+delta+i), heightToEclipticTail))
			self.BodyShape[0].append(pos=(RandomTail * cos(L5-delta-i), RandomTail * sin(L5-delta-i), heightToEclipticTail))
			# calculate positions on 1/2 values and complete by symetry for the rest
			self.BodyShape[0].append(pos=(RandomRadius * cos(L4-delta+i), RandomRadius * sin(L4-delta+i), heightToEcliptic))
			self.BodyShape[0].append(pos=(RandomRadius * cos(L4+delta-i), RandomRadius * sin(L4+delta-i), heightToEcliptic))
			self.BodyShape[0].append(pos=(RandomRadius * cos(L5-delta+i), RandomRadius * sin(L5-delta+i), heightToEcliptic))
			self.BodyShape[0].append(pos=(RandomRadius * cos(L5+delta-i), RandomRadius * sin(L5+delta-i), heightToEcliptic))

		self.Labels.append(label(pos=(self.RadiusMaxAU * AU * DIST_FACTOR * cos(L4), self.RadiusMaxAU * AU * DIST_FACTOR * sin(L4), 0), text="L4 Trojans", xoffset=20, yoffset=12, space=0, height=10, border=6, box=false, font='sans', visible = False))
		self.Labels.append(label(pos=(self.RadiusMaxAU * AU * DIST_FACTOR * cos(L5), self.RadiusMaxAU * AU * DIST_FACTOR * sin(L5), 0), text="L5 Trojans", xoffset=20, yoffset=12, space=0, height=10, border=6, box=false, font='sans', visible = False))


class makeBody:

	RING_BASE_THICKNESS = 2000
	STILL_ROTATION_INTERVAL = 50 #5 * 60 # (in seconds)
	def __init__(self, system, key, color, bodyType = INNERPLANET, sizeCorrectionType = INNERPLANET, RealisticCorrectionSize = SMALLBODY_SZ_CORRECTION, satelliteof = None):  # change default values during instantiation

		self.Labels = []
		self.compounded = False
		self.SatelliteOf = satelliteof
		self.isMoon = False
		self.RealisticCorrectionSize = RealisticCorrectionSize

		self.Foci = vector(satelliteof.Position[X_COOR], satelliteof.Position[Y_COOR], satelliteof.Position[Z_COOR])

		self.ObjectIndex = key
		self.SolarSystem 			= system
		self.Ring 					= False
		self.AxialTilt				= objects_data[key]["axial_tilt"]
		self.Name					= objects_data[key]["name"]		# body name
		self.Iau_name				= objects_data[key]["iau_name"]		# body iau name
		self.JPL_designation 		= objects_data[key]["jpl_designation"]
		self.Mass 					= objects_data[key]["mass"]		# body mass
		self.BodyRadius 			= objects_data[key]["radius"]		# body radius
		self.Color 					= color
		self.BodyType 				= bodyType
		self.Revolution 			= objects_data[key]["PR_revolution"]
		self.Perihelion 			= objects_data[key]["QR_perihelion"]	# body perhelion
		self.Distance 				= objects_data[key]["QR_perihelion"]	# body distance at perige from focus
		self.Details				= False
		self.hasRenderedOrbit		= False
		self.Absolute_mag			= objects_data[key]["absolute_mag"]
		self.Axis 					= [None,None,None]
		self.AxisLabel 				= ["","",""]

		if "tga_name" in objects_data[key]:
			self.Tga 				= objects_data[key]["tga_name"]
		else:
			self.Tga 				= ""

		self.wasAnimated 			= false
		self.rotationInterval 		= self.STILL_ROTATION_INTERVAL

		# for planets with rings
		self.Rings = []
		#w, h = 8, 2;
		#self.Rings = [[0 for x in range(w)] for y in range(h)]

		self.nRings = 0
		self.RingColors = []

		self.sizeCorrectionType = sizeCorrectionType
		self.BodyShape = [] #None

		self.Rotation = objects_data[key]["rotation"] if "rotation" in objects_data[key] else 0
		self.RotAngle = 0

		self.Moid = objects_data[key]["earth_moid"] if "earth_moid" in objects_data[key] else 0
		self.setOrbitalElements(key)

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

		if satelliteof.Name == "Sun":
			# 180 rotation so that vernal equinox points towards left
			self.Rotation_VernalEquinox = np.matrix([
				[-1,	 0, 	0],
				[ 0,	-1,		0],
				[ 0,	 0,		1]]
			)
		else:
			# for satellite rotate 90 back
			self.Rotation_VernalEquinox = np.matrix([  ###############################
				[ 0,	1, 		0],
				[-1,	0,		0],
				[ 0,	0,		1]]
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
		sizeCorrection = { SPACECRAFT: 1, INNERPLANET: 1200, SATELLITE:1400, GASGIANT: 3500, DWARFPLANET: 100, ASTEROID:1, COMET:0.02, SMALL_ASTEROID: 0.1, BIG_ASTEROID:0.1, PHA: 0.0013, TRANS_NEPT: 0.001}[sizeCorrectionType]
		self.shape = { SPACECRAFT: "cylinder", INNERPLANET: "sphere", OUTERPLANET: "sphere", SATELLITE: "sphere", DWARFPLANET: "sphere", ASTEROID:"cube", COMET:"cone", SMALL_ASTEROID:"cube", BIG_ASTEROID:"sphere", PHA:"cube", TRANS_NEPT: "cube"}[bodyType]

		self.SizeCorrection[0] = getSigmoid(self.Perihelion, sizeCorrection)
		self.SizeCorrection[1] = self.RealisticCorrectionSize #self.getRealisticSizeCorrection()

		self.RingThickness = self.RING_BASE_THICKNESS / self.SizeCorrection[self.sizeType]

		if self.BodyRadius < DEFAULT_RADIUS:
			self.radiusToShow = DEFAULT_RADIUS
		else:
			self.radiusToShow = self.BodyRadius

		self.makeShape()

		# attach a curve to the object to display its orbit
		if len(self.BodyShape) > 0: # != None:
			self.Trail = curve(color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))
			self.Trail.append(pos=self.BodyShape[0].pos)
		else:
			return

		#angle = deg2rad(self.AxialTilt)
		self.TiltAngle = deg2rad(self.AxialTilt) # +self.Inclination) # in the ecliptic coordinates system
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

		# add label
		self.Labels.append(label(pos=(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]), text=self.Name, xoffset=20, yoffset=12, space=0, height=10, color=color, border=6, box=false, font='sans'))

		if (self.SolarSystem.ShowFeatures & bodyType) == 0:
			self.BodyShape[0].visible = False
			self.Labels[0].visible = False

		self.makeAxis(self.radiusToShow/self.SizeCorrection[self.sizeType], self.Position) #(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]))
		self.setAspect(key)
		self.initRotation()

	def setAspect(self, key):
		#data = materials.loadTGA("./img/"+key) if objects_data[key]["material"] != 0 else materials.loadTGA("./img/asteroid")
		data = materials.loadTGA("./img/"+self.Tga) if objects_data[key]["material"] != 0 else materials.loadTGA("./img/asteroid")
		self.BodyShape[0].material = materials.texture(data=data, mapping="spherical", interpolate=False)

	def makeShape(self):
		self.BodyShape.append(sphere(pos=(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]), radius=self.radiusToShow/self.SizeCorrection[self.sizeType], make_trail=false))

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
		self.BodyShape[0].radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]

	def setTraceAndLabelVisibility(self, value):
		if self.BodyShape[0].visible == True:
			self.Trail.visible = value
			for i in range(len(self.Labels)):
				self.Labels[i].visible = value

	def animate(self, timeIncrement):
		if self.hasRenderedOrbit == False:
			self.draw()

		self.wasAnimated = true

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

		self.BodyShape[0].pos = vector(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR])
		self.Labels[0].pos = vector(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR])
		self.setRotation()
		if self.Ring == True:
			self.SolarSystem.setRingsPosition(self)
			#for i in range(0, self.nRings):
			#	self.Rings[i].pos = self.BodyShape[0].pos #self.Position
			#self.SolarSystem.makeRings(self) #self.SolarSystem, self.ObjectIndex)

		return self.getCurrentVelocity(), self.getCurrentDistanceFromEarth()

	def setOrbitalElements(self, key, timeincrement = 0):
		# For comets, asteroids or dwarf planets, data comes from data
		# files -or- predefined values. Orbital Position is calculated
		# from the last time of perihelion passage. This is the default
		# behavior
		self.setOrbitalFromPredefinedElements(objects_data[key], timeincrement) #-0.7)

	# unused
	"""
	def setEarthOrbitalFromKeplerianElements(self, elts, timeincrement):
		# get number of days since J2000 epoch and obtain the fraction of century
		# (the rate adjustment is given as a rate per century)
		days = daysSinceJ2000UTC() + timeincrement # what the hell was that thing - 1.5
		#T = (daysSinceJ2000UTC() + timeincrement)/36525. # T is in centuries
		T = days/36525. # T is in centuries

		#self.a = (elts["a"] + (elts["ar"] * T)) * AU
		self.a = 1.000001018 * AU

		#self.e = elts["EC_e"] + (elts["er"] * T)
		self.e = 0.01670862 - (0.000042037 * T) - (0.0000001236 * T**2) + (0.00000000044 * T**3)

		#self.Inclination = elts["i"] + (elts["ir"] * T)
		self.Inclination = 0.0 + (0.0130546 * T) - (0.00000931 * T**2) - (0.000000034 * T**3)

		# compute mean Longitude with correction factors beyond jupiter M = L - W + bT^2 +ccos(ft) + ssin(ft)
		#
		#L = elts["L"] + (elts["Lr"] * T) + (elts["b"] * T**2  +
		#									elts["c"] * cos(elts["f"] * T) +
		#									elts["s"] * sin(elts["f"] * T))
		#
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

	"""

	# will calculate current value of approximate position of the major planets
	# including pluto. This won't work for Asteroid, Comets or Dwarf planets
	def setOrbitalFromKeplerianElements(self, elts, timeincrement):
		# get number of days since J2000 epoch and obtain the fraction of century
		# (the rate adjustment is given as a rate per century)
		days = daysSinceJ2000UTC() + timeincrement - ADJUSTMENT_FACTOR_PLANETS # - 1.43
		#T = (daysSinceJ2000UTC() + timeincrement)/36525. # T is in centuries
		T = days/36525. # T is in centuries

		self.a = (elts["a"] + (elts["ar"] * T)) * AU
		self.e = elts["EC_e"] + (elts["er"] * T)
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
		self.e 							= elts["EC_e"]
		self.Longitude_of_perihelion 	= elts["longitude_of_perihelion"]
		self.Longitude_of_ascendingnode = elts["OM_longitude_of_ascendingnode"]
		self.Argument_of_perihelion 	= self.Longitude_of_perihelion - self.Longitude_of_ascendingnode
		self.a 							= getSemiMajor(self.Perihelion, self.e)
		self.Inclination 				= elts["IN_orbital_inclination"]

		#if self.SatelliteOf != None:
		#	self.Inclination -= self.SatelliteOf.AxialTilt
			
		self.Time_of_perihelion_passage = elts["Tp_Time_of_perihelion_passage_JD"]
		self.Mean_motion				= elts["N_mean_motion"]
		self.Epoch						= elts["epochJD"]
		self.Mean_anomaly				= elts["MA_mean_anomaly"]
		self.revolution					= elts["PR_revolution"]
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

		if self.BodyShape[0].visible:
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
		TEXTURE_POSITIONING_CORRECTION = pi/12
		# we need to rotate around X axis by pi/2 to properly align the planet's texture
		self.BodyShape[0].rotate(angle=(pi/2+self.TiltAngle), axis=self.XdirectionUnit, origine=(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]))
		# then further rotation will apply to Z axis
		self.RotAxis = self.ZdirectionUnit
		
		# calculate current RA, to position the obliquity properly:
		if "RA_1" in objects_data[self.ObjectIndex]:
			T = daysSinceJ2000UTC()/36525. # T is in centuries
			self.RA = objects_data[self.ObjectIndex]["RA_1"] + objects_data[self.ObjectIndex]["RA_2"] * T
			self.BodyShape[0].rotate(angle=deg2rad(self.RA), axis=self.ZdirectionUnit, origine=(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]))
		#else:
		#	print "No RA for " +self.Name


	# default
	def setRotation(self):
		ti = self.SolarSystem.getTimeIncrement()
		self.RotAngle = abs((2*pi/self.Rotation)*ti) if self.Rotation > 0 else 0

		if ti < 0:
			self.RotAngle *= -1

		self.updateAxis()
		self.BodyShape[0].rotate(angle=self.RotAngle, axis=self.RotAxis, origine=(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]))

	def updatePosition(self, trace = True):
		self.setCartesianCoordinates()
		self.BodyShape[0].pos = vector(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR])
		if trace:
			if self.Position[Z_COOR]+self.Foci[Z_COOR] < 0:
				"""
				self.Interval += 1
				if self.Interval % 2 == 0:
					#self.Trail.append(pos=self.BodyShape[0].pos, color=self.Color) #, interval=50)
					self.Trail.append(pos=self.BodyShape[0].pos, color=(self.Color[0]*0.3, self.Color[1]*0.3, self.Color[2]*0.3))			
				else:
					self.Trail.append(pos=self.BodyShape[0].pos, color=color.black) #, interval=50)
				"""
				# new
				self.Trail.append(pos=self.BodyShape[0].pos, color=(self.Color[0]*0.3, self.Color[1]*0.3, self.Color[2]*0.3))
			else:
				#self.Trail.append(pos=self.BodyShape[0].pos, color=self.Color)
				self.Trail.append(pos=self.BodyShape[0].pos, color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))

	def setCartesianCoordinates(self):
		self.Position[X_COOR] = self.R * DIST_FACTOR * ( cos(self.N) * cos(self.Nu+self.w) - sin(self.N) * sin(self.Nu+self.w) * cos(self.i) )
		self.Position[Y_COOR] = self.R * DIST_FACTOR * ( sin(self.N) * cos(self.Nu+self.w) + cos(self.N) * sin(self.Nu+self.w) * cos(self.i) )
		self.Position[Z_COOR] = self.R * DIST_FACTOR * ( sin(self.Nu+self.w) * sin(self.i) )

		self.Position = self.Rotation_VernalEquinox * self.Position

	def show(self):
		if self.hasRenderedOrbit == False:
			self.draw()

		for i in range(len(self.BodyShape)):
			self.BodyShape[i].visible = True
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
		for i in range(len(self.BodyShape)):
			self.BodyShape[i].visible = False
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
			if self.BodyShape[0].visible == False:
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
	
	def __init__(self, system, key, color, type, sizeCorrectionType, defaultSizeCorrection):
		makeBody.__init__(self, system, key, color, type, sizeCorrectionType, defaultSizeCorrection, system)

	def updateStillPosition(self, timeinsec):
		return

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

		self.BodyShape[0].radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]
		self.RingThickness = self.RING_BASE_THICKNESS / self.SizeCorrection[self.sizeType]
		if self.Ring == True:
			for i in range(0, self.nRings):
				self.Rings[i].visible = False
				self.Rings[i] = None
			self.SolarSystem.makeRings(self) #self.SolarSystem, self.ObjectIndex)

	def setOrbitalElements(self, key, timeincrement = 0):
		# for the Major planets (default) includig Pluto, we have Keplerian
		# elements to calculate the body's current approximated position on orbit
		elt = objects_data[key]["kep_elt_1"] if "kep_elt_1" in objects_data[key] else objects_data[key]["kep_elt"]
		self.setOrbitalFromKeplerianElements(elt, timeincrement) #-1.4) #0.7)


class makeEarth(planet):
	
	def __init__(self, system, color, type, sizeCorrectionType, defaultSizeCorrection):
		# corrective angle (earth only)
		self.Gamma = 0

		planet.__init__(self, system, "earth", color, type, sizeCorrectionType, defaultSizeCorrection)


	def initRotation(self):
		# texture alignment correction coefficient
		TEXTURE_POSITIONING_CORRECTION = pi/12

		# we need to rotate around X axis by pi/2 to properly align the planet's texture
		self.BodyShape[0].rotate(angle=(pi/2+self.TiltAngle), axis=self.XdirectionUnit, origine=(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]))

		# then further rotation will apply to Z axis
		self.RotAxis = self.ZdirectionUnit

		# calculate initial angle between body and solar referential x axis
		self.iDelta = atan2(self.Position[Y_COOR], self.Position[X_COOR])

		# Calculate the local initial angle between the normal to the sun and our location
		self.Gamma = deg2rad(locationInfo.solarT) \
					 - deg2rad(locationInfo.Time2degree(locationInfo.RelativeTimeToDateline)) \
					 - self.iDelta 

		# add correction due to initial position of texture on earth sphere, then rotate texture to make it match current time
		self.LocalInitialAngle = -TEXTURE_POSITIONING_CORRECTION + self.Gamma
		self.BodyShape[0].rotate(angle=(self.LocalInitialAngle), axis=self.RotAxis, origine=(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]))
		
		"""
		# calculate current RA, to position the obliquity properly:
		if "RA_1" in objects_data[self.ObjectIndex]:
			print "BURP!!!!!!!!!!!!!!!!!"
			T = daysSinceJ2000UTC()/36525. # T is in centuries
			self.RA = objects_data[self.ObjectIndex]["RA_1"] + objects_data[self.ObjectIndex]["RA_2"] * T
		#	self.BodyShape[0].rotate(angle=deg2rad(self.RA), axis=self.ZdirectionUnit, origine=(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]))
		#else:
		#	print "No RA for " +self.Name
		"""

	def updateStillPosition(self, timeinsec):
		if self.wasAnimated == false:
			self.rotationInterval -= timeinsec
			#print "rotation Interval = ", self.rotationInterval
			if self.rotationInterval <= 0:
				locationInfo.setSolarTime()
				self.incrementRotation()
				self.rotationInterval = self.STILL_ROTATION_INTERVAL

	def incrementRotation(self):
		# recalculate the angle of the texture on sphere based on updated time 
		newLocalInitialAngle = deg2rad(locationInfo.solarT) \
							   - deg2rad(locationInfo.Time2degree(locationInfo.RelativeTimeToDateline)) \
							   - self.iDelta 

		# rotate for the difference between updated angle and its formal value
		self.BodyShape[0].rotate(angle=(newLocalInitialAngle - self.Gamma), axis=self.RotAxis, origine=(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]))
		print "rotating by ", newLocalInitialAngle - self.Gamma, " degree"
		# update angle with its updated value
		self.Gamma = newLocalInitialAngle

	def setOrbitalFromKeplerianElements(self, elts, timeincrement):
		# get number of days since J2000 epoch and obtain the fraction of century
		# (the rate adjustment is given as a rate per century)
		days = daysSinceJ2000UTC() + timeincrement - ADJUSTMENT_FACTOR_PLANETS # - 1.43
		#T = (daysSinceJ2000UTC() + timeincrement)/36525. # T is in centuries

		T = (days-1.95)/36525. # T is in centuries
		#T = (days)/36525. # T is in centuries

		self.a = (elts["a"] + (elts["ar"] * T)) * AU
		self.e = elts["EC_e"] + (elts["er"] * T)
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


class satellite(makeBody):
	def __init__(self, system, key, color, planetBody):
		#if planetBody != None:
		#	print objects_data[key]['name']+" is a satellite of: "+planetBody.Name
		makeBody.__init__(self, system, key, color, SATELLITE, SATELLITE, SATELLITE_SZ_CORRECTION, planetBody)
		self.isMoon = True
		#self.Rotation_VernalEquinox = np.matrix([  ###############################
		#	[ 0,	1, 		0],
		#	[-1,	0,		0],
		#	[ 0,	0,		1]]
		#)

	def getRealisticSizeCorrectionXX(self):
		#SATELLITE_SZ_CORRECTION = 1/(DIST_FACTOR * 5)
		return 1/(DIST_FACTOR * 5)

	def setCartesianCoordinatesXX(self): # added tis to avoid correcting for vernal equinox rotation when dealing with moons
		self.Position[X_COOR] = self.R * DIST_FACTOR * ( cos(self.N) * cos(self.Nu+self.w) - sin(self.N) * sin(self.Nu+self.w) * cos(self.i) )
		self.Position[Y_COOR] = self.R * DIST_FACTOR * ( sin(self.N) * cos(self.Nu+self.w) + cos(self.N) * sin(self.Nu+self.w) * cos(self.i) )
		self.Position[Z_COOR] = self.R * DIST_FACTOR * ( sin(self.Nu+self.w) * sin(self.i) )

		#self.Position = self.Rotation_VernalEquinox * self.Position

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

		self.BodyShape[0].radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]

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
	def __init__(self, system, key, color, planetBody):
		makeBody.__init__(self, system, key, color, HYPERBOLIC, HYPERBOLIC, HYPERBOLIC_SZ_CORRECTION, planetBody)
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

		self.BodyShape[0].radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]

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

	
class spacecraft(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, SPACECRAFT, SPACECRAFT, SMALLBODY_SZ_CORRECTION, system)
		self.BARYCENTER = 0.0
		self.AFT_TANK_RADIUS = 0.0
		self.AFT_TANK_CENTER_XCOOR = 0.0
		self.FWD_TANK_RADIUS = 0.0
		self.FWD_TANK_CENTER_XCOOR = 0.0
		self.ENGINE_HEIGHT = 0.0
		self.ENGINE_TOP_XCOOR = 0.0
		self.COPV_RADIUS = 0.0

	def animate(self, timeIncrement):
		#makeBody.animate(self, timeIncrement)
		if self.hasRenderedOrbit == False:
			self.draw()

		self.wasAnimated = true

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

		self.BodyShape[0].pos = vector(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR])
		#self.BodyShape[1].pos = vector(self.Position[X_COOR] - 15 + self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR])

		self.Labels[0].pos = vector(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR])
		self.setRotation()
		if self.Ring == True:
			self.SolarSystem.setRingsPosition(self)
			#for i in range(0, self.nRings):
			#	self.Rings[i].pos = self.BodyShape.pos #self.Position
			#self.SolarSystem.makeRings(self) #self.SolarSystem, self.ObjectIndex)

		return self.getCurrentVelocity(), self.getCurrentDistanceFromEarth()


	def setAspect(self, key):
		if objects_data[key]["material"] != 0:
			data = materials.loadTGA("./img/"+ self.Tga)
			self.BodyShape[0].objects[0].material = materials.texture(data=data, mapping="cylinder", interpolate=False)

	def makeShape(self):
		self.length = 2 * self.radiusToShow/self.SizeCorrection[self.sizeType]
		self.radius = 20 
		self.compounded = True

		# create compound object
		self.BodyShape.append(frame())

		# create fuselage
		self.BARYCENTER_XCOOR = -self.length/2
		cylinder(frame=self.BodyShape[0], pos=(self.BARYCENTER_XCOOR,0,0), radius=self.radius, length=self.length)
#		sphere(frame=self.BodyShape[0], pos=(-self.length/14, self.length/8, 0), radius=self.length/15, color=color.yellowish)		

		# create aft tank
		self.AFT_TANK_RADIUS = self.radius
		self.AFT_TANK_CENTER_XCOOR = self.BARYCENTER_XCOOR + self.length/9
		sphere(frame=self.BodyShape[0], pos=(self.AFT_TANK_CENTER_XCOOR, 0, 0), radius=self.AFT_TANK_RADIUS, color=color.white)		

		# create forward Platform
		self.FWD_TANK_RADIUS = self.radius
		self.FWD_TANK_CENTER_XCOOR = self.BARYCENTER_XCOOR + self.length - self.radius/1.5
		sphere(frame=self.BodyShape[0], pos=(self.FWD_TANK_CENTER_XCOOR, 0, 0), radius=self.FWD_TANK_RADIUS, color=color.white)		

		# create tesla
		roadster = self.makeTesla()
		roadster.frame = self.BodyShape[0]
		# place roadster on the top of stage-2
		roadster.pos = (self.FWD_TANK_CENTER_XCOOR+(self.FWD_TANK_RADIUS)*1.3, self.carlength/2, -self.carwidth/2)
		roadster.axis = (-0.3, 1, 0)

		# create engine
		self.ENGINE_HEIGHT = self.length/13
		self.ENGINE_TOP_XCOOR = self.AFT_TANK_CENTER_XCOOR - self.AFT_TANK_RADIUS - self.ENGINE_HEIGHT/2 - self.length/30
		cylinder(frame=self.BodyShape[0], pos=(self.ENGINE_TOP_XCOOR,0,0), radius=self.AFT_TANK_RADIUS/5, length=self.length/13, color=color.darkgrey)

		# create COPV
		self.COPV_RADIUS = self.length/17
		sphere(frame=self.BodyShape[0], pos=(self.ENGINE_TOP_XCOOR + self.length/31, self.length/9, 0), radius=self.COPV_RADIUS, color=color.grey)		
	
		nozzle = self.makeNozzle()
		nozzle.frame = self.BodyShape[0]
		self.BodyShape[0].pos = self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]
		
	def initRotation(self):
		self.RotAngle = pi/200
		self.RotAxis = (5, 5, -5)
		
	def setRotation(self):
		for i in range(len(self.BodyShape)):
			self.BodyShape[i].rotate(angle=self.RotAngle, axis=self.RotAxis, origine=(self.Position[X_COOR] + 10*self.length, self.Position[Y_COOR] + 10*self.length, self.Position[Z_COOR])) #-sin(alpha), cos(alpha)))
		#self.Engine.rotate(angle=self.RotAngle, axis=self.RotAxis, origine=(self.Position[X_COOR] + 10*self.length, self.Position[Y_COOR] + 10*self.length, self.Position[Z_COOR])) #-sin(alpha), cos(alpha)))

	def makeAxis(self, size, position):
		return

	def setAxisVisibility(self, setTo):
		return


	def makeSimpleNozzle(self):
		# to create a nozzle, we need to start from a polygon representing the cross section of
		# the nozzle, and then create a cone by rotating this xsection around a circle

		# create a section of cone of 60, length d
		alpha = pi/2.5
		d = self.length/4 #self.radius/2
		THROAT_SECTION = self.radius/7
		section = Polygon([(0, 0), (self.length/100, 0), ((self.length/100)+d*np.cos(alpha), d*np.sin(alpha)), (d*np.cos(alpha), d*np.sin(alpha))])
		
		# set up to x=-1 so that the axis will be going towards the -x axis of the frame. also position the origin
		# negatively to push the nozzle cone further out
		circle = paths.arc(radius=THROAT_SECTION, angle2=2*pi, up=(-1,0,0), pos=(-self.length/6, 0, 0))
		return extrusion(pos=circle,
				shape=section,
				color=color.yellow)

	def makeNozzle(self):
		# to create a nozzle, we need to start from a polygon representing the cross section of
		# the nozzle, and then create a cone by rotating this xsection around a circle

		# create a section of cone of 60, length d
		alpha = pi/2.5
		d = self.length/4 #self.radius/2
		THROAT_SECTION = self.radius/7
		section = Polygon([(0, 0), (self.length/100, 0), ((self.length/100)+d*np.cos(alpha), d*np.sin(alpha)), (d*np.cos(alpha), d*np.sin(alpha))])
		
		# set up to x=-1 so that the axis will be going towards the -x axis of the frame. also position the origin
		# negatively to push the nozzle cone further out
		circle = paths.arc(radius=THROAT_SECTION, angle2=2*pi, up=(-1,0,0), pos=(self.BARYCENTER_XCOOR -self.length/6, 0, 0))
		return extrusion(pos=circle,
				shape=section,
				color=color.grey)
				#material=materials.silver)

	def makeTesla(self):
		roadster = frame()
		# create a box with a slight angle
		"""
		carbody = box(pos=(0, 0, 0), 
			frame=roadster
			axis=(0.25,1,0),
			length=self.radius*1.5, 
			height=self.radius*1.5/5, 
			width=self.radius*2.8/3, color=color.redish, material=materials.emissive)
		"""
		# describe extrusion path for wheels:
		self.carlength = self.radius*1.5
		self.carheight = self.radius*1.5/5
		self.carwidth = self.radius*2/3

		straight = [(0,0,0),(0,0,self.carwidth)]
		#wheelLiners = Polygon( [(-.5,.5),(-.5,2.5),(.5,2.5),(.5,.5)] )
		BODY_ROUND_VERTICAL = 2
		BODY_ROUND_HORIZONTAL = 3

		# create a 2D profile of roadster
		carbody2D = Polygon( [	(0,0),
								(self.carlength-BODY_ROUND_HORIZONTAL, 0),
								(self.carlength-BODY_ROUND_HORIZONTAL+BODY_ROUND_VERTICAL, BODY_ROUND_VERTICAL/2),
								(self.carlength, BODY_ROUND_VERTICAL),
 							  	(self.carlength, self.carheight), 
								(BODY_ROUND_HORIZONTAL, self.carheight),
								(0, self.carheight-BODY_ROUND_VERTICAL)])

		# Front wheels elements as (coordinates of center as (x, y), radius)
		FWelements = vector(4*self.carlength/5, 3*self.carheight/3.5, self.carheight/2.1)
		frontwheelWell = shapes.circle(
#			pos=(4*self.carlength/5, 3*self.carheight/3.5), radius=self.carheight/2.2)
			pos=(FWelements[0], FWelements[1]), radius=FWelements[2])

		# Rear wheels elements as (coordinates of center as (x, y), radius)
		RWelements = vector(self.carlength/5, 3*self.carheight/3.5, self.carheight/2.2)
		rearwheelWell = shapes.circle(
#			pos=(self.carlength/5, 3*self.carheight/3.5), radius=self.carheight/2.2)
			pos=(RWelements[0], RWelements[1]), radius=RWelements[2])

		# make car body from 2D polygones set
		body = extrusion(pos=straight, 
				shape=carbody2D-rearwheelWell-frontwheelWell,
				color=color.red,
				material=materials.emissive)


		body.frame = roadster
		self.makeWheels(body, FWelements, RWelements)
		self.makeHeadlights(body)
		return roadster
		
	def makeHeadlights(self, body):
#		rightHL = ellipsoid(frame=body.frame, pos=(-self.carlength * 0.95, self.carheight*0.1, self.carwidth*0.1), up=(0,1,0), axis=(1,0, -0.5),
		rightHL = ellipsoid(frame=body.frame, pos=(-self.carlength * 0.95, 0, self.carwidth*0.1), up=(0,1,0), axis=(-1, -1, -0.5),
         					length=self.carwidth/4, height=self.carheight/3, width=0.1, color=color.white, material=materials.emissive)

	def makeWheels(self, body, front, rear):
		
		cylinder(frame=body.frame, axis=(0,0,1), pos=(-front[0], front[1], 0), 					radius=front[2]*0.90, length=self.carwidth * 0.15, color=color.darkgrey)
		cylinder(frame=body.frame, axis=(0,0,1), pos=(-front[0], front[1], -0.1), 				radius=front[2]*0.60, length=self.carwidth * 0.10, color=color.white)

		cylinder(frame=body.frame, axis=(0,0,1), pos=(-front[0], front[1], (self.carwidth * (1 - 0.15))),  radius=front[2]*0.90, length=self.carwidth * 0.15, color=color.darkgrey)
		cylinder(frame=body.frame, axis=(0,0,1), pos=(-front[0], front[1], self.carwidth*0.91),	radius=front[2]*0.60, length=self.carwidth * 0.10, color=color.white)

		cylinder(frame=body.frame, axis=(0,0,1), pos=(-rear[0], rear[1], 0), 					radius=rear[2]*0.90, length=self.carwidth * 0.15, color=color.darkgrey)
		cylinder(frame=body.frame, axis=(0,0,1), pos=(-rear[0], rear[1], -0.1), 				radius=rear[2]*0.60, length=self.carwidth * 0.10, color=color.white)

		cylinder(frame=body.frame, axis=(0,0,1), pos=(-rear[0], rear[1], (self.carwidth * (1 - 0.15))), 	radius=rear[2]*0.90, length=self.carwidth * 0.15, color=color.darkgrey)
		cylinder(frame=body.frame, axis=(0,0,1), pos=(-rear[0], rear[1], self.carwidth*0.91), 	radius=rear[2]*0.60, length=self.carwidth * 0.10, color=color.white)


	def makeTesla2(self):
		carbody = box(frame=self.BodyShape[0], pos=(self.FWD_TANK_CENTER_XCOOR+(self.FWD_TANK_RADIUS)*1.1, 0, 0), 
			axis=(0.25,1,0),
			length=self.radius*1.5, 
			height=self.radius*1.5/5, 
			width=self.radius*2.8/3, color=color.redish, material=materials.emissive)

			# describe extrusion path for wheels:
			#straight = [(0, 0, 0)
		roadster =extrusion(pos=circle,
				shape=section,
				color=color.grey)
				#material=materials.silver)
		self.makeWheels(roadster)


	"""


	tri = Polygon( [(-2,0), (0,4), (2,0)] )

	circ = shapes.circle(pos=(0,1.5), radius=0.8)

	2) Create a path along which to extrude your shape (just like the pos attribute of a curve object), either by giving a list of points or by choosing a path from a supplied library of common shapes. Here are two example. The first is a 2-point line, headed into the screen (-z direction). The second chooses a semicircular arc from the paths library to be discussed later (pi radians is 180 degrees).

	straight = [(0,0,0),(0,0,-4)]

	semicircle = paths.arc(radius=3, angle2=pi)
	3) Create an extrusion object to extrude your shape along your path. Here we've assigned the "straight" path to the pos attribute, and the "tri" shape to the shape attribute.

	extrusion(pos=straight, shape=tri,
			color=color.yellow)

 

The result is that the triangular shape is extruded in the -z direction.

extruded triangle
An important feature is that you can combine simple shapes to make complex ones. For example, if we subtract the circular shape ("circ") from the triangle shape ("tri"), and assign this to the extrusion shape attribute, we get the following:

extrusion(pos=straight, shape=tri-circ,
          color=color.yellow)

triangle with hole
If we assign the semicircle path to the extrusion pos attribute, we get the following:

extrusion(pos=semicircle,
          shape=tri-circ,
          color=color.yellow)
"""

class comet(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, COMET, COMET, SMALLBODY_SZ_CORRECTION, system)

	def makeShape(self):
		self.BodyShape.append(ellipsoid(	pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]),
									length=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType], make_trail=false))
	def setAspect(self, key):
		# we don't need key for comets
		#self.BodyShape.material = materials.marble
		data = materials.loadTGA("./img/comet")
		self.BodyShape[0].material = materials.texture(data=data, mapping="spherical", interpolate=False)


	def initRotation(self):
		self.RotAngle = pi/6
		self.RotAxis = (1,1,1)

	def setRotation(self):
		#self.updateAxis()
		self.BodyShape[0].rotate(angle=self.RotAngle, axis=self.RotAxis, origine=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])) #-sin(alpha), cos(alpha)))

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
		self.BodyShape[0].length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyShape[0].height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyShape[0].width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

	def getIncrement(self):
		# for comets, due to their sometimes high eccentricity, an increment of 1 deg may not be small enough
		# to insure a smooth curve, hence we need to take smaller increments of 12.5 arcminutes or less in radians
		return pi/(180 * 4)

class asteroid(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, BIG_ASTEROID, BIG_ASTEROID, ASTEROID_SZ_CORRECTION, system)

	def initRotation(self):
		self.RotAngle = pi/6
		self.RotAxis = (1,1,1)

	def setRotation(self):
		self.BodyShape[0].rotate(angle=self.RotAngle, axis=self.RotAxis, origine=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])) #-sin(alpha), cos(alpha)))

	def makeAxis(self, size, position):
		return

	def setAxisVisibility(self, setTo):
		return

	def getRealisticSizeCorrectionXX(self):
		#ASTEROID_SZ_CORRECTION = 1e-2/(DIST_FACTOR*5)
		return 1e-2/(DIST_FACTOR*5)


class pha(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, PHA, PHA, SMALLBODY_SZ_CORRECTION, system)

	def makeShape(self):
		"""
		self.BodyShape[0] = ellipsoid(	pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]),
									length=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType], make_trail=false)
		"""
		asteroidRandom = [(1.5, 2, 1), (1.5, 2, 1)]
		self.BodyShape.append(ellipsoid(	pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]),
									length=(self.radiusToShow * asteroidRandom[self.sizeType][0])/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * asteroidRandom[self.sizeType][1])/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * asteroidRandom[self.sizeType][2])/self.SizeCorrection[self.sizeType], make_trail=false))

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		#asteroidRandom = [(randint(10, 20)/10, randint(10, 20)/10, randint(10, 20)/10), (1,1,1)]
		asteroidRandom = [(1.5, 2, 1), (1.5, 2, 1)]
		self.BodyShape[0].length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyShape[0].height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyShape[0].width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

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
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, SMALL_ASTEROID, SMALL_ASTEROID, SMALLBODY_SZ_CORRECTION, system)

	def makeShape(self):
		self.BodyShape.append(ellipsoid(	pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]),
									length=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType], make_trail=false))

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		asteroidRandom = [(randint(10, 20)/10, randint(10, 20)/10, randint(10, 20)/10), (1,1,1)]
		self.BodyShape[0].length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyShape[0].height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyShape[0].width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

	def initRotation(self):
		self.RotAngle = pi/6
		self.RotAxis = (1,1,1)

	def setRotation(self):
		self.BodyShape[0].rotate(angle=self.RotAngle, axis=self.RotAxis, origine=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])) #-sin(alpha), cos(alpha)))

	def makeAxis(self, size, position):
		return

	def setAxisVisibility(self, setTo):
		return

class dwarfPlanet(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, DWARFPLANET, DWARFPLANET, DWARFPLANET_SZ_CORRECTION, system)

	def getRealisticSizeCorrectionXX(self):
		#DWARFPLANET_SZ_CORRECTION = 1e-2/(DIST_FACTOR*5)
		return 1e-2/(DIST_FACTOR*5)


class transNeptunian(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, TRANS_NEPT, TRANS_NEPT, SMALLBODY_SZ_CORRECTION, system)

	def makeShape(self):
		self.BodyShape.append(ellipsoid(	pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]),
									length=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType], make_trail=false))

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		asteroidRandom = [(randint(10, 20)/10, randint(10, 20)/10, randint(10, 20)/10), (1,1,1)]
		self.BodyShape[0].length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyShape[0].height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyShape[0].width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

	def initRotation(self):
		self.RotAngle = pi/6
		self.RotAxis = (1,1,1)

	def setRotation(self):
		self.BodyShape[0].rotate(angle=self.RotAngle, axis=self.RotAxis, origine=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])) #-sin(alpha), cos(alpha)))

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
	beltname.BodyShape[0].visible = false
	beltname.Labels[0].visible = false

def showBelt(beltname):
	beltname.BodyShape[0].visible = true
	beltname.Labels[0].visible = true

def getColor():
	return { 0: color.white, 1: color.red, 2: color.orange, 3: color.yellow, 4: color.cyan, 5: color.magenta, 6: color.green}[randint(0,6)]

# Calculates Eccentric Anomaly (E) given the mean anomaly (M) and the depth of the Bessel first kind functions
def bessel_E(M, e, depth):
    return (M + sum(2.0 / n * sp.jv(n, n * e) * np.sin(n * M)
                    for n in range(1, depth, 1)))

# Calculates Eccentric Anomaly (E) given the mean anomaly (M), the depth and the
# precision required using an iterative method. If the precision has been reached
# within the maximum iteration depth, returns (True, E, precision, #iterations) or
# (False, E, precision, #iterations) otherwise

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


# load orbital parameters stored in JSON file
def loadBodies(SolarSystem, type, filename, maxentries = 0):
	fo  = open(filename, "r")
	allObj = json.loads(fo.read())

	maxentries = 1000 if maxentries == 0 else maxentries
	for obj in allObj:
		for key in obj:
			objects_data[obj[key]["jpl_designation"]] = {
				"material": 1 if obj[key]["tga_name"] != "" else 0,
				"name": str(obj[key]["name"]),
				"iau_name": str(obj[key]["iau_name"]),
				"jpl_designation": str(obj[key]["jpl_designation"]),
				"mass": (obj[key]["mu"]/G)*1.e+9, # convert km3 to m3
				"radius": obj[key]["diameter"]/2, 
				"QR_perihelion": obj[key]["QR_perihelion"] * AU,
				"EC_e": obj[key]["EC_e"],
				"PR_revolution": obj[key]["PR_revolution"],
				"IN_orbital_inclination": 	obj[key]["IN_orbital_inclination"],
				"OM_longitude_of_ascendingnode":obj[key]["OM_longitude_of_ascendingnode"],
				"W_argument_of_perihelion": obj[key]["W_argument_of_perihelion"],
				"longitude_of_perihelion": obj[key]["OM_longitude_of_ascendingnode"] + obj[key]["W_argument_of_perihelion"],
				"Tp_Time_of_perihelion_passage_JD": obj[key]["Tp_Time_of_perihelion_passage_JD"],
				"N_mean_motion": obj[key]["N_mean_motion"],
				"MA_mean_anomaly": obj[key]["MA_mean_anomaly"],
				"epochJD": obj[key]["epochJD"],
				"earth_moid": obj[key]["earth_moid"] * AU,
				"orbit_class": str(obj[key]["orbit_class"]),
				"absolute_mag": obj[key]["absolute_mag"],
				"axial_tilt": obj[key]["axial_tilt"], # in deg
				"tga_name": str(obj[key]["tga_name"])
			}
			
			#print obj[key]["jpl_designation"]
			#return
			body = {SPACECRAFT: 	spacecraft,
					COMET: 			comet,
					BIG_ASTEROID: 	asteroid,
					PHA:			pha,
					TRANS_NEPT:		transNeptunian,
					SATELLITE:		satellite,
					SMALL_ASTEROID:	smallAsteroid,
					}[type](SolarSystem, obj[key]["jpl_designation"], getColor())

			SolarSystem.addTo(body)
			#if body.Name == "Moon":
			#	print body.JPL_designation
			#	print "Satellite was added to solar system"
			maxentries -= 1
			if maxentries <= 0:
				break
		# test: break after 1 rec
		#break
	fo.close()

def loadBodiesOldway(SolarSystem, type, filename, maxentries = 0):
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
					"QR_perihelion": float(token[JPL_OE_q]) * AU,
					"EC_e": float(token[JPL_OE_e]),
					"PR_revolution": float(token[JPL_OE_Pd]),
					"IN_orbital_inclination": 	float(token[JPL_OE_i]),
					"OM_longitude_of_ascendingnode":float(token[JPL_OE_N]),
					"W_argument_of_perihelion": float(token[JPL_OE_w]),
					"longitude_of_perihelion":float(token[JPL_OE_N])+float(token[JPL_OE_w]),
					"Tp_Time_of_perihelion_passage_JD":float(token[JPL_OE_tp_JD]),
					"N_mean_motion": float(token[JPL_OE_n]) if token[JPL_OE_n] else 0,
					"MA_mean_anomaly": float(token[JPL_OE_M]) if token[JPL_OE_M] else 0,
					"epochJD": float(token[JPL_EPOCH_JD]),
					"earth_moid": (float(token[JPL_EARTH_MOID_AU])*AU) if token[JPL_EARTH_MOID_AU] else 0,
					"orbit_class":token[JPL_ORBIT_CLASS],
					"absolute_mag": float(token[JPL_MAG_H]) if token[JPL_MAG_H] else 0,
					"axial_tilt": 0, # in deg
					"tga_name": token[JPL_FULLNAME]

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

class flyingCamera():
	def __init__(self, system):
		self.MT = system.MT
	
_n = 0
_delta = 6
_incr = 35

def flyover_approach():
	return
#	while True:
	global _n 
	global _delta
	global _incr
	_n = _n+1

	if _n > 13:
		_delta -= 1
		if _delta <= 0:
			_delta = 0
		
	if _n > 50:
		_incr -= 1
		if _incr <= 1:
			_incr = 1
			#return

	mouse.press(Button.right)
	mouse.press(Button.left)
	mouse.move(0, -_incr)
	mouse.release(Button.right)
	mouse.release(Button.left)
	mouse.move(0, +_incr)
	sleep(0.01)
	mouse.press(Button.right)
	mouse.move(-3, -_delta)
	mouse.release(Button.right)
	mouse.move(3, _delta)

def testMouseOK():
	
	n = 0
	delta = 0
	while True:
		n = n+1
		if n > 100:
			delta = 0
		else:
			delta = 1
		mouse.press(Button.right)
		mouse.press(Button.left)
		mouse.move(0, -1)
		mouse.release(Button.right)
		mouse.release(Button.left)
		mouse.move(0, +1)
		sleep(0.01)
		mouse.press(Button.right)
		mouse.move(-3, -delta)
		mouse.release(Button.right)
		mouse.move(3, delta)
