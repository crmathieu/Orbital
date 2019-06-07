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
from orbital import *
from numberfmt import *
import urllib2
import httplib

import json
import wx
import wx.lib.newevent # necessary for custom event

MAIN_HEADING_Y = 40
DATE_Y = MAIN_HEADING_Y
DATE_SLD_Y = DATE_Y + 20
JPL_BRW_Y = DATE_SLD_Y
INNER_Y = MAIN_HEADING_Y + 20
ORB_Y = INNER_Y + 20
GASG_Y = ORB_Y + 20
DWARF_Y = GASG_Y + 20
#TNO_Y = DWARF_Y + 20
AB_Y = DWARF_Y + 20
JT_Y = AB_Y + 20
KB_Y = JT_Y + 20
IOC_Y = KB_Y + 20
ECL_Y = IOC_Y + 20
LABEL_Y = ECL_Y + 20
LIT_Y = LABEL_Y + 20
SIZE_Y = LIT_Y + 20
AXIS_Y = SIZE_Y + 20

REF_Y = AXIS_Y + 20
LSTB_Y = DATE_Y + 60
SLDS_Y = LSTB_Y + 40

STRT_Y = SLDS_Y
PAU_Y = STRT_Y + 40
JPL_Y = PAU_Y + 40
DET_Y = REF_Y + 70
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

PANEL_MAIN = 0
PANEL_POV = 1
PANEL_CAPP = 2

POV_Y = 15
POV_FOCUS_Y = POV_Y+150

