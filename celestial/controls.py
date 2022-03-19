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
import datetime #import datetime
import orbit3D 
from planetsdata import *
from visual import *

#from celestial.orbit3D import *
#import celestial.planetsdata as pd

#from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

from numberfmt import *
import urllib2
import httplib
from video import * #VideoRecorder
import re
import json

import wx
import wx.lib.newevent # necessary for custom event

MAIN_HEADING_Y = 40
DATE_Y = MAIN_HEADING_Y
DATE_SLD_Y = DATE_Y + 20
JPL_BRW_Y = DATE_SLD_Y

# checkboxes lines
CHK_L1 = MAIN_HEADING_Y + 20
CHK_L2 = CHK_L1 + 20
CHK_L3 = CHK_L2 + 20
CHK_L4 = CHK_L3 + 20
#TNO_Y = CHK_L4 + 20
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

LSTB_Y = DATE_Y + 60
SLDS_Y = LSTB_Y + 40

STRT_Y = SLDS_Y
PAU_Y = STRT_Y + 40
JPL_Y = PAU_Y + 40
DET_Y = CHK_L14 + 70
ANI_Y = JPL_Y + 100

INFO1_Y = DET_Y + 20
INFO1_V = INFO1_Y + 75

JPL_CLOSE_APPROACH_Y = INFO1_V+30

TOTAL_Y = INFO1_Y+180
TOTAL_X = 500

date_elements = {
	"d_p_m" : {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:20, 12:31},
	"d_p_m_leap" : {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:20, 12:31},
	"d_to_m" :{1:0, 2:31, 3:59, 4:90, 5:120, 6:151, 7:181, 8:212, 9:243, 10:273, 11:304, 12:334},
	"d_to_m_leap" :{1:0, 2:31, 3:60, 4:91, 5:121, 6:152, 7:182, 8:213, 9:244, 10:274, 11:305, 12:335},
	"d_since_J2000":{1995:-1827.5, 1996: -1462.5, 1997: -1096.5, 1998: -731.5, 1999:-366.5, 2000:-1.5, 2001: 364.5, 2002: 729.5, 2003:1094.5, 2004:1459.5, 2005:1825.5}
}

def isLeapYear(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

#
# JPL API search Panel
#

MAIN_HEADING_Y = 25
JPL_DOWNLOAD_Y = MAIN_HEADING_Y-15
JPL_LISTCTRL_Y = MAIN_HEADING_Y + 25

JPL_LIST_SZ = TOTAL_Y-160
JPL_BRW_Y = JPL_LISTCTRL_Y + JPL_LIST_SZ + 15

NASA_API_KEY = "KTTV4ZQFuTywtkoi3gA59Qdlk5H2V1ry6UdYL0xU"
#NASA_API_V1_FEED_TODAY = "https://api.nasa.gov/neo/rest/v1/feed/today?detailed=true&api_key="+NASA_API_KEY
NASA_API_V1_FEED_TODAY = "https://api.nasa.gov/neo/rest/v1/feed?api_key="+NASA_API_KEY

NASA_API_V1_FEED_TODAY_HOST = "https://api.nasa.gov"
#NASA_API_V1_FEED_TODAY_URL = "/neo/rest/v1/feed/today?detailed=true&api_key="+NASA_API_KEY
NASA_API_V1_FEED_TODAY_URL = "/neo/rest/v1/feed?detailed=true&api_key="+NASA_API_KEY
NASA_API_HTTPS_HOST = "https://api.nasa.gov"

NASA_API_KEY_DETAILS = "https://api.nasa.gov/neo/rest/v1/neo/"

# PANELS numbers - Note that panels MUST be added in the same order to the parent
# notebook to make it possible to switch from panel to panel programmatically

PANEL_MAIN 	= 0
PANEL_POV 	= 1
PANEL_CAPP 	= 2

POV_Y = 15
POV_FOCUS_Y = POV_Y+150

from abc import ABCMeta

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



#class POVpanel(wx.Panel, AbstractUI):
class POVpanel(AbstractUI):

	def InitVariables(self):
		self.ca_deltaT = 0

	def InitUI(self):
		self.BoldFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
		self.RegFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)

		#self.Header = wx.StaticText(self, label="", pos=(20, POV_Y), size=(TOTAL_X-40, 140))
		self.Header = wx.StaticText(self, label="", pos=(220, POV_Y), size=(TOTAL_X-210, 200))
		self.Header.SetFont(self.RegFont)
		self.Header.Wrap(self.GetSize().width)
		#self.Header.SetLabel("Select which body the animation should focus on. 'Current\nObject' will follow the last object selected, whether it comes\nfrom the Drop down selection, a paused slideshow selection\nor a Close Approach object pick.\n\nYou may also choose any particular planet or the sun." )
		Description = "Select which body the animation\nshould focus on. 'Current Object'\nwill follow the last object selected,\nwhether it comes from the Drop\ndown selection, a paused slide-\nshow selection or a Close App-\nroach object pick.\n\nYou may also choose any parti-\ncular planet or the sun."
		self.Header.SetLabel(Description)
		
		lblList = ['Current Object', 'Sun', 'Earth', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Sedna', 'Makemake', 'Haumea','Eris','Charon', 'Phobos', 'Deimos', 'Moon']
		self.rbox = wx.RadioBox(self, label = ' Focus on ', pos = (20, POV_Y), size=(170, 610), choices = lblList ,majorDimension = 1, style = wx.RA_SPECIFY_COLS)
		self.rbox.SetFont(self.RegFont)
		self.rbox.Bind(wx.EVT_RADIOBOX,self.OnRadioBox)

		self.cb = wx.CheckBox(self, label="Show Local Referential", pos=(200, POV_Y+580))
		#print "Y local ref=", POV_Y+580
		#print "Y bottom info=", POV_FOCUS_Y+80+TOTAL_Y-160

		self.cb.SetValue(False)
		self.cb.Bind(wx.EVT_CHECKBOX,self.OnLocalRef)

		self.Title = wx.StaticText(self, label="", pos=(200, POV_FOCUS_Y+60), size=(TOTAL_X-210, TOTAL_Y -240))# -160))
		self.Title.SetFont(self.BoldFont)
		self.Info = wx.StaticText(self, label="", pos=(200, POV_FOCUS_Y+80), size=(TOTAL_X-210, TOTAL_Y -240)) #-160))
		self.Info.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL)) #self.RegFont)

		self.Info.Wrap(self.GetSize().width)
		self.setSunFocus()
		self.resetPOV()
		self.Hide()

	def OnLocalRef(self, e):
		#print "on local ref -> "+str(self.cb.GetValue())
		print "currentPOV:",self.SolarSystem.currentPOVselection
		self.setLocalRef()

	def setLocalRef(self):
		self.SolarSystem.setFeature(LOCAL_REFERENTIAL, self.cb.GetValue())
		orbit3D.glbRefresh(self.SolarSystem, self.parentFrame.orbitalBox.AnimationInProgress)

	def setCurrentBodyFocus(self):
		if self.parentFrame.orbitalBox.currentBody == None:
			self.rbox.SetSelection(1)
			#self.SolarSystem.resetView()
			self.setSunFocus()

		else:
			self.SolarSystem.currentPOV = self.parentFrame.orbitalBox.currentBody
			self.parentFrame.orbitalBox.updateCameraPOV()
			self.setBodyFocus(self.SolarSystem.currentPOV)

	def setCurrentBodyFocusManually(self, body, selectIndex):
		#self.SolarSystem.currentPOV = body
		# TODO check the body's option box in POV tab 
		#self.parentFrame.orbitalBox.updateCameraPOV()
		self.setBodyFocus(body) #self.SolarSystem.currentPOV)
		self.rbox.SetSelection(selectIndex)


	def setBodyFocus(self, Body):
		# display planet Info
		if Body.Mass == 0:
			mass = "???"
		else:
			mass = setPrecision(str(Body.Mass), 3)

		radius = Body.BodyRadius/1000 if Body.BodyRadius != 0 and Body.BodyRadius != DEFAULT_RADIUS else 0
		rev = round(float(Body.Revolution / 365.25) * 1000)/1000

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
				"Orb.Period(yrs)  ", Body.Revolution/365.25,
				"Rot.Period(days) ", Body.Rotation,
				"Orb.Incli.(deg) ", i,
				"Lg.of Asc Node(deg) ", N,
				"Arg. of Perih.(deg) ", w,
				"Eccentricity ", e,
				"Axial Tilt(deg) ", Body.AxialTilt))

		if self.SolarSystem.currentPOVselection != 'curobj':
			print "CurrentPOV", self.SolarSystem.currentPOVselection

			if (Body.SolarSystem.ShowFeatures & Body.BodyType) == 0:
				#print "MAKING OBJECT VISIBLE"
				# if the body is not visible, Make it so
				#print "Making "+Body.Name+" visible! bodyType = "+str(Body.BodyType)
				#for i in range(len(body.BodyShape)):

				#Body.BodyShape.visible = True
				Body.Origin.visible = True
				Body.Labels[0].visible = True
				#planetBody.SolarSystem.ShowFeatures |= planetBody.BodyType
				Body.SolarSystem.setFeature(Body.BodyType, True)
				self.parentFrame.orbitalBox.checkboxList[Body.BodyType].SetValue(True)
				#glbRefresh(self.SolarSystem, self.parentFrame.orbitalBox.AnimationInProgress)
			#else:
			#	print "OBJECT ALREADY VISIBLE"

		self.SolarSystem.currentPOV = Body
		self.SolarSystem.currentPOVselection = Body.JPL_designation
		self.parentFrame.orbitalBox.updateCameraPOV()
		#print "END setBodyFocus..."

	def setPlanetFocus(self):
		#print "Focusing on "+self.SolarSystem.currentPOVselection
		planetBody = self.SolarSystem.getBodyFromName(self.SolarSystem.currentPOVselection)
		#print planetBody.Name
		return self.setBodyFocus(planetBody)

	def setSunFocus(self):
		mass = setPrecision(str(self.SolarSystem.Mass), 3)
		#radius = self.SolarSystem.BodyRadius * 1e-3

		self.Title.SetLabel(self.SolarSystem.Name)
		self.Info.SetLabel("{:<17}{:>10}\n{:<19}{:>6.1f}\n{:<14}{:>10.2f}\n{:<20}{:>7.2f}".
		format(	"Mass(kg) ", mass,
				"Radius(km) ", self.SolarSystem.BodyRadius,
				"Rot.Period(days) ", self.SolarSystem.Rotation,
				"Axial Tilt(deg) ", self.SolarSystem.AxialTilt))

		self.resetPOV()

	def resetPOV(self):
		self.SolarSystem.resetView()
		self.rbox.SetSelection(1)
		self.SolarSystem.currentPOVselection = "SUN"
		self.SolarSystem.currentPOV = None

	def OnRadioBox(self, e):
		index = self.rbox.GetSelection()

		self.SolarSystem.currentPOVselection = {0: "curobj", 1: "sun", 2:"earth", 3:"mercury", 4:"venus",
												5: "mars", 6:"jupiter", 7:"saturn", 8:"uranus", 9:"neptune",
												10:"pluto", 11:"sedna", 12:"makemake", 13:"haumea", 14:"eris", 15:"charon", 16: "phobos", 17:"deimos", 18:"moon"}[index]
		{0:	self.setCurrentBodyFocus, 1: self.setSunFocus,
		 2: self.setPlanetFocus, 3: self.setPlanetFocus,
		 4: self.setPlanetFocus, 5: self.setPlanetFocus,
		 6: self.setPlanetFocus, 7: self.setPlanetFocus,
		 8: self.setPlanetFocus, 9: self.setPlanetFocus,
		 10: self.setPlanetFocus, 11: self.setPlanetFocus,
		 12: self.setPlanetFocus, 13: self.setPlanetFocus,
		 14: self.setPlanetFocus, 15: self.setPlanetFocus,
		 16: self.setPlanetFocus, 17: self.setPlanetFocus,
		 18: self.setPlanetFocus }[index]()

		self.setLocalRef()

	def getCurrentPOVselection(self):
		return self.SolarSystem.currentPOVselection

	def OnReset(self, e):
		self.resetPOV()

