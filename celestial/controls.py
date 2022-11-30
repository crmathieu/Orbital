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
import orbit3D 
from location import locList #*
from planetsdata import *
from visual import *
import threading
import pytz
from utils import getOrthogonalVector #, sleep

#from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

from numberfmt import *
import urllib2, urllib
#import httplib
from video import * #VideoRecorder
#import re
import json

import wx
import wx.lib.newevent # necessary for custom event

import rate_func

MAIN_HEADING_Y = 40
MAIN_MIDDLE_X = 200
DATE_Y = MAIN_HEADING_Y
DATE_SLD_Y = DATE_Y + 20
JPL_BRW_Y = DATE_SLD_Y

# checkboxes lines
CHK_L1 = MAIN_HEADING_Y + 20
CHK_L2 = CHK_L1 + 20
CHK_L3 = CHK_L2 + 20
CHK_L4 = CHK_L3 + 20
CHK_L5 = CHK_L4 + 20
CHK_L6 = CHK_L5 + 20
CHK_L7 = CHK_L6 + 20
CHK_L8 = CHK_L7 + 20
CHK_L9 = CHK_L8 + 20
CHK_L10 = CHK_L9 + 20
CHK_L11 = CHK_L10 + 20
CHK_L12 = CHK_L11 + 20
CHK_L13 = CHK_L12 + 20
CHK_L14 = CHK_L13 + 20

CHK_L15 = CHK_L14 + 25
CHK_L15B = CHK_L14 + 20

CHK_L16 = CHK_L15B + 20
CHK_L17 = CHK_L16 + 20
CHK_L18 = CHK_L17 + 20
CHK_L19 = CHK_L18 + 20
CHK_L20 = CHK_L19 + 20
CHK_L21 = CHK_L20 + 20
CHK_L22 = CHK_L21 + 20
CHK_L23 = CHK_L22 + 20
CHK_L24 = CHK_L23 + 20
CHK_L25 = CHK_L24 + 20
CHK_L26 = CHK_L25 + 20
CHK_L27 = CHK_L26 + 20
CHK_L28 = CHK_L27 + 20
CHK_L29 = CHK_L28 + 20
CHK_L30 = CHK_L29 + 20
CHK_L31 = CHK_L30 + 20
CHK_L32 = CHK_L31 + 20

CBBOX_1 = CHK_L8+30
CBBOX_2 = CHK_L26 + 30

LSTB_Y = DATE_Y + 60
SLDS_Y = LSTB_Y + 40

STRT_Y = SLDS_Y
PAU_Y = STRT_Y + 40
JPL_Y = PAU_Y + 40
ANI_Y = JPL_Y + 100
DET_Y = CHK_L14 + 120 #70

INFO1_Y = DET_Y + 20
#INFO1_V = INFO1_Y + 75

#JPL_CLOSE_APPROACH_Y = INFO1_V+30

TOTAL_Y = INFO1_Y+180
TOTAL_X = 500

date_elements = {
	"d_p_m" : {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31},
	"d_p_m_leap" : {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31},
	"d_to_m" :{1:0, 2:31, 3:59, 4:90, 5:120, 6:151, 7:181, 8:212, 9:243, 10:273, 11:304, 12:334},
	"d_to_m_leap" :{1:0, 2:31, 3:60, 4:91, 5:121, 6:152, 7:182, 8:213, 9:244, 10:274, 11:305, 12:335},
	"d_since_J2000":{1995:-1827.5, 1996: -1462.5, 1997: -1096.5, 1998: -731.5, 1999:-366.5, 2000:-1.5, 2001: 364.5, 2002: 729.5, 2003:1094.5, 2004:1459.5, 2005:1825.5}
}

def isLeapYear(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

#
# JPL API search Panel
#

JPL_MAIN_HEADING_Y = 25
JPL_DOWNLOAD_Y = JPL_MAIN_HEADING_Y-15
JPL_LISTCTRL_Y = JPL_MAIN_HEADING_Y + 25

JPL_LIST_SZ = TOTAL_Y-160
JPL_BRW_Y = JPL_LISTCTRL_Y + JPL_LIST_SZ + 15

JPL_SEARCH_Y = JPL_BRW_Y + 20


# PANELS numbers - Note that panels MUST be added in the same order to the parent
# notebook to make it possible to switch from panel to panel programmatically

PANEL_MAIN 	= 0
PANEL_CVT 	= 1
PANEL_CAPP 	= 2

CVT_Y = 15
CVT_FOCUS_Y = CVT_Y+150

from abc import ABCMeta

# CLASS AbstractUI ------------------------------------------------------------
# abstract class from which each "panel" class derives
class AbstractUI(wx.Panel):
	__metaclass__ = ABCMeta

	def __init__(self, parent, notebook, solarsystem):
		wx.Panel.__init__(self, parent=notebook)
		self.parentFrame = parent
		self.nb = notebook
		self.SolarSystem = solarsystem
		self.Earth = solarsystem.EarthRef

		self.InitVariables()
		self.InitUI()

	def InitVariables(self):
		pass

	def InitUI(self):
		pass

	def createCheckBox(self, panel, title, type, xpos, ypos):
		cb = wx.CheckBox(panel, label=title, pos=(xpos, ypos))
		if self.SolarSystem.ShowFeatures & type != 0:
			cb.SetValue(True)
		else:
			cb.SetValue(False)
		self.checkboxList[type] = cb

"""
class DrawRect(wx.Panel):
     def __init__(self, parent=None, id=-1,pos=(-1,-1), size=(-1,-1), style=0):
         wx.Panel.__init__(self,parent,id,size,pos,style)
         self.SetBackgroundColour("#D18B47")
         self.Bind(wx.EVT_PAINT,self.onPaint)

     def onPaint(self, event):
         event.Skip()
         dc = wx.PaintDC(event.GetEventObject())
         self.drawRect(dc)

     def drawRect(self,dc):
         dc.SetPen(wx.Pen("FFCE8A", 0))
         dc.SetBrush(wx.Brush("C0C0C0"))
         dc.DrawRectangle(50,50,50,50)		
"""
class createVizualisationWindow(wx.Frame):

	def __init__(self, pos, size):
		style = (wx.CLIP_CHILDREN |wx.STAY_ON_TOP|wx.FRAME_NO_TASKBAR|wx.NO_BORDER|wx.FRAME_SHAPED)
		#        style = ( wx.CLIP_CHILDREN | wx.FRAME_FLOAT_ON_PARENT | wx.FRAME_NO_TASKBAR |
		#                  wx.NO_BORDER | wx.FRAME_SHAPED  )
		#        wx.Frame.__init__(self, parent=None, title='Fancy Window', style = style, size=(orbit3D.makeSolarSystem.SCENE_WIDTH, orbit3D.makeSolarSystem.SCENE_HEIGHT))

		wx.Frame.__init__(self, parent=None, id=10, title='', pos = pos, style = style, size=size)
		self.panel = wx.Panel(self, size=size) #(350, 200)) 
		self.panel.Bind(wx.EVT_PAINT, self.onPaint) 
		self.Fit() 

		self.pos = pos
		self.size = size
		self.SetBackgroundColour('BLACK')
		self.SetForegroundColour('WHITE')

		#self.Bind(wx.EVT_KEY_UP, self.OnKeyDown)
		#self.Bind(wx.EVT_MOTION, self.OnMouse)
		
#		self.BoldFont = wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD)
#		self.RegFont = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)

		self.BoldFont = wx.Font(20, wx.MODERN, wx.NORMAL, wx.BOLD)
		self.RegFont = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL)
		#DrawRect(parent=p, id=10, pos=(1,1), size=(498,148))
		self.infoLineGroup = []
		self.setInfoLineGroup(2)

	def setInfoLineGroup(self, dim):
		for i in range(0,dim):
			self.infoLineGroup = append(self.infoLineGroup, wx.StaticText(self, label="", pos=(10, 10+(i*30)), size=(self.size[0]-11, 30))) #50)))
			self.infoLineGroup[i].SetFont(self.RegFont)
			self.infoLineGroup[i].Wrap(self.GetSize().width)

	def setLine(self, text, n):
		if n < 0 or n > len(self.infoLineGroup)-1:
			return
		self.infoLineGroup[n].SetLabel(text)

	def onPaint(self, e):
		# establish the painting surface
		dc = wx.PaintDC(self.panel)

		dc.SetPen(wx.Pen('white', 1))
		dc.SetBrush(wx.Brush('black'))

#		print self.pos[0], self.pos[1], self.size[0], self.size[1]
#		rect = wx.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]) 

		rect = wx.Rect(0, 0, self.size[0], self.size[1]) 
		dc.DrawRoundedRectangleRect(rect, 0)

#		self.setLine("line1", 0)
#		self.setLine("line2", 1)
#		self.setLine("line3", 2)

		if False:
			dc.SetPen(wx.Pen('blue', 4))
			# draw a blue line (thickness = 4)
			dc.DrawLine(50, 20, 300, 20)
			dc.SetPen(wx.Pen('red', 1))
			# draw a red rounded-rectangle
			rect = wx.Rect(50, 50, 100, 100) 
			dc.DrawRoundedRectangleRect(rect, 8)
			# draw a red circle with yellow fill
			dc.SetBrush(wx.Brush('yellow'))
			x = 250
			y = 100
			r = 50
			dc.DrawCircle(x, y, r)

	def display(self, trueFalse):
		self.Show(trueFalse)

#	def hide(self):
#		self.SetTransparent(0)
#		self.Show(False)

#	def show(self):
#		self.SetTransparent(255)
#		self.Show(True)


"""
	def OnKeyDown(self, event):
		#quit if user press q or Esc
		if event.GetKeyCode() == 27 or event.GetKeyCode() == ord('Q'): #27 is Esc
			self.Close(force=True)
		else:
			event.Skip()

	def OnMouse(self, event):
		#implement dragging
		if not event.Dragging():
			self._dragPos = None
			return
		self.CaptureMouse()
		if not self._dragPos:
			self._dragPos = event.GetPosition()
		else:
			pos = event.GetPosition()
			displacement = self._dragPos - pos
			self.SetPosition( self.GetPosition() - displacement )
"""

#app = wx.App()
#f = FancyFrame()
#app.MainLoop()

#######################################################


# CLASS makeDashBoard ---------------------------------------------------------
# This is the GUI entry point
class makeDashBoard(wx.Frame):

	def __init__(self, solarsystem):
		
		newHeight = INFO1_Y+300 # +220
		wx.Frame.__init__(self, None, wx.ID_ANY, title="Orbits Control", size=(500, newHeight))
		
		# create parent panel
		self.Panel = wx.Panel(self, size=(500, newHeight))

		# create notebook to handle tabs
		self.Notebook = wx.Notebook(self.Panel, size=(500, newHeight))

		# create subpanels to be used with tabs
		self.orbitalTab = ORBITALpanel(self, self.Notebook, solarsystem)
		self.searchTab = SEARCHpanel(self, self.Notebook, solarsystem)
		self.focusTab = FOCUSpanel(self, self.Notebook, solarsystem)
		self.widgetsTab = WIDGETSpanel(self, self.Notebook, solarsystem)

		# Bind subpanels to tabs and name them.
		self.Notebook.AddPage(self.orbitalTab, "Main")
		self.Notebook.AddPage(self.focusTab, "Focus")
		self.Notebook.AddPage(self.searchTab, "Search")
		self.Notebook.AddPage(self.widgetsTab, "Widgets")

		#self.getLocationFromIPaddress()

		# if we want flyOver animation
		#if self.AutoRotation.GetValue() == True:
		#	self.orbitalTab.SetAnimationCallback(self.SolarSystem.camera.oneTickCameraCombination, (zoom=True, zoom_forward=True))
			#self.SolarSystem.camera.oneTickCameraCombination(zoom=True, zoom_forward=True)
		self.orbitalTab.Show()

		# create a window to use to display information above the viewPort
		self.infoWindow = createVizualisationWindow(pos=(50, 50), size=(300, 100))

		#self.c = FancyFrame(solarsystem.Scene)

	def setInfoLine(self, text, line):
		self.infoWindow.setLine(text, line)
		
	def showInfoWindow(self, trueFalse):
		self.infoWindow.display(trueFalse)


# CLASS FOCUSpanel ------------------------------------------------------------
# Point of Interest Tab
class FOCUSpanel(AbstractUI):


	def InitVariables(self):
		self.ca_deltaT = 0
		self.smoothTransition = False