class POVpanel(wx.Panel):
	def __init__(self, parent, notebook, solarsystem):
		wx.Panel.__init__(self, parent=notebook)
		self.parentFrame = parent
		self.nb = notebook
		self.SolarSystem = solarsystem
		self.ca_deltaT = 0
		self.InitUI()
		self.resetPOV()
		self.Hide()

	def InitUI(self):
		self.BoldFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
		self.RegFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)

		#self.Header = wx.StaticText(self, label="", pos=(20, POV_Y), size=(TOTAL_X-40, 140))
		self.Header = wx.StaticText(self, label="", pos=(220, POV_Y), size=(TOTAL_X-210, 200))
		self.Header.SetFont(self.RegFont)
		self.Header.Wrap(self.GetSize().width)
		self.Header.SetLabel("Select which body the animation should focus on. 'Current\nObject' will follow the last object selected, whether it comes\nfrom the Drop down selection, a paused slideshow selection\nor a Close Approach object pick.\n\nYou may also choose any particular planet or the sun." )
		size2 = "Select which body the animation\nshould focus on. 'Current Object'\nwill follow the last object selected,\nwhether it comes from the Drop\ndown selection, a paused slide-\nshow selection or a Close App-\nroach object pick.\n\nYou may also choose any parti-\ncular planet or the sun."
		self.Header.SetLabel(size2)
		lblList = ['Current Object', 'Sun', 'Earth', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Sedna', 'Makemake', 'Haumea','Eris']
		self.rbox = wx.RadioBox(self, label = ' Focus on ', pos = (20, POV_Y), size=(170, 500), choices = lblList ,majorDimension = 1, style = wx.RA_SPECIFY_COLS)
		self.rbox.SetFont(self.RegFont)
		self.rbox.Bind(wx.EVT_RADIOBOX,self.OnRadioBox)

		self.cb = wx.CheckBox(self, label="Show Local Referential", pos=(20, POV_Y+510))
		self.cb.SetValue(False)
		self.cb.Bind(wx.EVT_CHECKBOX,self.OnLocalRef)

		self.Title = wx.StaticText(self, label="", pos=(200, POV_FOCUS_Y+60), size=(TOTAL_X-210, TOTAL_Y-160))
		self.Title.SetFont(self.BoldFont)
		self.Info = wx.StaticText(self, label="", pos=(200, POV_FOCUS_Y+80), size=(TOTAL_X-210, TOTAL_Y-160))
		self.Info.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL)) #self.RegFont)

		self.Info.Wrap(self.GetSize().width)
		self.setSunFocus()

	def OnLocalRef(self, e):
		#print "on local ref -> "+str(self.cb.GetValue())
		self.setLocalRef()

	def setLocalRef(self):
		self.SolarSystem.setFeature(LOCAL_REFERENTIAL, self.cb.GetValue())
		glbRefresh(self.SolarSystem, self.parentFrame.orbitalBox.AnimationInProgress)

	def setCurrentBodyFocus(self):
		if self.parentFrame.orbitalBox.currentBody == None:
			self.rbox.SetSelection(1)
			#self.SolarSystem.resetView()
			self.setSunFocus()

		else:
			self.SolarSystem.currentPOV = self.parentFrame.orbitalBox.currentBody
			self.parentFrame.orbitalBox.updateCameraPOV()
			self.setBodyFocus(self.SolarSystem.currentPOV)

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

		if self.SolarSystem.currentPOVselection != 'CUROBJ':
			if (Body.SolarSystem.ShowFeatures & Body.BodyType) == 0:
				# if the body is not visible, Make it so
				#print "Making "+Body.Name+" visible! bodyType = "+str(Body.BodyType)
				Body.BodyShape.visible = True
				Body.Labels[0].visible = True
				#planetBody.SolarSystem.ShowFeatures |= planetBody.BodyType
				Body.SolarSystem.setFeature(Body.BodyType, True)
				self.parentFrame.orbitalBox.checkboxList[Body.BodyType].SetValue(True)
				#glbRefresh(self.SolarSystem, self.parentFrame.orbitalBox.AnimationInProgress)

		self.SolarSystem.currentPOV = Body
		self.parentFrame.orbitalBox.updateCameraPOV()
		#print "END setBodyFocus..."

	def setPlanetFocus(self):
		#print "Focusing on "+self.SolarSystem.currentPOVselection
		planetBody = self.SolarSystem.getBodyFromName(self.SolarSystem.currentPOVselection)
		return self.setBodyFocus(planetBody)



		# display planet Info
		mass = setPrecision(str(planetBody.Mass), 3)

		radius = planetBody.BodyRadius/1000
		rev = round(float(planetBody.Revolution / 365.25) * 1000)/1000

		i = round(float(planetBody.Inclination) * 1000)/1000
		N = round(float(planetBody.Longitude_of_ascendingnode) * 1000)/1000
		w = round(float(planetBody.Argument_of_perihelion) * 1000)/1000
		e = round(float(planetBody.e) * 1000)/1000
		q = round(float(planetBody.Perihelion/AU) * 1000)/1000
		a = round(float(planetBody.Aphelion/AU) * 1000)/1000

		######
		self.Title.SetLabel(planetBody.Name)
		self.Info.SetLabel("{:<17}{:>10}\n{:<20}{:>7.1f}\n{:<15}{:>12.4f}\n{:<15}{:>12.4f}\n{:<14}{:>10.2f}\n{:<14}{:>10.2f}\n{:<14}{:>10.2f}\n{:<22}{:>5.2f}\n{:<12}{:>7.3f}\n{:<12}{:>7.3f}\n{:<20}{:>7.3f}\n{:<20}{:>7.2f}".
		format(	"Mass(kg) ", mass,
				"Radius(km) ", radius,
				"Perihelion(AU) ", q,
				"Aphelion(AU) ", a,
				"Orb.Period(days) ", planetBody.Revolution,
				"Orb.Period(yrs)  ", planetBody.Revolution/365.25,
				"Rot.Period(days) ", planetBody.Rotation,
				"Orb.Incli.(deg) ", i,
				"Lg.of Asc Node(deg) ", N,
				"Arg. of Perih.(deg) ", w,
				"Eccentricity ", e,
				"Axial Tilt(deg) ", planetBody.AxialTilt))


		if (planetBody.SolarSystem.ShowFeatures & planetBody.BodyType) == 0:
			# if the body is not visible, Make it so
			#print "Making "+planetBody.Name+" visible! bodyType = "+str(planetBody.BodyType)
			planetBody.BodyShape.visible = True
			planetBody.Labels[0].visible = True
			#planetBody.SolarSystem.ShowFeatures |= planetBody.BodyType
			planetBody.SolarSystem.setFeature(planetBody.BodyType, True)
			self.parentFrame.orbitalBox.checkboxList[planetBody.BodyType].SetValue(True)
			#glbRefresh(self.SolarSystem, self.parentFrame.orbitalBox.AnimationInProgress)

		self.SolarSystem.currentPOV = planetBody
		self.parentFrame.orbitalBox.updateCameraPOV()
		#print "END setPlanetFocus..."

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
		self.SolarSystem.currentPOVselection = {0: "CUROBJ", 1: "SUN", 2:"EARTH", 3:"MERCURY", 4:"VENUS",
												5: "MARS", 6:"JUPITER", 7:"SATURN", 8:"URANUS", 9:"NEPTUNE",
												10:"PLUTO", 11:"SEDNA", 12:"MAKEMAKE", 13:"HAUMEA",14:"ERIS"}[index]
		{0:	self.setCurrentBodyFocus, 1: self.setSunFocus,
		 2: self.setPlanetFocus, 3: self.setPlanetFocus,
		 4: self.setPlanetFocus, 5: self.setPlanetFocus,
		 6: self.setPlanetFocus, 7: self.setPlanetFocus,
		 8: self.setPlanetFocus, 9: self.setPlanetFocus,
		 10: self.setPlanetFocus, 11: self.setPlanetFocus,
		 12: self.setPlanetFocus, 13: self.setPlanetFocus,
		 14: self.setPlanetFocus }[index]()

		self.setLocalRef()

	def getCurrentPOVselection(self):
		return self.SolarSystem.currentPOVselection

	def OnReset(self, e):
		self.resetPOV()

