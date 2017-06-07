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
from PIL import Image

import sys
import numpy as np
from matplotlib import *
from random import *
import scipy.special as sp
import datetime

import wx

INNERPLANET = 0x01
GASGIANT = 0x02
DWARFPLANET = 0x04
ASTEROID = 0x08
COMET = 0x10
SMALL_ASTEROID = 0x20
BIG_ASTEROID = 0x40
PHA = 0x80
ASTEROID_BELT = 0x100
KUIPER_BELT = 0x200
INNER_OORT_CLOUD = 0x400

TYPE_MASK = 0xFFF

SUN_M = 1.989e30
SUN_R = 696e6
G = 6.67384e-11
Mu = G * SUN_M
DIST_FACTOR = 10e-7
X_COOR = 0
Y_COOR = 1
Z_COOR = 2

AU = 149597870691

SATELLITE_M = 100
THREE_D = False
MAX_P_D = 1.1423e13
MIN_P_D = 46.0e9
LEGEND = true
REFERENTIAL = False

INNER_RING_COEF = 1.3
OUTTER_RING_COEF = 1.9

# read PHA list - each asteroid has its orbital elements pipe ('|') separated and stored with the following structure:
# object fullname|prim. desig.|IAU name|NEO (Y/N)|PHA (Y/N)|eccentricity|perihelion distance (au)|inclinaison (deg)|longitude of ascending node (deg)|
# argument of perihelion (deg)|orbital period (days)|Earth MOID (au)|orbit class|
NEO_FULLNAME = 0
NEO_DESIGNATION = 1
NEO_IAU_NAME = 2
NEO_NEAR_EARTH_ORBIT = 3
NEO_PHA = 4
NEO_DIAMETER = 5
NEO_GM = 6
NEO_EPOCH_JED = 7
NEO_EPOCH_MJD = 8
NEO_EPOCH_ET = 9
NEO_EQUINOX = 10
NEO_ECC = 11
NEO_SEMI_MAJOR = 12
NEO_DIST_OF_PERIHELION = 13
NEO_INC = 14
NEO_LAN = 15
NEO_AOP = 16
NEO_MEAN_ANOMALY = 17
NEO_MEAN_MOTION = 18
NEO_TIME_OF_PERIHELION_PASSAGE_JED = 19
NEO_TIME_OF_PERIHELION_PASSAGE_ET = 20
NEO_ORBITAL_P = 21
NEO_EARTH_MOID = 22

SMALL_OBJECTS = True

