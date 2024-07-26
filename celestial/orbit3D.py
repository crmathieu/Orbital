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
import pytz
import datetime
#import time

#import sys
from random import *

import numpy as np
from celestial.rate_func import F
from vpython_interface import ViewPort, Color
from visual import *
from visual.controls import *
import wx

#import spice

from location import EarthLocations
from planetsdata import *
from utils import deg2rad, rad2deg #, sleep

from camera import camera3D
from objects import simpleArrow
from referentials import make3DaxisReferential, makeBasicReferential

import json

# CLASS SOLARSYSTEM -----------------------------------------------------------
class makeSolarSystem:

	CELESTIAL_RADIUS = 500 # 2000 #10000
	INNER_RING_COEF = 1.3
	OUTER_RING_COEF = 1.9
	RING_INCREMENT = 0.6
	SCENE_WIDTH = 1920
	SCENE_HEIGHT = 1080
	bodies = []

	def __init__(self):
		print "### vpython v"+version[0]+"-"+version[1]+" ###"

		self.locationInfo = EarthLocations()
		self.todayUTCdatetime = self.locationInfo.getUTCDateTime()
		self.SurfaceView = False
		self.SurfaceDirection = [0,0,0]
		self.nameIndex = {}

		self.Dashboard = None
		self.AbortSlideShow = False
		self.SlideShowInProgress = False
		self.currentSource = PHA
		self.JTrojansIndex = -1
		self.cameraViewTargetBody = None
		self.cameraViewTargetSelection = SUN_NAME

		# create a base window to support adding overlay on Scene
		#self.baseWindow = self.createBaseWindow()

		# create the main display area
		self.Scene = ViewPort(	#window = self.baseWindow, 
								title = 'Solar System', 
								width  = self.SCENE_WIDTH, 
								height = self.SCENE_HEIGHT,
								x=0, #window.dwidth, 
								y=0, #window.dheight, #+window.menuheight,
								style=wx.NO_BORDER|~(wx.CAPTION|wx.CLOSE_BOX|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER),
								#style=wx.FRAME_FLOAT_ON_PARENT & ~(wx.RESIZE_BORDER), 
								#range=3, 
								#style=~(wx.CLIP_CHILDREN),
								fullscreen = True,
								visible=True) #, center = (0,0,0))
		self.Scene.up=(0,0,1)
		self.Scene.forward = vector(2, 0, -1)
		self.Scene.fov = deg2rad(60) 	
		#self.Scene.win.SetTransparent(255)
		#self.Scene.fullscreen = True

		#self.AltScene = ViewPort(title = 'XXXXXXXXXX', width = self.SCENE_WIDTH, height =self.SCENE_HEIGHT, range=3, visible=True, center = (0,0,0))
		#self.AltScene.fullscreen = True
		#self.Scene.select()

		self.UniversRadius = self.CELESTIAL_RADIUS * AU * DIST_FACTOR

		# the scene camera is a read only vector whose coordinates can be changed 
		# only through mouse events and/or resetting the scene Center
		self.camera = camera3D(self)
		
		self.objects_data = objects_data

		# TimeIncrement is a float representing the time quantity value by which 
		# the solar system planet positions get updated with every tick
		# during an animation - In fraction of day (from 1sec -> 1day)
		# for 1sec, TimeIncrement = 1/86400
		# for 1day, TimeIncrement = 1.0
		self.TimeIncrement = INITIAL_TIMEINCR 

		if False:
			#self.CorrectionSize = self.BodyRadius*DIST_FACTOR/1.e-2
			self.CorrectionSize = SUN_R * DIST_FACTOR / 1.e-2

			#self.Rotation = 25.05 # in days to complete a full rotation
			self.RotAngle = 0
			#self.AxialTilt = 7.25 # Sun axial tilt in degres
			#self.Position = vector(0,0,0)

			self.SizeCorrection = [1] * 2
			self.RealisticCorrectionSize = SUN_SZ_CORRECTION

			self.SizeCorrection[0] = 60
			self.SizeCorrection[1] = self.RealisticCorrectionSize 

			#self.sizeCorrectionType = OUTERPLANET

		self.sizeType 		= SCALE_OVERSIZED
		self.EarthRef 		= None
		self.Sun 			= None
		self.ShowFeatures 	= 0

		# make all light coming from origin
		self.sunLight = local_light(pos=(0,0,0), color=Color.white)
		self.Scene.ambient = Color.black
		self.Scene.background = Color.black

		if THREE_D:
			self.Scene.stereo='redcyan'
			self.Scene.stereodepth = 1

		self.toggleSize(False)

		######################################################
		self.CenterRef = self.makeSolarSystemReferential()
		self.CenterRef.setAxisTilt(0)
		######################################################
		self.makeCelestialSphere()
		self.makeConstellations()

		print "initial CAMERA POSITION ************************* ", self.Scene.mouse.camera

		#self.Scene.scale = self.Scene.scale * 10

	def getBaseWindow(self):
		return self.baseWindow

	def createBaseWindow(self):
		w = window(	x=0, y=0,
						width=(self.SCENE_WIDTH), #+window.dwidth), 
						height=(self.SCENE_HEIGHT), #+window.dheight+window.menuheight),
           				menus=False,
						#title='CACA',
           				style=(wx.NO_BORDER),
						#style=wx.CAPTION|wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX|wx.CLOSE_BOX ,
						#style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.CAPTION | wx.CLOSE_BOX,
						fullscreen = False) #wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
		#w.win.SetTransparent(0)
		return w

	def makeSolarSystemReferential(self):
		print "building Solar System Referential"
		return make3DaxisReferential({
					'body':			None,
					'radius': 		5*AU*DIST_FACTOR,
					'tiltangle': 	0,
					'show':			True,
					'color': 		Color.white,
					'ratio': 		[1,1,0.1],
					'legend': 		[u"\u2648", u"\u2649", "z"]
#					'legend': 		["x","y","z"],
				})		

	def rotateSolarSystemReferential(self, axis = vector(0,0,1)):
		self.Scene.up = axis

	def displaySolarSystem(self):
		sleep(1e-2)

	def setAutoScale(self, trueFalse):
		self.Scene.autoscale = trueFalse

	def introZoomIn(self, velocity):
		self._set_autoMovement(True)
		self.camera.cameraSet(velocity)
		self._set_autoMovement(False)

	def _set_autoMovement(self, is_movement):
		self.Scene._set_autoMovement(is_movement)

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x
		self.BodyShape.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]

	def setEarthLocations(self, db):
		self.setDashboard(db)
		self.camera.setEarthLocations()

	def getDashboard(self):
		return self.Dashboard

	def setDashboard(self, db):
		self.Dashboard = db

	def makeConstellations(self):
		import os.path
		#print "CELESTIAL SPHERE"
#		CELESTIAL_RADIUS = 2000 #10000
		#file = "./img/stars_const.tga"
		#file = "./img/starmap.tga"
		#file = "./img/star-map-normalized-4096x2048-reversed.tga"
		#file = "./img/8K-constellations-4-reversed.tga"
		#file = "./img/constellations_stars_to_MAG_21_RA_DEC_8192x4096_MONO-trimmed-deep-reversed.tga"
		#file = "./img/constellation_figures_8k-reversed.tga"
		#file = "./img/constellation_bounds_and_figures_8k-reversed.tga"
		#file = "./img/constellation_bounds_and_figures-8k-colored-reversed.tga"
		file = "./img/NASA/constellation_bounds_and_figures_colored_legend_reversed_8k.tga"

		if os.path.isfile(file):
			# adjust celestial Sphere position
			self.ConstellationOrigin = frame(pos=vector(0,0,0))
			self.Constellations = sphere(frame=self.ConstellationOrigin, pos=vector(0,0,0), visible = False, radius=self.UniversRadius, color=Color.white, opacity=0.2) #, up=vector(0,0,1))
			self.Constellations.material = materials.texture(data=materials.loadTGA(file), mapping="spherical", interpolate=False)

			# adjust constellations layout on our 3d window to match our coordinates system
			self.Constellations.rotate(angle=(pi/2), 		axis=self.CenterRef.XdirectionUnit, origin=(0,0,0))
			self.Constellations.rotate(angle=deg2rad(25), 	axis=self.CenterRef.YdirectionUnit, origin=(0,0,0))
			self.Constellations.rotate(angle=(pi/2), 		axis=self.CenterRef.ZdirectionUnit, origin=(0,0,0))

		else:
			print ("Could not find "+file)
		#self.Scene.scale = self.Scene.scale / 1e10

	def makeCelestialSphere(self): # Unused
		import os.path
		#print "CELESTIAL SPHERE"
#		CELESTIAL_RADIUS = 2000 #10000
		#file = "./img/8k_stars_milky_way-reversed.tga"
		file = "./img/NASA/starmap_8k-reversed.tga"

		if os.path.isfile(file):
			# adjust celestial Sphere position
			self.CelestialSphereOrigin = frame(pos=vector(0,0,0))
			self.Universe = sphere(frame=self.CelestialSphereOrigin, pos=vector(0,0,0), visible = False, radius=self.UniversRadius, color=Color.white, opacity=1.0) #, up=vector(0,0,1)) #0.8)
			self.Universe.material = materials.texture(data=materials.loadTGA(file), mapping="spherical", interpolate=False)
			
			# adjust celestial sphere layout on our 3d window to match our coordinates system
			self.Universe.rotate(angle=(pi/2), 		axis=self.CenterRef.XdirectionUnit, origin=(0,0,0))
			self.Universe.rotate(angle=deg2rad(25), axis=self.CenterRef.YdirectionUnit, origin=(0,0,0))
			self.Universe.rotate(angle=(pi/2), 		axis=self.CenterRef.ZdirectionUnit, origin=(0,0,0))

		else:
			print ("Could not find "+file)
		#self.Scene.scale = self.Scene.scale / 1e10


	# celestialSphere::animate
	def animate(self, deltaT):
		pass
		#self.setRotation()

	def isFeatured(self, type):
		return self.ShowFeatures & type

	def setFeature(self, type, value):
		if value == True:
			self.ShowFeatures |= type
		else:
			self.ShowFeatures = (self.ShowFeatures & ~type)
			if 	self.cameraViewTargetSelection != SUN_NAME and \
				self.cameraViewTargetBody.BodyType == type and \
				self.cameraViewTargetBody.Name.lower() != EARTH_NAME:
				# reset SUN as current ViewTarget when the currobject should not longer be visible
				return 1
		return 0

	def getTimeIncrement(self):
		#print "GTI-2", self.TimeIncrement
		return self.TimeIncrement

	def setTimeIncrement(self, value):
		self.TimeIncrement = value

	def setDefaultFeatures(self, flags):
		self.ShowFeatures = flags

	def resetView(self):
		self.Scene.center = (0,0,0)

	def updateCameraViewTarget(self, body):

		# the following values will do the following
		# (0,-1,-1): freezes rotation and looks down towards the left
		# (0,-1, 1): freezes rotation and looks up towards the left
		# (0, 1, 1): freezes rotation and looks up towards the right
		# (0, 1,-1): freezes rotation and looks down towards the right

		#self.SolarSystem.Scene.forward = (0, 0, -1)
		# For a planet, Foci(x, y, z) is (0,0,0). For a moon, Foci represents the position of the planet the moon orbits around
		self.cameraViewTargetBody = body
		self.cameraViewTargetSelection = body.Name.lower()
		self.Scene.center = (self.cameraViewTargetBody.Position[0]+self.cameraViewTargetBody.Foci[0],
							 self.cameraViewTargetBody.Position[1]+self.cameraViewTargetBody.Foci[1],
							 self.cameraViewTargetBody.Position[2]+self.cameraViewTargetBody.Foci[2])
		print self.Scene.center

	def register(self, sun):
		self.Sun = sun
		self.addTo(sun)

	def addTo(self, body):
		self.bodies.append(body)
		i = len(self.bodies) - 1
		self.nameIndex[body.JPL_designation.lower()] = i

		#print "Adding", body.Name
		if body.JPL_designation.lower() == EARTH_NAME:
			self.EarthRef = body
		return i # this is the index of the added body in the collection

	def addJTrojans(self, body):
		#print "Add Trojans"
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
		if self.JTrojansIndex >= 0:
			return self.bodies[self.JTrojansIndex]
		return None

	def drawAllBodiesTrajectory(self):
		for body in self.bodies:
			if body.BodyType in [OUTERPLANET, INNERPLANET, SATELLITE, DWARFPLANET, KUIPER_BELT, ASTEROID_BELT, INNER_OORT_CLOUD, ECLIPTIC_PLANE]:
				#print "drawing", body.Name
				body.draw()

		self.Scene.autoscale = False #0

	def getBodyFromName(self, jpl_designation):
		if jpl_designation in self.nameIndex:
			return self.bodies[self.nameIndex[jpl_designation]]
		return None

	def isRealsize(self):
		if self.ShowFeatures & REALSIZE != 0:
				return True
		return False

	def refresh(self, animationInProgress = False):
		orbitTrace 		= True if self.ShowFeatures & ORBITS 	!= 0 else False
		labelVisible 	= True if self.ShowFeatures & LABELS 	!= 0 else False
		realisticSize 	= True if self.ShowFeatures & REALSIZE 	!= 0 else False

		#self.toggleSize(realisticSize)

		for body in self.bodies:

			if body.BodyType in [SUN, SPACECRAFT, OUTERPLANET, INNERPLANET, ASTEROID, COMET, \
								 SATELLITE, DWARFPLANET, PHA, BIG_ASTEROID, TRANS_NEPT]:

				#print "FOUND BODY="+body.Name
				body.toggleSize(realisticSize)
				if body.BodyType == SUN:
					continue

				body.Origin.visible = True if self.ShowFeatures & body.BodyType != 0 else False ################################
#				body.toggleSize(realisticSize)
				if body.BodyType == OUTERPLANET:
					body.displayRings(body.Origin.visible) ############# NEW

				if body.Origin.visible == True:
					if body.Trail is not None:
						body.Trail.visible = orbitTrace
					if body.isMoon == True:
						# apply label on/off when moon in real size, otherwise do not show label
						value = labelVisible if body.sizeType == SCALE_NORMALIZED else False
					else:
						value = labelVisible

					for i in range(len(body.Labels)):
						body.Labels[i].visible = value
				else:
					pass #body.Origin.visible = bodyVisible

			else: # belts / rings
				if body.BodyType != ECLIPTIC_PLANE:
					
					if body.BodyShape.visible == True and animationInProgress == True:
						body.BodyShape.visible = False
						for i in range(len(body.Labels)):
							body.Labels[i].visible = False
		
		if self.ShowFeatures & LIT_SCENE != 0:
			print "LITE"
			self.Scene.ambient = Color.white
			self.sunLight.visible = False
			self.Sun.BodyShape.material = materials.texture(data=self.Sun.Texture, mapping="spherical", interpolate=False)
			self.Sun.BodyShape.opacity = 1.0
		else:
			print "DARK", self.Sun
			self.Scene.ambient = Color.nightshade #Color.black
			self.sunLight.visible = True
			self.Sun.BodyShape.material = materials.emissive
			
		setRefTo = True if self.ShowFeatures & REFERENTIAL != 0 else False
		