#		self.transitionVelocityFactor = 1.0  # normal speed. speed can go as slow as 1/100 and as fast as 4 times the normal speed

		#self.bodyname_to_index = {
		#	CURRENT_BODY: 0, 	SUN_NAME: 1, 		EARTH_NAME: 2, 	"mercury": 3, 	"venus": 4,
		#	"mars": 5, 			"jupiter": 6, 	"saturn": 7, 	"uranus": 8, 	"neptune": 9,
		#	"pluto": 10, 		"sedna": 11, 	"makemake": 12, "haumea": 13, 	"eris": 14, 
		#	"charon": 15, 		"phobos": 16, 	"deimos": 17, 	"moon": 18
		#}

		self.FocusFuncionsSet = {
		 0:	self.setCurrentBodyFocus, 1: self.setSunFocus,
		 2: self.setPlanetFocus, 3: self.setPlanetFocus,
		 4: self.setPlanetFocus, 5: self.setPlanetFocus,
		 6: self.setPlanetFocus, 7: self.setPlanetFocus,
		 8: self.setPlanetFocus, 9: self.setPlanetFocus,
		 10: self.setPlanetFocus, 11: self.setPlanetFocus,
		 12: self.setPlanetFocus, 13: self.setPlanetFocus,
		 14: self.setPlanetFocus, 15: self.setPlanetFocus,
		 16: self.setPlanetFocus, 17: self.setPlanetFocus,
		 18: self.setPlanetFocus }

	def InitUI(self):
		self.BoldFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
		self.RegFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)

		self.Header = wx.StaticText(self, label="", pos=(220, CVT_Y), size=(TOTAL_X-210, 200))
		self.Header.SetFont(self.RegFont)
		self.Header.Wrap(self.GetSize().width)

		Description = "Select which body the animation\nshould focus on. 'Current Object'\nwill follow the last object selected,\nwhether it comes from the Drop\ndown selection, a paused slide-\nshow selection or a Close App-\nroach object pick.\n\nYou may also choose any parti-\ncular planet or the sun."
		self.Header.SetLabel(Description)
		
		lblList = ['Current Object', 'Sun', 'Earth', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Sedna', 'Makemake', 'Haumea','Eris','Charon', 'Phobos', 'Deimos', 'Moon']
		self.rbox = wx.RadioBox(self, label = ' Focus on ', pos = (20, CVT_Y), size=(170, 610), choices = lblList ,majorDimension = 1, style = wx.RA_SPECIFY_COLS)
		self.rbox.SetFont(self.RegFont)
		self.rbox.Bind(wx.EVT_RADIOBOX,self.OnRadioBox)

		self.cb = wx.CheckBox(self, label="Show Local Referential", pos=(200, CVT_FOCUS_Y+40)) #   CVT_Y+560))
		self.cb.SetValue(False)
		self.cb.Bind(wx.EVT_CHECKBOX,self.OnLocalRef)

		self.cbst = wx.CheckBox(self, label="Smooth Transition", pos=(200, CVT_FOCUS_Y+60)) #   CVT_Y+560))
		self.cbst.SetValue(False)
		self.cbst.Bind(wx.EVT_CHECKBOX,self.OnTransition)

		self.Title = wx.StaticText(self, label="", pos=(200, CVT_FOCUS_Y+80), size=(TOTAL_X-210, TOTAL_Y -240))# -160))
		self.Title.SetFont(self.BoldFont)
		self.Info = wx.StaticText(self, label="", pos=(200, CVT_FOCUS_Y+100), size=(TOTAL_X-210, TOTAL_Y -240)) #-160))
		self.Info.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL)) #self.RegFont)

		self.Info.Wrap(self.GetSize().width)
		self.setSunFocus()
		self.resetCameraViewTarget()
		self.Hide()

	def OnTransition(self, e):
		self.smoothTransition = self.cbst.GetValue() 

	"""
	def moveToEarthLocation(self, destination):
		# going from current object to next current object
		print ("SMOOTH FOCUS to", destination)
		#self.SolarSystem.cameraViewTargetBody
		dest = self.SolarSystem.getBodyFromName(destination.lower())
		if dest is not None:
			print ("we got the body info")
			Xc = self.SolarSystem.Scene.center[0]
			Yc = self.SolarSystem.Scene.center[1]
			Zc = self.SolarSystem.Scene.center[2]
			print ("Xc=", Xc, ", Yc=", Yc,", Zc=", Zc)
			
			X = (dest.Position[0] - Xc)/100
			Y = (dest.Position[1] - Yc)/100
			Z = (dest.Position[2] - Zc)/100

			print "X=", X, ", Y=", Y,", Z=", Z

			for i in np.arange(0, 101, 1):
				#g = mag(vector( X0 + 100*i*X, Y0 + 100*i*Y, Z0 + 100*i*Z))
				self.SolarSystem.Scene.center = vector( (Xc + i*X),
														(Yc + i*Y),
														(Zc + i*Z))
				sleep(2e-2)
			#self.Planet.SolarSystem.camera.cameraRefresh()
			#print "forward=", self.Planet.SolarSystem.Scene.forward
			for i in np.arange(0,101, 1):
				print rate_func.ease_in_out(float(i)/100)
		else:
			print "failed to obtain destination"
	"""

	def OnLocalRef(self, e):
		#print ("cameraViewTargetBody:",self.SolarSystem.cameraViewTargetSelection)
		self.setLocalRef()

	def setLocalRef(self):
		#### self.parentFrame.widgetsTab.lrcb.SetValue(self.cb.GetValue())
		self.SolarSystem.setFeature(LOCAL_REFERENTIAL, self.cb.GetValue())
		orbit3D.glbRefresh(self.SolarSystem, self.parentFrame.orbitalTab.AnimationInProgress)

	def setCurrentBodyFocus(self):
		if self.parentFrame.orbitalTab.currentBody is None:
			self.rbox.SetSelection(1)
			#self.SolarSystem.resetView()
			self.setSunFocus()

		else:
			self.SolarSystem.cameraViewTargetBody = self.parentFrame.orbitalTab.currentBody
			###### self.parentFrame.orbitalTab.updateCameraViewTarget()
			self.setBodyFocus(self.SolarSystem.cameraViewTargetBody)

	def setCurrentBodyFocusManually(self, body, selectIndex):
		self.rbox.SetSelection(selectIndex)
		self.parentFrame.orbitalTab.initViewAngle(body)
		self.OnRadioBox(None)
		#self.setBodyFocus(body)

	def getBodyIndexInList(self, bodyName):
		index = bodyname_to_index[bodyName.lower()]
		if index is not None:
			return index
		return bodyname_to_index[SUN_NAME]

	def setBodyFocus(self, Body):
		print "setting body:", Body.Name
		# display planet Info
		if Body.Mass == 0:
			mass = "???"
		else:
			mass = setPrecision(str(Body.Mass), 3)

		radius = Body.BodyRadius/1000 if Body.BodyRadius != 0 and Body.BodyRadius != DEFAULT_RADIUS else 0
#		rev = round(float(Body.Revolution / 365.25) * 1000)/1000
		rev = round(float(Body.Revolution / EARTH_PERIOD) * 1000)/1000

		i = round(float(Body.Inclination) * 1000)/1000
		N = round(float(Body.Longitude_of_ascendingnode) * 1000)/1000
		w = round(float(Body.Argument_of_perihelion) * 1000)/1000
		e = round(float(Body.e) * 1000)/1000
		q = round(float(Body.Perihelion/AU) * 1000)/1000
		a = round(float(Body.Aphelion/AU) * 1000)/1000

		self.Title.SetLabel(Body.Name)
		self.Info.SetLabel("{:<17}{:>10}\n{:<20}{:>7.1f}\n{:<15}{:>12.4f}\n{:<15}{:>12.4f}\n{:<14}{:>10.2f}\n{:<14}{:>10.2f}\n{:<14}{:>10.2f}\n{:<22}{:>5.2f}\n{:<12}{:>7.3f}\n{:<12}{:>7.3f}\n{:<20}{:>7.3f}\n{:<20}{:>7.2f}".
		format(	"Mass(kg) ", mass,
				"Radius(km) ", radius,
				"Perihelion(AU) ", q,
				"Aphelion(AU) ", a,
				"Orb.Period(days) ", Body.Revolution,
				"Orb.Period(yrs)  ", Body.Revolution/EARTH_PERIOD, #365.25,
				"Rot.Period(days) ", Body.Rotation,
				"Orb.Incli.(deg) ", i,
				"Lg.of Asc Node(deg) ", N,
				"Arg. of Perih.(deg) ", w,
				"Eccentricity ", e,
				"Axial Tilt(deg) ", Body.AxialTilt))

		if self.SolarSystem.cameraViewTargetSelection != CURRENT_BODY:
			print "cameraViewTargetBody", self.SolarSystem.cameraViewTargetSelection

			# if object was hidden due to its body type, make body type
			# visible unless it's earth which always stays visible
			if (Body.SolarSystem.ShowFeatures & Body.BodyType) == 0 \
				and Body.Name.lower() != EARTH_NAME:
				#print "MAKING OBJECT VISIBLE"
				# if the body is not visible, Make it so
				#print "Making "+Body.Name+" visible! bodyType = "+str(Body.BodyType)
				#for i in range(len(body.BodyShape)):

				Body.Origin.visible = True
				Body.Labels[0].visible = True
				#planetBody.SolarSystem.ShowFeatures |= planetBody.BodyType
				Body.SolarSystem.setFeature(Body.BodyType, True)
				self.parentFrame.orbitalTab.checkboxList[Body.BodyType].SetValue(True)
				#glbRefresh(self.SolarSystem, self.parentFrame.orbitalTab.AnimationInProgress)

			#else:
			#	print "OBJECT ALREADY VISIBLE"

		self.SolarSystem.cameraViewTargetBody = Body
		#### self.SolarSystem.cameraViewTargetSelection = Body.JPL_designation
		print "cameraViewTargetBody selection is:", self.SolarSystem.cameraViewTargetSelection

		if self.smoothTransition == True:
			self.SolarSystem.camera.smoothFocus(Body.JPL_designation)
		else: # may have to remove "else" just for earth locations management
			self.SolarSystem.camera.updateCameraViewTarget()	

	def setPlanetFocus(self):
		planetBody = self.SolarSystem.getBodyFromName(self.SolarSystem.cameraViewTargetSelection)
		return self.setBodyFocus(planetBody)

	def setSunFocus(self):
		if self.SolarSystem.Sun is not None:
			mass = setPrecision(str(self.SolarSystem.Sun.Mass), 3)

			self.Title.SetLabel(self.SolarSystem.Sun.Name)
			self.Info.SetLabel("{:<17}{:>10}\n{:<19}{:>6.1f}\n{:<14}{:>10.2f}\n{:<20}{:>7.2f}".
			format(	"Mass(kg) ", mass,
					"Radius(km) ", self.SolarSystem.Sun.BodyRadius,
					"Rot.Period(days) ", self.SolarSystem.Sun.Rotation,
					"Axial Tilt(deg) ", self.SolarSystem.Sun.AxialTilt))

			self.resetCameraViewTarget()

	def resetCameraViewTarget(self):
		if self.smoothTransition == True:
			self.SolarSystem.camera.smoothFocus(SUN_NAME)
		else: 
			self.SolarSystem.resetView()
		self.rbox.SetSelection(1)
		self.SolarSystem.cameraViewTargetSelection = SUN_NAME
		self.SolarSystem.cameraViewTargetBody = None

	def OnRadioBox(self, e):
		index = self.rbox.GetSelection()

		# set type of object selected
		#self.SolarSystem.cameraViewTargetSelection = {	0: CURRENT_BODY, 1: SUN_NAME, 	2:EARTH_NAME,	3:"mercury", 	4:"venus",
		#												5: "mars", 		 6:"jupiter", 	7:"saturn", 	8:"uranus", 	9:"neptune",
		#												10:"pluto", 	11:"sedna", 	12:"makemake", 13:"haumea", 	14:"eris", 
		#												15:"charon", 	16: "phobos", 	17:"deimos", 	18:"moon"}[index]
		
		self.SolarSystem.cameraViewTargetSelection = index_to_bodyname[index]

		#self.SolarSystem.cameraViewTargetSelection = {	0: index_to_bodyname[0], 	1: index_to_bodyname[1], 	2: index_to_bodyname[2],	
		#												3: index_to_bodyname[3], 	4: index_to_bodyname[4],	5: index_to_bodyname[5],
		#												6: index_to_bodyname[6], 	7: index_to_bodyname[7], 	8: index_to_bodyname[8], 	
		#												9: index_to_bodyname[9],	10:index_to_bodyname[10], 	11:index_to_bodyname[11], 	
		#												12:index_to_bodyname[12], 	13:index_to_bodyname[13], 	14:index_to_bodyname[14], 
		#												15:index_to_bodyname[15], 	16:index_to_bodyname[16], 	17:index_to_bodyname[17], 	
		#												18:index_to_bodyname[18]}[index]

		# and then call proper focus function
		#{0:	self.setCurrentBodyFocus, 1: self.setSunFocus,
		# 2: self.setPlanetFocus, 3: self.setPlanetFocus,
		# 4: self.setPlanetFocus, 5: self.setPlanetFocus,
		# 6: self.setPlanetFocus, 7: self.setPlanetFocus,
		# 8: self.setPlanetFocus, 9: self.setPlanetFocus,
		# 10: self.setPlanetFocus, 11: self.setPlanetFocus,
		# 12: self.setPlanetFocus, 13: self.setPlanetFocus,
		# 14: self.setPlanetFocus, 15: self.setPlanetFocus,
		# 16: self.setPlanetFocus, 17: self.setPlanetFocus,
		# 18: self.setPlanetFocus }[index]()

		self.FocusFuncionsSet[index]()
		self.setLocalRef()

	def getcameraViewTargetSelection(self):
		return self.SolarSystem.cameraViewTargetSelection

	def OnReset(self, e):
		self.resetCameraViewTarget()



# CLASS SEARCHpanel --------------------------------------------------------------
# Near Earth Objects tab
class SEARCHpanel(AbstractUI):

	def InitVariables(self):
		self.ca_deltaT = 0 # close approach deltaT
		# read NASA API key
		self.LoadAPIKey("data/private-config.json", "data/public-config.json")
		self.searchHostdes = "https://ssd-api.jpl.nasa.gov/sbdb.api?des="
		self.searchHostsstr = "https://ssd-api.jpl.nasa.gov/sbdb.api?sstr="
		self.Hide()

	def LoadAPIKey(self, filename, altfilename):
		fo = None
		try:
			fo = open(filename, "r")
		except IOError:
			fo = open(altfilename, "r")

		js = json.loads(fo.read())

		self.NASA_API_KEY = js["NASA_API_KEY"]
		self.NASA_API_V1_FEED_TODAY = "https://api.nasa.gov/neo/rest/v1/feed?api_key="+self.NASA_API_KEY
		self.NASA_API_V1_FEED_TODAY_URL = "/neo/rest/v1/feed?detailed=true&api_key="+self.NASA_API_KEY
		self.NASA_API_V1_FEED_TODAY_HOST = "https://api.nasa.gov"
		self.NASA_API_HTTPS_HOST = "https://api.nasa.gov"
		self.NASA_API_KEY_DETAILS = "https://api.nasa.gov/neo/rest/v1/neo/"

		# ----------------------------------------------------------------------
		# The nasa API key used for all access to the JPL small objects database
		# This is a personal information that is obtained by submitting a request
		# at https://api.nasa.gov/
		# ----------------------------------------------------------------------

		print "Your API key .......... ", self.NASA_API_KEY


	def InitUI(self):
		self.fetchDate = datetime.date.today()
		self.fetchDateStr = self.fetchDate.strftime('%Y-%m-%d')

		self.BoldFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
		self.RegFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)

		self.heading = wx.StaticText(self, label='Close Approach for '+self.fetchDateStr, pos=(20, JPL_MAIN_HEADING_Y))
		self.heading.SetFont(self.BoldFont)

		self.download = wx.Button(self, label='Download List', pos=(320, JPL_DOWNLOAD_Y))
		self.download.Bind(wx.EVT_BUTTON, self.OnCloseApproach)

		self.next = wx.Button(self, label='Next', pos=(405, JPL_DOWNLOAD_Y), size=(50,35))
		self.next.Bind(wx.EVT_BUTTON, self.OnNext)
		self.next.Hide()

		self.prev = wx.Button(self, label='Prev', pos=(345, JPL_DOWNLOAD_Y), size=(50,35))
		self.prev.Bind(wx.EVT_BUTTON, self.OnPrev)
		self.prev.Hide()

		# type of body search call (BROAD using the sstr endpoint, or DETAILED using the des endpoint)
		self.SRCH_BROAD = 1
		self.SRCH_DETAILED = 2

		self.ListIndex = 0
		self.list = wx.ListCtrl(self, pos=(20, JPL_LISTCTRL_Y), size=(440, JPL_LIST_SZ-50), style = wx.LC_REPORT|wx.BORDER_SUNKEN|wx.LC_HRULES)
		self.list.InsertColumn(0, 'Name', width = 145)
		self.list.InsertColumn(1, 'PHA', wx.LIST_FORMAT_CENTER, width = 45)
		self.list.InsertColumn(2, 'SPK-ID', wx.LIST_FORMAT_CENTER, width = 70)
		self.list.InsertColumn(3, 'Miss Distance ', wx.LIST_FORMAT_RIGHT, width = 175)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnNEOListClick, self.list)

		# list of NEOs explainer text 
		self.legend = wx.StaticText(self, label="", pos=(20, JPL_BRW_Y-55))
		self.legend.SetFont(self.RegFont)
		self.legend.Wrap(230)

		# search box explainer
		self.searchHeader = wx.StaticText(self, label="For a specific body search, enter\nname and press ENTER", pos=(20, JPL_BRW_Y-5))
		self.searchHeader.SetFont(self.RegFont)
		self.searchHeader.Wrap(240)

