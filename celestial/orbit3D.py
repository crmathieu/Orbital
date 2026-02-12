# -*- coding: utf-8 -*-
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
#from moon_cgpt import moon_orbital_elements
#from moon_kimi import moon_orbital_elements


#from moon_copilot import getMoonElements

import json

System_utc = None

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

		global System_utc 
		System_utc = self.todayUTCdatetime
		
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

		# orientation parameters
		self.Pole_vec = vector(0,0,0)
		self.W_angle = 0
		self.Omega_angle = 0

		self.J2000_Equatorial_obliquity = 23.43928

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
		self.J2000eclipticFrame = frame(pos=(0,0,0))
		self.J2000eclipticRef = self.createJ2000eclipticReferential(self.J2000eclipticFrame)
		self.RefOrigin = self.J2000eclipticRef.referential.pos
		self.J2000eclipticRef.setAxisTilt()

		######################################################
		#self.makeCelestialSphere()
		#self.makeConstellations()

		#print "initial CAMERA POSITION ************************* ", self.Scene.mouse.camera

		

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

	def createJ2000eclipticReferential(self, parent_frame):
		# we do not provide any orientation information,
		# as this initial referential determines the Vernal
		# equinox as X and the North ecliptic a Z. This
		# correspond to a vector (0,0,1) that is set by
		# default in make3DaxisReferential

		#print "building Solar System Referential"
		return make3DaxisReferential({
					'parent_frame': parent_frame,
					'body':			None,
					'parent_frame': None,
					'radius': 		5*AU*DIST_FACTOR,
					'tiltangle': 	0,
					'show':			True,
					'color': 		Color.white,
					'ratio': 		[1,1,0.2],
					'legend': 		[u"\u2648", u"\u2649", "Ecl.North"]
				})		
		#self.RefOrigin = 

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

	# makeSolarSystem::
	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x
		self.BodyGeometry.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]

	def setEarthLocations(self, db):
		self.setDashboard(db)
		self.camera.setEarthLocations()

	def getDashboard(self):
		return self.Dashboard

	def setDashboard(self, db):
		self.Dashboard = db

	def makeConstellations2(self):
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
			self.Constellations.rotate(angle=(pi/2), 		axis=self.J2000eclipticRef.XdirectionUnit, origin=(0,0,0))
			self.Constellations.rotate(angle=deg2rad(self.J2000_Equatorial_obliquity), axis=self.J2000eclipticRef.YdirectionUnit, origin=(0,0,0))
			self.Constellations.rotate(angle=(pi/2), 		axis=self.J2000eclipticRef.ZdirectionUnit, origin=(0,0,0))

		else:
			print ("Could not find "+file)
		#self.Scene.scale = self.Scene.scale / 1e10

	def makeCelestialSphere2(self): # Unused
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
			self.Universe.rotate(angle=(pi/2), 		axis=self.J2000eclipticRef.XdirectionUnit, origin=(0,0,0))
			self.Universe.rotate(angle=deg2rad(self.J2000_Equatorial_obliquity), axis=self.J2000eclipticRef.YdirectionUnit, origin=(0,0,0))
			self.Universe.rotate(angle=(pi/2), 		axis=self.J2000eclipticRef.ZdirectionUnit, origin=(0,0,0))

		else:
			print ("Could not find "+file)
		#self.Scene.scale = self.Scene.scale / 1e10


	# makeSolarSystem::
	def animate(self, deltaT):
		pass
		#self.animateBodyRotation()

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
		#print "SCENE CENTER: ", self.Scene.center

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
			self.bodies[self.JTrojansIndex].BodyGeometry.visible = False
			self.bodies[self.JTrojansIndex].Labels = []
			self.bodies[self.JTrojansIndex] = body

		body.draw()

	def getJTrojans(self):
		if self.JTrojansIndex >= 0:
			return self.bodies[self.JTrojansIndex]
		return None

	# makeSolarSystem
	def drawAllBodiesTrajectory(self):
		"""
		Will trace the orbit of all declared objects, regardless of whether 
		the orbit is visible or not
		"""
		for body in self.bodies:
			if body.BodyType in [OUTERPLANET, INNERPLANET, SATELLITE, MOON, DWARFPLANET, KUIPER_BELT, ASTEROID_BELT, INNER_OORT_CLOUD, ECLIPTIC_PLANE]:
				print "drawing", body.Name
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

	# makeSolarSystem::
	def refresh(self, animationInProgress = False):
		orbitTrace 		= True if self.ShowFeatures & ORBITS 	!= 0 else False
		labelVisible 	= True if self.ShowFeatures & LABELS 	!= 0 else False
		realisticSize 	= True if self.ShowFeatures & REALSIZE 	!= 0 else False

		#self.toggleSize(realisticSize)

		for body in self.bodies:

			if body.BodyType in [SUN, SPACECRAFT, OUTERPLANET, INNERPLANET, ASTEROID, COMET, \
								 SATELLITE, MOON, DWARFPLANET, PHA, BIG_ASTEROID, TRANS_NEPT]:

				#print "FOUND BODY="+body.Name
				body.toggleSize(realisticSize)
				if body.BodyType == SUN:
					continue

				body.RefOrigin.visible = True if self.ShowFeatures & body.BodyType != 0 else False ################################
#				body.toggleSize(realisticSize)

				if body.BodyType == OUTERPLANET:
					body.displayRings(body.RefOrigin.visible) ############# NEW

				if body.RefOrigin.visible == True:
					if body.Orbit is not None:
						body.Orbit.visible = orbitTrace


					if False and body.isMoon == True: #### temporary hack to force the moon to be seen
						# apply label on/off when moon in real size, otherwise do not show label
						value = labelVisible if body.sizeType == SCALE_NORMALIZED else False
					else:
						value = labelVisible

					for i in range(len(body.Labels)):
						body.Labels[i].visible = value
				else:
					pass #body.RefOrigin.visible = bodyVisible

			else: # belts / rings
				if body.BodyType != ECLIPTIC_PLANE:
					
					if body.BodyGeometry.visible == True and animationInProgress == True:
						body.BodyGeometry.visible = False
						for i in range(len(body.Labels)):
							body.Labels[i].visible = False
		
		if self.ShowFeatures & LIT_SCENE != 0:
			#print "LITE"
			self.Scene.ambient = Color.white
			self.sunLight.visible = False
			self.Sun.BodyGeometry.material = materials.texture(data=self.Sun.Texture, mapping="spherical", interpolate=False)
			self.Sun.BodyGeometry.opacity = 1.0
		else:
			#print "DARK", self.Sun
			self.Scene.ambient = Color.nightshade #Color.black
			self.sunLight.visible = True
			self.Sun.BodyGeometry.material = materials.emissive
#			self.Sun.BodyGeometry.material = materials.texture(data=self.Sun.Texture, mapping="spherical", interpolate=False)
			
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
								 SATELLITE, MOON, DWARFPLANET, PHA, BIG_ASTEROID, TRANS_NEPT]:

				#print "FOUND BODY="+body.Name
				body.toggleSize(realisticSize)
				if body.BodyType == SUN:
					continue

				body.RefOrigin.visible = True if self.ShowFeatures & body.BodyType != 0 else False ################################
#				body.toggleSize(realisticSize)
				if body.RefOrigin.visible == True:
					if body.Orbit is not None:
						body.Orbit.visible = orbitTrace
					if body.isMoon == True:
						# apply label on/off when moon in real size, otherwise do not show label
						value = labelVisible if body.sizeType == SCALE_NORMALIZED else  False
					else:
						value = labelVisible

					for i in range(len(body.Labels)):
						body.Labels[i].visible = value
				else:
					pass #body.RefOrigin.visible = bodyVisible

			else: # belts / rings
				if body.BodyType != ECLIPTIC_PLANE:
					
					if body.BodyGeometry.visible == True and animationInProgress == True:
						body.BodyGeometry.visible = False
						for i in range(len(body.Labels)):
							body.Labels[i].visible = False
		
		if self.ShowFeatures & LIT_SCENE != 0:
			#print "LITE"
			self.Scene.ambient = Color.white
			self.sunLight.visible = False
			self.Sun.BodyGeometry.material = materials.texture(data=self.Sun.Texture, mapping="spherical", interpolate=False)
			self.Sun.BodyGeometry.opacity = 1.0
		else:
			#print "DARK", self.Sun
			self.Scene.ambient = Color.nightshade #Color.black
			self.sunLight.visible = True
			self.Sun.BodyGeometry.material = materials.emissive
			
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
		self.J2000eclipticRef.display(setRefTo)
		if self.Sun.PCPF != None:
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
		self.RefOrigin = frame(frame=system.J2000eclipticFrame)
		self.Labels.append(label(pos=(250*AU*DIST_FACTOR, 250*AU*DIST_FACTOR, 0), text=self.Name, xoffset=20, yoffset=12, space=0, height=10, border=6, box=false, font='sans', visible = False))

	# makeEcliptic::
	def toggleSize(self, realisticSize):
		pass

	def rotate(self):
		pass 

	def drawXX(self):
		pass

	# makeEcliptic::
	def draw(self):
		#print ("Drawing ecliptic")
		side = 250*AU*DIST_FACTOR
		self.BodyGeometry = box(frame=self.RefOrigin, pos=vector(0, 0, 0), length=side, width=0.0001, height=side, material=materials.emissive, color=self.Color, opacity=0.1) #, axis=(0, 0, 1), opacity=0.8) #opacity=self.Opacity)
		self.RefOrigin.visible = False

	# makeEcliptic::
	def refresh(self):
		#print("Refresh Ecliptic")
		self.RefOrigin.visible = True if (self.SolarSystem.ShowFeatures & ECLIPTIC_PLANE) != 0 else False


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
		self.BodyGeometry = points(pos=(self.RadiusMinAU, 0, 0), size=size, color=(color[0]*0.5, color[1]*0.5, color[2]*0.5))

		self.BodyGeometry.visible = False
		if self.Thickness == 0:
			self.Thickness = (self.RadiusMinAU + self.RadiusMaxAU)/2 * math.tan(math.pi/6)
		#shape = "cube"

	def getGaussian(self, position):
		mu = (self.RadiusMinAU + self.RadiusMaxAU)* AU * DIST_FACTOR/2
		sigma = (self.RadiusMaxAU - self.RadiusMinAU)* AU * DIST_FACTOR/3
		return float((1/(sigma*sqrt(math.pi*2)))*exp(-(((position-mu)/sigma)**2)/2))

	# makeBelt::
	def draw(self):
		for i in np.arange(0, 2*math.pi, math.pi/(180*self.Density)):
			# generate random radius between Min and MAX
			RandomRadius = randint(round(self.RadiusMinAU * AU * DIST_FACTOR, 3) * 1000, round(self.RadiusMaxAU * AU * DIST_FACTOR, 3) * 1000) / 1000
			MAX = self.getGaussian(RandomRadius) * self.Thickness * AU * DIST_FACTOR * self.ThicknessFactor
			heightToEcliptic = {0: 0, 1:1, 2:-1}[randint(0,2)] * randint(0, int(round(MAX, 6)*1.e6))/1.e6
			self.BodyGeometry.append(pos=(RandomRadius * cos(i), RandomRadius * sin(i), heightToEcliptic))

		self.Labels.append(label(pos=(self.RadiusMaxAU * AU * DIST_FACTOR * cos(i), self.RadiusMaxAU * AU * DIST_FACTOR * sin(i), 0), text=self.Name, xoffset=20, yoffset=12, space=0, height=10, border=6, box=False, font='sans', visible = False))

	# makeBelt::
	def refresh(self):
		if self.SolarSystem.ShowFeatures & self.BodyType != 0:
			if self.BodyGeometry.visible == False:
				self.BodyGeometry.visible = True

			labelVisible = True if self.SolarSystem.ShowFeatures & LABELS != 0 else False

			for i in range(len(self.Labels)):
				self.Labels[i].visible = labelVisible

		else:
			if self.BodyGeometry.visible == true:
				self.BodyGeometry.visible = false
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

	# makeJtrojan::
	def draw(self):
		# determine where the body is
		#if self.PlanetName is not None:
		#	return

		# grab Jupiter's current True Anomaly and add the Long. of perihelion to capture
		# the current angle in the fixed referential
		Nu = deg2rad(toRange(rad2deg(self.Planet.Nu) + self.Planet.Longitude_of_periapsis))

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
			self.BodyGeometry.append(pos=(RandomTail * cos(L4+delta+i), RandomTail * sin(L4+delta+i), heightToEclipticTail))
			self.BodyGeometry.append(pos=(RandomTail * cos(L5-delta-i), RandomTail * sin(L5-delta-i), heightToEclipticTail))
			# calculate positions on 1/2 values and complete by symetry for the rest
			self.BodyGeometry.append(pos=(RandomRadius * cos(L4-delta+i), RandomRadius * sin(L4-delta+i), heightToEcliptic))
			self.BodyGeometry.append(pos=(RandomRadius * cos(L4+delta-i), RandomRadius * sin(L4+delta-i), heightToEcliptic))
			self.BodyGeometry.append(pos=(RandomRadius * cos(L5-delta+i), RandomRadius * sin(L5-delta+i), heightToEcliptic))
			self.BodyGeometry.append(pos=(RandomRadius * cos(L5+delta-i), RandomRadius * sin(L5+delta-i), heightToEcliptic))

		self.Labels.append(label(pos=(self.RadiusMaxAU * AU * DIST_FACTOR * cos(L4), self.RadiusMaxAU * AU * DIST_FACTOR * sin(L4), 0), text="L4 Trojans", xoffset=20, yoffset=12, space=0, height=10, border=6, box=false, font='sans', visible = False))
		self.Labels.append(label(pos=(self.RadiusMaxAU * AU * DIST_FACTOR * cos(L5), self.RadiusMaxAU * AU * DIST_FACTOR * sin(L5), 0), text="L5 Trojans", xoffset=20, yoffset=12, space=0, height=10, border=6, box=false, font='sans', visible = False))