#		if 	self.cameraViewTargetSelection == self.Sun.JPL_designation and \
		if 	self.cameraViewTargetSelection == self.Sun.Name.lower() and \
			self.ShowFeatures & LOCAL_REFERENTIAL:
			setRelTo = True
		else:
			setRelTo = False

		self.setAxisVisibility(setRefTo, setRelTo)

		self.Universe.visible = self.isFeatured(CELESTIAL_SPHERE)
		self.Constellations.visible = self.isFeatured(CONSTELLATIONS)


	def refresh_SAVE(self, animationInProgress = False):
		orbitTrace 		= True if self.ShowFeatures & ORBITS 	!= 0 else False
		labelVisible 	= True if self.ShowFeatures & LABELS 	!= 0 else False
		realisticSize 	= True if self.ShowFeatures & REALSIZE 	!= 0 else False

		#self.toggleSize(realisticSize)

		for body in self.bodies:

			if body.BodyType in [SUN, SPACECRAFT, OUTERPLANET, INNERPLANET, ASTEROID, COMET, \
								 SATELLITE, DWARFPLANET, PHA, BIG_ASTEROID, TRANS_NEPT]:

				#print "FOUND BODY="+body.Name
				body.toggleSize(realisticSize)
				if body.BodyType == SUN:
					continue

				body.Origin.visible = True if self.ShowFeatures & body.BodyType != 0 else False ################################
#				body.toggleSize(realisticSize)
				if body.Origin.visible == True:
					if body.Trail is not None:
						body.Trail.visible = orbitTrace
					if body.isMoon == True:
						# apply label on/off when moon in real size, otherwise do not show label
						value = labelVisible if body.sizeType == SCALE_NORMALIZED else  False
					else:
						value = labelVisible

					for i in range(len(body.Labels)):
						body.Labels[i].visible = value
				else:
					pass #body.Origin.visible = bodyVisible

			else: # belts / rings
				if body.BodyType != ECLIPTIC_PLANE:
					
					if body.BodyShape.visible == True and animationInProgress == True:
						body.BodyShape.visible = False
						for i in range(len(body.Labels)):
							body.Labels[i].visible = False
		
		if self.ShowFeatures & LIT_SCENE != 0:
			print "LITE"
			self.Scene.ambient = Color.white
			self.sunLight.visible = False
			self.Sun.BodyShape.material = materials.texture(data=self.Sun.Texture, mapping="spherical", interpolate=False)
			self.Sun.BodyShape.opacity = 1.0
		else:
			print "DARK", self.Sun
			self.Scene.ambient = Color.nightshade #Color.black
			self.sunLight.visible = True
			self.Sun.BodyShape.material = materials.emissive
			
		setRefTo = True if self.ShowFeatures & REFERENTIAL != 0 else False
		
#		if 	self.cameraViewTargetSelection == self.Sun.JPL_designation and \
		if 	self.cameraViewTargetSelection == self.Sun.Name.lower() and \
			self.ShowFeatures & LOCAL_REFERENTIAL:
			setRelTo = True
		else:
			setRelTo = False

		self.setAxisVisibility(setRefTo, setRelTo)

		self.Universe.visible = self.isFeatured(CELESTIAL_SPHERE)
		self.Constellations.visible = self.isFeatured(CONSTELLATIONS)

	def setAxisVisibility(self, setRefTo, setRelTo):
		self.CenterRef.display(setRefTo)
		self.Sun.PCPF.updateReferential()
		self.Sun.PCPF.display(setRelTo)

		return
		for i in range(3):
			
			self.Axis[i].display(setRelTo)
			self.AxisLabel[i].visible = setRelTo

#			self.RefAxis[i].visible = setRefTo
			self.RefAxis[i].display(setRefTo) 
			self.RefAxisLabel[i].visible = setRefTo


# CLASS MAKEECLIPTIC ----------------------------------------------------------
class makeEcliptic:
	# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	# malfunctioning! Also the code has been altered to test earth's ecliptic, so it's totally malfunctioning
	# to REVIEW urgently after the time issue has been solved
	# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	def __init__(self, system, color, opacity):  # change default values during instantiation
		# draw a circle of 250 AU
		self.Labels = []
		self.Name = "Ecliptic Plane"
		self.Iau_name = "ecliptic"
		self.JPL_designation = "ecliptic"
		self.SolarSystem = system
		self.Color = color
		self.Opacity = opacity
		self.Lines = []
		self.BodyType = ECLIPTIC_PLANE
		self.Origin = frame()
		self.Labels.append(label(pos=(250*AU*DIST_FACTOR, 250*AU*DIST_FACTOR, 0), text=self.Name, xoffset=20, yoffset=12, space=0, height=10, border=6, box=false, font='sans', visible = False))

	def toggleSize(self, realisticSize):
		pass

	def rotate(self):
		pass 

	def drawXX(self):
		pass

	def draw(self):
		#print ("Drawing ecliptic")
		side = 250*AU*DIST_FACTOR
		self.BodyShape = box(frame=self.Origin, pos=vector(0, 0, 0), length=side, width=0.0001, height=side, material=materials.emissive, color=self.Color, opacity=0.1) #, axis=(0, 0, 1), opacity=0.8) #opacity=self.Opacity)
		self.Origin.visible = False

	def refresh(self):
		#print("Refresh Ecliptic")
		self.Origin.visible = True if (self.SolarSystem.ShowFeatures & ECLIPTIC_PLANE) != 0 else False


# CLASS MAKEBELT --------------------------------------------------------------
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
		self.BodyShape = points(pos=(self.RadiusMinAU, 0, 0), size=size, color=(color[0]*0.5, color[1]*0.5, color[2]*0.5))

		self.BodyShape.visible = False
		if self.Thickness == 0:
			self.Thickness = (self.RadiusMinAU + self.RadiusMaxAU)/2 * math.tan(math.pi/6)
		#shape = "cube"

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

		self.Labels.append(label(pos=(self.RadiusMaxAU * AU * DIST_FACTOR * cos(i), self.RadiusMaxAU * AU * DIST_FACTOR * sin(i), 0), text=self.Name, xoffset=20, yoffset=12, space=0, height=10, border=6, box=False, font='sans', visible = False))

	def refresh(self):
		if self.SolarSystem.ShowFeatures & self.BodyType != 0:
			if self.BodyShape.visible == False:
				self.BodyShape.visible = True
			labelVisible = True if self.SolarSystem.ShowFeatures & LABELS != 0 else False

			for i in range(len(self.Labels)):
				self.Labels[i].visible = labelVisible

		else:
			if self.BodyShape.visible == true:
				self.BodyShape.visible = false
				for i in range(len(self.Labels)):
					self.Labels[i].visible = False

# CLASS MAKETROJAN ------------------------------------------------------------
class makeJtrojan(makeBelt):

	def __init__(self, system, key, name, bodyType, color, size, density = 1, planetname = None):
		makeBelt.__init__(self, system, key, name, bodyType, color, size, density, planetname)
		self.Planet = self.SolarSystem.getBodyFromName(self.SolarSystem.objects_data[self.PlanetName]['jpl_designation'])
		if self.Planet is not None:
			self.JupiterX = self.Planet.Position[0]
			self.JupiterY = self.Planet.Position[1]
		else:
			self.JupiterX = 0
			self.JupiterY = 0

	def updateThickness(self, increment):
		self.RadiusMinAU = belt_data["jupiterTrojan"]["radius_min"]	- sqrt(increment) # in AU
		self.RadiusMaxAU = belt_data["jupiterTrojan"]["radius_max"]	+ sqrt(increment) # in AU
		self.Thickness = belt_data["jupiterTrojan"]["thickness"]	+ sqrt(increment)

	def draw(self):
		# determine where the body is
		#if self.PlanetName is not None:
		#	return

		# grab Jupiter's current True Anomaly and add the Long. of perihelion to capture
		# the current angle in the fixed referential
		Nu = deg2rad(toRange(rad2deg(self.Planet.Nu) + self.Planet.Longitude_of_perihelion))

		# get Lagrangian L4 and L5 based on body position
		L4 = (Nu + pi/3 )
		L5 = (Nu - pi/3)

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


# CLASS MAKEBODY --------------------------------------------------------------
"""
Main class describing system bodies, from star, 
to planets, asteroids, comets, spacecrafts etc 
"""
class makeBody:

	RING_BASE_THICKNESS = 2000
	STILL_ROTATION_INTERVAL = 50 #5 * 60 # (in seconds)
	def __init__(self, system, key, color, bodyType = INNERPLANET, sizeCorrectionType = INNERPLANET, RealisticCorrectionSize = SMALLBODY_SZ_CORRECTION, centralBody = None):  # change default values during instantiation

		self.Labels = []
		self.compounded = False
		self.CentralBody = centralBody
		self.isMoon = False
		self.RealisticCorrectionSize = RealisticCorrectionSize
		self.sizeCorrectionType = sizeCorrectionType

		self.Foci = vector(0,0,0)
		if centralBody is not None:
			self.Foci = vector(centralBody.Position[0], centralBody.Position[1], centralBody.Position[2])
		
		# load body data to data structure

		self.ObjectIndex = key
		self.SolarSystem 			= system
		self.locationInfo 			= system.locationInfo
		self.AxialTilt				= system.objects_data[key]["axial_tilt"]
		self.Name					= system.objects_data[key]["name"]				# body name
		if "symbol" in system.objects_data[key]:
			self.Symbol				= system.objects_data[key]["symbol"]			# body symbol
		else:
			self.Symbol				= " "
		self.Iau_name				= system.objects_data[key]["iau_name"]			# body iau name
		self.JPL_designation 		= system.objects_data[key]["jpl_designation"]
		self.Mass 					= system.objects_data[key]["mass"]				# body mass
		self.BodyRadius 			= system.objects_data[key]["radius"]			# body radius
		self.Color 					= color
		self.BodyType 				= bodyType
		self.BodyShape 				= None

		self.Revolution 			= system.objects_data[key]["PR_revolution"]
		self.Perihelion 			= system.objects_data[key]["QR_perihelion"]		# body perhelion
		self.Distance 				= system.objects_data[key]["QR_perihelion"]		# body distance at perige from focus
		self.Details				= False
		self.hasRenderedOrbit		= False
		self.Absolute_mag			= system.objects_data[key]["absolute_mag"]
		self.Trail					= None
		self.Position 				= np.matrix([[0],[0],[0]], np.float64)
		self.wasAnimated 			= False
		self.rotationInterval 		= self.STILL_ROTATION_INTERVAL
		self.Rotation 				= system.objects_data[key]["rotation"] if "rotation" in system.objects_data[key] else 0
		self.RotAngle 				= 0
		self.TiltAngle 				= deg2rad(self.AxialTilt) 						# in the ecliptic coordinates system
		
		# set scaling using bodyScaler dictionary based on body type  ...
		self.sizeType 				= SCALE_OVERSIZED
		self.SizeCorrection 		= {	SCALE_OVERSIZED: 	bodyScaler[sizeCorrectionType], 
										SCALE_NORMALIZED: 	self.RealisticCorrectionSize} 
		# for planets with rings
		self.Rings 					= []
		self.nRings 				= 0
		self.RingThickness 			= self.RING_BASE_THICKNESS / self.SizeCorrection[self.sizeType]

		if self.BodyRadius < DEFAULT_RADIUS:
			self.radiusToShow 		= DEFAULT_RADIUS
		else:
			self.radiusToShow 		= self.BodyRadius

		if "tga_name" in system.objects_data[key]:
			self.Tga 				= system.objects_data[key]["tga_name"]
		else:
			self.Tga 				= ""

		self.Moid = system.objects_data[key]["earth_moid"] if "earth_moid" in system.objects_data[key] else 0
		#############################
		self.setOrbitalElements(key)

		self.b = self.getSemiMinor(self.a, self.e)
		self.Aphelion = getAphelion(self.a, self.e)	# body aphelion

		# generate 2d coordinates in the initial orbital plane, with +X pointing
		# towards periapsis. Make sure to convert degree to radians before using
		# any sin or cos function

		self.setPolarCoordinates(deg2rad(self.E))

		# calculate current position of body on its orbit knowing
		# its current distance from Sun (R) and angle (Nu) that
		# were set up in setPolarCoordinates

		self.N = deg2rad(self.Longitude_of_ascendingnode)
		self.w = deg2rad(self.Argument_of_perihelion)
		self.i = deg2rad(self.Inclination)

		# convert polar to Cartesian in Sun referential
		self.Position = self.setCartesianCoordinates()
		##### self.shape = bodyShaper[bodyType]

		# calculate North Pole direction based on Right Ascension information
		self.RA = self.setNorthPoleRightAscensionAngle()
		
		# Create referentials:
		# The PCI referential (the "Planet-Centered Inertial" is fixed to the stars, in other words, 
		# it doesn't rotate with the planet). PCI coordinate frames have their origins at the center of mass of the planet 
		# and are fixed with respect to the stars. "I" in "PCI" stands for inertial (i.e. "not accelerating"), in 
		# contrast to the "Planet-centered - Planet-fixed" (PCPF) frames, which remains fixed with respect to 
		# the planet's surface in its rotation, and then rotates with respect to stars.
		#
		# For objects in space, the equations of motion that describe orbital motion are simpler in a non-rotating 
		# frame such as PCI. The PCI frame is also useful for specifying the direction toward celestial objects:
		#
		# To represent the positions and velocities of terrestrial objects, it is convenient to use PCPF coordinates 
		# or latitude, longitude, and altitude.
		#
		# In a nutshell: 
    	#		PCI: inertial, not rotating, with respect to the stars; useful to describe motion of 
		# 		celestial bodies and spacecraft.
		#
    	#		PCPF: not inertial, accelerated, rotating w.r.t stars; useful to describe motion of 
		# 		objects on Earth surface.

		# The default PCI is just None. Planets and Sun must override this 
		# method with a make3DaxisReferential call as they display the referential
		# upon user demand. 
		self.make_PCI_referential(self.TiltAngle)

		# determine axis of rotation
		self.setRotAxis() #self.TiltAngle)

		# set Planet-Centered-Planet_fixed referential (PCPF)
		self.make_PCPF_referential(self.TiltAngle) #, defaultaxis=self.PCI.RotAxis) # this referential moves and rotates with the planet  ####self.radiusToShow/self.SizeCorrection[self.sizeType], self.Position) #(self.Position[0],self.Position[1],self.Position[2]))

		# create body shape ...
		self.makeShape()
		# ... and add its texture 
		self.setAspect(key)

		# Now that texture has been properly positioned, tilt the body
		# by rotating the referential attached to it (PCPF)
		self.setPCPFAxisTilt()

		# create planet orbit curve and 1st vertex as the current position
		if self.makeOrbit() == False:
			return

		# add label
		self.Labels.append(label(pos=(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]), text=self.Symbol+self.Name, xoffset=20, yoffset=12, space=0, height=10, color=color, border=6, box=False, font='sans'))

		# hide body if not required
		if (self.SolarSystem.ShowFeatures & bodyType) == 0:
			self.Origin.visible = False
			self.Labels[0].visible = False

		# set body specific rotation characteristics
		self.initRotation()

	#### makeBody methods in the order they are called in the __init__ constructor ####

	# makeBody::setNorthPoleRightAscensionAngle to determine the direction of a planet's North Pole)
	def setNorthPoleRightAscensionAngle_XXXX(self):
		if "RA_1" in self.SolarSystem.objects_data[self.ObjectIndex]:
			T = daysSinceJ2000UTC(self.locationInfo)/EARTH_CENTURY #36525. # T is in centuries
			D = daysSinceJ2000UTC(self.locationInfo)
