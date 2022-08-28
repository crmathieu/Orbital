from visual import *
from rate_func import *
#import rate_func
from utils import deg2rad, rad2deg, getAngleBetweenVectors, getOrthogonalVector, getVectorOrthogonalToPlane
from objects import simpleArrow
from planetsdata import EARTH_NAME
from video import * 

# All camera movements occur using a focal point centered on the
# current object
#
# in this module, fake mouse events are generated to induce camera movements.
# Then, the vpython "report_mouse_state" method is called to update the view 
# based on mouse/keyboard events provided as parameters
#
# Examples:
# zoom -> 	both right and left buttons must be held down and the zoom
# 			velocity is a function of how many pixels the virtual mouse
#			is moving. The mouse motion is given by the difference between
#			lastx, lasty (the last position of the mouse) and x, y (its
# 			updated position)
#
# rotation -> the right button must be held down. If lastx != x and
#  			lasty == y, a rotation motion is created. Its direction depends
# 			on positive of negative changes:
# 				lastx > x	-> rotation towards the left
# 				lastx < x 	-> rotation towards the right 
# 			The rotation can be combined with a vertical panoramic movement 
#			if "y" changes as well.
#				lasty > y 	-> pano UP
#				lasty < y	-> pano DWN
# 			The intensity of the rotation and pano is given by the amount of 
# 			change happening between lastx, lasty (the last position of the mouse) 
# 			and x, y (its current position)



class camera3D:

	ROT_HOR = 1
	ROT_VER = 2
	ROT_UP = 4
	ROT_DWN = 8
	ROT_LEFT = 16
	ROT_RIGHT = 32

	ROT_CLKW = 64
	ROT_CCLKW = 128

	ROT_DIAG_RIGHT_DWN = ROT_HOR|ROT_RIGHT|ROT_VER|ROT_DWN
	ROT_DIAG_LEFT_DWN = ROT_HOR|ROT_LEFT|ROT_VER|ROT_DWN
	ROT_DIAG_LEFT_UP = ROT_HOR|ROT_LEFT|ROT_VER|ROT_UP
	ROT_DIAG_RIGHT_UP = ROT_HOR|ROT_RIGHT|ROT_VER|ROT_UP

	ZOOM_IN = 1
	ZOOM_OUT = 2

	LASTX_OFF = 0
	LASTY_OFF = 1
	X_OFF = 2
	Y_OFF = 3

	VELOCITY_MAX = 3.0
	VELOCITY_MIN = 0.1

	def __init__(self, solarSystem):
		self.view = solarSystem.Scene
		self.SolarSystem = solarSystem
		self.MAX_ZOOM_VELOCITY = 100
		self.transitionVelocityFactor = 1.0  # normal speed. speed can go as slow as 1/100 and as fast as 4 times the normal speed
		
		self.view.lights = []
		self.view.forward = vector(2, 0, -1)
		self.view.fov = deg2rad(40) 
		
		self.view.userspin = True
		self.view.userzoom = True
		self.view.autoscale = True
		self.view.autocenter = False
		self.view.up = (0,0,1)

	def setEarthLocations(self):
		self.Loc = self.SolarSystem.EarthRef.PlanetWidgets.Loc

	def getDirection(self):
		return self.view.forward
		
	def noTick(self):
		left, right, middle = True, True, False
		shift, ctrl, alt, cmd = False, False, False, False
		x, y = 500, 500
		lastx, lasty = 500, 500
		self.view.report_mouse_state([left, right, middle],
		lastx, lasty, x, y,
		[shift, ctrl, alt, cmd])

	def oneTickCameraZoom(self, forward = True):
		# for camera zoom motion, both right and left mouse buttons must be held down
		left, right, middle = True, True, False
		shift, ctrl, alt, cmd = False, False, False, False
		x, y = 499, 499
		lastx, lasty = 500, 500
		if not forward:
			x, y = 500, 500
			lastx, lasty = 499, 499
		self.view.report_mouse_state([left, right, middle],
		lastx, lasty, x, y,
		[shift, ctrl, alt, cmd])

	def oneTickCameraRotation(self):
		# for camera rotation motion, the right mouse button must be held down
		# y stays constant

		left, right, middle = False, True, False
		shift, ctrl, alt, cmd = False, False, False, False
		x, y = 500, 500
		lastx, lasty = 499, 500

		self.view.report_mouse_state([left, right, middle],
		lastx, lasty, x, y,
		[shift, ctrl, alt, cmd])

	def oneTickCameraRotationWithDirection(self, direction = ROT_HOR|ROT_LEFT|ROT_VER|ROT_DWN):
		# The default rotation path is: from RIGHT -> LEFT and UP -> DOWN
		# for camera rotation motion, the right mouse button must be held down
		# y stays constant

		x, y, lastx, lasty = 500,500,500,500
		left, right, middle = False, True, False
		shift, ctrl, alt, cmd = False, False, False, False
		if direction & self.ROT_HOR:
			if direction & self.ROT_LEFT:
				lastx = 495
			else: 
				x = 495

		# allow for vertical traveling from current position to ecliptic
		# forward[2] represents the z coordinate of the camera vector. Originally,
		# the camera points down using vector (2,0,-1). 

		if (direction & self.ROT_VER) and (self.view.forward[2] < 0):
			if direction & self.ROT_UP:
				lasty = 499
			else: 
				y = 499
		self.view.report_mouse_state([left, right, middle],
		lastx, lasty, x, y,
		[shift, ctrl, alt, cmd])
		#print ("F=", self.view.forward)


	def oneTickCameraCombination(self, zoom=True, zoom_forward=True, rot_direction = ROT_HOR|ROT_RIGHT|ROT_VER|ROT_DWN):
		# for camera combination motion, we alternate rotation and zoom 
		# for zoom both right and left mouse buttons must be held down
        # default is 10 seconds

		self.oneTickCameraRotationWithDirection(rot_direction)
		if zoom and self.view.forward[2] < 0:
			self.oneTickCameraZoom(zoom_forward)


	def cameraSet(self, velocity):
		if velocity > self.MAX_ZOOM_VELOCITY:
			velocity = self.MAX_ZOOM_VELOCITY
		elif velocity < 0:
			velocity = 1
		self.cameraZoom(duration=1, velocity=velocity, ratefunc = there_and_back)