# CLASS MAKEBODY --------------------------------------------------------------
class makeBody:

	"""
	Main class describing system bodies, from star to planets, asteroids, 
	comets, spacecrafts etc underlying category specific subclass derive 
	from the makeBody class  
	"""

	RING_BASE_THICKNESS = 2000
	STILL_ROTATION_INTERVAL = 50 #5 * 60 # (in seconds)
	def __init__(self, system, key, color, bodyType = INNERPLANET, sizeCorrectionType = INNERPLANET, RealisticCorrectionSize = SMALLBODY_SZ_CORRECTION, centralBody = None):  # change default values during instantiation

		self.Labels = []
		self.compounded = False
		
		
		self.CentralBody = centralBody
		"""
		if False:
			# if the central body is None, it is assumed that 
			# the central body is the solar sustem barycenter

			
			if centralBody == None:
				self.CentralBody = system
			else:
				self.CentralBody = centralBody
		"""

		self.isMoon = False
		self.RealisticCorrectionSize = RealisticCorrectionSize
		self.sizeCorrectionType = sizeCorrectionType

		self.Foci = vector(0,0,0)

		# orientation parameters (used for planets)
		self.Pole_vec = vector(0,0,0)
		self.W_angle = 0
		self.Omega_angle = 0
		
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
		self.BodyGeometry 			= None
		self.LocalEclipticRef 		= None

		self.Revolution 			= system.objects_data[key]["revolution_PR"]
		self.Periapsis 				= system.objects_data[key]["distance_to_periapsis"]		# body perhelion
		self.Distance 				= system.objects_data[key]["distance_to_periapsis"]		# body distance at perige from focus

		self.e 						= system.objects_data[key]["eccentricity_EC"]
		self.a 						= getSemiMajor(self.Periapsis, self.e)
		self.l  					= getSemiLatusRectum(self.a, self.e)

		self.Details				= False
		self.hasRenderedOrbit		= False
		self.Absolute_mag			= system.objects_data[key]["absolute_mag"]
		self.Orbit					= None
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
		self.Ring 					= False
		self.Rings 					= []
		self.nRings 				= 0
		self.RingThickness 			= self.RING_BASE_THICKNESS / self.SizeCorrection[self.sizeType]
		self.Ratio 					= [1,1,1]

		# J2 oblation factor - used to calculate the rate of regression of the ascending node
		if "J2" in system.objects_data[key]:
			self.J2 = system.objects_data[key]["J2"]
		else:
			self.J2 = 0.0

		if self.BodyRadius < DEFAULT_RADIUS:
			self.radiusToShow 		= DEFAULT_RADIUS
		else:
			self.radiusToShow 		= self.BodyRadius

		if "tga_name" in system.objects_data[key]:
			self.Tga 				= system.objects_data[key]["tga_name"]
		else:
			self.Tga 				= ""

		self.Moid = system.objects_data[key]["earth_moid"] if "earth_moid" in system.objects_data[key] else 0

		self.Eccentric_anomaly = 0

		# Calculate orbital elements
		self.setOrbitalElements(key)

		self.b = self.getSemiMinor(self.a, self.e)
		self.Aphelion = getAphelion(self.a, self.e)	# body aphelion

		# generate 2d coordinates in the initial orbital plane, with +X pointing
		# towards periapsis. Make sure to convert degree to radians before using
		# any sin or cos function

		self.R, self.Nu = self.setPolarCoordinates(deg2rad(self.Eccentric_anomaly))


		# calculate current position of body on its orbit knowing
		# its current distance from Sun (R) and angle (Nu) that
		# were set up by setPolarCoordinates

		self.N = deg2rad(self.Longitude_of_ascendingnode)
		self.w = deg2rad(self.Argument_of_periapsis)
		self.i = deg2rad(self.Inclination)


		# convert polar to Cartesian in body referential. It is the J2000 ecliptic
		# for planets and asteroids, and a planet's own PCPF referential for moons
		# of this planet

		self.Position = self.setCartesianCoordinates(0)

		# set North Pole orientation and angular distance 
		# of Prime Meridian wirh DESC node

		self.setBodyOrientation()

		# set the tracking Frame
		self.setLocalEclipticRef()


		# Create referentials:
		# for each body, 2 types of referentials can be created:
		# - Inertial (fixed to the stars and won't rotate with the planet)
		# - Non-inertial (rotating with the body's surface)
		#
		# PCI referentials are inertial ("Planet-Centered Inertial"). Its coordinate frames have their origins 
		# at the center of mass of the planet and are fixed with respect to the stars. "I" in "PCI" stands for 
		# inertial (i.e. "not accelerating"),
		#
		# In contrast
		#
		# PCPF referentials are non-inertial ("Planet-Centered Planet-Fixed"). They remains fixed with respect to 
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
		self.make_PCI_referential()

		# determine axis of rotation
		self.setRotAxis()

		# set Planet-Centered-Planet_fixed referential (PCPF)
		# that rotates with the planet's surface

		self.make_PCPF_referential() 

		# create body shape ...
		self.makeShape()
		# ... and add its texture 
		self.setAspect(key)

		# Now that texture has been properly positioned, tilt the body
		# by rotating the referential attached to it (PCPF)

		self.setPCPFAxisTilt()

		# create planet orbit curve and 1st vertex 
		# as the current position

		if self.makeOrbit() == False:
			print "Houston, we have a problem!! for ", self.Name
			return

		# add label

		self.Labels.append(label(pos=(self.Position[0],self.Position[1],self.Position[2]), text=self.Symbol+self.Name, xoffset=20, yoffset=12, space=0, height=10, color=color, border=6, box=False, font='sans'))

		# hide body if not required
		if (self.SolarSystem.ShowFeatures & bodyType) == 0:
			self.RefOrigin.visible = False
			self.Labels[0].visible = False

		# set body specific rotation characteristics
		self.initRotation()



	# makeBody::
	def setBodyOrientation(self):

		# setBodyOrientation will determine the direction of the North Pole
		# and the angle between the prime meridian and the descending node.

		self.Pole_vec, self.W_angle, self.Omega_angle = self.compute_Ecliptic_NorthPole_data()
		

	# makeBody::
	def AdjustNPforPeriodicTerms(self, RA, decl, T, d):
		# provided for planets only, otherwise unused: 
		# default is we do not provide adjustment for RA and declination.
		# It is up to the planet (in planet.py) to provide these adjustements
		return RA, decl

	# makeBody::
	def AdjustPMforPeriodicTerms(self, T, d):
		# provided for planets only, otherwise unused: 
		# default is we do not provide adjustment for the Prime Meridian.
		# It is up to the planet (in planet.py) to provide these adjustements
		# return W
		return 0.0


	def compute_Ecliptic_NorthPole_data(self):
		"""
		Calculates the north pole direction for the current body for a given date
		and their prime meridian angle W in the J2000 ecliptic coordinate system, 
		including perturbations. The RA and Dec values are measurement referring to
		where the planet planet points its north pole to the celestial sphere. In 
		essence, its origin is pointing to the vernal equinox, so the RA value is 
		the angle between the VE and the projection of the NP vector on the ecliptic 
		plane. Then from that point on, the DEC value is the angle we must rotate
		that projection vector perpendicularly to the ecliptic plane to reach the
		desired orientation
		"""
		bodies = [	"Sun", 	  "Mercury", "Venus",   "Earth", "Mars", "Jupiter", 
					"Saturn", "Uranus",  "Neptune", "Pluto"]

		if self.Name in bodies:

			#cur = datetime.datetime.now()

			# get UTC system time
			cur = System_utc

			#jd = julian_date_manual(year, month, day, hour, minute, second)

			# calculate jd date (in days)
			jd = julian_date_manual(cur.year, cur.month, cur.day, cur.hour, cur.minute, cur.second)
			# calculate the interval in Julian centuries (36525 days) from J2000
			T = calculate_T_from_jd(jd)
			# calculate days since J2000
			d = calculate_d_from_jd(jd)

			# Obliquity of the ecliptic for J2000.0 (in degrees)
			obliquity_ecliptic_deg = 23.43928
			obliquity_ecliptic_rad = np.radians(obliquity_ecliptic_deg)

			# generate the Rotation matrix from J2000 Equatorial to J2000 Ecliptic
			eq_to_ecl_matrix = rotation_matrix_x(-obliquity_ecliptic_rad)

			planet_data_results = {}

			# Re-using Omega values from the provided table for consistency with 
			# the request. These are standard IAU parameters for the ecliptic longitude 
			# of the ascending node of the equator.

			omega_values = {
				"Sun":     345.717, "Mercury": 318.528, "Venus":  27.502, "Earth":  89.642,
				"Mars":    352.883, "Jupiter": 272.072, "Saturn": 80.009, "Uranus": 18.232,
				"Neptune": 320.083, "Pluto":   318.472
			}

			try:
				# Get pole parameters in J2000 Equatorial ...
				RA_eq, dec_eq = get_planet_pole_parameters(self.Name, T, d)

				# ... and adjust for periodic terms
				RA_eq, dec_eq = self.AdjustNPforPeriodicTerms(RA_eq, dec_eq, T, d)

				pole_vector_eq = equatorial_to_cartesian_vector(RA_eq, dec_eq)

				# Transform to J2000 Ecliptic
				pole_vector_ecl = apply_rotation(pole_vector_eq, eq_to_ecl_matrix)

				# Get prime meridian angle W ...
				W_angle = get_planet_prime_meridian_W(self, T, d)

				#W_angle = self.get_planet_prime_meridian_W(T, d)

				# ... and adjust for periodic terms
				#W_angle = self.AdjustPMforPeriodicTerms(W_angle, T, d)

				# Get Omega angle
				Omega_angle = omega_values.get(self.Name, np.nan) # Use np.nan for missing values

				return pole_vector_ecl, W_angle, Omega_angle

			except ValueError as e:
				#         planet_data_results[planet] = f"Error: {e}"
				#	            planet_data_results[planet] = "Error: {e}"
				print "Error: {e}"

		return [0,0,0], 0, 0


	# makeBody
	def get_planet_prime_meridian_WXXX(self, T, d):
		pass

	# makeBody::
	def make_PCI_referential(self): 

		# This is the default makebody::make_PCI_referential method.
		# PCI (Planet Centered Intertial) is the referential fixed to the star. default is None 
		# (mostly for objects that don't require it such as PHA, comets, asteroids). 
		# Planets and the Sun must override this method to create a 3D referential, 
		# as it can be displayed through the user interface.

		self.PCI = None 

	# makeBody::
	def setRotAxis(self): 
		self.RotAxis = self.Pole_vec
	"""
		if self.PCI is not None:
			self.RotAxis = self.PCI.RotAxis
		else:
			self.RotAxis = self.setObliquity()


	def setObliquity(self): 
		print "setObliquity for ", self.Name
		return self.Pole_vec
		#####  TEST TEST remove return vector(0, sin(self.TiltAngle), cos(self.TiltAngle))
	"""
	
	def getRotAxis(self):
		return self.RotAxis

	# makeBody::
	#def setLocalEclipticRef(self):
	#	pass

	# makeBody::
	def setLocalEclipticRef(self):
		# the LocalEclipticRef frame is used mainly for planets acting as a central body,
		# meaning planets with moon(s). The LocalEclipticRef allows the moon(s)
		# orbits to be calculated related to the referential which is geocentric
		# ecliptic by nature instead of the J2000 ecliptic referential for the solar system.
		#print "SETTING LOCAL ECLIPTIC for "+self.Name
		self.LocalEclipticRef = frame(	frame=self.SolarSystem.J2000eclipticFrame,
										axis=self.SolarSystem.J2000eclipticFrame.axis, 
										up=self.SolarSystem.J2000eclipticFrame.up) 

		self.LocalEclipticRef.pos = self.Position

		# both J2000 ecliptic and geocentric ecliptic share the same (x,y) plane,
		# where x points to the vernal equinox


	# makeBody::
	def make_PCPF_referential(self): 
		
		# This is the default makebody::make_PCPF_referential method.
		# PCPF (Planet Centered Planet Fixed) is the referential that rotates with the body:
		# default PCPF referential: just a frame with no axis. Body texture is linked to
		# this referential and rotate with it. Only the makeEarth class must override this 
		# method as its PCPF requires to display its axis.
	
		referenceFrame = self.SolarSystem.J2000eclipticFrame
		if self.CentralBody != None:
#			referenceFrame = self.CentralBody.RefOrigin
			referenceFrame = self.CentralBody.LocalEclipticRef

		self.PCPF = makeBasicReferential({
			'parent_frame': referenceFrame,
			'body': self,
			'show':	False,
			'color': Color.cyan,
			'orientation': {
				'pole_vec': self.Pole_vec,
				'w_angle': self.W_angle,
				'omega_angle': self.Omega_angle,
			},
            'name':  self.Name+"PCPF",
		})
		
		#self.LocalEclipticRef 			= self.PCPF.referential
		self.RefOrigin 				= self.PCPF.referential
		self.RefOrigin.visible		= True

		# the tilt will be initiated after loading the body texture
		self.PCPF.display(True)



	# makeBody::
	def getSemiMinor(self, semimajor, eccentricity):

		# knowing the perihelion, the formula 
		# is given by rp = a(1-e)
		
		return semimajor * sqrt(1 - eccentricity**2)

	# makeBody::
	def setAspect(self, key):
		self.Texture = materials.loadTGA("./img/"+self.Tga) if self.SolarSystem.objects_data[key]["material"] != 0 else materials.loadTGA("./img/asteroid")
		self.BodyGeometry.material = materials.texture(data=self.Texture, mapping="spherical", interpolate=False)

	# makeBody::
	def makeShape(self):
		# default makebody::makeShape
		self.RefOrigin.pos= self.Position #(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2])
		self.BodyGeometry = sphere(frame=self.RefOrigin, pos=(0,0,0), np=64, radius=self.getBodyRadius(), make_trail=false, up=(0,0,1))

	def getBodyRadius(self):
		return self.radiusToShow/self.SizeCorrection[self.sizeType]

	def setPCPFAxisTilt(self):
		if self.PCPF is not None:
			self.PCPF.setAxisTilt()

	# makeBody::
	def makeOrbit(self):

		# attach a curve to the body to display its orbit

		if self.BodyGeometry is not None:
			# determine what the reference frame is:

			referenceFrame = self.SolarSystem.J2000eclipticFrame	# default is J2000 ecliptic ref
			if self.CentralBody != None:
				referenceFrame = self.CentralBody.LocalEclipticRef # for a moon, the referential is its planet tracking frame 

			# create an orbit either in the J2000 ecliptic referential centered 
			# in the SS Barycenter or a planet centric ecliptic referential

			self.Orbit = curve(frame=referenceFrame, Color=(self.Color[0]*0.8, self.Color[1]*0.8, self.Color[2]*0.8))

			self.Orbit.visible = True