#class JPLpanel(wx.Panel, AbstractUI):
class JPLpanel(AbstractUI):

	def InitVariables(self):
		self.ca_deltaT = 0 # close approach deltaT
		self.Hide()

	def InitUI(self):
		self.fetchDate = datetime.date.today()
		self.fetchDateStr = self.fetchDate.strftime('%Y-%m-%d')

		self.BoldFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
		self.RegFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)

		self.heading = wx.StaticText(self, label='Close Approach for '+self.fetchDateStr, pos=(20, MAIN_HEADING_Y))
		self.heading.SetFont(self.BoldFont)

		self.download = wx.Button(self, label='Download List', pos=(320, JPL_DOWNLOAD_Y))
		self.download.Bind(wx.EVT_BUTTON, self.OnCloseApproach)

		self.next = wx.Button(self, label='Next', pos=(405, JPL_DOWNLOAD_Y), size=(50,35))
		self.next.Bind(wx.EVT_BUTTON, self.OnNext)
		self.next.Hide()

		self.prev = wx.Button(self, label='Prev', pos=(345, JPL_DOWNLOAD_Y), size=(50,35))
		self.prev.Bind(wx.EVT_BUTTON, self.OnPrev)
		self.prev.Hide()

		self.ListIndex = 0
		self.list = wx.ListCtrl(self, pos=(20, JPL_LISTCTRL_Y), size=(440, JPL_LIST_SZ), style = wx.LC_REPORT|wx.BORDER_SUNKEN|wx.LC_HRULES)
		self.list.InsertColumn(0, 'Name', width = 145)
		self.list.InsertColumn(1, 'PHA', wx.LIST_FORMAT_CENTER, width = 45)
		self.list.InsertColumn(2, 'SPK-ID', wx.LIST_FORMAT_CENTER, width = 70)
		self.list.InsertColumn(3, 'Miss Distance ', wx.LIST_FORMAT_RIGHT, width = 180)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListClick, self.list)

		self.legend = wx.StaticText(self, label="", pos=(20, JPL_BRW_Y))
		self.legend.SetFont(self.RegFont)
		self.legend.Wrap(230)

		self.SetSize((TOTAL_X, TOTAL_Y))
		self.Centre()

	def OnNext(self, e):
		self.oneDay(1, "", self.nextUrl) #NASA_API_V1_FEED_TODAY_HOST, self.nextUrl)

	def OnPrev(self, e):
		self.oneDay(-1, "", self.prevUrl) #NASA_API_V1_FEED_TODAY_HOST, self.prevUrl)

	def oneDay(self, incr, host, url):
		self.ca_deltaT += incr
		self.fetchDate = datetime.date.today() + datetime.timedelta(days = self.ca_deltaT)
		self.fetchDateStr = self.fetchDate.strftime('%Y-%m-%d')