class controlWindow(wx.Frame):

	def __init__(self, dummy, solarsystem):
		wx.Frame.__init__(self, None)
		self.checkboxList = {}
		self.PauseAnimation = False
		self.Source = PHA
		self.solarsystem = solarsystem
		self.InitUI()

	def createCheckBox(self, panel, title, type, xpos, ypos):
		cb = wx.CheckBox(panel, label=title, pos=(xpos, ypos))
		if self.solarsystem.SHOW_BODIES & type <> 0:
			cb.SetValue(True)
		else:
			cb.SetValue(False)

		self.checkboxList[type] = cb

	def InitUI(self):
		pnl = wx.Panel(self)

		font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		heading = wx.StaticText(pnl, label='Show', pos=(20, 20))
		heading.SetFont(font)

		self.createCheckBox(pnl, "Inner Planets", INNERPLANET, 20, 40)
		self.createCheckBox(pnl, "Gas Giants", GASGIANT, 20, 60)
		self.createCheckBox(pnl, "Dwarf Planets", DWARFPLANET, 20, 80)
		self.createCheckBox(pnl, "Potentially Hazardous Asteroids with size > 100m", PHA, 20, 100)
		self.createCheckBox(pnl, "Comets", COMET, 20, 120)
		self.createCheckBox(pnl, "Big Asteroids", BIG_ASTEROID, 20, 140)
		self.createCheckBox(pnl, "Asteroids Belt", ASTEROID_BELT, 20, 160)
		self.createCheckBox(pnl, "Kuiper Belt", KUIPER_BELT, 20, 180)
		self.createCheckBox(pnl, "Inner Oort Cloud", INNER_OORT_CLOUD, 20, 200)

		cbtn = wx.Button(pnl, label='Refresh', pos=(20, 220))
		cbtn.Bind(wx.EVT_BUTTON, self.OnRefresh)

		lblList = ['PHA', 'Comets', 'Big Asteroids']
		self.rbox = wx.RadioBox(pnl,label = 'Animate', pos = (200,220), choices = lblList ,majorDimension = 1, style = wx.RA_SPECIFY_COLS)
		self.rbox.Bind(wx.EVT_RADIOBOX,self.OnRadioBox)

		self.Animate = wx.Button(pnl, label='Start', pos=(340, 220))
		self.Animate.Bind(wx.EVT_BUTTON, self.OnAnimate)

		self.Pause = wx.Button(pnl, label='Pause', pos=(340, 260))
		self.Pause.Bind(wx.EVT_BUTTON, self.OnPauseAnimate)
		self.Pause.Hide()

		self.InfoTitle = wx.StaticText(pnl, label="", pos=(20, 360))
		self.InfoTitle.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
		self.Info1 = wx.StaticText(pnl, label="", pos=(20, 380))
		self.Info1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)) #, wx.BOLD))
		self.Info1.Wrap(230)
		self.Info2 = wx.StaticText(pnl, label="", pos=(240, 380))
		self.Info2.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)) #, wx.BOLD))
		self.Info2.Wrap(250)

		self.SetSize((500, 550))
		self.SetTitle('Orbital Control')
		self.Centre()
		self.Show(True)

	def OnRadioBox(self, e):
		index = self.rbox.GetSelection()
		self.Source = {0: PHA, 1: COMET, 2:BIG_ASTEROID}[index]
		self.solarsystem.currentSource = self.Source

	def OnRefresh(self, e):
		for type, cbox in self.checkboxList.iteritems():
			if cbox.GetValue() == True:
				self.solarsystem.SHOW_BODIES |= type
			else:
				self.solarsystem.SHOW_BODIES = (self.solarsystem.SHOW_BODIES & ~type)
		refresh(self.solarsystem)

	def OnPauseAnimate(self, e):
		if self.PauseAnimation:
			e.GetEventObject().SetLabel("Pause")
			self.PauseAnimation = False
		else:
			e.GetEventObject().SetLabel("Resume")
			self.PauseAnimation = True

	def OnAnimate(self, e):
		if self.solarsystem.AnimationInProgress:
			self.solarsystem.AbortAnimation = True
			self.PauseAnimation = False
			e.GetEventObject().SetLabel("Start")
			self.InfoTitle.SetLabel('')
			self.Info1.SetLabel('')
			self.Info2.SetLabel('')
			self.Pause.SetLabel("Pause")
			self.Pause.Hide()
			return
		else:
			self.solarsystem.AnimationInProgress = True
			self.Pause.Show()
			self.Animate.SetLabel("Stop")

		for body in self.solarsystem.bodies:
			if body.BodyType == self.Source: #PHA:
				if self.checkboxList[self.Source].GetValue() == True:
					self.checkboxList[self.Source].SetValue(False)
					self.solarsystem.SHOW_BODIES = (self.solarsystem.SHOW_BODIES & ~self.Source)
					AnimationState = self.solarsystem.AnimationInProgress
					self.solarsystem.AnimationInProgress = False
					refresh(self.solarsystem)
					self.solarsystem.AnimationInProgress = AnimationState

				self.InfoTitle.SetLabel(body.Name)

				mass = str(body.Mass)+" kg" if body.Mass <> 0 else "Not Provided"
				radius = str(body.BodyRadius)+" km" if body.BodyRadius <> 0 else "Not Provided"
				moid = str(body.Moid/1000)+" km" if body.Moid <> 0 else "N/A"
				rev = str(body.Revolution / (86400 *365.25))

				self.Info1.SetLabel("i  : "+str(body.Inclinaison)+" deg\nN : "+str(body.Longitude_of_ascendingnode)+" deg\nw : "+str(body.Argument_of_perihelion)+" deg\ne : "+str(body.e)+"\nq : "+str(body.Perihelion/1000)+" km")
				self.Info2.SetLabel("M : "+mass+"\nR : "+radius+"\nP: "+rev+" yr"+"\n\nMoid :"+moid)

				body.Look.visible = True
				body.Label.visible = True
				body.Trail.visible = True
				for i in range(0,2):
					rate(1)

				while (self.PauseAnimation and self.solarsystem.AbortAnimation == False):
					rate(1)

				body.Look.visible = False
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
		"neptune" :{"material":1,
					"name": "Neptune",
					"mass":102e24,
					"radius":24622e3,
					"perihelion":4444.45e9,
					"e":0.00858587,
					"revolution":164.179 * 365 * 86400,
					"orbital_inclinaison":1.769,
					"longitude_of_ascendingnode":131.72169,
					"longitude_of_perihelion":44.97135},

		"uranus" : {"material":1,
					"name": "Uranus",
					"mass":86.8e24,
					"radius":25362e3,
					"perihelion":2741.30e9,
					"e":0.04716771,
					"revolution":84.011 * 365 * 86400,
					"orbital_inclinaison":0.770,
					"longitude_of_ascendingnode":74.22988,
					"longitude_of_perihelion":170.96424},

		"saturn" : {"material":1,
					"name": "Saturn",
					"mass":568e24,
					"radius":58232e3,
					"perihelion":1352.55e9,
					"e":0.05415060,
					"revolution":29.457 * 365 * 86400,
					"orbital_inclinaison":2.484,
					"longitude_of_ascendingnode":113.71504,
					"longitude_of_perihelion":92.43194},

		"jupiter" :{"material":1,
					"name": "Jupiter",
					"mass":1898e24,
					"radius":69911e3,
					"perihelion":740.52e9,
					"e":0.04839266,
					"revolution":11.862 * 365 * 86400,
					"orbital_inclinaison":1.305,
					"longitude_of_ascendingnode":100.55615,
					"longitude_of_perihelion":14.75385},

		"mars" : {	"material":1,
					"name": "Mars",
					"mass":0.642e24,
					"radius":3389e3,
					"perihelion":206.62e9,
					"e":0.09341233,
					"revolution":686.98 * 86400,
					"orbital_inclinaison":1.851,
					"longitude_of_ascendingnode":49.57854,
					"longitude_of_perihelion":336.04084},

		"mercury" :{"material":1,
					"name": "Mercury",
					"mass":0.330e24,
					"radius":2439e3,
					"perihelion":46.0e9,
					"e":0.20563069,
					"revolution":87.969 * 86400,
					"orbital_inclinaison":7.005,
					"longitude_of_ascendingnode":48.33167,
					"longitude_of_perihelion":77.45645},

		"venus" : {	"material":1,
					"name": "Venus",
					"mass":4.87e24,
					"radius":6052e3,
					"perihelion":107.48e9,
					"e":0.00677323,
					"revolution":224.701 * 86400,
					"orbital_inclinaison":3.3947,
					"longitude_of_ascendingnode":76.68069,
					"longitude_of_perihelion":131.53298},

		"earth" : {	"material":1,
					"name": "Earth",
					"mass":5.972e24,
					"radius":6371e3,
					"perihelion":147.09e9,
					"e":0.01671022,
					"revolution":355.256 * 86400,
					"orbital_inclinaison":0,
					"longitude_of_ascendingnode":-11.26064, # or +360-11.26064 = 348.73936
					"longitude_of_perihelion":102.94719},

		"eris" : {	"material":0,
					"name": "Eris",
					"mass":1.66e22,
					"radius":1163e3,
					"perihelion":5.723e12,
					"e":0.44068,
					"revolution": 203830 * 86400,
					"orbital_inclinaison":44.0445,
					"longitude_of_ascendingnode": 35.9531,
					"longitude_of_perihelion":186.9301},

		"pluto" : {	"material":1,
					"name": "Pluto",
					"mass":0.0146e24,
					"radius":1195e3,
					"perihelion":4436.82e9,
					"e":0.24880766,
					"revolution":247.68 * 365 * 86400,
					"orbital_inclinaison":17.142,
					"longitude_of_ascendingnode":110.30347,
					"longitude_of_perihelion":224.06676},

		"makemake":{"material":0,
					"name": "Makemake",
					"mass":4.4e21,
					"radius":739e3,
					"perihelion":5.77298e12,
					"e":0.15586,
					"revolution": 112897 * 86400,
					"orbital_inclinaison":29.00685,
					"longitude_of_ascendingnode": 79.3659,
					"longitude_of_perihelion":376.6059},

		"sedna":   {"material":0,
					"name": "Sedna",
					"mass":4.4e21, # mass is undetermined
					"radius":995e3,
					"perihelion":1.1423e13,
					"e":0.85491,
					"revolution": 11400 * 365 * 86400,
					"orbital_inclinaison":11.92872,
					"longitude_of_ascendingnode":144.546,
					"longitude_of_perihelion":455.836},

		"haumea":  {"material":0,
					"name": "Haumea",
					"mass":4.006e21,
					"radius":620e3,
					"perihelion":5.228745e+12,
					"e":0.19126,
					"revolution": 112897 * 86400,
					"orbital_inclinaison":28.19,
					"longitude_of_ascendingnode":121.79,
					"longitude_of_perihelion":361.99},

		"67P":{"material":0,
					"name": "Churyumov-Gerasimenko",
					"mass":5e13, # unknown
					"radius":2000,
					"perihelion":1.2432 * AU,
					"e":0.64102,
					"revolution": 6.44 * 365 * 86400,
					"orbital_inclinaison":7.0405,
					"longitude_of_ascendingnode":50.147,
					"argument_of_perihelion": 12.780,
					"longitude_of_perihelion":62.927}
}

