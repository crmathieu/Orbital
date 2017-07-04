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
from visual import *
from visual.controls import *

import sys
import numpy as np

from random import *
import scipy.special as sp
import datetime

import wx

date_elements = {
				"d_to_m" :{1:0, 2:31, 3:59, 4:90, 5:120, 6:151, 7:181, 8:212, 9:243, 10:273, 11:304, 12:334},
				"d_to_m_leap" :{1:0, 2:31, 3:60, 4:91, 5:121, 6:152, 7:182, 8:213, 9:244, 10:274, 11:305, 12:335},
				"d_since_J2000":{1995:-1827.5, 1996: -1462.5, 1997: -1096.5, 1998: -731.5, 1999:-366.5, 2000:-1.5, 2001: 364.5, 2002: 729.5, 2003:1094.5, 2004:1459.5, 2005:1825.5}
}

INNERPLANET = 0x01
OUTTERPLANET = 0x02
DWARFPLANET = 0x04
ASTEROID = 0x08
COMET = 0x10
SMALL_ASTEROID = 0x20
BIG_ASTEROID = 0x40
PHA = 0x80
ASTEROID_BELT = 0x100
KUIPER_BELT = 0x200
INNER_OORT_CLOUD = 0x400
ECLIPTIC_PLANE = 0x800
LIT_SCENE = 0x1000
REFERENTIAL = 0x2000
ORBITS = 0x4000
GASGIANT = 0x8000

TYPE_MASK = 0xFFFF

SATELLITE_M = 100
THREE_D = False
MAX_P_D = 1.1423e13
MIN_P_D = 46.0e9
LEGEND = true

SUN_M = 1.989e+30
SUN_R = 696e+6
G = 6.67384e-11	# Universal gravitational constant
Mu = G * SUN_M
DIST_FACTOR = 10e-7
X_COOR = 0
Y_COOR = 1
Z_COOR = 2

TYPE_PLANET = 1
TYPE_ASTEROID = 2
TYPE_DWARF_PLANET = 3
TYPE_COMET = 4
TYPE_TRANS_N = 5

AU = 149597870691

JPL_FULLNAME = 0
JPL_DESIGNATION = 1
JPL_IAU_NAME = 2
JPL_PREFIX = 3
JPL_NEAR_EARTH_ORBIT = 4
JPL_PHA = 5
JPL_MAG_H = 6
JPL_MAG_G = 7
JPL_MAG_M1 = 8
JPL_MAG_M2 = 9
JPL_MAG_K1 = 10
JPL_MAG_K2 = 11
JPL_MAG_PC = 12
JPL_DIAMETER = 13
JPL_EXTENT = 14
JPL_ALBEDO = 15
JPL_ROT_PER = 16
JPL_GM = 17
JPL_MAG_BV = 18
JPL_MAG_UB = 19
JPL_MAG_IR = 20
JPL_SPEC_1 = 21
JPL_SPEC_2 = 22
JPL_H_SIGMA = 23
JPL_DIAMETER_SIGMA = 24
JPL_ORBIT_ID = 25
JPL_EPOCH_JD = 26
JPL_EPOCH_MJD = 27
JPL_EPOCH_ET = 28
JPL_EQUINOX = 29
JPL_OE_e = 30
JPL_OE_a = 31
JPL_OE_q = 32
JPL_OE_i = 33
JPL_OE_N = 34
JPL_OE_w = 35
JPL_OE_M = 36
JPL_OE_Q = 37
JPL_OE_n = 38
JPL_OE_tp_JD = 39
JPL_OE_tp_ET = 40
JPL_OE_Pd = 41
JPL_OE_Py = 42
JPL_EARTH_MOID_AU = 43
JPL_EARTH_MOID_LD = 44
JPL_JUPITER_MOID_AU = 45