#		self.fetchJPL(host, url)
		self.fetchJPL(NASA_API_V1_FEED_TODAY_HOST, NASA_API_V1_FEED_TODAY_URL)
		self.heading.SetLabel('Close Approaches On '+self.fetchDateStr)

	def OnCloseApproach(self, event):
		self.download.SetLabel("Fetching ...")
		self.fetchDate = datetime.date.today()
		self.fetchDateStr = self.fetchDate.strftime('%Y-%m-%d')
		self.fetchJPL(NASA_API_V1_FEED_TODAY_HOST, NASA_API_V1_FEED_TODAY_URL)
		self.download.Hide()
		self.next.Show()
		self.prev.Show()
		self.legend.SetLabel("To display orbit details, double click on desired row")



		"""
		{
			u'orbital_data': {
				u'last_observation_date': u'2021-12-21', 
				u'equinox': u'J2000', 
				u'first_observation_date': u'2021-12-12', 
				u'orbit_uncertainty': u'6', 
				u'aphelion_distance': u'1.18532314028115', 
				u'data_arc_in_days': 9, 
				u'orbit_class': {
					u'orbit_class_type': u'APO', 
					u'orbit_class_description': u'Near-Earth asteroid orbits which cross the Earth\u2019s orbit similar to that of 1862 Apollo', 
					u'orbit_class_range': u'a (semi-major axis) > 1.0 AU; q (perihelion) < 1.017 AU'
				}, 
				u'mean_anomaly': u'318.8328851178307', 
				u'orbital_period': u'375.1140964088063', 
				u'ascending_node_longitude': u'270.7427283860751', 
				u'orbit_id': u'2', 
				u'inclination': u'5.221606940066634', 
				u'observations_used': 27, 
				u'epoch_osculation': u'2459600.5', 
				u'mean_motion': u'.9597080020359068', 
				u'jupiter_tisserand_invariant': u'5.981', 
				u'orbit_determination_date': u'2021-12-21 04:57:50', 
				u'perihelion_time': u'2459643.395458613285', 
				u'eccentricity': u'.1644659421290264', 
				u'perihelion_argument': u'268.1851698378069', 
				u'minimum_orbit_intersection': u'.000831432', 
				u'semi_major_axis': u'1.017911385294781', 
				u'perihelion_distance': u'.8504996303084128'
			}, 
			u'links': {
				u'self': u'http://www.neowsapp.com/rest/v1/neo/54231259?api_key=KTTV4ZQFuTywtkoi3gA59Qdlk5H2V1ry6UdYL0xU'
			}, 
			u'nasa_jpl_url': u'http://ssd.jpl.nasa.gov/sbdb.cgi?sstr=54231259', 
			u'absolute_magnitude_h': 27.489, 
			u'estimated_diameter': {
				u'feet': {
					u'estimated_diameter_max': 61.9762122093, 
					u'estimated_diameter_min': 27.7166046976
				}, 
				u'miles': {
					u'estimated_diameter_max': 0.011737915, 
					u'estimated_diameter_min': 0.0052493552
				}, 
				u'meters': {
					u'estimated_diameter_max': 18.8903488769, 
					u'estimated_diameter_min': 8.4480208415
				}, 
				u'kilometers': {
					u'estimated_diameter_max': 0.0188903489, 
					u'estimated_diameter_min': 0.0084480208
				}
			}, 
			u'close_approach_data': [
				{	u'epoch_date_close_approach': 1640218740000L, 
					u'orbiting_body': u'Earth', 
					u'close_approach_date': u'2021-12-23', 
					u'relative_velocity': {
						u'kilometers_per_second': u'5.7756022357', 
						u'miles_per_hour': u'12919.4446409401', 
						u'kilometers_per_hour': u'20792.1680483635'
					}, 
					u'miss_distance': {
						u'astronomical': u'0.0037073317', 
						u'miles': u'344618.0062828502', 
						u'lunar': u'1.4421520313', 
						u'kilometers': u'554608.925703479'
					}, 
					u'close_approach_date_full': u'2021-Dec-23 00:19'
				}
			], 
			u'neo_reference_id': u'54231259', 
			u'is_potentially_hazardous_asteroid': False, 
			u'is_sentry_object': False, 
			u'id': u'54231259', 
			u'name': u'(2021 YB)'
		}
		"""

	def fetchJPL(self, host, url):
		import ssl

		url = url+"&start_date="+self.fetchDateStr
		#print host+url+"\n"
		try:

			#opener = urllib2.build_opener()
			#opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36')]
			#response = opener.urlopen(host+url)
			
			print host
			print url
			
			####
			#req = urllib2.Request(host+url, headers={ 'X-Mashape-Key': 'XXXXXXXXXXXXXXXXXXXX', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36' })
			req = urllib2.Request(host+url, headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36' })
 			#response = urllib2.urlopen(req).read()
			#gcontext = ssl.SSLContext()  # Only for gangstars
			gcontext = ssl._create_unverified_context()
			response = urllib2.urlopen(req, context=gcontext)
			####


			#c = httplib.HTTPSConnection(host)
			#c.request("GET", url)
			#response = c.getresponse()
			#print response
			#response = urllib2.urlopen(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})

		except urllib2.HTTPError as err:
			print "Exception...\n\nError: " + str(err.code)
			raise

		#response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})

		self.BodiesSPK_ID = []
		rawResp = response.read()
		#print rawResp
		self.jsonResp = json.loads(rawResp)

		# use if "prev" not in "links"  
		self.nextUrl = self.jsonResp["links"]["next"] if "next" in self.jsonResp["links"] else ""
		self.prevUrl = self.jsonResp["links"]["prev"] if "prev" in self.jsonResp["links"] else ""
		self.selfUrl = self.jsonResp["links"]["self"] if "self" in self.jsonResp["links"] else ""
 
		if self.ListIndex != 0:
			self.list.DeleteAllItems()

 		#print "*****PREV "+self.prevUrl
 		#print "*****CURR "+self.selfUrl
 		#print "*****NEXT "+self.nextUrl

		self.ListIndex = 0
		if self.jsonResp["element_count"] > 0:
#			for i in range(0, len(self.jsonResp[self.fetchDateStr])-1):
			today = self.jsonResp["near_earth_objects"][self.fetchDateStr]
			for entry in today:
				if entry["close_approach_data"][0]["orbiting_body"].upper() == 'EARTH':
					self.list.InsertStringItem(self.ListIndex, entry["name"])
					if entry["is_potentially_hazardous_asteroid"] == True:
							ch = "Y"
					else:
							ch = "N"
					self.list.SetStringItem(self.ListIndex, 1, ch)
					self.list.SetStringItem(self.ListIndex, 2, entry["neo_reference_id"])
					self.list.SetStringItem(self.ListIndex, 3, str(round(float(entry["close_approach_data"][0]["miss_distance"]["lunar"]) * 100)/100)  +
											" LD | " + str(round(float(entry["close_approach_data"][0]["miss_distance"]["astronomical"]) * 100)/100) + " AU ")
					#self.list.SetStringItem(self.ListIndex, 3, entry["close_approach_data"][0]["miss_distance"]["astronomical"] + " AU ")
					# record the spk-id corresponding to this row
					self.BodiesSPK_ID.append(entry["neo_reference_id"])
					self.ListIndex += 1

	
	def fetchDetailsXX(self, link):
		#https://api.nasa.gov/neo/rest/v1/neo/3542519?api_key=DEMO_KEY
		#url = NASA_API_KEY_DETAILS+
		#url = url+"&start_date="+self.fetchDateStr
		#print host+url+"\n"
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36')]
			response = opener.open(link)

			#c = httplib.HTTPSConnection(host)
			#print url
			#c.request("GET", url)
			#response = c.getresponse()
			#print response
			rawResp = response.read()
			print rawResp
			return json.loads(rawResp)
			#response = urllib2.urlopen(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})
		except urllib2.HTTPError as err:
			print "Exception...\n\nError: " + str(err.code)
			raise

	def OnListClick(self, e):
		#print e.GetText() + " - " + self.BodiesSPK_ID[e.m_itemIndex] + " - " + str(e.m_itemIndex)
		# load orbital elements
		id = self.loadBodyInfo(e.m_itemIndex)
		
		# switch to main panel to display orbit
		self.nb.SetSelection(PANEL_MAIN)
		
		# If slide show in progress, stop it, and reset body List
		self.parentFrame.orbitalBox.stopSlideSHow()
		self.parentFrame.orbitalBox.resetBodyList()

		# make sure to reset the date to today's date
		####### self.parentFrame.orbitalBox.resetDate(self.ca_deltaT)  <<<<<<<<<<<----------------------
		self.parentFrame.orbitalBox.setCurrentBodyFromId(id)
		if self.SolarSystem.currentPOVselection == "curobj":
			self.SolarSystem.currentPOV = self.parentFrame.orbitalBox.currentBody
			self.parentFrame.orbitalBox.updateCameraPOV()
		toggle = False
		if self.SolarSystem.isRealsize():
			toggle = True
		self.parentFrame.orbitalBox.currentBody.toggleSize(toggle)

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

	def loadBodyInfo(self, index):
		entry = self.jsonResp["near_earth_objects"][self.fetchDateStr][index]
		print entry

		# if the key already exists, the object has already been loaded, simply return its spk-id
		#if entry["neo_reference_id"] in objects_data:
		#	return entry["neo_reference_id"]

		# grab details link
		#entry = self.fetchDetails(entry["links"]["self"])
		utc_timestamp = entry["close_approach_data"][0]["epoch_date_close_approach"]*0.001
		
		utc_close_approach = datetime.datetime.utcfromtimestamp(utc_timestamp)

		# utc_close_approach is a naive datetime object
		print "LOADBODY_INFO utc_close_approach= ", utc_close_approach, "==? timestamp=", utc_timestamp

		# otherwise add data to dictionary
		objects_data[entry["neo_reference_id"]] = {
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
			"utc": utc_close_approach,
#			"local": orbit3D.datetime_from_utc_to_local(utc_close_approach)
			"local": datetime.datetime.fromtimestamp(utc_timestamp) #, utc_close_approach.TZ)
#			"local": orbit3D.UTC_to_local(utc_close_approach)
		}
		print "UTCstr =========>", objects_data[entry["neo_reference_id"]]["utcstr"]
		print "Local  --------->", objects_data[entry["neo_reference_id"]]["local"]
		"""
		{'orbital_data': 
			{'last_observation_date': '2021-05-25', 
			 'equinox': 'J2000', 
			 'first_observation_date': '2021-05-18', 
			 'orbit_uncertainty': '8', 
			 'aphelion_distance': '3.366832672811661', 
			 'data_arc_in_days': 7, 
			 'orbit_class': {
			 					'orbit_class_type': 'APO', 
			 					'orbit_class_description': 'Near-Earth asteroid orbits which cross the Earths orbit similar to that of 1862 Apollo', 
			 					'orbit_class_range': 'a (semi-major axis) > 1.0 AU; q (perihelion) < 1.017 AU'
			 				}, 
			 'mean_anomaly': '350.1777410030417', 
			 'orbital_period': '1161.694290418128', 
			 'ascending_node_longitude': '65.36895860260729', 
			 'orbit_id': '6', 
			 'inclination': '9.045387641087999', 
			 'observations_used': 28, 
			 'epoch_osculation': '2459354.5', 
			 'mean_motion': '.3098922005293023', 
			 'jupiter_tisserand_invariant': '3.464', 
			 'orbit_determination_date': '2021-05-25 09:49:07', 
			 'perihelion_time': '2459386.195728321596', 
			 'eccentricity': '.5567752354409493', 
			 'perihelion_argument': '211.3061357765496', 
			 'minimum_orbit_intersection': '.00110192', 
			 'semi_major_axis': '2.162696705448312', 
			 'perihelion_distance': '.9585607380849626'
			}, 
		'links': {
			'self': 'http://www.neowsapp.com/rest/v1/neo/54146674?api_key=KTTV4ZQFuTywtkoi3gA59Qdlk5H2V1ry6UdYL0xU'
		}, 
		'nasa_jpl_url': 'http://ssd.jpl.nasa.gov/sbdb.cgi?sstr=54146674', 
		'absolute_magnitude_h': 26.119, 
		'estimated_diameter': {
			'feet': {
				'estimated_diameter_max': 116.4729378467, 
				'estimated_diameter_min': 52.0882813128
			}, 
			'miles': {
				'estimated_diameter_max': 0.022059261, 
				'estimated_diameter_min': 0.0098652014
			}, 
			'meters': {
				'estimated_diameter_max': 35.5009503196, 
				'estimated_diameter_min': 15.8765076361
			}, 
			'kilometers': {
				'estimated_diameter_max': 0.0355009503, 
				'estimated_diameter_min': 0.0158765076
			}
		}, 
		'close_approach_data': [{
								'epoch_date_close_approach': 1622077320000L, 
								'orbiting_body': 'Earth', 
								'close_approach_date': '2021-05-27', 
								'relative_velocity': {
									'kilometers_per_second': '11.1194145219', 
									'miles_per_hour': '24873.0183439614', 
									'kilometers_per_hour': u'40029.8922787165'
								},
								'miss_distance': {
									'astronomical': '0.0040865681', 
									'miles': '379870.2315093886', 
									'lunar': '1.5896749909', 
									'kilometers': '611341.883369947'
								}, 
								'close_approach_date_full': '2021-May-27 01:02'
								}], 
		'neo_reference_id': '54146674', 
		'is_potentially_hazardous_asteroid': False, 
		'is_sentry_object': False, 
		'id': '54146674', 
		'name': '(2021 KP)'
	}
		"""

		"""
		{
		'epochJD': 2459352.5, 
		'Tp_Time_of_perihelion_passage_JD': 2459406.6742558605, 
		'radius': 0.0084763715, 
		'orbit_class': 'N/A', 
		'iau_name': u'(2021 KW)', 
		'W_argument_of_perihelion': 221.3606034753813, 
		'earth_moid': 559452653.0018396, 
		'local': datetime(2021, 5, 22, 8, 21), 
		'material': 0, 
		'utc': '2021-05-22 15:21:00', 
		'IN_orbital_inclination': 0.3739940530040262, 
		'epoch_date_close_approach': datetime(2021, 5, 22, 15, 21), 
		'N_mean_motion': 0.46579168692434, 
		'jpl_designation': u'54146681', 
		'QR_perihelion': 110379200877.4296, 
		'EC_e': 0.5523345202621396, 
		'name': u'(2021 KW)', 
		'longitude_of_perihelion': 317.9484100244705, 
		'OM_longitude_of_ascendingnode': 96.58780654908915, 
		'absolute_mag': 27.724, 
		'mass': 0.0, 
		'axial_tilt': 0.0, 
		'MA_mean_anomaly':334.7660819748012, 
		'PR_revolution': 772.8776835351206
		}
		"""

		# convert UTC to local time
		utcNewdate = objects_data[entry["neo_reference_id"]]["utc"]

		# for animation sake, calculate the dayIncrement
		
		#utcNewdate = objects_data[entry["neo_reference_id"]]["utc"]
		self.SolarSystem.utcTimeInCurrentDay = (utcNewdate).hour * TI_ONE_HOUR + \
											(utcNewdate).minute * TI_ONE_MINUTE + \
											(utcNewdate).second * TI_ONE_SECOND
		self.SolarSystem.utcDaysIncrement = (utcNewdate.day - self.SolarSystem.utcTodayDate.day) + self.SolarSystem.utcTimeInCurrentDay

		newdate = objects_data[entry["neo_reference_id"]]["local"]
		self.SolarSystem.TimeInCurrentDay = (newdate).hour * TI_ONE_HOUR + \
											(newdate).minute * TI_ONE_MINUTE + \
											(newdate).second * TI_ONE_SECOND
		self.SolarSystem.DaysIncrement = (newdate.day - self.SolarSystem.todayDate.day) + self.SolarSystem.TimeInCurrentDay


		print objects_data[entry["neo_reference_id"]]
		# print time of closest approach on this date
		#utc = datetime.utcfromtimestamp(objects_data[entry["neo_reference_id"]]["epoch_date_close_approach"])
		#print "Local Time of approach: ", orbit3D.datetime_from_utc_to_local(utc_close_approach).strftime('%Y-%m-%d %H:%M:%S')
 		print "Local Time of approach: ", datetime.datetime.fromtimestamp(utc_timestamp)

		# CLose approach objects are considered as PHAs
		body = orbit3D.pha(self.SolarSystem, entry["neo_reference_id"], orbit3D.getColor())
		self.SolarSystem.addTo(body)
		return entry["neo_reference_id"]


#
# Orbital Control Panel
#

#class orbitalCtrlPanel(wx.Panel, AbstractUI):
class orbitalCtrlPanel(AbstractUI):

	def InitVariables(self):
		self.Earth = self.SolarSystem.getBodyFromName("earth")
		self.checkboxList = {}
		self.ResumeSlideShowLabel = False
		self.AnimationInProgress = False
		self.Source = PHA
		self.TimeIncrement = INITIAL_TIMEINCR
		self.BaseTimeIncrement = INITIAL_TIMEINCR
		self.TimeIncrementKey = INITIAL_INCREMENT_KEY
		self.AnimLoop = 0
#		self.todayDate = datetime.date.today()

#		self.DaysIncrement = 0 # number of days from today - used for animation into future or past (detalT < 0)
		self.velocity = 0
		self.distance = 0
		self.list = []
		self.listjplid = []
		self.DetailsOn = False
		self.currentBody = None
		self.DisableAnimationCallback = True
		self.RecorderOn = False


		#self.InitUI()
		self.Hide()
		#f = codecs.open("unicode.txt", "r", "utf-8")


	def resetDate(self, DaysIncrement):
		self.SolarSystem.DaysIncrement = DaysIncrement
		self.SolarSystem.utcDaysIncrement = DaysIncrement
		self.updateSolarSystem()

	def createBodyList(self, xpos, ypos):
		for body in self.SolarSystem.bodies:
			if body.BodyType in [SPACECRAFT, PHA, BIG_ASTEROID, COMET, TRANS_NEPT]:
				self.list.append(body.Name)
				self.listjplid.append(body.JPL_designation)

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
			if self.SolarSystem.currentPOVselection == "curobj":
				self.SolarSystem.currentPOV = self.currentBody
				self.parentFrame.povBox.setBodyFocus(self.currentBody)
				self.updateCameraPOV()


	def setCurrentBody(self, body):
		if self.currentBody != None:
			self.currentBody.hide()

		self.currentBody = body
		self.currentBody.Details = True
		self.showObjectDetails(self.currentBody)

	def setCurrentBodyFromId(self, id):
		if self.currentBody != None:
			self.currentBody.hide()

		self.currentBody = self.SolarSystem.getBodyFromName(id)
		self.currentBody.Details = True
		self.showObjectDetails(self.currentBody)

	def setLocalDateTimeLabel(self, ldt):
		self.localTimeLabel.SetLabel("{:>2}:{:>2}:{:2}".format(str(ldt.tm_hour).zfill(2), str(ldt.tm_min).zfill(2), str(ldt.tm_sec).zfill(2)))
		self.localDateLabel.SetLabel("{:>2}/{:>2}/{:2}".format(str(ldt.tm_mon).zfill(2), str(ldt.tm_mday).zfill(2), str(ldt.tm_year).zfill(2)))

	def setUTCDateTimeLabel(self, utcdt):
		self.UTCtimeLabel.SetLabel("{:>2}:{:>2}:{:2}".format(str(utcdt.tm_hour).zfill(2), str(utcdt.tm_min).zfill(2), str(utcdt.tm_sec).zfill(2)))
		self.UTCdateLabel.SetLabel("{:>2}/{:>2}/{:2}".format(str(utcdt.tm_mon).zfill(2), str(utcdt.tm_mday).zfill(2), str(utcdt.tm_year).zfill(2)))

	def InitUI(self):
		self.BoldFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
		self.RegFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)

		heading = wx.StaticText(self, label='Show', pos=(20, MAIN_HEADING_Y))
		heading.SetFont(self.BoldFont)

		OFF_TIME = 0
		dateLabel = wx.StaticText(self, label='Orbital Date', pos=(200, DATE_Y))
		dateLabel.SetFont(self.BoldFont)
		wx.StaticText(self, label='Local Time: ', pos=(200+OFF_TIME, DATE_Y-18))
		wx.StaticText(self, label='Universal Time:', pos=(200+OFF_TIME, DATE_Y-33))

		self.localTimeLabel = wx.StaticText(self, label='hh:mm:ss', pos=(280+OFF_TIME+5, DATE_Y-18))
		self.localDateLabel = wx.StaticText(self, label='mm/dd/yyyy', pos=(280+OFF_TIME+75, DATE_Y-18))
		self.UTCtimeLabel = wx.StaticText(self, label='hh:mm:ss', pos=(280+OFF_TIME+5, DATE_Y-33))
		self.UTCdateLabel = wx.StaticText(self, label='mm/dd/yyyy', pos=(280+OFF_TIME+75, DATE_Y-33))

		lt = orbit3D.locationInfo.getLocalTime()
		utct = orbit3D.locationInfo.getUTCtime()

		self.setLocalDateTimeLabel(lt)
		self.setUTCDateTimeLabel(utct)