#		self.cameraZoom(duration=3, velocity=0)

	def cameraRefresh(self):
		sleep(1e-2)
		return


	# for normal zoom operation, a rate function such as "there_and_back" creates a smooth zoom. If the zoom
	# needs to be followed up by further motions as a continuous flow, a rate function that ends up at its
	# max (value 1) such as "easy_in_quad" is desirable, so that the motion from one primitive to the next 
	# will look natural. 

	def cameraZoom(self, duration, velocity = 1, recorder = False, zoom = ZOOM_IN, ratefunc = there_and_back):

		# for camera zoom motion, both right and left mouse buttons must be held down
		left, right, middle = True, True, False
		shift, ctrl, alt, cmd = False, False, False, False
		x, y, lastx, lasty = 500, 500, 500, 500
		delta = 1
		if zoom == self.ZOOM_IN:
			delta = -1

#		if recorder == True:
#			if self.parentFrame.orbitalTab.VideoRecorder == None:
#				self.parentFrame.orbitalTab.VideoRecorder = setVideoRecording(framerate = 20, filename = "output.avi")

		# calculate number of ticks
		ticks = int(duration * 70 * self.transitionVelocityFactor)
		for i in range(ticks):
			# calculate rate of velocity as a function of time
			r = ratefunc(float(i)/ticks)

			# calculate instant zoom velocity value as a function of time and max velocity
			v = int(velocity * r)+1
			
			# feed coordinate with new increment value
			y = 500 + delta * v
	
			self.view.report_mouse_state([left, right, middle],
			lastx, lasty, x, y,
			[shift, ctrl, alt, cmd])

			sleep(1e-2)
			if self.SolarSystem.Dashboard.orbitalTab.AnimationInProgress == True:
				self.SolarSystem.Dashboard.orbitalTab.OneTimeIncrement()
			if recorder == True:
				recOneFrame(self.SolarSystem.Dashboard.orbitalTab.VideoRecorder)