belt_data = {
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
	bodies = []

	def __init__(self):
		self.Name = "Sun"
		self.BodyRadius = SUN_R
		self.Mass = SUN_M
		self.AbortAnimation = False
		self.AnimationInProgress = False
		self.currentSource = PHA

		self.Scene = display(title = 'Solar System', width = 1300, height = 740, center = (0,0,0)) #, forward=forward)

		self.Scene.lights = []
		self.Scene.forward = (0,0,-1)
		self.Scene.fov = math.pi/3
		self.Scene.userspin = True
		self.Scene.userzoom = True
		self.Scene.autoscale = True
		self.Scene.autocenter = False
		self.Scene.up = (0,0,1)

		# make all light coming from origin
		sunLight = local_light(pos=(0,0,0))

		if THREE_D:
			self.Scene.stereo='redcyan'
			self.Scene.stereodepth = 1

		self.Look = sphere(pos=vector(0,0,0), radius=self.BodyRadius/(35000), color=color.white)
		self.Look.material = materials.emissive

		if REFERENTIAL:
			self.makeAxes(color.white, AU*1.2*DIST_FACTOR, (0,0,0))

	def makeAxes(self, color, size, position):
	    directions = [vector(size,0,0), vector(0,size,0), vector(0,0,size)]
	    texts = ["x","y","z"]
	    pos = vector(position)
	    for i in range (3):
	       curve( frame = None, color = color, pos= [ pos, pos+directions[i]])
	       label( frame = None, color = color,  text = texts[i],
		   			pos = pos+directions[i], opacity = 0, box = False )

	def addTo(self, body):
		self.bodies.append(body)

	def drawAllBodiesTrajectory(self):
		for body in self.bodies:
			body.drawOrbit()
			rate(10000)

	def getBodyFromName(self, bodyname):
		for body in self.bodies:
			if body.Name == bodyname:
				return body
		return None

	def setBodyPosition(self, bodyName, theta):
		body = self.getBodyFromName(bodyName)
		if body <> None:
			theta = (math.pi * theta)/180 # convert degrees to radians
			R = (body.a*(1 - body.e**2))/(1 + body.e*cos(theta))
			body.X = R * cos(theta)
			body.Y = R * sin(theta)
			body.updatePosition(false)
			if LEGEND:
				body.Label.visible = false
				body.Label = label(pos=(body.Position[X_COOR],body.Position[Y_COOR],body.Position[Z_COOR]), text=body.Name, xoffset=20, yoffset=12, space=0, height=10, color=body.Color, border=6, box=false, font='sans')

	def makeRings(self, system, bodyName, density = 1):
		global planets_data
		self.solarsystem = system
		bodyName = planets_data[bodyName]['name']
		planet = self.getBodyFromName(bodyName)
		if planet <> None:
			InnerRadius = planet.BodyRadius * INNER_RING_COEF / planet.SizeCorrection
			OutterRadius = planet.BodyRadius * OUTTER_RING_COEF / planet.SizeCorrection
			planet.Ring = true
			planet.InnerRing = curve(color=planet.Color)
			planet.OutterRing = curve(color=planet.Color)

			if (self.solarsystem.SHOW_BODIES & planet.BodyType) == 0:
				planet.InnerRing.visible = false
				planet.OutterRing.visible = false

			for i in np.arange(0, 2*math.pi, math.pi/(180*density)):
				planet.OutterRing.append(pos=((OutterRadius * cos(i))+planet.Position[X_COOR], (OutterRadius * sin(i))+planet.Position[Y_COOR], planet.Position[Z_COOR]), color=planet.Color) #radius=pointRadius/planet.SizeCorrection, size=1)
				planet.InnerRing.append(pos=((InnerRadius * cos(i))+planet.Position[X_COOR], (InnerRadius * sin(i))+planet.Position[Y_COOR], planet.Position[Z_COOR]), color=planet.Color) #radius=pointRadius/planet.SizeCorrection, size=1)


class makeBelt:
	def __init__(self, system, index, name, bodyType, color, size, density = 1):

		self.Name = name
		self.solarsystem = system
		self.Density = density
		self.RadiusMinAU = belt_data[index]["radius_min"]	# in AU
		self.RadiusMaxAU = belt_data[index]["radius_max"]	# in AU
		self.Thickness = belt_data[index]["thickness"]		# in AU
		self.ThicknessFactor = belt_data[index]["thickness_factor"]
		self.Color = color
		self.BodyType = bodyType
		self.Look =	points(pos=(self.RadiusMinAU, 0, 0), size=size, color=color)
		self.Look.visible = False
		if self.Thickness == 0:
			self.Thickness = (self.RadiusMinAU + self.RadiusMaxAU)/2 * math.tan(math.pi/6)

		shape = "cube"

	def getGaussian(self, position):
		mu = (self.RadiusMinAU + self.RadiusMaxAU)* AU * DIST_FACTOR/2
		sigma = (self.RadiusMaxAU - self.RadiusMinAU)* AU * DIST_FACTOR/3
		return float((1/(sigma*sqrt(math.pi*2)))*exp(-(((position-mu)/sigma)**2)/2))

	def drawOrbit(self):
		for i in np.arange(0, 2*math.pi, math.pi/(180*self.Density)):
			# generate random radius between Min and MAX
			RandomRadius = randint(round(self.RadiusMinAU * AU * DIST_FACTOR, 3) * 1000, round(self.RadiusMaxAU * AU * DIST_FACTOR, 3) * 1000) / 1000
			MAX = self.getGaussian(RandomRadius) * self.Thickness * AU * DIST_FACTOR * self.ThicknessFactor
			Z = {0: 0, 1:1, 2:-1}[randint(0,2)] * randint(0, int(round(MAX, 6)*1.e6))/1e6
			self.Look.append(pos=(RandomRadius * cos(i), RandomRadius * sin(i), Z))

		self.Label = label(pos=(self.RadiusMaxAU * AU * DIST_FACTOR * cos(i), self.RadiusMaxAU * AU * DIST_FACTOR * sin(i), 0), text=self.Name, xoffset=20, yoffset=12, space=0, height=10, border=6, box=false, font='sans')
		self.Label.visible = False

	def refresh(self):
		if self.BodyType & self.solarsystem.SHOW_BODIES <> 0:
			if self.Look.visible == false:
				self.Look.visible = true
				self.Label.visible = true
		else:
			if self.Look.visible == true:
				self.Look.visible = false
				self.Label.visible = false


class makeRings:

	def __init__(self, system, planet, density = 1):
		self.solarsystem = system
		InnerRadius = planet.BodyRadius * INNER_RING_COEF / planet.SizeCorrection
		OutterRadius = planet.BodyRadius * OUTTER_RING_COEF / planet.SizeCorrection
		planet.Ring = true
		planet.InnerRing = curve(color=planet.Color)
		planet.OutterRing = curve(color=planet.Color)

		if (self.solarsystem.SHOW_BODIES & planet.BodyType) == 0:
			planet.InnerRing.visible = false
			planet.OutterRing.visible = false

		for i in np.arange(0, 2*math.pi, math.pi/(180*density)):
			planet.OutterRing.append(pos=((OutterRadius * cos(i))+planet.Position[X_COOR], (OutterRadius * sin(i))+planet.Position[Y_COOR], planet.Position[Z_COOR]), color=planet.Color) #radius=pointRadius/planet.SizeCorrection, size=1)
			planet.InnerRing.append(pos=((InnerRadius * cos(i))+planet.Position[X_COOR], (InnerRadius * sin(i))+planet.Position[Y_COOR], planet.Position[Z_COOR]), color=planet.Color) #radius=pointRadius/planet.SizeCorrection, size=1)


class makeBody:

	def __init__(self, system, index, color, trueAnomaly, bodyType = INNERPLANET):  # change default values during instantiation
		self.solarsystem = system
		self.Ring = false
		self.TrueAnomaly = trueAnomaly
		self.Name = planets_data[index]["name"]
		self.Mass = planets_data[index]["mass"]
		self.Perihelion = planets_data[index]["perihelion"]
		self.Distance = planets_data[index]["perihelion"]
		self.BodyRadius = planets_data[index]["radius"]
		self.e = planets_data[index]["e"]
		self.Color = color
		self.BodyType = bodyType
		self.Revolution = planets_data[index]["revolution"]
		self.Longitude_of_perihelion = planets_data[index]["longitude_of_perihelion"]
		self.Longitude_of_ascendingnode = planets_data[index]["longitude_of_ascendingnode"]
		self.Argument_of_perihelion = self.Longitude_of_perihelion - self.Longitude_of_ascendingnode
		if "earth_moid" in planets_data[index]:
			self.Moid = planets_data[index]["earth_moid"]
		else:
			self.Moid = 0
		self.a = getSemiMajor(self.Perihelion, self.e)
		self.b = getSemiMinor(self.a, self.e)
		self.Aphelion = getAphelion(self.a, self.e)

		self.Inclinaison = planets_data[index]["orbital_inclinaison"]

		self.Angle_Om = self.Longitude_of_ascendingnode*math.pi/180
		self.Angle_i = self.Inclinaison*math.pi/180
		self.Angle_w = self.Argument_of_perihelion*math.pi/180

		# initial acceleration
		self.Acceleration = vector(0,0,0)
		self.Interval = 0

		# calculate body initial location
		self.nu = (math.pi * self.TrueAnomaly)/180 # convert degrees to radians
		R = (self.a*(1 - self.e**2))/(1 + self.e*cos(self.nu))
		self.X = R * cos(self.nu)
		self.Y = R * sin(self.nu)

		self.Position = np.matrix([
			[self.X*DIST_FACTOR],
			[self.Y*DIST_FACTOR],
			[0]])

		self.Euler_3D_Rotation = np.matrix([
			[cos(self.Angle_w)*cos(self.Angle_Om) - sin(self.Angle_w)*cos(self.Angle_i)*sin(self.Angle_Om),
			 cos(self.Angle_w)*sin(self.Angle_Om) + sin(self.Angle_w)*cos(self.Angle_i)*cos(self.Angle_Om),
			 sin(self.Angle_w)*sin(self.Angle_i)
			],
			[-sin(self.Angle_w)*cos(self.Angle_Om) - cos(self.Angle_w)*cos(self.Angle_i)*sin(self.Angle_Om),
			 -sin(self.Angle_w)*sin(self.Angle_Om) + cos(self.Angle_w)*cos(self.Angle_i)*cos(self.Angle_Om),
			 cos(self.Angle_w)*sin(self.Angle_i)
			],
			[sin(self.Angle_Om)*sin(self.Angle_i),
			 -sin(self.Angle_i)*cos(self.Angle_Om),
			 cos(self.Angle_i)
			]]
		)

		self.Position = self.Euler_3D_Rotation * self.Position

		self.X = self.Position[X_COOR]
		self.Y = self.Position[Y_COOR]
		self.Z = self.Position[Z_COOR]

		sizeCorrection = { INNERPLANET: 500, GASGIANT: 1500, DWARFPLANET: 20, ASTEROID:1, COMET:0.01, SMALL_ASTEROID: 0.1, BIG_ASTEROID:0.1, PHA: 0.003}[bodyType]
		shape = { INNERPLANET: "sphere", GASGIANT: "sphere", DWARFPLANET: "sphere", ASTEROID:"cube", COMET:"cone", SMALL_ASTEROID:"cube", BIG_ASTEROID:"sphere", PHA:"cube"}[bodyType]
		self.SizeCorrection = getSigmoid(self.Perihelion, sizeCorrection)

		if shape == "sphere":
			self.Look = sphere(pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]), radius=self.BodyRadius/self.SizeCorrection, make_trail=false)
			self.Angle = pi/2
		else:
			self.Look = ellipsoid(pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]), length=(self.BodyRadius * randint(1, 5))/self.SizeCorrection, height=(self.BodyRadius * randint(1, 5))/self.SizeCorrection, width=(self.BodyRadius * randint(1, 5))/self.SizeCorrection, make_trail=false)
			self.Angle = pi/randint(2,6)

		self.Trail = curve(color=self.Color)
		self.Trail.append(pos=self.Look.pos)

		if planets_data[index]["material"] <> 0:
			data = materials.loadTGA("./img/"+index)
		else:
			data = materials.loadTGA("./img/asteroid")

		self.Look.material = materials.texture(data=data, mapping="spherical", interpolate=False)
		self.Look.rotate(angle=self.Angle)

		# add LEGEND
		self.Label = label(pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]), text=self.Name, xoffset=20, yoffset=12, space=0, height=10, color=color, border=6, box=false, font='sans')
		if (self.solarsystem.SHOW_BODIES & bodyType) == 0:
			self.Look.visible = false
			self.Label.visible = false

		# initial velocity at perihelion
		self.InitialVelocity = self.getCurrentVelocity()

	def drawOrbit(self):
		#loop by 1 degree increment (math.pi/180)
		self.Trail.visible = false
		for theta in np.arange(self.nu, (2*math.pi)+(math.pi/180)+self.nu, math.pi/(180)):
			R = (self.a*(1 - self.e**2))/(1 + self.e*cos(theta))
			self.X = R*cos(theta)
			self.Y = R*sin(theta)
			self.updatePosition()
			rate(5000)

		if self.Look.visible:
			self.Trail.visible = true

	def updatePosition(self, trace = true):

		# rotate around lontitude of ascending node, inclinaison and argument of perhelion, all at once
		self.Position = self.Euler_3D_Rotation * np.matrix([[self.X*DIST_FACTOR],
																[self.Y*DIST_FACTOR],
																[self.Z*DIST_FACTOR]])

		self.Look.pos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])
		if trace:
			if self.Position[Z_COOR] < 0:
				self.Interval += 1
				if self.Interval % 2 == 0:
					self.Trail.append(pos=self.Look.pos, color=self.Color) #, interval=50)
				else:
					self.Trail.append(pos=self.Look.pos, color=color.black) #, interval=50)
			else:
				self.Trail.append(pos=self.Look.pos, color=self.Color)


	def refresh(self):
		#global AnimationInProgress #, currentSource #, SHOW_BODIES
		if self.solarsystem.AnimationInProgress and self.BodyType == self.solarsystem.currentSource:
			return

		if self.BodyType & self.solarsystem.SHOW_BODIES <> 0 or self.Name == 'Earth':
			if self.Look.visible == false:
				self.Look.visible = true
				self.Label.visible = true
				self.Trail.visible = true
				if self.Ring:
					self.InnerRing.visible = true
					self.OutterRing.visible = true
		else:
			self.Look.visible = false
			self.Label.visible = false
			self.Trail.visible = false
			if self.Ring:
				self.InnerRing.visible = false
				self.OutterRing.visible = false


	def getCurrentOrbitRadius(angle_in_rd):
		self.CurrRadius = (self.a * (1 - self.e**2))/(1 + cos(angle_in_rd))
		return self.CurrRadius

	def getCurrentVelocity(self):
		# the formulat is v^2 = GM(2/r - 1/a)
		return sqrt(G*SUN_M*((2/self.Distance) - (1/self.a)))

	def calculatePositionXX(self):
		self.X = self.Distance
		self.Velocity = sqrt((G * SUN_M)/self.Distance)
		#print self.Velocity



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