#		self.localTimeLabel.SetLabel("{:>2} : {:>2} : {:2}".format(str(lt.tm_hour).zfill(2), str(lt.tm_min).zfill(2), str(lt.tm_sec).zfill(2)))
#		self.localDateLabel.SetLabel("{:>2}/{:>2}/{:2}".format(str(lt.tm_mon).zfill(2), str(lt.tm_mday).zfill(2), str(lt.tm_year).zfill(2)))
#		self.UTCtimeLabel.SetLabel("{:>2} : {:>2} : {:2}".format(str(utct.tm_hour).zfill(2), str(utct.tm_min).zfill(2), str(utct.tm_sec).zfill(2)))
#		self.UTCdateLabel.SetLabel("{:>2}/{:>2}/{:2}".format(str(utct.tm_mon).zfill(2), str(utct.tm_mday).zfill(2), str(utct.tm_year).zfill(2)))

		# date spinner
		self.dateMSpin = wx.SpinCtrl(self, id=wx.ID_ANY, initial=self.SolarSystem.todayDate.month, min=1, max=12, pos=(200, DATE_SLD_Y), size=(65, 25), style=wx.SP_ARROW_KEYS)
		self.dateMSpin.Bind(wx.EVT_SPINCTRL,self.OnTimeSpin)
		self.dateDSpin = wx.SpinCtrl(self, id=wx.ID_ANY, initial=self.SolarSystem.todayDate.day, min=1, max=31, pos=(265, DATE_SLD_Y), size=(65, 25), style=wx.SP_ARROW_KEYS)
		self.dateDSpin.Bind(wx.EVT_SPINCTRL,self.OnTimeSpin)

		# Create a custom event in order to update the content of the day spinner if its value is out-of-range
		self.CustomEvent, EVT_RESET_SPINNER = wx.lib.newevent.NewEvent()
		self.dateDSpin.Bind(EVT_RESET_SPINNER, self.ResetSpinner) # bind it as usual
		# The day spinner has 2 events. one triggered when clicking on an arrow, and one
		# triggered programmatically to update the value of the day spinner in order to correct it
		# The firing of the EVT_RESET_SPINNER is programmatically done during the execution
		# of the EVT_SPINCTRL handler


		self.dateYSpin = wx.SpinCtrl(self, id=wx.ID_ANY, initial=self.SolarSystem.todayDate.year, min=-3000, max=3000, pos=(330, DATE_SLD_Y), size=(65, 25), style=wx.SP_ARROW_KEYS)
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
		self.createCheckBox(self, "Inner Oort Cloud", INNER_OORT_CLOUD, 20, CHK_L8)
		self.createCheckBox(self, "Ecliptic", ECLIPTIC_PLANE, 20, CHK_L9)
		self.createCheckBox(self, "Labels", LABELS, 20, CHK_L10)
		self.createCheckBox(self, "Lit Scene", LIT_SCENE, 20, CHK_L11)
		self.createCheckBox(self, "Adjust objects size", REALSIZE, 20, CHK_L12)
		self.createCheckBox(self, "Referential", REFERENTIAL, 20, CHK_L13)

		self.createBodyList(200, LSTB_Y)

		cbtn = wx.Button(self, label='Refresh', pos=(20, CHK_L14))
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