#			self.Orbit.append(pos=self.RefOrigin.pos)
			self.Orbit.append(pos=self.Position)
			return True
		else:

			print "Failed to initiate orbit for ", self.Name
			return False

	# makeBody::
	def initRotation(self):
		print "INIT ROT for ", self.Name
		# this method is provided as a placeholder on this base class
		# and should be overwritten by any child class requiring a precise
		# orientation of its texture based on time of day (ie earth)
		return

	def getRealisticSizeCorrection(self):
		return self.RealisticCorrectionSize

	def setRealisticSizeCorrection(self, value):
		self.RealisticCorrectionSize = value

	# makeBody::
	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x
		self.BodyGeometry.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]

	def setTraceAndLabelVisibility(self, trueFalse):
		if self.RefOrigin.visible == True:
			self.Orbit.visible = trueFalse
			for i in range(len(self.Labels)):
				self.Labels[i].visible = trueFalse

	
	# makeBody::
	def animate(self, timeIncrement):

		# makeBody::animate This is the default method
		# this method takes care of moving the current body on 
		# its orbit as well as rotating its surface around its 
		# North Pole axis, given the provided time increment

		if self.hasRenderedOrbit == False:
			self.draw()

		self.wasAnimated = true

		# update position

		self.updateOrbitalElements(self.ObjectIndex, timeIncrement)
		self.R, self.Nu = self.setPolarCoordinates(deg2rad(self.Eccentric_anomaly))

		# calculate current body position in its orbit knowing
		# its current distance from the central object and True anomaly (Nu)
		# that were set in setPolarCoordinates

		self.N = deg2rad(self.Longitude_of_ascendingnode)
		self.w = deg2rad(self.Argument_of_periapsis)
		self.i = deg2rad(self.Inclination)

		# convert polar to Cartesian in Sun referential
		self.Position = self.setCartesianCoordinates(timeIncrement)
		
		# update foci position
		"""
		if False and self.CentralBody is not None and self.CentralBody.Position != (0,0,0):
			print "BODY: ", self.Name, " - central body position", self.CentralBody.Position #self.Foci 
			self.Foci = self.CentralBody.Position

			
			print "...orbit.pos=", self.Orbit.pos
			#raw_input("type a key")

			self.Orbit.pos = self.Foci
			#raw_input("type another one...")
		"""

		self.RefOrigin.pos = self.Labels[0].pos = self.Position #vector(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2])

		# finally, rotate the body's 
		# surface around its North Pole

		self.animateBodyRotation()

		return self.getCurrentVelocity(), self.getCurrentDistanceFromEarth(), self.getCurrentDistanceFromSun()

	# makeBody::
	def setOrbitalElements(self, key, timeincrement = 0):
		
		# makeBody::setOrbitalElements (default)
		# Comets, asteroids or dwarf planets data comes from pre-ploaded data
		# files -or- predefined values. Orbital Position is calculated from the 
		# last time of perihelion passage. This is the default behavior

		self.setOrbitalFromJPLhorizon(self.SolarSystem.objects_data[key], timeincrement) #-0.7)


	def setOrbitalFromJPLhorizon(self, elts, timeincrement=0):
		# data comes from data file or predefined values
		self.e 							= elts["eccentricity_EC"]
		self.Longitude_of_periapsis 	= elts["longitude_of_periapsis_W"]
		self.Longitude_of_ascendingnode = elts["longitude_of_ascendingnode_OM"]
		self.Argument_of_periapsis 		= self.Longitude_of_periapsis - self.Longitude_of_ascendingnode
		self.Inclination 				= elts["orbital_inclination_IN"]
		self.a 							= getSemiMajor(self.Periapsis, self.e)


		#if self.CentralBody is not None:
		#	self.Inclination -= self.CentralBody.AxialTilt
			
		self.Time_of_perihelion_passage = elts["jd_time_of_periapsis_passage_Tp"]
		self.Mean_motion				= elts["mean_motion_N"]
		self.Epoch						= elts["epochJD"]
		self.Mean_anomaly				= elts["mean_anomaly_MA"] 	# the Mean Anomaly angle can also be computed using
																	# the orbital period and Time of perihelion as:
																	# M = (t - T) * 2*PI/P where T is the timeOfPeriapsis,
																	# t is the current time and P the orbital period 
		self.revolution					= elts["revolution_PR"]
		self.OrbitClass					= elts["orbit_class"]

		# save original value of longitude of ascending node coming from the mean elements.
		# It will be used to calculate deviation with time on the current value of 
		# longOfAscMode in makeBody::updateOrbitalElements

		self.Omega0 =  self.Longitude_of_ascendingnode

		# calculate current position based on orbital elements

		success, self.Eccentric_anomaly = self.updateBodyPosition(timeincrement)
		if success == False:
			print (self.Name+" Warning Could not converge - E = "+str(self.Eccentric_anomaly))


	# makeBody::
	def updateOrbitalElements(self, key, timeincrement = 0):
		# makeBody::updateOrbitalElements (default)
		# It is called from the makeBody::animate method

		success, self.Eccentric_anomaly = self.updateBodyPosition(timeincrement)
		if success == False:
			print (self.Name+" Warning Could not converge - E = "+str(self.Eccentric_anomaly))


	# makeBody::
	def updateBodyPosition(self, timeIncrement):

		# calculate current position based on orbital 
		# elements (timeIncrement comes in days as a float)
		
		dT = daysSinceEpochJD(self.Epoch, self.locationInfo) + timeIncrement 

		# compute Longitude of Ascending node taking 
		# into account the time elapsed since epoch

		self.Longitude_of_ascendingnode = self.Omega0 + 3.82394e-5 * dT
		print "Updating Body Position for: ", self.Name

		# adjust Mean Anomaly with time elapsed since epoch
		M = toRange(self.Mean_anomaly + self.Mean_motion * dT)

		# since we can't solve Kepler's equation analytically,
		# we use an iterative numerical method

		return solveKepler(M, self.e, 20000)

	# makeBody::
	def updateAllReferentials(self):

		# update position and the 
		# rotation (when non-inertial)

		if self.PCI is not None:
			self.PCI.updateReferential()
		
		if self.PCPF is not None:
			self.PCPF.updateReferential()
			self.PCPF.rotate(angle=self.RotAngle)

		self.LocalEclipticRef.pos = self.Position


	def getIncrement(self):
		# provide 1 degree increment in radians
		return pi/180


	# makebody::
	def draw(self):
		
		# this method will render the orbit shape of the current body. 
		# Typically, moons do not show their orbit, hence this method
		# is overridden by a dummy method in the moon classes

		self.Orbit.visible = False
		rad_E = deg2rad(self.Eccentric_anomaly)
		increment = self.getIncrement()

		# draw small segments between 2 
		# angulars steps looping between 0 to 2PI

		for E in np.arange(0, 2*pi+increment, increment):
			#self.setPolarCoordinates(E+rad_E)
			self.R, self.Nu = self.setPolarCoordinates(E+rad_E)


			# from R and Nu, calculate 3D coordinates 
			# and update current position
			
			self.drawSegment(trace = True) #E*180/pi)
			### rate(5000) # ??

		if self.RefOrigin.visible:
			self.Orbit.visible = True

		self.hasRenderedOrbit = True


	# makeBody::
	def setPolarCoordinates(self, E_rad):

		# given the provided Eccentric Anomaly E, we can calculate
		# the coordinates X,Y of the body and its in the orbit plane 
		# by using the semi-major a and the orbit excentricity e 
		# using the formulas:

		X = self.a * (cos(E_rad) - self.e)
		Y = self.a * sqrt(1 - self.e**2) * sin(E_rad)

		# Now calculate current 
		# Radius and true Anomaly

		return sqrt(X**2 + Y**2), atan2(Y, X)
		#self.R = sqrt(X**2 + Y**2)
		#self.Nu = atan2(Y, X)

		# Note that atan2 returns an angle in
		# radian, so Nu is always in radian


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

		# follow planet rotation
		self.PCPF.referential.rotate(angle=RotAngle, axis=self.PCPF.RotAxis) #, origin=(0,0,0)) #self.PCPF.referential.pos) #(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]))
#		self.PCPF.referential.rotate(angle=RotAngle, axis=self.PCPF.ZdirectionUnit) #, origin=(0,0,0)) #self.PCPF.referential.pos) #(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]))

	# makeBody::
	def animateBodyRotation(self):
		ti = self.SolarSystem.getTimeIncrement()
		#if self.Rotation <= 0:
		#	print self.Name
			
		self.RotAngle = (2*pi/self.Rotation)*ti
		self.updateAllReferentials()

	# makeBody::
	def drawSegment(self, trace = True):
		
		# append to the orbit curve the segment 
		# corresponding to the current coordinate

		self.Position = self.setCartesianCoordinates(0)

		# update origin

		self.RefOrigin.pos = self.Position
				
		# when we want to visualize the orbit, we show the 
		# section under the ecliptic with dimmer colors

		if trace:

			# display orbit in brighter Color when above ecliptic
			if self.Position[2] < 0:
				"""
				self.Interval += 1
				if self.Interval % 2 == 0:
					#self.Orbit.append(pos=self.BodyGeometry.pos, color=self.Color) #, interval=50)
					self.Orbit.append(pos=self.BodyGeometry.pos, color=(self.Color[0]*0.3, self.Color[1]*0.3, self.Color[2]*0.3))			
				else:
					self.Orbit.append(pos=self.BodyGeometry.pos, color=Color.black) #, interval=50)
				"""
				# new
				self.Orbit.append(pos=self.RefOrigin.pos, color=(self.Color[0]*0.3, self.Color[1]*0.3, self.Color[2]*0.3))
			else:
				self.Orbit.append(pos=self.RefOrigin.pos, color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))


	# makeBody::
	def setCartesianCoordinates(self, timeIncrement, scale_correction=DIST_FACTOR):

		"""
			from polar coordinates, deduct cartesian coordinates in ecliptic referential, 
			using the current distance to object (R), the True anomaly (Nu), and the 
			orbital parameters pertaining to the orbit's orientation: (N, i, w): This is the 
			combination of 3 rotations. 
			
			Note: the timeIncrement parameter is generally unused for bodies whose cartesian
			coordinates are calculated directly from their orbital elements. In some instances
			(mostly moons) there are too many perturbations that affect the body to trust the
			normal derivation from orbital elements. The position has to be calculated using
			polynomials that take into account the various perurbations. This default behavior
			uses the traditional derivation from orbital elements. For Moons, the scale_correction
			value is different than for planets because we want to exagerate the moon's orbit around
			its central object to keep bodies from fusing or being unrealistically close (see moons.py) 
		"""

		return (self.R * scale_correction * ( cos(self.N) * cos(self.Nu+self.w) - sin(self.N) * sin(self.Nu+self.w) * cos(self.i) ),
				self.R * scale_correction * ( sin(self.N) * cos(self.Nu+self.w) + cos(self.N) * sin(self.Nu+self.w) * cos(self.i) ),
				self.R * scale_correction * ( sin(self.Nu+self.w) * sin(self.i) ))

	# makeBody::
	def show(self):

		print "SHOW "+ self.Name
		if self.Name == "Moon" or self.Name == "Moon":
			print "SHOWING MOON! *********************"

		if self.hasRenderedOrbit == False:
			if self.Name == "Moon":
				print "+++++++++++++ RENDERING MOON ORBIT"
			self.draw()

		self.RefOrigin.visible = True
		self.Orbit.visible = True if self.SolarSystem.ShowFeatures & ORBITS != 0 else False

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
		self.RefOrigin.visible = False
		for i in range(len(self.Labels)):
			self.Labels[i].visible = False
		self.Orbit.visible = False
		#if self.Ring:
#		if self.nRings > 0:
#			self.SolarSystem.hideRings(self)

	def setAxisVisibility(self, setTo):
		if self.PCI is not None: 
			self.PCI.display(setTo)
		"""	
		return

		for i in range(3):
#			self.Axis[i].visible = setTo
			self.PCI.Axis[i].display(setTo)
			self.PCI.AxisLabel[i].visible = setTo
		"""
	# makeBody::
	def refresh(self):
		#print "refreshing "+self.Name

		if 	self.SolarSystem.SlideShowInProgress and \
			self.BodyType == self.SolarSystem.currentSource:
			return

		if 	self.BodyType & self.SolarSystem.ShowFeatures != 0 or \
			self.Name.lower() == EARTH_NAME or \
			self.Details == True:
			if self.RefOrigin.visible == False:
				self.show()

			# if this is the cameraViewTargetBody, 
			# check for local referential attribute

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
		return mag(vector(self.Position)) / DIST_FACTOR / AU

	# ----------------------------------------------
	# following redraw the orbit when required. it should be used in the update loop:
		"""
		def update_simulation(dt):
	    for body in bodies:
	        body.update_orbital_elements(dt)   # your Ω, ω, M evolution
	        update_orbit_curve_if_needed(body) # rebuild only when needed

		"""
	# ----------------------------------------------

	def build_orbit_curve(self, body, N=200):
	    """
	    Build a VPython curve for the body's orbit using its current orbital elements.
	    Stores the curve object and the elements used to build it.
	    """
	    # Remove old curve if it exists
	    if hasattr(body, "orbit_curve") and body.orbit_curve is not None:
	        body.orbit_curve.visible = False
	        del body.orbit_curve

	    pts = []
	    for k in range(N+1):
	        f = 2 * math.pi * k / N  # true anomaly sample
	        r_vec = body.position_from_true_anomaly(f)  # your own function
	        pts.append(r_vec)

	    body.orbit_curve = curve(pos=pts, color=body.color, radius=body.orbit_width)

	    # Store the elements used to build this curve
	    body.last_Omega_for_curve = body.Omega
	    body.last_omega_for_curve = body.omega
	    body.last_i_for_curve     = body.i


	def update_orbit_curve_if_needed(self, body, threshold_deg=1.0):
	    """
	    Rebuild the orbit curve only if the orbital plane or ellipse orientation
	    has changed enough to matter visually.
	    """
	    # Compute angular differences
	    dOmega = abs((body.Omega - body.last_Omega_for_curve + math.pi) % (2*math.pi) - math.pi)
	    domega = abs((body.omega - body.last_omega_for_curve + math.pi) % (2*math.pi) - math.pi)
	    di     = abs((body.i     - body.last_i_for_curve     + math.pi) % (2*math.pi) - math.pi)

	    # Convert threshold
	    thresh = math.radians(threshold_deg)

	    # If any orientation changed enough, rebuild
	    if dOmega > thresh or domega > thresh or di > thresh:
	        build_orbit_curve(body)


class emptyTrail:
	visible = False