#			return 90 + self.SolarSystem.objects_data[self.ObjectIndex]["RA_1"] + self.SolarSystem.objects_data[self.ObjectIndex]["RA_2"] * D #T
			return self.SolarSystem.objects_data[self.ObjectIndex]["RA_1"] + self.SolarSystem.objects_data[self.ObjectIndex]["RA_2"] * D #T
		return 0

	def setNorthPoleRightAscensionAngle(self):
		if "rotationalElts" in self.SolarSystem.objects_data[self.ObjectIndex]:
			#T = daysSinceJ2000UTC(self.locationInfo)/EARTH_CENTURY #36525. # T is in centuries
			D = daysSinceJ2000UTC(self.locationInfo)
			RE = self.SolarSystem.objects_data[self.ObjectIndex]["rotationalElts"]
			return RE["W_1"] + RE["W_2"] * D + RE["W_C"] # "W_C" is a correction factor
		return 0

	# this the referential fixed to the star. default is None (mostly for objects that don't
	# require it such as PHA, comets, asteroids). Planets and the Sun must override this method
	# to create a 3D referential, as it can be displayed through the user interface.
	def make_PCI_referential(self, tiltAngle): 
		self.PCI = None 

	def setRotAxis(self): 
		if self.PCI is not None:
			self.RotAxis = self.PCI.RotAxis
		else:
			self.RotAxis = self.setObliquity()

	def setObliquity(self): 
		print "setObliquity for ", self.Name
		return vector(0, sin(self.TiltAngle), cos(self.TiltAngle))

	def getRotAxis(self):
		return self.RotAxis

	# This is the referential that rotates with the body:
	# default PCPF referential: just a frame with no referential. Body texture is linked to
	# this referential and rotate with it. Only the makeEarth class must override this 
	# method as its PCPF requires to display its axis.
	def make_PCPF_referential(self, tiltAngle): 
	
		#print "build PCPF ref for", self.Name
		self.PCPF = makeBasicReferential({
			'body': self,
			'tiltangle': -tiltAngle,
			'show':	False,
			'color': Color.cyan
		})
		self.Origin 				= self.PCPF.referential
		self.Origin.visible			= True

		# the tilt will be initiated after loading the body texture
		self.PCPF.display(True)



	def getSemiMinor(self, semimajor, eccentricity):
		# knowing the perihelion, the formula is given by rp = a(1-e)
		return semimajor * sqrt(1 - eccentricity**2)

	def setAspect(self, key):
		self.Texture = materials.loadTGA("./img/"+self.Tga) if self.SolarSystem.objects_data[key]["material"] != 0 else materials.loadTGA("./img/asteroid")
		self.BodyShape.material = materials.texture(data=self.Texture, mapping="spherical", interpolate=False)

	def makeShape(self):
		self.Origin.pos=(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2])
		self.BodyShape = sphere(frame=self.Origin, pos=(0,0,0), np=64, radius=self.getBodyRadius(), make_trail=false, up=(0,0,1))

	def getBodyRadius(self):
		return self.radiusToShow/self.SizeCorrection[self.sizeType]

	def setPCPFAxisTilt(self):
		if self.PCPF is not None:
			self.PCPF.setAxisTilt(self.RA)

	def makeOrbit(self):
		# attach a curve to the object to display its orbit
		if self.BodyShape is not None:
			# create an orbit in the solar system central referential
			self.Trail = curve(Color=(self.Color[0]*0.8, self.Color[1]*0.8, self.Color[2]*0.8))
			self.Trail.append(pos=self.Origin.pos)
			return True
		else:
			print "Failed to draw body", self.Name
			return False

	def initRotation(self):
		return

	def getRealisticSizeCorrection(self):
		return self.RealisticCorrectionSize

	def setRealisticSizeCorrection(self, value):
		self.RealisticCorrectionSize = value

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x
		self.BodyShape.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]

	def setTraceAndLabelVisibility(self, trueFalse):
		if self.Origin.visible == True:
			self.Trail.visible = trueFalse
			for i in range(len(self.Labels)):
				self.Labels[i].visible = trueFalse

	# makeBody::animate default
	def animate(self, timeIncrement):
		if self.hasRenderedOrbit == False:
			self.draw()

		self.wasAnimated = true
		#if timeIncrement != 0.0:

		#######################
		# update position
		#self.setOrbitalElements(self.ObjectIndex, timeIncrement)
		self.updateOrbitalElements(self.ObjectIndex, timeIncrement)
		self.setPolarCoordinates(deg2rad(self.E))

		# calculate current body position in its orbit knowing
		# its current distance from Sun (R) and True anomaly (Nu)
		# that were set in setPolarCoordinates

		self.N = deg2rad(self.Longitude_of_ascendingnode)
		self.w = deg2rad(self.Argument_of_perihelion)
		self.i = deg2rad(self.Inclination)

		# convert polar to Cartesian in Sun referential
		self.Position = self.setCartesianCoordinates()
		#print "ANIMATE: position=", self.Position
		# update foci position
		if self.CentralBody is not None:
			self.Foci = self.CentralBody.Position
			#print "central body position", self.Foci
			#raw_input("type a key...")

			#self.Trail.pos = self.Foci

		self.Origin.pos = self.Labels[0].pos = vector(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2])
		#self.Labels[0].pos = vector(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2])
		self.setRotation()
		return self.getCurrentVelocity(), self.getCurrentDistanceFromEarth(), self.getCurrentDistanceFromSun()

	# makeBody::setOrbitalElements (default)
	def setOrbitalElements(self, key, timeincrement = 0):
		# For comets, asteroids or dwarf planets, data comes from data
		# files -or- predefined values. Orbital Position is calculated
		# from the last time of perihelion passage. This is the default
		# behavior
		self.setOrbitalFromJPLhorizon(self.SolarSystem.objects_data[key], timeincrement) #-0.7)


	def setOrbitalFromJPLhorizon(self, elts, timeincrement=0):
		# data comes from data file or predefined values
		self.e 							= elts["EC_e"]
		self.Longitude_of_perihelion 	= elts["longitude_of_perihelion"]
		self.Longitude_of_ascendingnode = elts["OM_longitude_of_ascendingnode"]
		self.Argument_of_perihelion 	= self.Longitude_of_perihelion - self.Longitude_of_ascendingnode
		self.a 							= getSemiMajor(self.Perihelion, self.e)
		self.Inclination 				= elts["IN_orbital_inclination"]

		#if self.CentralBody is not None:
		#	self.Inclination -= self.CentralBody.AxialTilt
			
		self.Time_of_perihelion_passage = elts["Tp_Time_of_perihelion_passage_JD"]
		self.Mean_motion				= elts["N_mean_motion"]
		self.Epoch						= elts["epochJD"]
		self.Mean_anomaly				= elts["MA_mean_anomaly"] 	# the Mean Anomaly angle can also be computed using
																	# the orbital period and Time of perihelion as:
																	# M = (t - T) * 2*PI/P where T is the timeOfPerihelion,
																	# t is the current time and P the orbital period 
		self.revolution					= elts["PR_revolution"]
		self.OrbitClass					= elts["orbit_class"]

		# save original value of longitude of ascending node
		# (will be used to calculate current value of longOfAscMode in makeBody::updateOrbitalElements)
		self.Initial_longitude_of_ascendingNode = self.Longitude_of_ascendingnode

		# calculate current position based on orbital elements
		self.updateBodyPosition(timeincrement)
		"""
		#dT = daysSinceEpochJD(self.Epoch) + timeincrement # timeincrement comes in days
		

		dT = daysSinceEpochJD(self.Epoch, self.locationInfo) + timeincrement # - ADJUSTMENT_COEFFICIENT # substracting 0.5 to match for earth correction
#		dT = daysSinceEpochJD(self.Time_of_perihelion_passage) + timeincrement 

		# compute Longitude of Ascending node taking into account the time elapsed since epoch
		incrementYears = timeincrement / EARTH_PERIOD # 365.25
		self.Longitude_of_ascendingnode +=  0.013967 * (2000.0 - (getCurrentYear() + incrementYears)) + 3.82394e-5 * dT

		# adjust Mean Anomaly with time elapsed since epoch
		M = toRange(self.Mean_anomaly + self.Mean_motion * dT)
		success, self.E, dE, it = solveKepler(M, self.e, 20000)
		if success == False:
			print (self.Name+" Warning Could not converge - E = "+str(self.E))
		"""
	# makeBody::updateOrbitalElements (default)
	# Called from the makeBody::animate method
	def updateOrbitalElements(self, key, timeincrement = 0):
		# first restore original longitude of ascending node
		self.Longitude_of_ascendingnode = self.Initial_longitude_of_ascendingNode
		self.updateBodyPosition(timeincrement)

	def updateBodyPosition(self, timeIncrement):
		# calculate current position based on orbital elements (timeIncrement comes in days as a float)
		dT = daysSinceEpochJD(self.Epoch, self.locationInfo) + timeIncrement # - ADJUSTMENT_COEFFICIENT # substracting 0.5 to match for earth correction

		# compute Longitude of Ascending node taking into account the time elapsed since epoch
		incrementYears = timeIncrement / EARTH_PERIOD # 365.25
		self.Longitude_of_ascendingnode +=  0.013967 * (2000.0 - (getCurrentYear() + incrementYears)) + 3.82394e-5 * dT

		# adjust Mean Anomaly with time elapsed since epoch
		self.Mean_anomaly = toRange(self.Mean_anomaly + self.Mean_motion * dT)
		success, self.E, dE, it = solveKepler(self.Mean_anomaly, self.e, 20000)
		if success == False:
			print (self.Name+" Warning Could not converge - E = "+str(self.E))

	def update_referentials(self):
		if self.PCI is not None:
			self.PCI.updateReferential()
		#if self.PCPF is not None:	
		self.PCPF.updateReferential()
		self.PCPF.rotate(angle=self.RotAngle)

		#self.PCI.referential.pos = self.Position
		#self.update_PCPF_PositionRotation()

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
	# makeBody::computeOrbitalEltFromPlanetPositionApproximation default
	def computeOrbitalEltFromPlanetPositionApproximation(self, elts, timeincrement):
		# will calculate current value of approximate position of the major planets
		# including pluto. This won't work for Asteroid, Comets or Dwarf planets.
		# Principle: for every timeIncrement, all orbital elements are recalculated. 
		# This include aphelion, eccentricity and inclinaison, followed by 
		# long-of-ascending-node and argument-of-perihelion

		Adjustment = 0 #0.5

		# get number of days since J2000 epoch and obtain the fraction of century
		# (the rate adjustment is given as a rate per century)
		days = daysSinceJ2000UTC(self.locationInfo) + timeincrement #- ADJUSTMENT_FACTOR_PLANETS # - 1.43
		#T = (daysSinceJ2000UTC() + timeincrement)/36525. # T is in centuries

        # These formulas use 'days' based on days since 1/Jan/2000 12:00 UTC ("J2000.0"), 
        # instead of 0/Jan/2000 0:00 UTC ("day value"). Correct by subtracting 1.5 days...

		T = (days - Adjustment)/EARTH_CENTURY #36525. # T is in centuries (previous)

#		T = days/36525. # T is in centuries
# 		T = (days-1.5)/36525. # T is in centuries

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
		self.Mean_anomaly = toRange(L - self.Longitude_of_perihelion) #W)

		# Obtain ecc. Anomaly E (in degrees) from M using an approx method of resolution:
		success, self.E, dE, it = solveKepler(self.Mean_anomaly, self.e, 12000)
		if success == False:
			print ("Could not converge for "+self.Name+", E = "+str(self.E)+", last precision = "+str(dE))

	def getIncrement(self):
		# provide 1 degree increment in radians
		return pi/180

	def draw(self):
		#print "Rendering orbit for ", self.Name
		self.Trail.visible = False
		rad_E = deg2rad(self.E)
		increment = self.getIncrement()
#		print("draw: X = ", self.a * (cos(rad_E) - self.e), "Y =", self.a * sqrt(1 - self.e**2) * sin(rad_E))

#		for E in np.arange(increment, 2*pi+increment, increment):
#		for E in np.arange(0, 2*pi, increment):
		for E in np.arange(0, 2*pi+increment, increment):
			self.setPolarCoordinates(E+rad_E)
			# from R and Nu, calculate 3D coordinates and update current position
			self.drawSegment(trace = True) #E*180/pi)
			### rate(5000) # ??

#		if self.BodyShape.visible:
		if self.Origin.visible:
			self.Trail.visible = True

		self.hasRenderedOrbit = True
		#print "DRAW: origin.pos=",self.Origin.pos, "label.pos=", self.Labels[0].pos

	def setPolarCoordinates(self, E_rad):
		X = self.a * (cos(E_rad) - self.e)
		Y = self.a * sqrt(1 - self.e**2) * sin(E_rad)
		# Now calculate current Radius and true Anomaly
		self.R = sqrt(X**2 + Y**2)
		self.Nu = atan2(Y, X)
		# Note that atan2 returns an angle in
		# radian, so Nu is always in radian


	# default initRotation behavior
	def initRotationXX(self):
	#	TEXTURE_POSITIONING_CORRECTION = pi/12
		# we need to rotate around X axis by pi/2 to properly align the planet's texture
###		self.Origin.rotate(angle=(pi/2+self.TiltAngle), axis=self.XdirectionUnit, origin=(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]))
		self.Origin.rotate(angle=(pi/2 - self.TiltAngle), axis=self.PCI.XdirectionUnit, origin=(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]))

		# then further rotation will apply to Z axis
		self.RotAxis = self.PCI.ZdirectionUnit
		
		# calculate current RA, to position the obliquity properly:
		if "RA_1" in self.SolarSystem.objects_data[self.ObjectIndex]:
			T = daysSinceJ2000UTC(self.locationInfo)/EARTH_CENTURY #36525. # T is in centuries
			self.RA = self.SolarSystem.objects_data[self.ObjectIndex]["RA_1"] + self.SolarSystem.objects_data[self.ObjectIndex]["RA_2"] * T
			self.Origin.rotate(angle=deg2rad(self.RA), axis=self.PCI.ZdirectionUnit, origin=(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]))
		#else:
		#	print "No RA for " +self.Name




	def update_PCPF_RotationXX(self):
		# here the widgets rotates by the same amount the earth texture is rotated
		self.referential.pos = self.Position
		ti = self.SolarSystem.getTimeIncrement()
		RotAngle = (2*pi/self.Rotation)*ti

		# update RotAxis vector
		self.PCPF.RotAxis = self.PCPF.referential.frame_to_world(self.PCPF.ZdirectionUnit)
		print self.PCPF.RotAxis

		# if polar axis inverted, reverse rotational direction
		#print self.RotAxis