#		self.aniSpeed = wx.StaticText(self, label="10 mi", pos=(305, ANI_Y), size=(15, 20))
		self.aniSpeed = wx.StaticText(self, label= "%s %s" % (Frame_Intervals[self.TimeIncrementKey]["label"], Frame_Intervals[self.TimeIncrementKey]["unit"]), pos=(305, ANI_Y), size=(15, 20))
		self.aniSpeed.SetFont(self.BoldFont)
		self.aniSpeedSlider = wx.Slider(self, id=wx.ID_ANY, value=1, minValue=-24, maxValue=24, pos=(195, ANI_Y+30), size=(150, 20), style=wx.SL_HORIZONTAL)
		self.aniSpeedSlider.Bind(wx.EVT_SLIDER,self.OnAnimSpeedSlider)


		self.Animate = wx.Button(self, label='>', pos=(360, ANI_Y), size=(35, 35))
		self.Animate.Bind(wx.EVT_BUTTON, self.OnAnimate)

		self.Stepper = wx.Button(self, label='+', pos=(395, ANI_Y), size=(35, 35))
		self.Stepper.Bind(wx.EVT_BUTTON, self.OnStepper)

		#s = u'\u25a0' # square character
		self.Recorder = wx.Button(self, label=u'\u25a0', pos=(440, ANI_Y), size=(35, 35))
		self.Recorder.Bind(wx.EVT_BUTTON, self.OnRecord)

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

		self.setDeltaT()

	def setCameraPOV(self, body):
		self.SolarSystem.currentPOV = body

	def updateCameraPOV(self):

		# the following values will do the following
		# (0,-1,-1): freezes rotation and looks down towards the left
		# (0,-1, 1): freezes rotation and looks up towards the left
		# (0, 1, 1): freezes rotation and looks up towards the right
		# (0, 1,-1): freezes rotation and looks down towards the right

		#self.SolarSystem.Scene.forward = (0, 0, -1)
		# For a planet, Foci(x, y, z) is (0,0,0). For a moon, Foci represents the position of the planet the moon orbits around
		self.SolarSystem.Scene.center = (self.SolarSystem.currentPOV.Position[X_COOR]+self.SolarSystem.currentPOV.Foci[X_COOR],
										 self.SolarSystem.currentPOV.Position[Y_COOR]+self.SolarSystem.currentPOV.Foci[Y_COOR],
										 self.SolarSystem.currentPOV.Position[Z_COOR]+self.SolarSystem.currentPOV.Foci[Z_COOR])

	def updateSolarSystem(self):
		self.refreshDate()
		self.SolarSystem.animate(self.SolarSystem.DaysIncrement)