class JPLpanel(wx.Panel):

	def __init__(self, parent, notebook, solarsystem):
		wx.Panel.__init__(self, parent=notebook)
		self.parentFrame = parent
		self.nb = notebook
		self.SolarSystem = solarsystem
		self.ca_deltaT = 0
		self.InitUI()
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
		self.fetchJPL(host, url)
		self.heading.SetLabel('Close Approach for '+self.fetchDateStr)


	def OnCloseApproach(self, event):
		self.download.SetLabel("Fetching ...")
		self.fetchDate = datetime.date.today()
		self.fetchDateStr = self.fetchDate.strftime('%Y-%m-%d')
		self.fetchJPL(NASA_API_V1_FEED_TODAY_HOST, NASA_API_V1_FEED_TODAY_URL)
		self.download.Hide()
		self.next.Show()
		self.prev.Show()
		self.legend.SetLabel("To display orbit details, double click on desired row")

	def fetchJPL(self, host, url):
		url = url+"&start_date="+self.fetchDateStr
		print host+url+"\n"
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36')]
			response = opener.open(host+url)

			#c = httplib.HTTPSConnection(host)
			#print url
			#c.request("GET", url)
			#response = c.getresponse()
			print response
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

 		print "*****PREV"+self.prevUrl
 		print "*****CURR"+self.selfUrl
 		print "*****NEXT"+self.nextUrl

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

	def fetchJPLSAVE(self, host, url):
		url = url+"&start_date="+self.fetchDateStr
		print host+url+"\n"
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36')]
			response = opener.open(host+url)

			#c = httplib.HTTPSConnection(host)
			#print url
			#c.request("GET", url)
			#response = c.getresponse()
			print response
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

		self.ListIndex = 0
		if self.jsonResp["element_count"] > 0:
			for i in range(0, self.jsonResp["element_count"]-1):
				entry = self.jsonResp["near_earth_objects"][self.fetchDateStr][i]
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

	def fetchDetails(self, link):
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
			print response
			rawResp = response.read()
			#print rawResp
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
		self.parentFrame.orbitalBox.resetDate(self.ca_deltaT)
		self.parentFrame.orbitalBox.setCurrentBodyFromId(id)
		if self.SolarSystem.currentPOVselection == "CUROBJ":
			self.SolarSystem.currentPOV = self.parentFrame.orbitalBox.currentBody
			self.parentFrame.orbitalBox.updateCameraPOV()
		toggle = False
		if self.SolarSystem.isRealsize():
			toggle = True
		self.parentFrame.orbitalBox.currentBody.toggleSize(toggle)

	def loadBodyInfo(self, index):
		entry = self.jsonResp["near_earth_objects"][self.fetchDateStr][index]
		#print entry

		# if the key already exists, the object has already been loaded, simply return its spk-id
		#if entry["neo_reference_id"] in objects_data:
		#	return entry["neo_reference_id"]

		# grab details link
		#entry = self.fetchDetails(entry["links"]["self"])

		# otherwise add data to dictionary
		objects_data[entry["neo_reference_id"]] = {
			"material": 0,
			"name": entry["name"],
			"iau_name": entry["name"],
			"jpl_designation": entry["neo_reference_id"],
			"mass": 0.0,
			"radius": float(entry["estimated_diameter"]["kilometers"]["estimated_diameter_max"])/2, # if float(entry["estimated_diameter"]["kilometers"]["estimated_diameter_max"])/2 > DEFAULT_RADIUS else DEFAULT_RADIUS,
			"perihelion": float(entry["orbital_data"]["perihelion_distance"]) * AU,
			"e": float(entry["orbital_data"]["eccentricity"]),
			"revolution": float(entry["orbital_data"]["orbital_period"]),
			"orbital_inclination": float(entry["orbital_data"]["inclination"]),
			"longitude_of_ascendingnode":float(entry["orbital_data"]["ascending_node_longitude"]),
			"argument_of_perihelion": float(entry["orbital_data"]["perihelion_argument"]),
			"longitude_of_perihelion": float(entry["orbital_data"]["ascending_node_longitude"])+float(entry["orbital_data"]["perihelion_argument"]),
			"Time_of_perihelion_passage_JD": float(entry["orbital_data"]["perihelion_time"]),
			"mean_motion": float(entry["orbital_data"]["mean_motion"]),
			"mean_anomaly": float(entry["orbital_data"]["mean_anomaly"]),
			"epochJD": float(entry["orbital_data"]["epoch_osculation"]),
			"earth_moid": float(entry["orbital_data"]["minimum_orbit_intersection"]) * AU,
			"orbit_class": "N/A",
			"absolute_mag": float(entry["absolute_magnitude_h"]),
			"axial_tilt": 0.0
		}
		# CLose approach objects are considered as PHAs
		body = pha(self.SolarSystem, entry["neo_reference_id"], getColor())
		self.SolarSystem.addTo(body)
		return entry["neo_reference_id"]