#		if self.PCPF.ZdirectionUnit[2] < 0:
		if self.PCPF.RotAxis[2] < 0:
			RotAngle *= -1

		# follow planet rotation
		self.PCPF.referential.rotate(angle=RotAngle, axis=self.PCPF.RotAxis) #, origin=(0,0,0)) #self.PCPF.referential.pos) #(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]))
#		self.PCPF.referential.rotate(angle=RotAngle, axis=self.PCPF.ZdirectionUnit) #, origin=(0,0,0)) #self.PCPF.referential.pos) #(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]))

	def update_PCI_Position(self):
		self.PCI.referential.pos = self.Position

	def update_PCPF_PositionRotation_SAVE(self):		
		self.PCPF.referential.pos = self.Position
		# here the widgets rotates by the same amount the earth texture is rotated

		ti = self.SolarSystem.getTimeIncrement()
		RotAngle = (2*pi/self.Rotation)*ti

		if self.PCPF.RotAxis[2] < 0:
			RotAngle *= -1

		self.PCPF.rotate(RotAngle)

		# update RotAxis vector
		#self.PCPF.RotAxis = self.PCPF.referential.frame_to_world(self.PCPF.ZdirectionUnit)
		#print self.PCPF.RotAxis

		# if polar axis inverted, reverse rotational direction
		#print self.RotAxis
#		if self.PCPF.ZdirectionUnit[2] < 0:
		#if self.PCPF.RotAxis[2] < 0:
		#	RotAngle *= -1

		# follow planet rotation
		#self.PCPF.referential.rotate(angle=RotAngle, axis=self.PCPF.RotAxis) #, origin=(0,0,0)) #self.PCPF.referential.pos) #(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]))
#		self.PCPF.referential.rotate(angle=RotAngle, axis=self.PCPF.ZdirectionUnit) #, origin=(0,0,0)) #self.PCPF.referential.pos) #(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]))

	def update_PCPF_PositionRotationXX(self):
		# here the widgets rotates by the same amount the earth texture is rotated
		self.PCPF.referential.pos = self.Position
		ti = self.SolarSystem.getTimeIncrement()
		RotAngle = (2*pi/self.Rotation)*ti

		# update RotAxis vector
		self.PCPF.RotAxis = self.PCPF.referential.frame_to_world(self.PCPF.ZdirectionUnit)

		if self.PCPF.RotAxis[2] < 0:
			RotAngle *= -1

	###	self.PCPF.rotate(RotAngle)

		# update RotAxis vector
		#self.PCPF.RotAxis = self.PCPF.referential.frame_to_world(self.PCPF.ZdirectionUnit)
		#print self.PCPF.RotAxis

		# if polar axis inverted, reverse rotational direction
		#print self.RotAxis
#		if self.PCPF.ZdirectionUnit[2] < 0:
		#if self.PCPF.RotAxis[2] < 0:
		#	RotAngle *= -1

		# follow planet rotation
		self.PCPF.referential.rotate(angle=RotAngle, axis=self.PCPF.RotAxis) #, origin=(0,0,0)) #self.PCPF.referential.pos) #(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]))
#		self.PCPF.referential.rotate(angle=RotAngle, axis=self.PCPF.ZdirectionUnit) #, origin=(0,0,0)) #self.PCPF.referential.pos) #(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]))

	# default
	def setRotation(self):
		ti = self.SolarSystem.getTimeIncrement()
		self.RotAngle = (2*pi/self.Rotation)*ti

		# if polar axis inverted, reverse rotational direction
#		if self.PCI.ZdirectionUnit[2] < 0:
#			self.RotAngle *= -1

		if self.RotAxis[2] < 0:
			self.RotAngle *= -1

		self.update_referentials()
		#self.PCPF.rotate(angle=self.RotAngle)

		#self.Origin.rotate(angle=self.RotAngle, axis=self.RotAxis, origin=(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]))
		return


		self.update_PCI_Position()
		self.update_PCPF_PositionRotation()
		return

		ti = self.SolarSystem.getTimeIncrement()
		self.RotAngle = (2*pi/self.Rotation)*ti
		# if polar axis inverted, reverse rotational direction
		if self.PCPF.ZdirectionUnit[2] < 0:
			self.RotAngle *= -1

		self.updateAxis()
		self.Origin.rotate(angle=self.RotAngle, axis=self.RotAxis, origin=(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]))

	def drawSegment(self, trace = True):
		self.Position = self.setCartesianCoordinates()
		self.Origin.pos = vector(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2])
		if trace:
			# display orbit in brighter Color when above ecliptic
			if self.Position[2]+self.Foci[2] < 0:
				"""
				self.Interval += 1
				if self.Interval % 2 == 0:
					#self.Trail.append(pos=self.BodyShape.pos, color=self.Color) #, interval=50)
					self.Trail.append(pos=self.BodyShape.pos, color=(self.Color[0]*0.3, self.Color[1]*0.3, self.Color[2]*0.3))			
				else:
					self.Trail.append(pos=self.BodyShape.pos, color=Color.black) #, interval=50)
				"""
				# new
				self.Trail.append(pos=self.Origin.pos, color=(self.Color[0]*0.3, self.Color[1]*0.3, self.Color[2]*0.3))
			else:
				self.Trail.append(pos=self.Origin.pos, color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))

	def setCartesianCoordinates(self):
		# from polar coordinates, deduct cartesian coordinates in ecliptic referential, using the current distance to object (R), the 
		# True anomaly (Nu), and the orbital parameters pertaining to the orbit's orientation: (N, i, w) 
#		self.Position[0] = self.R * DIST_FACTOR * ( cos(self.N) * cos(self.Nu+self.w) - sin(self.N) * sin(self.Nu+self.w) * cos(self.i) )
#		self.Position[1] = self.R * DIST_FACTOR * ( sin(self.N) * cos(self.Nu+self.w) + cos(self.N) * sin(self.Nu+self.w) * cos(self.i) )
#		self.Position[2] = self.R * DIST_FACTOR * ( sin(self.Nu+self.w) * sin(self.i) )
		return (self.R * DIST_FACTOR * ( cos(self.N) * cos(self.Nu+self.w) - sin(self.N) * sin(self.Nu+self.w) * cos(self.i) ),
				self.R * DIST_FACTOR * ( sin(self.N) * cos(self.Nu+self.w) + cos(self.N) * sin(self.Nu+self.w) * cos(self.i) ),
				self.R * DIST_FACTOR * ( sin(self.Nu+self.w) * sin(self.i) ))

		# finally, calculate these coordinates in our arbitrary definition of the Constellation of Pisces (Vernal Equinox) referential.
		########## self.Position = self.Rotation_VernalEquinox * self.Position  # modified on 06/11/22

	def show(self):
		if self.hasRenderedOrbit == False:
			self.draw()

		self.Origin.visible = True
		self.Trail.visible = True if self.SolarSystem.ShowFeatures & ORBITS != 0 else False

		trueFalse = self.SolarSystem.ShowFeatures & LABELS != 0
		for i in range(len(self.Labels)):
			self.Labels[i].visible = trueFalse
		"""
		if self.SolarSystem.ShowFeatures & LABELS != 0:
			for i in range(len(self.Labels)):
				self.Labels[i].visible = True
		else:
			for i in range(len(self.Labels)):
				self.Labels[i].visible = False
		"""

	def hide(self):
		self.Details = False
		self.Origin.visible = False
		for i in range(len(self.Labels)):
			self.Labels[i].visible = False
		self.Trail.visible = False

	def setAxisVisibility(self, setTo):
		#print "display PCI for ", self.Name, "as ", setTo
		if self.PCI is not None: 
			self.PCI.display(setTo)
		return

		for i in range(3):
#			self.Axis[i].visible = setTo
			self.PCI.Axis[i].display(setTo)
			self.PCI.AxisLabel[i].visible = setTo

	def refresh(self):
		if 	self.SolarSystem.SlideShowInProgress and \
			self.BodyType == self.SolarSystem.currentSource:
			return

		if 	self.BodyType & self.SolarSystem.ShowFeatures != 0 or \
			self.Name.lower() == EARTH_NAME or \
			self.Details == True:
			if self.Origin.visible == False:
				self.show()
			# if this is the cameraViewTargetBody, check for local referential attribute
#			if 	self.SolarSystem.cameraViewTargetSelection == self.JPL_designation and \
			if 	self.SolarSystem.cameraViewTargetSelection == self.Name.lower() and \
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
		return sqrt((self.Position[0] - self.SolarSystem.EarthRef.Position[0])**2 + \
					(self.Position[1] - self.SolarSystem.EarthRef.Position[1])**2 + \
					(self.Position[2] - self.SolarSystem.EarthRef.Position[2])**2)/DIST_FACTOR/AU

	def getCurrentDistanceFromSun(self):
		#return sqrt((self.Position[0])**2 + (self.Position[1])**2 + (self.Position[2])**2)/DIST_FACTOR/AU
		return mag(vector(self.Position)) / DIST_FACTOR / AU

class emptyTrail:
	visible = False

# CLASS MAKESUN ---------------------------------------------------------------
class makeSun(makeBody):
	
	def __init__(self, system, Color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makeBody.__init__(self, system, SUN_NAME, Color, ptype, sizeCorrectionType, defaultSizeCorrection, None) #system)
		self.BodyShape.visible = True
		self.Trail = emptyTrail()

	def makeShape(self):
		self.Origin.pos=(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2])
#		self.BodyShape = sphere(frame=self.Origin, pos=(0,0,0), np=64, radius=self.radiusToShow/self.SizeCorrection[self.sizeType], make_trail=False, color=Color.yellow)
		self.BodyShape = sphere(frame=self.Origin, pos=(0,0,0), np=64, radius=self.getBodyRadius(), make_trail=False, color=Color.yellow)
		#self.PCPF.referential.visible = True

	def setAspect(self, key):
		#print "loading"+"./img/"+self.Tga
		self.Texture = materials.loadTGA("./img/"+self.Tga) if self.SolarSystem.objects_data[key]["material"] != 0 else materials.loadTGA("./img/asteroid")
		#self.BodyShape.material = materials.texture(data=self.Texture, mapping="spherical", interpolate=False)
		print "setting sun as emissive"
		self.BodyShape.material = materials.emissive

	def updateStillPosition(self, timeinsec):
		pass

	def draw(self):
		self.hasRenderedOrbit = True
		
	def setPolarCoordinates(self, E_rad):
		self.R = 0
		self.Nu = 0

	def getCurrentVelocity(self):
		return 0

	def setCartesianCoordinates(self):
		return (0,0,0)

	def getSemiMinor(self, semimajor, eccentricity):
		pass

	def makeOrbit(self):
		pass

	# makeSun::setOrbitalElements (overrides makeBody::setOrbitalElements)
	def setOrbitalElements(self, key, timeincrement = 0):
		self.E = self.a = self.e = self.Longitude_of_ascendingnode = self.Argument_of_perihelion = self.Inclination = 0

	# makeSun::updateOrbitalElements (overrides makeBody::updateOrbitalElements)
	def updateOrbitalElements(self, key, timeIncrement):
		pass

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		self.BodyShape.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]


# CLASS PLANET ----------------------------------------------------------------
class makePlanet(makeBody):
	
	def __init__(self, system, key, Color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makeBody.__init__(self, system, key, Color, ptype, sizeCorrectionType, defaultSizeCorrection, system.Sun)
		#self.BodyShape.visible = False
		self.setRings()

	def make_PCPF_referentialXX(self, tiltAngle): ###########################
		self.PCPF = None

	def make_PCI_referential(self, tiltAngle): ###, size, position):
		# This is the referential that doesn't rotate with the planet and is fixed to the stars.
		# in other words, it always points to the same direction
		
		#print "Planet: build PCI ref for", self.Name
		self.PCI = make3DaxisReferential({
			'body': self,
			'radius': 0,
			'tiltangle': -tiltAngle,
			'show':	False,
			'color': Color.white,
			'ratio': [1,1,1],
			'legend': ["x", "y", "z"],
		})  

		self.Origin 				= self.PCI.referential
		self.Origin.visible			= True

		self.PCI.setAxisTilt(self.RA)
		self.PCI.display(False)
		#self.setRotAxis()

	# makePlanet::setOrbitalElements  (overrides makeBody)
	def setOrbitalElements(self, key, timeincrement = 0):
		# for the Major planets includig Pluto, we have Keplerian elements to calculate 
		# the body's current approximated position on orbit based on NASA formula <link-to-formula-here>
		self.updateOrbitalElements(key, timeincrement)
		#elt = self.SolarSystem.objects_data[key]["kep_elt_1"] if "kep_elt_1" in self.SolarSystem.objects_data[key] else self.SolarSystem.objects_data[key]["kep_elt"]
		#self.computeOrbitalEltFromPlanetPositionApproximation(elt, timeincrement)

	# makePlanet::updateOrbitalElements (overrides makeBody::updateOrbitalElements)
	# Called from the makeBody::animate method
	def updateOrbitalElements(self, key, timeincrement = 0):
		# updateOrbitalElements for planet consists of recalculating every single elements 
		# through the NASA formula. Hence it has the same functionality as the initial setOrbitalElements method
		elt = self.SolarSystem.objects_data[key]["kep_elt_1"] if "kep_elt_1" in self.SolarSystem.objects_data[key] else self.SolarSystem.objects_data[key]["kep_elt"]
		self.computeOrbitalEltFromPlanetPositionApproximation(elt, timeincrement)

	def setRotAxisXX(self):
		print "SET PCI.rotaAxis as AXIS for", self.Name
		self.RotAxis = self.PCI.RotAxis

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

		print "TOGGLING!"
		self.BodyShape.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]
		if self.nRings > 0:
			print "toggling rings for", self.Name
			#self.hideRings()
			self.removeRings()
			self.setRings()

	def setRings(self): #, colorArray):  # change default values during instantiation
		if self.Name.lower() in rings_data:
			ringData = rings_data[self.Name.lower()]["rings"]
			if ringData is not None:
				self.RingsFrame = frame()
				# make each ring element relative to the PCI Referential
				# so that they are aligned with the planet tilt and 
				# won't have to rotate
				self.RingsFrame.frame = self.PCI.referential				
				self.makeRings(ringData)

	def makeRings(self, ringData):
		#print "generating rings"
		self.nRings = 0
		for ring in ringData:
			curRadius = ring["radius"] / self.SizeCorrection[self.sizeType]
			thickness = 100e3 / self.SizeCorrection[self.sizeType]
			width = ring["width"] / self.SizeCorrection[self.sizeType]
			#print self.Name, "ring radius=", curRadius
			self.Rings.insert(self.nRings, self.makeRingElt(curRadius, width, thickness, ring["color"]))
			self.nRings += 1

	def makeRingElt_SAVE(self, radius, width, thickness, colour):

		ringframe = frame()
		straight = [(0,0,0),(0,0,thickness)]

		# shape of outer edge
		outerEdge = shapes.circle(pos=(0, 0), radius=radius, np=128)

		# shape of inner edge
		innerEdge = shapes.circle(pos=(0,0), radius=radius-width, np=128)

		# create ring body from extrusion
		body = extrusion(pos=straight, 
						shape=outerEdge-innerEdge,
						color=colour)

		body.frame = ringframe

