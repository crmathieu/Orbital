from visual import *
from rate_func import *

# All camera movements occur using a focal point centered on the
# current object
#
# in this module, fake mouse events are generated to induce camera movements.
# Then, the vpython report_mouse_state method is called to update the canvas 
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


ROT_HOR = 1
ROT_VER = 2
ROT_UP = 4
ROT_DWN = 8
ROT_LEFT = 16
ROT_RIGHT = 32

ROT_DIAG_RIGHT_DWN = ROT_HOR|ROT_RIGHT|ROT_VER|ROT_DWN
ROT_DIAG_LEFT_DWN = ROT_HOR|ROT_LEFT|ROT_VER|ROT_DWN
ROT_DIAG_LEFT_UP = ROT_HOR|ROT_LEFT|ROT_VER|ROT_UP
ROT_DIAG_RIGHT_UP = ROT_HOR|ROT_RIGHT|ROT_VER|ROT_UP

ZOOM_IN = 1
ZOOM_OUT = 2

class camera:


	def __init__(self, display):
		self.canvas = display
		self.MAX_ZOOM_VELOCITY = 50
		
	def oneTickCameraZoom(self, forward = True):
		# for camera zoom motion, both right and left mouse buttons must be held down
		left, right, middle = True, True, False
		shift, ctrl, alt, cmd = False, False, False, False
		x, y = 499, 499
		lastx, lasty = 500, 500
		if not forward:
			x, y = 500, 500
			lastx, lasty = 499, 499
		self.canvas.report_mouse_state([left, right, middle],
		lastx, lasty, x, y,
		[shift, ctrl, alt, cmd])

	def oneTickCameraRotation(self):
		# for camera rotation motion, the right mouse button must be held down
		# y stays constant

		left, right, middle = False, True, False
		shift, ctrl, alt, cmd = False, False, False, False
		x, y = 500, 500
		lastx, lasty = 499, 500

		self.canvas.report_mouse_state([left, right, middle],
		lastx, lasty, x, y,
		[shift, ctrl, alt, cmd])

	def oneTickCameraRotationWithDirection(self, direction = ROT_HOR|ROT_LEFT|ROT_VER|ROT_DWN):
		# The default rotation path is: from RIGHT -> LEFT and UP -> DOWN
		# for camera rotation motion, the right mouse button must be held down
		# y stays constant
		x, y, lastx, lasty = 500,500,500,500
		left, right, middle = False, True, False
		shift, ctrl, alt, cmd = False, False, False, False
		if direction & ROT_HOR:
			if direction & ROT_LEFT:
				lastx = 495
			else: 
				x = 495

		# allow for vertical traveling from current position to ecliptic
		# forward[2] represents the z coordinate of the camera vector. Originally,
		# the camera points down using vector (2,0,-1). 
		if (direction & ROT_VER) and (self.canvas.forward[2] < 0):
			if direction & ROT_UP:
				lasty = 499
			else: 
				y = 499
		self.canvas.report_mouse_state([left, right, middle],
		lastx, lasty, x, y,
		[shift, ctrl, alt, cmd])
		#print ("F=", self.canvas.forward)

	def cameraComboXX(self, length=10):
		# for camera combo motion, we alternate rotation and zoom 
		# for zoom both right and left mouse buttons must be held down
        # default is 10 seconds
		for i in range(1000):
			self.oneTickCameraRotation()
			self.oneTickCameraZoom(forward=True)
			sleep(1e-2)

	def oneTickCameraCombination(self, zoom=True, zoom_forward=True, rot_direction = ROT_HOR|ROT_RIGHT|ROT_VER|ROT_DWN):
		# for camera combination motion, we alternate rotation and zoom 
		# for zoom both right and left mouse buttons must be held down
        # default is 10 seconds
		self.oneTickCameraRotationWithDirection(rot_direction)
		if zoom and self.canvas.forward[2] < 0:
			self.oneTickCameraZoom(zoom_forward)

	def cameraCombination2(self, frame=100, rot_direction = ROT_HOR|ROT_LEFT|ROT_VER|ROT_DWN, zoom=True, zoom_forward=True ):
		# for camera combination motion, we alternate rotation and zoom 
		# for zoom both right and left mouse buttons must be held down
        # default is 10 seconds
		for i in range(frame):
			self.oneTickCameraRotationWithDirection(rot_direction)
			if zoom:
				self.oneTickCameraZoom(zoom_forward)
			sleep(1e-2)

	def cameraZoom2(self, rate_func = linear):
		# for camera zoom motion, both right and left mouse buttons must be held down
		left, right, middle = True, True, False
		shift, ctrl, alt, cmd = False, False, False, False
		x, y = 500, 500
		lastx, lasty = 499, 499

		for i in range(100):
			self.canvas.report_mouse_state([left, right, middle],
			lastx, lasty, x, y,
			[shift, ctrl, alt, cmd])
			lastx = x
			lasty = y
			x -= 1
			y -= 1
			sleep(1e-2)

	def cameraSet(self, velocity):
		if velocity > self.MAX_ZOOM_VELOCITY:
			velocity = self.MAX_ZOOM_VELOCITY
		elif velocity < 0:
			velocity = 1
		self.cameraZoom(duration=1, velocity=velocity)

	def cameraRefresh(self):
		sleep(1e-2)
		return

	def cameraZoom(self, duration, velocity = 1, zoom = ZOOM_IN):
		# for camera zoom motion, both right and left mouse buttons must be held down
		left, right, middle = True, True, False
		shift, ctrl, alt, cmd = False, False, False, False
		x, y, lastx, lasty = 500, 500, 500, 500
		delta = 1
		if zoom == ZOOM_IN:
			delta = -1

		# calculate number of ticks
		ticks = duration * 70 # duration / sleep time which is 0.01
		for i in range(ticks):
			#j = smooth(i+1)
			#print ("i=", i+1, "smooth(x)=", j)
			#continue
			#k = int(floor(j/(i+1)))
			y = 500 + delta * velocity
			#print ("Y=", y)
			self.canvas.report_mouse_state([left, right, middle],
			lastx, lasty, x, y,
			[shift, ctrl, alt, cmd])
			sleep(1e-2)


	def cameraPan(self):
		# for camera vertical motion, the right mouse button must be held down
		# x stays constant
		left, right, middle = False, True, False
		shift, ctrl, alt, cmd = False, False, False, False
		x, y = 500, 500
		lastx, lasty = 500, 499

		for i in range(100):
			self.canvas.report_mouse_state([left, right, middle],
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
			self.canvas.report_mouse_state([left, right, middle],
			lastx, lasty, x, y,
			[shift, ctrl, alt, cmd])
			lastx = x
			x -= 1
			sleep(1e-2)
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