#		self.search = wx.TextCtrl(self, value="", pos=(20, JPL_SEARCH_Y), size=(200, 25), style=wx.TE_PROCESS_ENTER)
		self.search = wx.TextCtrl(self, value="", pos=(20+220, JPL_BRW_Y), size=(220, 25), style=wx.TE_PROCESS_ENTER)
		self.search.Bind(wx.EVT_TEXT_ENTER, self.onSearch)

		self.searchListIndex = 0
		self.searchList = wx.ListCtrl(self, pos=(20, JPL_BRW_Y+30), size=(440, 90), style = wx.LC_REPORT|wx.BORDER_SUNKEN|wx.LC_HRULES)
		self.searchList.InsertColumn(0, 'Name', width = 120)
		self.searchList.InsertColumn(1, 'Search Name', wx.LIST_FORMAT_CENTER, width = 120)
		self.searchList.InsertColumn(2, 'SPK-ID', wx.LIST_FORMAT_CENTER, width = 195)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnSearchListClick, self.searchList)

		self.SetSize((TOTAL_X, TOTAL_Y))
		self.Centre()
	

	def onSearch(self, e):
		print ("ENTER"+self.search.GetValue())
		self.searchList.DeleteAllItems()
		self.searchByName(self.search.GetValue(), searchtype=self.SRCH_BROAD)
		
	def OnNext(self, e):
		self.oneDay(1, "", self.nextUrl)

	def OnPrev(self, e):
		self.oneDay(-1, "", self.prevUrl)

	def oneDay(self, incr, host, url):
		self.ca_deltaT += incr
		self.fetchDate = datetime.date.today() + datetime.timedelta(days = self.ca_deltaT)
		self.fetchDateStr = self.fetchDate.strftime('%Y-%m-%d')
		self.searchNEOByDay(self.NASA_API_V1_FEED_TODAY_HOST, self.NASA_API_V1_FEED_TODAY_URL)

	def OnCloseApproach(self, e):
		self.download.SetLabel("Fetching ...")
		self.fetchDate = datetime.date.today()
		self.fetchDateStr = self.fetchDate.strftime('%Y-%m-%d')
		self.searchNEOByDay(self.NASA_API_V1_FEED_TODAY_HOST, self.NASA_API_V1_FEED_TODAY_URL)
		self.download.Hide()
		self.next.Show()
		self.prev.Show()
		self.legend.SetLabel("To display orbit details, double click on desired row")

	def doFetchByDay(self, host, url):
		import ssl
		url = url+"&start_date="+self.fetchDateStr+"&end_date="+self.fetchDateStr
		try:

			print host
			print url
			
			req = urllib2.Request(host+url, headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36' })
			gcontext = ssl._create_unverified_context()
			response = urllib2.urlopen(req, context=gcontext)

		except urllib2.HTTPError as err:
			print ("Exception...\n\nError: " + str(err.code))
			raise

		self.BodiesSPK_ID = []
		rawResp = response.read()
		self.jsonResp = json.loads(rawResp)
		#print rawResp

		# use if "prev" not in "links"  
		self.nextUrl = self.jsonResp["links"]["next"] if "next" in self.jsonResp["links"] else ""
		self.prevUrl = self.jsonResp["links"]["prev"] if "prev" in self.jsonResp["links"] else ""
		self.selfUrl = self.jsonResp["links"]["self"] if "self" in self.jsonResp["links"] else ""

		if self.ListIndex != 0:
			self.list.DeleteAllItems()

		self.ListIndex = 0
		if self.jsonResp["element_count"] > 0:
			today = self.jsonResp["near_earth_objects"][self.fetchDateStr]
			for entry in today:
				if entry["close_approach_data"][0]["orbiting_body"].lower() == EARTH_NAME:
					self.list.InsertStringItem(self.ListIndex, entry["name"])
					if entry["is_potentially_hazardous_asteroid"] == True:
							ch = "Y"
					else:
							ch = "N"
					self.list.SetStringItem(self.ListIndex, 1, ch)
					self.list.SetStringItem(self.ListIndex, 2, entry["neo_reference_id"])
					self.list.SetStringItem(self.ListIndex, 3, str(round(float(entry["close_approach_data"][0]["miss_distance"]["lunar"]) * 100)/100)  +
											" LD | " + str(round(float(entry["close_approach_data"][0]["miss_distance"]["astronomical"]) * 100)/100) + " AU ")
					# record the spk-id corresponding to this row
					self.BodiesSPK_ID.append(entry["neo_reference_id"])
					self.ListIndex += 1
		
		# enable buttons to unlock date
		self.next.Enable()
		self.prev.Enable()
		self.heading.SetLabel('Close Approaches On '+self.fetchDateStr)

	def searchNEOByDay(self, host, url):
		
		# check the new target day has been cached already
		#if self.fetchDateStr in self.jsonResp["near_earth_objects"]:
			# if yes, directly load info in self.SolarSystem.objects_data 
		#	self.doFetchByDayFromCache()
		#else:
		# start a new thread to retrieve the list of NEOs from JPL
		jplThread = threading.Thread(target=self.doFetchByDay, name="SearchByDay", args=[host, url] )
		jplThread.start()

		# disable buttons to lock date (button will be unlocked by the callJPL thread)
		self.next.Disable()
		self.prev.Disable()


	def OnNEOListClick(self, e):
		# load orbital elements
		id = self.loadBodyInfoFromDaily(e.m_itemIndex)
		if id > 0:
			
			# switch to main panel to display orbit
			self.nb.SetSelection(PANEL_MAIN)
			
			# If slide show in progress, stop it, and reset body List
			self.parentFrame.orbitalTab.stopSlideSHow()
			self.parentFrame.orbitalTab.resetBodyList()

			# make sure to reset the date using the selected object close encounter date time (provided as UTC)
			self.parentFrame.orbitalTab.resetDateFromBodyId(id)
			############self.parentFrame.orbitalTab.refreshDate()

			self.parentFrame.orbitalTab.setCurrentBodyFromId(id)
			if self.SolarSystem.cameraViewTargetSelection == CURRENT_BODY:
				self.SolarSystem.cameraViewTargetBody = self.parentFrame.orbitalTab.currentBody
				self.SolarSystem.camera.updateCameraViewTarget()	
				#self.parentFrame.orbitalTab.updateCameraViewTarget()
			toggle = False
			if self.SolarSystem.isRealsize():
				toggle = True
			self.parentFrame.orbitalTab.currentBody.toggleSize(toggle)



	def doFetchByName(self, host, target, type):
		#print (host+target+"\n")
		multiple = False
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36')]
			print "Querying: ", host+target
			response = opener.open(host+target)
			rawResp = response.read()

		except urllib2.HTTPError as err:
			if err.code == 300:
				# catch multiple results exception
				multiple = True
				rawResp = err.fp.read()
			else:
				print ("Exception...\n\nError: " + str(err.code))
				raise

		self.jsonBNResp = json.loads(rawResp)
		print (rawResp)

		# check if there are multiple results or not
		if type == self.SRCH_BROAD:
			if self.searchListIndex != 0:
				self.searchList.DeleteAllItems()
				self.searchListIndex = 0

			if multiple:

				# load searchList with results
				for entry in self.jsonBNResp["list"]:
					self.searchList.InsertStringItem(self.searchListIndex, entry["name"])
					self.searchList.SetStringItem(self.searchListIndex, 1, entry["pdes"])
					self.searchList.SetStringItem(self.searchListIndex, 2, "")
					self.searchListIndex += 1
				return 0

			# we have a unique result, hence insert it in the list
			entry = self.jsonBNResp
			if "object" not in entry:
				self.search.SetValue(self.search.GetValue() + " <no result>")
				return -1

			self.searchList.InsertStringItem(self.searchListIndex, entry["object"]["fullname"])
			self.searchList.SetStringItem(self.searchListIndex, 1, entry["object"]["des"])
			self.searchList.SetStringItem(self.searchListIndex, 2, entry["object"]["spkid"])
			self.searchListIndex += 1
			return 0

		# for "DETAILED" search, load body and draw its orbit
		print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
		id = self.loadBodyInfoFromSearch()
		if id > 0:
			#self.parentFrame.orbitalTab.refreshDate()
			# switch to main panel to display orbit
			self.nb.SetSelection(PANEL_MAIN)

			# If slide show in progress, stop it, and reset body List
			self.parentFrame.orbitalTab.stopSlideSHow()
			self.parentFrame.orbitalTab.resetBodyList()

			##########self.parentFrame.orbitalTab.refreshDate()

			self.parentFrame.orbitalTab.setCurrentBodyFromId(id)
			if self.SolarSystem.cameraViewTargetSelection == CURRENT_BODY:
				self.SolarSystem.cameraViewTargetBody = self.parentFrame.orbitalTab.currentBody
				#self.parentFrame.orbitalTab.updateCameraViewTarget()
				self.SolarSystem.camera.updateCameraViewTarget()	
				
			toggle = False
			if self.SolarSystem.isRealsize():
				toggle = True
			self.parentFrame.orbitalTab.currentBody.toggleSize(toggle)

		return id

	# Note: for spacecraft search, the small objects database won't work. 
	# Instead the Horizon system web scrapping should be used instead
	
	def searchByName(self, url, searchtype):

		# add code here
		if searchtype == self.SRCH_DETAILED:
			host = self.searchHostdes
		else:
			host = self.searchHostsstr

		# start a new thread to retrieve a particular body from JPL. The
		#jplThread = threading.Thread(target=self.doFetchByName, name="SearchByName", args=[host, urllib.quote(url), searchtype] )
		#jplThread.start()

		self.doFetchByName(host, urllib.quote(url), searchtype)
		#self.doFetchByName(host, "%2D226", searchtype)
		

	def OnSearchListClick(self, e):
		pdes = self.searchList.GetItem(itemId=e.m_itemIndex, col=1).GetText()
		#print("searching -> "+self.searchHostdes+pdes)
#		self.searchByName(self.searchHostdes, pdes, searchtype = self.SRCH_DETAILED)
		self.searchByName(pdes, searchtype = self.SRCH_DETAILED)


	# attempt to use SPICE functions to obtain orbital elements
	def GetOcltx(self, objectId, timeincrement):
		# load spice files from meta kernel
		spice.furnsh("spice/spice-kernels/solarsys_metakernel.mk")

		_, GM_SUN_PRE = spice.bodvcd(10, item='GM', maxn=1)
		print GM_SUN_PRE

		# odt contains the date (as string) we want to get ocultation info for
		et = spice.str2et(self.fetchDateStr) # 'Apr 13, 2021' );
		print et

		# 	state, ltime = spice.spkezr( 'EARTH', et, 'ECLIPJ2000', 'LT+S', 'SUN' );
		state, ltime = spice.spkezr( objectId, et, FRAME, 'LT+S', 'SUN' );

		y = spice.oscltx( state, et, GM_SUN_PRE[0] );
		print "=========="
		print "Perifocal:" + str(y[0]) + " km"
		print "Eccentricity:"+str(y[1])
		
		print "Inclination:"+str(rad2deg(y[2])) + " deg"
		print "Long.Ascending Node:"+str(rad2deg(y[3])) + " deg"
		print "Argumt of periapsis:"+str(rad2deg(y[4])) + " deg"
		print "Mean anomaly:"+str(rad2deg(y[5]))
		print "Epoch:"+str(y[6])
		print "MU:"+str(y[7])
		print "NU:"+str(rad2deg(y[8])) + " deg/s"
		print "Semi-major:"+str(y[9])
		print "Period:"+str(y[10]/86400) + " d"
		return y


	def loadBodyInfoFromSearch(self):
		#entry = self.jsonResp["near_earth_objects"][self.fetchDateStr][index]
		#print entry
		#utc_close_approach = datetime.datetime.fromtimestamp(2459600.5)
		#print ("FROM_TIMESTAMP = ", utc_close_approach)
		
		entry = self.jsonBNResp
		if "object" not in entry:
			return -1

		spkid = entry["object"]["spkid"]

		# if the key already exists, the object has already been loaded, simply return its spk-id
		if spkid in self.SolarSystem.objects_data:
			return spkid

		print ("SPKID="+ spkid)

		self.SolarSystem.objects_data[spkid] = {
			"material": 0,
			# epoch_date_close_approach comes as the number of milliseconds in unix TT
#			"epoch_date_close_approach": utc_close_approach, # in seconds using J2000
			"name": entry["object"]["fullname"],
			"iau_name": entry["object"]["des"],
			"jpl_designation": entry["object"]["spkid"],
			"epochJD": float(entry["orbit"]["epoch"]),
			"mass": 0.0,
			"radius": DEFAULT_RADIUS,
			"earth_moid": float(entry["orbit"]["moid"]) * AU,
			"orbit_class": entry["object"]["orbit_class"]["name"],
			"axial_tilt": 0.0,
			"absolute_mag": 0.0
		}

		om = W = 0.0
		# add what follows through a loop going through all elements of entry["orbit"]["elements"]
		for elt in entry["orbit"]["elements"]:
			if elt["name"] == "e":
				self.SolarSystem.objects_data[spkid].update({"EC_e": float(elt["value"])})
			elif elt["name"] == "q":
				self.SolarSystem.objects_data[spkid].update({"QR_perihelion": float(elt["value"]) * AU})
			elif elt["name"] == "i":
				self.SolarSystem.objects_data[spkid].update({"IN_orbital_inclination": float(elt["value"])})
			elif elt["name"] == "om":
				om = float(elt["value"])
				self.SolarSystem.objects_data[spkid].update({"OM_longitude_of_ascendingnode": om})
			elif elt["name"] == "w":
				W = float(elt["value"])
				self.SolarSystem.objects_data[spkid].update({"W_argument_of_perihelion": W})
			elif elt["name"] == "ma":
				self.SolarSystem.objects_data[spkid].update({"MA_mean_anomaly": float(elt["value"])})
			elif elt["name"] == "tp":
				self.SolarSystem.objects_data[spkid].update({"Tp_Time_of_perihelion_passage_JD": float(elt["value"])}) # value unit in "TDB" (Time Dynamic Baricenter)
			elif elt["name"] == "per":
				self.SolarSystem.objects_data[spkid].update({"PR_revolution": float(elt["value"])})
			elif elt["name"] == "n":
				self.SolarSystem.objects_data[spkid].update({"N_mean_motion": float(elt["value"])})

		self.SolarSystem.objects_data[spkid].update({"longitude_of_perihelion": om+W})

		print (self.SolarSystem.objects_data[spkid])

		# for now let's consider "search" bodies as PHAs
		body = orbit3D.makePha(self.SolarSystem, spkid, color.white) #orbit3D.getColor())
		self.SolarSystem.addTo(body)
		return spkid

	def loadBodyInfoFromDaily(self, index):

		if "near_earth_objects" not in self.jsonResp:
			return -1

		entry = self.jsonResp["near_earth_objects"][self.fetchDateStr][index]
		#print entry

		# if the key already exists, the object has already been loaded, simply return its spk-id
		if entry["neo_reference_id"] in self.SolarSystem.objects_data:
			if "utc_dt" in self.SolarSystem.objects_data[entry["neo_reference_id"]]:
				return entry["neo_reference_id"]
			else:
				# object was previously loaded from normal search but lack time of close 
				# approach ("utc_dt") hence we must reload it with this extra information
				del(self.SolarSystem.objects_data[entry["neo_reference_id"]])

		# grab utc timestamp of encounter time and date (value is in ms, hence divide by 1000 to get the value in seconds)
		utc_timestamp = entry["close_approach_data"][0]["epoch_date_close_approach"]*0.001
		
		# make a datetime off of that timestamp 
		utc_close_approach = datetime.datetime.fromtimestamp(utc_timestamp)
		utc_close_approach = utc_close_approach.replace(tzinfo=pytz.utc)

		print "*******************"
		print "FROM_TIMESTAMP = ", utc_close_approach, ", WITH TZ info=", datetime.datetime.fromtimestamp(utc_timestamp, tz=self.SolarSystem.locationInfo.getPytzValue())
		print "*******************"

		# utc_close_approach is a naive datetime object
		print "LOADBODY_INFO utc_close_approach= ", utc_close_approach, "UTC from timestamp=", utc_timestamp

		# Add data to dictionary
		self.SolarSystem.objects_data[entry["neo_reference_id"]] = {
			"material": 0,
			# epoch_date_close_approach comes as the number of milliseconds in unix TT
			"epoch_date_close_approach": utc_close_approach, # in seconds using J2000
			"name": entry["name"],
			"iau_name": entry["name"],
			"jpl_designation": entry["neo_reference_id"],
			"mass": 0.0,
			"radius": float(entry["estimated_diameter"]["kilometers"]["estimated_diameter_max"])*0.5, # if float(entry["estimated_diameter"]["kilometers"]["estimated_diameter_max"])/2 > DEFAULT_RADIUS else DEFAULT_RADIUS,
			"QR_perihelion": float(entry["orbital_data"]["perihelion_distance"]) * AU,
			"EC_e": float(entry["orbital_data"]["eccentricity"]),
			"PR_revolution": float(entry["orbital_data"]["orbital_period"]),
			"IN_orbital_inclination": float(entry["orbital_data"]["inclination"]),
			"OM_longitude_of_ascendingnode":float(entry["orbital_data"]["ascending_node_longitude"]),
			"W_argument_of_perihelion": float(entry["orbital_data"]["perihelion_argument"]),
			"longitude_of_perihelion": float(entry["orbital_data"]["ascending_node_longitude"])+float(entry["orbital_data"]["perihelion_argument"]),
			"Tp_Time_of_perihelion_passage_JD": float(entry["orbital_data"]["perihelion_time"]),
			"N_mean_motion": float(entry["orbital_data"]["mean_motion"]),
			"MA_mean_anomaly": float(entry["orbital_data"]["mean_anomaly"]),
			"epochJD": float(entry["orbital_data"]["epoch_osculation"]),
			"earth_moid": float(entry["orbital_data"]["minimum_orbit_intersection"]) * AU,
			"orbit_class": "N/A",
			"absolute_mag": float(entry["absolute_magnitude_h"]),
			"axial_tilt": 0.0,
			"utcstr": utc_close_approach.strftime('%Y-%m-%d %H:%M:%S'),
			"utc_dt": utc_close_approach,
			"local_dt": orbit3D.utc_to_local_fromTimestamp(utc_timestamp, self.SolarSystem.locationInfo)
		}

		#print "UTC time of approach   =========>", self.SolarSystem.objects_data[entry["neo_reference_id"]]["utc_dt"]
		#print "Local time of approach --------->", self.SolarSystem.objects_data[entry["neo_reference_id"]]["local_dt"]

		# convert UTC to local time
		utcNewdatetime = self.SolarSystem.objects_data[entry["neo_reference_id"]]["utc_dt"]
		LocNewdatetime = self.SolarSystem.objects_data[entry["neo_reference_id"]]["local_dt"]

		# print time of closest approach on this date
 		print ">>> Local Time of approach: ", self.SolarSystem.objects_data[entry["neo_reference_id"]]["local_dt"]

		# CLose approach objects are considered as PHAs
		body = orbit3D.makePha(self.SolarSystem, entry["neo_reference_id"], orbit3D.getColor())
		self.SolarSystem.addTo(body)

		print "UTC time of approach   =========>", utcNewdatetime
		print "Local time of approach --------->", LocNewdatetime

		# update timeStamps
		self.parentFrame.orbitalTab.updateTimeStamps(LocNewdatetime, utcNewdatetime)

		# update texture and widgets references
		self.parentFrame.widgetsTab.Earth.setTextureFromSolarTime(LocNewdatetime)

		# we return the index of the object in array of cosmic bodies
		# (to access the data, retrieve self.SolarSystem.objects_data[index])
		return entry["neo_reference_id"]


# CLASS ORBITALpanel ------------------------------------------------------
# Orbital control tab
class ORBITALpanel(AbstractUI):

	def InitVariables(self):
		self.Earth = self.SolarSystem.getBodyFromName(EARTH_NAME)
		self.checkboxList = {}
		self.ResumeSlideShowLabel = False
		self.AnimationInProgress = False
		self.Source = PHA
		self.TimeIncrement = INITIAL_TIMEINCR
		self.BaseTimeIncrement = INITIAL_TIMEINCR
		self.TimeIncrementKey = INITIAL_INCREMENT_KEY
		self.AnimLoop = 0
		self.surfaceRadius = 0.0  # used for surface focus
		self.todayUTCdatetime = self.SolarSystem.locationInfo.getUTCDateTime()
		self.new_utcDatetime = self.todayUTCdatetime
		self.new_localDatetime = self.todayUTCdatetime


#		self.DaysIncrement = 0 # number of days from today - used for animation into future or past (detalT < 0)
		self.DeltaT = 0
		self.velocity = 0
		self.distance = 0
		self.list = []
		self.listjplid = []
		self.DetailsOn = False
		self.currentBody = None
		self.DisableAnimationCallback = True
		self.RecorderOn = False
		self.VideoRecorder = None
		self.earthLoc = None
		self.viewAngle = 0
		self.followModeView = False
		self.Hide()

	def initViewAngle(self, body):
		# update viewAngle with current body view Angle
		print "init view angle for", body.Name 
		self.viewAngle = atan2(body.Position[1], body.Position[0])

	def resetDateFromBodyId(self, id):
		diff =  self.SolarSystem.objects_data[id]["utc_dt"] - self.todayUTCdatetime
		self.DeltaT = diff.total_seconds()/86400.0
		print "ResetDateFromBodyId: DELTA from right now (in days) =", self.DeltaT
		self.updateSolarSystem()
		return

	def createBodyList(self, xpos, ypos):
		for body in self.SolarSystem.bodies:
			if body.BodyType in [SPACECRAFT, PHA, BIG_ASTEROID, COMET, TRANS_NEPT]:
				self.list.append(body.Name)
				self.listjplid.append(body.JPL_designation.lower())

		self.comb = wx.ComboBox(self, id=wx.ID_ANY, value="Select Object Individually", size=wx.DefaultSize, pos=(xpos, ypos), choices=self.list, style=(wx.CB_DROPDOWN))
		self.comb.Bind(wx.EVT_COMBOBOX, self.OnSelect)

	def resetBodyList(self):
		self.comb.SetSelection(-1)
		self.comb.SetValue("Select Object Individually")

	def OnSelect(self, e):
		#if self.SolarSystem.SlideShowInProgress == False:
			index = e.GetSelection()
			jpl_designation = self.listjplid[index]
			self.setCurrentBodyFromId(jpl_designation)
			if self.SolarSystem.cameraViewTargetSelection == CURRENT_BODY:
				print ""
				print "CHANGING CURRENT OBJECT"
				print ""
				self.SolarSystem.cameraViewTargetBody = self.currentBody
				self.parentFrame.focusTab.setBodyFocus(self.currentBody)
				#self.updateCameraViewTarget()
				self.SolarSystem.camera.updateCameraViewTarget()	

			else:
				print "OnSELECT: cameraViewTargetBody is", self.SolarSystem.cameraViewTargetBody.Name, "current ViewTarget selection type is", self.SolarSystem.cameraViewTargetSelection

	def setCurrentBody(self, body):
		if self.currentBody is not None:
			self.currentBody.hide()

		self.currentBody = body
		self.currentBody.Details = True
		self.showObjectDetails(self.currentBody)

	def setCurrentBodyFromId(self, id):
		if self.currentBody is not None:
			self.currentBody.hide()

		body = self.SolarSystem.getBodyFromName(id)
		if body is not None:
			self.currentBody = body
			self.initViewAngle(body)
			self.currentBody.Details = True
			#print "Current body SET-1 with ", self.currentBody.Name, "Origin=",self.currentBody.Origin.pos
			#print ""
			self.showObjectDetails(self.currentBody)
			print "\nBODY:",body.Name, "\nposition=",body.Position, "\nbody.pos=",body.BodyShape.pos, "\nlabels.pos=", body.Labels[0].pos, "\norigin.pos=",body.Origin.pos
		else:
			print "SetCurrentBodyFromId: could not find", id
		#print "Current body SET-2 with ", self.currentBody.Name, "Origin=",self.currentBody.Origin.pos

	def setCurrentBodyFromIdSAVE(self, id):
		if self.currentBody is not None:
			self.currentBody.hide()

		self.currentBody = self.SolarSystem.getBodyFromName(id)
		self.currentBody.Details = True
		#print "Current body SET-1 with ", self.currentBody.Name, "Origin=",self.currentBody.Origin.pos
		#print ""
		self.showObjectDetails(self.currentBody)
		#print "Current body SET-2 with ", self.currentBody.Name, "Origin=",self.currentBody.Origin.pos

	def updateTimeStamps(self, ldt, utcdt):
		self.setLocalDateTimeLabel(ldt)
		self.setUTCDateTimeLabel(utcdt)

	def setLocalDateTimeLabel(self, ldt):
		self.localTimeLabel.SetLabel("{:>2}:{:>2}:{:2}".format(str(ldt.hour).zfill(2), str(ldt.minute).zfill(2), str(ldt.second).zfill(2)))
		#print ("{:>2}:{:>2}:{:2}".format(str(ldt.hour).zfill(2), str(ldt.minute).zfill(2), str(ldt.second).zfill(2)))

		self.localDateLabel.SetLabel("{:>2}/{:>2}/{:2}".format(str(ldt.month).zfill(2), str(ldt.day).zfill(2), str(ldt.year).zfill(2)))
		#print ("{:>2}/{:>2}/{:2}".format(str(ldt.month).zfill(2), str(ldt.day).zfill(2), str(ldt.year).zfill(2)))

	def setUTCDateTimeLabel(self, utcdt):
		self.UTCtimeLabel.SetLabel("{:>2}:{:>2}:{:2}".format(str(utcdt.hour).zfill(2), str(utcdt.minute).zfill(2), str(utcdt.second).zfill(2)))
		self.UTCdateLabel.SetLabel("{:>2}/{:>2}/{:2}".format(str(utcdt.month).zfill(2), str(utcdt.day).zfill(2), str(utcdt.year).zfill(2)))

	def InitUI(self):
		self.BoldFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
		self.RegFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)

		heading = wx.StaticText(self, label='Show', pos=(20, MAIN_HEADING_Y))
		heading.SetFont(self.BoldFont)

		OFF_TIME = 0
		dateLabel = wx.StaticText(self, label='Orbital Date (UTC)', pos=(MAIN_MIDDLE_X, DATE_Y))
		dateLabel.SetFont(self.BoldFont)
		wx.StaticText(self, label='Local Time: ', pos=(MAIN_MIDDLE_X+OFF_TIME, DATE_Y-18))
		wx.StaticText(self, label='Universal Time:', pos=(MAIN_MIDDLE_X+OFF_TIME, DATE_Y-33))

		self.localTimeLabel = wx.StaticText(self, label='hh:mm:ss', pos=(280+OFF_TIME+5, DATE_Y-18))
		self.localDateLabel = wx.StaticText(self, label='mm/dd/yyyy', pos=(280+OFF_TIME+75, DATE_Y-18))
		self.UTCtimeLabel = wx.StaticText(self, label='hh:mm:ss', pos=(280+OFF_TIME+5, DATE_Y-33))
		self.UTCdateLabel = wx.StaticText(self, label='mm/dd/yyyy', pos=(280+OFF_TIME+75, DATE_Y-33))

		lt = self.SolarSystem.locationInfo.getLocalDateTime()

		self.setLocalDateTimeLabel(lt)
		self.setUTCDateTimeLabel(self.todayUTCdatetime)

		# date spinner
		self.dateMSpin = wx.SpinCtrl(self, id=wx.ID_ANY, initial=self.todayUTCdatetime.month, min=1, max=12, pos=(MAIN_MIDDLE_X, DATE_SLD_Y), size=(60,25), style=wx.SP_ARROW_KEYS)
		self.dateMSpin.Bind(wx.EVT_SPINCTRL,self.OnTimeSpin)
		self.dateDSpin = wx.SpinCtrl(self, id=wx.ID_ANY, initial=self.todayUTCdatetime.day, min=1, max=31, pos=(MAIN_MIDDLE_X+62, DATE_SLD_Y), size=(60, 25), style=wx.SP_ARROW_KEYS)
		self.dateDSpin.Bind(wx.EVT_SPINCTRL,self.OnTimeSpin)

		# Create a custom event in order to update the content of the day spinner if its value is out-of-range
		self.CustomEvent, EVT_RESET_SPINNER = wx.lib.newevent.NewEvent()
		self.dateDSpin.Bind(EVT_RESET_SPINNER, self.ResetSpinner) # bind it as usual
		# The day spinner has 2 events. one triggered when clicking on an arrow, and one
		# triggered programmatically to update the value of the day spinner in order to correct it
		# The firing of the EVT_RESET_SPINNER is programmatically done during the execution
		# of the EVT_SPINCTRL handler


		self.dateYSpin = wx.SpinCtrl(self, id=wx.ID_ANY, initial=self.todayUTCdatetime.year, min=-3000, max=3000, pos=(MAIN_MIDDLE_X+124, DATE_SLD_Y), size=(60, 25), style=wx.SP_ARROW_KEYS)
		self.dateYSpin.Bind(wx.EVT_SPINCTRL,self.OnTimeSpin)

		self.ValidateDate = wx.Button(self, label='Set', pos=(400, DATE_SLD_Y), size=(60, 25))
		self.ValidateDate.Bind(wx.EVT_BUTTON, self.OnValidateDate)


		self.createCheckBox(self, "Inner Planets", INNERPLANET, 20, CHK_L1)
		self.createCheckBox(self, "Orbits", ORBITS, 20, CHK_L2)
		self.createCheckBox(self, "Outer Planets", OUTERPLANET, 20, CHK_L3)
		self.createCheckBox(self, "Dwarf Planets", DWARFPLANET, 20, CHK_L4)
		self.createCheckBox(self, "Asteroids Belt", ASTEROID_BELT, 20, CHK_L5)
		self.createCheckBox(self, "Jupiter Trojans", JTROJANS, 20, CHK_L6)
		self.createCheckBox(self, "Kuiper Belt", KUIPER_BELT, 20, CHK_L7)
		#self.createCheckBox(self, "Inner Oort Cloud", INNER_OORT_CLOUD, 20, CHK_L8)
		self.createCheckBox(self, "Celestial Sphere", CELESTIAL_SPHERE, 20, CHK_L8)
		self.createCheckBox(self, "Constellations", CONSTELLATIONS, 20, CHK_L9)
		
		self.createCheckBox(self, "Ecliptic", ECLIPTIC_PLANE, 20, CHK_L10)
		self.createCheckBox(self, "Labels", LABELS, 20, CHK_L11)
		self.createCheckBox(self, "Lit Scene", LIT_SCENE, 20, CHK_L12)
		self.createCheckBox(self, "Adjust objects size", REALSIZE, 20, CHK_L13)
		self.createCheckBox(self, "Referential", REFERENTIAL, 20, CHK_L14)

		self.createBodyList(200, LSTB_Y)

		cbtn = wx.Button(self, label='Refresh', pos=(20, CHK_L15))
		cbtn.Bind(wx.EVT_BUTTON, self.OnRefresh)

		lblList = ['PHA', 'Comets', 'Major Asteroids', 'Trans Neptunians']
		self.rbox = wx.RadioBox(self,label = 'Slideshow', pos = (200, SLDS_Y), size=(165, 170), choices = lblList ,majorDimension = 1, style = wx.RA_SPECIFY_COLS)
		self.rbox.SetFont(self.RegFont)
		self.rbox.Bind(wx.EVT_RADIOBOX,self.OnRadioBox)

		self.SlideShow = wx.Button(self, label='Start', pos=(370, SLDS_Y))
		self.SlideShow.Bind(wx.EVT_BUTTON, self.OnSlideShow)

		self.Pause = wx.Button(self, label='Pause', pos=(370, PAU_Y))
		self.Pause.Bind(wx.EVT_BUTTON, self.OnPauseSlideShow)
		self.Pause.Hide()

		# Time slider

		self.sliderTitle = wx.StaticText(self, label="Frame Interval: ", pos=(200-30, ANI_Y), size=(60, 20))
		self.sliderTitle.SetFont(self.BoldFont)

		self.aniTime = wx.StaticText(self, label= "%s %s" % (Frame_Intervals[self.TimeIncrementKey]["label"], Frame_Intervals[self.TimeIncrementKey]["unit"]), pos=(250, ANI_Y+30), size=(15, 20))
		self.aniTime.SetFont(self.BoldFont)
		self.aniTimeSlider = wx.Slider(self, id=wx.ID_ANY, value=1, minValue=1, maxValue=10, pos=(195, ANI_Y+50), size=(150, 20), style=wx.SL_HORIZONTAL)
		self.aniTimeSlider.Bind(wx.EVT_SLIDER,self.OnAnimTimeSlider) 

		# Speed slider

		self.aniSpeed = wx.StaticText(self, label= "%s %s" % (Frame_Intervals[self.TimeIncrementKey]["label"], Frame_Intervals[self.TimeIncrementKey]["unit"]), pos=(305, ANI_Y), size=(15, 20))
		self.aniSpeed.SetFont(self.BoldFont)
		self.aniSpeedSlider = wx.Slider(self, id=wx.ID_ANY, value=1, minValue=-24, maxValue=24, pos=(195, ANI_Y+30), size=(150, 20), style=wx.SL_HORIZONTAL)
		self.aniSpeedSlider.Bind(wx.EVT_SLIDER,self.OnAnimSpeedSlider)


		self.Animate = wx.Button(self, label='>', pos=(360, ANI_Y), size=(35, 35))
		self.Animate.Bind(wx.EVT_BUTTON, self.OnAnimate)

		self.Stepper = wx.Button(self, label='+', pos=(395, ANI_Y), size=(35, 35))
		self.Stepper.Bind(wx.EVT_BUTTON, self.OnStepper)

		# u'\u25a0' = square character
		self.Recorder = wx.Button(self, label=u'\u25a0', pos=(440, ANI_Y), size=(35, 35))
		self.Recorder.Bind(wx.EVT_BUTTON, self.OnRecord)

		self.AutoRotation = wx.CheckBox(self, label="Auto-Rotation in Animation", pos=(200-30, DET_Y-40))
		self.AutoRotation.SetValue(False)
		self.AutoRotation.Bind(wx.EVT_CHECKBOX,self.OnAutoAnimationClick)

		self.followMode = wx.CheckBox(self, label="Follow Mode", pos=(200-30, DET_Y-20))
		self.followMode.SetValue(False)
		self.followMode.Bind(wx.EVT_CHECKBOX,self.OnFollowModeClick)

		#
		# current object details
		#

		self.InfoTitle = wx.StaticText(self, label="", pos=(20, DET_Y))
		self.InfoTitle.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

		self.ObjVelocity = wx.StaticText(self, label="", pos=(240, DET_Y+20), size=(130, 20))
		self.ObjDistance = wx.StaticText(self, label="", pos=(240, DET_Y+40), size=(130, 20))
		#self.ObjVelocity.SetFont(self.RegFont)
		self.ObjVelocity.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))
		self.ObjDistance.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))

		self.Info1 = wx.StaticText(self, label="", pos=(20, INFO1_Y))
		self.Info1.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL)) #self.RegFont)
		#self.Info1.SetFont(self.RegFont)
		self.Info1.Wrap(230)
		self.Info2 = wx.StaticText(self, label="", pos=(240, INFO1_Y+38)) #+19))
		self.Info2.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL)) #self.RegFont)
		self.Info2.Wrap(250)

		self.SetSize((TOTAL_X, TOTAL_Y))
		self.Centre()

		#self.setDeltaT()

	def OnAutoAnimationClick(self, e):
		# enable / disable mouse tracking based on auto animation status
		self.SolarSystem._set_autoMovement(self.AutoRotation.GetValue())
		wx.Event.Skip(e, True)

	def OnFollowModeClick(self, e):
		self.followModeView = self.followMode.GetValue()

	def setCameraViewTarget(self, body):
		self.SolarSystem.cameraViewTargetBody = body

	def updateCameraViewTarget_ADV_XX(self):

		# the following values will do the following
		# (0,-1,-1): freezes rotation and looks down towards the left
		# (0,-1, 1): freezes rotation and looks up towards the left
		# (0, 1, 1): freezes rotation and looks up towards the right
		# (0, 1,-1): freezes rotation and looks down towards the right

		#self.SolarSystem.Scene.forward = (0, 0, -1)
		# For a planet, Foci(x, y, z) is (0,0,0). For a moon, Foci represents the position of the planet the moon orbits around
		####surfaceRadius = (1.1 * self.SolarSystem.cameraViewTargetBody.BodyShape.radius) if self.SolarSystem.SurfaceView == True else 0
		surfaceRadius = 0.0
		if self.SolarSystem.SurfaceView == True:
			surfaceRadius = (1.3 * self.SolarSystem.cameraViewTargetBody.BodyShape.radius)
		#print "surfaceRadius = ", surfaceRadius

		self.SolarSystem.Scene.center = (
			self.SolarSystem.cameraViewTargetBody.Position[0]+self.SolarSystem.cameraViewTargetBody.Foci[0]+surfaceRadius * self.SolarSystem.SurfaceDirection[0],
			self.SolarSystem.cameraViewTargetBody.Position[1]+self.SolarSystem.cameraViewTargetBody.Foci[1]+surfaceRadius * self.SolarSystem.SurfaceDirection[1],
			self.SolarSystem.cameraViewTargetBody.Position[2]+self.SolarSystem.cameraViewTargetBody.Foci[2]+surfaceRadius * self.SolarSystem.SurfaceDirection[2]
		)
	
	"""
	def updateCameraViewTarget(self, loc = None):
		if loc != None:
			print "Location is", loc.Name

		if self.SolarSystem.cameraViewTargetBody == None:
			print "no curent object"
			return

		if self.SolarSystem.cameraViewTargetBody.Name.lower() == EARTH_NAME:
			earthLocPos = None
			w = self.Earth.PlanetWidgets
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

	"""			
	

	def updateSolarSystem(self):
		# animate all visible bodies in the solar system 
		self.refreshDate()
		#self.SolarSystem.animate(self.DeltaT)
		for body in self.SolarSystem.bodies:
			if body.BodyType in [SUN, SPACECRAFT, OUTERPLANET, INNERPLANET, SATELLITE, ASTEROID, \
								 COMET, DWARFPLANET, PHA, BIG_ASTEROID, TRANS_NEPT]:
				if body.Origin.visible == True or body.Name.lower() == EARTH_NAME:
					velocity, distance = body.animate(self.DeltaT)
					if self.SolarSystem.cameraViewTargetBody is not None:
						# update center position if we are NOT in the middle of a smooth transition and
						# NOT in a location Referential view mode (point of view from current location)
						if body.JPL_designation == self.SolarSystem.cameraViewTargetBody.JPL_designation and \
							(self.SolarSystem.Dashboard.focusTab.smoothTransition == False and \
							 self.SolarSystem.Dashboard.widgetsTab.Earth.PlanetWidgets.locationEarthEyeView == False):
							self.SolarSystem.camera.updateCameraViewTarget()

					if body.BodyType == self.Source or body.Details == True:
						self.velocity = velocity
						self.distance = distance

			#else:
			#	print("UNKNOWN BODYTYPE:", body.BodyType)

	def OnValidateDate(self, e):
		# typically the date spinner only changes the date. We keep the current time. 
		# Obtain the displayed UTC time hh:mm:ss 
		utctime = self.UTCtimeLabel.GetLabel().split(":")
		if len(utctime) <= 0:
			utctime = ["00","00","00"]

		# the date in the spinners is the UTC date
		# make new utc date using spinner for mm/dd/yyyy and utctime for hh:mm:ss 
		new_utcDatetime = datetime.datetime(self.dateYSpin.GetValue(), self.dateMSpin.GetValue(), self.dateDSpin.GetValue(), int(utctime[0]), int(utctime[1]), int(utctime[2]))
		#print "Resetting UTC datetime to -> ", new_utcDatetime
		new_utcDatetime = new_utcDatetime.replace(tzinfo=pytz.utc)

		# from that utc datetime, calculate local datetime
		new_localDatetime = orbit3D.utc_to_local_fromDatetime(new_utcDatetime, self.SolarSystem.locationInfo)
		#print "Resetting LOCAL datetime to -> ", new_localDatetime

		# calculate the time difference between current "today's Date" with new selected date
		diff = new_utcDatetime - self.todayUTCdatetime
		

		# ... and convert the difference in days (as a float value)
		self.DeltaT = diff.total_seconds()/86400.0
		print "OnValidateDate: DELTA from right now (in days) =", self.DeltaT

		# update planet positions accordingly
		# (adjust earth rotation by (2*pi/365.25 )* DeltaT)
		self.parentFrame.widgetsTab.Earth.updateSiderealAngleFromNewDate(self.DeltaT)
		self.updateSolarSystem()
		self.disableBeltsForAnimation()
		#self.refreshDate()


	def setVelocityLabel(self):
		if self.DetailsOn == True:
			self.ObjVelocity.SetLabel("{:<12}{:>10.4f}".format("Vel.(km/s)", round(self.velocity/1000, 2)))

	def setDistanceLabel(self):
		if self.DetailsOn == True:
			#print "distance="+str(self.distance)
			self.ObjDistance.SetLabel("{:<12}{:>10.4f}".format("DTE (AU)", float(self.distance)))


	# deltaTick is used for earth realtime rotation update, when enabled
	def deltaTtick(self, timeinsec):
		# make sure to convert timeinsec as a fraction of day
		#print self.SolarSystem.DaysIncrement, "+", float(timeinsec)/86400, "for", timeinsec 
		#self.SolarSystem.DaysIncrement += float(timeinsec)/86400
		self.DeltaT += float(timeinsec)/86400
		print "deltaTtick: DELTA from right now (in days) =", self.DeltaT

		#print self.SolarSystem.DaysIncrement

	def refreshDate(self):
		self.new_utcDatetime = self.todayUTCdatetime + datetime.timedelta(days = self.DeltaT)
		self.new_localDatetime = orbit3D.utc_to_local_fromDatetime(self.new_utcDatetime, self.SolarSystem.locationInfo)
		#print "Refresh DATE: UTC = ", new_utcDatetime, ", LOCAL=",new_localDatetime
		
		self.dateDSpin.SetValue(self.new_utcDatetime.day)
		self.dateMSpin.SetValue(self.new_utcDatetime.month)
		self.dateYSpin.SetValue(self.new_utcDatetime.year)

		self.updateTimeDisplay(self.new_utcDatetime, self.new_localDatetime)

		self.setVelocityLabel()
		self.setDistanceLabel()
		#print ("refresh Date")

	def updateTimeDisplay(self, utcDatetime, localDatetime):
		self.setLocalDateTimeLabel(localDatetime)
		self.setUTCDateTimeLabel(utcDatetime)

	def disableBeltsForAnimation(self):
		self.checkboxList[JTROJANS].SetValue(False)
		self.checkboxList[ASTEROID_BELT].SetValue(False)
		self.checkboxList[KUIPER_BELT].SetValue(False)
		#self.checkboxList[INNER_OORT_CLOUD].SetValue(False)
		self.SolarSystem.setFeature(JTROJANS|ASTEROID_BELT|KUIPER_BELT|INNER_OORT_CLOUD, False)
		#self.SolarSystem.ShowFeatures = (self.SolarSystem.ShowFeatures & ~(JTROJANS|ASTEROID_BELT|KUIPER_BELT|INNER_OORT_CLOUD))
		orbit3D.glbRefresh(self.SolarSystem, self.AnimationInProgress)

	def updateJTrojans(self):
		##print "TROJAN INDEX=",self.SolarSystem.JTrojansIndex
		curTrojans = self.SolarSystem.getJTrojans()
		if curTrojans is not None:
			JupiterBody = self.SolarSystem.getBodyFromName(self.SolarSystem.objects_data[curTrojans.PlanetName]['jpl_designation'])
			# if Jupiter coordinates haven't changed since this Trojans were generated, don't do anything
			if JupiterBody.Position[0] == curTrojans.JupiterX and JupiterBody.Position[1] == curTrojans.JupiterY:
				return

			# otherwise, generate a new set of Trojans corresponding to Jupiter's new location
			self.SolarSystem.addJTrojans(orbit3D.makeJtrojan(self.SolarSystem, 'jupiterTrojan', 'Jupiter Trojans', JTROJANS, color.green, 2, 5, 'jupiter'))

	def OnRadioBox(self, e):
		if self.ResumeSlideShowLabel == True or self.SolarSystem.SlideShowInProgress == True:
			self.SolarSystem.AbortSlideShow = True
			self.ResumeSlideShowLabel = False
			self.SolarSystem.SlideShowInProgress = False
			self.resetSlideShow()
			self.resetBodyList()

		index = self.rbox.GetSelection()
		self.Source = {0: PHA, 1: COMET, 2:BIG_ASTEROID, 3:TRANS_NEPT}[index]
		self.SolarSystem.currentSource = self.Source

	def OnAnimSpeedSlider(self, e):
		#print "OnAnimSpeedSlider", self.TimeIncrementKey, self.BaseTimeIncrement
		self.TimeIncrement = float(self.aniSpeedSlider.GetValue()) * self.BaseTimeIncrement
		
		# copy time increment to solarsystem class for realtime update
		self.SolarSystem.setTimeIncrement(self.TimeIncrement)
		# self.aniSpeed.SetLabel(str(self.aniSpeedSlider.GetValue()*10)+" mi")
		self.aniSpeed.SetLabel(str(self.aniSpeedSlider.GetValue()*Frame_Intervals[self.TimeIncrementKey]["value"])+" "+Frame_Intervals[self.TimeIncrementKey]["unit"])

	def OnAnimTimeSlider(self, e):
		self.TimeIncrementKey = float(self.aniTimeSlider.GetValue())
		self.BaseTimeIncrement = Frame_Intervals[self.TimeIncrementKey]["incr"]

		# Reflect new time interval in speed slider		
		self.OnAnimSpeedSlider(e)
		return

	def OnTimeSpin(self, e):
		day = self.dateDSpin.GetValue()
		month = self.dateMSpin.GetValue()
		if isLeapYear(self.dateYSpin.GetValue()):
			validDays = date_elements["d_p_m_leap"][month]
		else:
			validDays = date_elements["d_p_m"][month]

		if validDays < day:
			# Here we need to fire our own event in order to change the value
			# of dateDSpin. As a rule of thumb, you cannot change the value
			# of a control from an event handler because changing its value would
			# trigger another call to the same handler. To avoid possible problems,
			# wxPyhton disables the event attached to the handler causing the update.
			# Hence we need to trigger an event whose handler will make the change
			# on the behalf of the original handler

			# fire the EVT_RESET_SPINNER event (which was created during initialization)
			# self.CustomEvent is the object attached to this event. validDays is
			# the parameter passed to the event Handler (ResetSpinner, in this case)
			wx.PostEvent(self.dateDSpin, self.CustomEvent(day=validDays))
		return

	def ResetSpinner(self, e):
		self.dateDSpin.SetValue(e.day)

	def OnRefresh(self, e):
		if self.AnimationInProgress == False:
			self.updateJTrojans()
		else:
			self.checkboxList[JTROJANS].SetValue(False)
			self.checkboxList[ASTEROID_BELT].SetValue(False)
			self.checkboxList[KUIPER_BELT].SetValue(False)

				
		for type, cbox in self.checkboxList.iteritems():
			reset = self.SolarSystem.setFeature(type, cbox.GetValue())
			if reset == True:
				self.parentFrame.focusTab.setSunFocus()

			#if self.SolarSystem.cameraViewTargetBody is not None and self.SolarSystem.cameraViewTargetBody.BodyType == type:
			#		self.parentFrame.focusTab.resetCameraViewTarget()
			"""
		for type, cbox in self.checkboxList.iteritems():
			if cbox.GetValue() == True:
				self.SolarSystem.ShowFeatures |= type
			else:
				if self.SolarSystem.cameraViewTargetBody is not None and self.SolarSystem.cameraViewTargetBody.BodyType == type:
					self.parentFrame.focusTab.resetCameraViewTarget()
				self.SolarSystem.ShowFeatures = (self.SolarSystem.ShowFeatures & ~type)
			"""

		orbit3D.glbRefresh(self.SolarSystem, self.AnimationInProgress)

	def OnPauseSlideShow(self, e):
		self.AnimationInProgress = False

		if self.ResumeSlideShowLabel == True:
			self.resetBodyList()
			e.GetEventObject().SetLabel("Pause")
			self.ResumeSlideShowLabel = False
		else:
			e.GetEventObject().SetLabel("Resume")
			self.ResumeSlideShowLabel = True
			if self.SolarSystem.cameraViewTargetSelection == CURRENT_BODY:
				self.SolarSystem.cameraViewTargetBody = self.currentBody
				self.SolarSystem.camera.updateCameraViewTarget()

	def showObjectDetails(self, body):
		self.InfoTitle.SetLabel(body.Name)

		print "ANIMATE deltaT=", self.DeltaT
		self.velocity, self.distance = body.animate(self.DeltaT)
		if body.Mass == 0:
			mass = "???"
		else:
			mass = setPrecision(str(body.Mass), 3)

		radius = round(float(body.BodyRadius) * 1000)/1000 if body.BodyRadius != 0 and body.BodyRadius != DEFAULT_RADIUS else 0
		moid = round(float(body.Moid/AU) * 10000)/10000 if body.Moid != 0 else 0