# CLASS MAKESUN ---------------------------------------------------------------
class makeSun(makeBody):
	
	def __init__(self, system, Color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makeBody.__init__(self, system, SUN_NAME, Color, ptype, sizeCorrectionType, defaultSizeCorrection, None) #system)
		self.BodyGeometry.visible = True
		self.Orbit = emptyTrail()
		self.Labels[0].visible = False

	def setReferentialProfile(self):
		self.Ratio = [0,0,1]

	# makeSun::
	def make_PCI_referential(self): 

		# This is the referential that doesn't rotate with the 
		# planet and is fixed to the stars. In other words, it 
		# always points to the same direction
		
		self.setReferentialProfile()

		#print "Planet: build PCI ref for", self.Name
		self.PCI = make3DaxisReferential({
			'parent_frame': self.SolarSystem.J2000eclipticFrame,
			'body': self,
			'radius': 0,
			'orientation': {
				'pole_vec': self.Pole_vec,
				'w_angle': self.W_angle,
				'omega_angle': self.Omega_angle,
			},
			'show':	False,
			'color': Color.white,
			'ratio': self.Ratio,
            'name':  self.Name+"PCI",
			'legend': ["x", "y", "Eq.North"],
		})  

		self.RefOrigin 				= self.PCI.referential
		self.RefOrigin.visible		= True

		self.PCI.setAxisTilt()
		self.PCI.display(False)

	# makeSun::
	def make_PCPF_referential(self):
		self.PCPF = None
		pass 		

	# makeSun::
	def makeShape(self):
		self.RefOrigin.pos=self.Position #(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2])
		self.BodyGeometry = sphere(frame=self.RefOrigin, pos=(0,0,0), np=64, radius=self.getBodyRadius(), make_trail=False, color=Color.yellow)
		#self.PCPF.referential.visible = True

	# makeSun::
	def setAspect(self, key):
		#print "loading"+"./img/"+self.Tga
		self.Texture = materials.loadTGA("./img/"+self.Tga) if self.SolarSystem.objects_data[key]["material"] != 0 else materials.loadTGA("./img/asteroid")
		#self.BodyGeometry.material = materials.texture(data=self.Texture, mapping="spherical", interpolate=False)
		#print "setting sun as emissive"
		self.BodyGeometry.material = materials.emissive

	def updateStillPosition(self, timeinsec):
		pass

	# makeSun
	def draw(self):
		self.hasRenderedOrbit = True
		
	# makeSun::
	def setPolarCoordinates(self, E_rad):
		return 0.0, 0.0 
		#self.R = 0
		#self.Nu = 0

	# makeSun
	def getCurrentVelocity(self):
		return 0

	# makeSun
	def setCartesianCoordinates(self, timeIncrement):
		return (0,0,0)

	# makeSun::
	def getSemiMinor(self, semimajor, eccentricity):
		pass

	# makeSun::
	def makeOrbit(self):
		pass

	# makeSun::
	def setOrbitalElements(self, key, timeincrement = 0):
		# makeSun::setOrbitalElements 
		# (overrides makeBody::setOrbitalElements)

		self.Eccentric_anomaly = self.a = self.e = self.Longitude_of_ascendingnode = self.Argument_of_periapsis = self.Inclination = 0

	# makeSun::
	def updateOrbitalElements(self, key, timeIncrement):
		# makeSun::updateOrbitalElements 
		# (overrides makeBody::updateOrbitalElements)

		pass

	# makeSun::
	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		self.BodyGeometry.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]


# CLASS PLANET ----------------------------------------------------------------
class makePlanet(makeBody):
	
	def __init__(self, system, key, Color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makeBody.__init__(self, system, key, Color, ptype, sizeCorrectionType, defaultSizeCorrection, None) #system.Sun)
		#self.BodyGeometry.visible = False

		self.setRings()


	def setReferentialProfile(self):

		# overwrites the makebody::setReferentialProfile
		# this is the default ratio for planets' referential axis:
		# we only show the "z" axis to show the north Pole

		self.Ratio = [0,0,1]


	# makePlanet
	def make_PCI_referential(self): 

		# This is the referential that doesn't rotate with the 
		# planet and is fixed to the stars. In other words, it 
		# always points to the same direction
		
		self.setReferentialProfile()

		#print "Planet: build PCI ref for", self.Name

		self.PCI = make3DaxisReferential({
			'parent_frame': self.SolarSystem.J2000eclipticFrame,
			'body': self,
			'radius': 0,
			'orientation': {
				'pole_vec': self.Pole_vec,
				'w_angle': self.W_angle,
				'omega_angle': self.Omega_angle,
			},
			'show':	False,
			'color': Color.white,
			'ratio': self.Ratio,
            'name':  self.Name+"PCI",
			#'initial_rotation': pi/2,
			'legend': ["x", "y", "Eq.North"],
		})  

		self.RefOrigin 				= self.PCI.referential
		self.RefOrigin.visible		= True

		self.PCI.setAxisTilt()
		self.PCI.display(False)

		#self.setRotAxis()

	# makePlanet::
	def initRotation(self):
		# rotate the pre-loaded texture by the W angle that determines 
		# the prime meridian orientation at the present time
		print "INIT ROT for ", self.Name, ", W = ", self.W_angle, " degrees"
		self.RefOrigin.rotate(angle=(deg2rad(self.W_angle)), axis=self.RotAxis, origin=(0,0,0))


	# makePlanet::
	def setOrbitalElements(self, key, timeincrement = 0):
		
		# for the Major planets includig Pluto, we need to calculate 
		# the drift in precession with time of orbital elements (a, e, i, Omega, omega, M).
		# It follows an analytical T-based model (VSOP/Meeus style) -> drift a,e,i,L,Omega,W 

		self.updateOrbitalElements(key, timeincrement)


	# makePlanet::
	def updateOrbitalElements(self, key, timeincrement = 0):
		
		# Called from the makeBody::animate method.
		# update Orbital Elements based of time drift

		self.updatePlanetOrbitFromPrecession(self.SolarSystem.objects_data[key]["drift_coef"], timeincrement)

	# makePlanet::
	def updatePlanetOrbitFromPrecession(self, elts, timeincrement):

		# makeBody::updatePlanetOrbitFromPrecession
		#
		# re-calculate the osculating elements and current value of approximate position 
		# of the planet. Valid for all planets including pluto. Based in the time increment. 
		# This method is only applicable to planets.
		# 
		# Principle: for every timeIncrement, all orbital elements are recalculated. 
		# This include aphelion, eccentricity and inclinaison, followed by 
		# long-of-ascending-node and argument-of-perihelion

		
		# get number of days since J2000 epoch and obtain the fraction of century
		# (the rate adjustment is given as a rate per century)

		days = daysSinceJ2000UTC(self.locationInfo) + timeincrement
		
		# These formulas use 'days' based on days since 1/Jan/2000 12:00 UTC ("J2000.0"), 
        # instead of 0/Jan/2000 0:00 UTC ("day value"). Correct by subtracting 1.5 days...

		T = days/EARTH_CENTURY # T is in centuries (previous)

		self.a 			 = (elts["a"]   + (elts["ar"] * T)) * AU
		self.e 			 = elts["e"]    + (elts["er"] * T)
		self.Inclination = elts["i"]    + (elts["ir"] * T)

		# compute mean Longitude with correction factors 
		# beyond jupiter M = L - W + bT^2 +ccos(ft) + ssin(ft)
		
		L = elts["L"] + (elts["Lr"] * T) + (elts["b"] * T**2  +
											elts["c"] * cos(elts["f"] * T) +
											elts["s"] * sin(elts["f"] * T))

		self.Longitude_of_periapsis 	= elts["W"] + (elts["Wr"] * T)
		self.Longitude_of_ascendingnode = elts["N"] + (elts["Nr"] * T)

		# compute Argument of periapsis w

		self.Argument_of_periapsis = self.Longitude_of_periapsis - self.Longitude_of_ascendingnode

		# compute mean Anomaly M = L - W
		
		M = toRange(L - self.Longitude_of_periapsis) #W)

		# Obtain ecc. Anomaly E (in degrees) from M 
		# using an approx method of resolution:
		
		success, self.Eccentric_anomaly = solveKepler(M, self.e, 12000)
		if success == False:
			print ("Could not converge for "+self.Name+", E = "+str(self.Eccentric_anomaly))


	def setRotAxisXX(self):
		print "SET PCI.rotaAxis as AXIS for", self.Name
		self.RotAxis = self.PCI.RotAxis

	def updateStillPosition(self, timeinsec):
		return

	def getRealisticSizeCorrectionXX(self):
		#return 1/(DIST_FACTOR * 50)
		#PLANET_SZ_CORRECTION = 1/(DIST_FACTOR * 5)
		return 1/(DIST_FACTOR * 5)

	# makePlanet::
	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		print "TOGGLING!"
		self.BodyGeometry.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]
		if self.nRings > 0:
			#print "toggling rings for", self.Name
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
		
#		ringframe.frame = self.RefOrigin

		# make each ring element relative to the PCI Referential
		# so that they are aligned with the planet tilt and 
		# won't have to rotate
		#ringframe.frame = self.PCI.referential
		
		self.RingsFrame.frame = self.PCI.referential

		#ringframe.rotate(angle=pi/2, axis=(1,0,0))
		#ringframe.rotate(angle=(self.TiltAngle), axis=(1,0,0))
		return body #ringframe

	def removeRings(self):
		#print "attempting to remove rings..."

		for ring in self.Rings:
			#print "hidding ring from", self.Name
			ring.visible = False
			del(ring)

		del(self.RingsFrame)
		del(self.Rings)
		self.Rings = []
		self.nRings = 0


	def displayRings(self, trueFalse):
		if self.nRings > 0:
			#print "setting rings to ", trueFalse
			self.RingsFrame.visible = trueFalse

	def hideRings(self):
		#print "attempting to hide rings..."
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
USING_W_ANGLE = False 

# CLASS MAKEEARTH -------------------------------------------------------------
from widgets import *
class makeEarth_and_widgets(makePlanet):

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
		makePlanet
		makePlanet.__init__(self, system, EARTH_NAME, ccolor, type, sizeCorrectionType, defaultSizeCorrection)

		# Create widgets. This must be done after initializing earth. This will correctly
		# position the widgets with the earth current appearence
		
		self.PlanetWidgets = makePlanetWidgets(self)

		self.makeCelestialSphere()
		self.makeConstellations()

		# reposition the celestial sphere on the earth location:
		#self.SolarSystem.CelestialSphereOrigin = self.RefOrigin.pos
		#self.SolarSystem.ConstellationsOrigin = self.RefOrigin.pos
#-----------------------------------------------


	# makeEarth_and_widget::
	def makeShape(self):
		# overrides makebody::makeShape
		self.RefOrigin.pos= self.Position #(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2])
		self.BodyGeometry = sphere(frame=self.RefOrigin, pos=(0,0,0), np=64, radius=self.getBodyRadius(), make_trail=False, up=(0,0,1))
		#self.EarthNight   = sphere(frame=self.RefOrigin, pos=(0,0,0), np=64, 
		#						   radius=self.getBodyRadius()*1.001, make_trail=False, up=(0,0,1),
		#						   emissive=True,
		#	                       opacity=0.5, visible = True)

		"""
								   texture=night_texture,  
								   axis=axis_vec,
			                       up=(0,0,1),
			                       emissive=True,
			                       opacity=0.0)
		"""

	# makeEarth_and_widget::
	def setAspect(self, key):
		# overrides makebody::makeShape
		self.Texture = materials.loadTGA("./img/"+self.Tga) if self.SolarSystem.objects_data[key]["material"] != 0 else materials.loadTGA("./img/asteroid")


		self.BodyGeometry.material = materials.texture(data=self.Texture, mapping="spherical", interpolate=False)

		self.NightTexture = materials.loadTGA("./img/source/2k_earth_nightmap-boosted.tga")
		#self.EarthNight.material = materials.texture(data=self.NightTexture, mapping="spherical", interpolate=False)
		#self.EarthNight.rotation(axis=(0,0,1), angle=deg2rad(self.W_angle))


#-----------------------------------------------------


	#def refresh(self):
	#	makePlanet.refresh(self)
	#	self.Universe.visible = self.isFeatured(CELESTIAL_SPHERE)
	#	self.Constellations.visible = self.isFeatured(CONSTELLATIONS)
	
	def showTrackingReferentialVernalEqXXXXX(self):

		self.LocalEclipticRefAxis = simpleArrow(Color.yellow, 0, 5, vector(0,0,0), axisp = self.LocalEclipticRef.axis*100, context=self.LocalEclipticRef) #self.RefOrigin) #self.referential)
		self.LocalEclipticRefAxis.display(True)

		# Calculate angle between LocalEclipticRef X-axis and PCI X-axis
		dot_product = np.dot(np.linalg.norm(self.LocalEclipticRef.axis), np.linalg.norm(self.PCI.referential.axis))
	#	cross_product = np.cross(np.linalg.norm(self.LocalEclipticRef.axis), np.linalg.norm(self.PCI.referential.axis))

	#	axis = cross_product / np.linalg.norm(cross_product)

		#print ">>>>>>>>>>>>>>>>>> ANGLE=", dot_product, " - ", rad2deg(dot_product)

		# now rotate the LocalEclipticRef referential to align with PCI
		#self.LocalEclipticRef.rotate(angle=rad2deg(dot_product), axis=self.PCI.referential.axis)        
	
	# makeEarth::
	def toggleSize(self, realisticSize):
		makePlanet.toggleSize(self, realisticSize)
		self.PlanetWidgets.OVRL.visible = False if self.sizeType == SCALE_NORMALIZED else True


	# makeEarth_and_widget::
	def initRotation(self):
		if USING_W_ANGLE:
			# uses same method as for other planets
			makePlanet.initRotation()
		else:			
			
			# using old method to position the PM 
			# properly based on localtime

			self.setTextureFromSolarTime(None)
		

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

			self.RefOrigin.rotate(angle=(-self.SiderealCorrectionAngle), axis=self.RotAxis, origin=(0,0,0))
			self.SiderealCorrectionAngle = 0.0

			# alternate method would be to reapply the earth texture to start from scratch
			# including resetting self.Psi = 0.0

		# Reverse the previous texture initial angle 
		# ...and apply the new one
		self.RefOrigin.rotate(angle=(Psi-self.Psi), axis=self.RotAxis, origin=(0,0,0))
		self.Psi = Psi

		# also reflect the same reset amount with the widgets, if they already exist
		#if self.PlanetWidgets != None:
		#	self.PlanetWidgets.resetWidgetsRefFromSolarTime()


	# makeEarth_and_widget:: 
	def make_PCI_referential(self): 

		# makeEarth::make_PCI_referential overrides the makePlanet 
		# method as we want all axis to be visible for earth

		# This is the referential that is fixed to the stars
		#	z: North Equatorial: Polaris direction
		#	y: 
		#	x: u"\u2648": Vernal equinox

		self.PCI = make3DaxisReferential({
			'parent_frame': self.SolarSystem.J2000eclipticFrame,
			'body': 		self,
			'radius': 		0,
			'orientation': {
				'pole_vec': self.Pole_vec,
				'w_angle': self.W_angle,
				'omega_angle': self.Omega_angle,
			},
			'show':			False,
			'color': 		Color.white,
			'ratio': 		[1,1,1],
            'name': 		"EarthPCI",
			'legend': 		[u"\u2648", "y", "Eq.North"]
		})  


		# orientate the North Pole
		self.PCI.setAxisTilt()
		self.PCI.display(False)

		# set planet origin as the PCPF referential (rotates with the planet)

#		self.RefOrigin 				= self.PCI.referential #frame()
#		self.RefOrigin.visible			= True


	# makeEarth_and_widget::
	def make_PCPF_referential(self): #, size, position):
		
		# makeEarth::make_PCPF_referential overrides the parent class 
		# (makePlanet). This is the referential that rotates with the 
		# earth surface
			
		#	z:North-Equatorial: Polaris direction: 
		#	y: 
		#	x: Prime Meridian

		self.PCPF = make3DaxisReferential({
			'parent_frame': 	self.SolarSystem.J2000eclipticFrame,
			'body': 			self,
			'radius': 			0,

			'orientation': {
				'pole_vec': self.Pole_vec,
				'w_angle': self.W_angle,
				'omega_angle': self.Omega_angle,
			},
			'show':				True,
			'color': 			Color.cyan,
			'ratio': 			[1,1,1],
            'name': 			"EarthPCPF",
			'initial_rotation': -pi/2, #
			'legend': 			["Prime M", "y", "Eq.North"]
		})


		# Note: the referential tilt will be initiated after loading the body texture
		# set planet origin as the PCPF referential (rotates with the planet)

		self.RefOrigin 				= self.PCPF.referential #frame()