############################ GOOD FROM HERE DOWN

	# for normal rotation operation, a rate function such as "ease_in_out" creates a smooth panoramic. If the rotation
	# was preceded by a zoom that ended at its ratefunc maximum throughput, the rotation could use a rate function
	# that starts at its maximum value, such as "1 - rush_into",  to ensure a continuous flow.

	def cameraRotationAxis(self, angle, axis, recorder, direction, ratefunc):
		total_steps = int(100 * self.transitionVelocityFactor)

		rangle = deg2rad(angle) * (-1 if direction == self.ROT_CLKW else 1)
		dangle = 0.0
		for i in np.arange(0, total_steps+1, 1):
			r = ratefunc(float(i)/total_steps)
			iAngle = rangle * r
			self.view.forward = rotate(self.view.forward, angle=(iAngle-dangle), axis=axis)
			dangle = iAngle
			sleep(1e-2)
			if self.SolarSystem.Dashboard.orbitalTab.AnimationInProgress == True:
				self.SolarSystem.Dashboard.orbitalTab.OneTimeIncrement()
			if recorder == True:
				recOneFrame(self.SolarSystem.Dashboard.orbitalTab.VideoRecorder)


	def cameraRotateDown(self, angle, recorder, ratefunc = ease_in_out):
		# find vector orthogonal to forward vector
		axis = getOrthogonalVector(self.view.forward)

		# if angle between vertical anf forward is smaller than
		# desired rotation angle, adjust rotation angle accordingly.
		vangle = getAngleBetweenVectors(self.view.forward, vector(0,0,1))
		if vangle < angle:
			angle = vangle - 1

		self.cameraRotationAxis(angle, axis, recorder, direction=self.ROT_CLKW, ratefunc = ratefunc)

	def cameraRotateUp(self, angle, recorder, ratefunc = ease_in_out):
		# find vector orthogonal to forward vector
		axis = getOrthogonalVector(self.view.forward)

		# if angle between vertical anf forward is smaller than
		# desired rotation angle, adjust rotation angle accordingly.
		vangle = getAngleBetweenVectors(self.view.forward, vector(0,0,-1))
		if vangle < angle:
			angle = vangle - 1

		self.cameraRotationAxis(angle, axis, recorder, direction=self.ROT_CCLKW, ratefunc = ratefunc)

	def cameraRotateLeft(self, angle, recorder, axis=vector(0,0,1), ratefunc = ease_in_out):
		self.cameraRotationAxis(angle, axis, recorder, direction=self.ROT_CLKW, ratefunc = ratefunc)


	def cameraRotateRight(self, angle, recorder, axis=vector(0,0,1), ratefunc = ease_in_out):
		self.cameraRotationAxis(angle, axis, recorder, direction=self.ROT_CCLKW, ratefunc = ratefunc)