#		self.SolarSystem.animate(self.SolarSystem.utcDaysIncrement)
		for body in self.SolarSystem.bodies:
			if body.BodyType in [SPACECRAFT, OUTERPLANET, INNERPLANET, SATELLITE, ASTEROID, COMET, DWARFPLANET, PHA, BIG_ASTEROID, TRANS_NEPT]:
#				if body.BodyShape.visible == True:
				if body.Origin.visible == True:
					velocity, distance = body.animate(self.SolarSystem.DaysIncrement)
#					velocity, distance = body.animate(self.SolarSystem.utcDaysIncrement)
					if self.SolarSystem.currentPOV != None:
						if body.JPL_designation == self.SolarSystem.currentPOV.JPL_designation:
							self.updateCameraPOV()

					if body.BodyType == self.Source or body.Details == True:
						self.velocity = velocity
						self.distance = distance

	def OnValidateDate(self, e):

		ztime = self.localTimeLabel.GetLabel().split(":")
		if len(ztime) > 0:
			#self.timeInDay = (float(ztime[0]) * TI_ONE_HOUR) + (float(ztime[1]) * TI_ONE_MINUTE) + (float(ztime[2]) * TI_ONE_SECOND)
			
			new_Localdate =datetime.datetime(self.dateYSpin.GetValue(), self.dateMSpin.GetValue(), self.dateDSpin.GetValue(), int(ztime[0]), int(ztime[1]), int(ztime[2]))
			# newLocaldate is naive (no tz info)

#			utcNewdate = orbit3D.local_to_utc(newLocaldate)
			NewUTCdate, NewLocaldate = orbit3D.local_to_UTC(new_Localdate) # tz aware date

#		newdate = datetime(self.dateYSpin.GetValue(),self.dateMSpin.GetValue(),self.dateDSpin.GetValue())

#		self.SolarSystem.DaysIncrement = (newdate - self.SolarSystem.todayDate).days 
		self.SolarSystem.DaysIncrement = (NewLocaldate - self.SolarSystem.todayDate).days + self.SolarSystem.TimeInCurrentDay
#		self.SolarSystem.utcDaysIncrement = (NewUTCdate - self.SolarSystem.utcTodayDate).days + self.SolarSystem.utcTimeInCurrentDay


		"""
		ztime = split(self.localTimeLabel.Getvalue(), " : ")
		print len(ztime)
		if len(ztime) > 0:
			self.DaysIncrement += (float(ztime[0]) * TI_ONE_HOUR) + (float(ztime[1]) * TI_ONE_MINUTE) + (float(ztime[2]) * TI_ONE_SECOND)
			print "##############", self.DaysIncrement
		"""
		self.OneTimeIncrement()
		self.disableBeltsForAnimation()
		self.SolarSystem.DaysIncrement -= self.TimeIncrement

		self.setLocalDateTimeLabel(NewLocaldate) ##################

		self.refreshDate()

	def setVelocityLabel(self):
		if self.DetailsOn == True:
			self.ObjVelocity.SetLabel("{:<12}{:>10.4f}".format("Vel.(km/s)", round(self.velocity/1000, 2)))

	def setDistanceLabel(self):
		if self.DetailsOn == True:
			#print "distance="+str(self.distance)
			self.ObjDistance.SetLabel("{:<12}{:>10.4f}".format("DTE (AU)", float(self.distance)))



	def deltaTtick(self, timeinsec):
		# make sure to convert timeinsec as a fraction of day
		#print self.SolarSystem.DaysIncrement, "+", float(timeinsec)/86400, "for", timeinsec 
		self.SolarSystem.DaysIncrement += float(timeinsec)/86400

		#print self.SolarSystem.DaysIncrement

	def refreshDate(self):
		# update date spin wheels
		time_delta = datetime.timedelta(days = self.SolarSystem.DaysIncrement)
		#print time_delta.seconds

		newdate = self.SolarSystem.todayDate + time_delta
		self.dateDSpin.SetValue(newdate.day)
		self.dateMSpin.SetValue(newdate.month)
		self.dateYSpin.SetValue(newdate.year)

		# update time display
		self.updateTimeDisplay(time_delta)

		"""
		zdelta = time_delta.seconds
		hours = zdelta / 3600
		zdelta -= hours * 3600
		minutes = zdelta / 60
		zdelta -= minutes * 60
		seconds = zdelta
		self.localTimeLabel.SetLabel("{:>2} : {:>2} : {:2}".format(str(hours).zfill(2), str(minutes).zfill(2), str(seconds).zfill(2)))
		"""

		self.setVelocityLabel()
		self.setDistanceLabel()

	def updateTimeDisplay(self, timeDelta):
		zdelta = timeDelta.seconds
		hours = zdelta / 3600
		zdelta -= hours * 3600
		minutes = zdelta / 60
		zdelta -= minutes * 60
		seconds = zdelta
		self.localTimeLabel.SetLabel("{:>2} : {:>2} : {:2}".format(str(hours).zfill(2), str(minutes).zfill(2), str(seconds).zfill(2)))



	def disableBeltsForAnimation(self):
		self.checkboxList[JTROJANS].SetValue(False)
		self.checkboxList[ASTEROID_BELT].SetValue(False)
		self.checkboxList[KUIPER_BELT].SetValue(False)
		self.checkboxList[INNER_OORT_CLOUD].SetValue(False)
		self.SolarSystem.setFeature(JTROJANS|ASTEROID_BELT|KUIPER_BELT|INNER_OORT_CLOUD, False)
		#self.SolarSystem.ShowFeatures = (self.SolarSystem.ShowFeatures & ~(JTROJANS|ASTEROID_BELT|KUIPER_BELT|INNER_OORT_CLOUD))
		orbit3D.glbRefresh(self.SolarSystem, self.AnimationInProgress)

	def updateJTrojans(self):
		curTrojans = self.SolarSystem.getJTrojans()
		JupiterBody = self.SolarSystem.getBodyFromName(objects_data[curTrojans.PlanetName]['jpl_designation'])
		# if Jupiter coordinates haven't changed since this Trojans were generated, don't do anything
		if JupiterBody.Position[X_COOR] == curTrojans.JupiterX and JupiterBody.Position[Y_COOR] == curTrojans.JupiterY:
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
#		self.aniSpeed.SetLabel(str(self.aniSpeedSlider.GetValue()*10)+" mi")
		self.aniSpeed.SetLabel(str(self.aniSpeedSlider.GetValue()*Frame_Intervals[self.TimeIncrementKey]["value"])+" "+Frame_Intervals[self.TimeIncrementKey]["unit"])
		
		return

	def OnAnimTimeSlider(self, e):
		self.TimeIncrementKey = float(self.aniTimeSlider.GetValue())
		self.BaseTimeIncrement = Frame_Intervals[self.TimeIncrementKey]["incr"]
		#print "OnAnimTimeSlider", self.TimeIncrementKey, self.BaseTimeIncrement