#		ringframe.frame = self.Origin

		# make each ring element relative to the PCI Referential
		# so that they are aligned with the planet tilt and 
		# won't have to rotate
		ringframe.frame = self.PCI.referential

		#ringframe.rotate(angle=pi/2, axis=(1,0,0))
		#ringframe.rotate(angle=(self.TiltAngle), axis=(1,0,0))
		return ringframe

	def makeRingElt(self, radius, width, thickness, colour):

		#ringframe = frame()
		straight = [(0,0,0),(0,0,thickness)]

		# shape of outer edge
		outerEdge = shapes.circle(pos=(0, 0), radius=radius, np=128)

		# shape of inner edge
		innerEdge = shapes.circle(pos=(0,0), radius=radius-width, np=128)

		# create ring body from extrusion
		body = extrusion(pos=straight, 
						shape=outerEdge-innerEdge,
						color=colour)

		body.frame = self.RingsFrame
		
#		ringframe.frame = self.Origin

		# make each ring element relative to the PCI Referential
		# so that they are aligned with the planet tilt and 
		# won't have to rotate
		#ringframe.frame = self.PCI.referential

		#ringframe.rotate(angle=pi/2, axis=(1,0,0))
		#ringframe.rotate(angle=(self.TiltAngle), axis=(1,0,0))
		return body #ringframe

	def removeRings(self):
		print "attempting to remove rings..."

		for ring in self.Rings:
			print "hidding ring from", self.Name
			ring.visible = False
			del(ring)

		del(self.RingsFrame)
		del(self.Rings)
		self.Rings = []
		self.nRings = 0

	def removeRings2(self):
		print "attempting to remove rings..."
		if self.nRings > 0:
			print "hidding rings from", self.Name
			#ring.visible = False
			#del(ring)
			del(self.Rings)
			del(self.RingsFrame)
			self.Rings = []
			self.nRings = 0

	def displayRings(self, trueFalse):
		if self.nRings > 0:
			#print "setting rings to ", trueFalse
			self.RingsFrame.visible = trueFalse

	def hideRings(self):
		print "attempting to hide rings..."
		self.displayRings(False)

		#if self.nRings > 0:
		#	self.Ringsframe.visible = False
		#return
		"""
		for ring in self.Rings:
			print "hidding ring from", self.Name
			ring.visible = False
			del(ring)

		self.Rings = []
		self.nRings = 0
		"""

	def showRings(self, planet):
		self.displayRings(True)
		return

		if self.nRings > 0:
			self.Ringsframe.visible = True
		return

		for i in range(0, self.nRings):
			planet.Rings[i].visible = True



ADJUSTMENT_COEFFICIENT = 0.5

# CLASS MAKEEARTH -------------------------------------------------------------
from widgets import *
class makeEarth(makePlanet):

	def __init__(self, system, ccolor, type, sizeCorrectionType, defaultSizeCorrection):
		self.Opacity = 0.4
		self.NumberOfSiderealDaysPerYear = 366.25

		# The angle we need to initially rotate the 
		# earth texture to make it match the solar time

		self.Psi = 0.0
		self.PlanetWidgets = None

		# When a "validate date" is set, a sidereal rotation 
		# correction is required to compensate for the earth
		# rotation around the sun between the old and new dates 		

		self.SiderealCorrectionAngle = 0.0  

		# texture alignment correction coefficient. This is to take 
		# into account the way vpython applies texture on a sphere 

		self.Alpha = deg2rad(80) # 2*math.pi/5 #pi/12
	
		makePlanet.__init__(self, system, EARTH_NAME, ccolor, type, sizeCorrectionType, defaultSizeCorrection)

		# Create widgets. This must be done after initializing earth. This will correctly
		# position the widgets with the earth current appearence
		
		self.PlanetWidgets = makePlanetWidgets(self)	

	# .--------------------------------------------.
	# | Called by the superclass __init__ methods. |
	# `--------------------------------------------'	

	# makeEarth::make_PCI_referential (overrides the makePlanet method)
	# This is the referential that is fixed to the stars

	def make_PCI_referential(self, tiltAngle): 
		#print "makeEarth: build PCI ref for", self.Name
		#	P: Polaris direction
		#	y: 
		#	u"\u2648": Point of Aries character
		self.PCI = make3DaxisReferential({
			'body': 		self,
			'radius': 		0,
			'tiltangle': 	-tiltAngle,
			'show':			False,
			'color': 		Color.white,
			'ratio': 		[1,1,1],
			'legend': 		[u"\u2648", "y", "P"]
		})  
		self.PCI.setAxisTilt(0)
		self.PCI.display(False)		

	# makeEarth::make_PCPF_referential (overrides the makePlanet method)
	# This is the referential that rotates with the earth surface

	def make_PCPF_referential(self, tiltAngle): #, size, position):
		#print "makeEarth: build PCPF ref for", self.Name
		#	P: Polaris direction
		#	y: 
		#	A: Antimeridian
		self.PCPF = make3DaxisReferential({
			'body': 			self,
			'radius': 			0,
			'tiltangle': 		-tiltAngle,
			'show':				True,
			'color': 			Color.cyan,
			'ratio': 			[-1,-1,1],
			'initial_rotation': pi/2,
			'legend': 			["A", "y", "P"]
		})

		# set planet origin as the PCPF referential (rotates with the planet)
		self.Origin 				= self.PCPF.referential #frame()
		self.Origin.visible			= True

		# Note: the referential tilt will be initiated after loading the body texture
		self.PCPF.display(False)

	# This overrides the default initRotation method provided in the makeBody superclass. 
	# This is where we initially position the earth texture

	def toggleSize(self, realisticSize):
		makePlanet.toggleSize(self, realisticSize)
		self.PlanetWidgets.OVRL.visible = False if self.sizeType == SCALE_NORMALIZED else True

	def initRotation(self):

		# we need to rotate around X axis by pi/2 to properly align the planet's texture,
		# and also, we need to take into account planet tilt around X axis 
#		self.BodyShape.rotate(angle=(pi/2+self.TiltAngle), axis=self.XdirectionUnit, origin=(0,0,0))

		# here we use "-" tilt angle to make it point to the correct direction
		print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
		#self.BodyShape.rotate(angle=(pi/2 - self.TiltAngle), axis=self.PCPF.XdirectionUnit, origin=(0,0,0))

#		self.BodyShape.rotate(angle=pi/2, axis=self.PCPF.XdirectionUnit, origin=(0,0,0))

		#self.PCI.referential.rotate(angle=(self.TiltAngle), axis=self.PCI.XdirectionUnit, origin=(0,0,0))
		#self.PCPF.referential.rotate(angle=(self.TiltAngle), axis=self.PCPF.XdirectionUnit, origin=(0,0,0))

		# rotate texture by 90 degrees along x
		#self.BodyShape.rotate(angle=(pi/2), axis=self.PCPF.XdirectionUnit)

		# then further rotation will apply to Z axis
		
		##### self.RotAxis = self.PCPF.ZdirectionUnit

#		planet.initRotation(self)
		#self.BodyShape.rotate(angle=(pi/2), axis=self.PCPF.XdirectionUnit, origin=(0,0,0))

		# induce initial tilt
		#self.PCPF.referential.rotate(angle=(-self.TiltAngle), axis=self.PCPF.XdirectionUnit, origin=(0,0,0))

		# then further rotation will apply to Z axis
		#self.RotAxis = self.PCPF.RotAxis #self.PCPF.ZdirectionUnit
		### self.RotAxis = self.PCPF.referential.frame_to_world(self.PCPF.ZdirectionUnit)
		#print self.RotAxis , "for", self.Name

		# adjust earth texture based on solar time
		################################
		self.setTextureFromSolarTime(None)
		################################
		return

	def setTextureFromSolarTime(self, localDatetime):
		# Called when a full update is required for the texture position, 
		# mainly due to a change in date, but also in time (ie when loading a CA body)

		# This will position the Earth texture to match the solar time
		# to better understand what is being calculated in this method, 
		# see the document "data/texture-positioning.png"

		if localDatetime == None:
			localDatetime = self.locationInfo.getLocalDateTime() #localdatetime

		# calculate initial angle (theta) between sun-earth 
		# axis and solar referential x axis tan(theta) = Y/X

		Theta = math.atan2(self.Position[1], self.Position[0])
		#print "setTextureFromSolarTime: Initial angle between earth and Ecliptic referential Y is ", Theta, " rd (", Theta * (180/math.pi), "degrees)"

		# calculate angle between location and the antiMeridian
		Beta =  deg2rad(self.locationInfo.Time2degree(self.locationInfo.TimeToWESTantiMeridian))
		Omega = Beta - self.Alpha

		# calculate rotation necessary to position texture properly for this local time
		Psi = Theta + deg2rad(self.locationInfo.computeLocalSolarTime(localDatetime)) - Omega

		if False:
			print "adjust "+self.Name+": Alpha .............  ", self.Alpha
			print "adjust "+self.Name+": Theta .............  ", Theta
			print "adjust "+self.Name+": Beta ..............  ", Beta
			print "adjust "+self.Name+": Omega .............  ", Omega
			print "adjust "+self.Name+": Psi ...............  ", Psi

		if self.SiderealCorrectionAngle != 0.0:
			# there has been a previous manual reset of the UTC date which has resulted in a sidereal 
			# correction. We need to undo it prior to reposition the texture for the new date

			self.Origin.rotate(angle=(-self.SiderealCorrectionAngle), axis=self.RotAxis, origin=(0,0,0))
			self.SiderealCorrectionAngle = 0.0

			# alternate method would be to reapply the earth texture to start from scratch
			# including resetting self.Psi = 0.0

		# Reverse the previous texture initial angle 
		# ...and apply the new one
		self.Origin.rotate(angle=(Psi-self.Psi), axis=self.RotAxis, origin=(0,0,0))
		self.Psi = Psi

		# also reflect the same reset amount with the widgets, if they already exist
		#if self.PlanetWidgets != None:
		#	self.PlanetWidgets.resetWidgetsRefFromSolarTime()


	# makeEarth::animate (overrides makeBody::animate")
	def animate(self, timeIncrement):
		# run default planet animation as defined in makeBody class
		velocity, dte, dts = makePlanet.animate(self, timeIncrement)

		# and animate widgets as well
		if self.PlanetWidgets is not None:
			self.PlanetWidgets.animate() #timeIncrement)

		return velocity, dte, dts

	def resetTexture(self): # TO REVIEW!!!!
		self.BodyShape = None
		self.Origin.visible = False
		New_Origin = frame(pos=self.Origin.pos)
		del self.Origin
		del self.BodyShape
		self.Origin = New_Origin
		self.BodyShape = sphere(frame=self.Origin, pos=(0,0,0), np=64, radius=self.getBodyRadius(), make_trail=false)
		self.BodyShape.material = materials.texture(data=self.Texture, mapping="spherical", interpolate=False)
		self.SiderealCorrectionAngle = 0.0  
		self.Psi = 0.0

	def updateAxis_XX(self):
		self.PCI.updateAxis() #self) ##################
		self.PCPF.updateAxis() #self) ##################
####		self.ECSS.updateAxis(self) ##################


	def setTextureFromSolarTime_v2(self, localDatetime):
		# Called when a full update is required for the texture position, 
		# mainly due to a change in date, but also in time (ie when loading a CA body)

		# This will position the Earth texture to match the solar time
		# to better understand what is being calculated in this method, 
		# see the document "data/texture-positioning.png"

		if localDatetime is None:
			localDatetime = self.locationInfo.localdatetime
		else:
			# reset texture
			self.resetTexture()


		# calculate initial angle (theta) between sun-earth 
		# axis and solar referential x axis tan(theta) = Y/X

		Theta = math.atan2(self.Position[1], self.Position[0])
		#print "setTextureFromSolarTime: Initial angle between earth and Ecliptic referential Y is ", Theta, " rd (", Theta * (180/math.pi), "degrees)"

		# calculate angle between location and the antiMeridian
		Beta =  deg2rad(self.locationInfo.Time2degree(self.locationInfo.TimeToWESTantiMeridian))
		Omega = Beta - self.Alpha

		# calculate rotation necessary to position texture properly for this local time
		Psi = Theta + deg2rad(self.locationInfo.computeLocalSolarTime(localDatetime)) - Omega

		if False:
			print "adjust "+self.Name+": Alpha .............  ", self.Alpha
			print "adjust "+self.Name+": Theta .............  ", Theta
			print "adjust "+self.Name+": Beta ..............  ", Beta
			print "adjust "+self.Name+": Omega .............  ", Omega
			print "adjust "+self.Name+": Psi ...............  ", Psi

		"""
		if self.SiderealCorrectionAngle != 0.0:
			# there has been a previous manual reset of the UTC date which has resulted in a sidereal 
			# correction. We need to undo it prior to reposition the texture for the new date
			self.BodyShape.rotate(angle=(-self.SiderealCorrectionAngle), axis=self.RotAxis, origin=(0,0,0))
			self.SiderealCorrectionAngle = 0.0

			# alternate method would be to reapply the earth texture to start from scratch
			# including resetting self.Psi = 0.0
		"""

		# Reverse the previous texture initial angle 
		#self.BodyShape.rotate(angle=(-self.Psi), axis=self.RotAxis, origin=(0,0,0))
		# ...and apply the new one