######################

	def updateCameraViewTarget(self, loc = None):
		if loc != None:
			print "Location is", loc.Name

		if self.SolarSystem.cameraViewTargetBody == None:
			print "no curent object"
			return

		if self.SolarSystem.cameraViewTargetBody.Name.lower() == EARTH_NAME:
			earthLocPos = None
			w = self.SolarSystem.EarthRef.PlanetWidgets
			if loc == None:
				if w.currentLocation >= 0:
					#w = self.Earth.PlanetWidgets.Loc[w.currentLocation]
					earthLocPos = w.Loc[w.currentLocation].getEclipticPosition()
			else:
				loc.updateEclipticPosition()
				earthLocPos = loc.getEclipticPosition()
				print "reading ecliptic from loc", loc.getEclipticPosition()

			if earthLocPos != None:
				#print "centering on loc", earthLocPos.Name
				self.SolarSystem.Scene.center = (
					earthLocPos[0],
					earthLocPos[1],
					earthLocPos[2]
				)
				return
		#else:
		
		# the following values will do the following
		# (0,-1,-1): freezes rotation and looks down towards the left
		# (0,-1, 1): freezes rotation and looks up towards the left
		# (0, 1, 1): freezes rotation and looks up towards the right
		# (0, 1,-1): freezes rotation and looks down towards the right

		# self.SolarSystem.Scene.forward = (0, 0, -1)
		# For a planet, Foci(x, y, z) is (0,0,0). For a moon, Foci represents the 
		# position of the planet the moon orbits around in the ecliptic referential

		######self.surfaceRadius = (1.1 * self.SolarSystem.cameraViewTargetBody.BodyShape.radius) if self.SolarSystem.SurfaceView == True else 0
		#print "UPDATING Scene Center with ViewTarget origin"
		self.SolarSystem.Scene.center = (
			self.SolarSystem.cameraViewTargetBody.Position[0] + self.SolarSystem.cameraViewTargetBody.Foci[0],
			self.SolarSystem.cameraViewTargetBody.Position[1] + self.SolarSystem.cameraViewTargetBody.Foci[1],
			self.SolarSystem.cameraViewTargetBody.Position[2] + self.SolarSystem.cameraViewTargetBody.Foci[2]
		)
		#print "----------"
		#print "updateCameraViewTarget: position:",self.SolarSystem.cameraViewTargetBody.Position
		##print "label coordinates:",self.SolarSystem.cameraViewTargetBody.Labels[0].pos
		#print "updateCameraViewTarget: label=", self.SolarSystem.cameraViewTargetBody.Labels[0].pos, "origin=", self.SolarSystem.cameraViewTargetBody.Origin.pos
		#print "----------"

	def setTransitionVelocity(self, velocity):
		if velocity > self.VELOCITY_MAX:
			velocity = self.VELOCITY_MAX
		elif velocity <= 0:
			velocity = self.VELOCITY_MIN

		# the higher the velocity, the smaller number of steps
		self.transitionVelocityFactor = 1/float(velocity)


	def _smoothFocus(self, newloc, ratefunc = ease_in_out):

		# (Xc, Yc, Zc) is the current location (scene center before transition)
		Xc = self.SolarSystem.Scene.center[0]
		Yc = self.SolarSystem.Scene.center[1]
		Zc = self.SolarSystem.Scene.center[2]
		print ("Xc=", Xc, ", Yc=", Yc,", Zc=", Zc)
		
		# calculate distance between current location and 
		# destination for each coordinate 
		deltaX = (newloc[0] - Xc)
		deltaY = (newloc[1] - Yc)
		deltaZ = (newloc[2] - Zc)

		print ("X=", deltaX, ", Y=", deltaY,", Z=", deltaZ)

		if self.SolarSystem.Dashboard.orbitalTab.RecorderOn == True:
			if self.SolarSystem.Dashboard.orbitalTab.VideoRecorder == None:
				self.SolarSystem.Dashboard.orbitalTab.VideoRecorder = setVideoRecording(framerate = 20, filename = "output.avi")


		# Calculate number of steps based on current transition velocity factor (default is 1.0)
		#print ("Smooth Focus TRANSITION VELOCITY=", self.transitionVelocityFactor)
		total_steps = int(100 * self.transitionVelocityFactor)
		#print ("Smooth Focus TOTAL_STEPS=", total_steps)

		# move scene center by an increment towards the destination coordinates. Since 
		# we use 100 * transitionVelocityFactor steps to do that, and our rate function 
		# only takes an input between 0 and 1, we divide the current increment by the 
		# total number of steps to always keep the rate function input between these limits.
		# Incremental location is calculated as the initial location + difference between initial
		# and final locations time the rate for this particular step.

		for i in np.arange(0, total_steps+1, 1):
			r = ratefunc(float(i)/total_steps)
			self.SolarSystem.Scene.center = vector( (Xc + r*deltaX),
													(Yc + r*deltaY),
													(Zc + r*deltaZ))
			sleep(2e-2)
			if self.SolarSystem.Dashboard.orbitalTab.AnimationInProgress == True:
				self.SolarSystem.Dashboard.orbitalTab.OneTimeIncrement()
			if self.SolarSystem.Dashboard.orbitalTab.RecorderOn == True:
				recOneFrame(self.SolarSystem.Dashboard.orbitalTab.VideoRecorder)


	def smoothFocus2target(self, target, ratefunc = ease_in_out):
		return self._smoothFocus(target, ratefunc)

	def smoothFocus(self, targetBodyName, ratefunc =  ease_in_out):
		# going from current object to next current object
		target = None
		targetBody = self.SolarSystem.getBodyFromName(targetBodyName.lower())
		if targetBody == None:
			# use sun as target
			target = vector(0,0,0)
		else:
			target = targetBody.Position

		return self._smoothFocus(target, ratefunc)


	def gotoEarthLocation(self, nextLocation, ratefunc = ease_in_out_quart):

		self.Loc[nextLocation].updateEclipticPosition()
		nextPos = self.Loc[nextLocation].getGeoPosition()


		#self.B =  simpleArrow(color.green, 0, 20, nextPos, axisp = self.Loc[nextLocation].Grad/10, context = self.Loc[nextLocation].Origin)
		#self.B.display(True)

		# build radial vector vertical to location in ecliptic coordinates
		dest = self.Loc[nextLocation].getEclipticPosition()
		A = dest[0] - self.SolarSystem.EarthRef.Origin.pos[0] #self.Planet.Origin.pos[0]
		B = dest[1] - self.SolarSystem.EarthRef.Origin.pos[1] #self.Planet.Origin.pos[1]
		C = dest[2] - self.SolarSystem.EarthRef.Origin.pos[2] #self.Planet.Origin.pos[2] 
		radialToLocation = vector(A, B, C)/np.sqrt(A**2 + B**2 + C**2)

        # (Xc, Yc, Zc) is the current location of center (before transition)
		Xc = self.SolarSystem.Scene.center[0]
		Yc = self.SolarSystem.Scene.center[1]
		Zc = self.SolarSystem.Scene.center[2]
        
		# calculate distance between current location and 
		# destination for each coordinate 
		deltaX = (dest[0] - Xc)
		deltaY = (dest[1] - Yc)
		deltaZ = (dest[2] - Zc)

		if self.SolarSystem.Dashboard.orbitalTab.RecorderOn == True:
			if self.SolarSystem.Dashboard.orbitalTab.VideoRecorder == None:
				self.SolarSystem.Dashboard.orbitalTab.VideoRecorder = setVideoRecording(framerate = 20, filename = "output.avi")


		# radialToCamera (vector between center of earth and camera location)
		radialToCamera = -self.SolarSystem.Scene.forward

		# determine axis of rotation. We do that by obtaining a vector orthogonal 
		# to the plane defined our 2 radial vectors
		rotAxis = getVectorOrthogonalToPlane(radialToCamera, radialToLocation)
		if False:
			self.K =  simpleArrow(color.cyan, 0, 20, self.Planet.SolarSystem.Scene.mouse.camera, axisp = 1e4*rotAxis, context = None) #self.Loc[locationID].Origin)
			self.K.display(True)

		# calculate angle between rot axis and vertical
		vAngle = getAngleBetweenVectors(rotAxis, vector(0,0,1))
		velocityF = self.transitionVelocityFactor

		# when the rotation plane is nearly vertical, we need to add more steps
		# to slow down possible vpython jerky rotation.
		if abs(vAngle - float(90)) < 5:
			print "Close enough to vertical!!!", vAngle
			velocityF = velocityF * 1.7

		# determine angle between 2 radial vectors
		rotAngle = deg2rad(getAngleBetweenVectors(radialToCamera, radialToLocation))

        # Calculate number of steps based on current transition velocity factor (default is 1.0)
		total_steps = int(100) * velocityF

		accumulated_rot = 0.0
		for i in np.arange(0, total_steps+1, 1):
			# incrementally, change center focus and rotate
			r = ratefunc(float(i)/total_steps)
			self.SolarSystem.Scene.center = vector( (Xc + r*deltaX),
													(Yc + r*deltaY),
													(Zc + r*deltaZ))

			iAngle = rotAngle * r

			self.SolarSystem.Scene.forward = rotate(self.SolarSystem.Scene.forward, angle=(iAngle-accumulated_rot), axis=rotAxis)
			accumulated_rot = iAngle

			sleep(2e-2)
			if self.SolarSystem.Dashboard.orbitalTab.AnimationInProgress == True:
				self.SolarSystem.Dashboard.orbitalTab.OneTimeIncrement()
			if self.SolarSystem.Dashboard.orbitalTab.RecorderOn == True:
				recOneFrame(self.SolarSystem.Dashboard.orbitalTab.VideoRecorder)

		self.SolarSystem.EarthRef.PlanetWidgets.currentLocation = nextLocation


