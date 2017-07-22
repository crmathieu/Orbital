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

import wx
import wx.lib.newevent

HEADING_Y = 20
DATE_Y = HEADING_Y
DATE_SLD_Y = DATE_Y + 20
INNER_Y = HEADING_Y + 20
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
AXIS_Y = LIT_Y + 20

REF_Y = AXIS_Y + 20
SLDS_Y = DATE_Y + 60

STRT_Y = SLDS_Y
PAU_Y = STRT_Y + 40
SIMU_Y = PAU_Y + 40
DET_Y = REF_Y + 60
ANI_Y = SIMU_Y + 120

date_elements = {
	"d_p_m" : {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:20, 12:31},
	"d_p_m_leap" : {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:20, 12:31},
	"d_to_m" :{1:0, 2:31, 3:59, 4:90, 5:120, 6:151, 7:181, 8:212, 9:243, 10:273, 11:304, 12:334},
	"d_to_m_leap" :{1:0, 2:31, 3:60, 4:91, 5:121, 6:152, 7:182, 8:213, 9:244, 10:274, 11:305, 12:335},
	"d_since_J2000":{1995:-1827.5, 1996: -1462.5, 1997: -1096.5, 1998: -731.5, 1999:-366.5, 2000:-1.5, 2001: 364.5, 2002: 729.5, 2003:1094.5, 2004:1459.5, 2005:1825.5}
}