######		self.BodyShape.rotate(angle=(Psi-self.Psi), axis=self.RotAxis, origin=(0,0,0))
		self.BodyShape.rotate(angle=(Psi), axis=self.RotAxis, origin=(0,0,0))
		self.Psi = Psi

		# also reflect the same reset amount with the widgets, if they already exist
		if self.PlanetWidgets is not None:
			self.PlanetWidgets.fullReset()
			#self.PlanetWidgets.resetWidgetsRefFromSolarTime()


	# Called when only a sidereal angle correction is needed, this happens 
	# when dates change, but the time remains (ie when updating UTC date wheels)

	def	updateSiderealAngleFromNewDate(self, fl_diff_in_days):
		print "Calculating Earth texture reset"
		if self.SiderealCorrectionAngle != 0.0:
			# there has been a previous manual reset of the UTC date -or- a reset due to a close 
			# approach body's date-of-approach which has resulted in a sidereal correction. 
			# We need to undo it prior to reposition the texture for the new date

			print "Removing previous sidereal angle correction of", rad2deg(self.SiderealCorrectionAngle), "degres"
			self.Origin.rotate(angle=(-self.SiderealCorrectionAngle), axis=self.RotAxis, origin=(0,0,0))

		# reset the new sidereal correction angle

		self.SiderealCorrectionAngle = (2 * pi / self.NumberOfSiderealDaysPerYear)* fl_diff_in_days
		print "Injecting sidereal angle correction of", rad2deg(self.SiderealCorrectionAngle), "degres"
		self.Origin.rotate(angle=(self.SiderealCorrectionAngle), axis=self.RotAxis, origin=(0,0,0))

		# also reflect the same reset amount with the widgets

		######### self.PlanetWidgets.resetWidgetsReferencesFromNewDate() #fl_diff_in_days)


	# method called every few sec to allow for an update of the time label. BUT, the position is not updated
	# until we call this method self.STILL_ROTATION_INTERVAL/timeinsec times.

	def updateStillPosition(self, orbitalBoxInstance, timeinsec):

		return # disabled for the moment as we are debugging the UTC/local time issue

		if self.wasAnimated == false:
			# here insert call to update clock
			orbitalBoxInstance.deltaTtick(timeinsec)
			orbitalBoxInstance.refreshDate()

			self.rotationInterval -= timeinsec
			if self.rotationInterval <= 0:
				self.locationInfo.setSolarTime()
				self.incrementRotation()
				self.rotationInterval = self.STILL_ROTATION_INTERVAL

	def incrementRotation(self):
		# recalculate the angle of the texture on sphere based on updated time 
		#newLocalInitialAngle = deg2rad(self.locationInfo.solarT) \
		#					   - deg2rad(self.locationInfo.Time2degree(self.locationInfo.TimeToEASTantiMeridian)) \
		#					   - self.Theta 

		newLocalInitialAngle = deg2rad(self.locationInfo.solarT) \
							   + deg2rad(self.locationInfo.Time2degree(self.locationInfo.TimeToEASTantiMeridian)) \
					 		   + self.Theta 

		# rotate for the difference between updated angle and its formal value
#		self.BodyShape.rotate(angle=(newLocalInitialAngle - self.Gamma), axis=self.RotAxis, origin=(0,0,0))
		self.Origin.rotate(angle=(newLocalInitialAngle - self.Gamma), axis=self.RotAxis, origin=(0,0,0))
		print "rotating by ", newLocalInitialAngle - self.Gamma, " degree"

		# update angle with its updated value
		self.Gamma = newLocalInitialAngle

	# makeEarth::computeOrbitalEltFromPlanetPositionApproximation (overrides makeBody's) 
	def computeOrbitalEltFromPlanetPositionApproximation(self, elts, timeincrement):
		Adjustment = 0 #0.35

		# get number of days since J2000 epoch and obtain the fraction of century
		# (the rate adjustment is given as a rate per century)
		days = daysSinceJ2000UTC(self.locationInfo) + timeincrement
		
        # These formulas use 'days' based on days since 1/Jan/2000 12:00 UTC ("J2000.0"), 
        # instead of 0/Jan/2000 0:00 UTC ("day value"). Correct by subtracting 1.5 days...

		T = (days - Adjustment)/EARTH_CENTURY # T is in Julian centuries since J2000.0

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
		self.Mean_anomaly = toRange(L - self.Longitude_of_perihelion) #W)

		# Obtain ecc. Anomaly E (in degrees) from M using an approx method of resolution:
		success, self.E, dE, it = solveKepler(self.Mean_anomaly, self.e, 12000)
		if success == False:
			print ("Could not converge for "+self.Name+", E = "+str(self.E)+", last precision = "+str(dE))

##########################################################################################
class makeEarthTest(makePlanet):

	
	def __init__(self, system, ccolor, type, sizeCorrectionType, defaultSizeCorrection):
	
		makePlanet.__init__(self, system, EARTH_NAME_2, ccolor, type, sizeCorrectionType, defaultSizeCorrection)



	def initRotation(self):

		# we need to rotate around X axis by pi/2 to properly align the planet's texture,
		# and also, we need to take into account planet tilt around X axis 
#		self.BodyShape.rotate(angle=(pi/2+self.TiltAngle), axis=self.XdirectionUnit, origin=(0,0,0))

		# here we use "-" tilt angle to make it point to the correct direction
		print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
		#self.BodyShape.rotate(angle=(pi/2 - self.TiltAngle), axis=self.PCPF.XdirectionUnit, origin=(0,0,0))

#		self.BodyShape.rotate(angle=pi/2, axis=self.PCPF.XdirectionUnit, origin=(0,0,0))

		#self.PCI.referential.rotate(angle=(self.TiltAngle), axis=self.PCI.XdirectionUnit, origin=(0,0,0))
		#self.PCPF.referential.rotate(angle=(self.TiltAngle), axis=self.PCPF.XdirectionUnit, origin=(0,0,0))

		# rotate texture by 90 degrees along x
		#self.BodyShape.rotate(angle=(pi/2), axis=self.PCPF.XdirectionUnit)

		# then further rotation will apply to Z axis
		
		##### self.RotAxis = self.PCPF.ZdirectionUnit

#		planet.initRotation(self)
		#self.BodyShape.rotate(angle=(pi/2), axis=self.PCPF.XdirectionUnit, origin=(0,0,0))

		# induce initial tilt
		#self.PCPF.referential.rotate(angle=(-self.TiltAngle), axis=self.PCPF.XdirectionUnit, origin=(0,0,0))

		# then further rotation will apply to Z axis
		#self.RotAxis = self.PCPF.RotAxis #self.PCPF.ZdirectionUnit
		### self.RotAxis = self.PCPF.referential.frame_to_world(self.PCPF.ZdirectionUnit)
		#print self.RotAxis , "for", self.Name

		# adjust earth texture based on solar time
		################################
		################################
		return



	# makeEarth::computeOrbitalEltFromPlanetPositionApproximation (overrides makeBody's) 
	def computeOrbitalEltFromPlanetPositionApproximation(self, elements, timeincrement):

		ns = NasaSpice(10)
		id = 399 # earth

		elts = ns.getPlanetElements(id, datetime.datetime.today().strftime('%Y %b %d, %H:%M:%S'))


		self.a = getSemiMajor(elts[0], elts[1]) * 1000 * AU # perihelion, eccentricity

		self.e = elts[1]
		self.Inclination = elts[2]

		self.Longitude_of_perihelion = elts[4]
		self.Longitude_of_ascendingnode = elts[3]

		self.Argument_of_perihelion = self.Longitude_of_perihelion - self.Longitude_of_ascendingnode

		self.Mean_anomaly = elts[5]

		success, self.E, dE, it = solveKepler(self.Mean_anomaly, self.e, 12000)
		if success == False:
			print ("Could not converge for "+self.Name+", E = "+str(self.E)+", last precision = "+str(dE))



		if False:

			Adjustment = 0 #0.35

			# get number of days since J2000 epoch and obtain the fraction of century
			# (the rate adjustment is given as a rate per century)
			days = daysSinceJ2000UTC(self.locationInfo) + timeincrement
			
			# These formulas use 'days' based on days since 1/Jan/2000 12:00 UTC ("J2000.0"), 
			# instead of 0/Jan/2000 0:00 UTC ("day value"). Correct by subtracting 1.5 days...

			T = (days - Adjustment)/EARTH_CENTURY # T is in Julian centuries since J2000.0

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

##########################################################################################



# CLASS SATELLITE -------------------------------------------------------------
class makeSatellite(makeBody):
	def __init__(self, system, key, color, planetBody):
		makeBody.__init__(self, system, key, color, SATELLITE, SATELLITE, SATELLITE_SZ_CORRECTION, planetBody)
		self.isMoon = True

	def getRealisticSizeCorrectionXX(self):
		#SATELLITE_SZ_CORRECTION = 1/(DIST_FACTOR * 5)
		return 1/(DIST_FACTOR * 5)

	def setCartesianCoordinatesXX(self): # added tis to avoid correcting for vernal equinox rotation when dealing with moons
		self.Position[0] = self.R * DIST_FACTOR * ( cos(self.N) * cos(self.Nu+self.w) - sin(self.N) * sin(self.Nu+self.w) * cos(self.i) )
		self.Position[1] = self.R * DIST_FACTOR * ( sin(self.N) * cos(self.Nu+self.w) + cos(self.N) * sin(self.Nu+self.w) * cos(self.i) )
		self.Position[2] = self.R * DIST_FACTOR * ( sin(self.Nu+self.w) * sin(self.i) )

		#self.Position = self.Rotation_VernalEquinox * self.Position

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		if self.SolarSystem.isFeatured(self.CentralBody.BodyType):
			if self.sizeType == SCALE_OVERSIZED:
				self.Labels[0].visible = False
			else:
				self.Labels[0].visible = True

		self.BodyShape.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]

	def draw(self):
		#print "drawing "+self.Name
		self.Trail.visible = False
		rad_E = deg2rad(self.E)
		increment = self.getIncrement()

		for E in np.arange(increment, 2*pi+increment, increment):
			self.setPolarCoordinates(E+rad_E)
			# from R and Nu, calculate 3D coordinates and update current position
			self.drawSegment(trace = False) #E*180/pi, False)
			
			#### rate(5000) # ?!

		self.hasRenderedOrbit = True

# CLASS HYBERBOLIC ------------------------------------------------------------
class hyperbolic(makeBody):
	def __init__(self, system, key, color, planetBody):
		makeBody.__init__(self, system, key, color, HYPERBOLIC, HYPERBOLIC, HYPERBOLIC_SZ_CORRECTION, planetBody)
		self.isMoon = false

	def setAxisVisibility(self, setTo):
		pass

	def getRealisticSizeCorrectionXX(self):
		#SATELLITE_SZ_CORRECTION = 1/(DIST_FACTOR * 5)
		return 1/(DIST_FACTOR * 5)

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		if self.SolarSystem.isFeatured(self.CentralBody.BodyType):
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
			self.drawSegment(trace = False) #E*180/pi, False)
			
			### rate(5000) #?!

		self.hasRenderedOrbit = True


# CLASS GENERICSPACECRAFT -----------------------------------------------------
class makeGenericSpacecraft(makeBody):
	def __init__(self, system, key, color):
		#print "makeGenericSpacecraft: CALLED FOR KEY=", key
		makeBody.__init__(self, system, key, color, SPACECRAFT, SPACECRAFT, SMALLBODY_SZ_CORRECTION, system.Sun)
		self.BARYCENTER = 0.0
		self.AFT_TANK_RADIUS = 0.0
		self.AFT_TANK_CENTER_XCOOR = 0.0
		self.FWD_TANK_RADIUS = 0.0
		self.FWD_TANK_CENTER_XCOOR = 0.0
		self.ENGINE_HEIGHT = 0.0
		self.ENGINE_TOP_XCOOR = 0.0
		self.COPV_RADIUS = 0.0
		"""
		print "SPACECRAFT is", key
		print "Spacecraft:Init: label=", self.Labels[0].pos, "origin=", self.Origin.pos
		print "*** FINISHED init makeGenericSpacecraft ***"
		print ""
		"""
	def setAxisVisibility(self, setTo):
		pass

	# makeGenericSpacecraft::animate
	def animate(self, timeIncrement):
		#makeBody.animate(self, timeIncrement)
		if self.hasRenderedOrbit == False:
			self.draw()

		self.wasAnimated = true

		# update position
		self.setOrbitalElements(self.ObjectIndex, timeIncrement)
		self.setPolarCoordinates(deg2rad(self.E))

		# initial acceleration
		#self.Acceleration = vector(0,0,0)

		# calculate current body position on its orbit knowing
		# its current distance from Sun (R) and True anomaly (Nu)
		# that were set in setPolarCoordinates

		self.N = deg2rad(self.Longitude_of_ascendingnode)
		self.w = deg2rad(self.Argument_of_perihelion)
		self.i = deg2rad(self.Inclination)

		# convert polar to Cartesian in Sun referential
		self.Position = self.setCartesianCoordinates()

		# update foci position
		self.Foci = self.CentralBody.Position
		#print "ANIMATING-1 ", self.Name, "Origin=",self.Origin.pos, "Foci =",self.Foci

		self.Origin.pos = vector(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2])
		self.Labels[0].pos = self.Origin.pos
		
		#print "ANIMATING-2 ", self.Name, "Origin=",self.Origin.pos, "Foci =",self.Foci
#		self.Labels[0].pos = vector(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2])
		self.setRotation()
		#print "ANIMATING-3 ", self.Name, "Origin=",self.Origin.pos, "Foci =",self.Foci

		return self.getCurrentVelocity(), self.getCurrentDistanceFromEarth(), self.getCurrentDistanceFromSun()


	def setAspect(self, key):
		if self.SolarSystem.objects_data[key]["material"] != 0:
			data = materials.loadTGA("./img/"+ self.Tga)
			self.BodyShape.objects[0].material = materials.texture(data=data, mapping="cylinder", interpolate=False)


	def makeShape(self):