#		self.LocalEclipticRef 			= self.PCPF.referential
		self.RefOrigin.visible			= True

		self.PCPF.display(False)

	# makeEarth_and_widget::
	def animate(self, timeIncrement):
		# makeEarth::animate (overrides makeBody::animate")
		# first, run default planet animation as defined in makeBody class
		velocity, dte, dts = makePlanet.animate(self, timeIncrement)

		# and then, animate widgets features as well
		if self.PlanetWidgets is not None:
			self.PlanetWidgets.animate() #timeIncrement)

		#self.SolarSystem.CelestialSphereOrigin = self.RefOrigin.pos
		#self.SolarSystem.ConstellationsOrigin = self.RefOrigin.pos
		
		return velocity, dte, dts

	def resetTexture(self): # TO REVIEW!!!!
		self.BodyGeometry = None
		self.RefOrigin.visible = False
		New_Origin = frame(pos=self.RefOrigin.pos)
		del self.RefOrigin
		del self.BodyGeometry
		self.RefOrigin = New_Origin
		self.BodyGeometry = sphere(frame=self.RefOrigin, pos=(0,0,0), np=64, radius=self.getBodyRadius(), make_trail=false)
		self.BodyGeometry.material = materials.texture(data=self.Texture, mapping="spherical", interpolate=False)
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
			self.BodyGeometry.rotate(angle=(-self.SiderealCorrectionAngle), axis=self.RotAxis, origin=(0,0,0))
			self.SiderealCorrectionAngle = 0.0

			# alternate method would be to reapply the earth texture to start from scratch
			# including resetting self.Psi = 0.0
		"""

		# Reverse the previous texture initial angle 
		#self.BodyGeometry.rotate(angle=(-self.Psi), axis=self.RotAxis, origin=(0,0,0))
		# ...and apply the new one
######		self.BodyGeometry.rotate(angle=(Psi-self.Psi), axis=self.RotAxis, origin=(0,0,0))
		self.BodyGeometry.rotate(angle=(Psi), axis=self.RotAxis, origin=(0,0,0))
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
			self.RefOrigin.rotate(angle=(-self.SiderealCorrectionAngle), axis=self.RotAxis, origin=(0,0,0))

		# reset the new sidereal correction angle

		self.SiderealCorrectionAngle = (2 * pi / self.NumberOfSiderealDaysPerYear)* fl_diff_in_days
		print "Injecting sidereal angle correction of", rad2deg(self.SiderealCorrectionAngle), "degres"
		self.RefOrigin.rotate(angle=(self.SiderealCorrectionAngle), axis=self.RotAxis, origin=(0,0,0))

		# also reflect the same reset amount with the widgets

		######### self.PlanetWidgets.resetWidgetsReferencesFromNewDate() #fl_diff_in_days)


	# method called every few sec to allow for an update of the time label. BUT, the position is not updated
	# until we call this method self.STILL_ROTATION_INTERVAL/timeinsec times.

	# makeEarth_and_widgets::
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
#		self.BodyGeometry.rotate(angle=(newLocalInitialAngle - self.Gamma), axis=self.RotAxis, origin=(0,0,0))
		self.RefOrigin.rotate(angle=(newLocalInitialAngle - self.Gamma), axis=self.RotAxis, origin=(0,0,0))
		print "rotating by ", newLocalInitialAngle - self.Gamma, " degree"

		# update angle with its updated value
		self.Gamma = newLocalInitialAngle


	# makeEarth_and_widget::
	def makeConstellations(self):
		"""
		Constellations and Celestial sphere are bound to the 
		Earth's Inertial Frame of Reference: self.PCI
		"""
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
		

#		file = "./img/source/8k_constellation_figures-normalized.tga"
#		file = "./img/source/4k_starmap_cleaned_up-flipped.tga"
		file = "./img/NASA/constellation_bounds_and_figures_colored_legend_reversed_8k.tga" # traditional one
#		file = "./img/source/8k_constellations_flipped-normalized.tga"
#		file = "./img/source/4k_starmap_cleaned_up-flipped-normalized.tga"

		if os.path.isfile(file):
			# adjust celestial Sphere position
			#self.ConstellationOrigin = frame(frame=self.LocalEclipticRef, pos=vector(0,0,0))
#			self.SolarSystem.Constellations = sphere(frame=self.LocalEclipticRef, pos=vector(0,0,0), visible = False, radius=self.SolarSystem.UniversRadius, color=Color.white, opacity=0.2) #, up=vector(0,0,1))
			self.SolarSystem.Constellations = sphere(frame=self.PCI.referential, pos=vector(0,0,0), visible = False, radius=self.SolarSystem.UniversRadius, color=Color.white, opacity=0.2) #, up=vector(0,0,1))
			self.SolarSystem.Constellations.material = materials.texture(data=materials.loadTGA(file), mapping="spherical", interpolate=False)

			# adjust constellations layout on our 3d window to match our coordinates system
			self.SolarSystem.Constellations.rotate(angle=(pi/2), 		axis=self.SolarSystem.J2000eclipticRef.XdirectionUnit, origin=(0,0,0))
			self.SolarSystem.Constellations.rotate(angle=(pi/2), 		axis=self.SolarSystem.J2000eclipticRef.ZdirectionUnit, origin=(0,0,0))



		else:
			print ("Could not find "+file)
		#self.Scene.scale = self.Scene.scale / 1e10

	# makeEarth_and_widget::
	def makeCelestialSphere(self): # Unused
		"""
		Constellations and Celestial sphere are bound to the 
		Earth's Inertial Frame of Reference: self.PCI
		"""
		import os.path
		#print "CELESTIAL SPHERE"
#		CELESTIAL_RADIUS = 2000 #10000
		#file = "./img/8k_stars_milky_way-reversed.tga"
		file = "./img/NASA/starmap_8k-reversed.tga"
#		file = "./img/source/8k-stellarium-normalized-flipped.tga"

		if os.path.isfile(file):
			# adjust celestial Sphere position
			#self.CelestialSphereOrigin = frame(pos=vector(0,0,0))
#			self.SolarSystem.Universe = sphere(frame=self.LocalEclipticRef, pos=vector(0,0,0), visible = False, radius=self.SolarSystem.UniversRadius, color=Color.white, opacity=1.0) #, up=vector(0,0,1)) #0.8)
			self.SolarSystem.Universe = sphere(frame=self.PCI.referential, pos=vector(0,0,0), visible = False, radius=self.SolarSystem.UniversRadius, color=Color.white, opacity=1.0) #, up=vector(0,0,1)) #0.8)
			self.SolarSystem.Universe.material = materials.texture(data=materials.loadTGA(file), mapping="spherical", interpolate=False)
			
			# adjust celestial sphere layout on our 3d window to match our coordinates system
			self.SolarSystem.Universe.rotate(angle=(pi/2), 		axis=self.SolarSystem.J2000eclipticRef.XdirectionUnit, origin=(0,0,0))
#			self.SolarSystem.Universe.rotate(angle=deg2rad(self.SolarSystem.J2000_Equatorial_obliquity), axis=self.SolarSystem.J2000eclipticRef.YdirectionUnit, origin=(0,0,0))
			self.SolarSystem.Universe.rotate(angle=(pi/2), 		axis=self.SolarSystem.J2000eclipticRef.ZdirectionUnit, origin=(0,0,0))

		else:
			print ("Could not find "+file)
		#self.Scene.scale = self.Scene.scale / 1e10


# CLASS SATELLITE -------------------------------------------------------------

def nodePrecession():
	MOON_CYCLE = 18.6 # years
	CORRECTION_PER_YEAR = 360 / 18.6
	CYCLE_START_YEAR = 2024

		

# CLASS HYBERBOLIC ------------------------------------------------------------
class hyperbolic(makeBody):
	def __init__(self, system, key, color, planetBody):
		makeBody.__init__(self, system, key, color, HYPERBOLIC, HYPERBOLIC, HYPERBOLIC_SZ_CORRECTION, None) #planetBody)
		self.isMoon = false

	def setAxisVisibility(self, setTo):
		pass

	def getRealisticSizeCorrectionXX(self):
		#SATELLITE_SZ_CORRECTION = 1/(DIST_FACTOR * 5)
		return 1/(DIST_FACTOR * 5)

	# hyperbolic::
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

		self.BodyGeometry.radius = self.radiusToShow  / self.SizeCorrection[self.sizeType]

	# hyperbolic::
	def setPolarCoordinates(self, E_rad):
		# TBD
		# calculate coordinates for an hyperbolic curve
		X = self.a * (cos(E_rad) - self.e)
		Y = self.a * sqrt(1 - self.e**2) * sin(E_rad)

		# Now calculate current Radius and true Anomaly
		return sqrt(X**2 + Y**2), atan2(Y, X)
		
		# Note that atan2 returns an angle in
		# radian, so Nu is always in radian


	# hyperbolic::
	def draw(self):
		print "drawing "+self.Name
		self.Orbit.visible = False
		rad_E = deg2rad(self.Eccentric_anomaly)
		increment = self.getIncrement()

		for E in np.arange(increment, 2*pi+increment, increment):
			#self.setPolarCoordinates(E+rad_E)
			self.R, self.Nu = self.setPolarCoordinates(E+rad_E)

			# from R and Nu, calculate 3D coordinates and update current position
			self.drawSegment(trace = False) #E*180/pi, False)
			
			### rate(5000) #?!

		self.hasRenderedOrbit = True

	# hyperbolic::
	def make_PCPF_referential(self):
		self.RefOrigin = frame()
		self.RefOrigin.visible	= True
		self.PCPF = None



# CLASS GENERICSPACECRAFT -----------------------------------------------------
class makeGenericSpacecraft(makeBody):
	def __init__(self, system, key, color):
		#print "makeGenericSpacecraft: CALLED FOR KEY=", key
		makeBody.__init__(self, system, key, color, SPACECRAFT, SPACECRAFT, SMALLBODY_SZ_CORRECTION, None) #system.Sun)
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
		print "Spacecraft:Init: label=", self.Labels[0].pos, "origin=", self.RefOrigin.pos
		print "*** FINISHED init makeGenericSpacecraft ***"
		print ""
		"""
	def setAxisVisibility(self, setTo):
		pass

	# makeGenericSpacecraft::
	def animate(self, timeIncrement):
		#makeBody.animate(self, timeIncrement)
		if self.hasRenderedOrbit == False:
			self.draw()

		self.wasAnimated = true

		# update position
		self.setOrbitalElements(self.ObjectIndex, timeIncrement)
		#self.setPolarCoordinates(deg2rad(self.Eccentric_anomaly))
		self.R, self.Nu = self.setPolarCoordinates(deg2rad(self.Eccentric_anomaly))


		# initial acceleration
		#self.Acceleration = vector(0,0,0)

		# calculate current body position on its orbit knowing
		# its current distance from Sun (R) and True anomaly (Nu)
		# that were set in setPolarCoordinates

		self.N = deg2rad(self.Longitude_of_ascendingnode)
		self.w = deg2rad(self.Argument_of_periapsis)
		self.i = deg2rad(self.Inclination)

		# convert polar to Cartesian in Sun referential
		self.Position = self.setCartesianCoordinates(timeIncrement)

		# update foci position
		#self.Foci = self.CentralBody.Position

		#print "ANIMATING-1 ", self.Name, "Origin=",self.RefOrigin.pos, "Foci =",self.Foci

#		self.RefOrigin.pos = vector(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2])
		self.RefOrigin.pos = vector(self.Position[0],self.Position[1],self.Position[2])
		self.Labels[0].pos = self.RefOrigin.pos
		
		#print "ANIMATING-2 ", self.Name, "Origin=",self.RefOrigin.pos, "Foci =",self.Foci
#		self.Labels[0].pos = vector(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2])
		self.animateBodyRotation()
		#print "ANIMATING-3 ", self.Name, "Origin=",self.RefOrigin.pos, "Foci =",self.Foci

		return self.getCurrentVelocity(), self.getCurrentDistanceFromEarth(), self.getCurrentDistanceFromSun()


	# makeGenericSpacecraft::
	def setAspect(self, key):
		if self.SolarSystem.objects_data[key]["material"] != 0:
			data = materials.loadTGA("./img/"+ self.Tga)
			self.BodyGeometry.objects[0].material = materials.texture(data=data, mapping="cylinder", interpolate=False)


	# makeGenericSpacecraft::
	def makeShape(self):
#		self.length = self.lengthFactor * 2 * self.radiusToShow/self.SizeCorrection[self.sizeType]
		self.length = self.lengthFactor * 2 * self.getBodyRadius()
		self.radius = 20 
		self.compounded = True

		# create compound object
		self.BodyGeometry = self.RefOrigin

		# create fuselage
		self.BARYCENTER_XCOOR = -self.length/2
		cylinder(frame=self.RefOrigin, pos=(self.BARYCENTER_XCOOR,0,0), radius=self.radius, length=self.length)

		# create aft tank
		self.AFT_TANK_RADIUS = self.radius
		self.AFT_TANK_CENTER_XCOOR = self.BARYCENTER_XCOOR + self.length/9
		sphere(frame=self.RefOrigin, pos=(self.AFT_TANK_CENTER_XCOOR, 0, 0), radius=self.AFT_TANK_RADIUS, color=Color.white, np=64)		

		# create forward Platform
		self.FWD_TANK_RADIUS = self.radius
		self.FWD_TANK_CENTER_XCOOR = self.BARYCENTER_XCOOR + self.length - self.radius/1.5
		sphere(frame=self.RefOrigin, pos=(self.FWD_TANK_CENTER_XCOOR, 0, 0), radius=self.FWD_TANK_RADIUS, color=Color.white)		

		# create engine
		self.makeEngine()
		"""
		self.ENGINE_HEIGHT = self.length/13
		self.ENGINE_TOP_XCOOR = self.AFT_TANK_CENTER_XCOOR - self.AFT_TANK_RADIUS - self.ENGINE_HEIGHT/2 - self.length/30
		cylinder(frame=self.BodyGeometry, pos=(self.ENGINE_TOP_XCOOR,0,0), radius=self.AFT_TANK_RADIUS/5, length=self.length/13, color=Color.darkgrey)

		# create COPV
		self.COPV_RADIUS = self.length/17
		sphere(frame=self.BodyGeometry, pos=(self.ENGINE_TOP_XCOOR + self.length/31, self.length/9, 0), radius=self.COPV_RADIUS, color=Color.grey)		
	
		nozzle = self.makeNozzle()
		nozzle.frame = self.BodyGeometry
		"""