class controlWindow(wx.Frame):

	def __init__(self, frame, solarsystem):
		wx.Frame.__init__(self, None)
		self.checkboxList = {}
		self.PauseAnimation = False
		self.Source = PHA
		self.solarsystem = solarsystem

		# Associate some events with methods of this class
		self.InitUI()

	def createCheckBox(self, panel, title, type, xpos, ypos):

		cb = wx.CheckBox(panel, label=title, pos=(xpos, ypos))
		if self.solarsystem.ShowBodies & type <> 0:
			cb.SetValue(True)
		else:
			cb.SetValue(False)
		self.checkboxList[type] = cb

	def InitUI(self):
		pnl = wx.Panel(self)

		font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		heading = wx.StaticText(pnl, label='Show', pos=(20, 20))
		heading.SetFont(font)

		INNER_Y = 40
		ORB_Y = INNER_Y + 20
		GASG_Y = ORB_Y + 20
		DWARF_Y = GASG_Y + 20
		AB_Y = DWARF_Y + 20
		KB_Y = AB_Y + 20
		IOC_Y = KB_Y + 20
		ECL_Y = IOC_Y + 20
		LIT_Y = ECL_Y + 20
		AXIS_Y = LIT_Y + 20
		REF_Y = AXIS_Y + 20

		STRT_Y = REF_Y
		PAU_Y = REF_Y + 40
		DET_Y = PAU_Y + 100

		self.createCheckBox(pnl, "Inner Planets", INNERPLANET, 20, INNER_Y)
		self.createCheckBox(pnl, "Orbits", ORBITS, 20, ORB_Y)
		self.createCheckBox(pnl, "Outter Planets", OUTTERPLANET, 20, GASG_Y)
		self.createCheckBox(pnl, "Dwarf Planets", DWARFPLANET, 20, DWARF_Y)
		self.createCheckBox(pnl, "Asteroids Belt", ASTEROID_BELT, 20, AB_Y)
		self.createCheckBox(pnl, "Kuiper Belt", KUIPER_BELT, 20, KB_Y)
		self.createCheckBox(pnl, "Inner Oort Cloud", INNER_OORT_CLOUD, 20, IOC_Y)
		self.createCheckBox(pnl, "Ecliptic", ECLIPTIC_PLANE, 20, ECL_Y)
		self.createCheckBox(pnl, "Lit Scene", LIT_SCENE, 20, LIT_Y)
		self.createCheckBox(pnl, "Referential", REFERENTIAL, 20, AXIS_Y)

		cbtn = wx.Button(pnl, label='Refresh', pos=(20, REF_Y))
		cbtn.Bind(wx.EVT_BUTTON, self.OnRefresh)

		lblList = ['PHA', 'Comets', 'Big Asteroids']
		self.rbox = wx.RadioBox(pnl,label = 'Animate', pos = (200, REF_Y), choices = lblList ,majorDimension = 1, style = wx.RA_SPECIFY_COLS)
		self.rbox.Bind(wx.EVT_RADIOBOX,self.OnRadioBox)

		self.Animate = wx.Button(pnl, label='Start', pos=(340, REF_Y))
		self.Animate.Bind(wx.EVT_BUTTON, self.OnAnimate)

		self.Pause = wx.Button(pnl, label='Pause', pos=(340, PAU_Y))
		self.Pause.Bind(wx.EVT_BUTTON, self.OnPauseAnimate)
		self.Pause.Hide()

		INFO1_Y = DET_Y + 20

		self.InfoTitle = wx.StaticText(pnl, label="", pos=(20, DET_Y))
		self.InfoTitle.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
		self.Info1 = wx.StaticText(pnl, label="", pos=(20, INFO1_Y))
		self.Info1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)) #, wx.BOLD))
		self.Info1.Wrap(230)
		self.Info2 = wx.StaticText(pnl, label="", pos=(240, INFO1_Y))
		self.Info2.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)) #, wx.BOLD))
		self.Info2.Wrap(250)

		self.SetSize((500, INFO1_Y+180))
		self.SetTitle('Orbital Control')
		self.Centre()
		self.Show(True)

	def OnRadioBox(self, e):
		index = self.rbox.GetSelection()
		self.Source = {0: PHA, 1: COMET, 2:BIG_ASTEROID}[index]
		self.solarsystem.currentSource = self.Source

	def onCharEvent(self, event):
		keycode = event.GetKeyCode()
		controlDown = event.CmdDown()
		altDown = event.AltDown()
		shiftDown = event.ShiftDown()

		#print keycode
		if keycode == wx.WXK_SPACE:
			print "you pressed the spacebar!"
		elif controlDown and altDown:
			print keycode
		event.Skip()

	def OnKeyDown(self, e):
		print "key down"

	def OnRefresh(self, e):
		for type, cbox in self.checkboxList.iteritems():
			if cbox.GetValue() == True:
				self.solarsystem.ShowBodies |= type
			else:
				self.solarsystem.ShowBodies = (self.solarsystem.ShowBodies & ~type)
		glbRefresh(self.solarsystem)

	def OnPauseAnimate(self, e):
		if self.PauseAnimation:
			e.GetEventObject().SetLabel("Pause")
			self.PauseAnimation = False
		else:
			e.GetEventObject().SetLabel("Resume")
			self.PauseAnimation = True
		#self.PauseAnimation = True if self.PauseAnimation == False else False

	def OnAnimate(self, e):
		if self.solarsystem.AnimationInProgress:
			# click on the Stop button
			self.solarsystem.AbortAnimation = True
			self.PauseAnimation = False
			# reset label as 'Start'
			e.GetEventObject().SetLabel("Start")
			self.InfoTitle.SetLabel('')
			self.Info1.SetLabel('')
			self.Info2.SetLabel('')
			self.Pause.SetLabel("Pause")
			self.Pause.Hide()
			return
		else:
			# click on the start button
			self.solarsystem.AnimationInProgress = True
			self.Pause.Show()
			# reset label as 'Stop'
			self.Animate.SetLabel("Stop")

		# loop through each body. If the bodyType matches what the Animation
		# is about,
		for body in self.solarsystem.bodies:
			if body.BodyType == self.Source: #PHA:
				if 0 and self.checkboxList[self.Source].GetValue() == True:
					self.checkboxList[self.Source].SetValue(False)
					self.solarsystem.ShowBodies = (self.solarsystem.ShowBodies & ~self.Source)
					AnimationState = self.solarsystem.AnimationInProgress
					self.solarsystem.AnimationInProgress = False
					glbRefresh(self.solarsystem)
					self.solarsystem.AnimationInProgress = AnimationState

				glbRefresh(self.solarsystem) ##
				self.InfoTitle.SetLabel(body.Name)

				mass = str(body.Mass)+" kg" if body.Mass <> 0 else "Not Provided"
				radius = str(body.BodyRadius)+" km" if body.BodyRadius <> 0 else "Not Provided"
				moid = str(body.Moid/1000)+" km" if body.Moid <> 0 else "N/A"
				rev = str(body.Revolution / 365.25)
				#self.Info1.SetLabel("{0:3} : ".format("i", str(body.Inclinaison)+" deg\n")) #N : "+str(body.Longitude_of_ascendingnode)+"\nw : "+str(body.Argument_of_perihelion)+"\ne : "+str(body.e)+"\nq : "+str(body.Perihelion/1000)+" km")

				self.Info1.SetLabel("i  : "+str(body.Inclinaison)+" deg\nN : "+str(body.Longitude_of_ascendingnode)+" deg\nw : "+str(body.Argument_of_perihelion)+" deg\ne : "+str(body.e)+"\nq : "+str(body.Perihelion/1000)+" km")
				self.Info2.SetLabel("Mass : "+mass+"\nRadius : "+radius+"\nPeriod: "+rev+" yr"+"\n\nMoid :"+moid)


				body.BodyShape.visible = True
				body.Label.visible = True
				body.Trail.visible = True
				for i in range(0,2):
					#print "*"
					rate(1)
				while (self.PauseAnimation and self.solarsystem.AbortAnimation == False):
					rate(1)
				body.BodyShape.visible = False
				body.Label.visible = False
				body.Trail.visible = False
				if self.solarsystem.AbortAnimation:
					self.solarsystem.AbortAnimation = False
					self.solarsystem.AnimationInProgress = False
					return
		self.solarsystem.AnimationInProgress = False
		self.Pause.Hide()
		self.Animate.SetLabel("Start")
		self.InfoTitle.SetLabel('')
		self.Info1.SetLabel('')
		self.Info2.SetLabel('')