def animateXX(solarSystem):
	while true:
		#for time_incr in range[0, PLU_REV, 100*86400]:

		for body in solarSystem.bodies:
			body.dawTrajectory()
		#body.Velocity = vector(10e3, 10e3, 0)
		#body.getCurrentVelocity()
		#body.calculatePosition()

def refresh(solarSystem):
	for body in solarSystem.bodies:
		body.refresh()

def hideBelt(beltname):
	beltname.Look.visible = false
	beltname.Label.visible = false

def showBelt(beltname):
	beltname.Look.visible = true
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

def loadBodies(solarsystem, type, filename):
	fo  = open(filename, "r")
	MAX = 10000#1750
	token = []
	#try:
	for line in fo:
		if line[0] == '#':
			print line
		else:
			token = line.split('|')
			if len(token) > 0:
				planets_data[token[NEO_DESIGNATION]] = {"material": 	0,
													"name":			token[NEO_FULLNAME],
													"mass":			(float(token[NEO_GM])/G)*1.e+9 if token[NEO_GM] else 0, #5e13,
													"radius":		float(token[NEO_DIAMETER])/2 if token[NEO_DIAMETER] else 0, #2000,
													"perihelion":	float(token[NEO_DIST_OF_PERIHELION]) * AU,
													"e":	float(token[NEO_ECC]),
													"revolution":	float(token[NEO_ORBITAL_P])*86400,
													"orbital_inclinaison": float(token[NEO_INC]),
													"longitude_of_ascendingnode":float(token[NEO_LAN]),
													"argument_of_perihelion": float(token[NEO_AOP]),
													"longitude_of_perihelion":float(token[NEO_LAN])+float(token[NEO_AOP]),
													"time_of_perihelion_passage":float(token[NEO_TIME_OF_PERIHELION_PASSAGE_JED]),
													"earth_moid": (float(token[NEO_EARTH_MOID])*AU) if token[NEO_EARTH_MOID] else 0
													}

				solarsystem.addTo(makeBody(solarsystem, token[NEO_DESIGNATION], getColor(), 0, type))
				MAX = MAX - 1
				if MAX <= 0:
					break
	#except:
	print 10000 - MAX
	fo.close()