#		self.TimeIncrement = float(self.aniTimeSlider.GetValue()) * BaseTimeIncrement
		# copy time increment to solarsystem class for realtime update
#		self.SolarSystem.setTimeIncrement(self.TimeIncrement)
#		self.aniTimeSpeed.SetLabel(str(self.aniSpeedSlider.GetValue()*Frame_Intervals[TimeIncrementKey]["value"])+" "+Frame_Intervals[TimeIncrementKey]["unit"])

		# finally reflect new time interval in speed slider		
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
				self.parentFrame.povBox.setSunFocus()

			#if self.SolarSystem.currentPOV != None and self.SolarSystem.currentPOV.BodyType == type:
			#		self.parentFrame.povBox.resetPOV()
			"""
		for type, cbox in self.checkboxList.iteritems():
			if cbox.GetValue() == True:
				self.SolarSystem.ShowFeatures |= type
			else:
				if self.SolarSystem.currentPOV != None and self.SolarSystem.currentPOV.BodyType == type:
					self.parentFrame.povBox.resetPOV()
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
			if self.SolarSystem.currentPOVselection == "curobj":
				self.SolarSystem.currentPOV = self.currentBody
				self.updateCameraPOV()

	def showObjectDetails(self, body):
		self.InfoTitle.SetLabel(body.Name)
		self.velocity, self.distance = body.animate(self.SolarSystem.DaysIncrement)
		if body.Mass == 0:
			mass = "???"
		else:
			mass = setPrecision(str(body.Mass), 3)

		radius = round(float(body.BodyRadius) * 1000)/1000 if body.BodyRadius != 0 and body.BodyRadius != DEFAULT_RADIUS else 0
		moid = round(float(body.Moid/AU) * 10000)/10000 if body.Moid != 0 else 0
		rev = round(float(body.Revolution / 365.25) * 1000)/1000
		H = body.Absolute_mag if body.Absolute_mag != 0 else 0

		i = round(float(body.Inclination) * 1000)/1000
		N = round(float(body.Longitude_of_ascendingnode) * 1000)/1000
		w = round(float(body.Argument_of_perihelion) * 1000)/1000
		e = round(float(body.e) * 1000)/1000
		q = round(float(body.Perihelion/AU) * 1000)/1000

		self.DetailsOn = True
		"""
		self.Info1.SetLabel("{:<12}{:>7.3f}\n{:<12}{:>7.3f}\n{:<12}{:>7.3f}\n{:<12}{:>7.3f}\n{:<12}{:>7.3f}\n{:<12}{:>7}".
		format(	"i(deg) ", i,
				"N(deg) ", N,
				"w(deg) ", w,
				"e ", e,
				"q(AU) ", q,
				"Orbit Class ", body.OrbitClass));
		"""
		self.Info1.SetLabel("{:<12}{:>7.3f}\n{:<12}{:>7.3f}\n{:<12}{:>7.3f}\n{:<12}{:>7.3f}\n{:<12}{:>7.3f}\n{:<12}{:>7.3f}".
		format(	"i(deg) ", i,
				"N(deg) ", N,
				"w(deg) ", w,
				"e ", e,
				"q(AU) ", q,
				"Abs. Mag. ", H));
		"""
		self.Info2.SetLabel("{:<12}{:>10}\n{:<12}{:>10.4f}\n{:<12}{:>10.4f}\n{:<12}{:>10.4f}\n{:<12}{:>10.4f}\n".
		format(	"Mass(kg) ", mass,
				"Radius(km) ", radius,
				"Period(yr) ", rev,
				"Moid(AU) ", moid,
				"Abs. Mag. ", H));
		"""
		self.Info2.SetLabel("{:<12}{:>10}\n{:<12}{:>10.4f}\n{:<12}{:>10.4f}\n{:<12}{:>10.4f}\n".
		format(	"Mass(kg) ", mass,
				"Radius(km) ", radius,
				"Period(yr) ", rev,
				"Moid(AU) ", moid));

		self.refreshDate()

		#for i in range(len(body.BodyShape)):

#		body.BodyShape.visible = True
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
		if self.SolarSystem.currentPOVselection == 'curobj':
			#print "currPOVselection = curobj - Reset to SUN"
			self.parentFrame.povBox.resetPOV()

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
		self.SolarSystem.DaysIncrement += self.TimeIncrement
		#self.SolarSystem.utcDaysIncrement += self.TimeIncrement
		self.SolarSystem.TimeInCurrentDay = self.SolarSystem.DaysIncrement % 86400
		#self.SolarSystem.utcTimeInCurrentDay = self.SolarSystem.utcDaysIncrement % 86400
		self.updateSolarSystem()
		sleep(1e-4)

	def SetAnimationCallback(self, callbackFunc):
		self.DisableAnimationCallback = True
		self.AnimationCallback = callbackFunc
		self.DisableAnimationCallback = False

	def OnAnimateTest(self, e):
		sleep(2)
		while True:
			sleep(1e-2)
			if self.DisableAnimationCallback == False:
				self.AnimationCallback()
	
	#def setTimeLabel(self):



	def setDeltaT(self):

#		ztime = self.localTimeLabel.GetLabel().split(" : ")
		ztime = self.localTimeLabel.GetLabel().split(":")
		if len(ztime) > 0:
			#print "before correction", self.DaysIncrement
			self.SolarSystem.TimeInCurrentDay = (float(ztime[0]) * TI_ONE_HOUR) + (float(ztime[1]) * TI_ONE_MINUTE) + (float(ztime[2]) * TI_ONE_SECOND)
			print "SETDELTA_T", self.SolarSystem.TimeInCurrentDay
		
		self.SolarSystem.DaysIncrement = self.SolarSystem.TimeInCurrentDay
		#print self.SolarSystem.TimeInCurrentDay

	def setDeltaT_XXX(self):

		ztime = self.localTimeLabel.GetLabel().split(" : ")
		if len(ztime) > 0:
			#print "before correction", self.DaysIncrement
			self.SolarSystem.DaysIncrement = (float(ztime[0]) * TI_ONE_HOUR) + (float(ztime[1]) * TI_ONE_MINUTE) + (float(ztime[2]) * TI_ONE_SECOND)
			print "##############", self.SolarSystem.DaysIncrement
		
		print self.SolarSystem.DaysIncrement

	def OnAnimate(self, e):
		self.StepByStep = False
		if self.AnimationInProgress == True:
			self.AnimationInProgress = False
			self.Animate.SetLabel(">")
			if self.RecorderOn == True and self.VideoRecorder != None:
				stopRecording(self.VideoRecorder)

			return

		self.VideoRecorder = None

		self.Animate.SetLabel("||")
		self.disableBeltsForAnimation()
		self.AnimationInProgress = True

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
		self.setDeltaT()

		sec = time.gmtime(time.time()).tm_sec
		framerate = 0
		while self.AnimationInProgress:
#			sleep(1e-2)
			#sleep(1e-3)

			self.OneTimeIncrement()
			if self.RecorderOn == True:
				if self.VideoRecorder == None:
					self.VideoRecorder = setVideoRecording(25, "output.avi")
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

		#self.Recorder.SetColor() ####


#class WIDGETSpanel(wx.Panel, AbstractUI):
class WIDGETSpanel(AbstractUI):

	def InitVariables(self):	
		self.ca_deltaT = 0
		self.Earth = self.SolarSystem.EarthRef
		self.checkboxList = {}

		self.drawEquator()
		#self.drawTimeZone()

	def InitUI(self):

		self.BoldFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
		self.RegFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)

		heading = wx.StaticText(self, label='Earth Widgets', pos=(20, MAIN_HEADING_Y))
		heading.SetFont(self.BoldFont)

		#dateLabel = wx.StaticText(self, label='Orbital Date', pos=(200, DATE_Y))
		#dateLabel.SetFont(self.BoldFont)

		#self.localTimeLabel = wx.StaticText(self, label='hh:mm:ss', pos=(320, DATE_Y-2))
		#lt = orbit3D.locationInfo.getLocalTime()
		#self.localTimeLabel.SetLabel("{:>2} : {:>2} : {:2}".format(str(lt.tm_hour).zfill(2), str(lt.tm_min).zfill(2), str(lt.tm_sec).zfill(2)))

		#self.dateMSpin = wx.SpinCtrl(self, id=wx.ID_ANY, initial=self.todayDate.month, min=1, max=12, pos=(200, DATE_SLD_Y), size=(65, 25), style=wx.SP_ARROW_KEYS)
		#self.dateMSpin.Bind(wx.EVT_SPINCTRL,self.OnTimeSpin)
		#self.dateDSpin = wx.SpinCtrl(self, id=wx.ID_ANY, initial=self.todayDate.day, min=1, max=31, pos=(265, DATE_SLD_Y), size=(65, 25), style=wx.SP_ARROW_KEYS)
		#self.dateDSpin.Bind(wx.EVT_SPINCTRL,self.OnTimeSpin)

		# Create a custom event in order to update the content of the day spinner if its value is out-of-range
		#self.CustomEvent, EVT_RESET_SPINNER = wx.lib.newevent.NewEvent()
		#self.dateDSpin.Bind(EVT_RESET_SPINNER, self.ResetSpinner) # bind it as usual
		# The day spinner has 2 events. one triggered when clicking on an arrow, and one
		# triggered programmatically to update the value of the day spinner in order to correct it
		# The firing of the EVT_RESET_SPINNER is programmatically done during the execution
		# of the EVT_SPINCTRL handler


		#self.dateYSpin = wx.SpinCtrl(self, id=wx.ID_ANY, initial=self.todayDate.year, min=-3000, max=3000, pos=(330, DATE_SLD_Y), size=(65, 25), style=wx.SP_ARROW_KEYS)
		#self.dateYSpin.Bind(wx.EVT_SPINCTRL,self.OnTimeSpin)

		#self.ValidateDate = wx.Button(self, label='Set', pos=(400, DATE_SLD_Y), size=(60, 25))
		#self.ValidateDate.Bind(wx.EVT_BUTTON, self.OnValidateDate)


		self.createCheckBox(self, "Equator", INNERPLANET, 20, CHK_L1)
		self.createCheckBox(self, "Time Zones", OUTERPLANET, 20, CHK_L2)
		self.createCheckBox(self, "Referential", REFERENTIAL, 20, CHK_L3)

		#self.createBodyList(200, LSTB_Y)

		cbtn = wx.Button(self, label='Refresh', pos=(20, CHK_L14))
		cbtn.Bind(wx.EVT_BUTTON, self.OnRefresh)

	def OnRefresh(self, e):
		pass

	def OnRadioBox(self, e):
		index = self.rbox.GetSelection()

		self.SolarSystem.currentPOVselection = {0: "curobj", 1: "sun", 2:"earth", 3:"mercury", 4:"venus",
												5: "mars", 6:"jupiter", 7:"saturn", 8:"uranus", 9:"neptune",
												10:"pluto", 11:"sedna", 12:"makemake", 13:"haumea", 14:"eris", 15:"charon", 16: "phobos", 17:"deimos", 18:"moon"}[index]
		{0:	self.setCurrentBodyFocus, 1: self.setSunFocus,
		 2: self.setPlanetFocus, 3: self.setPlanetFocus,
		 4: self.setPlanetFocus, 5: self.setPlanetFocus,
		 6: self.setPlanetFocus, 7: self.setPlanetFocus,
		 8: self.setPlanetFocus, 9: self.setPlanetFocus,
		 10: self.setPlanetFocus, 11: self.setPlanetFocus,
		 12: self.setPlanetFocus, 13: self.setPlanetFocus,
		 14: self.setPlanetFocus, 15: self.setPlanetFocus,
		 16: self.setPlanetFocus, 17: self.setPlanetFocus,
		 18: self.setPlanetFocus }[index]()

		self.setLocalRef()

	def drawEquator(self):
		print "draw equator..."
		#self.eq = cylinder(frame=self.Earth.Origin, pos=(0,0,0), color=color.blue, radius=self.Earth.BodyShape.radius*1.003, length=self.Earth.BodyShape.radius*0.003)
		self.eq = cylinder(frame=self.Earth.Origin, pos=(0,0,0), color=color.cyan, radius=self.Earth.BodyShape.radius*1.004, length=self.Earth.BodyShape.radius*0.003)
		self.eq.rotate(angle=(pi/2), axis=self.Earth.YdirectionUnit, origine=(0,0,0))

	def drawTimeZone(self):
		for i in np.arange(0, pi, deg2rad(15)):
			TZ = cylinder(frame=self.Earth.Origin, pos=(0,0,0), color=color.blue, radius=self.Earth.BodyShape.radius*1.003, length=self.Earth.BodyShape.radius*0.003)
			TZ.rotate(angle=(i), axis=self.Earth.ZdirectionUnit, origine=(0,0,0))
#
#	This is the GUI entry point
#
class controlWindow(wx.Frame):

	def __init__(self, solarsystem):
		newHeight = INFO1_Y+300 # +220
		wx.Frame.__init__(self, None, wx.ID_ANY, title="Orbits Control", size=(500, newHeight))

		# create parent panel
		self.Panel = wx.Panel(self, size=(500, newHeight))

		# create notebook to handle tabs
		self.Notebook = wx.Notebook(self.Panel, size=(500, newHeight))

		# create subpanels to be used with tabs
		self.orbitalBox = orbitalCtrlPanel(self, self.Notebook, solarsystem)
		self.jplBox = JPLpanel(self, self.Notebook, solarsystem)
		self.povBox = POVpanel(self, self.Notebook, solarsystem)
		self.widgetBox = WIDGETSpanel(self, self.Notebook, solarsystem)

		# Bind subpanels to tabs and name them.
		self.Notebook.AddPage(self.orbitalBox, "Main")
		self.Notebook.AddPage(self.povBox, "Animation POV")
		self.Notebook.AddPage(self.jplBox, "Close Approach Data")
		self.Notebook.AddPage(self.widgetBox, "Animation Widgets")
		#self.getLocationFromIPaddress()

		# if we want flyOver animation
		#self.orbitalBox.SetAnimationCallback(orbit3D.flyover_approach)

		self.orbitalBox.Show()

	"""
	def getLocationFromIPaddress(self):
		url = 'http://ipinfo.io/json'
		print url+"\n"
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36')]
			response = opener.open(url)
			print response
		except urllib2.HTTPError as err:
			print "Exception...\n\nError: " + str(err.code)
			raise


		#response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})

		rawResp = response.read()
		data = json.loads(rawResp)

		self.IP			 = data['ip']
		self.org		 = data['org']
		self.city 		 = data['city']
		self.country	 = data['country']
		self.region		 = data['region']
		self.coordinates = data['loc']
		self.timezone	 = data['timezone']
		print 'Your IP detail\n '
		print 'IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0}'.format(org,region,country,city,IP)
	"""