planets_data = {
				"neptune" :{"type": TYPE_PLANET,
							"material":1,
							"name": "Neptune",
							"mass":102e24,
							"radius":24622e3,
							"perihelion":4444.45e9,
							"e":0.00858587,
							"revolution":164.179 * 365,
							"orbital_inclinaison":1.769,
							"longitude_of_ascendingnode":131.72169,
							"longitude_of_perihelion":44.97135,
							"orbital_obliquity": 28.3,
							"kep_elt":{"a" : 30.06952752, "ar": 0.00006447,"e" : 0.00895439,"er": 0.00000818,"i" : 1.77005520,"ir": 0.00022400,"L" : 304.22289287,"Lr": 218.46515314,"W" : 46.68158724,"Wr": 0.01009938,"N" : 131.78635853,"Nr": -0.00606302,"b" : -0.00041348,"c" : 0.68346318,"s" : -0.10162547,"f" : 7.67025000}
							},

				"uranus" : {"type": TYPE_PLANET,
							"material":1,
							"name": "Uranus",
							"mass":86.8e24,
							"radius":25362e3,
							"perihelion":2741.30e9,
							"e":0.04716771,
							"revolution":84.011 * 365,
							"orbital_inclinaison":0.770,
							"longitude_of_ascendingnode":74.22988,
							"longitude_of_perihelion":170.96424,
							"orbital_obliquity": 97.8,
							"kep_elt":{"a" : 19.18797948, "ar": -0.00020455, "e" : 0.04685740, "er": -0.00001550, "i" : 0.77298127, "ir": -0.00180155, "L" : 314.20276625, "Lr": 428.49512595, "W" : 172.43404441, "Wr": 0.09266985, "N": 73.96250215, "Nr": 0.05739699, "b" : 0.00058331, "c" : -0.97731848, "s" : 0.17689245, "f" : 7.67025000}
							},

				"saturn" : {"type": TYPE_PLANET,
							"material":1,
							"name": "Saturn",
							"mass":568e24,
							"radius":58232e3,
							"perihelion":1352.55e9,
							"e":0.05415060,
							"revolution":29.457 * 365,
							"orbital_inclinaison":2.484,
							"longitude_of_ascendingnode":113.71504,
							"longitude_of_perihelion":92.43194,
							"orbital_obliquity": 26.7,
							"kep_elt":{"a" : 9.54149883, "ar": -0.00003065, "e" : 0.05550825, "er": -0.00032044, "i" : 2.49424102, "ir": 0.00451969, "L" : 50.07571329, "Lr": 1222.11494724, "W" : 92.86136063, "Wr": 0.54179478, "N": 113.63998702, "Nr": -0.25015002, "b" : 0.00025899, "c" : -0.13434469, "s" : 0.87320147, "f" : 38.35125}
							},

				"jupiter" :{"type": TYPE_PLANET,
							"material":1,
							"name": "Jupiter",
							"mass":1898e24,
							"radius":69911e3,
							"perihelion":740.52e9,
							"e":0.04839266,
							"revolution":11.862 * 365,
							"orbital_inclinaison":1.305,
							"longitude_of_ascendingnode":100.55615,
							"longitude_of_perihelion":14.75385,
							"orbital_obliquity": 3.1,
							"kep_elt":{"a" : 5.20248019, "ar": -0.00002864, "e" : 0.04853590, "er": 0.00018026, "i" : 1.29861416, "ir": -0.00322699, "L" : 34.33479152, "Lr": 3034.90371757, "W" : 14.27495244, "Wr": 0.18199196, "N": 100.29282654, "Nr": 0.13024619, "b" : -0.00012452, "c" : 0.06064060, "s" : -0.35635438, "f" : 38.35125}
							},
				"mars" : {	"type": TYPE_PLANET,
							"material":1,
							"name": "Mars",
							"mass":0.642e24,
							"radius":3389e3,
							"perihelion":206.62e9,
							"e":0.09341233,
							"revolution":686.98,
							"orbital_inclinaison":1.851,
							"longitude_of_ascendingnode":49.57854,
							"longitude_of_perihelion":336.04084,
							"orbital_obliquity": 25.2,
							"kep_elt":{'a' : 1.52371243, 'ar': 9.7e-07, 'e' : 0.09336511, 'er':9.149e-05, 'i' :1.85181869, 'ir':-0.00724757, 'L' :-4.56813164, 'Lr':19140.2993424, 'W' :-23.91744784, 'Wr':0.45223625, 'N' :49.71320984, 'Nr':-0.26852431, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0}
							},

				"mercury" :{"type": TYPE_PLANET,
							"material":1,
							"name": "Mercury",
							"mass":0.330e24,
							"radius":2439e3,
							"perihelion":46.0e9,
							"e":0.20563069,
							"revolution":87.969,
							"orbital_inclinaison":7.005,
							"longitude_of_ascendingnode":48.33167,
							"longitude_of_perihelion":77.45645,
							"orbital_obliquity": 0.034,
							"kep_elt":{'a' : 0.38709843, 'ar': 0.0, 'e' : 0.20563661, 'er':0.00002123, 'i' :7.00559432, 'ir':-0.00590158, 'L' :252.25166724, 'Lr':149472.674866, 'W' :77.45771895, 'Wr':0.15940013, 'N' :48.33961819, 'Nr':-0.12214182, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
							},

				"venus" : {	"type": TYPE_PLANET,
							"material":1,
							"name": "Venus",
							"mass":4.87e24,
							"radius":6052e3,
							"perihelion":107.48e9,
							"e":0.00677323,
							"revolution":224.701,
							"orbital_inclinaison":3.3947,
							"longitude_of_ascendingnode":76.68069,
							"longitude_of_perihelion":131.53298,
							"orbital_obliquity": 177.4,
							"kep_elt":{'a' : 0.72332102, 'ar': -2.6e-07, 'e' : 0.00676399, 'er':-5.107e-05, 'i' :3.39777545, 'ir':0.00043494, 'L' :181.9797085, 'Lr':58517.8156026, 'W' :131.76755713, 'Wr':0.05679648, 'N' :76.67261496, 'Nr':-0.27274174, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
							},

				"earth" : {	"type": TYPE_PLANET,
							"material":1,
							"name": "Earth",
							"mass":5.972e24,
							"radius":6371e3,
							"perihelion":147.09e9,
							"e":0.01671022,
							"revolution":365.256,
							"orbital_inclinaison":0,
							"longitude_of_ascendingnode":-11.26064,
							"longitude_of_perihelion":102.94719,
							"orbital_obliquity": 23.4,
							"kep_elt":{'a' : 1.00000018, 'ar': -3e-08, 'e' : 0.01673163, 'er':-3.661e-05, 'i' :-0.00054346, 'ir':-0.01337178, 'L' :100.46691572, 'Lr':35999.3730633, 'W' :102.93005885, 'Wr':0.3179526, 'N' :-5.11260389, 'Nr':-0.24123856, 'b' :0.0, 'c' :0.0, 's':0.0, 'f' :0.0},
							},

				"pluto" : {	"type": TYPE_PLANET,
							"material":1,
							"name": "Pluto",
							"mass":0.0146e24,
							"radius":1195e3,
							"perihelion":4436.82e+9,
							"e":0.24880766,
							"revolution":247.68 * 365,
							"orbital_inclinaison":17.142,
							"longitude_of_ascendingnode":110.30347,
							"longitude_of_perihelion":224.06676,
							"orbital_obliquity": 122.5,
							"kep_elt":{'a' : 39.48686035, 'ar': 0.00449751, 'e' : 0.24885238, 'er':6.016e-05, 'i' :17.1410426, 'ir':5.01e-06, 'L' :238.96535011, 'Lr':145.18042903, 'W' :224.09702598, 'Wr':-0.00968827, 'N' :110.30167986, 'Nr':-0.00809981, 'b' :-0.01262724, 'c' :0.0, 's':0.0, 'f' :0.0}
							},

				"eris" : {	"type": TYPE_DWARF_PLANET,
							"material":0,
							"name": "Eris",
							"mass":1.66e22,
							"radius":1163e3,
							"perihelion":5.723e12,
							"e":0.4417142619088136,
							"revolution": 203830,
							"orbital_inclinaison":44.0445,
							"longitude_of_ascendingnode": 35.87791199490014,
							"longitude_of_perihelion":186.9301,

							"Time_of_perihelion_passage_JD": 2545575.799683113451,
							"mean_motion":.001771354370292503,
							"epochJD": 2458000.5,
							"mean_anomaly": 204.8731101766414,

							"orbital_obliquity": 0
							},


				"makemake":{"type": TYPE_DWARF_PLANET,
							"material":0,
							"name": "Makemake",
							"mass":4.4e21,
							"radius":739e3,
							"perihelion":5.77298e12,
							"e":.154682767507142,
							"revolution": 112897.9710682497,
							"orbital_inclinaison":29.00685,
							"longitude_of_ascendingnode": 79.3659,
							"longitude_of_perihelion":376.6059,

							"Time_of_perihelion_passage_JD": 2407499.827534289027,
							"mean_motion":.003188719837864677,
							"epochJD": 2458000.5,
							"mean_anomaly": 161.032496116919,

							"orbital_obliquity": 0
							},

				"sedna":   {"type": TYPE_DWARF_PLANET,
							"material":0,
							"name": "Sedna",
							"mass":4.4e21, # mass is undetermined
							"radius":995e3,
							"perihelion":1.1423e13,
							"e":0.85491,
							"revolution": 3934726.687924069,
							"orbital_inclinaison":11.92872,
							"longitude_of_ascendingnode":144.546,
							"longitude_of_perihelion":455.836,

							"Time_of_perihelion_passage_JD": 2479566.507375652123,
							"mean_motion":9.149301299753888e-5,
							"epochJD": 2458000.5,
							"mean_anomaly": 358.0268610068745,

							"orbital_obliquity": 0
							},

				"haumea":  {"type": TYPE_DWARF_PLANET,
							"material":0,
							"name": "Haumea",
							"mass":4.006e21,
							"radius":620e3,
							"perihelion":35.14529440338772*AU,
							"e":0.1893662787361186,
							"revolution": 104270.6801862633,
							"orbital_inclinaison":28.20363151617822,
							"longitude_of_ascendingnode":121.9702799705751,
							"longitude_of_perihelion":360.8407349965672,

							"Time_of_perihelion_passage_JD": 2500269.703252029540,
							"mean_motion":.003452552523460249,
							"epochJD": 2458000.5,
							"mean_anomaly": 214.0633556475513,

							"orbital_obliquity": 0
							},
				"MU69" : {"type": TYPE_TRANS_N,
							"material":0,
							"name": "NHorizon (2014 MU69)",
							"mass":4.006e21,
							"radius":620e3,
							"perihelion":42.36382619492954 * AU,
							"e":0.04710496472429965,
							"revolution": 108273.8543019219,
							"orbital_inclinaison":2.451806641801155,
							"longitude_of_ascendingnode": 158.9860995817701,
							"longitude_of_perihelion":342.6477922062032,

							"Time_of_perihelion_passage_JD": 2474149.642000547787,
							"mean_motion":0.003324902418234221,
							"epochJD": 2458000.5,
							"mean_anomaly": 306.3056787099708,

							"orbital_obliquity": 0
							}
}

belt_data = {
	"jupiterTrojan": {
		"radius_min":5.05,
		"radius_max":5.35,
		"thickness": 0.6,
		"thickness_factor":5.e4},
	"asteroid":	{
		"radius_min":2.06,
		"radius_max":3.27,
		"thickness": 0,
		"thickness_factor":5.e4},
	"kuiper":   {
		"radius_min":30,
		"radius_max":50,
		"thickness": 10,
		"thickness_factor":1.e6},
	"inneroort":	{
		"radius_min":2000,
		"radius_max":20000,
		"thickness": 0,
		"thickness_factor":1.e9},
}

class solarSystem:

	INNER_RING_COEF = 1.3
	OUTTER_RING_COEF = 1.9

	bodies = []
	def __init__(self):
		self.Name = "Sun"
		self.BodyRadius = SUN_R
		self.Mass = SUN_M
		self.AbortAnimation = False
		self.AnimationInProgress = False
		self.currentSource = PHA

		self.Scene = display(title = 'Solar System', width = 1300, height = 740, center = (0,0,0))

		self.Scene.lights = []
		self.Scene.forward = (0,0,-1)
		self.Scene.fov = math.pi/3
		self.Scene.userspin = True
		self.Scene.userzoom = True
		self.Scene.autoscale = 1
		self.Scene.autocenter = False
		self.Scene.up = (0,0,1)
		self.Axis = [0,0,0]
		self.AxisLabel = ["","",""]

		# make all light coming from origin
		self.sunLight = local_light(pos=(0,0,0), color=color.white)
		self.Scene.ambient = color.black

		if THREE_D:
			self.Scene.stereo='redcyan'
			self.Scene.stereodepth = 1

		self.BodyShape = sphere(pos=vector(0,0,0), radius=self.BodyRadius/(35000), color=color.white)
		self.BodyShape.material = materials.emissive

		# make referential
		self.makeAxes(color.white, 3*AU*DIST_FACTOR, (0,0,0))

	def makeAxes(self, color, size, position):
	    directions = [vector(size,0,0), vector(0,size,0), vector(0,0,size/4)]
	    texts = ["x (vernal eq.)","y","z"]
	    pos = vector(position)
	    for i in range (3): # Each direction
	       self.Axis[i] = curve( frame = None, color = color, pos= [ pos, pos+directions[i]], visible=False)
	       self.AxisLabel[i] = label( frame = None, color = color,  text = texts[i],
		   							pos = pos+directions[i], opacity = 0, box = False, visible=False )

	def addTo(self, body):
		self.bodies.append(body)

	def drawAllBodiesTrajectory(self):
		for body in self.bodies:
			body.draw()
			rate(10000)
		self.Scene.autoscale = 1

	def getBodyFromName(self, bodyname):
		for body in self.bodies:
			if body.Name == bodyname:
				return body
		return None

	def refresh(self):
		if self.ShowBodies & ORBITS <> 0:
			orbitTrace = True
		else:
			orbitTrace = False

		for body in self.bodies:
			if body.BodyType in [OUTTERPLANET, INNERPLANET, ASTEROID, COMET, DWARFPLANET, PHA, BIG_ASTEROID]:
				if body.BodyShape.visible == True:
					body.Trail.visible = orbitTrace

		if self.ShowBodies & LIT_SCENE <> 0:
			self.Scene.ambient = color.white
			self.sunLight.visible = False
		else:
			self.Scene.ambient = color.black
			self.sunLight.visible = True

		if self.ShowBodies & REFERENTIAL <> 0:
			for i in range(3):
				self.Axis[i].visible = True
				self.AxisLabel[i].visible = True
		else:
			for i in range(3):
				self.Axis[i].visible = False
				self.AxisLabel[i].visible = False

	def setBodyPosition(self, bodyName, trueAnomaly):
		body = self.getBodyFromName(bodyName)
		if body <> None:
			theta = (math.pi * trueAnomaly)/180 # convert degrees to radians
			R = (body.a*(1 - body.e**2))/(1 + body.e*cos(trueAnomaly))
			body.X = R * cos(trueAnomaly)
			body.Y = R * sin(trueAnomaly)
			body.updatePosition(false)
			if LEGEND:
				body.Label.visible = false
				body.Label = label(pos=(body.Position[X_COOR],body.Position[Y_COOR],body.Position[Z_COOR]), text=body.Name, xoffset=20, yoffset=12, space=0, height=10, color=body.Color, border=6, box=false, font='sans')

	def makeRings(self, system, bodyName, density = 1):  # change default values during instantiation
		global planets_data
		self.solarsystem = system
		planet = self.getBodyFromName(planets_data[bodyName]['name'])
		if planet <> None:
			InnerRadius = planet.BodyRadius * self.INNER_RING_COEF / planet.SizeCorrection
			OutterRadius = planet.BodyRadius * self.OUTTER_RING_COEF / planet.SizeCorrection
			planet.Ring = true
			planet.InnerRing = curve(color=planet.Color)
			planet.OutterRing = curve(color=planet.Color)

			if (self.solarsystem.ShowBodies & planet.BodyType) == 0:
				planet.InnerRing.visible = false
				planet.OutterRing.visible = false

			Position = np.matrix([[0],[0],[0]])
			angle = planet.Angle + pi/2
			Rotation_3D = np.matrix([
				[1, 0, 					0],
				[0, cos(angle), 	-sin(angle)],
				[0, sin(angle), 	cos(angle)]]
			)

			for i in np.arange(0, 2*pi, pi/(180*density)):
				Position = [[(OutterRadius * cos(i))], [(OutterRadius * sin(i))], [0]]
				Position = Rotation_3D * Position + planet.Position
				planet.OutterRing.append(pos=(Position[X_COOR], Position[Y_COOR], Position[Z_COOR]), color=planet.Color) #radius=pointRadius/planet.SizeCorrection, size=1)

				Position = [[(InnerRadius * cos(i))], [(InnerRadius * sin(i))], [0]]
				Position = Rotation_3D * Position + planet.Position
				planet.InnerRing.append(pos=(Position[X_COOR], Position[Y_COOR], Position[Z_COOR]), color=planet.Color) #radius=pointRadius/planet.SizeCorrection, size=1)


class makeEcliptic:

	def __init__(self, system, color):  # change default values during instantiation
		# draw a circle of 250 AU
		self.Name = "Ecliptic Plane"
		self.solarsystem = system
		self.Color = color
		self.BodyType = ECLIPTIC_PLANE

	def refresh(self):
		if self.solarsystem.ShowBodies & ECLIPTIC_PLANE <> 0:
			#self.solarsystem.Scene.autoscale = 0
			self.Ecliptic.visible = True
		else:
			self.Ecliptic.visible = False
			#self.solarsystem.Scene.autoscale = 1

	def draw(self):
		self.Ecliptic = cylinder(pos=vector(0,0,0), radius=250*AU*DIST_FACTOR, color=self.Color, length=100, opacity=0.2, axis=(0,0,1))
		self.Ecliptic.visible = False


class makeBelt:

	def __init__(self, system, index, name, bodyType, color, size, density = 1):  # change default values during instantiation
		self.Name = name
		self.solarsystem = system
		self.Density = density		# body name
		self.RadiusMinAU = belt_data[index]["radius_min"]	# in AU
		self.RadiusMaxAU = belt_data[index]["radius_max"]	# in AU
		self.Thickness = belt_data[index]["thickness"]	# in AU
		self.ThicknessFactor = belt_data[index]["thickness_factor"]
		self.Color = color
		self.BodyType = bodyType
		self.BodyShape =	points(pos=(self.RadiusMinAU, 0, 0), size=size, color=color)
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
			eclipticHeight = {0: 0, 1:1, 2:-1}[randint(0,2)] * randint(0, int(round(MAX, 6)*1.e6))/1e6
			self.BodyShape.append(pos=(RandomRadius * cos(i), RandomRadius * sin(i), eclipticHeight))

		self.Label = label(pos=(self.RadiusMaxAU * AU * DIST_FACTOR * cos(i), self.RadiusMaxAU * AU * DIST_FACTOR * sin(i), 0), text=self.Name, xoffset=20, yoffset=12, space=0, height=10, border=6, box=false, font='sans')
		self.Label.visible = False

	def refresh(self):
		if self.BodyType & self.solarsystem.ShowBodies <> 0:
			if self.BodyShape.visible == false:
				self.BodyShape.visible = true
				self.Label.visible = true
		else:
			if self.BodyShape.visible == true:
				self.BodyShape.visible = false
				self.Label.visible = false

class makeBody:

	def __init__(self, system, index, color, trueAnomaly, bodyType = INNERPLANET, sizeCorrectionType = INNERPLANET):  # change default values during instantiation
		self.solarsystem = system
		self.Ring = false
		self.OrbitalObliquity 				= planets_data[index]["orbital_obliquity"]
		self.Name 							= planets_data[index]["name"]		# body name
		self.Mass 							= planets_data[index]["mass"]		# body mass
		self.BodyRadius 					= planets_data[index]["radius"]	# body radius at perhelion
		self.Color 							= color
		self.BodyType 						= bodyType
		self.Revolution 					= planets_data[index]["revolution"]
		self.Perihelion 					= planets_data[index]["perihelion"]	# body perhelion
		self.Distance 						= planets_data[index]["perihelion"]	# body distance at perige from focus
		if "earth_moid" in planets_data[index]:
			self.Moid 						= planets_data[index]["earth_moid"]
		else:
			self.Moid 						= 0

		if "kep_elt" in planets_data[index]:
			# we have built-in data to calculate the body's current position on orbit
			self.updateKeplerianElements(planets_data[index]["kep_elt"])
		else:
			# data comes from data files or predefined values
			self.updateElements(planets_data[index])

		# generate 2d coordinate in the initial orbital plane, with +X pointing
		# towards periapsis. Make sure to convert degree to radians before using
		# any sin or cos function

		curr_E_rad = deg2rad(self.E)
		self.X = self.a * (cos(curr_E_rad) - self.e)
		self.Y = self.a * sqrt(1 - self.e**2) * sin(curr_E_rad)
		self.Z = 0

		# Now calculate current Radius and true Anomaly
		self.R = sqrt(self.X**2 + self.Y**2)
		self.Nu = atan2(self.Y,self.X)
		# Note that atan2 returns an angle in
		# radian, so Nu is always in radian

		self.b = getSemiMinor(self.a, self.e)
		self.Aphelion = getAphelion(self.a, self.e)	# body aphelion

		# initial acceleration
		self.Acceleration = vector(0,0,0)
		self.Interval = 0

		self.Position = np.matrix([[0],[0],[0]], np.float64)

		self.Rotation_VernalEquinox = np.matrix([
			[-1,	 0, 	0],
			[ 0,	-1,		0],
			[ 0,	 0,		1]]
		)

		# calculate current position of body on its orbit knowing
		# its current distance from Sun (R) and angle (Nu)

		self.N = deg2rad(self.Longitude_of_ascendingnode)
		self.w = deg2rad(self.Argument_of_perihelion)
		self.i = deg2rad(self.Inclinaison)

		# go polar to Cartesian
		self.Position[X_COOR] = self.R * DIST_FACTOR * ( cos(self.N) * cos(self.Nu+self.w) - sin(self.N) * sin(self.Nu+self.w) * cos(self.i) )
		self.Position[Y_COOR] = self.R * DIST_FACTOR * ( sin(self.N) * cos(self.Nu+self.w) + cos(self.N) * sin(self.Nu+self.w) * cos(self.i) )
	 	self.Position[Z_COOR] = self.R * DIST_FACTOR * ( sin(self.Nu+self.w) * sin(self.i) )

		# Last, rotate 180 degrees to match the vernal equinox referential
		self.Position = self.Rotation_VernalEquinox * self.Position

		sizeCorrection = { INNERPLANET: 500, GASGIANT: 1500, DWARFPLANET: 100, ASTEROID:1, COMET:0.001, SMALL_ASTEROID: 0.1, BIG_ASTEROID:0.1, PHA: 0.003}[sizeCorrectionType]
		shape = { INNERPLANET: "sphere", OUTTERPLANET: "sphere", DWARFPLANET: "sphere", ASTEROID:"cube", COMET:"cone", SMALL_ASTEROID:"cube", BIG_ASTEROID:"sphere", PHA:"cube"}[bodyType]
		self.SizeCorrection = getSigmoid(self.Perihelion, sizeCorrection)

		if shape == "sphere":
			self.BodyShape = sphere(pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]), radius=self.BodyRadius/self.SizeCorrection, make_trail=false)
			self.Angle = pi/2 + deg2rad(self.OrbitalObliquity)
		else:
			self.BodyShape = ellipsoid(pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]), length=(self.BodyRadius * randint(1, 5))/self.SizeCorrection, height=(self.BodyRadius * randint(1, 5))/self.SizeCorrection, width=(self.BodyRadius * randint(1, 5))/self.SizeCorrection, make_trail=false)
			self.Angle = pi/randint(2,6)

		# attach a curve to the object to display its orbit
		self.Trail = curve(color=self.Color)
		self.Trail.append(pos=self.BodyShape.pos)

		if planets_data[index]["material"] <> 0:
			data = materials.loadTGA("./img/"+index)
		else:
			data = materials.loadTGA("./img/asteroid")

		self.BodyShape.material = materials.texture(data=data, mapping="spherical", interpolate=False)
		self.BodyShape.rotate(angle=self.Angle)

		# add LEGEND
		self.Label = label(pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]), text=self.Name, xoffset=20, yoffset=12, space=0, height=10, color=color, border=6, box=false, font='sans')
		if (self.solarsystem.ShowBodies & bodyType) == 0:
			self.BodyShape.visible = false
			self.Label.visible = false

	# will calculate current value of approximate position of the major planets
	# including pluto. This won't work for Asteroid, Comets or Dwarf planets
	def updateKeplerianElements(self, elts):
		# get number of days since J2000 epoch
		T = daysSinceJ2000UTC()/36525.

		self.a = (elts["a"] + (elts["ar"] * T)) * AU
		self.e = elts["e"] + (elts["er"] * T)
		self.Inclinaison = elts["i"] + (elts["ir"] * T)

		# compute mean Longitude with correction factors beyond jupiter M = L - W + bT^2 +ccos(ft) + ssin(ft)
		L = elts["L"] + (elts["Lr"] * T) + (elts["b"] * T**2  +
											elts["c"] * cos(elts["f"] * T) +
											elts["s"] * sin(elts["f"] * T))
		self.Longitude_of_perihelion = elts["W"] + (elts["Wr"] * T)
		self.Longitude_of_ascendingnode = elts["N"] + (elts["Nr"] * T)

		# compute Argument of perihelion w = Longitude of Perihelion - Longitude of ascending Node
		#self.Longitude_of_perihelion 	= W
		#self.Longitude_of_ascendingnode = N
		self.Argument_of_perihelion 	= self.Longitude_of_perihelion - self.Longitude_of_ascendingnode

		# compute mean Anomaly M = L - W
		M = toRange(L-self.Longitude_of_perihelion) #W)

		"""
		# Obtain ecc. Anomaly E (in degrees) from M using an approx method of resolution:
		"""
		success, self.E, dE, it = solveKepler(M, self.e, 12000)
		if success == False:
			print "Could not converge for "+self.Name+", E = "+str(self.E)+", last precision = "+str(dE)

	def updateElements(self, elts):
			# data comes from data files or predefined values
			self.e 							= elts["e"]
			self.Longitude_of_perihelion 	= elts["longitude_of_perihelion"]
			self.Longitude_of_ascendingnode = elts["longitude_of_ascendingnode"]
			self.Argument_of_perihelion 	= self.Longitude_of_perihelion - self.Longitude_of_ascendingnode
			self.a 							= getSemiMajor(self.Perihelion, self.e)
			self.Inclinaison 				= elts["orbital_inclinaison"]
			self.Time_of_perihelion_passage = elts["Time_of_perihelion_passage_JD"]
			self.Mean_motion				= elts["mean_motion"]
			self.Epoch						= elts["epochJD"]
			self.Mean_anomaly				= elts["mean_anomaly"]
			self.revolution					= elts["revolution"]

			# calculate current position based on orbital elements
			# the formula is E - esinE = (t - T)n

			dT = daysSinceEpochJD(self.Epoch)
			N = self.Longitude_of_ascendingnode + 0.013967 * (2000.0 - getCurrentYear()) + 3.82394e-5 * dT
			self.Longitude_of_ascendingnode = N

			# adjust Mean Anomaly with time elapsed since epoch
			M = self.Mean_anomaly + self.Mean_motion * dT
			M = toRange(M)

			success, self.E, dE, it = solveKepler(M, self.e, 20000)
			if success == False:
				print self.Name+" Warning Could not converge - E = "+str(self.E)

	def draw(self):

		self.Trail.visible = false
		rad_E = deg2rad(self.E)
		if self.BodyType == COMET:
			# for comets, due to their sometimes high eccentricity, an increment of 1 deg may not be small enough
			# to insure a smooth curve, hence we need to take smaller increments of 12.5 arcminutes in radians
			increment = pi/(180 * 4)
		else:
			# Otherwise use 1 degree increment in radians
			increment = pi/180

		for E in np.arange(increment, 2*pi+increment, increment):

			X = self.a * (cos(E+rad_E) - self.e)
			Y = self.a * sqrt(1 - self.e**2)*sin(E+rad_E)
			Z = 0

			self.R = sqrt(X**2 + Y**2)
			self.Nu = atan2(Y, X) # the result is in rads, so no need to convert

			# from R and Nu, calculate 3D coordinates and update current position
			self.updatePosition(E*180/pi)
			rate(5000)

		if self.BodyShape.visible:
			self.Trail.visible = true

	def updatePosition(self, trace = true):

		self.Position[X_COOR] = self.R * DIST_FACTOR * ( cos(self.N) * cos(self.Nu+self.w) - sin(self.N) * sin(self.Nu+self.w) * cos(self.i) )
		self.Position[Y_COOR] = self.R * DIST_FACTOR * ( sin(self.N) * cos(self.Nu+self.w) + cos(self.N) * sin(self.Nu+self.w) * cos(self.i) )
	 	self.Position[Z_COOR] = self.R * DIST_FACTOR * ( sin(self.Nu+self.w) * sin(self.i) )

		self.Position = self.Rotation_VernalEquinox * self.Position

		self.BodyShape.pos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])
		if trace:
			if self.Position[Z_COOR] < 0:
				self.Interval += 1
				if self.Interval % 2 == 0:
					self.Trail.append(pos=self.BodyShape.pos, color=self.Color) #, interval=50)
				else:
					self.Trail.append(pos=self.BodyShape.pos, color=color.black) #, interval=50)
			else:
				self.Trail.append(pos=self.BodyShape.pos, color=self.Color)


	def refresh(self):
		if self.solarsystem.AnimationInProgress and self.BodyType == self.solarsystem.currentSource:
			return

		if self.BodyType & self.solarsystem.ShowBodies <> 0 or self.Name == 'Earth':
			if self.BodyShape.visible == False:
				self.BodyShape.visible = True
				self.Label.visible = True
				if self.solarsystem.ShowBodies & ORBITS <> 0:
					self.Trail.visible = True
				else:
					self.Trail.visible = False

				if self.Ring:
					self.InnerRing.visible = True
					self.OutterRing.visible = True
		else:
			self.BodyShape.visible = False
			self.Label.visible = False
			self.Trail.visible = False
			if self.Ring:
				self.InnerRing.visible = False
				self.OutterRing.visible = False


	def getCurrentOrbitRadius(self, angle_in_rd):
		self.CurrRadius = (self.a * (1 - self.e**2))/(1 + cos(angle_in_rd))
		return self.CurrRadius

	def getCurrentVelocity(self):
		# the formulat is v^2 = GM(2/r - 1/a)
		return sqrt(G*SUN_M*((2/self.Distance) - (1/self.a)))