def main():
	solarsystem = solarSystem()
	solarsystem.SHOW_BODIES = INNERPLANET

	solarsystem.addTo(makeBody(solarsystem, 'mercury', color.green, 70))
	solarsystem.addTo(makeBody(solarsystem, 'venus', color.yellow, 0))
	solarsystem.addTo(makeBody(solarsystem, 'earth', color.cyan, 225))
	solarsystem.addTo(makeBody(solarsystem, 'mars', color.red, 0))
	solarsystem.addTo(makeBody(solarsystem, 'jupiter', color.magenta, 0, GASGIANT))
	solarsystem.addTo(makeBody(solarsystem, 'saturn', color.cyan, 20, GASGIANT))
	solarsystem.addTo(makeBody(solarsystem, 'uranus', color.yellow, 0, GASGIANT))
	solarsystem.addTo(makeBody(solarsystem, 'neptune', color.orange, 0, GASGIANT))

	solarsystem.makeRings(solarsystem, "saturn")

	# generate DWARF planets
	solarsystem.addTo(makeBody(solarsystem, 'eris', color.yellow, 0, DWARFPLANET))
	solarsystem.addTo(makeBody(solarsystem, 'pluto', color.green, 0, DWARFPLANET))
	solarsystem.addTo(makeBody(solarsystem, 'makemake', color.magenta, 0, DWARFPLANET))
	solarsystem.addTo(makeBody(solarsystem, 'sedna', color.orange, 0, DWARFPLANET))
	solarsystem.addTo(makeBody(solarsystem, 'haumea', color.white, 0, DWARFPLANET))

	# generate Belts
	solarsystem.addTo(makeBelt(solarsystem, 'kuiper', 'Kuiper Belt', KUIPER_BELT, color.cyan, 2, 4))
	solarsystem.addTo(makeBelt(solarsystem, 'asteroid', 'Asteroid Belt', ASTEROID_BELT, color.white, 2, 2))
	solarsystem.addTo(makeBelt(solarsystem, 'inneroort', 'Inner Oort Cloud', INNER_OORT_CLOUD, color.white, 2, 5))

	if SMALL_OBJECTS:
		# generate PHA, Big Asteroid and Comets
		loadBodies(solarsystem, PHA, "orbital elements of PHA with size greater than 100m.txt")
		loadBodies(solarsystem, BIG_ASTEROID,"orbital elements big asteroids.txt")
		loadBodies(solarsystem, COMET, "orbital elements comets.txt")

	solarsystem.drawAllBodiesTrajectory()

	# Start control window
	print wx.version()

	ex = wx.App()
	cw = controlWindow(None, solarsystem)

	while True:
		rate(2)

if __name__ == '__main__' :
	main()