#		self.RefOrigin.pos = self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]
		self.RefOrigin.pos = self.Position[0],self.Position[1],self.Position[2]

		#print "GenericSpacecraft: MakeShape: self.RefOrigin.pos=", self.RefOrigin.pos

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
			cylinder(frame=self.RefOrigin, axis=(0,1,0), pos=(self.ENGINE_TOP_XCOOR + (self.ENGINE_HEIGHT*0.8), -self.length/12, 0), radius=self.ENGINE_RADIUS, length=self.length/6, color=Color.darkgrey)

		k = -1
		for i in range(self.engine):
			cylinder(frame=self.RefOrigin, pos=(self.ENGINE_TOP_XCOOR, self.ENGINE_YOFFSET * k, 0), radius=self.ENGINE_RADIUS, length=self.ENGINE_HEIGHT, color=Color.darkgrey)
			nozzle = self.makeNozzle(self.ENGINE_YOFFSET * k)
			nozzle.frame = self.RefOrigin
			k = -k
		k = -1
		for i in range(self.COPV):
			# create COPV
			self.COPV_RADIUS = self.length/18 - i*(self.length/100)
			sphere(frame=self.RefOrigin, pos=(self.ENGINE_TOP_XCOOR + self.length/31, 0, self.length/11 * k), radius=self.COPV_RADIUS, color=Color.grey)		
			k = -k

	def makeEngineSAVE(self):
		# create engine
		if self.engine <= 1:
			self.ENGINE_HEIGHT = self.length/13
		else:
			self.engine = 2
			self.ENGINE_HEIGHT = self.length/16

		self.ENGINE_TOP_XCOOR = self.AFT_TANK_CENTER_XCOOR - self.AFT_TANK_RADIUS - self.ENGINE_HEIGHT/2 - self.length/30
		cylinder(frame=self.RefOrigin, pos=(self.ENGINE_TOP_XCOOR,0,0), radius=self.AFT_TANK_RADIUS/5, length=self.length/13, color=Color.darkgrey)

		# create COPV
		self.COPV_RADIUS = self.length/17
		sphere(frame=self.RefOrigin, pos=(self.ENGINE_TOP_XCOOR + self.length/31, self.length/9, 0), radius=self.COPV_RADIUS, color=Color.grey)		
	
		nozzle = self.makeNozzle()
		nozzle.frame = self.RefOrigin

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

	# makeGenericSpacecraft::
	def initRotation(self):
		self.RotAngle = pi/400
		self.RotAxis = (5, 5, -5)
		
	# makeGenericSpacecraft::
	def animateBodyRotation(self):
		# I used to set the rotation using the origin parameter, but the end result would send the
		# spacecraft off its trajectory. So I took it off. FYI, down bellow was the call
		# self.RefOrigin.rotate(angle=self.RotAngle, axis=self.RotAxis, origin=(0,0,0)) #origin=(10*self.length, 10*self.length, 0)) #-sin(alpha), cos(alpha)))
		self.RefOrigin.rotate(angle=self.RotAngle, axis=self.RotAxis) 

	# makeGenericSpacecraft::
	def make_PCPF_referential(self):
		self.RefOrigin = frame()
		self.RefOrigin.visible	= True
		self.PCPF = None

	#def make_PCI_referential(self): #, size, position):
	#	return

	#def setAxisVisibility(self, setTo):
	#	return


# CLASS STARMAN ---------------------------------------------------------------
class starman(makeBody):
	def __init__(self, system, key, color):
		print "starman: CALLED FOR KEY=", key
		makeBody.__init__(self, system, key, color, SPACECRAFT, SPACECRAFT, SMALLBODY_SZ_CORRECTION, None) #system.Sun)

		print "*** FINISHED init starman ***"
		print ""

	def setAxisVisibility(self, setTo):
		pass

	# starman::
	def make_PCPF_referential(self):
		self.RefOrigin = frame()
		self.RefOrigin.visible	= True
		self.PCPF = None

	# starman::
	def makeShape(self):
		#print "====================making FUSELAGE\n"
		makeGenericSpacecraft.makeShape(self)
		#print "Starman: MakeShape-A: self.RefOrigin.pos=", self.RefOrigin.pos
		
		#print "--------------------------now making ROADSTER\n"

		# create tesla
		roadster = self.makeTesla()
		#print "Starman: MakeShape-B: self.RefOrigin.pos=", self.RefOrigin.pos

		roadster.frame = self.RefOrigin

		# place roadster on the top of stage-2
		roadster.pos = (self.FWD_TANK_CENTER_XCOOR+(self.FWD_TANK_RADIUS)*1.14, self.carlength/2, -self.carwidth/2)
		roadster.axis = (-0.3, 1, 0)

		#print "Starman: MakeShape-C: self.RefOrigin.pos=", self.RefOrigin.pos

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
			#print system.objects_data[key]["profile"]
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
			raise ValueError("Could not find spacecraft profile for {key}")
	
	# makeSpacecraft::
	def makeShape(self):
		# call appropriate makeShape method based on required profile
		globals()[self.profile].makeShape(self)


# CLASS COMET -----------------------------------------------------------------
class makeComet(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, COMET, COMET, SMALLBODY_SZ_CORRECTION, None) #system.Sun)

	# makeComet::
	def makeShape(self):
		self.RefOrigin.pos = vector(self.Position[0],self.Position[1],self.Position[2])
		self.BodyGeometry = ellipsoid(	frame=self.RefOrigin, pos=(0,0,0),
									length=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType], make_trail=false)
	# makeComet::
	def setAspect(self, key):
		# we don't need key for comets
		data = materials.loadTGA("./img/comet")
		self.BodyGeometry.material = materials.texture(data=data, mapping="spherical", interpolate=False)

	def setAxisVisibility(self, setTo):
		pass

	# makeComet::
	def initRotation(self):
		self.RotAngle = pi/512
		self.RotAxis = (0,1,1)

	# makeComet::
	def animateBodyRotation(self):
		self.RefOrigin.rotate(angle=self.RotAngle, axis=self.RotAxis)

	# makeComet::
	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		asteroidRandom = {SCALE_OVERSIZED: (randint(10, 20)/10, randint(10, 20)/10, randint(10, 20)/10), SCALE_NORMALIZED: (1,1,1)}

		self.BodyGeometry.length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyGeometry.height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyGeometry.width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

	def getIncrement(self):
		# for comets, due to their sometimes high eccentricity, an increment of 1 deg may not be small enough
		# to insure a smooth curve, hence we need to take smaller increments of 12.5 arcminutes or less in radians
		return pi/(180 * 4)

	# makeComet::
	def make_PCPF_referential(self):
		self.RefOrigin = frame()
		self.RefOrigin.visible	= True
		self.PCPF = None


# CLASS ASTEROID --------------------------------------------------------------
class makeAsteroid(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, BIG_ASTEROID, BIG_ASTEROID, ASTEROID_SZ_CORRECTION, None)

	def setAxisVisibility(self, setTo):
		pass

	# makeAsteroid::
	def initRotation(self):
		self.RotAngle = pi/512
		self.RotAxis = (1,1,1)

	# makeAsteroid::
	def animateBodyRotation(self):
		self.RefOrigin.rotate(angle=self.RotAngle, axis=self.RotAxis)

	def getRealisticSizeCorrectionXX(self):
		return 1e-2/(DIST_FACTOR*5)

	# makeAsteroid::
	def make_PCPF_referential(self):
		self.RefOrigin = frame()
		self.RefOrigin.visible	= True
		self.PCPF = None


# CLASS PHA -------------------------------------------------------------------
class makePha(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, PHA, PHA, SMALLBODY_SZ_CORRECTION, None) #system.Sun)

	def setAxisVisibility(self, setTo):
		pass

	# makePha::
	def makeShape(self):
		asteroidRandom = [(1.5, 2, 1), (1.5, 2, 1)]
		self.RefOrigin.pos = vector(self.Position[0],self.Position[1],self.Position[2])
		self.BodyGeometry = ellipsoid(	frame = self.RefOrigin, pos=(0,0,0),
									length=(self.radiusToShow * asteroidRandom[self.sizeType][0])/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * asteroidRandom[self.sizeType][1])/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * asteroidRandom[self.sizeType][2])/self.SizeCorrection[self.sizeType], make_trail=false)
		if self.JPL_designation == '4179':
			pass
			#print "makePHA:", self.Name,", position=:", self.Position, ", body position=",self.BodyGeometry.pos, "body Origin=", self.RefOrigin.pos

	# makePha::
	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		#asteroidRandom = [(randint(10, 20)/10, randint(10, 20)/10, randint(10, 20)/10), (1,1,1)]
		asteroidRandom = {SCALE_OVERSIZED: (1.5, 2, 1), SCALE_NORMALIZED: (1.5/3.95, 2/3.95, 1/3.95)}

		self.BodyGeometry.length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyGeometry.height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyGeometry.width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

	# makePha::
	def initRotation(self):
		self.RotAngle = pi/48
		self.RotAxis = (1,1,1)

	# makePha::
	def animateBodyRotation(self):
		self.RefOrigin.rotate(angle=self.RotAngle, axis=self.RotAxis) 

	# makePha::
	def make_PCPF_referential(self):
		self.RefOrigin = frame()
		self.RefOrigin.visible	= True
		self.PCPF = None



# CLASS SMALLASTEROID ---------------------------------------------------------
class makeSmallAsteroid(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, SMALL_ASTEROID, SMALL_ASTEROID, SMALLBODY_SZ_CORRECTION, None) #system.Sun)

	def setAxisVisibility(self, setTo):
		pass

	# makeSmallAsteroid::
	def makeShape(self):
		self.RefOrigin.pos = vector(self.Position[0],self.Position[1],self.Position[2])
		self.BodyGeometry = ellipsoid(	frame=self.RefOrigin, pos=(0,0,0),
									length=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType], make_trail=false)

	# makeSmallAsteroid::
	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		asteroidRandom = {SCALE_OVERSIZED: (randint(10, 20)/10, randint(10, 20)/10, randint(10, 20)/10), SCALE_NORMALIZED: (1,1,1)}
		self.BodyGeometry.length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyGeometry.height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyGeometry.width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

	# makeSmallAsteroid::
	def initRotation(self):
		self.RotAngle = pi/512

	# makeSmallAsteroid::
	def animateBodyRotation(self):
		self.RefOrigin.rotate(angle=self.RotAngle, axis=self.RotAxis)

	# smallAsteroid::
	def make_PCI_referential(self):
		pass
		#self.RefOrigin = frame()
		#self.RefOrigin.visible	= True

	def setRotAxis(self):
		self.RotAxis = (1,1,1)

	# makeSmallAsteroid::
	def make_PCPF_referential(self):
		self.RefOrigin = frame()
		self.RefOrigin.visible	= True
		self.PCPF = None


# CLASS DWARFPLANET -----------------------------------------------------------
class makeDwarfPlanet(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, DWARFPLANET, DWARFPLANET, DWARFPLANET_SZ_CORRECTION, None) #system.Sun)

	def setAxisVisibility(self, setTo):
		pass

	# makeDwardPlanet::
	def makeShape(self):
		makeBody.makeShape(self)

	def getRealisticSizeCorrectionXX(self):
		#DWARFPLANET_SZ_CORRECTION = 1e-2/(DIST_FACTOR*5)
		return 1e-2/(DIST_FACTOR*5)

	# makeDwarfPlanet::
	def make_PCPF_referential(self):
		self.RefOrigin = frame()
		self.RefOrigin.visible	= True
		self.PCPF = None


# CLASS TRANSNEPTUNIAN --------------------------------------------------------
class makeTransNeptunian(makeBody):
	def __init__(self, system, key, color):
		makeBody.__init__(self, system, key, color, TRANS_NEPT, TRANS_NEPT, SMALLBODY_SZ_CORRECTION, None) #system.Sun)

	def setAxisVisibility(self, setTo):
		pass

	# makeTransNeptunian::
	def makeShape(self):
		self.RefOrigin.pos = vector(self.Position[0],self.Position[1],self.Position[2])
		self.BodyGeometry = ellipsoid(	frame=self.RefOrigin, pos=(0,0,0),
									length=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									height=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType],
									width=(self.radiusToShow * randint(10, 20)/10)/self.SizeCorrection[self.sizeType], make_trail=false)

	# makeTransNeptunian::
	def toggleSize(self, realisticSize):
		x = SCALE_NORMALIZED if realisticSize == True else SCALE_OVERSIZED
		if x == self.sizeType:
			return
		else:
			self.sizeType = x

		asteroidRandom = [(randint(10, 20)/10, randint(10, 20)/10, randint(10, 20)/10), (1,1,1)]
		self.BodyGeometry.length = self.radiusToShow * asteroidRandom[self.sizeType][0] / self.SizeCorrection[self.sizeType]
		self.BodyGeometry.height = self.radiusToShow * asteroidRandom[self.sizeType][1] / self.SizeCorrection[self.sizeType]
		self.BodyGeometry.width  = self.radiusToShow * asteroidRandom[self.sizeType][2] / self.SizeCorrection[self.sizeType]

	# makeTransNeptunian::
	def initRotation(self):
		self.RotAngle = pi/512
		self.RotAxis = (0,1,1)

	# makeTransNeptunian::
	def animateBodyRotation(self):
#		self.RefOrigin.pos = vector(self.Position[0],self.Position[1],self.Position[2])
#		self.BodyGeometry.rotate(angle=self.RotAngle, axis=self.RotAxis, origin=(0,0,0)) #-sin(alpha), cos(alpha)))
		self.RefOrigin.rotate(angle=self.RotAngle, axis=self.RotAxis) #, origin=(0,0,0)) #-sin(alpha), cos(alpha)))

	# makeTransNeptunian::
	def make_PCPF_referential(self):
		self.RefOrigin = frame()
		self.RefOrigin.visible	= True
		self.PCPF = None


#
# various functions
#

def getSigmoid(distance, correction):
	#print "peri=", distance,", correction=", correction
	if distance > 0:
		sigmoid = 1/(1+exp(-MAX_P_D/distance))
		return correction * sigmoid
	return correction

# independent functions
def getPerihelion(semimajor, eccentricity):
	# knowing the semi major, the formulat is: a(1-e)
	return semimajor * (1 - eccentricity)

def getSemiMajor(perihelion, eccentricity):
	# knowing the perihelion, the formula is given by:  a(1-e)
	return perihelion /(1 - eccentricity)

# independant
def getSemiMinor(semimajor, eccentricity):
	# knowing the semi-major, the formula is given by: a.sqrt(1-e^2)
	return semimajor * sqrt(1 - eccentricity**2)

def getSemiLatusRectum(semimajor, eccentricity):
	# knowing the semi-major, the formula is given by: a.(1-e^2)
	return semimajor * (1 - eccentricity**2)

def getAphelion(semimajor, eccentricity):
	# knowing the semi major, the formulat is: a(1+e)
	return semimajor * (1 + eccentricity)