#		rev = round(float(body.Revolution / 365.25) * 1000)/1000
		rev = round(float(body.Revolution / EARTH_PERIOD) * 1000)/1000
		H = body.Absolute_mag if body.Absolute_mag != 0 else 0

		i = round(float(body.Inclination) * 1000)/1000
		N = round(float(body.Longitude_of_ascendingnode) * 1000)/1000
		w = round(float(body.Argument_of_perihelion) * 1000)/1000
		e = round(float(body.e) * 1000)/1000
		q = round(float(body.Perihelion/AU) * 1000)/1000

		self.DetailsOn = True
		self.Info1.SetLabel("{:<12}{:>7.3f}\n{:<12}{:>7.3f}\n{:<12}{:>7.3f}\n{:<12}{:>7.3f}\n{:<12}{:>7.3f}\n{:<12}{:>7.3f}".
		format(	"i(deg) ", i,
				"N(deg) ", N,
				"w(deg) ", w,
				"e ", e,
				"q(AU) ", q,
				"Abs. Mag. ", H));
		self.Info2.SetLabel("{:<12}{:>10}\n{:<12}{:>10.4f}\n{:<12}{:>10.4f}\n{:<12}{:>10.4f}\n".
		format(	"Mass(kg) ", mass,
				"Radius(km) ", radius,
				"Period(yr) ", rev,
				"Moid(AU) ", moid));

		############ self.refreshDate() 

		#for i in range(len(body.BodyShape)):
		print ">>>>DETAILS:\norigin.pos=", body.Origin.pos, "\nlabel.pos", body.Labels[0].pos
		body.Origin.visible = True
		for i in range(len(body.Labels)):
			body.Labels[i].visible = True
		body.Trail.visible = True

	def stopSlideSHow(self):
		if self.AnimationInProgress == True:
			self.AnimationInProgress = False
			self.Animate.SetLabel(">")

		if self.SolarSystem.SlideShowInProgress:
			# click on the Stop button
			self.SolarSystem.AbortSlideShow = True
			self.ResumeSlideShowLabel = False
			# reset label as 'Start'
			self.resetSlideShow()
			return True # when slideshow was in progress return true
		return False	# else return false

	def OnSlideShow(self, e):
		if self.SolarSystem.cameraViewTargetSelection == CURRENT_BODY:
			#print "currViewTargetselection = CURRENT_BODY - Reset to SUN"
			self.parentFrame.focusTab.resetCameraViewTarget()

		if self.stopSlideSHow() == True:
			# slideshow was stop and reset. Exit
			return

		# Slideshow wasn't running: There was a click on the start button
		self.resetBodyList() # deselect possible body from combo list
		self.SolarSystem.SlideShowInProgress = True
		self.Pause.Show()

		# reset label as 'Stop'
		self.SlideShow.SetLabel("Stop")

		# loop through each body. If the bodyType matches
		# what the slideshow is about, display it
		for body in self.SolarSystem.bodies:
			if body.BodyType == self.Source:
				orbit3D.glbRefresh(self.SolarSystem, self.AnimationInProgress)
				#self.showObjectDetails(body)
				self.setCurrentBody(body)
				sleep(2)

				while (self.ResumeSlideShowLabel and self.SolarSystem.AbortSlideShow == False):
					sleep(2)

				self.hideCurrentObject(body)

				if self.SolarSystem.AbortSlideShow:
					self.SolarSystem.AbortSlideShow = False
					self.SolarSystem.SlideShowInProgress = False
					return

		self.SolarSystem.SlideShowInProgress = False
		self.resetSlideShow()

	def hideCurrentObject(self, body):
		#body.BodyShape.visible = False
		body.Origin.visible = False
		for i in range(len(body.Labels)):
			body.Labels[i].visible = False

		body.Trail.visible = False

	def resetSlideShow(self):
		self.SlideShow.SetLabel("Start")
		self.Pause.Hide()
		self.InfoTitle.SetLabel('')
		self.Info1.SetLabel('')
		self.Info2.SetLabel('')
		#self.ObjVelocity.SetLabel("{:<12}{:>10.4f}".format("Vel.(km/s)", 0.0))
		self.ObjVelocity.SetLabel("")
		self.ObjDistance.SetLabel("")
		self.DetailsOn = False
		self.Pause.SetLabel("Pause")

	def OnStepper(self, e):
		if self.RecorderOn == True:
			self.RecorderOn = False

		self.StepByStep = True
		self.disableBeltsForAnimation()
		self.AnimationInProgress = False # stop potential animation in progress
		self.OneTimeIncrement()

	def OnRecord(self, e):
		if self.RecorderOn == False:
			self.RecorderOn = True
			self.Recorder.SetOwnForegroundColour(wx.RED)
		else:
			self.RecorderOn = False
			self.Recorder.SetOwnForegroundColour(wx.BLACK)

		#self.disableBeltsForAnimation()
		#self.AnimationInProgress = False # stop potential animation in progress
		#self.OneTimeIncrement()


	def OneTimeIncrement(self):
		self.DeltaT += self.TimeIncrement

		# perform animation actions when requested
		self.executeAnimationActions()

		# animate by one TimeIncrement all bodies in the solar system
		self.updateSolarSystem()
		sleep(1e-2)
		#sleep(1e-4)

	def executeAnimationActions(self):
		# if auto movement is required, execute it
		if self.AutoRotation.GetValue() == True:
#			self.SolarSystem.camera.cameraTest(frame=1)
			#self.SolarSystem.camera.oneTickCameraCombination(zoom=True, zoom_forward=True)
			self.SolarSystem.camera.oneTickCameraRotationWithDirection(direction = self.SolarSystem.camera.ROT_HOR|self.SolarSystem.camera.ROT_LEFT)

		# follow mode view (camera tracks the subject 
		# in its trajectory using the same angle)
		if self.followModeView == True:
            # update camera forward vector to follow the earth (either from the 
            # sun's perspective or from the forward vector current position)
			self.updateConstantForwardVectorMode()

	def updateConstantForwardVectorMode(self, sunPerspective = False):
		# we use self.SolarSystem.cameraViewTargetBody
		# alternate view: using the current forward vector, match vector rotation with earth angular speed
		if self.SolarSystem.cameraViewTargetBody is not None:
			angle = atan2(self.SolarSystem.cameraViewTargetBody.Position[1], self.SolarSystem.cameraViewTargetBody.Position[0])
			self.SolarSystem.Scene.forward = rotate(self.SolarSystem.Scene.forward, angle=(angle-self.viewAngle), axis=(0,0,1)) #self.Widgets.ECSS.ZdirectionUnit)
			self.viewAngle = angle


	def SetAnimationCallback(self, callbackFunc, args):
		self.DisableAnimationCallback = True
		self.AnimationCallback = callbackFunc(args)
		self.DisableAnimationCallback = False

	def OnAnimateTest(self, e):
		sleep(2)
		while True:
			sleep(1e-2)
			if self.DisableAnimationCallback == False:
				self.AnimationCallback()
	
	def OnAnimate(self, e):
		self.StepByStep = False
		if self.AnimationInProgress == True:
			self.AnimationInProgress = False
			self.parentFrame.widgetsTab.comb.Enable()

			# at the end of animation, disable autoMovement to enable 
			# mouse tracking from display._mouse_tracker method  
			self.SolarSystem._set_autoMovement(False) ####
			self.AutoRotation.SetValue(False)

			self.Animate.SetLabel(">")
			if self.RecorderOn == True and self.VideoRecorder is not None:
				stopRecording(self.VideoRecorder)

			return

		self.VideoRecorder = None

		self.Animate.SetLabel("||")
		self.disableBeltsForAnimation()
		self.AnimationInProgress = True
		self.parentFrame.widgetsTab.comb.Disable()

		# if we animate for the first time, make sure to initialize 
		# DaysIncrement with current time as a fraction of day
		"""
		if UNINITIALIZED == self.SolarSystem.DaysIncrement:
			ztime = self.localTimeLabel.GetLabel().split(" : ")
			if len(ztime) > 0:
				#print "before correction", self.DaysIncrement
				self.SolarSystem.DaysIncrement += (float(ztime[0]) * TI_ONE_HOUR) + (float(ztime[1]) * TI_ONE_MINUTE) + (float(ztime[2]) * TI_ONE_SECOND)
				print "##############", self.SolarSystem.DaysIncrement
		print self.SolarSystem.DaysIncrement
		"""
		#self.setDeltaT()

		# When the autoRotation checkbox is true, enable autoMovement to disable 
		# mouse tracking from display._mouse_tracker method  
		if self.AutoRotation.GetValue() == True:
			self.set_autoMovement(True)

		# start a new thread to retrieve the list of NEOs from JPL
		#animateThread = threading.Thread(target=self.doAnimation, name="doAnimation", args=[] )
		#animateThread.start()
		self.doAnimation()
		# loop was here

		#self.Recorder.SetColor() ####
	def doAnimation(self):
		# set mechanic to determine the # of frame per seconds in Animation (if recorder is ON)
		sec = time.gmtime(time.time()).tm_sec
		framerate = 0


		while self.AnimationInProgress:
#			sleep(1e-2)
			#sleep(1e-3)

			self.OneTimeIncrement()
			if self.RecorderOn == True:
				if self.VideoRecorder is None:
					self.VideoRecorder = setVideoRecording(framerate = 20, filename = "output.avi")
				recOneFrame(self.VideoRecorder)
			
			# if we have an animation callback set up, run it
			if self.DisableAnimationCallback == False:
				self.AnimationCallback()
			#	print self.SolarSystem.Scene.center

			# determine # of frames/sec
			t = time.gmtime(time.time()).tm_sec
			if t != sec:
				sec = t 
				#print framerate
				framerate = 0
			else:
				framerate += 1

		# as soon as we exit animation, restore "play" sign
		self.Animate.SetLabel(">")


	# this method calls the display class _set_autoMovement to enable or disable
	# mouse tracking, depending on whether we have or not an auto movement in progress
	def set_autoMovement(self, is_movement):
		self.SolarSystem.Scene._set_autoMovement(is_movement)



# CLASS WIDGETSpanel ----------------------------------------------------------
# Current Planet widgets Tab
class WIDGETSpanel(AbstractUI):

	def InitVariables(self):	
		self.ca_deltaT = 0
		self.Earth = self.SolarSystem.EarthRef
		
		self.checkboxList = {}
		self.Locations = []
		self.locIndexes = []

		self.currentInfoAction = 1 # need to find a mechanism to assign a value to currentAction based on what the user picks (each option is mutually exclusive)
		self.infoWindowActions = {
                0: self.dummy,
                1: self.UTCdatetime
            }
		"""
		self.CameraSettings = []
		self.cameraSettingActions = {
			0: self.OnFollowMode,
			1: self.OnEarthEyeView
		}
		"""

	def UTCdatetime(self):
		ctrl = self.parentFrame.orbitalTab
		self.parentFrame.setInfoLine("UTC: "+index_to_month[ctrl.dateMSpin.GetValue()]+" {:>02}/{:>4}".format(str(ctrl.dateDSpin.GetValue()), str(ctrl.dateYSpin.GetValue())), 0)
		self.parentFrame.setInfoLine("{:>5}{:>2}:{:>2}:{:2}".format("", str(ctrl.new_utcDatetime.hour).zfill(2), str(ctrl.new_utcDatetime.minute).zfill(2), str(ctrl.new_utcDatetime.second).zfill(2)), 1)

	def dummy(self):
		pass

	def InitUI(self):

		self.BoldFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
		self.RegFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)
		self.SurfaceDirection = [0,0,0]

		######## Widgets section ########
		heading = wx.StaticText(self, label='Earth Widgets', pos=(50, MAIN_HEADING_Y))
		heading.SetFont(self.BoldFont)

		self.eqcb = wx.CheckBox(self, label="Equator", pos=(50, CHK_L1)) #   CVT_Y+560))
		self.eqcb.SetValue(False)
		self.eqcb.Bind(wx.EVT_CHECKBOX,self.OnDrawEquator)

		self.trcb = wx.CheckBox(self, label="Tropics", pos=(230, CHK_L1)) #   CVT_Y+560))
		self.trcb.SetValue(False)
		self.trcb.Bind(wx.EVT_CHECKBOX,self.OnDrawTropics)

		self.mrcb = wx.CheckBox(self, label="Longitude lines", pos=(50, CHK_L2)) #   CVT_Y+560))
		self.mrcb.SetValue(False)
		self.mrcb.Bind(wx.EVT_CHECKBOX,self.OnDrawLongitudeLines)

		self.tzcb = wx.CheckBox(self, label="Time zones", pos=(230, CHK_L2)) #   CVT_Y+560))
		self.tzcb.SetValue(False)
		self.tzcb.Bind(wx.EVT_CHECKBOX,self.OnDrawTZLines)

		self.latcb = wx.CheckBox(self, label="Latitude lines", pos=(50, CHK_L3)) #   CVT_Y+560))
		self.latcb.SetValue(False)
		self.latcb.Bind(wx.EVT_CHECKBOX,self.OnDrawLatitudeLines)

		self.eqpcb = wx.CheckBox(self, label="Equatorial Plane", pos=(50, CHK_L4)) #   CVT_Y+560))
		self.eqpcb.SetValue(False)
		self.eqpcb.Bind(wx.EVT_CHECKBOX,self.OnDrawEquatorialPlane)

		self.ncb = wx.CheckBox(self, label="Nodes", pos=(50, CHK_L5)) #   CVT_Y+560))
		self.ncb.SetValue(False)
		self.ncb.Bind(wx.EVT_CHECKBOX,self.OnShowNodes)

		self.hpcb = wx.CheckBox(self, label="Hide Planet", pos=(50, CHK_L6)) #CHK_L8)) #   CVT_Y+560))
		self.hpcb.SetValue(False)
		self.hpcb.Bind(wx.EVT_CHECKBOX,self.OnHidePlanet)

		########### Locations section ###########
		lheading = wx.StaticText(self, label='Locations', pos=(50, CHK_L8))
		lheading.SetFont(self.BoldFont)

		self.createLocationList(50, CBBOX_1)

		#self.flcb = wx.CheckBox(self, label="Center to surface", pos=(50, CHK_L8)) #   CVT_Y+560))
		#self.flcb.SetValue(False)
		#self.flcb.Bind(wx.EVT_CHECKBOX,self.OnCenterToSurface)

		self.lacb = wx.CheckBox(self, label="Location Referential View", pos=(50, CHK_L11)) #CHK_L18)) #   CVT_Y+560))
		self.lacb.SetValue(False)
		self.lacb.Disable()
		self.lacb.Bind(wx.EVT_CHECKBOX,self.OnEarthEyeView)

		self.cpcb = wx.CheckBox(self, label="Re-Center to Earth's center", pos=(50, CHK_L12)) #230, CHK_L12)) #   CVT_Y+560))
		self.cpcb.SetValue(False)
		self.cpcb.Disable()
		self.cpcb.Bind(wx.EVT_CHECKBOX,self.OnReCenter)


		######## Referentials section #########
		rheading = wx.StaticText(self, label='Referentials', pos=(50, CHK_L14))
		rheading.SetFont(self.BoldFont)

		self.lrcb = wx.CheckBox(self, label="Earth-Centered-Inertial (ECI) Referential", pos=(50, CHK_L15B)) #   CVT_Y+560))
		self.lrcb.SetValue(False)
		self.lrcb.Bind(wx.EVT_CHECKBOX,self.OnLocalRef)

		self.lr2cb = wx.CheckBox(self, label="Earth-Centered-Earth-Fixed (ECEF) Referential", pos=(50, CHK_L16)) #   CVT_Y+560))
		self.lr2cb.SetValue(False)
		self.lr2cb.Bind(wx.EVT_CHECKBOX,self.OnECEFRef)

		self.arcb = wx.CheckBox(self, label="Earth-Centered-Sun-Synchronous (ECSS) Referential", pos=(50, CHK_L17)) #   CVT_Y+560))
		self.arcb.SetValue(False)
		self.arcb.Bind(wx.EVT_CHECKBOX,self.OnShowECSS)

		self.ncpcb = wx.CheckBox(self, label="TopoCentric Referential", pos=(50, CHK_L18)) #   CVT_Y+560))
		self.ncpcb.SetValue(False)
		self.ncpcb.Disable()
		self.ncpcb.Bind(wx.EVT_CHECKBOX,self.OnShowTopoCentricRef)

		########## Analemma section ##########
		aheading = wx.StaticText(self, label='Analemma', pos=(50, CHK_L20))
		aheading.SetFont(self.BoldFont)

		self.acb = wx.CheckBox(self, label="Animate 24h period", pos=(50, CHK_L21)) 
		self.acb.SetValue(False)
		self.acb.Disable()
		self.acb.Bind(wx.EVT_CHECKBOX,self.OnAnimate24h)
		self.animate24 = False


		self.srcb = wx.CheckBox(self, label="Show Sun Ray", pos=(50, CHK_L22)) #CHK_L18)) #   CVT_Y+560))
		self.srcb.SetValue(False)
		self.srcb.Disable()
		self.srcb.Bind(wx.EVT_CHECKBOX,self.OnShowSunRay)

		self.sacb = wx.CheckBox(self, label="Show Analemma", pos=(50, CHK_L23)) #CHK_L18)) #   CVT_Y+560))
		self.sacb.SetValue(False)
		self.sacb.Disable()
		self.sacb.Bind(wx.EVT_CHECKBOX,self.OnShowAnalemma)

		self.dmcb = wx.CheckBox(self, label="Display Months", pos=(250, CHK_L23)) #CHK_L18)) #   CVT_Y+560))
		self.dmcb.SetValue(False)
		self.dmcb.Disable()
		self.dmcb.Bind(wx.EVT_CHECKBOX,self.OnDisplayMonths)

		self.racb = wx.CheckBox(self, label="Reset Analemma", pos=(50, CHK_L24)) #CHK_L17)) #   CVT_Y+560))
		self.racb.SetValue(False)
		self.racb.Disable()
		self.racb.Bind(wx.EVT_CHECKBOX,self.OnResetAnalemma)

		########## Camera section ##########

		iheading = wx.StaticText(self, label='Info Settings', pos=(50, CHK_L26))
		iheading.SetFont(self.BoldFont)
		self.iscb = wx.CheckBox(self, label="UTC time", pos=(50, CHK_L27)) #CHK_L17)) #   CVT_Y+560))
		self.iscb.SetValue(False)
		self.iscb.Bind(wx.EVT_CHECKBOX,self.OnShowUTCInfo)

		if False:
			cheading = wx.StaticText(self, label='Camera Settings', pos=(50, CHK_L26))
			cheading.SetFont(self.BoldFont)
			lblList = ['Follow Mode', 'Location View']
			self.rbox = wx.RadioBox(self,label = 'Animation Settings', pos = (50, CBBOX_2), size=(165, 170), choices = lblList ,majorDimension = 1, style = wx.RA_SPECIFY_COLS)
			self.rbox.SetFont(self.RegFont)
			self.rbox.Bind(wx.EVT_RADIOBOX,self.OnCameraSettings)

	#		self.createCameraSettingsList(50, CBBOX_2)

	INFO_UTC = 0
	def OnShowUTCInfo(self, e):
		self.parentFrame.showInfoWindow(self.iscb.GetValue()) #### need to parametrize to allow for other actions than just UTC info

	def OnCameraSettingsXX(self, e):

		index = self.rbox.GetSelection()
		self.Source = {0: PHA, 1: COMET, 2:BIG_ASTEROID, 3:TRANS_NEPT}[index]
		self.cameraSettingsActions[index](e)

	def OnFollowMode(self, e):
		self.Parent.orbitalTab.followModeView = True


	def createCameraSettingsListXXX(self, xpos, ypos):
		self.CameraSettings = ["Follow Mode", "Location Referential View"]
		self.cameraSettingActions = {
			0: self.OnFollowMode,
			1: self.OnEarthEyeView
		}

		
		#i = 0
		#for setting in settings:
		#	self.CameraSettings.append(setting)
		#	self.CameraSettingsIndexes.append(i)
		#	i += 1

		self.combCam = wx.ComboBox(self, id=wx.ID_ANY, value="Select a Camera Setting", size=wx.DefaultSize, pos=(xpos, ypos), choices=self.CameraSettings, style=(wx.CB_DROPDOWN))
		self.combCam.Bind(wx.EVT_COMBOBOX, self.OnSelectCameraSetting)

	def createLocationList(self, xpos, ypos):
		i = 0
		for loc in self.SolarSystem.locationInfo.tzEarthLocations:
			self.Locations.append(loc["name"]+" ("+loc["tzname"]+")")
			self.locIndexes.append(i)
			i += 1

		self.comb = wx.ComboBox(self, id=wx.ID_ANY, value="Select a location on Earth", size=wx.DefaultSize, pos=(xpos, ypos), choices=self.Locations, style=(wx.CB_DROPDOWN))
		self.comb.Bind(wx.EVT_COMBOBOX, self.OnSelectLocation)

	def resetLocationList(self):
		self.comb.SetSelection(-1)
		self.comb.SetValue("Select a location on Earth")

	def OnSelectLocation(self, e):
		if self.parentFrame.orbitalTab.AnimationInProgress == False:
			locationID = self.locIndexes[e.GetSelection()]
			self.comb.Dismiss() # this will close the combo 
			self.cpcb.Enable()
			self.SolarSystem.camera.gotoEarthLocationVertical(locationID)
			self.Earth.PlanetWidgets.Loc[self.Earth.PlanetWidgets.currentLocation].makeTopoCentricRef()
			self.acb.Enable()
			self.ncpcb.Enable()
			self.lacb.Enable()
			self.srcb.Enable()
			self.dmcb.Enable()
			self.racb.Enable()
			self.sacb.Enable()
		else:
			self.comb.Dismiss() # this will close the combo 
			self.resetLocationList()
			print ">> Earth Location motion are disabled when animation is in progress"

	def OnSelectCameraSetting(self, e):
		self.cameraActions[e.GetSelection()](e)

	def OnResetAnalemma(self, e):
		loc = self.getLocation()
		if loc is not None:
			if self.racb.GetValue() == True:
				#self.Earth.PlanetWidgets.Loc[self.Earth.PlanetWidgets.currentLocation].resetAnalemma()
				loc.resetAnalemma()
				self.racb.SetValue(False)
				self.racb.Disable()
		else:
			self.racb.SetValue(False)


	def OnEarthEyeView(self, e):
		loc = self.getLocation()
		if loc is not None:
			if self.lacb.GetValue() == True:
				#self.Earth.PlanetWidgets.Loc[self.Earth.PlanetWidgets.currentLocation].setEarthEyeView(True)
				loc.setEarthEyeView(True)
				#self.lacb.Disable()
			else:
#				self.Earth.PlanetWidgets.Loc[self.Earth.PlanetWidgets.currentLocation].setEarthEyeView(False)
				loc.setEarthEyeView(False)
				self.lacb.SetValue(False)
		else:
			self.lacb.SetValue(False)


	def OnResetAnalemma_save(self, e):
		if self.racb.GetValue() == True:
			#self.Earth.PlanetWidgets.AnaLemma.Shape.visible = False
			#del self.Earth.PlanetWidgets.AnaLemma.Shape
			#self.Earth.PlanetWidgets.AnaLemma.Shape = None

			#self.Earth.PlanetWidgets.AnaLemma.resetAnalemma()
			self.Earth.PlanetWidgets.Loc[self.Earth.PlanetWidgets.currentLocation].resetAnalemma()
			self.racb.SetValue(False)


	def OnAnimate24h(self, e):
		loc = self.getLocation()
		if loc is not None:
			if self.acb.GetValue() == True:
				self.animate24 = True
				self.parentFrame.orbitalTab.TimeIncrement = TI_24_HOURS
				self.SolarSystem.setTimeIncrement(self.parentFrame.orbitalTab.TimeIncrement)

				########### loc.createAnalemma()
				####loc.showAnalemma(True)
				
				self.parentFrame.orbitalTab.OnAnimate(e)
				self.racb.Enable()
			else:
				# 1) stop animation
				self.parentFrame.orbitalTab.OnAnimate(e)
				# 2) reset TimeIncrement with proper value from sliders
				self.parentFrame.orbitalTab.OnAnimTimeSlider(e)
				
				#loc.showAnalemma(False)
				
				self.animate24 = False
		else:
			self.acb.SetValue(False)

	def OnShowSunRay(self, e):
		loc = self.getLocation()
		if loc is not None:
			loc.displaySunRay(self.srcb.GetValue())
		else:
			self.srcb.SetValue(False)

	def OnShowAnalemma(self, e):
		loc = self.getLocation()
		if loc is not None:
			loc.showAnalemma(self.sacb.GetValue())
		else:
			self.acb.SetValue(False)


	def OnDisplayMonths(self, e):
		loc = self.getLocation()
		if loc is not None:
			loc.analemma.showAnaLabels(self.dmcb.GetValue())
		else:
			self.dmcb.SetValue(False)

	def getLocation(self):
		if self.Earth.PlanetWidgets.currentLocation == -1:
			return None
		else:
			return self.Earth.PlanetWidgets.Loc[self.Earth.PlanetWidgets.currentLocation]















	def OnAnimate24h_save(self, e):
		if self.acb.GetValue() == True:
			self.parentFrame.orbitalTab.TimeIncrement = TI_24_HOURS
			self.SolarSystem.setTimeIncrement(self.parentFrame.orbitalTab.TimeIncrement)
			loc = self.Earth.PlanetWidgets.Loc[self.Earth.PlanetWidgets.currentLocation]
			#loc.createAnalemma()
			loc.showAnalemma(True)
			#-> self.parentFrame.orbitalTab.OnAnimate(e)
		else:
			# 1) stop animation
			#-> self.parentFrame.orbitalTab.OnAnimate(e)
			# 2) reset TimeIncrement with proper value from sliders
			self.parentFrame.orbitalTab.OnAnimTimeSlider(e)
			#self.Earth.PlanetWidgets.AnaLemma.display(False)
			self.Earth.PlanetWidgets.Loc[self.Earth.PlanetWidgets.currentLocation].showAnalemma(False)

	def OnShowECSS(self, e):
		self.Earth.PlanetWidgets.ECSS.display(self.arcb.GetValue())


	def OnShowTopoCentricRef(self, e):
		if False:
			self.SolarSystem.camera.cameraZoom(1, 50) #, velocity = 1, recorder = False, zoom = ZOOM_IN, ratefunc = there_and_back)
			#axis = getOrthogonalVector(self.SolarSystem.camera.view.forward)

			#self.SolarSystem.camera.cameraRotateLeft(85, False, axis=-axis)
	#		self.SolarSystem.camera.cameraRotateLeft(80, False)
			self.SolarSystem.camera.cameraRotateDown(90, False)
			#self.SolarSystem.camera.cameraZoom(1, 50, recorder = False, zoom = self.SolarSystem.camera.ZOOM_OUT) #, ratefunc = there_and_back)

			return

		# focus on current location
		#self.ssys.EarthRef.PlanetWidgets.currentLocation
		#self.Earth.PlanetWidgets.currentLocation = self.Earth.PlanetWidgets.defaultLocation
		if self.Earth.PlanetWidgets.currentLocation != -1:
			loc = self.Earth.PlanetWidgets.Loc[self.Earth.PlanetWidgets.currentLocation]
			#loc.show(self.ncpcb.GetValue())
			loc.displayTopoCentricRef(self.ncpcb.GetValue())

		if False:
			# testing shifting earth locations
			self.Earth.PlanetWidgets.shiftLocation(locList.TZ_AUS_SYD)
			self.Earth.PlanetWidgets.shiftLocation(locList.TZ_FR_PARIS)
			self.Earth.PlanetWidgets.shiftLocation(locList.TZ_JP_TAN)
			self.Earth.PlanetWidgets.shiftLocation(locList.TZ_US_VDBERG)
			self.Earth.PlanetWidgets.shiftLocation(locList.TZ_RUS_BAIK)
			### self.Earth.SolarSystem.camera.cameraRefresh()

		
	def OnReCenter(self, e):
		# recenter on earth's center
		print "re-centering in ", self.Earth.Origin.pos
		# reset current location value
		self.Earth.PlanetWidgets.currentLocation = -1
		self.resetLocationList()
		self.cpcb.Disable()
		self.cpcb.SetValue(False)
		self.acb.Disable()
		self.acb.SetValue(False)
		self.ncpcb.Disable()
		self.ncpcb.SetValue(False)

		self.lacb.Disable()
		self.lacb.SetValue(False)
		self.srcb.Disable()
		self.srcb.SetValue(False)
		self.dmcb.Disable()
		self.dmcb.SetValue(False)
		self.lacb.Disable()
		self.lacb.SetValue(False)
		self.racb.Disable()
		self.racb.SetValue(False)
		self.sacb.Disable()
		self.sacb.SetValue(False)


		# if an anmation is in progress, make sure to stop it.
		if self.animate24 == True:
			self.OnAnimate24h(e)
		elif self.parentFrame.orbitalTab.AnimationInProgress == True:
			self.parentFrame.orbitalTab.OnAnimate(e)

		#self.SolarSystem.camera.updateCameraViewTarget()
		self.SolarSystem.camera.smoothFocus(self.Earth.JPL_designation)	

		#self.SolarSystem.Scene.center = self.Earth.Origin.pos
		
		#(
		#				self.Earth.Origin.pos[0],
		#				self.Earth.Origin.pos[1],
		#				self.Earth.Origin.pos[2]
		#			)
		# focus on current location
		return
		
		loc = None
		if self.cpcb.GetValue() == True:
			self.centerToDefaultLocation()
		else:
			self.Earth.PlanetWidgets.currentLocation = -1

	def centerToDefaultLocation(self):


		self.SolarSystem.camera.gotoEarthLocationVertical(locList.TZ_RUS_BAIK)
		self.SolarSystem.camera.gotoEarthLocationVertical(locList.TZ_CHN_XI)
		self.SolarSystem.camera.gotoEarthLocationVertical(locList.TZ_FR_KOUR)
		self.SolarSystem.camera.gotoEarthLocationVertical(locList.TZ_FR_PARIS)
		self.SolarSystem.camera.gotoEarthLocationVertical(locList.TZ_JP_TAN)
		self.SolarSystem.camera.gotoEarthLocationVertical(locList.TZ_EG_CAIRO)
		self.SolarSystem.camera.gotoEarthLocationVertical(locList.TZ_US_VDBERG)
		
		return

		self.Earth.PlanetWidgets.defaultLocation = TZ_RUS_BAIK
		loc = self.Earth.PlanetWidgets.Loc[self.Earth.PlanetWidgets.defaultLocation]
		loc.updateEclipticPosition()
		self.Earth.PlanetWidgets.gotoVertical(self.Earth.PlanetWidgets.defaultLocation)
		self.Earth.PlanetWidgets.currentLocation = self.Earth.PlanetWidgets.defaultLocation


		self.Earth.PlanetWidgets.defaultLocation = TZ_CHN_XI
		loc = self.Earth.PlanetWidgets.Loc[self.Earth.PlanetWidgets.defaultLocation]
		loc.updateEclipticPosition()
		self.Earth.PlanetWidgets.gotoVertical(self.Earth.PlanetWidgets.defaultLocation)
		self.Earth.PlanetWidgets.currentLocation = self.Earth.PlanetWidgets.defaultLocation
		return

		self.Earth.PlanetWidgets.defaultLocation = TZ_FR_KOUR
		loc = self.Earth.PlanetWidgets.Loc[self.Earth.PlanetWidgets.defaultLocation]
		loc.updateEclipticPosition()
		self.Earth.PlanetWidgets.gotoVertical(self.Earth.PlanetWidgets.defaultLocation)
		self.Earth.PlanetWidgets.currentLocation = self.Earth.PlanetWidgets.defaultLocation

		self.Earth.PlanetWidgets.defaultLocation = TZ_FR_PARIS
		loc = self.Earth.PlanetWidgets.Loc[self.Earth.PlanetWidgets.defaultLocation]
		loc.updateEclipticPosition()
		self.Earth.PlanetWidgets.gotoVertical(self.Earth.PlanetWidgets.defaultLocation)
		self.Earth.PlanetWidgets.currentLocation = self.Earth.PlanetWidgets.defaultLocation

		self.Earth.PlanetWidgets.defaultLocation = TZ_JP_TAN
		loc = self.Earth.PlanetWidgets.Loc[self.Earth.PlanetWidgets.defaultLocation]
		loc.updateEclipticPosition()
		self.Earth.PlanetWidgets.gotoVertical(self.Earth.PlanetWidgets.defaultLocation)
		self.Earth.PlanetWidgets.currentLocation = self.Earth.PlanetWidgets.defaultLocation