#
# Orbital Control Panel
#

class orbitalCtrlPanel(wx.Panel):

	def __init__(self, parent, notebook, solarsystem):
		wx.Panel.__init__(self, parent=notebook)
		self.parentFrame = parent
		self.Earth = solarsystem.getBodyFromName("EARTH")
		self.nb = notebook
		self.checkboxList = {}
		self.ResumeSlideShowLabel = False
		self.AnimationInProgress = False
		self.Source = PHA
		self.TimeIncrement = INITIAL_TIMEINCR
		self.AnimLoop = 0
		self.SolarSystem = solarsystem
		self.todayDate = datetime.date.today()

		self.DeltaT = 0 # number of days from today - used for animation into future or past (detalT < 0)
		self.velocity = 0
		self.distance = 0
		self.list = []
		self.listjplid = []
		self.DetailsOn = False
		self.currentBody = None

		self.InitUI()
		self.Hide()

	def resetDate(self, deltaT):
		self.DeltaT = deltaT
		self.updateSolarSystem()

	def createBodyList(self, xpos, ypos):
		for body in self.SolarSystem.bodies:
			if body.BodyType in [PHA, BIG_ASTEROID, COMET, TRANS_NEPT]:
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
			if self.SolarSystem.currentPOVselection == "CUROBJ":
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

	def createCheckBox(self, panel, title, type, xpos, ypos):
		cb = wx.CheckBox(panel, label=title, pos=(xpos, ypos))
		if self.SolarSystem.ShowFeatures & type != 0:
			cb.SetValue(True)
		else:
			cb.SetValue(False)
		self.checkboxList[type] = cb

	def InitUI(self):
		self.BoldFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
		self.RegFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)

		heading = wx.StaticText(self, label='Show', pos=(20, MAIN_HEADING_Y))
		heading.SetFont(self.BoldFont)

		dateLabel = wx.StaticText(self, label='Orbital Date', pos=(200, DATE_Y))
		dateLabel.SetFont(self.BoldFont)

		self.dateMSpin = wx.SpinCtrl(self, id=wx.ID_ANY, initial=self.todayDate.month, min=1, max=12, pos=(200, DATE_SLD_Y), size=(65, 25), style=wx.SP_ARROW_KEYS)
		self.dateMSpin.Bind(wx.EVT_SPINCTRL,self.OnTimeSpin)
		self.dateDSpin = wx.SpinCtrl(self, id=wx.ID_ANY, initial=self.todayDate.day, min=1, max=31, pos=(265, DATE_SLD_Y), size=(65, 25), style=wx.SP_ARROW_KEYS)
		self.dateDSpin.Bind(wx.EVT_SPINCTRL,self.OnTimeSpin)

		# Create a custom event in order to update the content of the day spinner if its value is out-of-range
		self.CustomEvent, EVT_RESET_SPINNER = wx.lib.newevent.NewEvent()
		self.dateDSpin.Bind(EVT_RESET_SPINNER, self.ResetSpinner) # bind it as usual
		# The day spinner has 2 events. one triggered when clicking on an arrow, and one
		# triggered programmatically to update the value of the day spinner in order to correct it
		# The firing of the EVT_RESET_SPINNER is programmatically done during the execution
		# of the EVT_SPINCTRL handler


		self.dateYSpin = wx.SpinCtrl(self, id=wx.ID_ANY, initial=self.todayDate.year, min=-3000, max=3000, pos=(330, DATE_SLD_Y), size=(65, 25), style=wx.SP_ARROW_KEYS)
		self.dateYSpin.Bind(wx.EVT_SPINCTRL,self.OnTimeSpin)

		self.ValidateDate = wx.Button(self, label='Set', pos=(400, DATE_SLD_Y), size=(60, 25))
		self.ValidateDate.Bind(wx.EVT_BUTTON, self.OnValidateDate)


		self.createCheckBox(self, "Inner Planets", INNERPLANET, 20, INNER_Y)
		self.createCheckBox(self, "Orbits", ORBITS, 20, ORB_Y)
		self.createCheckBox(self, "Outer Planets", OUTERPLANET, 20, GASG_Y)
		self.createCheckBox(self, "Dwarf Planets", DWARFPLANET, 20, DWARF_Y)
		self.createCheckBox(self, "Asteroids Belt", ASTEROID_BELT, 20, AB_Y)
		self.createCheckBox(self, "Jupiter Trojans", JTROJANS, 20, JT_Y)
		self.createCheckBox(self, "Kuiper Belt", KUIPER_BELT, 20, KB_Y)
		self.createCheckBox(self, "Inner Oort Cloud", INNER_OORT_CLOUD, 20, IOC_Y)
		self.createCheckBox(self, "Ecliptic", ECLIPTIC_PLANE, 20, ECL_Y)
		self.createCheckBox(self, "Labels", LABELS, 20, LABEL_Y)
		self.createCheckBox(self, "Lit Scene", LIT_SCENE, 20, LIT_Y)
		self.createCheckBox(self, "Adjust objects size", REALSIZE, 20, SIZE_Y)
		self.createCheckBox(self, "Referential", REFERENTIAL, 20, AXIS_Y)

		self.createBodyList(200, LSTB_Y)

		cbtn = wx.Button(self, label='Refresh', pos=(20, REF_Y))
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

		self.sliderTitle = wx.StaticText(self, label="Ani.Frame = ", pos=(200, ANI_Y), size=(60, 20))
		self.sliderTitle.SetFont(self.BoldFont)

		self.aniSpeed = wx.StaticText(self, label="10 mi", pos=(305, ANI_Y), size=(15, 20))
		self.aniSpeed.SetFont(self.BoldFont)

		self.aniSlider = wx.Slider(self, id=wx.ID_ANY, value=1, minValue=-24, maxValue=24, pos=(195, ANI_Y+30), size=(150, 20), style=wx.SL_HORIZONTAL)
		self.aniSlider.Bind(wx.EVT_SLIDER,self.OnAnimSlider)

		self.Animate = wx.Button(self, label='>', pos=(370, ANI_Y), size=(40, 40))
		self.Animate.Bind(wx.EVT_BUTTON, self.OnAnimate)

		self.Stepper = wx.Button(self, label='+', pos=(415, ANI_Y), size=(40, 40))
		self.Stepper.Bind(wx.EVT_BUTTON, self.OnStepper)

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

	def setCameraPOV(self, body):
		self.SolarSystem.currentPOV = body

	def updateCameraPOV(self):

		# the following values will do the following
		# (0,-1,-1): freezes rotation and looks down towards the left
		# (0,-1, 1): freezes rotation and looks up towards the left
		# (0, 1, 1): freezes rotation and looks up towards the right
		# (0, 1,-1): freezes rotation and looks down towards the right

		#self.SolarSystem.Scene.forward = (0, 0, -1)
		self.SolarSystem.Scene.center = (self.SolarSystem.currentPOV.Position[X_COOR],
										 self.SolarSystem.currentPOV.Position[Y_COOR],
										 self.SolarSystem.currentPOV.Position[Z_COOR])

	def updateSolarSystem(self):
		self.refreshDate()
		self.SolarSystem.animate(self.DeltaT)
		for body in self.SolarSystem.bodies:
			if body.BodyType in [OUTERPLANET, INNERPLANET, SATELLITE, ASTEROID, COMET, DWARFPLANET, PHA, BIG_ASTEROID, TRANS_NEPT]:
				if body.BodyShape.visible == True:
					velocity, distance = body.animate(self.DeltaT)
					if self.SolarSystem.currentPOV != None:
						if body.JPL_designation == self.SolarSystem.currentPOV.JPL_designation:
							self.updateCameraPOV()

					if body.BodyType == self.Source or body.Details == True:
						self.velocity = velocity
						self.distance = distance

	def OnValidateDate(self, e):
		newdate = datetime.date(self.dateYSpin.GetValue(),self.dateMSpin.GetValue(),self.dateDSpin.GetValue())
		self.DeltaT = (newdate - self.todayDate).days
		self.OneTimeIncrement()
		self.disableBeltsForAnimation()
		self.DeltaT -= self.TimeIncrement

		self.refreshDate()

	def setVelocityLabel(self):
		if self.DetailsOn == True:
			self.ObjVelocity.SetLabel("{:<12}{:>10.4f}".format("Vel.(km/s)", round(self.velocity/1000, 2)))

	def setDistanceLabel(self):
		if self.DetailsOn == True:
			#print "distance="+str(self.distance)
			self.ObjDistance.SetLabel("{:<12}{:>10.4f}".format("DTE (AU)", float(self.distance)))

	def refreshDate(self):
		newdate = self.todayDate + datetime.timedelta(days = self.DeltaT)
		self.dateDSpin.SetValue(newdate.day)
		self.dateMSpin.SetValue(newdate.month)
		self.dateYSpin.SetValue(newdate.year)

		self.setVelocityLabel()
		self.setDistanceLabel()

	def disableBeltsForAnimation(self):
		self.checkboxList[JTROJANS].SetValue(False)
		self.checkboxList[ASTEROID_BELT].SetValue(False)
		self.checkboxList[KUIPER_BELT].SetValue(False)
		self.checkboxList[INNER_OORT_CLOUD].SetValue(False)
		self.SolarSystem.setFeature(JTROJANS|ASTEROID_BELT|KUIPER_BELT|INNER_OORT_CLOUD, False)
		#self.SolarSystem.ShowFeatures = (self.SolarSystem.ShowFeatures & ~(JTROJANS|ASTEROID_BELT|KUIPER_BELT|INNER_OORT_CLOUD))
		glbRefresh(self.SolarSystem, self.AnimationInProgress)

	def updateJTrojans(self):
		curTrojans = self.SolarSystem.getJTrojans()
		JupiterBody = self.SolarSystem.getBodyFromName(objects_data[curTrojans.PlanetName]['jpl_designation'])
		# if Jupiter coordinates haven't changed since this Trojans were generated, don't do anything
		if JupiterBody.Position[X_COOR] == curTrojans.JupiterX and JupiterBody.Position[Y_COOR] == curTrojans.JupiterY:
		   return

		# otherwise, generate a new set of Trojans corresponding to Jupiter's new location
		self.SolarSystem.addJTrojans(makeJtrojan(self.SolarSystem, 'jupiterTrojan', 'Jupiter Trojans', JTROJANS, color.green, 2, 5, 'jupiter'))

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

	def OnAnimSlider(self, e):
		self.TimeIncrement = float(self.aniSlider.GetValue()) * INITIAL_TIMEINCR
		# copy time increment to solarsystem class for realtime update
		self.SolarSystem.setTimeIncrement(self.TimeIncrement)
		#self.aniSpeed.SetLabel(setPrecision(str(self.TimeIncrement), 2)+" d")
		self.aniSpeed.SetLabel(str(self.aniSlider.GetValue()*10)+" mi")
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
			self.SolarSystem.setFeature(type, cbox.GetValue())
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

		glbRefresh(self.SolarSystem, self.AnimationInProgress)

	def OnPauseSlideShow(self, e):
		self.AnimationInProgress = False

		if self.ResumeSlideShowLabel == True:
			self.resetBodyList()
			e.GetEventObject().SetLabel("Pause")
			self.ResumeSlideShowLabel = False
		else:
			e.GetEventObject().SetLabel("Resume")
			self.ResumeSlideShowLabel = True
			if self.SolarSystem.currentPOVselection == "CUROBJ":
				self.SolarSystem.currentPOV = self.currentBody
				self.updateCameraPOV()

	def showObjectDetails(self, body):
		self.InfoTitle.SetLabel(body.Name)
		self.velocity, self.distance = body.animate(self.DeltaT)
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

		body.BodyShape.visible = True
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
		if self.SolarSystem.currentPOVselection == 'CUROBJ':
			#print "currPOVselection = CUROBJ - Reset to SUN"
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
				glbRefresh(self.SolarSystem, self.AnimationInProgress)
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
		body.BodyShape.visible = False
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
		self.StepByStep = True
		self.disableBeltsForAnimation()
		self.AnimationInProgress = False # stop potential animation in progress
		self.OneTimeIncrement()

	def OneTimeIncrement(self):
		self.DeltaT += self.TimeIncrement
		self.updateSolarSystem()
		sleep(1e-4)

	def OnAnimate(self, e):
		self.StepByStep = False
		if self.AnimationInProgress == True:
			self.AnimationInProgress = False
			self.Animate.SetLabel(">")
			return

		self.Animate.SetLabel("||")
		self.disableBeltsForAnimation()
		self.AnimationInProgress = True
		while self.AnimationInProgress:
			self.OneTimeIncrement()
		self.Animate.SetLabel(">")

#
#	This is the GUI entry point
#
class controlWindow(wx.Frame):

	def __init__(self, solarsystem):
		wx.Frame.__init__(self, None, wx.ID_ANY, title="Orbits Control", size=(500, INFO1_Y+220))

		# create parent panel
		self.Panel = wx.Panel(self, size=(500, INFO1_Y+220))

		# create notebook to handle tabs
		self.Notebook = wx.Notebook(self.Panel, size=(500, INFO1_Y+220))
		# create subpanels to be used with tabs
		self.orbitalBox = orbitalCtrlPanel(self, self.Notebook, solarsystem)
		self.jplBox = JPLpanel(self, self.Notebook, solarsystem)
		self.povBox = POVpanel(self, self.Notebook, solarsystem)

		# Bind subpanels to tabs and name them.
		self.Notebook.AddPage(self.orbitalBox, "Main")
		self.Notebook.AddPage(self.povBox, "Animation POV")
		self.Notebook.AddPage(self.jplBox, "Close Approach Data")

		self.orbitalBox.Show()