def getOrbitalPeriod(semimajor):
	# knowing the semi major, the formulat is T = 2 pi sqrt(a^3/Mu)
	return 2*math.pi*sqrt((semimajor**3)/Mu)

def glbRefresh(solarSystem, animationInProgress):
	solarSystem.refresh(animationInProgress)
	for body in solarSystem.bodies:
		body.refresh()

def hideBelt(beltname):
	beltname.BodyGeometry.visible = false
	beltname.Labels[0].visible = false

def showBelt(beltname):
	beltname.BodyGeometry.visible = true
	beltname.Labels[0].visible = true

def getColor():
	return { 0: Color.white, 1: Color.red, 2: Color.orange, 3: Color.yellow, 4: Color.cyan, 5: Color.magenta, 6: Color.green}[randint(0,6)]

def solveKepler(M, e, depth, precision = 1.e-8):

	# Calculates Eccentric Anomaly (E) given the mean anomaly (M), the depth and the
	# precision required using an iterative method. If the precision has been reached
	# within the maximum iteration depth, returns (True, E) or (False, E) otherwise

	M = deg2rad(M)
	threshold = deg2rad(precision)
	E0 = M
	it = 0
	while True:
		E1 = M + e*sin(E0)
		if abs(E1-E0) < threshold:
			return True, rad2deg(E0)
		it = it + 1
		if it > depth:
			return False, rad2deg(E0)
		E0 = E1

def bessel_E(M, e, depth):

	# Alternate method to solve the kepler equation:
	# calculates Eccentric Anomaly (E) given the mean anomaly (M) 
	# and the depth of the Bessel first kind functions

    return (M + sum(2.0 / n * sp.jv(n, n * e) * np.sin(n * M)
                    for n in range(1, depth, 1)))

def toRange (angle):
	n = angle % 360
	if n < 0:
		n = n + 360
	return n


def getTrueAnomalyAndRadius(E, e, a):

	# Calculates the true anomaly (NU) and Radius given the Eccentric
	# Anomaly (E), the orbit eccentricity and the semi-major axis

	ta = 2 * atan(sqrt((1+e)/(1-e)) * tan(E/2))
	R = a * (1 - e*cos(E))
	if ta < 0:
		ta = ta + 2*pi
	return ta, R


def loadBodies(SolarSystem, type, filename, maxentries = 0):

	# load orbital parameters stored in JSON file

	fo  = open(filename, "r")
	allObj = json.loads(fo.read())

	maxentries = 1000 if maxentries == 0 else maxentries
	for obj in allObj:
		for key in obj:
			JPL_designation = obj[key]["jpl_designation"].lower()
			SolarSystem.objects_data[JPL_designation] = {
				"profile": "{ \"look\":\""+obj[key]["profile"]["look"]+"\", \"engine\":"+str(obj[key]["profile"]["engine"])+", \"length\":"+str(obj[key]["profile"]["length"])+", \"COPV\":"+str(obj[key]["profile"]["COPV"])+"}" if "profile" in obj[key] else "",
				"material": 1 if obj[key]["tga_name"] != "" else 0,
				"name": str(obj[key]["name"]),
				"iau_name": str(obj[key]["iau_name"]),
				"jpl_designation": str(obj[key]["jpl_designation"]),
				"mass": (obj[key]["mu"]/G)*1.e+9, # convert km3 to m3
				"radius": obj[key]["diameter"]/2, 
				"distance_to_periapsis": obj[key]["distance_to_periapsis"] * AU,
				"eccentricity_EC": obj[key]["eccentricity_EC"],
				"revolution_PR": obj[key]["revolution_PR"],
				"orbital_inclination_IN": 	obj[key]["orbital_inclination_IN"],
				"longitude_of_ascendingnode_OM":obj[key]["longitude_of_ascendingnode_OM"],
				"argument_of_periapsis_w": obj[key]["argument_of_periapsis_w"],
				"longitude_of_periapsis_W": obj[key]["longitude_of_ascendingnode_OM"] + obj[key]["argument_of_periapsis_w"],
				"jd_time_of_periapsis_passage_Tp": obj[key]["jd_time_of_periapsis_passage_Tp"],
				"mean_motion_N": obj[key]["mean_motion_N"],
				"mean_anomaly_MA": obj[key]["mean_anomaly_MA"],
				"epochJD": obj[key]["epochJD"],
				"earth_moid": obj[key]["earth_moid"] * AU,
				"orbit_class": str(obj[key]["orbit_class"]),
				"absolute_mag": obj[key]["absolute_mag"],
				"axial_tilt": obj[key]["axial_tilt"], # in deg
				"tga_name": str(obj[key]["tga_name"])
			}
			
			# build body using proper body type
			from moons import makePlanetMoon

			body = {SPACECRAFT: 	makeSpacecraft,
					COMET: 			makeComet,
					BIG_ASTEROID: 	makeAsteroid,
					PHA:			makePha,
					TRANS_NEPT:		makeTransNeptunian,
					SATELLITE:		makePlanetMoon,
					MOON:			makePlanetMoon,
					SMALL_ASTEROID:	makeSmallAsteroid,
					}[type](SolarSystem, JPL_designation, getColor())

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
					"distance_to_periapsis": float(token[JPL_OE_q]) * AU,
					"eccentricity_EC": float(token[JPL_OE_e]),
					"revolution_PR": float(token[JPL_OE_Pd]),
					"orbital_inclination_IN": 	float(token[JPL_OE_i]),
					"longitude_of_ascendingnode_OM":float(token[JPL_OE_N]),
					"argument_of_periapsis_w": float(token[JPL_OE_w]),
					"longitude_of_periapsis_W":float(token[JPL_OE_N])+float(token[JPL_OE_w]),
					"jd_time_of_periapsis_passage_Tp":float(token[JPL_OE_tp_JD]),
					"mean_motion_N": float(token[JPL_OE_n]) if token[JPL_OE_n] else 0,
					"mean_anomaly_MA": float(token[JPL_OE_M]) if token[JPL_OE_M] else 0,
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
						SATELLITE:		makePlanetMoon,
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
	return EPOCH_2000_JD

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