def isLeapYear(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

class controlWindow(wx.Frame):

	def __init__(self, frame, solarsystem):

		wx.Frame.__init__(self, None)
		self.checkboxList = {}
		self.ResumeSlideShowLabel = False
		self.AnimationInProgress = False
		self.Source = PHA
		self.TimeIncrement = 1
		self.AnimLoop = 0
		self.SolarSystem = solarsystem
		self.todayDate = datetime.date.today()
		self.DeltaT = 0 # number of days from today - used for animation into future or past (detalT < 0)
		self.velocity = 0

		# Associate some events with methods of this class
		self.InitUI()

	def createCheckBox(self, panel, title, type, xpos, ypos):

		cb = wx.CheckBox(panel, label=title, pos=(xpos, ypos))
		if self.SolarSystem.ShowFeatures & type <> 0:
			cb.SetValue(True)
		else:
			cb.SetValue(False)
		self.checkboxList[type] = cb

	def InitUI(self):
		pnl = wx.Panel(self)

		self.BoldFont = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		self.RegFont = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
		heading = wx.StaticText(pnl, label='Show', pos=(20, HEADING_Y))
		heading.SetFont(self.BoldFont)
		dateLabel = wx.StaticText(pnl, label='Orbital Date', pos=(200, DATE_Y))
		dateLabel.SetFont(self.BoldFont)

		#self.today = wx.StaticText(pnl, label="", pos=(200, 20), size=(130, 25))
		#self.today.SetFont(self.RegFont)
		#self.today.Wrap(230)
		#self.today.SetLabel("Date: "+str(self.todayDate))

		self.dateMSpin = wx.SpinCtrl(pnl, id=wx.ID_ANY, initial=self.todayDate.month, min=1, max=12, pos=(200, DATE_SLD_Y), size=(65, 25), style=wx.SP_ARROW_KEYS)
		self.dateMSpin.Bind(wx.EVT_SPINCTRL,self.OnTimeSpin)

		self.dateDSpin = wx.SpinCtrl(pnl, id=wx.ID_ANY, initial=self.todayDate.day, min=1, max=31, pos=(265, DATE_SLD_Y), size=(65, 25), style=wx.SP_ARROW_KEYS)
		self.dateDSpin.Bind(wx.EVT_SPINCTRL,self.OnTimeSpin)

		# we need now to create a custom event in order to update the content of the day spinner if its value is out-of-range
		self.CustomEvent, EVT_RESET_SPINNER = wx.lib.newevent.NewEvent()
		self.dateDSpin.Bind(EVT_RESET_SPINNER, self.ResetSpinner) # bind it as usual
		# So, the day spinner has 2 events. one triggered when clicking on the arrow, and one
		# triggered programmatically to update the value of the day spinner in order to correct it
		# The firing of the EVT_RESET_SPINNER is programmatically done during the execution
		# of the EVT_SPINCTRL handler


		self.dateYSpin = wx.SpinCtrl(pnl, id=wx.ID_ANY, initial=self.todayDate.year, min=-3000, max=3000, pos=(330, DATE_SLD_Y), size=(65, 25), style=wx.SP_ARROW_KEYS)
		self.dateYSpin.Bind(wx.EVT_SPINCTRL,self.OnTimeSpin)

		self.ValidateDate = wx.Button(pnl, label='!', pos=(400, DATE_SLD_Y), size=(60, 25))
		self.ValidateDate.Bind(wx.EVT_BUTTON, self.OnValidateDate)


		self.createCheckBox(pnl, "Inner Planets", INNERPLANET, 20, INNER_Y)
		self.createCheckBox(pnl, "Orbits", ORBITS, 20, ORB_Y)
		self.createCheckBox(pnl, "Outter Planets", OUTTERPLANET, 20, GASG_Y)
		self.createCheckBox(pnl, "Dwarf Planets", DWARFPLANET, 20, DWARF_Y)
		self.createCheckBox(pnl, "Asteroids Belt", ASTEROID_BELT, 20, AB_Y)
		self.createCheckBox(pnl, "Jupiter Trojans", JTROJANS, 20, JT_Y)
		self.createCheckBox(pnl, "Kuiper Belt", KUIPER_BELT, 20, KB_Y)
		self.createCheckBox(pnl, "Inner Oort Cloud", INNER_OORT_CLOUD, 20, IOC_Y)
		self.createCheckBox(pnl, "Ecliptic", ECLIPTIC_PLANE, 20, ECL_Y)
		self.createCheckBox(pnl, "Labels", LABELS, 20, LABEL_Y)
		self.createCheckBox(pnl, "Lit Scene", LIT_SCENE, 20, LIT_Y)
		self.createCheckBox(pnl, "Referential", REFERENTIAL, 20, AXIS_Y)

		cbtn = wx.Button(pnl, label='Refresh', pos=(20, REF_Y))
		cbtn.Bind(wx.EVT_BUTTON, self.OnRefresh)

		lblList = ['PHA', 'Comets', 'Major Asteroids', 'Trans Neptunians']
		self.rbox = wx.RadioBox(pnl,label = 'Slideshow', pos = (200, SLDS_Y), choices = lblList ,majorDimension = 1, style = wx.RA_SPECIFY_COLS)
		self.rbox.SetFont(self.RegFont)
		self.rbox.Bind(wx.EVT_RADIOBOX,self.OnRadioBox)

		self.SlideShow = wx.Button(pnl, label='Start', pos=(360, SLDS_Y))
		self.SlideShow.Bind(wx.EVT_BUTTON, self.OnSlideShow)

		self.Pause = wx.Button(pnl, label='Pause', pos=(360, PAU_Y))
		self.Pause.Bind(wx.EVT_BUTTON, self.OnPauseSlideShow)
		self.Pause.Hide()

		self.sliderTitle = wx.StaticText(pnl, label="Anim. Speed x", pos=(200, ANI_Y), size=(60, 20))
		self.sliderTitle.SetFont(self.BoldFont)

		self.aniSpeed = wx.StaticText(pnl, label="1", pos=(315, ANI_Y), size=(15, 20))
		self.aniSpeed.SetFont(self.BoldFont)

		self.aniSlider = wx.Slider(pnl, id=wx.ID_ANY, value=1, minValue=-20, maxValue=20, pos=(195, ANI_Y+30), size=(150, 20), style=wx.SL_HORIZONTAL)
		self.aniSlider.Bind(wx.EVT_SLIDER,self.OnAnimSlider)

		self.Animate = wx.Button(pnl, label='>', pos=(360, ANI_Y), size=(40, 40))
		self.Animate.Bind(wx.EVT_BUTTON, self.OnAnimate)
		#self.Animate.Hide()

		self.Stepper = wx.Button(pnl, label='+', pos=(405, ANI_Y), size=(40, 40))
		self.Stepper.Bind(wx.EVT_BUTTON, self.OnStepper)

		INFO1_Y = DET_Y + 20
		INFO1_V = INFO1_Y + 75

		self.InfoTitle = wx.StaticText(pnl, label="", pos=(20, DET_Y))
		self.InfoTitle.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
		self.Info1 = wx.StaticText(pnl, label="", pos=(20, INFO1_Y))
		self.Info1.SetFont(self.RegFont)
		self.Info1.Wrap(230)
		self.Info2 = wx.StaticText(pnl, label="", pos=(240, INFO1_Y))
		self.Info2.SetFont(self.RegFont)
		self.Info2.Wrap(250)
		self.ObjVelocity = wx.StaticText(pnl, label="", pos=(305, INFO1_V), size=(130, 25))
		self.ObjVelocity.SetFont(self.RegFont)

		self.SetSize((500, INFO1_Y+180))
		self.SetTitle('Orbital Control')
		self.Centre()
		self.Show(True)

	def OnValidateDate(self, e):
		newdate = datetime.date(self.dateYSpin.GetValue(),self.dateMSpin.GetValue(),self.dateDSpin.GetValue())
		self.DeltaT = (newdate - self.todayDate).days
		self.OneTimeIncrement()
		self.disableBeltsForAnimation()
		self.DeltaT -= self.TimeIncrement
		self.refreshDate()

		if self.SolarSystem.SlideShowInProgress == True:
			self.ObjVelocity.SetLabel(str(round(self.velocity/1000, 2))+" km/s")

	def refreshDate(self):
		newdate = self.todayDate + datetime.timedelta(days = self.DeltaT)
		self.dateDSpin.SetValue(newdate.day)
		self.dateMSpin.SetValue(newdate.month)
		self.dateYSpin.SetValue(newdate.year)

		if self.SolarSystem.SlideShowInProgress == True:
			self.ObjVelocity.SetLabel(str(round(self.velocity/1000, 2))+" km/s")

	def disableBeltsForAnimation(self):
		self.checkboxList[JTROJANS].SetValue(False)
		self.checkboxList[ASTEROID_BELT].SetValue(False)
		self.checkboxList[KUIPER_BELT].SetValue(False)
		self.SolarSystem.ShowFeatures = (self.SolarSystem.ShowFeatures & ~(JTROJANS|ASTEROID_BELT|KUIPER_BELT))
		glbRefresh(self.SolarSystem, self.AnimationInProgress)

	def enableBelts(self):
		self.SolarSystem.addJTrojans(makeJtrojan(self.SolarSystem, 'jupiterTrojan', 'Jupiter Trojans', JTROJANS, color.green, 2, 5, 'jupiter'))

	def OnRadioBox(self, e):
		index = self.rbox.GetSelection()
		self.Source = {0: PHA, 1: COMET, 2:BIG_ASTEROID, 3:TRANS_NEPT}[index]
		self.SolarSystem.currentSource = self.Source

	def OnAnimSlider(self, e):
		self.TimeIncrement = self.aniSlider.GetValue()
		self.aniSpeed.SetLabel(str(self.TimeIncrement))
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
			# wxPyhton disable the event attached to the handler causing the update.
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
			self.enableBelts()
		else:
			self.checkboxList[JTROJANS].SetValue(False)
			self.checkboxList[ASTEROID_BELT].SetValue(False)
			self.checkboxList[KUIPER_BELT].SetValue(False)

		for type, cbox in self.checkboxList.iteritems():
			if cbox.GetValue() == True:
				self.SolarSystem.ShowFeatures |= type
			else:
				self.SolarSystem.ShowFeatures = (self.SolarSystem.ShowFeatures & ~type)


		glbRefresh(self.SolarSystem, self.AnimationInProgress)

	def OnPauseSlideShow(self, e):
		self.AnimationInProgress = False

		if self.ResumeSlideShowLabel == True:
			e.GetEventObject().SetLabel("Pause")
			self.ResumeSlideShowLabel = False
		else:
			e.GetEventObject().SetLabel("Resume")
			self.ResumeSlideShowLabel = True

	def OnSlideShow(self, e):
		self.AnimationInProgress = False
		if self.SolarSystem.SlideShowInProgress:
			# click on the Stop button
			self.SolarSystem.AbortSlideShow = True
			self.ResumeSlideShowLabel = False
			# reset label as 'Start'
			e.GetEventObject().SetLabel("Start")
			self.InfoTitle.SetLabel('')
			self.Info1.SetLabel('')
			self.Info2.SetLabel('')
			self.ObjVelocity.SetLabel('')
			self.Pause.SetLabel("Pause")
			self.Pause.Hide()
			return
		else:
			# click on the start button
			self.SolarSystem.SlideShowInProgress = True
			self.Pause.Show()
			# reset label as 'Stop'
			self.SlideShow.SetLabel("Stop")

		# loop through each body. If the bodyType matches what the Animation
		# is about,
		for body in self.SolarSystem.bodies:
			if body.BodyType == self.Source: #PHA:
				glbRefresh(self.SolarSystem, self.AnimationInProgress)
				self.InfoTitle.SetLabel(body.Name)

				self.velocity = body.animate(self.DeltaT)
				mass = str(body.Mass)+" kg" if body.Mass <> 0 else "Not Provided"
				radius = str(body.BodyRadius)+" km" if body.BodyRadius <> 0 and body.BodyRadius <> DEFAULT_RADIUS else "Not Provided"
				moid = str(body.Moid/1000)+" km" if body.Moid <> 0 else "N/A"
				rev = str(body.Revolution / 365.25)

				self.Info1.SetLabel("i  : "+str(body.Inclinaison)+" deg\nN : "+str(body.Longitude_of_ascendingnode)+" deg\nw : "+str(body.Argument_of_perihelion)+" deg\ne : "+str(body.e)+"\nq : "+str(body.Perihelion/1000)+" km")
				self.Info2.SetLabel("Mass : "+mass+"\nRadius : "+radius+"\nPeriod: "+rev+" yr"+"\nMoid :"+moid+"\nVelocity: ") #)+self.velocity)
				self.refreshDate()

				body.BodyShape.visible = True
				for i in range(len(body.Labels)):
					body.Labels[i].visible = True
				body.Trail.visible = True

				sleep(2)

				while (self.ResumeSlideShowLabel and self.SolarSystem.AbortSlideShow == False):
					sleep(1)

				body.BodyShape.visible = False
				for i in range(len(body.Labels)):
					body.Labels[i].visible = False

				body.Trail.visible = False
				if self.SolarSystem.AbortSlideShow:
					self.SolarSystem.AbortSlideShow = False
					self.SolarSystem.SlideShowInProgress = False
					return

		self.SolarSystem.SlideShowInProgress = False
		self.Pause.Hide()
		self.SlideShow.SetLabel("Start")
		self.InfoTitle.SetLabel('')
		self.Info1.SetLabel('')
		self.Info2.SetLabel('')
		self.ObjVelocity.SetLabel('')

	def OnStepper(self, e):
		self.StepByStep = True
		self.disableBeltsForAnimation()
		self.AnimationInProgress = False
		self.OneTimeIncrement()

	def OneTimeIncrement(self):
		self.DeltaT += self.TimeIncrement
		self.refreshDate()
		for body in self.SolarSystem.bodies:
			if body.BodyType in [OUTTERPLANET, INNERPLANET, ASTEROID, COMET, DWARFPLANET, PHA, BIG_ASTEROID, TRANS_NEPT]:
				if body.BodyShape.visible == True:
					velocity = body.animate(self.DeltaT)
					if body.BodyType == self.Source:
						self.velocity = velocity

		sleep(1e-4)


	def OnAnimate(self, e):
		self.StepByStep = False
		if self.AnimationInProgress == True:
			return

		self.disableBeltsForAnimation()
		self.AnimationInProgress = True
		while self.AnimationInProgress:
			self.OneTimeIncrement()
