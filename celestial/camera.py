from visual import *
from rate_func import *
from utils import deg2rad, rad2deg, getAngleBetweenVectors, getOrthogonalVector

from video import * 

# All camera movements occur using a focal point centered on the
# current object
#
# in this module, fake mouse events are generated to induce camera movements.
# Then, the vpython report_mouse_state method is called to update the view 
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



class camera:

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

	def __init__(self, solSys):
		self.view = solSys.Scene
		self.solarSystem = solSys
		self.MAX_ZOOM_VELOCITY = 100
		
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
		self.cameraZoom(duration=1, velocity=velocity)
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
#				self.parentFrame.orbitalTab.VideoRecorder = setVideoRecording(25, "output.avi")

		# calculate number of ticks
		#### ticks = duration * 70 # duration / sleep time which is 0.01
		ticks = int(duration * 70 * self.solarSystem.Dashboard.focusTab.transitionVelocityFactor)
		for i in range(ticks):
			# calculate rate of velocity as a function of time
			##### r = there_and_back(float(i)/ticks)
			r = ratefunc(float(i)/ticks)

			# calculate instant zoom velocity value as a function of time and max velocity
			v = int(velocity * r)+1
			
			# feed coordinate with new increment value
			y = 500 + delta * v
	
			self.view.report_mouse_state([left, right, middle],
			lastx, lasty, x, y,
			[shift, ctrl, alt, cmd])
			sleep(1e-2)
			if recorder == True:
				recOneFrame(self.solarSystem.Dashboard.orbitalTab.VideoRecorder)




############################ GOOD FROM HERE DOWN

	def getAngleBetweenVectorsXX(self, v1, v2):
		dotProduct = v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]
		theta = np.arccos(dotProduct/(mag(v1)*mag(v2)))
		return rad2deg(theta)

	# for normal rotation operation, a rate function such as "ease_in_out" creates a smooth panoramic. If the rotation
	# was preceded by a zoom that ended at its ratefunc maximum value (1), the rotation could use a rate function
	# that starts at its maximum value, such as "1 - rush_into",  to ensure a continuous flow.

	def cameraRotationAxis(self, angle, axis, recorder, direction, ratefunc = ease_in_out):
		total_steps = int(100 * self.solarSystem.Dashboard.focusTab.transitionVelocityFactor)

		rangle = deg2rad(angle) * (-1 if direction == self.ROT_CLKW else 1)
		dangle = 0.0
		for i in np.arange(0, total_steps+1, 1):
#			r = ease_in_out(float(i)/total_steps)
			r = ratefunc(float(i)/total_steps)
			iAngle = rangle * r
			self.view.forward = rotate(self.view.forward, angle=(iAngle-dangle), axis=axis)
			dangle = iAngle
			sleep(1e-2)
			if recorder == True:
				recOneFrame(self.solarSystem.Dashboard.orbitalTab.VideoRecorder)


	def getOrthogonalVectorXX(self, vec):
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

	def cameraRotateDown(self, angle, recorder):
#		vangle = self.getAngleBetweenVectors(self.view.forward, vector(0,0,-1))
		axis = getOrthogonalVector(self.view.forward)

		# if angle between vertical anf forward is smaller than
		# desired rotation angle, adjust rotation angle accordingly.
		vangle = getAngleBetweenVectors(self.view.forward, vector(0,0,1))
		if vangle < angle:
			angle = vangle - 1

		self.cameraRotationAxis(angle, axis, recorder, direction=self.ROT_CLKW)

	def cameraRotateUp(self, angle, recorder):
		# find vector orthogonal to forward vector
		axis = getOrthogonalVector(self.view.forward)

		# if angle between vertical anf forward is smaller than
		# desired rotation angle, adjust rotation angle accordingly.
		vangle = getAngleBetweenVectors(self.view.forward, vector(0,0,-1))
		if vangle < angle:
			angle = vangle - 1

		self.cameraRotationAxis(angle, axis, recorder, direction=self.ROT_CCLKW)

	def cameraRotateLeft(self, angle, recorder):
		self.cameraRotationAxis(angle, vector(0,0,1), recorder, direction=self.ROT_CLKW)


	def cameraRotateRight(self, angle, recorder):
		self.cameraRotationAxis(angle, vector(0,0,1), recorder, direction=self.ROT_CCLKW)

######################
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
"""