#
# various functions
#
def getSigmoid(distance, correction):
	sigmoid = 1/(1+exp(-MAX_P_D/distance))
	return correction * sigmoid

# independent functions
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

def glbRefresh(solarSystem):
	solarSystem.refresh()
	for body in solarSystem.bodies:
		body.refresh()

def hideBelt(beltname):
	beltname.BodyShape.visible = false
	beltname.Label.visible = false

def showBelt(beltname):
	beltname.BodyShape.visible = true
	beltname.Label.visible = true

def setBodyPosition(body, theta):
	theta = (math.pi * theta)/180
	R = (body.a*(1 - body.e**2))/(1 + body.e*cos(theta))
	body.X = R*cos(theta)
	body.Y = R*sin(theta)
	body.updatePosition(false)
	if LEGEND:
		body.Label.visible = false
		body.Label = label(pos=(body.Position[X_COOR],body.Position[Y_COOR],body.Position[Z_COOR]), text=body.Name, xoffset=20, yoffset=12, space=0, height=10, color=body.Color, border=6, box=false, font='sans')

def getColor():
	return { 0: color.white, 1: color.red, 2: color.orange, 3: color.yellow, 4: color.cyan, 5: color.magenta, 6: color.green}[randint(0,6)]

# Calculates Eccentric Anomaly (E) given the mean anomaly (M) and the depth of the Bessel first kind functions
def bessel_E(M, e, depth):
    return (M + sum(2.0 / n * sp.jv(n, n * e) * np.sin(n * M)
                    for n in range(1, depth, 1)))