def makeJulianDate(utc, delta):
    # Fliegel / Van Flandern Formula - delta is fractional days
    Y = utc.year
    M = utc.month
    D = utc.day

    # Fraction of the day
    frac = (utc.hour + (utc.minute + utc.second/60.0)/60.0) / 24.0

    # Correct floor divisions
    A = (14 - M) // 12
    Yp = Y + 4800 - A
    Mp = M + 12*A - 3

    JD = D + ((153*Mp + 2)//5) + 365*Yp + Yp//4 - Yp//100 + Yp//400 - 32045

    return JD + frac + delta

def datetime_to_julian_date(dt, day_increment=0.0):
	"""
	Takes a datetime and day_increment as a fraction of day, and
	converts it to a julian date
	"""
	# Normalize to UTC
	if dt.tzinfo is None:
		dt_utc = dt.replace(tzinfo=pytz.utc)
	else:
		dt_utc = dt.astimezone(pytz.utc)

	year   = dt_utc.year
	month  = dt_utc.month
	day    = dt_utc.day
	hour   = dt_utc.hour
	minute = dt_utc.minute
	second = dt_utc.second + dt_utc.microsecond / 1e6

	# Fraction of the day
	day_fraction = (hour + minute/60.0 + second/3600.0) / 24.0

	# Shift Jan/Feb into previous year
	if month <= 2:
		year  -= 1
		month += 12

	A = year // 100
	B = 2 - A + (A // 4)

	jd_day = (int(365.25 * (year + 4716)) +
			int(30.6001 * (month + 1)) +
			day + B - 1524.5)

	# Add fractional day increment
	return jd_day + day_fraction + day_increment    


def makeJulianDateOffset(utc, delta=0.0):
	"""
	returns the offset in days + fraction of day since J2000

	Fliegel / Van Flandern Formula - "delta" is a float to accept fractional 
	days (added minutes and seconds)

	Note that the // operator means "__floordiv__", where the result is rounded 
	to the lower closest integer (it 1.689 -> 1). For the leftOver though, we 
	need the exact value in float
	"""

	Y = utc.year
	M = utc.month
	D = utc.day

	# Fraction of the day
	frac = (utc.hour + utc.minute/60.0 + utc.second/3600.0) / 24.0

	# Shift Jan/Feb into previous year
	if M <= 2:
		Y -= 1
		M += 12

	A = Y // 100
	B = 2 - A + (A // 4)

	JD = int(365.25 * (Y + 4716)) \
		+ int(30.6001 * (M + 1)) \
		+ D + B - 1524.5

	return JD + frac + delta - EPOCH_2000_JD # the # of days since J2000

"""

def makeJulianDateALTernate2(utc, delta):
	# Fliegel / Van Flandern Formula - "delta" is in days (added minutes and seconds)
	JL = delta + 367*utc.year - (7*(utc.year + ((utc.month+9)/12)))/4 + (275*utc.month)/9 + utc.day + 1721013.5 + (((utc.second/60) + utc.minute)/60 +utc.hour)/24

	#print "makeJulian------------", JL
	return JL

def makeJulianDate2(utc, delta):
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
"""

def julian(d,m,y):
	temp1 = m - 14
	temp2 = d - 32075 + 1461 * (y + 4800 + int(temp1 / 12.0)) / 4
	temp3 = int(temp1 / 12.0) * 12
	temp4 = ((y + 4900 + int(temp1 / 12.0)) / 100)
	return temp2 + 367 * (m - 2 - temp3) / 12 - 3 * temp4 / 4

def daysSinceJ2000UTC(locationInfo, delta = 0):
	# will compute the number of days since J2000 UTC
	utc = locationInfo.getUTCDateTime()
	return makeJulianDateOffset(utc, delta)

def daysSinceEpochJD(julianDate, locationInfo):
	# will compute the number of days since a particular julian date
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

# for earth focusing only: in order to show the nightmap on the dark side, we need
# to update the opacity of the nightmap based on the camera position relative to 
# the earth current exposure to the sun

def update_earth_lighting(earth_day, earth_night, sun_pos, earth_pos, cam_pos):
    # Unit vectors
    sun_dir = norm(sun_pos - earth_pos)
    cam_dir = norm(cam_pos - earth_pos)

    # Earth’s local +Z axis (already oriented by RA/Dec/W)
    n = norm(earth_day.axis)

    # Physical night factor
    d_sun = max(0.0, -dot(n, sun_dir))

    # Camera-facing-night factor
    d_cam = max(0.0, -dot(n, cam_dir))

    # Final opacity
    earth_night.opacity = d_sun * d_cam

"""
North Pole direction functions
"""

def julian_date_manual(year, month, day, hour=0, minute=0, second=0):
    
    # Calculates the Julian Date for a given Gregorian calendar date and time.
    # This function avoids the 'datetime' library as per constraint.
    # J2000.0 epoch is JD 2451545.0 TDB.

    # Algorithm from Fliegel and Van Flandern (1968)
    # Simplified for positive Julian Dates (after 4713 BC)

    if month <= 2:
        year -= 1
        month += 12

    A = np.floor(year / 100)
    B = 2 - A + np.floor(A / 4)

    JD = np.floor(365.25 * (year + 4716)) + \
         np.floor(30.6001 * (month + 1)) + \
         day + B - 1524.5

    # Add fractional part for time
    JD += (hour + minute / 60 + second / 3600) / 24.0
    return JD


def calculate_T_from_jd(jd):

    # Calculates T, the interval in Julian centuries (36525 days) from J2000.0.
    # J2000.0 epoch Julian Date (JD) = 2451545.0
    
    return (jd - 2451545.0) / 36525.0


def calculate_d_from_jd(jd):
    
    # Calculates d, the interval in days from J2000.0.
    # J2000.0 epoch Julian Date (JD) = 2451545.0

    return jd - 2451545.0


def equatorial_to_cartesian_vector(ra_deg, dec_deg):

    # Converts Right Ascension (RA) and Declination (Dec) to a Cartesian
    # unit vector [X, Y, Z] in the J2000 equatorial coordinate system (ICRF).

    ra_rad = np.radians(ra_deg)
    dec_rad = np.radians(dec_deg)
    x = np.cos(dec_rad) * np.cos(ra_rad)
    y = np.cos(dec_rad) * np.sin(ra_rad)
    z = np.sin(dec_rad)
    magnitude = np.sqrt(x**2 + y**2 + z**2)
    if magnitude == 0:
        return np.array([0.0, 0.0, 0.0]) # Return numpy array
    return np.array([x / magnitude, y / magnitude, z / magnitude]) # Return numpy array


def get_planet_pole_parameters(planet_name, T, d):

    # Retrieves the time-dependent pole parameters (alpha0, delta0) for a given planet.
    # These coefficients are based on the IAU 2009 WGCCRE report (Archinal et al. 2010),
    # including periodic terms for Jupiter.
    # 
    # Args:
    #    planet_name (str): The name of the planet (e.g., "Earth", "Mars").
    #    T (float): Julian centuries from J2000.0.
    #    d (float): Days from J2000.0.
    #
    # Returns:
    #    tuple: (alpha0_deg, delta0_deg) in degrees, representing the pole in J2000 
    #           equatorial coordinates.
    # -----------------------------------------------------------------------------
    # Coefficients (alpha0_J2000, alpha0_dot, delta0_J2000, delta0_dot)
    # alpha0_dot and delta0_dot are per Julian century
    # Periodic terms are added where applicable.
    # Data from IAU 2009 WGCCRE Report (Archinal et al. 2010), Table 2.
    # Note: For Earth, these simplified formulas are for comparison, IERS data is more precise.

    planet_data = {
        "Sun":       (286.13,     0.0,     63.87,     0.0),
        "Mercury":   (281.0097,  -0.0328,  61.4143,  -0.0049),
        "Venus":     (272.76,     0.0,     67.16,     0.0), # Retrograde rotation, but pole is defined by north of invariable plane
        "Earth":     (0.00,      -0.641,   90.00,    -0.557),
        "Mars":      (317.68143, -0.1061,  52.88650, -0.0609),
        # Jupiter includes periodic terms
        "Jupiter":   (268.056595,-0.006499,64.495303, 0.008391),
        "Saturn":    (40.589,    -0.036,   83.537,   -0.004),
        "Uranus":    (257.311,    0.0,    -15.175,    0.0), # Retrograde rotation, but pole is defined by north of invariable plane
        "Neptune":   (299.36,     0.70,    43.46,     0.0),
        # Pluto's pole model in IAU 2009 is linear, no periodic terms listed.
        "Pluto":     (313.02,    -0.001,   9.09,      0.005)
    }

    if planet_name not in planet_data:
        raise ValueError("Data for {planet_name} not available.")

    alpha0_j2000, alpha0_dot, delta0_j2000, delta0_dot = planet_data[planet_name]

    alpha0 = alpha0_j2000 + alpha0_dot * T
    delta0 = delta0_j2000 + delta0_dot * T

    # additional periodic terms will be used to adjust the current values 
    # of RA (alpha0) and DECL (delta0) for Jupiter and Neptune by overwriting 
    # the " AdjustNPforPeriodicTerms" method of the makeBody class, which by
    # default leaves RA and DECL unchanged. 

    return alpha0, delta0

def get_planet_prime_meridian_W(planet, T, d):
    
    # Retrieves the time-dependent prime meridian angle (W) for a given planet.
    # These coefficients are based on the IAU 2009 WGCCRE report (Archinal et al. 2010).
    # W is measured eastward along the planet's equator from the ascending node
    # on the Earth's mean equator of J2000.0.
    
    # W = W0 + W_dot * d
    # W0 is the angle at J2000.0, W_dot is the daily rate.
    # d is days from J2000.0.

    # Simplified to linear terms and major periodic terms where applicable.
    # For full precision, more periodic terms for some planets would be needed.
    
    prime_meridian_data = {
        "Sun":       (84.176,   14.1844000),
        "Mercury":   (329.5469,  6.1385025),
        "Venus":     (160.20,   -1.4813688), # Retrograde rotation, W decreases
        "Earth":     (190.147, 360.9856235), # Earth's prime meridian (Greenwich)
        "Mars":      (176.630, 350.89198226),
        "Jupiter":   (284.95,  870.536),  	 # W for Jupiter is often given as alpha0, but here we use the specific W formula
        "Saturn":    (38.90,   810.7939024),
        "Uranus":    (203.81, -501.1600928), # Retrograde rotation, but W increases
        "Neptune":   (253.18,  536.3128492),
        "Pluto":     (313.02,   56.3625225)
    }

    if planet.Name not in prime_meridian_data:
        raise ValueError("Prime meridian data for {planet.Name} not available.")

    W0, W_dot = prime_meridian_data[planet.Name]

    # caluclate W @ present time
    W = W0 + W_dot * d

    # ... and add possible adjustment, depending on the planet
    W = W + planet.AdjustPMforPeriodicTerms(T, d)

    # Normalize W (ensure its value is within 0-360 degrees)
    W = W % 360.0
    if W < 0:
        W += 360.0

    return W


def rotation_matrix_x(angle_rad):
    """
    Creates a 3x3 rotation matrix for rotation around the X-axis 
    to convert Equatorial coordinates to Ecliptic coordinates.
    (we rotate around the X axis by an angle corresponding to 
    the inclination of the equatorial plane on the ecliptic, 
    which is the earth inclination)
    """
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)
    return np.array([
        [1.0, 0.0, 0.0],
        [0.0, cos_a, -sin_a],
        [0.0, sin_a, cos_a]
    ])

def apply_rotation(vector, matrix):
    """
    Applies a 3x3 rotation matrix to a 3D vector.
    """
    return np.dot(matrix, vector)


"""
# --- Example Usage ---
# Define a specific date for calculation
# Using a fixed date instead of datetime.now() due to the "no external libraries except numpy" constraint
calculation_year = 2025
calculation_month = 7
calculation_day = 22
calculation_hour = 8
calculation_minute = 42
calculation_second = 15

# Get all planet data
all_planet_data = get_all_planet_data_ecliptic_with_perturbations(
    calculation_year, calculation_month, calculation_day,
    calculation_hour, calculation_minute, calculation_second
)

# Format and print the table
#current_date_str = f"{calculation_year}-{calculation_month:02d}-{calculation_day:02d} {calculation_hour:02d}:{calculation_minute:02d}:{calculation_second:02d} UTC"
current_date_str = "{calculation_year}-{calculation_month:02d}-{calculation_day:02d} {calculation_hour:02d}:{calculation_minute:02d}:{calculation_second:02d} UTC"

print("Calculations for: {current_date_str}")
print("| Planet  | X (J2000 Ecliptic) | Y (J2000 Ecliptic) | Z (J2000 Ecliptic) | W (Prime Meridian Angle, deg) | $\Omega$ (Ecliptic Ascending Node, deg) |")
print("|---------|--------------------|--------------------|--------------------|-------------------------------|------------------------------------------|")

for planet, data in all_planet_data.items():
    if isinstance(data, dict):
        pole_vec = data["pole_vector_ecl"]
        W_angle = data["W_angle"]
        Omega_angle = data["Omega_angle"]
#        print(f"| {planet.ljust(7)} | {pole_vec[0]:<18.6f} | {pole_vec[1]:<18.6f} | {pole_vec[2]:<18.6f} | {W_angle:<29.4f} | {Omega_angle:<40.3f} |")
        print("| {:7} | {:<18.6f} | {:<18.6f} | {:<18.6f} | {:<29.4f} | {:<40.3f} |".
        format(planet, pole_vec[0], pole_vec[1], pole_vec[2], W_angle, Omega_angle))
    else:
        print("| {planet.ljust(7)} | {data.ljust(18)} | {'':<18} | {'':<18} | {'':<29} | {'':<40} |")


"""


'''
Good values:
Body	North Pole Vector (J2000 Ecliptic Cartesian)	Tilt Angle (degrees)
Sun		(0.0130, 0.0468, 0.9988)						7.25
Mercury	(0.0000, -0.0039, 1.0000)						0.01
Venus	(0.0543, 0.0000, -0.9985)						177.36
Earth	(0.0000, 0.3978, 0.9175)						23.44
Mars	(0.0613, 0.2598, 0.9639)						25.19
Jupiter	(-0.0381, 0.0090, 0.9992)						3.13
Saturn	(-0.0084, 0.0560, 0.9984)						26.73
Uranus	(0.7570, -0.6385, -0.1294)						97.77
Neptune	(-0.0706, -0.2831, 0.9566)						28.32
Pluto	(0.5366, -0.7602, 0.3664)						122.53 (or 57.47 to its orbit)

'''

"""
NEW NEW. to integrate with the rest ....

This is the code that calculates the Sun's coordinates in the J2000 ecliptic 
referential. The key principle is that the Sun's position is the negative of the solar 
system's barycenter position, if the barycenter is calculated with the Sun as the origin.

I've modified the previous script to create a function that directly deduces the Sun's 
position based on this principle. The example now calculates the barycenter of all bodies 
(including the Sun, which is initially at (0,0,0)) and then returns the negative of that 
value as the Sun's coordinate in the barycentric J2000 frame.

This script provides a function that explicitly deduces the Sun's coordinates and also 
returns the barycenter's coordinates as a reference. This is a common method used in 
celestial mechanics to shift from a heliocentric (Sun-centered) frame to a barycentric 
(center of mass) frame.
"""

def deduce_sun_position(celestial_bodies):
    """
    Deduces the Sun's coordinates in the J2000 Ecliptic referential (where the
    barycenter is the origin) based on the positions and masses of all bodies.

    The method works by calculating the barycenter of the system, assuming
    the Sun's initial position is the origin (0, 0, 0). The resulting barycenter
    vector points from the Sun to the system's center of mass.
    Therefore, the Sun's position relative to the barycenter is simply the
    negative of this barycenter vector.

    Args:
        celestial_bodies (list of dict): A list where each dictionary
            represents a celestial body and must contain:
            - 'mass' (float): The mass of the body.
            - 'position' (list or np.array): A list/array of [x, y, z] coordinates.
            - 'name' (str): The name of the body (used to find the Sun's position).

    Returns:
        tuple: A tuple containing two items:
            - np.array: A numpy array of the [x, y, z] coordinates of the Sun
              in the J2000 Ecliptic referential.
            - np.array: A numpy array of the [x, y, z] coordinates of the barycenter,
              which will be approximately [0, 0, 0] in this frame.
    """
    total_mass = 0
    weighted_position_sum = np.zeros(3)

    # Sum the masses and the mass-weighted positions
    for body in celestial_bodies:
        mass = body['mass']
        position = np.array(body['position'])

        # Accumulate total mass
        total_mass += mass
        
        # Accumulate the sum of (mass * position) for each coordinate
        weighted_position_sum += mass * position

    # Calculate the barycenter assuming the Sun is at the origin.
    # This vector represents the displacement of the barycenter from the Sun.
    barycenter_from_sun = weighted_position_sum / total_mass
    
    # In the J2000 Ecliptic referential (origin = barycenter), the Sun's position
    # is the negative of the barycenter's position relative to the Sun.
    sun_position_j2000 = -barycenter_from_sun
    
    # The barycenter's position in this referential is the origin, [0,0,0].
    barycenter_position_j2000 = np.zeros(3)
    
    return sun_position_j2000, barycenter_position_j2000

# Example usage:
# The masses are given in kilograms.
# The positions are in a hypothetical heliocentric coordinate system
# (e.g., millions of kilometers) where the Sun's center is at (0,0,0).
solar_system_bodies = [
    # Data is simplified for demonstration purposes.
    {'name': 'Sun',     'mass': 1.989e30, 'position': np.array([0, 0, 0])},
    {'name': 'Mercury', 'mass': 3.301e23, 'position': np.array([57.9e6, 0, 0])},
    {'name': 'Venus',   'mass': 4.867e24, 'position': np.array([108.2e6, 0, 0])},
    {'name': 'Earth',   'mass': 5.972e24, 'position': np.array([149.6e6, 0, 0])},
    {'name': 'Mars',    'mass': 6.417e23, 'position': np.array([227.9e6, 0, 0])},
    {'name': 'Jupiter', 'mass': 1.898e27, 'position': np.array([778.5e6, 0, 0])},
    {'name': 'Saturn',  'mass': 5.683e26, 'position': np.array([1433.5e6, 0, 0])},
    {'name': 'Uranus',  'mass': 8.681e25, 'position': np.array([2872.5e6, 0, 0])},
    {'name': 'Neptune', 'mass': 1.024e26, 'position': np.array([4495.1e6, 0, 0])},
]

def getJ2000EclipticSunCoordinates():
	# Deduce the Sun's position in the barycentric frame
	sun_pos_j2000, barycenter_pos_j2000 = deduce_sun_position(solar_system_bodies)

	print("The Sun's coordinates in the J2000 Ecliptic referential are: ",sun_pos_j2000)
	print("The barycenter's coordinates in this referential are: ",barycenter_pos_j2000)


def get_moon_position_preciseXXXX(dt):
    """
    Calculates the more precise geocentric Cartesian coordinates (x, y, z)
    of the Moon for a given datetime object.

    This function uses a more detailed astronomical model, including
    more terms for the Moon's orbital elements. The output is in a
    geocentric ecliptic reference frame (can be returned also as coordinates
    in the geocentric equatorial reference frame).

    Args:
        dt (datetime): The date and time for which to calculate the position.

    Returns:
        tuple: A tuple (x, y, z) of the Moon's Cartesian coordinates in kilometers.
    """
    # === Step 1: Calculate Julian Day and Epoch Time ===


    current_utc_time = dt.datetime.utcnow()
    formatted_utc = current_utc_time.strftime("%Y-%m-%d %H:%M:%S UTC")

    print (formatted_utc)

    year, month = current_utc_time.year, current_utc_time.month
    day = current_utc_time.day + current_utc_time.hour / 24.0 + current_utc_time.minute / (24.0 * 60.0) + current_utc_time.second / (24.0 * 3600.0)
    #===========


   # year = dt.year
   # month = dt.month
   # day = dt.day + dt.hour / 24.0 + dt.minute / (24.0 * 60.0) + dt.second / (24.0 * 3600.0)

    if month <= 2:
        year -= 1
        month += 12

    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5

    # Time since J2000.0 epoch in Julian centuries
    t = (jd - 2451545.0) / 36525.0

    # === Step 2: More Precise Lunar Orbital Calculations (Simplified Ecliptic Coordinates) ===
    # Using more terms for a more accurate result.
    
    # Mean longitude of the Moon (degrees)
    L0 = 218.3164477 + 481267.88123421 * t - 0.00157864 * t**2 + t**3 / 189474.0 - t**4 / 189474000.0
    L0 = math.fmod(L0, 360)

    # Mean anomaly of the Moon (degrees)
    M = 134.9634114 + 477198.86763 * t + 0.008997 * t**2 + t**3 / 69699.0 - t**4 / 14712000.0
    M = math.fmod(M, 360)

    # Elongation of the Moon from the Sun (degrees)
    D = 297.8501921 + 445267.11152 * t - 0.00163004 * t**2 + t**3 / 545860.0 - t**4 / 153300000.0
    D = math.fmod(D, 360)

    # Mean anomaly of the Sun (degrees)
    M_sun = 357.5291092 + 35999.05029 * t - 0.0001536 * t**2 + t**3 / 24490000.0
    M_sun = math.fmod(M_sun, 360)

    # Longitude of the Moon's ascending node (degrees)
    F = 93.2720993 + 483202.01753 * t - 0.00368257 * t**2 + t**3 / 327270.0 + t**4 / 4300000.0
    F = math.fmod(F, 360)
    
    # Arguments in radians for trigonometric functions
    M_rad = math.radians(M)
    M_sun_rad = math.radians(M_sun)
    D_rad = math.radians(D)
    F_rad = math.radians(F)

    # Ecliptic longitude terms (degrees)
    ecliptic_longitude = L0 + (6.289 * math.sin(M_rad)) + (1.274 * math.sin(2 * D_rad - M_rad)) + \
                         (0.658 * math.sin(2 * D_rad)) + (0.214 * math.sin(2 * M_rad))
    ecliptic_longitude = math.fmod(ecliptic_longitude, 360)
    if ecliptic_longitude < 0:
        ecliptic_longitude += 360

    # Ecliptic latitude terms (degrees)
    ecliptic_latitude = (5.128 * math.sin(F_rad)) + (0.280 * math.sin(M_rad + F_rad))
    
    # Distance terms (kilometers)
    distance_km = 384400.0 * (1 - 0.0549 * math.cos(M_rad) - 0.00412 * math.cos(2*M_rad) - 0.00282 * math.cos(2*D_rad-M_rad))
    
    # === Step 3: Convert from Ecliptic to Cartesian Equatorial Coordinates ===
    lambda_rad = math.radians(ecliptic_longitude)
    beta_rad = math.radians(ecliptic_latitude)
    
    # Obliquity of the Ecliptic (tilt of the Earth's axis) in degrees
    epsilon_degrees = 23.439 - 0.013 * t
    epsilon_rad = math.radians(epsilon_degrees)

    # Calculate x, y, z in geocentric ecliptic coordinates
    x_ecliptic = distance_km * math.cos(beta_rad) * math.cos(lambda_rad)
    y_ecliptic = distance_km * math.cos(beta_rad) * math.sin(lambda_rad)
    z_ecliptic = distance_km * math.sin(beta_rad)

    # Convert from ecliptic to equatorial Cartesian coordinates using the obliquity
    
    x_eq = x_ecliptic
    y_eq = y_ecliptic * math.cos(epsilon_rad) - z_ecliptic * math.sin(epsilon_rad)
    z_eq = y_ecliptic * math.sin(epsilon_rad) + z_ecliptic * math.cos(epsilon_rad)
	
    return x_eq, y_eq, z_eq
	
    #return x_ecliptic, y_ecliptic, z_ecliptic