####		self.SolarSystem.camera.smoothFocus2target(loc.getEclipticPosition(), ratefunc = rate_func.ease_in_out)

	def OnCenterToLocation2(self, e):
		# focus on current location
		loc = None
		if self.cpcb.GetValue() == True:
			self.Earth.PlanetWidgets.currentLocation = self.Earth.PlanetWidgets.defaultLocation
			loc = self.Earth.PlanetWidgets.Loc[self.Earth.PlanetWidgets.currentLocation]
		else:
			self.Earth.PlanetWidgets.currentLocation = -1


#		self.Earth.SolarSystem.cameraViewTargetBody = self.Earth
		#self.parentFrame.orbitalTab.updateCameraViewTarget(loc)
		self.SolarSystem.camera.updateCameraViewTarget(loc)

	"""
	def OnCenterToSurfaceSouth(self, e):
		# focus on surface rather than center
		if self.flscb.GetValue() == True:
			self.SolarSystem.SurfaceDirection[2] = -1
		else:
			self.SolarSystem.SurfaceDirection[2] = 0
		self.parentFrame.orbitalTab.updateCameraViewTarget()

	def OnCenterToSurfaceNorth(self, e):
		# focus on surface rather than center
		if self.flncb.GetValue() == True:
			self.SolarSystem.SurfaceDirection[2] = 1
		else:
			self.SolarSystem.SurfaceDirection[2] = 0
		self.parentFrame.orbitalTab.updateCameraViewTarget()

	def OnCenterToSurfaceEast(self, e):
		# focus on surface rather than center
		if self.flecb.GetValue() == True:
			self.SolarSystem.SurfaceDirection[0] = 1
		else:
			self.SolarSystem.SurfaceDirection[0] = 0
		self.parentFrame.orbitalTab.updateCameraViewTarget()

	def OnCenterToSurfaceWest(self, e):
		# focus on surface rather than center
		if self.flwcb.GetValue() == True:
			self.SolarSystem.SurfaceDirection[0] = -1
		else:
			self.SolarSystem.SurfaceDirection[0] = 0
		self.parentFrame.orbitalTab.updateCameraViewTarget()

	def OnCenterToSurfaceBright(self, e):
		# focus on surface rather than center
		if self.flbrightcb.GetValue() == True:
			self.SolarSystem.SurfaceDirection[1] = 1
		else:
			self.SolarSystem.SurfaceDirection[0] = 0
		self.parentFrame.orbitalTab.updateCameraViewTarget()

	def OnCenterToSurfaceDark(self, e):
		# focus on surface rather than center
		if self.fldarkcb.GetValue() == True:
			self.SolarSystem.SurfaceDirection[1] = -1
		else:
			self.SolarSystem.SurfaceDirection[0] = 0
		self.parentFrame.orbitalTab.updateCameraViewTarget()
	"""
	def OnCenterToSurface(self, e):
		# focus on surface rather than center
		self.SolarSystem.SurfaceView = self.flcb.GetValue()
		self.parentFrame.orbitalTab.surfaceRadius = (1.1 * self.SolarSystem.cameraViewTargetBody.BodyShape.radius) if self.SolarSystem.SurfaceView == True else 0

		#self.SolarSystem.SurfaceDirection[0] = 0		
		#self.SolarSystem.SurfaceDirection[1] = 0		
		#self.SolarSystem.SurfaceDirection[2] = -1	
		self.SolarSystem.camera.updateCameraViewTarget()	
		#self.parentFrame.orbitalTab.updateCameraViewTarget()

	def OnHidePlanet(self, e):
		self.Earth.Origin.visible = not self.hpcb.GetValue()

	def OnDrawEquator(self, e):
		self.Earth.PlanetWidgets.showEquator(self.eqcb.GetValue())

	def OnDrawTropics(self, e):
		self.Earth.PlanetWidgets.showTropics(self.trcb.GetValue())

	def OnShowNodes(self, e):
		self.Earth.PlanetWidgets.showNodes(self.ncb.GetValue())

	def OnDrawEquatorialPlane(self, e):
		self.Earth.PlanetWidgets.showEquatorialPlane(self.eqpcb.GetValue())

	def OnDrawLongitudeLines(self, e):
		self.Earth.PlanetWidgets.showLongitudes(self.mrcb.GetValue())

	def OnDrawTZLines(self, e):
		self.Earth.PlanetWidgets.showTimezones(self.tzcb.GetValue())

	def OnDrawLatitudeLines(self, e):
		self.Earth.PlanetWidgets.showLatitudes(self.latcb.GetValue())

	def OnLocalRef(self, e):
		self.parentFrame.focusTab.cb.SetValue(self.lrcb.GetValue())
		self.SolarSystem.setFeature(LOCAL_REFERENTIAL, self.lrcb.GetValue())
		orbit3D.glbRefresh(self.SolarSystem, self.parentFrame.orbitalTab.AnimationInProgress)

	def OnECEFRef(self, e):
		self.SolarSystem.EarthRef.PCPF.display(self.lr2cb.GetValue())