# Calculates Eccentric Anomaly (E) given the mean anomaly (M), the depth and the
# precision required using an iterative method. If the precision has been reached
# within the maximum iteration depth, returns (True, E) or (False, E) otherwise

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
# Anomaly (E), the orbit eccentricity and the semi-majour axis

def getTrueAnomalyAndRadius(E, e, a):
	ta = 2 * arctan(sqrt((1+e)/(1-e)) * tan(E/2))
	R = a * (1 - e*cos(E))
	if ta < 0:
		ta = ta + 2*math.pi
	return ta, R

def loadBodies(solarsystem, type, filename):
	fo  = open(filename, "r")
	limit = 10000
	token = []
	print "Loading "+filename
	for line in fo:
		if line[0] == '#':
			continue
		else:
			token = line.split('|')
			if len(token) > 0:
				planets_data[token[JPL_DESIGNATION]] = {
					"material": 0,
					"name": token[JPL_FULLNAME],
					"mass": (float(token[JPL_GM])/G)*1.e+9 if token[JPL_GM] else 0, # convert km3 to m3
					"radius": float(token[JPL_DIAMETER])/2 if token[JPL_DIAMETER] else 0,
					"perihelion": float(token[JPL_OE_q]) * AU,
					"e": float(token[JPL_OE_e]),
					"revolution": float(token[JPL_OE_Pd]),
					"orbital_inclinaison": 	float(token[JPL_OE_i]),
					"longitude_of_ascendingnode":float(token[JPL_OE_N]),
					"argument_of_perihelion": float(token[JPL_OE_w]),
					"longitude_of_perihelion":float(token[JPL_OE_N])+float(token[JPL_OE_w]),
					"Time_of_perihelion_passage_JD":float(token[JPL_OE_tp_JD]),
					"mean_motion": float(token[JPL_OE_n]) if token[JPL_OE_n] else 0,
					"mean_anomaly": float(token[JPL_OE_M]) if token[JPL_OE_M] else 0,
					"epochJD": float(token[JPL_EPOCH_JD]),
					"earth_moid": (float(token[JPL_EARTH_MOID_AU])*AU) if token[JPL_EARTH_MOID_AU] else 0,
					"orbital_obliquity": 0 # in deg
				}

				solarsystem.addTo(makeBody(solarsystem, token[JPL_DESIGNATION], getColor(), 0, type, type))
				limit = limit - 1
				if limit <= 0:
					break
	fo.close()