#		self.length = self.lengthFactor * 2 * self.radiusToShow/self.SizeCorrection[self.sizeType]
		self.length = self.lengthFactor * 2 * self.getBodyRadius()
		self.radius = 20 
		self.compounded = True

		# create compound object
		self.BodyShape = self.Origin

		# create fuselage
		self.BARYCENTER_XCOOR = -self.length/2
		cylinder(frame=self.Origin, pos=(self.BARYCENTER_XCOOR,0,0), radius=self.radius, length=self.length)

		# create aft tank
		self.AFT_TANK_RADIUS = self.radius
		self.AFT_TANK_CENTER_XCOOR = self.BARYCENTER_XCOOR + self.length/9
		sphere(frame=self.Origin, pos=(self.AFT_TANK_CENTER_XCOOR, 0, 0), radius=self.AFT_TANK_RADIUS, color=Color.white, np=64)		

		# create forward Platform
		self.FWD_TANK_RADIUS = self.radius
		self.FWD_TANK_CENTER_XCOOR = self.BARYCENTER_XCOOR + self.length - self.radius/1.5
		sphere(frame=self.Origin, pos=(self.FWD_TANK_CENTER_XCOOR, 0, 0), radius=self.FWD_TANK_RADIUS, color=Color.white)		

		# create engine
		self.makeEngine()
		"""
		self.ENGINE_HEIGHT = self.length/13
		self.ENGINE_TOP_XCOOR = self.AFT_TANK_CENTER_XCOOR - self.AFT_TANK_RADIUS - self.ENGINE_HEIGHT/2 - self.length/30
		cylinder(frame=self.BodyShape, pos=(self.ENGINE_TOP_XCOOR,0,0), radius=self.AFT_TANK_RADIUS/5, length=self.length/13, color=Color.darkgrey)

		# create COPV
		self.COPV_RADIUS = self.length/17
		sphere(frame=self.BodyShape, pos=(self.ENGINE_TOP_XCOOR + self.length/31, self.length/9, 0), radius=self.COPV_RADIUS, color=Color.grey)		
	
		nozzle = self.makeNozzle()
		nozzle.frame = self.BodyShape
		"""
		self.Origin.pos = self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]
		#print "GenericSpacecraft: MakeShape: self.Origin.pos=", self.Origin.pos

	def makeEngine(self):
		# create engine
		print "engine=", self.engine
		if self.engine <= 1:
			self.ENGINE_HEIGHT = self.length/13
			self.ENGINE_YOFFSET = 0
			self.ENGINE_RADIUS = self.AFT_TANK_RADIUS/5
			self.NOZZLE_LENGTH = self.length/4
			self.NOZZLE_THROAT = self.radius/7
			self.ENGINE_TOP_XCOOR = self.AFT_TANK_CENTER_XCOOR - self.AFT_TANK_RADIUS - self.ENGINE_HEIGHT/2 - self.length/30
		else:
			self.engine = 2
			self.ENGINE_HEIGHT = self.length/16
			self.ENGINE_YOFFSET = self.AFT_TANK_RADIUS / (self.engine+1)
			self.ENGINE_RADIUS = self.AFT_TANK_RADIUS/7
			self.NOZZLE_LENGTH = self.length/6
			self.NOZZLE_THROAT = self.radius * 0.01
			self.ENGINE_TOP_XCOOR = self.AFT_TANK_CENTER_XCOOR - self.AFT_TANK_RADIUS - self.ENGINE_HEIGHT/2 - self.length/30
			cylinder(frame=self.Origin, axis=(0,1,0), pos=(self.ENGINE_TOP_XCOOR + (self.ENGINE_HEIGHT*0.8), -self.length/12, 0), radius=self.ENGINE_RADIUS, length=self.length/6, color=Color.darkgrey)

		k = -1
		for i in range(self.engine):
			cylinder(frame=self.Origin, pos=(self.ENGINE_TOP_XCOOR, self.ENGINE_YOFFSET * k, 0), radius=self.ENGINE_RADIUS, length=self.ENGINE_HEIGHT, color=Color.darkgrey)
			nozzle = self.makeNozzle(self.ENGINE_YOFFSET * k)
			nozzle.frame = self.Origin
			k = -k
		k = -1
		for i in range(self.COPV):
			# create COPV
			self.COPV_RADIUS = self.length/18 - i*(self.length/100)
			sphere(frame=self.Origin, pos=(self.ENGINE_TOP_XCOOR + self.length/31, 0, self.length/11 * k), radius=self.COPV_RADIUS, color=Color.grey)		
			k = -k

	def makeEngineSAVE(self):
		# create engine
		if self.engine <= 1:
			self.ENGINE_HEIGHT = self.length/13
		else:
			self.engine = 2
			self.ENGINE_HEIGHT = self.length/16

		self.ENGINE_TOP_XCOOR = self.AFT_TANK_CENTER_XCOOR - self.AFT_TANK_RADIUS - self.ENGINE_HEIGHT/2 - self.length/30
		cylinder(frame=self.Origin, pos=(self.ENGINE_TOP_XCOOR,0,0), radius=self.AFT_TANK_RADIUS/5, length=self.length/13, color=Color.darkgrey)

		# create COPV
		self.COPV_RADIUS = self.length/17
		sphere(frame=self.Origin, pos=(self.ENGINE_TOP_XCOOR + self.length/31, self.length/9, 0), radius=self.COPV_RADIUS, color=Color.grey)		
	
		nozzle = self.makeNozzle()
		nozzle.frame = self.Origin

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
		circle = paths.arc(radius=self.ENGINE_THROAT, angle2=2*pi, up=(-1,0,0), pos=(-self.length/6, 0, 0))
		return extrusion(pos=circle,
				shape=section,
				color=Color.yellow)

	def makeNozzle(self, yoffset):
		# to create a nozzle, we need to start from a polygon representing the cross section of
		# the nozzle, and then create a cone by rotating this xsection around a circle

		# create a section of cone of 60, length d
		A1 = pi/2.5
		A2 = pi/2.3
		# L1 and L2 are the percentage on nozzle length for each segment. L1 + L2 must equal 1
		L1 = 0.6
		L2 = 0.4
		d = self.NOZZLE_LENGTH #self.length/4
		thickness = self.length/250

		#THROAT_SECTION = self.radius/7
		section = Polygon([	(0, 0), (thickness, 0), 
							(thickness + (d*L1)*np.cos(A1), (d*L1)*np.sin(A1)), 
							(thickness + (d*L1)*np.cos(A1) + (d*L2)*np.cos(A2), (d*L1)*np.sin(A1) + (d*L2)*np.sin(A2)), 
							((d*L1)*np.cos(A1) + (d*L2)*np.cos(A2), (d*L1)*np.sin(A1) + (d*L2)*np.sin(A2)), 
							((d*L1)*np.cos(A1), (d*L1)*np.sin(A1))])
		
		# set up to x=-1 so that the axis will be going towards the -x axis of the frame. also position the origin
		# negatively to push the nozzle cone further out
		circle = paths.arc(radius=self.NOZZLE_THROAT, angle2=2*pi, up=(-1,0,0), pos=(self.BARYCENTER_XCOOR -self.length/6, yoffset, 0))
		return extrusion(pos=circle,
				shape=section,
				color=Color.grey)

	def initRotation(self):
		self.RotAngle = pi/400
		self.RotAxis = (5, 5, -5)
		
	def setRotation(self):
		# I used to set the rotation using the origin parameter, but the end result would send the
		# spacecraft off its trajectory. So I took it off. FYI, down bellow was the call
		# self.Origin.rotate(angle=self.RotAngle, axis=self.RotAxis, origin=(0,0,0)) #origin=(10*self.length, 10*self.length, 0)) #-sin(alpha), cos(alpha)))
		self.Origin.rotate(angle=self.RotAngle, axis=self.RotAxis) 

	#def make_PCI_referential(self): #, size, position):
	#	return

	#def setAxisVisibility(self, setTo):
	#	return


# CLASS STARMAN ---------------------------------------------------------------
class starman(makeBody):
	def __init__(self, system, key, color):
		print "starman: CALLED FOR KEY=", key
		makeBody.__init__(self, system, key, color, SPACECRAFT, SPACECRAFT, SMALLBODY_SZ_CORRECTION, system.Sun)

		print "*** FINISHED init starman ***"
		print ""

	def setAxisVisibility(self, setTo):
		pass

	def makeShape(self):
		#print "====================making FUSELAGE\n"
		makeGenericSpacecraft.makeShape(self)
		print "Starman: MakeShape-A: self.Origin.pos=", self.Origin.pos
		
		#print "--------------------------now making ROADSTER\n"

		# create tesla
		roadster = self.makeTesla()
		print "Starman: MakeShape-B: self.Origin.pos=", self.Origin.pos

		roadster.frame = self.Origin

		# place roadster on the top of stage-2
		roadster.pos = (self.FWD_TANK_CENTER_XCOOR+(self.FWD_TANK_RADIUS)*1.14, self.carlength/2, -self.carwidth/2)
		roadster.axis = (-0.3, 1, 0)

		print "Starman: MakeShape-C: self.Origin.pos=", self.Origin.pos

	def makeTesla(self):
		roadster = frame()
		# create a box with a slight angle using an extruded polygon...
		self.carlength = self.radius*1.5
		self.carheight = self.radius*1.5/5
		self.carwidth = self.radius*2/3

		straight = [(0,0,0),(0,0,self.carwidth)]
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

		# describe extrusion path for wheels:
		# Front wheels elements as (coordinates of center as (x, y), radius)
		FWelements = vector(4*self.carlength/5, 3*self.carheight/3.5, self.carheight/2.1)
		frontwheelWell = shapes.circle(
			pos=(FWelements[0], FWelements[1]), radius=FWelements[2])

		# Rear wheels elements as (coordinates of center as (x, y), radius)
		RWelements = vector(self.carlength/5, 3*self.carheight/3.5, self.carheight/2.2)
		rearwheelWell = shapes.circle(
			pos=(RWelements[0], RWelements[1]), radius=RWelements[2])

		# make car body from 2D polygones set
		body = extrusion(pos=straight, 
						shape=carbody2D-rearwheelWell-frontwheelWell,
						color=Color.red)


		body.frame = roadster
		self.makeWheels(body, FWelements, RWelements)
		self.makeHeadlights(body)
		return roadster
		
	def makeHeadlights(self, body):
		HL_SCALE = 0.45
		HL1 = Polygon([(0, 0),(5*HL_SCALE, 0),(0, 3*HL_SCALE)])
		LeftHL = extrusion(	pos=[(0,-0.1,0),(0,0.4,0)], 
							shape=HL1,
							color=Color.white,
							material=materials.emissive)
		LeftHL.x = -self.carlength * 0.94
		LeftHL.z = LeftHL.z + self.carwidth * 0.1
		LeftHL.frame = body.frame

		HL2 = Polygon([(0, self.carwidth),(5*HL_SCALE, self.carwidth),(0, self.carwidth - 3*HL_SCALE)])
		RightHL = extrusion(pos=[(0,-0.1,0),(0,0.4,0)], 
							shape=HL2,
							color=Color.white,
							material=materials.emissive)
		RightHL.x = -self.carlength * 0.94
		RightHL.z = RightHL.z - self.carwidth * 0.1
		RightHL.frame = body.frame

		# make windshield
		WS = Polygon([(0, 0), (0.2,0), (self.carheight*0.6, -self.carheight*0.4), (self.carheight*0.6 - 0.2, -self.carheight*0.4)])
		windshield = extrusion(	pos=[(0, 0, 0),(0, 0, -self.carwidth * 0.90)], 
								shape=WS, material=materials.glass,
								color=Color.cyan)
		windshield.x = -self.carlength * 0.6
		windshield.z = windshield.z + self.carwidth * 0.95
		windshield.frame = body.frame

		# make starman
		sphere(frame=body.frame, radius=self.carheight * 0.2, 
								 pos=(-self.carlength * 0.41, -self.carheight/5, 2 * self.carwidth/7), 
								 color=Color.white)

	def makeWheels(self, body, front, rear):
		
		cylinder(frame=body.frame, axis=(0,0,1), pos=(-front[0], front[1], 0), 					radius=front[2]*0.90, length=self.carwidth * 0.15, color=Color.darkgrey)
		cylinder(frame=body.frame, axis=(0,0,1), pos=(-front[0], front[1], -0.1), 				radius=front[2]*0.60, length=self.carwidth * 0.10, color=Color.white)

		cylinder(frame=body.frame, axis=(0,0,1), pos=(-front[0], front[1], (self.carwidth * (1 - 0.15))),  radius=front[2]*0.90, length=self.carwidth * 0.15, Color=Color.darkgrey)
		cylinder(frame=body.frame, axis=(0,0,1), pos=(-front[0], front[1], self.carwidth*0.91),	radius=front[2]*0.60, length=self.carwidth * 0.10, color=Color.white)

		cylinder(frame=body.frame, axis=(0,0,1), pos=(-rear[0], rear[1], 0), 					radius=rear[2]*0.90, length=self.carwidth * 0.15, color=Color.darkgrey)
		cylinder(frame=body.frame, axis=(0,0,1), pos=(-rear[0], rear[1], -0.1), 				radius=rear[2]*0.60, length=self.carwidth * 0.10, color=Color.white)

		cylinder(frame=body.frame, axis=(0,0,1), pos=(-rear[0], rear[1], (self.carwidth * (1 - 0.15))), 	radius=rear[2]*0.90, length=self.carwidth * 0.15, color=Color.darkgrey)
		cylinder(frame=body.frame, axis=(0,0,1), pos=(-rear[0], rear[1], self.carwidth*0.91), 	radius=rear[2]*0.60, length=self.carwidth * 0.10, color=Color.white)


# CLASS SPACECRAFT ------------------------------------------------------------
class makeSpacecraft(makeGenericSpacecraft, starman):
	def __init__(self, system, key, color):
		if "profile" in system.objects_data[key]:
			print system.objects_data[key]["profile"]
			profile = json.loads(system.objects_data[key]["profile"])
			self.profile 		= profile["look"]
			self.engine  		= profile["engine"]
			self.COPV    		= profile["COPV"]
			self.lengthFactor 	= profile["length"]

			if self.profile == "generic":
				self.profile = "makeGenericSpacecraft" #"genericSpacecraft"

			# call appropriate class based on profile name
			globals()[self.profile].__init__(self, system, key, color)
		else:
			print "Could not find spacecraft profile for ", key
			raise 
	
	def makeShape(self):
		# call appropriate makeShape method based on required profile
		globals()[self.profile].makeShape(self)


# CLASS COMET -----------------------------------------------------------------
class makeComet(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, COMET, COMET, SMALLBODY_SZ_CORRECTION, system.Sun)

	def makeShape(self):
		self.Origin.pos = vector(self.Position[0],self.Position[1],self.Position[2])
		self.BodyShape = ellipsoid(	frame=self.Origin, pos=(0,0,0),
									length=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType], make_trail=false)
	def setAspect(self, key):
		# we don't need key for comets
		#self.BodyShape.material = materials.marble
		data = materials.loadTGA("./img/comet")
		self.BodyShape.material = materials.texture(data=data, mapping="spherical", interpolate=False)

	def setAxisVisibility(self, setTo):
		pass

	def initRotation(self):
#		self.RotAngle = pi/6
		self.RotAngle = pi/512
		self.RotAxis = (0,1,1)

	def setRotation(self):
		#self.updateAxis()
#		self.Origin.pos = vector(self.Position[0],self.Position[1],self.Position[2])
#		self.BodyShape.rotate(angle=self.RotAngle, axis=self.RotAxis, origin=(0,0,0)) #-sin(alpha), cos(alpha)))
		self.Origin.rotate(angle=self.RotAngle, axis=self.RotAxis) #, origin=(0,0,0)) #-sin(alpha), cos(alpha)))

	def make_PCI_referential(self): #, size, position):
		return

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		asteroidRandom = {SCALE_OVERSIZED: (randint(10, 20)/10, randint(10, 20)/10, randint(10, 20)/10), SCALE_NORMALIZED: (1,1,1)}

		self.BodyShape.length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyShape.height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyShape.width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

	def getIncrement(self):
		# for comets, due to their sometimes high eccentricity, an increment of 1 deg may not be small enough
		# to insure a smooth curve, hence we need to take smaller increments of 12.5 arcminutes or less in radians
		return pi/(180 * 4)

# CLASS ASTEROID --------------------------------------------------------------
class makeAsteroid(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, BIG_ASTEROID, BIG_ASTEROID, ASTEROID_SZ_CORRECTION, system.Sun)

	def setAxisVisibility(self, setTo):
		pass

	def initRotation(self):
		self.RotAngle = pi/512
		self.RotAxis = (1,1,1)

	def setRotation(self):