"""	
	#def cameraPan(self, duration, velocity = 1, direction = ROT_CLKW):
	def cameraPan(self, angle, axis, recorder, direction, ptype):
		total_steps = int(100 * self.solarSystem.Dashboard.focusTab.transitionVelocityFactor)

		rangle = deg2rad(angle) * (-1 if direction == self.ROT_CLKW else 1)
		dangle = 0.0
		#if ptype == ROT_
		for i in np.arange(0, total_steps+1, 1):
			r = ease_in_out(float(i)/total_steps)
			iAngle = rangle * r
#			self.view.forward = rotate(self.view.forward, angle=(iAngle-dangle), axis=axis)
			self.view.forward.rotate(angle=(iAngle-dangle), axis=axis)
			dangle = iAngle
			sleep(1e-2)
			if recorder == True:
				recOneFrame(self.solarSystem.Dashboard.orbitalTab.VideoRecorder)


	def getDurationFactor(self, angle):
		if angle <= 10:
			return 100
		elif angle <= 30:
			return 70
		elif angle <= 50:
			return 60
		elif angle <= 60:
			return 50
		elif angle <= 80:
			return 50
		return 45



	def cameraLeft(self, duration, velocity = 1):
		v1 = self.view.mouse.camera-self.view.center
		print "vector BEFORE MVT=", v1
		self.cameraMovement(duration, velocity, direction = self.ROT_LEFT)
		v2 = self.view.mouse.camera-self.view.center
		print "vector AFTER MVT=", v2
		dotProduct = v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]
		theta = np.arccos(dotProduct/(mag(v1)*mag(v2)))
		print "THETA=", rad2deg(theta)

	def cameraRight(self, duration, velocity = 1):
		return self.cameraMovement(duration, velocity, direction = self.ROT_RIGHT)
	
	def cameraPanUp(self, duration, velocity = 1):
		return self.cameraMovement(duration, velocity, direction = self.ROT_UP)
	
	def cameraPanDown(self, duration, velocity = 1):
		return self.cameraMovement(duration, velocity, direction = self.ROT_DWN)

	def cameraMovement(self, duration, velocity = 1, direction = ROT_UP):
		# for camera vertical motion, the right mouse button must be held down
		# x stays constant
		left, right, middle = False, True, False
		shift, ctrl, alt, cmd = False, False, False, False
		elements = [500, 500, 500, 500]

		#x, y = 500, 500
		#lastx, lasty = 500, 500 #499

		# default is vertical UP
		delta = 1
		elt = self.LASTY_OFF
		if direction == self.ROT_DWN:
			delta = -1 
		elif direction == self.ROT_LEFT:
			elt = self.LASTX_OFF
			delta = -1 
		elif direction == self.ROT_RIGHT:
			elt = self.LASTX_OFF

		ticks = duration * 70 # duration / sleep time which is 0.01

		for i in range(ticks):
		#for i in range(100):
			# calculate rate of velocity as a function of time
			r = there_and_back(float(i)/ticks)

			# calculate instant zoom velocity value as a function of time and max velocity
			v = int(velocity * r)+1
			print "V=", v

			# feed coordinate with new increment value
			elements[elt] = 500 + delta * v
			#lasty = 500 + delta * v

			self.view.report_mouse_state([left, right, middle],
			#lastx, lasty, x, y,
			elements[self.LASTX_OFF], elements[self.LASTY_OFF], elements[self.X_OFF], elements[self.Y_OFF],
			[shift, ctrl, alt, cmd])


			#lasty = y
			#y -= 1
			sleep(1e-2)

	def cameraPanOLD(self):
		# for camera vertical motion, the right mouse button must be held down
		# x stays constant
		left, right, middle = False, True, False
		shift, ctrl, alt, cmd = False, False, False, False
		x, y = 500, 500
		lastx, lasty = 500, 499

		for i in range(100):
			self.view.report_mouse_state([left, right, middle],
			lastx, lasty, x, y,
			[shift, ctrl, alt, cmd])
			lasty = y
			y -= 1
			sleep(1e-2)

	def cameraRotation(self):
		# for camera rotation motion, the right mouse button must be held down
		# y stays constant

		left, right, middle = False, True, False
		shift, ctrl, alt, cmd = False, False, False, False
		x, y = 500, 500
		lastx, lasty = 499, 500

		for i in range(100):
			self.view.report_mouse_state([left, right, middle],
			lastx, lasty, x, y,
			[shift, ctrl, alt, cmd])
			lastx = x
			x -= 1
			sleep(1e-2)
"""
"""
if False:
	# Draw window & 3D pane =================================================

	win = window(width=1024, height=720, menus=False, title='SIMULATE VPYTHON GUI')
							# make a main window. Also sets w.panel to addr of wx window object. 
	scene = display( window=win, width=830, height=690, forward=-vector(1,1,2))

	vss = scene

	# Event handlers =========================

	def setModView():  # set so that we see view from mod-cam
		global saved_pyvars
		vss.userspin = vss.userzoom = False
		vss.autoscale = vss.autocenter = False  # should not be necessary,  but is! 
		saved_pyvars = [ tuple(vss.forward), tuple(vss.center), vss.fov ]
		# save VPython GUI status (so that we can restore it later ). tuple()is NEEDED so the data
		# is copied - not just its address.   vss.range is not useful. 
		vss.forward = - cam_frame.axis 
		vss.center =  cam_frame.pos
		vss.fov = fov
		vss.range = range_x
		cam_box.visible = fwd_arrow.visible = mouse_arrow.visible = False
		cam_tri.visible = False    
		
	def setPyView():  # set so we see view from py-cam (ie std VPython)  
		vss.userspin = vss.userzoom = True
		vss.forward, vss.center, vss.fov = saved_pyvars
										# Restore py-vars to what they were when qPy was turned off.
										# Except RANGE - as cannot be saved.  So.... 
		vss.range = scene_size*1.5   # SET it.  
		cam_box.visible = fwd_arrow.visible = mouse_arrow.visible = True
		cam_tri.visible = True   


	def hCamera(evt): # re "Switch Camera" button
		global qPy
		if qPy:  # we are seeing view from py-cam 
		qPy = False     
		setModView()  # set so that we see view from mod-cam
		else:          
		qPy = True
		setPyView()  # set so we see view from py-cam (ie std VPython)
				
	def hReset(evt): # re "Reset" button
		global cam_frame
		cam_box.visible = fwd_arrow.visible = mouse_arrow.visible = True
		cam_tri.visible = True  # so is included in cam_frame.objects list.
		for obj in cam_frame.objects:
		obj.visible = False
		del obj
		del cam_frame
		drawCameraFrame()  # recreate camera frame and its contents
		mode_lab.SetLabel("")  # as is no longer right 
		if not qPy:  setModView() # because drawCameraFrame() assumes qPy is True. 

def drawCameraFrame():  # create frame and draw its contents
    global  cam_box, cent_plane,  cam_lab, cam_tri, range_lab, linelen, fwd_line
    global fwd_arrow, mouse_line, mouse_arrow, mouse_lab, fov, range_x, cam_dist, cam_frame
    global ray
    cam_frame = vs.frame( pos = vs.vector(0,2,2,),  axis = (0,0,1))
               # NB: contents are rel to this frame.  start with camera looking "forward"
               # origin is at simulated scene.center
    fov = vs.pi/3.0  # 60 deg 
    range_x = 6  # simulates scene.range.x  
    cam_dist = range_x / vs.tan(fov/2.0)  # distance between camera and center. 
    ray = vs.vector(-20.0, 2.5, 3.0).norm()  # (unit) direction of ray vector (arbitrary)
                                         #  REL TO CAMERA FRAME
    cam_box = vs.box(frame=cam_frame, length=1.5, height=1, width=1.0, color=clr.blue,
                                                   pos=(cam_dist,0,0)) # camera-box
    cent_plane = vs.box(frame=cam_frame, length=0.01, height=range_x*1.3, width=range_x*2,
                                                    pos=(0,0,0), opacity=0.5 )  # central plane
    cam_lab = vs.label(frame=cam_frame, text= 'U', pos= (cam_dist,0,0), height= 9, xoffset= 6)
    cam_tri = vs.faces( frame=cam_frame, pos=[(0,0,0), (0,0,-range_x), (cam_dist,0,0)])
    cam_tri.make_normals()
    cam_tri.make_twosided()
    range_lab = vs.label(frame=cam_frame, text= 'R', pos= (0, 0, -range_x), height= 9, xoffset= 6)
    linelen = scene_size + vs.mag( cam_frame.axis.norm()*cam_dist + cam_frame.pos)
                                                                   # len of lines from camera
    fwd_line = drawLine( vs.vector(cam_dist,0,0), linelen, vs.vector(-1,0,0))
    fwd_arrow = vs.arrow(frame=cam_frame, axis=(-2,0,0), pos=(cam_dist, 0, 0), shaftwidth=0.08,
                                                                            color=clr.yellow)
    vs.label(frame=cam_frame, text='C', pos=(0,0,0), height=9, xoffset=6, color=clr.yellow)
    mouse_line = drawLine ( vs.vector(cam_dist,0,0), linelen, ray ) 
    mouse_arrow = vs.arrow(frame=cam_frame, axis=ray*2, pos=(cam_dist,0,0), shaftwidth=0.08,
                                                                                   color=clr.red)
    mouse_lab = vs.label(frame=cam_frame, text= 'M', height= 9, xoffset= 10, color=clr.red, 
                                pos=  -ray*(cam_dist/vs.dot(ray,(1,0,0))) + (cam_dist,0,0))

"""