# ----------------
# TIME MANAGEMENT
# ----------------
def getJ2000():
	return 2451545.0

def getCurrentYear(year = 0):
	if year == 0:
		utc = datetime.datetime.utcnow()
		y = utc.year
	else:
		y = year
	return float(y)

def JDdaydiff(jd):
	# note that if jd corresponds to a date before 2000
	# jd - 2451543.5 will be a negative value
	return float(jd - 2451543.5)

def MJDdaydiff(mjd):
	return float(mjd - 51543.0)

# returns number of days since J2000 from current JDE
def JDE2day(jde):
	return float(jde - 2451543.5)

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

# will compute the number of days since J2000 UTC
def daysSinceJ2000UTC(delta = 0):
	utc = datetime.datetime.utcnow()
	return delta + 367*utc.year - (7*(utc.year + ((utc.month+9)/12)))/4 + (275*utc.month)/9 + utc.day - 730530 + (utc.hour + utc.minute/60)/24

def daysSinceEpochJD(epochJD):
	if epochJD == 0:
		# when epoch is not known, epoch is set to zero
		return 0
	# otherwise determine number of days since epoch
	days = daysSinceJ2000UTC() # days from 2000
	return days - (epochJD - 2451543.5)

def day():
	y = 1999
	m = 12
	D = 31
	return 367*y - 7 * ( y + (m+9)/12 ) / 4 + 275*m/9 + D - 730530