#		self.Origin.pos = vector(self.Position[0],self.Position[1],self.Position[2]) ### !!!!!
#		self.BodyShape.rotate(angle=self.RotAngle, axis=self.RotAxis, origin=(0,0,0)) #-sin(alpha), cos(alpha)))
		self.Origin.rotate(angle=self.RotAngle, axis=self.RotAxis) #, origin=(0,0,0)) #-sin(alpha), cos(alpha)))

	def make_PCI_referential(self): #, size, position):
		return

	def getRealisticSizeCorrectionXX(self):
		#ASTEROID_SZ_CORRECTION = 1e-2/(DIST_FACTOR*5)
		return 1e-2/(DIST_FACTOR*5)

# CLASS PHA -------------------------------------------------------------------
class makePha(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, PHA, PHA, SMALLBODY_SZ_CORRECTION, None) #system.Sun)

	def setAxisVisibility(self, setTo):
		pass

	def make_PCPF_referentialXX(self, tiltAngle): #, size, position):
		# This is the referential that rotates with the earth surface
		print "makPHA: build PCPF ref for", self.Name
		self.PCPF = make3DaxisReferential({
			'body': self,
			'radius': 0,
			'tiltangle': -tiltAngle,
			'show':	True,
			'color': Color.cyan,
			'ratio': [1,1,1],
			'legend': ["x", "y", "z-PCPF"]
		})# this referential moves and rotates with the planet  ####self.radiusToShow/self.SizeCorrection[self.sizeType], self.Position) #(self.Position[0],self.Position[1],self.Position[2]))
		# set planet origin as the PCPF referential (rotates with the planet)
		self.Origin 				= self.PCPF.referential #frame()
		self.Origin.visible			= True

		# Note: the referential tilt will be initiated after loading the body texture
		self.PCPF.display(True)

	def makeShape(self):
		asteroidRandom = [(1.5, 2, 1), (1.5, 2, 1)]
		self.Origin.pos = vector(self.Position[0],self.Position[1],self.Position[2])
		self.BodyShape = ellipsoid(	frame = self.Origin, pos=(0,0,0),
									length=(self.radiusToShow * asteroidRandom[self.sizeType][0])/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * asteroidRandom[self.sizeType][1])/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * asteroidRandom[self.sizeType][2])/self.SizeCorrection[self.sizeType], make_trail=false)
		if self.JPL_designation == '4179':
			print "makePHA:", self.Name,", position=:", self.Position, ", body position=",self.BodyShape.pos, "body Origin=", self.Origin.pos

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		#asteroidRandom = [(randint(10, 20)/10, randint(10, 20)/10, randint(10, 20)/10), (1,1,1)]
		asteroidRandom = {SCALE_OVERSIZED: (1.5, 2, 1), SCALE_NORMALIZED: (1.5/3.95, 2/3.95, 1/3.95)}

		self.BodyShape.length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyShape.height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyShape.width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

	def initRotation(self):
		self.RotAngle = pi/48
		self.RotAxis = (1,1,1)
		print "LABEL position:", self.Labels[0].pos

	def setRotation(self):
		#print "PHA rotates"
		#self.updateAxis()
		#self.Origin.pos = vector(self.Position[0],self.Position[1],self.Position[2])

#		self.BodyShape.rotate(angle=self.RotAngle, axis=self.RotAxis, origin=(0,0,0)) #-sin(alpha), cos(alpha)))
		self.Origin.rotate(angle=self.RotAngle, axis=self.RotAxis) #, origin=(0,0,0)) #-sin(alpha), cos(alpha)))

	#def make_PCI_referential(self): #, size, position):
	#	return

	#def setAxisVisibility(self, setTo):
	#	return

# CLASS SMALLASTEROID ---------------------------------------------------------
class makeSmallAsteroid(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, SMALL_ASTEROID, SMALL_ASTEROID, SMALLBODY_SZ_CORRECTION, system.Sun)

	def setAxisVisibility(self, setTo):
		pass

	def makeShape(self):
		self.Origin.pos = vector(self.Position[0],self.Position[1],self.Position[2])
		self.BodyShape = ellipsoid(	frame=self.Origin, pos=(0,0,0),
									length=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType], make_trail=false)

	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		asteroidRandom = {SCALE_OVERSIZED: (randint(10, 20)/10, randint(10, 20)/10, randint(10, 20)/10), SCALE_NORMALIZED: (1,1,1)}
		self.BodyShape.length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyShape.height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyShape.width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

	def initRotation(self):
#		self.RotAngle = pi/6
		self.RotAngle = pi/512
		#self.RotAxis = (1,1,1)

	def setRotation(self):
#		self.Origin.pos= vector(self.Position[0],self.Position[1],self.Position[2])
#		self.BodyShape.rotate(angle=self.RotAngle, axis=self.RotAxis, origin=(0,0,0)) #-sin(alpha), cos(alpha)))
		self.Origin.rotate(angle=self.RotAngle, axis=self.RotAxis) #, origin=(0,0,0)) #-sin(alpha), cos(alpha)))

	def make_PCI_referential(self): #, size, position):
		self.Origin = frame()
		self.Origin.visible	= True

	def setRotAxis(self):
		self.RotAxis = (1,1,1)

	def make_PCPF_referential(self): #, size, position):
		pass

	#def setAxisVisibility(self, setTo):
	#	return

# CLASS DWARFPLANET -----------------------------------------------------------
class makeDwarfPlanet(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, DWARFPLANET, DWARFPLANET, DWARFPLANET_SZ_CORRECTION, system.Sun)

	def setAxisVisibility(self, setTo):
		pass

	def makeShape(self):
		makeBody.makeShape(self)
		#print "DWARF ", self.Name

	def getRealisticSizeCorrectionXX(self):
		#DWARFPLANET_SZ_CORRECTION = 1e-2/(DIST_FACTOR*5)
		return 1e-2/(DIST_FACTOR*5)

# CLASS TRANSNEPTUNIAN --------------------------------------------------------
class makeTransNeptunian(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, TRANS_NEPT, TRANS_NEPT, SMALLBODY_SZ_CORRECTION, system.Sun)

	def setAxisVisibility(self, setTo):
		pass

	def makeShape(self):
		self.Origin.pos = vector(self.Position[0],self.Position[1],self.Position[2])
		self.BodyShape = ellipsoid(	frame=self.Origin, pos=(0,0,0),
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
#		self.RotAngle = pi/6
		self.RotAngle = pi/512
		self.RotAxis = (0,1,1)

	def setRotation(self):
#		self.Origin.pos = vector(self.Position[0],self.Position[1],self.Position[2])
#		self.BodyShape.rotate(angle=self.RotAngle, axis=self.RotAxis, origin=(0,0,0)) #-sin(alpha), cos(alpha)))
		self.Origin.rotate(angle=self.RotAngle, axis=self.RotAxis) #, origin=(0,0,0)) #-sin(alpha), cos(alpha)))

	#def make_PCI_referential(self): #, size, position):
	#	return

	#def setAxisVisibility(self, setTo):
	#	return

#
# various functions
#
def getSigmoid(distance, correction):
	print "peri=", distance,", correction=", correction
	if distance > 0:
		sigmoid = 1/(1+exp(-MAX_P_D/distance))
		return correction * sigmoid
	return correction

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
	return { 0: Color.white, 1: Color.red, 2: Color.orange, 3: Color.yellow, 4: Color.cyan, 5: Color.magenta, 6: Color.green}[randint(0,6)]

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
			idx = obj[key]["jpl_designation"].lower()
			#print "KEY IS ", idx
			SolarSystem.objects_data[idx] = {
#			self.objects_data[obj[key]] = {
				"profile": "{ \"look\":\""+obj[key]["profile"]["look"]+"\", \"engine\":"+str(obj[key]["profile"]["engine"])+", \"length\":"+str(obj[key]["profile"]["length"])+", \"COPV\":"+str(obj[key]["profile"]["COPV"])+"}" if "profile" in obj[key] else "",
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
			
			body = {SPACECRAFT: 	makeSpacecraft,
					COMET: 			makeComet,
					BIG_ASTEROID: 	makeAsteroid,
					PHA:			makePha,
					TRANS_NEPT:		makeTransNeptunian,
					SATELLITE:		makeSatellite,
					SMALL_ASTEROID:	makeSmallAsteroid,
					}[type](SolarSystem, idx, getColor())
#						}[type](SolarSystem, obj[key]["jpl_designation"], getColor())

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

"""
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
				self.objects_data[token[JPL_DESIGNATION]] = {
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
				body = {COMET: 			makeComet,
						BIG_ASTEROID: 	makeAsteroid,
						PHA:			makePha,
						TRANS_NEPT:		makeTransNeptunian,
						SATELLITE:		makeSatellite,
						SMALL_ASTEROID:	makeSmallAsteroid,
						}[type](SolarSystem, token[JPL_DESIGNATION], getColor())

				SolarSystem.addTo(body)
				#if body.Name == "Moon":
				#	print body.JPL_designation
				#	print "Satellite was added to solar system"
				maxentries -= 1
				if maxentries <= 0:
					break
	fo.close()
"""
"""
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
	# orthogonal vectors we choose the one that also to the (x,y) plane (with z=0) 
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
"""


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
#	return int(365.25*(utc.year+4716)) + int(30.6001*(utc.month+1)) + utc.day - 1524.5
	return int(EARTH_PERIOD*(utc.year+4716)) + int(30.6001*(utc.month+1)) + utc.day - 1524.5

def gregoriandate2JDE(year, month, day):
	if month <= 2:
		year = year-1
		month = month + 12
	A = int(year/100)
	B = 2 - A + int(A/4)
#	return int(365.25*(year+4716)) + int(30.6001*(month+1)) + day + B - 1524.5
	return int(EARTH_PERIOD*(year+4716)) + int(30.6001*(month+1)) + day + B - 1524.5

def JDEtoJulian(jdediff_indays):
	Y = jdediff_indays / EARTH_PERIOD #365.25
	years = int(Y)
	days = (Y - years) * EARTH_PERIOD #365.25
	return days

def makeJulianDateALTernate(utc, delta):
	# Fliegel / Van Flandern Formula - "delta" is in days (added minutes and seconds)
	JL = delta + 367*utc.year - (7*(utc.year + ((utc.month+9)/12)))/4 + (275*utc.month)/9 + utc.day + 1721013.5 + (((utc.second/60) + utc.minute)/60 +utc.hour)/24

	print "makeJulian------------", JL
	return JL

def makeJulianDate(utc, delta):
	# Fliegel / Van Flandern Formula - "delta" is a float to accept fractional days (added minutes and seconds)
	# JL = delta + 367*utc.year - (7*(utc.year + ((utc.month+9)//12)))//4 + (275*utc.month)//9 + utc.day - 730530 + (utc.hour/24.0) + \
	#		(utc.minute/1440.0) + (utc.second/86400.0)

	# Note that the // operator means "__floordiv__", where the result is rounded to the lower closest integer (it 1.689 -> 1)
	# For the leftOver though, we need the exact value in float

	JL = delta + 367*utc.year - 7*(utc.year + (utc.month+9)//12)//4 - 3*(((utc.year+(utc.month-9)//7)//100) + 1)//4 + 275*utc.month//9 + utc.day - 730515
	leftOver = (utc.hour/24.0) + (utc.minute/1440.0) + (utc.second/86400.0)

	#print "makeJulian------------", JL+leftOver
	return JL+leftOver

	#return delta + julian(utc.day, utc.month, utc.year)

def julian(d,m,y):
	temp1 = m - 14
	temp2 = d - 32075 + 1461 * (y + 4800 + int(temp1 / 12.0)) / 4
	temp3 = int(temp1 / 12.0) * 12
	temp4 = ((y + 4900 + int(temp1 / 12.0)) / 100)
	return temp2 + 367 * (m - 2 - temp3) / 12 - 3 * temp4 / 4

# will compute the number of days since J2000 UTC
def daysSinceJ2000UTC(locationInfo, delta = 0):
	#utc = datetime.datetime.utcnow()
	utc = locationInfo.getUTCDateTime()

	return makeJulianDate(utc, delta)

def daysSinceEpochJD(julianDate, locationInfo):
	if julianDate == 0:
		# when epoch is not known, epoch is set to zero
		return 0
	# otherwise determine number of days since epoch
	days = daysSinceJ2000UTC(locationInfo) # days from 2000
	return days - (julianDate - EPOCH_2000_JD)

def daysSinceEpochJDfromUnixTimeStamp(UnixTimeStamp, locationInfo):
	# Unix timestamp are the number of seconds since 01-01-1970 GMT.
	# first let's convert that number in a number of days, by a)
	# calculating the number of days since 1970 and b) add the number
	# of JULIAN DAYS corresponding to 01-01-1970
	ndays = (UnixTimeStamp / 86400.0) + EPOCH_1970_JD

	# second convert that number of days into the number of days since
	# 01-01-2000
	return daysSinceEpochJD(ndays, locationInfo)

#    now_timestamp = time.time()
#    offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
#    return utc_datetime + offset


def utc_to_local_fromTimestamp(utcTimeStamp, locationInfo):
	# given a UTC timestamp, figure out local datetime
	utc	= datetime.datetime.fromtimestamp(utcTimeStamp)
	utc = utc.replace(tzinfo=pytz.utc)
	# deduct local time ...
	return utc.astimezone(pytz.timezone(locationInfo.getTZ()))


# Convert date/time from UTC to location of interest date/time
def utc_to_local_fromDatetime(utc_datetime, locationInfo):
#	return utc_datetime + locationInfo.longitudeSign * datetime.timedelta(seconds=locationInfo.TimeToUtcInSec())
	return utc_datetime + datetime.timedelta(seconds=locationInfo.TimeToUtcInSec())
	#return utc_datetime - datetime.timedelta(seconds=locationInfo.TimeToUtcInSec())

	
# Convert date/time from UTC to local date/time
"""
def utc_to_localXX():
	UTC_datetime = datetime.datetime.utcnow()
	UTC_datetime_timestamp = datetime.datetime.timestamp(UTC_datetime) #float(UTC_datetime.strftime("%S"))
	local_datetime_converted = datetime.datetime.fromtimestamp(UTC_datetime_timestamp)
	print "local datetime from utc", local_datetime_converted
	return local_datetime_converted

def UTC_to_localXX(utc_naivedatetime):
	utc_time = pytz.utc #timezone(locationInfo.getTZ())
	utc_datetime = utc_time.localize(utc_naivedatetime, is_dst=None)
	local_datetime = utc_datetime.astimezone(pytz.timezone(locationInfo.getTZ()))
	print "UTC=", utc_naivedatetime, "local=", local_datetime
	return local_datetime, utc_datetime


def to_timestampXX(a_date):

    if a_date.tzinfo:
    	pass
    	
    	#print "TZINFO", a_date.tzinfo
        #epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.UTC)
        #diff = a_date.astimezone(pytz.UTC) - epoch
        
    else:
        epoch = datetime.datetime(1970, 1, 1)
        diff = a_date - epoch
    return int(diff.total_seconds())


def from_timestampXX(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, pytz.UTC)

"""