def deg2rad(deg):
	return deg * math.pi/180

def rad2deg(rad):
	return rad * 180/math.pi

def main():
	solarsystem = solarSystem()
	solarsystem.ShowBodies = INNERPLANET|ORBITS

	solarsystem.addTo(makeEcliptic(solarsystem, color.white))
	solarsystem.addTo(makeBody(solarsystem, 'mercury', color.green, 70))
	solarsystem.addTo(makeBody(solarsystem, 'venus', color.yellow, 0))
	solarsystem.addTo(makeBody(solarsystem, 'earth', color.cyan, 225))
	solarsystem.addTo(makeBody(solarsystem, 'mars', color.red, 0))
	solarsystem.addTo(makeBody(solarsystem, 'jupiter', color.magenta, 0, OUTTERPLANET, GASGIANT))
	solarsystem.addTo(makeBody(solarsystem, 'saturn', color.cyan, 20, OUTTERPLANET, GASGIANT))
	solarsystem.addTo(makeBody(solarsystem, 'uranus', color.yellow, 0, OUTTERPLANET, GASGIANT))
	solarsystem.addTo(makeBody(solarsystem, 'neptune', color.orange, 0, OUTTERPLANET, GASGIANT))
	solarsystem.addTo(makeBody(solarsystem, 'pluto', color.green, 0, OUTTERPLANET, DWARFPLANET))

	solarsystem.makeRings(solarsystem, "saturn")

	# generate DWARF planets
	solarsystem.addTo(makeBody(solarsystem, 'eris', color.yellow, 0, DWARFPLANET, DWARFPLANET))
	solarsystem.addTo(makeBody(solarsystem, 'makemake', color.magenta, 0, DWARFPLANET, DWARFPLANET))
	solarsystem.addTo(makeBody(solarsystem, 'sedna', color.orange, 0, DWARFPLANET, DWARFPLANET))
	solarsystem.addTo(makeBody(solarsystem, 'haumea', color.white, 0, DWARFPLANET, DWARFPLANET))
	solarsystem.addTo(makeBody(solarsystem, 'MU69', color.red, 0, DWARFPLANET, DWARFPLANET))

	# generate Belts
	solarsystem.addTo(makeBelt(solarsystem, 'kuiper', 'Kuiper Belt', KUIPER_BELT, color.cyan, 2, 4))
	solarsystem.addTo(makeBelt(solarsystem, 'asteroid', 'Asteroid Belt', ASTEROID_BELT, color.white, 2, 2))
	solarsystem.addTo(makeBelt(solarsystem, 'inneroort', 'Inner Oort Cloud', INNER_OORT_CLOUD, color.white, 2, 5))

	LOAD_SMALL_OBJECTS = True

	if LOAD_SMALL_OBJECTS:
		loadBodies(solarsystem, PHA, "200m+PHA_orbital_elements.txt")
		loadBodies(solarsystem, BIG_ASTEROID,"200km+asteroids_orbital_elements.txt")
		loadBodies(solarsystem, COMET, "200m+comets_orbital_elements.txt")

	solarsystem.drawAllBodiesTrajectory()

	# Start control window
	print wx.version()
	ex = wx.App()
	cw = controlWindow(None, solarsystem)

	while True:
		rate(2)

if __name__ == '__main__' :
	main()
