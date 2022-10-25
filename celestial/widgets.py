from celestial.utils import getAngleBetweenVectors, getOrthogonalVector, getVectorOrthogonalToPlane, getXYprojection, getYZprojection
from orbit3D import *
from vpython_interface import ViewPort, Color
from visual import *
from utils import deg2rad
#from objects import circle
from location import locList
from video import *
import rate_func

class makePlanetWidgets():

    ROT_CLKW = 64
    ROT_CCLKW = 128

    def __init__(self, planet):

        self.Planet = planet
        self.Origin = planet.Origin
        self.visible = True
        self.makeOverlayRef()
        self.makePCPFref()
        self.makePCIref()
        self.makeECSSref()
        self.Eq = self.eqPlane = self.Lons = self.Lats = None

        self.Psi = 0.0
        self.NumberOfSiderealDaysPerYear = 0.0
        self.SiderealCorrectionAngle = 0.0
        self.zoomToLocation = False
        self.Loc = []
        self.initWidgets()


    def makePCPFref(self):
        # this is the PCPF referential or GeoCentric referential 
        # The "Earth-centered, Earth-fixed coordinate system": fixed to the earth (moves with its rotation)
        # is a cartesian spatial reference system that represents locations in the vicinity of the 
        # Earth (including its surface, interior, atmosphere, and surrounding outer space) as X, Y, and Z 
        # measurements from its center of mass. Its most common use is in tracking the orbits of 
        # satellites and in satellite navigation systems for measuring locations on the surface of the 
        # Earth, but it is also used in applications such as tracking crustal motion.
        # 
        # The distance from a given point of interest to the center of Earth is called the geocentric 
        # distance, R = (X2 + Y2 + Z2)0.5, which is a generalization of the geocentric radius, R0, not 
        # restricted to points on the reference ellipsoid surface. The geocentric altitude is a type of 
        # altitude defined as the difference between the two aforementioned quantities: h'= R-R0  
        # it is not to be confused for the geodetic altitude.
        #
        # Conversions between PCPF and geodetic coordinates (latitude and longitude) are discussed at 
        # geographic coordinate conversion. 

        #self.PCPF = frame()     
        #self.PCPF.pos = self.Planet.Origin.pos
        
        #### self.PCPF = make3DaxisReferential(self.Planet, tilt=True, color=Color.red)
        #### self.PCPF.referential.rotate(angle=(-self.Planet.TiltAngle), axis=self.PCPF.XdirectionUnit) #, origin=(0,0,0))
        
        self.PCPF = self.Planet.PCPF # has been done already 
        #self.PCPF.display(True)

    def makePCIref(self):
		# The PCI referential (the "Earth-Centered Inertial" is fixed to the stars, in other words, 
		# it doesn't rotate with the earth). PCI coordinate frames have their origins at the center of mass of Earth 
		# and are fixed with respect to the stars. "I" in "PCI" stands for inertial (i.e. "not accelerating"), in 
		# contrast to the "Earth-centered - Earth-fixed" (PCPF) frames, which remains fixed with respect to 
		# Earth's surface in its rotation, and then rotates with respect to stars.
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

        #self.PCI = frame() #self.Planet.PCI   
        #self.PCI.pos = self.Planet.Origin.pos

        #self.PCI = make3DaxisReferential(self.Planet, tilt=True)
        self.PCI = self.Planet.PCI # has been done already 
        #self.PCI.referential.rotate(angle=(-self.Planet.TiltAngle), axis=self.PCI.XdirectionUnit)

    def makeECSSref(self):

        # The ECSS referential (the "Earth-Centered Sun Synchronous") always has its x-axis
        # tangent to the earth orbit and its y-axis pointing towards the sun. Its z-axis
        # is always aligned with the ecliptic's z-axis
        self.ECSS = make3DaxisReferential({
            'body': self.Planet,
            'radius': 0,
            'tiltangle': 0,
            'show':	False,
            'color': Color.yellow,
            'ratio': [1,1,1],
            'legend': ["tg","orth","z"],
   			'make_axis': True
        })
        self.ECSS.setAxisTilt() #initiateReferentialTilt()
        #def  __init__(self, body, radius, tiltAngle, show = False, color = Color.white, ratio = [1,1,1], legend = ["x", "y", "z"], axisLock = False):

        """
        self.ECSS = frame()     
        self.ECSS.pos = self.Planet.Origin.pos
        self.Axis = [None,None,None]
        self.radius = (self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType])*0.999
        """

        # compute rotation
        self.ECSSangle = atan2(self.Planet.Position[1], self.Planet.Position[0])
#        self.ECSS.referential.rotate(angle=(pi/2 + self.ECSSangle), axis=(0,0,self.ECSS.Axis[2])) #self.Planet.SolarSystem.ZdirectionUnit)
#        self.ECSS.referential.rotate(angle=(pi/2 + self.ECSSangle), axis=(0,0,self.ECSS.ZdirectionUnit)) #self.Planet.SolarSystem.ZdirectionUnit)

        self.ECSS.referential.rotate(angle=(self.ECSSangle + pi/2), axis=self.ECSS.ZdirectionUnit) #self.Planet.SolarSystem.ZdirectionUnit)

        #self.ECSS.referential.rotate(angle=(self.ECSSangle), axis=self.ECSS.ZdirectionUnit) #self.Planet.SolarSystem.ZdirectionUnit)

        self.ECSS.display(False)
        return 

        pos = vector(self.ECSS.pos)
        directions = [vector(2*self.radius,0,0), vector(0,2*self.radius,0), vector(0,0,2*self.radius)]

        for i in [0,1,2]:
            self.Axis[i] = simpleArrow(Color.white, 0, 20, self.ECSS.pos, axisp = directions[i])
            self.Axis[i].display(True)


    def makeOverlayRef(self):
        # the overlay referential will display all the earth's widgets:
        # meridians, latitudes, earth locations, analemma etc...
        self.OVRL = frame()

        # link the overlay to earth's PCPF referential that rotates with the earth,
        # so that the widgets rotation will happen through the PCPF ref
        self.OVRL.frame = self.Planet.PCPF.referential
        self.OVRL.pos = (0,0,0)

    def resetWidgetsRefFromSolarTime(self):

        print "RESET WIDGET FROM SOLAR-TIME"
        if self.SiderealCorrectionAngle != 0.0:
            self.OVRL.rotate(angle=(-self.SiderealCorrectionAngle), axis=self.Planet.RotAxis) #, origin=(0,0,0))
            #self.Origin.rotate(angle=(-self.SiderealCorrectionAngle), axis=self.Planet.RotAxis) #, origin=(0,0,0))
            self.SiderealCorrectionAngle = 0.0

        print "Planet.Psi ....... ", self.Planet.Psi
        print "widgets.Psi ...... ", self.Psi
        self.OVRL.rotate(angle=(self.Planet.Psi-self.Psi), axis=self.Planet.RotAxis) #, origin=(0,0,0))
#        self.Origin.rotate(angle=(self.Planet.Psi-self.Psi), axis=self.Planet.RotAxis) #, origin=(0,0,0))


        # Psi is the initial rotation to apply on the sphere texture to match the solar Time
        self.Psi = self.Planet.Psi
        print "resetWidgetsRefFromSolarTime: Psi =", self.Psi


    def resetWidgetsReferencesFromNewDate(self): #, fl_diff_in_days):
        print "RESET WIDGETS REF"
        if self.SiderealCorrectionAngle != 0.0:
            # there has been a previous manual reset of the UTC date which has resulted in a sidereal 
            # correction. We need to undo it prior to reposition the texture for the new date
            self.OVRL.rotate(angle=(-self.SiderealCorrectionAngle), axis=self.Planet.RotAxis)
#            self.Origin.rotate(angle=(-self.SiderealCorrectionAngle), axis=self.Planet.RotAxis)

        self.SiderealCorrectionAngle = self.Planet.SiderealCorrectionAngle #(2 * pi / self.NumberOfSiderealDaysPerYear) * fl_diff_in_days
        self.OVRL.rotate(angle=(self.SiderealCorrectionAngle), axis=self.Planet.RotAxis) #, origin=(0,0,0))
#        self.Origin.rotate(angle=(self.SiderealCorrectionAngle), axis=self.Planet.RotAxis) #, origin=(0,0,0))

    def initWidgets(self):
        self.NumberOfSiderealDaysPerYear = self.Planet.NumberOfSiderealDaysPerYear
        self.Eq = makeEquator(self)
        self.Tr = makeTropics(self)
        self.EqPlane = makeEquatorialPlane(self, Color.orange, opacity=self.Planet.Opacity)
        self.Lons = makeLongitudes(self)
        self.Lats = makeLatitudes(self)
        self.tz = makeTimezones(self)
        self.Loc = []
        self.currentLocation = -1
        self.defaultLocation = -1
        #self.makeLocation(TZ_US_CAPE)
        self.makeMultipleLocations(locList.TZ_US_CAPE)
         
        # align widgets origin with planet tilt
        #self.PCPF.rotate(angle=(-self.Planet.TiltAngle), axis=self.Planet.XdirectionUnit) #, origin=(0,0,0))

        # align longitude to greenwich when the planet is Earth
        if self.Planet.Name.lower() == EARTH_NAME:

            # adjust widgets positions in relation with earth texture at current time
            ##### self.resetWidgetsRefFromSolarTime()
             
            # align GMT: the initial position of the GMT meridian on the texture is 6 hours
            # off its normal position. Ajusting by 6 hours x 15 degres = 90 degres
            #### self.PCPF.referential.rotate(angle=(deg2rad(6*15)), axis=self.Planet.RotAxis) #ZdirectionUnit)
            self.OVRL.rotate(angle=(deg2rad(6*15)), axis=(0,0,1)) #self.Planet.PCPF.ZdirectionUnit) #ZdirectionUnit)
            
            # init position in ecliptic referential
            #self.updateCurrentLocationEcliptic()
            if self.currentLocation >= 0:
                self.Loc[self.currentLocation].updateEclipticPosition()

            #### -> self.AnaLemma = makeAnalemma(self, locList.TZ_NORTH_P) #TZ_US_KOD) #TZ_US_COUVE)
    

    """
    def shiftFocus(self, dest, long_angle, lat_angle, long_direction, lat_direction, axis = (0,0,1), ratefunc = rate_func.ease_in_out):
        # going from current location to next destination location coordinates
        #print ("SHIFT-FOCUS: angle=", long_angle)

        # (Xc, Yc, Zc) is the current location of camera (before transition)
        Xc = self.Planet.SolarSystem.Scene.center[0]
        Yc = self.Planet.SolarSystem.Scene.center[1]
        Zc = self.Planet.SolarSystem.Scene.center[2]
        #print ("Xc=", Xc, ", Yc=", Yc,", Zc=", Zc)
        
        # calculate distance between current location and 
        # destination for each coordinate 
        deltaX = (dest[0] - Xc)
        deltaY = (dest[1] - Yc)
        deltaZ = (dest[2] - Zc)

        #print ("X=", deltaX, ", Y=", deltaY,", Z=", deltaZ)

        if self.Planet.SolarSystem.Dashboard.orbitalTab.RecorderOn == True:
            if self.Planet.SolarSystem.Dashboard.orbitalTab.VideoRecorder == None:
                self.Planet.SolarSystem.Dashboard.orbitalTab.VideoRecorder = setVideoRecording(framerate = 20, filename = "output.avi")


        # Calculate number of steps based on current transition velocity factor (default is 1.0)
        total_steps = int(100) * self.Planet.SolarSystem.camera.transitionVelocityFactor
        #print ("Smooth Focus TOTAL_STEPS=", total_steps)

        # move scene center by an increment towards the destination coordinates. Since 
        # we use 100 * transitionVelocityFactor steps to do that, and our rate function 
        # only takes an input between 0 and 1, we divide the current increment by the 
        # total number of steps to always keep the rate function input between these limits.
        # Incremental location is calculated as the initial location + difference between initial
        # and final locations time the rate for this particular step.

        lg_rangle = deg2rad(long_angle) * (-1 if long_direction == self.ROT_CLKW else 1)
        lg_dangle = 0.0

        lat_axis = 1
        if lat_angle < 0:
            lat_axis = -1
            lat_angle = - lat_angle

        la_rangle = deg2rad(lat_angle)* (-1 if lat_direction == self.ROT_CLKW else 1)
        la_dangle = 0.0

        for i in np.arange(0, total_steps+1, 1):
            # incrementally, change center focus and rotate
            r = ratefunc(float(i)/total_steps)
            self.Planet.SolarSystem.Scene.center = vector( (Xc + r*deltaX),
                                                    (Yc + r*deltaY),
                                                    (Zc + r*deltaZ))

            lg_iAngle = lg_rangle * r
            la_iAngle = la_rangle * r
            self.Planet.SolarSystem.Scene.forward = rotate(self.Planet.SolarSystem.Scene.forward, angle=(lg_iAngle-lg_dangle), axis=(0,0,1)) #(0,0,1))
            self.Planet.SolarSystem.Scene.forward = rotate(self.Planet.SolarSystem.Scene.forward, angle=(la_iAngle-la_dangle), axis=(lat_axis,0,0)) #(0,0,1))
            lg_dangle = lg_iAngle
            la_dangle = la_iAngle

            sleep(2e-2)
            if self.Planet.SolarSystem.Dashboard.orbitalTab.RecorderOn == True:
                recOneFrame(self.Planet.SolarSystem.Dashboard.orbitalTab.VideoRecorder)


#################
#  		rangle = deg2rad(angle) * (-1 if direction == self.ROT_CLKW else 1)
#		dangle = 0.0
#		for i in np.arange(0, total_steps+1, 1):
#			r = ease_in_out(float(i)/total_steps)
#			iAngle = rangle * r
#			self.view.forward = rotate(self.view.forward, angle=(iAngle-dangle), axis=axis)
#			dangle = iAngle
#			sleep(1e-2)

          
    def gotoVerticalXX(self, locationID, ratefunc = rate_func.ease_in_out_sine):

        self.Loc[self.defaultLocation].updateEclipticPosition()
        nextPos = self.Loc[locationID].getGeoPosition()

        if False:
            self.C =  simpleArrow(Color.yellow, 0, 20, self.Loc[self.defaultLocation].getEclipticPosition(), axisp = 0.1*vector(x,y,z), context = self.Loc[locationID].Origin) #, context = self.Planet.Origin) #self.Loc[self.defaultLocation].Origin)
            self.C =  simpleArrow(Color.yellow, 0, 20, self.Planet.SolarSystem.Scene.mouse.camera, axisp = 1e4*self.Planet.SolarSystem.Scene.forward, context = None) #self.Loc[locationID].Origin) #, context = self.Planet.Origin) #self.Loc[self.defaultLocation].Origin)
            self.C.display(True)

            ortho = getOrthogonalVector(self.Planet.SolarSystem.Scene.forward)
            self.C =  simpleArrow(Color.red, 0, 20, self.Planet.SolarSystem.Scene.mouse.camera, axisp = 1e4*ortho, context = None) #self.Loc[locationID].Origin)
            self.C.display(True)
            x = self.Planet.SolarSystem.Scene.forward[0]
            y = self.Planet.SolarSystem.Scene.forward[1]
            z = self.Planet.SolarSystem.Scene.forward[2]
            print "(XF,YF,ZF)=(",x,",",y,",",z,")"

            self.C =  simpleArrow(Color.red, 0, 20, curPos, axisp = 20*vector(x,y,z), context = self.Planet.Origin) #, context = self.Loc[self.defaultLocation].Origin)
            self.C.display(True)


        self.V =  simpleArrow(Color.green, 0, 20, nextPos, axisp = self.Loc[locationID].Grad/10, context = self.Loc[locationID].Origin) #self.Loc[self.defaultLocation].Origin)
        self.V.display(True)

        EC = self.Loc[locationID].getEclipticPosition()
        A = EC[0] - self.Planet.Origin.pos[0] #self.Planet.Origin.pos[0]
        B = EC[1] - self.Planet.Origin.pos[1] #self.Planet.Origin.pos[1]
        C = EC[2] - self.Planet.Origin.pos[2] #self.Planet.Origin.pos[2] 

        #self.D =  simpleArrow(Color.white, 0, 20, self.Planet.Origin.pos, axisp = 5*vector(A,B,C), context = None) #self.Loc[locationID].Origin) #self.Loc[self.defaultLocation].Origin)
        #self.D.display(True)

        # (Xc, Yc, Zc) is the current location of camera (before transition)
        Xc = self.Planet.SolarSystem.Scene.center[0]
        Yc = self.Planet.SolarSystem.Scene.center[1]
        Zc = self.Planet.SolarSystem.Scene.center[2]
        
        dest = self.Loc[locationID].getEclipticPosition()
        # calculate distance between current location and 
        # destination for each coordinate 
        deltaX = (dest[0] - Xc)
        deltaY = (dest[1] - Yc)
        deltaZ = (dest[2] - Zc)

        #print ("X=", deltaX, ", Y=", deltaY,", Z=", deltaZ)

        if self.Planet.SolarSystem.Dashboard.orbitalTab.RecorderOn == True:
            if self.Planet.SolarSystem.Dashboard.orbitalTab.VideoRecorder == None:
                self.Planet.SolarSystem.Dashboard.orbitalTab.VideoRecorder = setVideoRecording(framerate = 20, filename = "output.avi")

        # Calculate number of steps based on current transition velocity factor (default is 1.0)
        total_steps = int(100) * self.Planet.SolarSystem.camera.transitionVelocityFactor
        #print ("Smooth Focus TOTAL_STEPS=", total_steps)

        #dX = (self.Planet.SolarSystem.Scene.forward[0] - A)
        #dY = (self.Planet.SolarSystem.Scene.forward[1] - B)
        #dZ = (self.Planet.SolarSystem.Scene.forward[2] - C)
        Initial = -self.Planet.SolarSystem.Scene.forward


        rotAxis = getVectorOrthogonalToPlane(Initial, vector(A,B,C))
        self.K =  simpleArrow(Color.cyan, 0, 20, self.Planet.SolarSystem.Scene.mouse.camera, axisp = 1e4*rotAxis, context = None) #self.Loc[locationID].Origin)
        self.K.display(True)

        rotAngle = deg2rad(getAngleBetweenVectors(Initial, vector(A,B,C)))
        print "Rot Angle is", rotAngle, "radians", "-initial=",deg2rad(getAngleBetweenVectors(-Initial, vector(A,B,C)))
        print "Rot Axis is", rotAxis
        
        accumulated_rot = 0.0
        for i in np.arange(0, total_steps+1, 1):
            # incrementally, change center focus and rotate
            r = ratefunc(float(i)/total_steps)
            self.Planet.SolarSystem.Scene.center = vector( (Xc + r*deltaX),
                                                    (Yc + r*deltaY),
                                                    (Zc + r*deltaZ))

            iAngle = rotAngle * r

            self.Planet.SolarSystem.Scene.forward = rotate(self.Planet.SolarSystem.Scene.forward, angle=(iAngle-accumulated_rot), axis=rotAxis)
            accumulated_rot = iAngle

            sleep(2e-2)
            if self.Planet.SolarSystem.Dashboard.orbitalTab.RecorderOn == True:
                recOneFrame(self.Planet.SolarSystem.Dashboard.orbitalTab.VideoRecorder)


        return
        lg_rangle = deg2rad(Hangle) #* (-1 if long_direction == self.ROT_CLKW else 1)
        lg_dangle = 0.0

        lat_axis = 1
        #if lat_angle < 0:
        #    lat_axis = -1
        #    lat_angle = - lat_angle

        la_rangle = deg2rad(Vangle) #* (-1 if lat_direction == self.ROT_CLKW else 1)
        la_dangle = 0.0rotatemakePCI
        return 

        for i in np.arange(0, total_steps+1, 1):
            # incrementally, change center focus and rotate
            r = ratefunc(float(i)/total_steps)
            self.Planet.SolarSystem.Scene.center = vector( (Xc + r*deltaX),
                                                    (Yc + r*deltaY),
                                                    (Zc + r*deltaZ))

            lg_iAngle = lg_rangle * r
            la_iAngle = la_rangle * r
            self.Planet.SolarSystem.Scene.forward = rotate(self.Planet.SolarSystem.Scene.forward, angle=(lg_iAngle-lg_dangle), axis=(0,0,1)) #(0,0,1))
            self.Planet.SolarSystem.Scene.forward = rotate(self.Planet.SolarSystem.Scene.forward, angle=(la_iAngle-la_dangle), axis=(lat_axis,0,0)) #(0,0,1))
            lg_dangle = lg_iAngle
            la_dangle = la_iAngle

            sleep(2e-2)
            if self.Planet.SolarSystem.Dashboard.orbitalTab.RecorderOn == True:
                recOneFrame(self.Planet.SolarSystem.Dashboard.orbitalTab.VideoRecorder)

#############


    def shiftLocation(self, locationID):

        if self.currentLocation == -1:
            print "Auto shifting to default location ..."
            self.Planet.SolarSystem.Dashboard.widgetTab.centerToDefaultLocation()

        # set current and next coordinates in PCI referential

        curPos = self.Loc[self.defaultLocation].getGeoPosition()
        nextPos = self.Loc[locationID].getGeoPosition()

        # calculate angle between normal of camera location and normal vector in next location. 
        # Here (x,y,z) is the vector between camera location and center of earth
        
        x = self.Planet.SolarSystem.Scene.mouse.camera[0] - self.Planet.Origin.pos[0]
        y = self.Planet.SolarSystem.Scene.mouse.camera[1] - self.Planet.Origin.pos[1]
        z = self.Planet.SolarSystem.Scene.mouse.camera[2] - self.Planet.Origin.pos[2] 

        long_diff = getAngleBetweenVectors(self.Loc[locationID].Grad, -vector(x,y,z))

        self.B =  simpleArrow(Color.green, 0, 20, nextPos, axisp = self.Loc[locationID].Grad/10, context = self.Loc[locationID].Origin) #self.Loc[self.defaultLocation].Origin)
        self.B.display(True)

        if False:
            self.Z =  simpleArrow(Color.magenta, 20, 20, self.Planet.Origin.pos, axisp = vector(x,y,z), context =None)
            if self.Z != None:
                self.Z.display(True)

            self.A =  simpleArrow(Color.yellow, 0, 20, nextPos, axisp = self.Loc[self.defaultLocation].Grad/10, context = self.Loc[self.defaultLocation].Origin) #self.Loc[self.defaultLocation].Origin)
            self.A.display(True)
            self.B =  simpleArrow(Color.green, 0, 20, nextPos, axisp = self.Loc[locationID].Grad/10, context = self.Loc[locationID].Origin) #self.Loc[self.defaultLocation].Origin)
            self.B.display(True)

            # calculate angle between (x,y,z) and default location Nomal vector
            # angleA = getAngleBetweenVectors(self.Loc[self.defaultLocation].Grad, -vector(x,y,z))
            #print "Angle between ", self.Loc[self.defaultLocation].Name, " and camera:", angleA

            # zoom out
            #### self.Planet.SolarSystem.camera.cameraZoom(duration = 1, velocity = 10, recorder = False, zoom = self.Planet.SolarSystem.camera.ZOOM_OUT)
            # refocus smoothly from current location to planet center
            #self.Planet.SolarSystem.Dashboard.focusTab.smoothFocus2target(self.Planet.Origin.pos) #, ratefunc=rate_func.ease_in_quad) #, ratefunc = rate_func.ease_in_quad)

            # calculate angle between camera location Normal and new location normal
            #### angle = getAngleBetweenVectors(-self.Planet.SolarSystem.camera.view.forward, self.Loc[locationID].Grad)
        ### angle = getAngleBetweenVectors(-vector(x,y,z), self.Loc[locationID].Grad)
        
            ### angle = getAngleBetweenVectors(self.Loc[self.defaultLocation].Grad, self.Loc[locationID].Grad)
        
            #print "Angle between", self.Loc[self.defaultLocation].Name, " and ", self.Loc[locationID].Name, "=", angle
            #print "ALTERNATE METHOD gives:", self.Loc[locationID].long - self.Loc[self.defaultLocation].long

        self.Loc[locationID].updateEclipticPosition()
        clg = self.Loc[self.defaultLocation].long
        nlg = self.Loc[locationID].long

        lg_direction = 0
        angle = 0
        if clg < 0:
            if nlg >= 0:
                angle = nlg + abs(clg)
                lg_direction = self.ROT_CCLKW
            else:
                angle = abs(clg-nlg)
                lg_direction = self.ROT_CCLKW if nlg > clg else self.ROT_CLKW
        else:
            if nlg >= 0:
                angle = abs(clg-nlg)
                lg_direction = self.ROT_CCLKW if nlg > clg else self.ROT_CLKW
            else:
                angle = clg + abs(nlg)
                lg_direction = self.ROT_CCLKW
        long_diff = angle

        cla = self.Loc[self.defaultLocation].lat
        nla = self.Loc[locationID].lat
        if cla < 0:
            if nla >= 0:
                aangle = nla + abs(cla)
                la_direction = self.ROT_CCLKW
            else:
                angle = abs(cla-nla)
                la_direction = self.ROT_CCLKW if nla > cla else self.ROT_CLKW
        else:
            if nla >= 0:
                angle = abs(cla-nla)
                la_direction = self.ROT_CCLKW if nla > cla else self.ROT_CLKW
            else:
                angle = cla + abs(nla)
                la_direction = self.ROT_CCLKW

        lat_diff = angle
        #lat_diff = self.Loc[locationID].lat - self.Loc[self.defaultLocation].lat

        if self.zoomToLocation == True:
            self.Planet.SolarSystem.camera.cameraZoom(duration = 1, velocity = 10, recorder = False, zoom = self.Planet.SolarSystem.camera.ZOOM_OUT)
            self.zoomToLocation = False

#        self.shiftFocus(self.Loc[locationID].getEclipticPosition(), ((angle+angleA)*1.5) % 180, lat_angle, direction = direction, axis=vector(0,0,1))#, ratefunc = rate_func.ease_in_quad_mirror) #, axis=vector(xA, yA, zA)) #, ratefunc = rate_func.ease_in_quad_mirror)
####        self.shiftFocus(self.Loc[locationID].getEclipticPosition(), long_diff, lat_diff, direction = direction, axis=vector(0,0,1))#, ratefunc = rate_func.ease_in_quad_mirror) #, axis=vector(xA, yA, zA)) #, ratefunc = rate_func.ease_in_quad_mirror)
        self.shiftFocus(self.Loc[locationID].getEclipticPosition(), long_diff, lat_diff, long_direction = lg_direction, lat_direction = la_direction, axis=vector(0,0,1))#, ratefunc = rate_func.ease_in_quad_mirror) #, axis=vector(xA, yA, zA)) #, ratefunc = rate_func.ease_in_quad_mirror)
        print "LONG_DIFF=", long_diff, ", LAT_DIFF", lat_diff
        self.defaultLocation = locationID

        #### self.Planet.SolarSystem.Dashboard.focusTab.smoothFocus2target(self.Loc[locationID].getEclipticPosition())
        self.Planet.SolarSystem.camera.cameraZoom(duration = 1, velocity = 10, recorder = False, zoom = self.Planet.SolarSystem.camera.ZOOM_IN)
        self.zoomToLocation = True

        # rotate camera direction by the same angle
        #self.Planet.SolarSystem.camera.cameraRotateRight(angle, False)

        return
    """

    def makeMultipleLocations(self, defaultLoc_idx):
        self.defaultLocation = defaultLoc_idx
        #self.currentLocation = defaultLoc
        for i in np.arange(0, len(self.Planet.SolarSystem.locationInfo.tzEarthLocations), 1):
            self.Loc.append(makeEarthLocation(self, i))

    def makeLocation(self, locIndex):
        self.defaultLocation = locIndex # 0
        #self.currentLocation = 0
        self.Loc.append(makeEarthLocation(self, locIndex))

    def update_PCPF_RotationXX(self):
        # here the widgets rotates by the same amount the earth texture is rotated
        ti = self.Planet.SolarSystem.getTimeIncrement()
        RotAngle = (2*pi/self.Planet.Rotation)*ti

        # if polar axis inverted, reverse rotational direction
        if self.PCPF.ZdirectionUnit[2] < 0:
            RotAngle *= -1

        # follow planet rotation
        self.PCPF.referential.rotate(angle=RotAngle, axis=self.Planet.RotAxis, origin=self.PCPF.referential.pos) #(self.Position[0]+self.Foci[0],self.Position[1]+self.Foci[1],self.Position[2]+self.Foci[2]))

    def update_ECSS_Rotation(self):
        angle = atan2(self.Planet.Position[1], self.Planet.Position[0])
        self.ECSS.referential.rotate(angle=(angle-self.ECSSangle), axis=self.ECSS.ZdirectionUnit)
        self.ECSSangle = angle


    def update_PCI_PCPF_ECSS_Position(self):
        self.ECSS.referential.pos = self.PCPF.referential.pos = self.PCI.referential.pos = self.Planet.Origin.pos
###        self.ECSS.referential.pos = self.Planet.Origin.pos

    def updateCurrentLocationEcliptic(self):
        if self.currentLocation >= 0: 
            self.Loc[self.currentLocation].updateEclipticPosition()

    def updateCurrentLocationAnalemma(self):
        if self.currentLocation >= 0: 
            self.Loc[self.currentLocation].updateAnalemmaPosition()



    def animate(self):
        self.update_PCI_PCPF_ECSS_Position()
        ### self.update_PCPF_Rotation()
        self.update_ECSS_Rotation()
        #### self.Eq.updateNodesPosition()
        self.updateCurrentLocationEcliptic()
        #self.AnaLemma.updateAnalemmaPosition()
        self.updateCurrentLocationAnalemma()

        ### self.EqPlane.updateEquatorialPlanePosition()	

    def showEquatorialPlane(self, value):
        self.EqPlane.display(value)

    def showEquator(self, value):
        self.Eq.display(value)

    def showTropics(self, value):
        self.Tr.display(value)

    def showLatitudes(self, value):
        self.Lats.display(value)

    def showLongitudes(self, value):
        self.Lons.display(value)

    def showTimezones(self, value):
        self.tz.display(value)

    def showNodes(self, value):
        self.Eq.showNodes(value)


class makeEarthLocation():
    SUN_VERTEX = 0
    EARTH_VERTEX = 1

    #
    # An Earth location is defined in the OVRL referential which 
    # is itself bound to the PCPF referential. This allows to 
    # adjust the positions of all overlay objects at once without 
    # messing with the Planet-Centered-Planet-Fixed referential
    #
    def __init__(self, widgets, tz_index):
#        self.Origin = widgets.Planet.PCPF.referential
        self.Origin = widgets.OVRL
        self.Widgets = widgets
        self.Planet = widgets.Planet
        self.Color = Color.red
        self.EclipticPosition = vector(0,0,0)
        self.lat = self.long = 0
    #    self.AnaLemma = self.makeAnalemma(widgets, tz_index)

        self.anaLemmaTgPlane = None
        self.anaLemmaShape = None
        self.anaLemmaIncrement = 0

        self.GeoLoc = sphere(frame=self.Origin, pos=vector(0,0,0), radius=10, color=self.Color, material = materials.emissive, opacity=0.5, axis=(0,0,1))

        #self.GeoLoc = circle(color=self.Color, radius=10, pos=(0,0,0), normalAxis=(0,0,1), context=self.Origin)        
        self.Origin.axis.visible = True

        # obtain location info. Earthloc is a tuple (lat, long, timezone)
        earthLoc = self.Planet.SolarSystem.locationInfo.getLocationInfo(tz_index)
        if earthLoc != {}:
            self.Name = earthLoc["name"]
            self.lat = earthLoc["lat"]
            self.long = earthLoc["long"]
            self.setGeoPosition()
            self.updateEclipticPosition()
            self.setNormalToSurface()
            self.setOrientation(self.Grad)
            self.initAnalemma()
        else:
            self.Name = "None"

    def initAnalemma(self):
        self.Shape = None
        self.analemmaIncrement = 0
        self.anaLemmaDistanceFactor = 1.15
        self.SphereIntersecRadius = self.Planet.getBodyRadius() * self.anaLemmaDistanceFactor
        self.GeoPlaneCenter = self.GeoLoc.pos * self.anaLemmaDistanceFactor
        self.CurrentGeoLoc = self.EclipticPosition
        self.setTgPlane()
        #self.setAnaLemmaSphere()
        self.makeSunAxis() #locIndex)
        self.displayAnalemma(False)

    def displayAnalemma(self, trueFalse):
        self.SunAxis.visible = trueFalse
        self.CurrentGeoLoc.visible = trueFalse
        #self.Loc.displayanaLemmaTgPlane(trueFalse)

    def resetAnalemma(self):
        self.Shape.visible = False
        del self.Shape
        self.Shape = None
        self.analemmaIncrement = 0

    def getAnalemmaPlaneIntersec(self):
        # given a vector normal to a location, we can deduct the plane equation that is perpendicular to that vector:
        # The plane is centered on self.anaLemmaDistanceFactor x self.GeoLoc.pos (the earth location amplified by a 
        # factor self.anaLemmaDistanceFactor so that the plane doesn't touch the earth's surface)
        # Let be (nX, nY, nZ) a vector normal to the plane, (xo, yo, zo) a known point on the plane, and (x, y, z) a 
        # random point on the plane. Since the 2 vectors (nX, nY, nZ) and (x-xo, y-y0, z-z0) are perpendicular, the 
        # scalar product must be zero, hence the equation:
        #
        #       (x - xo)*nX + (y - y0)*nY + (z - z0)*nZ = 0 
        #
        # The parametric equation of the line coming from the sun and going to the earth location is given by:
        #
        #       r(t) = P + t.D 
        #
        # where P is a point on the line and D is the direction vector. If we have 2 points (x0,y0,z0) (x1,y1,z1)
        # on the line, then the direction D = (x0 -x1, y0 -y1, z0 -z1)
        # the final eq is r(t) = (xloc, yloc, zloc) + t * (x0 -x1, y0 -y1, z0 -z1) with r(t) = (x,y,z)
        #
        # Soo, to find the line and plane intersec, we need to replace the coordinate of r(t) in the plane equation
        # and find the value of t. We then find r(t) by replacing the value of t in each coordinate.
        # 
        # in an EarthLocation context: 
        #   - the point belonging to the plane is self.GeoLoc * self.anaLemmaDistanceFactor
        #   - the normal vector to the plane is self.UnitGrad
        #   - the point of the line P is the Earth vertex self.GeoLoc
        #   - the direction D is Earth Vertex - Sun Vertex
        
        # first calculate t so that the intersection we are looking for verify the plane equation

        if self.analemmaIncrement < TI_FULL_YEAR:
            PlaneCenter = self.Widgets.PCPF.referential.frame_to_world(self.Widgets.OVRL.frame_to_world(self.GeoPlaneCenter))
            Normal = self.Widgets.PCPF.referential.frame_to_world(self.Widgets.OVRL.frame_to_world(self.UnitGrad))

            t = (PlaneCenter[0] - self.SunAxis.pos[self.SUN_VERTEX][0])*Normal[0] + \
                (PlaneCenter[1] - self.SunAxis.pos[self.SUN_VERTEX][1])*Normal[1] + \
                (PlaneCenter[2] - self.SunAxis.pos[self.SUN_VERTEX][2])*Normal[2]

            t = t / ((self.SunAxis.pos[self.SUN_VERTEX][0] - self.SunAxis.pos[self.EARTH_VERTEX][0])*Normal[0] +\
                    (self.SunAxis.pos[self.SUN_VERTEX][1] - self.SunAxis.pos[self.EARTH_VERTEX][1])*Normal[1] + \
                    (self.SunAxis.pos[self.SUN_VERTEX][2] - self.SunAxis.pos[self.EARTH_VERTEX][2])*Normal[2])
            # second, deduct the coordinates
            self.Intersec =       ( self.SunAxis.pos[self.SUN_VERTEX][0] + t * (self.SunAxis.pos[self.SUN_VERTEX][0] - self.SunAxis.pos[self.EARTH_VERTEX][0]),
                                    self.SunAxis.pos[self.SUN_VERTEX][1] + t * (self.SunAxis.pos[self.SUN_VERTEX][1] - self.SunAxis.pos[self.EARTH_VERTEX][1]),
                                    self.SunAxis.pos[self.SUN_VERTEX][2] + t * (self.SunAxis.pos[self.SUN_VERTEX][2] - self.SunAxis.pos[self.EARTH_VERTEX][2]))
            print "intersec=",self.Intersec
            print "geoLocAB=", self.EclipticPosition
            if self.Shape == None:
                self.Shape = curve(frame=self.Widgets.OVRL, color=Color.red, visible=True, radius=5, material=materials.emissive)
            
            # make sure the intersec is allowed (it must be between the sun and the 
            # earth location. If it's not, it means that the sun is bolow the horizon)
            if mag(vector(self.Intersec)) < mag(vector(self.EclipticPosition)):
                # add a point to the analemma shape until a full year is complete
                pos = self.Widgets.OVRL.world_to_frame(self.Widgets.PCPF.referential.world_to_frame(self.Intersec))
                self.Shape.append(pos= pos)
                self.analemmaIncrement = self.analemmaIncrement + self.Planet.SolarSystem.Dashboard.orbitalTab.TimeIncrement

    def getAnalemmaSphereIntersec(self):
        # The sphere is centered on the earth center and has a radius self.anaLemmaDistanceFactor x self.radius (the sphere 
        # radius is amplified by a factor self.anaLemmaDistanceFactor so that the sphere distance with the earth surface
        # can be changed)
        # 
        # The equation of a sphere centered on earth is: (x - x0)^2 + (y - y0)^2 + (z - z0)^2 = R^2 where (x0, y0, z0) are
        # the coordinates of the earth center.
        #
        # The parametric equation of the line coming from the sun and going to the earth location is given by:
        #
        #       r(t) = P + t.D 
        #
        # where P is a point on the line and D is the direction vector. If we have 2 points (x0,y0,z0) (x1,y1,z1)
        # on the line, then the direction D = (x0 -x1, y0 -y1, z0 -z1). Since this line passes through the sun and
        # the current location on the earth's surface, the final eq is:
        #   
        #       r(t) = (xloc, yloc, zloc) + t * (x0 -x1, y0 -y1, z0 -z1) with r(t) = (x,y,z)
        #
        # Soo, to find the line and sphere intersec, we need to replace the coordinate of r(t) in the sphere equation
        # and find the value of t. We then find r(t) by replacing the value of t in each coordinate.
        # 
        # This results in a quadratic equation for t. Finding a solution means calculating its discriminant D and, after
        # making sure it's positive, keep the positive solution t1 = (-B + sqrt(D))/(2*A)
        # Last, but not least, we need to make sure, the line coming from the sun doesn't intersect the earth surface
        # before reaching the location. In other words, we need to make sure the location has its y coordinate positive
        # in the ECSS referential.
        #
        # in an EarthLocation context: 
        #   - the point of the line P is the Earth vertex self.GeoLoc
        #   - the direction D is Earth Vertex - Sun Vertex
         
        # first calculate t so that the intersection we are looking for verifies the sphere equation

        if self.analemmaIncrement < TI_FULL_YEAR:
            sx = self.Planet.Origin.pos[0]
            sy = self.Planet.Origin.pos[1]
            sz = self.Planet.Origin.pos[2]

            px = self.SunAxis.pos[self.SUN_VERTEX][0]
            py = self.SunAxis.pos[self.SUN_VERTEX][1]
            pz = self.SunAxis.pos[self.SUN_VERTEX][2]

            vx = px - self.SunAxis.pos[self.EARTH_VERTEX][0]
            vy = py - self.SunAxis.pos[self.EARTH_VERTEX][1]
            vz = pz - self.SunAxis.pos[self.EARTH_VERTEX][2]

            A = vx*vx + vy*vy + vz*vz
            B = 2.0 * (px * vx + py * vy + pz * vz - vx * sx - vy * sy - vz * sz)
            C = px * px - 2 * px * sx + sx * sx + py * py - 2 * py * sy + sy * sy + \
                   pz * pz - 2 * pz * sz + sz * sz - self.SphereIntersecRadius * self.SphereIntersecRadius 
            #vk = self.SunAxis.pos[self.SUN_VERTEX] - self.SunAxis.pos[self.EARTH_VERTEX]
            #v0 = self.Planet.Origin.pos
            #A = vk[0]**2 + vk[1]**2 + vk[2]**2
            
#           # B = 2 * (vk[0]*(1 - v0[0]) + vk[1]*(1 - v0[1]) + vk[2]*(1 - v0[2]))
            #B = 2 * (vk[0]*(self.SunAxis.pos[self.EARTH_VERTEX][0] - v0[0]) + \
            #         vk[1]*(self.SunAxis.pos[self.EARTH_VERTEX][1] - v0[1]) + \
            #         vk[2]*(self.SunAxis.pos[self.EARTH_VERTEX][2] - v0[2])) 

            #C = self.SunAxis.pos[self.SUN_VERTEX][0]**2 + \
            #    self.SunAxis.pos[self.SUN_VERTEX][1]**2 + \
            #    self.SunAxis.pos[self.SUN_VERTEX][2]**2 + \
            ##    self.SunAxis.pos[self.EARTH_VERTEX][0]**2 + \
             #   self.SunAxis.pos[self.EARTH_VERTEX][1]**2 + \
            #    self.SunAxis.pos[self.EARTH_VERTEX][2]**2 + \
            #    -2*(self.SunAxis.pos[self.SUN_VERTEX][0] * v0[0] + \
            #    self.SunAxis.pos[self.SUN_VERTEX][1] * v0[1] + \
            #    self.SunAxis.pos[self.SUN_VERTEX][2] * v0[2]) - self.SphereIntersecRadius**2

            # for the intersec to be on the sphere, we have 2 possible solutions for t
            D = B*B - 4*A*C
            t1 = 0
            if D > 0:
                t1 = (-B + sqrt(D))/(2.0*A)
            else:
                print "Negative discriminant: B^2=", B*B, ", 4AC=", 4*C*A
                return

            #D = math.sqrt(B**2 - 4*A*C)
            #t1 = (-B + D)/2*A
            #t2 = (-B - D)/2*A      

            # second, deduct the coordinates
            self.Intersec =       ( px + (t1 * vx),
                                    py + (t1 * vy),
                                    pz + (t1 * vz))

#            print "P(sun)=", vector(px,py,pz)
#            print "V(sun-loc)=", vector(vx,vy,vz)
##            print "discriminant D=", D, ", sqrt(D)=", sqrt(D), ", -B=", -B, ", 2A=", 2.0*A, ", t=", t1
#            print "solution t=", t1
#            print "intersec=",self.Intersec
#            print "geoLocAB=", self.EclipticPosition
#            print "----------------------------"
            if self.Shape == None:
                self.Shape = curve(frame=self.Widgets.OVRL, color=Color.red, visible=True, radius=5, material=materials.emissive)
            
            # make sure the intersec is allowed (it must be between the sun and the 
            # earth location. If it's not, it means that the sun is bolow the horizon)

#            if mag(vector(self.Intersec)) < mag(vector(self.EclipticPosition)):

            ECSSgeoLoc = self.Widgets.ECSS.referential.world_to_frame(self.SunAxis.pos[self.EARTH_VERTEX])
            print "intersecInECSS:", ECSSgeoLoc
            if ECSSgeoLoc[1] >= 0:
                # add a point to the analemma shape until a full year is complete
                pos = self.Widgets.OVRL.world_to_frame(self.Widgets.PCPF.referential.world_to_frame(self.Intersec))
                #print "inserting ANALEMMA POINT: ", pos
                self.Shape.append(pos = pos)

            self.analemmaIncrement = self.analemmaIncrement + self.Planet.SolarSystem.Dashboard.orbitalTab.TimeIncrement
        else:
            print "full year!"

    def getAnalemmaSphereIntersec_bis(self):
        # The sphere is centered on the earth center and has a radius self.anaLemmaDistanceFactor x self.radius (the sphere 
        # radius is amplified by a factor self.anaLemmaDistanceFactor so that the sphere distance with the earth surface
        # can be changed)
        # 
        # The equation of a sphere centered on earth is: (x - x0)^2 + (y - y0)^2 + (z - z0)^2 = R^2 where (x0, y0, z0) are
        # the coordinates of the earth center.
        #
        # The parametric equation of the line coming from the sun and going to the earth location is given by:
        #
        #       r(t) = P + t.D 
        #
        # where P is a point on the line and D is the direction vector. If we have 2 points (x0,y0,z0) (x1,y1,z1)
        # on the line, then the direction D = (x0 -x1, y0 -y1, z0 -z1). Since this line passes through the sun and
        # the current location on the earth's surface, the final eq is:
        #   
        #       r(t) = (xloc, yloc, zloc) + t * (x0 -x1, y0 -y1, z0 -z1) with r(t) = (x,y,z)
        #
        # Soo, to find the line and sphere intersec, we need to replace the coordinate of r(t) in the sphere equation
        # and find the value of t. We then find r(t) by replacing the value of t in each coordinate.
        # 
        # This results in a quadratic equation for t. Finding a solution means calculating its discriminant D and, after
        # making sure it's positive, keep the positive solution t1 = (-B + sqrt(D))/(2*A)
        # Last, but not least, we need to make sure, the line coming from the sun doesn't intersect the earth surface
        # before reaching the location. In other words, we need to make sure the location has its y coordinate positive
        # in the ECSS referential.
        #
        # in an EarthLocation context: 
        #   - the point of the line P is the Earth vertex self.GeoLoc
        #   - the direction D is Earth Vertex - Sun Vertex
        
        # first calculate t so that the intersection we are looking for verifies the sphere equation

        if self.analemmaIncrement < TI_FULL_YEAR:
            #PlaneCenter = self.Widgets.PCPF.referential.frame_to_world(self.Widgets.OVRL.frame_to_world(self.GeoPlaneCenter))
            #Normal = self.Widgets.PCPF.referential.frame_to_world(self.Widgets.OVRL.frame_to_world(self.UnitGrad))
            vk = self.SunAxis.pos[self.SUN_VERTEX] - self.SunAxis.pos[self.EARTH_VERTEX]
            v0 = self.Planet.Origin.pos
            A = vk[0]**2 + vk[1]**2 + vk[2]**2
            
            B = 2 * (vk[0]*(1 - v0[0]) + vk[1]*(1 - v0[1]) + vk[2]*(1 - v0[2]))
#            B = 2 * (vk[0]*(self.SunAxis.pos[self.EARTH_VERTEX][0] - v0[0]) + \
#                     vk[1]*(self.SunAxis.pos[self.EARTH_VERTEX][1] - v0[1]) + \
#                     vk[2]*(self.SunAxis.pos[self.EARTH_VERTEX][2] - v0[2])) 

            C = self.SunAxis.pos[self.SUN_VERTEX][0]**2 + \
                self.SunAxis.pos[self.SUN_VERTEX][1]**2 + \
                self.SunAxis.pos[self.SUN_VERTEX][2]**2 + \
                self.SunAxis.pos[self.EARTH_VERTEX][0]**2 + \
                self.SunAxis.pos[self.EARTH_VERTEX][1]**2 + \
                self.SunAxis.pos[self.EARTH_VERTEX][2]**2 + \
                -2*(self.SunAxis.pos[self.SUN_VERTEX][0] * v0[0] + \
                self.SunAxis.pos[self.SUN_VERTEX][1] * v0[1] + \
                self.SunAxis.pos[self.SUN_VERTEX][2] * v0[2]) - self.SphereIntersecRadius*self.SphereIntersecRadius

            # for the intersec to be on the sphere, we have 2 possible solutions for t
            D = B*B - 4*A*C
            t1 = 0
            if D > 0:
                t1 = (-B + sqrt(D))/(2.0*A)
            else:
                print "Negative discriminant: B^2=", B*B, ", 4AC=", 4*C*A
                exit()

            #D = math.sqrt(B**2 - 4*A*C)
            #t1 = (-B + D)/2*A
            #t2 = (-B - D)/2*A      

            # second, deduct the coordinates
            self.Intersec =       ( self.SunAxis.pos[self.SUN_VERTEX][0] + t1 * (self.SunAxis.pos[self.SUN_VERTEX][0] - self.SunAxis.pos[self.EARTH_VERTEX][0]),
                                    self.SunAxis.pos[self.SUN_VERTEX][1] + t1 * (self.SunAxis.pos[self.SUN_VERTEX][1] - self.SunAxis.pos[self.EARTH_VERTEX][1]),
                                    self.SunAxis.pos[self.SUN_VERTEX][2] + t1 * (self.SunAxis.pos[self.SUN_VERTEX][2] - self.SunAxis.pos[self.EARTH_VERTEX][2]))
            print "intersec=",self.Intersec
            print "geoLocAB=", self.EclipticPosition
            if self.Shape == None:
                self.Shape = curve(frame=self.Widgets.OVRL, color=Color.red, visible=True, radius=5, material=materials.emissive)
            
            # make sure the intersec is allowed (it must be between the sun and the 
            # earth location. If it's not, it means that the sun is bolow the horizon)
            ECSSgeoLoc = self.Widgets.ECSS.referential.world_to_frame(self.SunAxis.pos[self.EARTH_VERTEX])
            print "intersecInECSS:", ECSSgeoLoc
            if ECSSgeoLoc[1] >= 0:
                # add a point to the analemma shape until a full year is complete
                pos = self.Widgets.OVRL.world_to_frame(self.Widgets.PCPF.referential.world_to_frame(self.Intersec))
                self.Shape.append(pos = pos)
                self.analemmaIncrement = self.analemmaIncrement + self.Planet.SolarSystem.Dashboard.orbitalTab.TimeIncrement
        else:
            print "full year!"

    def updateAnalemmaPosition(self):
       
        self.CurrentGeoLoc = self.updateEclipticPosition()
        self.SunAxis.pos[self.EARTH_VERTEX] = self.CurrentGeoLoc 
        self.SunAxis.pos[self.SUN_VERTEX] = (0, 0, self.CurrentGeoLoc[2])

        # if we are in 24h animation mode, update forward vector to face earth from the sun's perspective
        if self.Planet.SolarSystem.Dashboard.widgetsTab.acb.GetValue() == True:

            #self.getAnalemmaPlaneIntersec()

            self.getAnalemmaSphereIntersec()

            # set camera forward vector to follow the earth from the sun's perspective
            #self.Planet.SolarSystem.Scene.forward = vector(self.Planet.Origin.pos - (0, 0, self.CurrentGeoLoc[2] + 5*self.radius))

            # alternate view: using the normal vector
            self.Planet.SolarSystem.Scene.forward = self.Planet.PCPF.referential.frame_to_world(self.Origin.frame_to_world(self.UnitGrad))
            self.Planet.SolarSystem.Scene.center = (0,0,0)

    def setGeoPosition(self):
        # set the Geo position based on 
        # latitude/longitude of location

        self.radius = (self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType])*0.999
        
        # calculate distance from z-axis to latitude line
        eqPlane = self.radius * cos(deg2rad(self.lat))

        # deduct (x,y) from eqPlane. Note, we need to extend the longitude 
        # value by 180 degrees to take into account the way the earth texture
        # was applied on the sphere
        self.GeoLoc.pos[0] = eqPlane * cos(deg2rad(self.long)+pi)
        self.GeoLoc.pos[1] = eqPlane * sin(deg2rad(self.long)+pi)
        self.GeoLoc.pos[2] = self.radius * sin(deg2rad(self.lat))

#        self.GeoPlaneCenter = self.anaLemmaDistanceFactor * self.GeoLoc.pos

    def makeSunAxis(self):

        # create first vertex in sun at z coordinate = earth latitude to create an axis parallel to ecliptic
        self.SunAxis = curve(pos=[(0,0,self.CurrentGeoLoc[2])], color=Color.white, visible=False,  material=materials.emissive, radius=0)
        ## -> self.SunAxis = curve(pos=[(0,0,0)], color=Color.white, visible=False,  material=materials.emissive, radius=0)

        # add point location in ecliptic coordinate
        self.SunAxis.append(pos=self.CurrentGeoLoc, color=Color.green)

        # we now have a sun-earth line that links a particular latitude to the Sun light direction

    def updateEclipticPosition(self):
        # init position in ecliptic referential
        # It is calculated by first getting the position of OVRL objects 
        # in the PCPF referential, and then convert it from PCPF to ecliptic (absolute)
        # This method is used mainly by the camera object
        #self.EclipticPosition = self.Widgets.PCPF.referential.frame_to_world(self.Origin.frame_to_world(self.GeoLoc.pos))
        self.EclipticPosition = self.Widgets.PCPF.referential.frame_to_world(self.Origin.frame_to_world(self.GeoLoc.pos))
        #self.GeoPlaneCenter = 1.2 * self.EclipticPosition

        return self.EclipticPosition

    def getEclipticPosition(self):
        # return ecliptic coordinates
        return self.EclipticPosition

    def getGeoPosition(self):
        # return PCPF coordinates
        return self.GeoLoc.pos

    def display(self, trueFalse):
        self.GeoLoc.visible = trueFalse

    def setNormalToSurfaceALT(self):
        # the equation of the earth surface is S: (x-xcenter)^2 + (y-ycenter)^2 + (z-zcenter)^2 = R^2
        # the coordinates of a vector normal to the earth surface is given by the earth's surface gradient:
        #   Gradient(S) = (DS/Dx, DS/Dy, DS/Dz)
        # DS/Dx = 2(x-xcenter) partial derivative of surface for x
        # DS/Dy = 2(y-ycenter) partial derivative of surface for y 
        # DS/Dz = 2(z-zcenter) partial derivative of surface for z
        # the normal vector in our location is given by [xloc+DS/Dx(loc)]
        base = self.getGeoPosition() # self.Planet.Origin.pos
        A = base[0] - self.Origin.pos[0] #self.Planet.Origin.pos[0]
        B = base[1] - self.Origin.pos[1] #self.Planet.Origin.pos[1]
        C = base[2] - self.Origin.pos[2] #self.Planet.Origin.pos[2] 
        self.Grad = vector(A, B, C)/np.sqrt(A**2 + B**2 + C**2)

##        self.GradientX = 2*(base[0]-self.Origin.pos[0])
#        self.GradientY = 2*(base[1]-self.Origin.pos[1])
#        self.GradientZ = 2*(base[2]-self.Origin.pos[2])
#        self.Grad = vector(self.GradientX, self.GradientY, self.GradientZ)

        ####zob = sphere(pos=base, radius=300, color=Color.yellow, visible=True, material = materials.emissive, opacity=1.0, frame=self.Origin)

#        self.GradientX = 2*(self.EclipticPosition[0]-self.Planet.Origin.pos[0])
#        self.GradientY = 2*(self.EclipticPosition[1]-self.Planet.Origin.pos[1])
#        self.GradientZ = 2*(self.EclipticPosition[2]-self.Planet.Origin.pos[2])

        #self.Grad = vector(self.GradientX, self.GradientY, self.GradientZ)
        #self.Grad = theGrad * 1/mag(theGrad)
#        self.NormalVec = simpleArrow(Color.white, 0, 10, self.GeoLoc.pos, axisp = (self.Grad/10), context = self.Origin)
        self.NormalVec = simpleArrow(Color.white, 0, 10, self.GeoLoc.pos, axisp = (1000 * self.Grad), context = self.Origin)
        self.NormalVec.display(False)

    def setNormalToSurface(self):
        # the equation of the earth surface is S: (x-xcenter)^2 + (y-ycenter)^2 + (z-zcenter)^2 = R^2
        # the coordinates of a vector normal to the earth surface is given by the earth's surface gradient:
        #   Gradient(S) = (DS/Dx, DS/Dy, DS/Dz)
        # DS/Dx = 2(x-xcenter) partial derivative of surface for x
        # DS/Dy = 2(y-ycenter) partial derivative of surface for y 
        # DS/Dz = 2(z-zcenter) partial derivative of surface for z
        # the normal vector in our location is given by [xloc+DS/Dx(loc)]
        # Since center is alway (0,0,0) in OVRL referential, calculating DS
        # translates as: DS/Dx = 2x,  Ds/Dy = 2y,  De/Dz = 2z
        base = self.getGeoPosition() #self.updateEclipticPosition() # self.Planet.Origin.pos
#        self.GradientX = 2*(base[0]) #-self.Origin.pos[0])
#        self.GradientY = 2*(base[1]) #-self.Origin.pos[1])
#        self.GradientZ = 2*(base[2]) #-self.Origin.pos[2])
        self.GradientX = (base[0]) #-self.Origin.pos[0])
        self.GradientY = (base[1]) #-self.Origin.pos[1])
        self.GradientZ = (base[2]) #-self.Origin.pos[2])
        self.Grad = vector(self.GradientX, self.GradientY, self.GradientZ)
        self.UnitGrad = norm(self.Grad)
        self.NormalVec = simpleArrow(Color.white, 0, 10, self.GeoLoc.pos, axisp = (self.Grad/5), context = self.Origin)
        self.NormalVec.display(False)

    def setTgPlane(self):
        self.anaLemmaTgPlane = box(frame=self.Origin, pos=self.anaLemmaDistanceFactor*self.GeoLoc.pos, axis = self.UnitGrad, width=10*self.radius, length=0.0001, height=10*self.radius, material=materials.emissive, visible=False, color=Color.grey, opacity=1)

    def setAnaLemmaSphere(self):
        self.anaLemmaSphere = sphere(frame=self.Origin, pos=(0,0,0), radius=self.SphereIntersecRadius, material=materials.emissive, visible=True, color=Color.gray, opacity=0.1)

    def displayTgPlane(self, trueFalse):
        self.anaLemmaTgPlane.visible = trueFalse

    def setOrientation(self, axis):
        self.GeoLoc.axis = axis * (1 / mag(axis))

    def show(self, trueFalse):
        self.NormalVec.display(trueFalse)



class makeNode():
    def __init__(self, widgets, colr, ascending = true):
        #self.Origin = widgets.PCPF

        # Nodes do not rotate with the planet. They are fixed to the stars, 
        # hence must be relative to the PCI referential

        self.Planet = widgets.Planet
        self.Origin = widgets.Planet.PCI.referential
        self.Color = colr
        self.ascending = -1 if ascending else 1

        # Note: the nodes can't be attached to the widgets frame, as we don't 
        # want the nodes to rotate with the frame during an animation. That's
        # why their position needs to be updated by an external animation
        # routine using the "updateNodesPosition" method.

        self.Node = sphere(frame=self.Origin, pos=(0,0,0), np=32, radius=100, make_trail=False, color=self.Color, visible=False, material=materials.emissive) 
#        self.Node = sphere(frame=widgets.PCI, pos=(0,0,0), np=32, radius=3000, make_trail=False, color=self.Color, visible=False, material=materials.emissive) 
        self.setPosition()


    def setPosition(self):
        self.Node.pos[0] = self.ascending * self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]
        self.Node.pos[1] = 0 #self.Planet.Position[1]
        self.Node.pos[2] = 0 #self.Planet.Position[2]


    def display(self, trueFalse):
        self.Node.visible = trueFalse


class makeEquator():

    def __init__(self, widgets): #planet):
        self.Planet = widgets.Planet
#        self.Origin = self.Planet.Origin #widgets.PCPF.referential
        self.Origin = widgets.OVRL
        print "ORIGIN=", self.Origin.pos
        #self.PCI = widgets.PCI
        self.Color = Color.red

        self.Trail = curve(frame=self.Origin, color=self.Color, visible=False, radius=25, material=materials.emissive)
#        self.Trail = curve(frame=self.Planet.PCPF.referential, color=self.Color, visible=False, radius=25, material=materials.emissive)
#        self.Trail = curve(frame=self.Planet.PCI.referential, color=self.Color, visible=False, radius=25, material=materials.emissive)
        self.Position = np.matrix([[0],[0],[0]], np.float64)

        # The equator holds the Asc and Des objects as they are always along the equator line
        self.AscNode = makeNode(widgets, Color.green, ascending=True)
        self.DesNode = makeNode(widgets, Color.red, ascending=False)

        """
        self.NodesAxis = curve( frame=widgets.PCI, 
#                                pos=[(2 * (self.DesNode.Node.pos[0] - self.Planet.Position[0]), 0, 0), 
#                                     (2 * (self.AscNode.Node.pos[0] - self.Planet.Position[0]), 0, 0)], 
                                pos = [(-2*self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType],0,0),
                                       (2*self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType],0,0)],
                                     color=Color.cyan, visible=True, radius=0, material=materials.emissive)
        """
        self.makeNodeAxis()
        self.draw()

    def makeNodeAxis(self):
        # Nodes axis is fixed to the stars and therefore 
        # must be relative to the PCI referential
        self.NodesAxis = curve( frame=self.Planet.PCI.referential, #self.PCI.referential, 
                                #pos=[(2 * (self.DesNode.Node.pos[0] - self.Planet.Position[0]), 0, 0), 
                                #    (2 * (self.AscNode.Node.pos[0] - self.Planet.Position[0]), 0, 0)], 
                                pos = [ (-2*self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType],0,0),
                                        (2*self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType],0,0)],
                                color=Color.cyan, visible=False, radius=0, material=materials.emissive)


    def display(self, trueFalse):
        self.Trail.visible = trueFalse

    def draw(self):
        increment = pi/180
        for E in np.arange(0, 2*pi+increment, increment):
            # build Equator line using angular segments of increments degres
            self.drawSegment(E)


    def drawSegment(self, E, trace = True):
        self.Position = self.setCartesianCoordinates(E)

        # add angular portion of equator
        self.Trail.append(pos= vector(self.Position[0],self.Position[1],self.Position[2]), color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))


    def setCartesianCoordinates(self, angleIncr):
        radius = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]

#        self.Position[0] = radius * cos(angleIncr) 
#        self.Position[1] = radius * sin(angleIncr)
#        self.Position[2] = 0
        return (radius * cos(angleIncr),
                radius * sin(angleIncr),
                0)


    def showNodes(self, trueFalse):
        self.AscNode.display(trueFalse)
        self.DesNode.display(trueFalse)
        self.NodesAxis.visible = trueFalse

    #def updateNodesAxisPosition(self):

    def updateNodesPosition(self):
        pass
        #self.AscNode.updatePosition()
        #self.DesNode.updatePosition()
        #self.updateNodesAxisPosition()

class makeEquatorialPlane():

    def __init__(self, widgets, color, opacity): #planet, color, opacity):
        # Equatorial Plane is fixed to the stars and therefore 
        # must be relative to the PCI referential
        
        self.Planet = widgets.Planet
        self.Origin = widgets.Planet.PCI.referential #widgets.Planet.Origin
        self.Opacity = opacity
        self.Color = color 

        side = 0.1*AU*DIST_FACTOR
        # define plane in fix referential PCI
        self.eqPlane = box(frame=self.Origin, pos=(0,0,0), length=side, width=0.0001, height=side, material=materials.emissive, visible=True, color=self.Color, opacity=0) #, axis=(0, 0, 1), opacity=0.8) #opacity=self.Opacity)


    def display(self, trueFalse):
        STEPS = 10
        if trueFalse == True:
            bound = 0
        else:
            bound = STEPS-1
        
        for i in range(STEPS):
            self.eqPlane.opacity = float(abs(bound-i))/(3*STEPS)
            sleep(1e-2)


class doMeridian():

    def __init__(self, widgets, colr, longitudeAngle):
        self.longAngle = longitudeAngle
        self.Origin = widgets.OVRL
#        self.Origin = widgets.Planet.Origin
        self.Planet = widgets.Planet
        #Radius = 25 if longitudeAngle == 0 else 0
        # define meridian in rotating referential PCPF
        self.Trail = curve(frame=self.Origin, color=colr, visible=False,  material=materials.emissive, radius=(25 if longitudeAngle == 0 else 0))
        self.Position = np.matrix([[0],[0],[0]], np.float64)
        self.Color = colr #Color.cyan
        self.draw()


    def display(self, trueFalse):
        self.Trail.visible = trueFalse

    def draw(self):
        increment = pi/180
        for E in np.arange(0, 2*pi+increment, increment):
            # build longitude using angular segments of increments degres
            self.drawSegment(E)


    def setCartesianCoordinates(self, angleIncr):
        radius = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]
        projectionOnXYplane = radius * cos(angleIncr)
#        self.Position[0] = projectionOnXYplane * cos(self.longAngle)
#        self.Position[1] = projectionOnXYplane * sin(self.longAngle)
#        self.Position[2] = radius * sin(angleIncr)

        return (projectionOnXYplane * cos(self.longAngle),
                projectionOnXYplane * sin(self.longAngle),
                radius * sin(angleIncr))


    def drawSegment(self, E, trace = True):
        self.Position = self.setCartesianCoordinates(E)
        newpos = vector(self.Position[0],self.Position[1],self.Position[2])

        # add angular portion of longitude curve
        self.Trail.append(pos=newpos, color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))

class makeMeridians():
    def __init__(self, widgets, colr):
        self.Origin = widgets.OVRL
#        self.Origin = widgets.Planet.Origin
        self.Origin.visible = True
        self.Widgets = widgets
        self.Color = colr
        self.Meridians = []


    def display(self, trueFalse):
        for mrd in self.Meridians:
            mrd.display(trueFalse)


    def draw(self, angle, origColr):
        colr = origColr #Color.red
        for i in np.arange(0, pi, deg2rad(angle)):
            # build Meridians by longitude circles
            self.Meridians.append(doMeridian(self.Widgets, colr, i))
            colr = self.Color


class makeLongitudes(makeMeridians):
        
    def __init__(self, widgets):

        makeMeridians.__init__(self, widgets, Color.cyan)
        self.draw(10, Color.red)


class makeTimezones(makeMeridians):
        
    def __init__(self, widgets):
        makeMeridians.__init__(self, widgets, Color.white)
        self.draw(15, Color.white)



class doLatitude():

    def __init__(self, widgets, latitudeAngle, colr, thickness=0):
        self.latAngle = latitudeAngle
        self.Origin = widgets.OVRL
#        self.Origin = widgets.Planet.Origin
        self.Planet = widgets.Planet
        self.Color = colr

        # define latitude in rotating referential PCPF
        self.Trail = curve(frame=self.Origin, color=self.Color, material=materials.emissive, visible=False, radius=thickness)
        self.Position = np.matrix([[0],[0],[0]], np.float64)
        self.draw()


    def display(self, trueFalse):
        self.Trail.visible = trueFalse


    def draw(self):
        increment = pi/180
        for E in np.arange(0, 2*pi+increment, increment):
            # build latitude level using angular segments of E increments degres
            self.drawSegment(E)


    def setCartesianCoordinates(self, angleIncr):
        radius = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]
        projection = radius * cos(self.latAngle)

#        self.Position[0] = projection * sin(angleIncr)
#        self.Position[1] = projection * cos(angleIncr)
#        self.Position[2] = radius * sin(self.latAngle)
        return (projection * sin(angleIncr),
                projection * cos(angleIncr),
                radius * sin(self.latAngle))


    def drawSegment(self, E):
        self.Position = self.setCartesianCoordinates(E)
        newpos = vector(self.Position[0],self.Position[1],self.Position[2])

        # add angular portion of latitude curve
        self.Trail.append(pos=newpos, color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))


class makeLatitudes():
        
    def __init__(self, widgets):
        self.Origin = widgets.OVRL
#        self.Origin = widgets.Planet.Origin
        self.Origin.visible = True
        self.Widgets = widgets
        self.Color = Color.cyan
        self.lats = []
        self.draw()


    def display(self, trueFalse):
        for lat in self.lats:
            lat.display(trueFalse)


    def draw(self):
        for i in np.arange(-pi/2, pi/2, deg2rad(10)):
            # build latitudes levels every 10deg from -90 to +90            
            self.lats.append(doLatitude(self.Widgets, i, Color.cyan))


class makeTropics():
        
    def __init__(self, widgets):
#        self.Origin = widgets.PCI.referential
        self.Origin = widgets.OVRL
        self.Widgets = widgets
        self.Tropics = []
        self.Color = Color.cyan
        self.TROPIC_ABS_LATITUDES = deg2rad(23.5)
        self.draw()


    def display(self, trueFalse):
        for trop in self.Tropics:
            trop.display(trueFalse)


    def draw(self):
        # build latitudes levels every 10deg from -90 to +90            
        self.Tropics.append(doLatitude(self.Widgets, -self.TROPIC_ABS_LATITUDES, Color.yellow, thickness=25))
        self.Tropics.append(doLatitude(self.Widgets, +self.TROPIC_ABS_LATITUDES, Color.yellow, thickness=25))


class makeAnalemmaXX():
    SUN_VERTEX = 0
    EARTH_VERTEX = 1

    def __init__(self, widgets, locIndex = -1):
        # draw earth sun segment between center 
        # of sun and a point at a given latitude
        self.ECSS = widgets.ECSS
#        self.Origin = widgets.Planet.Origin #widgets.ECSS.referential  # let's use the sun synchrnous referential
        self.Origin = widgets.ECSS.referential  # let's use the sun synchrnous referential
        self.Planet = widgets.Planet
        self.ECSSangle = widgets.ECSSangle
        self.Color = Color.red
        self.Widgets = widgets
        self.Loc = None
        self.Shape = None
        self.analemmaIncrement = 0

#        self.CurrentGeoLoc = sphere(frame=self.Origin, pos=(0,0,0), np=32, radius=50, material = materials.emissive, make_trail=True, color=self.Color, visible=True) 
        
        # attach a sphere to "Planet-Centered Inertial" non-rotating reference frame
        #self.CurrentGeoLoc = sphere(frame=self.Origin, pos=(0,0,0), np=32, radius=50, material = materials.emissive, make_trail=True, color=self.Color, visible=True) 
#        self.CurrentGeoLoc = sphere(frame=self.Planet.PCI.referential, pos=(0,0,0), np=32, radius=0, material = materials.emissive, make_trail=True, color=Color.green, visible=True)

        if locIndex != -1:
            self.Loc = self.Widgets.Loc[locIndex]
            self.CurrentGeoLoc = self.Loc.updateEclipticPosition()
            print "ANALEMMA EARTH LOC", self.CurrentGeoLoc, self.Loc.GeoLoc.pos
        else:
            self.CurrentGeoLoc = self.Planet.Origin.pos
            #self.CurrentGeoLoc = sphere(frame=self.Origin, pos=(0,0,0), np=32, radius=150, material = materials.emissive, make_trail=True, color=Color.green, visible=True) 

        # set the radius (will be used in creating the sun axis)
        self.radius = (self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]) #### *0.999

        # compute semi-latus Rectum: L = a(1 - e**2)
#        self.semiLactusRectum = widgets.Planet.a * (1 - widgets.Planet.e**2)

        #self.Trail = curve(frame=self.Origin, color=self.Color, visible=False, radius=25, material=materials.emissive)
        #self.Position = np.matrix([[0],[0],[0]], np.float64)

        # The equator holds the Asc and Desc objects as they are always along the equator line
        #self.AnaLemmaNode = makeNode(widgets, Color.green, ascending=True)
        #self.DesNode = makeNode(widgets, Color.red, ascending=False)

        # make plane
        #self.makeAnalemmaPlane()
        self.Loc.setTgPlane()
        self.makeSunAxis() #locIndex)
        self.display(False)

    def makeAnalemmaPlaneXX(self):
        self.ECSS.display(True)
        self.analemmaPlane = box(frame=self.Origin, pos=(0,self.radius,0), length=2*self.radius, width=0.0001, height=2*self.radius, material=materials.emissive, visible=True, color=Color.yellow, opacity=0.1)
        self.analemmaPlane.rotate(angle=pi/2, axis=self.ECSS.XdirectionUnit) #(self.Axis[0], 0, 0))
        self.Analemma = None

    def makeAnalemmaGraph(self):
        
        # calculate distance from z-axis to latitude line
        self.latPlane = self.radius * cos(deg2rad(self.lat))

        # deduct (x,y) from latPlane. Note, we need to extend the longitude 
        # value by 180 degrees to take into account the way the earth texture
        # was applied on the sphere
        Position = (self.latPlane * cos(deg2rad(self.long)), 
                    self.latPlane * sin(deg2rad(self.long)),
                    self.radius * sin(deg2rad(self.lat)))

        #self.graph = curve(frame=self.OVRL, pos=[Position], color=Color.green, visible=True,  material=materials.emissive, radius=40)
          
    def updateAnalemmaGraph(self):
        pass

    def makeSunAxis(self):
        
        print "make Sun Axis"
 #######       self.setNoonPosition(loc)



#        self.SunAxisFrame = frame()
#        self.SunAxisFrame.pos = self.Origin.frame_to_world(self.CurrentGeoLoc.pos)

        # create first vertex in sun at z coordinate = earth latitude to create an axis parallel to ecliptic
#        self.SunAxis = curve(pos=[(0,0,self.Planet.PCI.referential.frame_to_world(self.CurrentGeoLoc.pos)[2])], color=Color.green, visible=False,  material=materials.emissive, radius=0)
#######        self.SunAxis = curve(pos=[(0,0,self.CurrentGeoLoc.pos[2])], color=Color.green, visible=False,  material=materials.emissive, radius=0)

        self.SunAxis = curve(pos=[(0,0,self.CurrentGeoLoc[2])], color=Color.white, visible=False,  material=materials.emissive, radius=0)
        ## -> self.SunAxis = curve(pos=[(0,0,0)], color=Color.white, visible=False,  material=materials.emissive, radius=0)

        #self.SunAxis = curve(pos=[(0,0,self.Planet.PCPF.referential.frame_to_world(self.CurrentGeoLoc.pos)[2])], color=Color.green, visible=False,  material=materials.emissive, radius=0)


###        self.SunAxis = curve(pos=self.Planet.PCPF.referential.frame_to_world(self.CurrentGeoLoc.pos), color=Color.green, visible=False,  material=materials.emissive, radius=0)

        # add point at latitude (0,0, self.radius * sin(lat)) in ecliptic coordinate, inside the sun
###        self.SunAxis.append(pos=(0, 0, self.CurrentGeoLoc.pos[2]), color=Color.green)

##########        self.SunAxis.append(pos=self.Planet.PCI.referential.frame_to_world(vector(0, 0, self.CurrentGeoLoc.pos[2])), color=Color.green)
        self.SunAxis.append(pos=self.CurrentGeoLoc, color=Color.green)


        #self.SunAxis.append(pos=self.Planet.PCPF.referential.frame_to_world(vector(0, 0, self.CurrentGeoLoc.pos[2])), color=Color.green)

        # we now have a sun-earth line that links a particular latitude to the Sun light direction

#        self.SunAxis.append(pos=self.Origin.frame_to_world(self.CurrentGeoLoc.pos), color=Color.green)


        """
        self.NodesAxis = curve( #frame=self.PCI, 
                                #pos=[(2 * (self.DesNode.Node.pos[0] - self.Planet.Position[0]), 0, 0), 
                                #    (2 * (self.AscNode.Node.pos[0] - self.Planet.Position[0]), 0, 0)], 
                                pos = [(self.Planet.Position[0],self.Planet.Position[1],self.Planet.Position[2]), (0,0,0)], 
                                color=Color.green, visible=True, radius=0, material=materials.emissive)
        """
        ##### self.analemma = curve(frame=self.Origin, pos=[(2*self.radius,2*self.radius,self.CurrentGeoLoc.pos[2])], color=Color.red, visible=True,  material=materials.emissive, radius=1000)

    def makeSunAxis2(self, locIndex):
        
        print "make Sun Axis"
        loc = None
        if locIndex != -1:
            loc = self.Planet.SolarSystem.locationInfo.getLocationInfo(locIndex)

 #######       self.setNoonPosition(loc)



#        self.SunAxisFrame = frame()
#        self.SunAxisFrame.pos = self.Origin.frame_to_world(self.CurrentGeoLoc.pos)

        # create first vertex in sun at z coordinate = earth latitude to create an axis parallel to ecliptic
#        self.SunAxis = curve(pos=[(0,0,self.Planet.PCI.referential.frame_to_world(self.CurrentGeoLoc.pos)[2])], color=Color.green, visible=False,  material=materials.emissive, radius=0)
#######        self.SunAxis = curve(pos=[(0,0,self.CurrentGeoLoc.pos[2])], color=Color.green, visible=False,  material=materials.emissive, radius=0)

        self.SunAxis = curve(pos=[(0,0,self.CurrentGeoLoc[2])], color=Color.green, visible=False,  material=materials.emissive, radius=0)

        #self.SunAxis = curve(pos=[(0,0,self.Planet.PCPF.referential.frame_to_world(self.CurrentGeoLoc.pos)[2])], color=Color.green, visible=False,  material=materials.emissive, radius=0)


###        self.SunAxis = curve(pos=self.Planet.PCPF.referential.frame_to_world(self.CurrentGeoLoc.pos), color=Color.green, visible=False,  material=materials.emissive, radius=0)

        # add point at latitude (0,0, self.radius * sin(lat)) in ecliptic coordinate, inside the sun
###        self.SunAxis.append(pos=(0, 0, self.CurrentGeoLoc.pos[2]), color=Color.green)

##########        self.SunAxis.append(pos=self.Planet.PCI.referential.frame_to_world(vector(0, 0, self.CurrentGeoLoc.pos[2])), color=Color.green)
        self.SunAxis.append(pos=self.CurrentGeoLoc, color=Color.green)


        #self.SunAxis.append(pos=self.Planet.PCPF.referential.frame_to_world(vector(0, 0, self.CurrentGeoLoc.pos[2])), color=Color.green)

        # we now have a sun-earth line that links a particular latitude to the Sun light direction

#        self.SunAxis.append(pos=self.Origin.frame_to_world(self.CurrentGeoLoc.pos), color=Color.green)


        """
        self.NodesAxis = curve( #frame=self.PCI, 
                                #pos=[(2 * (self.DesNode.Node.pos[0] - self.Planet.Position[0]), 0, 0), 
                                #    (2 * (self.AscNode.Node.pos[0] - self.Planet.Position[0]), 0, 0)], 
                                pos = [(self.Planet.Position[0],self.Planet.Position[1],self.Planet.Position[2]), (0,0,0)], 
                                color=Color.green, visible=True, radius=0, material=materials.emissive)
        """
        ##### self.analemma = curve(frame=self.Origin, pos=[(2*self.radius,2*self.radius,self.CurrentGeoLoc.pos[2])], color=Color.red, visible=True,  material=materials.emissive, radius=1000)

    def setNoonPosition(self, loc):

        self.lat = 0.0
        self.long = 0.0
        if loc != None:
            self.lat = loc["lat"]
            #self.lat = 0.0
            self.long = loc["long"]

        
        # calculate distance from z-axis to latitude line
        self.latPlane = self.radius * cos(deg2rad(self.lat))

        # deduct (x,y) from latPlane. Note, we need to extend the longitude 
        # value by 180 degrees to take into account the way the earth texture
        # was applied on the sphere
        self.CurrentGeoLoc.pos[0] = self.latPlane * cos(deg2rad(self.long)) #+pi)
        self.CurrentGeoLoc.pos[1] = self.latPlane * sin(deg2rad(self.long)) #+pi)
        self.CurrentGeoLoc.pos[2] = self.radius * sin(deg2rad(self.lat))
        #print "ZZZZZZZZZZZZZZZZZZZ", self.CurrentGeoLoc.pos[2]

    def updateAnalemmaPosition(self):
        
        #self.sunPerspective = vector(0,0, self.radius)
        ###self.CurrentGeoLoc.pos[0] = self.latPlane * cos(deg2rad(0)+pi)
        ###self.CurrentGeoLoc.pos[1] = self.latPlane * sin(deg2rad(0)+pi)
        
        # update Earth's vertex position with respect to ecliptic
#        self.SunAxis.pos[self.EARTH_VERTEX] = self.Origin.frame_to_world(self.CurrentGeoLoc.pos)
#        self.SunAxis.pos[self.EARTH_VERTEX] = self.Planet.PCI.referential.frame_to_world(self.CurrentGeoLoc.pos)


    #####    self.SunAxis.pos[self.EARTH_VERTEX] = self.Planet.PCPF.referential.frame_to_world(self.CurrentGeoLoc.pos)

        if self.Loc != None:
            self.CurrentGeoLoc = self.Loc.updateEclipticPosition()
        else:
            self.CurrentGeoLoc = self.Planet.Origin.pos

        self.SunAxis.pos[self.EARTH_VERTEX] = self.CurrentGeoLoc #.pos
        self.SunAxis.pos[self.SUN_VERTEX] = (0, 0, self.CurrentGeoLoc[2])

        """
        if False:
            self.Planet.SolarSystem.Dashboard.orbitalTab.TimeIncrement = TI_24_HOURS * 2# * 10 #EARTH_DAILY_MEAN_MOTION #EPHEMERIS_DAY # * 10 * 6
            self.Planet.SolarSystem.setTimeIncrement(self.Planet.SolarSystem.Dashboard.orbitalTab.TimeIncrement)

#        self.Planet.SolarSystem.Scene.forward = vector(self.Planet.Origin.pos - (0, 0, self.sunPerspective[2] + self.CurrentGeoLoc.pos[2]))
        """

        

        # if we are in 24h animation mode, update forward vector to face earth from the sun's perspective
        if self.Planet.SolarSystem.Dashboard.widgetsTab.acb.GetValue() == True:

            self.getLinePlaneIntersec()

            # set camera forward vector to follow the earth from the sun's perspective
########            self.Planet.SolarSystem.Scene.forward = vector(self.Planet.Origin.pos - (0, 0, self.Planet.PCI.referential.frame_to_world(self.CurrentGeoLoc.pos)[2] + 5*self.radius))
            
            
            
            self.Planet.SolarSystem.Scene.forward = vector(self.Planet.Origin.pos - (0, 0, self.CurrentGeoLoc[2] + 5*self.radius))



            #self.Planet.SolarSystem.Scene.forward = vector(self.Planet.Origin.pos - (0, 0, self.Planet.PCPF.referential.frame_to_world(self.CurrentGeoLoc.pos)[2] + 5*self.radius))

    #####        self.Planet.SolarSystem.Scene.forward = vector(self.Planet.Origin.pos - (0, 0, self.CurrentGeoLoc.pos[2] + 5*self.radius))
            if False:
                normal = vector(self.Planet.Origin.pos - (0, 0, self.Planet.PCI.referential.frame_to_world(self.CurrentGeoLoc.pos)[2] + 5*self.radius))

                # get a 20 degres angle with normal
                normalToLoc = vector(self.Planet.PCI.referential.frame_to_world(self.CurrentGeoLoc.pos)
                                        - (0, 0, self.Planet.PCI.referential.frame_to_world(self.CurrentGeoLoc.pos)[2] + 5*self.radius))
        
        

########        self.Planet.SolarSystem.Scene.forward = vector(self.Planet.Position - (self.Planet.PCI.referential.frame_to_world(self.CurrentGeoLoc.pos)[0], self.Planet.PCI.referential.frame_to_world(self.CurrentGeoLoc.pos)[1], self.Planet.PCI.referential.frame_to_world(self.CurrentGeoLoc.pos)[2] + 5*self.radius))

####        self.Planet.SolarSystem.Scene.forward = vector(self.Planet.Origin.pos - (self.Planet.PCI.referential.frame_to_world(self.CurrentGeoLoc.pos)[0], self.Planet.PCI.referential.frame_to_world(self.CurrentGeoLoc.pos)[1], self.Planet.PCI.referential.frame_to_world(self.CurrentGeoLoc.pos)[2] + 5*self.radius))

###        self.Planet.SolarSystem.Scene.forward = vector(self.Planet.Origin.pos - (self.CurrentGeoLoc.pos[0], self.CurrentGeoLoc.pos[1],self.CurrentGeoLoc.pos[2]+ 5*self.radius))

        ####  self.analemma.append(pos=self.CurrentGeoLoc.pos, color=Color.red)


    def updateAnalemmaPosition2(self):
        """
        The angular precession per orbit for an Earth orbiting satellite is given by

        delta = -(3*pi.J2.RE^2/p^2).cos(i)

        where
            J2 = 1.08263e-3 is the coefficient for the second zonal term related to the oblateness of the Earth,
            RE ~ 6378 km is the mean radius of the Earth,
            p is the semi-latus rectum of the orbit,
            i is the inclination of the orbit to the equator.        
        """
        J2 = 1.08263e-3
        precession = -3 * pi * cos(self.Planet.Inclination) * J2 * ((self.radius**2)/(self.semiLactusRectum**2)) 
        angle = precession * self.Planet.SolarSystem.Dashboard.orbitalTab.TimeIncrement/5400     
        print "increment = ", self.Planet.SolarSystem.Dashboard.orbitalTab.TimeIncrement

        self.CurrentGeoLoc.pos[0] = 0 #self.latPlane * cos(deg2rad(0)+pi)
        self.CurrentGeoLoc.pos[1] = 0 #self.latPlane * sin(deg2rad(0)+pi)
        self.SunAxis.pos[1] = self.Origin.frame_to_world(self.CurrentGeoLoc.pos)
        #self.SunAxis.append(pos=self.Origin.frame_to_world(self.CurrentGeoLoc.pos), color=Color.green)
        self.Planet.SolarSystem.Scene.forward = rotate(self.Planet.SolarSystem.Scene.forward, angle=-angle, axis=(0,0,1))
        
        #self.Planet.SolarSystem.Scene.forward = vector(self.Planet.SolarSystem.Scene.center)

    def display(self, trueFalse):
        self.SunAxis.visible = trueFalse
        self.CurrentGeoLoc.visible = trueFalse
        #self.Loc.displayTgPlane(trueFalse)

    def resetAnalemma(self):
        self.Shape.visible = False
        del self.Shape
        self.Shape = None
        self.analemmaIncrement = 0

    def getLinePlaneIntersec(self):
        # given a vector normal to a location, we can deduct the plane equation that is perpendicular to that vector:
        # The plane is centered on self.anaLemmaDistanceFactor x self.GeoLoc.pos (the earth location amplified by a 
        # factor self.anaLemmaDistanceFactor so that the plane doesn't touch the earth's surface)
        # Let be (nX, nY, nZ) a vector normal to the plane, (xo, yo, zo) a known point on the plane, and (x, y, z) a 
        # random point on the plane. Since the 2 vectors (nX, nY, nZ) and (x-xo, y-y0, z-z0) are perpendicular, the 
        # scalar product must be zero, hence the equation:
        #
        #       (x - xo)*nX + (y - y0)*nY + (z - z0)*nZ = 0 
        #
        # The parametric equation of the line coming from the sun and going to the earth location is given by:
        #
        #       r(t) = P + t.D 
        #
        # where P is a point on the line and D is the direction vector. If we have 2 points (x0,y0,z0) (x1,y1,z1)
        # on the line, then the direction D = (x0 -x1, y0 -y1, z0 -z1)
        # the final eq is r(t) = (xloc, yloc, zloc) + t * (x0 -x1, y0 -y1, z0 -z1) with r(t) = (x,y,z)
        #
        # Soo, to find the line and plane intersec, we need to replace the coordinate of r(t) in the plane equation
        # and find the value of t. We then find r(t) by replacing the value of t in each coordinate.
        # 
        # in an EarthLocation context: 
        #   - the point belonging to the plane is self.GeoLoc * self.anaLemmaDistanceFactor
        #   - the normal vector to the plane is self.UnitGrad
        #   - the point of the line P is the Earth vertex self.GeoLoc
        #   - the direction D is Earth Vertex - Sun Vertex
        
        # first calculate t so that the intersection we are looking for verify the plane eqaution

        if self.analemmaIncrement < TI_FULL_YEAR:
            PlaneCenter = self.Widgets.PCPF.referential.frame_to_world(self.Widgets.OVRL.frame_to_world(self.Loc.GeoPlaneCenter))
            Normal = self.Widgets.PCPF.referential.frame_to_world(self.Widgets.OVRL.frame_to_world(self.Loc.UnitGrad))

            t = (PlaneCenter[0] - self.SunAxis.pos[self.SUN_VERTEX][0])*Normal[0] + \
                (PlaneCenter[1] - self.SunAxis.pos[self.SUN_VERTEX][1])*Normal[1] + \
                (PlaneCenter[2] - self.SunAxis.pos[self.SUN_VERTEX][2])*Normal[2]

            t = t / ((self.SunAxis.pos[self.SUN_VERTEX][0] - self.SunAxis.pos[self.EARTH_VERTEX][0])*Normal[0] +\
                    (self.SunAxis.pos[self.SUN_VERTEX][1] - self.SunAxis.pos[self.EARTH_VERTEX][1])*Normal[1] + \
                    (self.SunAxis.pos[self.SUN_VERTEX][2] - self.SunAxis.pos[self.EARTH_VERTEX][2])*Normal[2])
            # second, deduct the coordinates
            self.Intersec =       ( self.SunAxis.pos[self.SUN_VERTEX][0] + t * (self.SunAxis.pos[self.SUN_VERTEX][0] - self.SunAxis.pos[self.EARTH_VERTEX][0]),
                                    self.SunAxis.pos[self.SUN_VERTEX][1] + t * (self.SunAxis.pos[self.SUN_VERTEX][1] - self.SunAxis.pos[self.EARTH_VERTEX][1]),
                                    self.SunAxis.pos[self.SUN_VERTEX][2] + t * (self.SunAxis.pos[self.SUN_VERTEX][2] - self.SunAxis.pos[self.EARTH_VERTEX][2]))
            if self.Shape == None:
                self.Shape = curve(frame=self.Widgets.OVRL, color=Color.red, visible=True, radius=5, material=materials.emissive)
            
            # make sure the intersec is allowed (it must be between the sun and the 
            # earth location. If it's not, it means that the sun is bolow the horizon)
            if mag(vector(self.Intersec)) < mag(vector(self.Loc.EclipticPosition)):
                # add a point to the analemma shape until a full year is complete
                pos = self.Widgets.OVRL.world_to_frame(self.Widgets.PCPF.referential.world_to_frame(self.Intersec))
                self.Shape.append(pos= pos)
                self.analemmaIncrement = self.analemmaIncrement + self.Planet.SolarSystem.Dashboard.orbitalTab.TimeIncrement
        
    

"""
class makeAnalemmaSAVE():

    def __init__(self, widgets, locIndex = -1):
        # draw earth sun segment between center 
        # of sun and a point at a given latitude

#        self.Origin = widgets.PCINT
#        self.Origin = widgets.PCI
        self.Origin = widgets.Planet.Origin #widgets.PCPF.referential
        self.Planet = widgets.Planet
        self.Color = Color.red
        self.Widgets = widgets
        self.CurrentGeoLoc = sphere(frame=self.Origin, pos=(0,0,0), np=32, radius=50, material = materials.emissive, make_trail=True, color=self.Color, visible=True) 

        # compute semi-latus Rectum: L = a(1 - e**2)
        self.semiLactusRectum = widgets.Planet.a * (1 - widgets.Planet.e**2)

        #self.Trail = curve(frame=self.Origin, color=self.Color, visible=False, radius=25, material=materials.emissive)
        #self.Position = np.matrix([[0],[0],[0]], np.float64)

        # The equator holds the Asc and Desc objects as they are always along the equator line
        #self.AnaLemmaNode = makeNode(widgets, Color.green, ascending=True)
        #self.DesNode = makeNode(widgets, Color.red, ascending=False)

        # make plane
        self.makeSunAxis(locIndex)
        self.eqPlane = box(pos=self.Origin.pos, length=2*self.radius, width=0.0001, height=2*self.radius, material=materials.emissive, visible=True, color=self.Color, opacity=1)
        self.zob = False
        self.display(True)

    def setNoonPosition(self, loc):

        lat = 0.0
        #long = 0.0
        if loc != None:
            lat = loc["lat"]
            #lat = 85
            #long = loc["long"]

        # set the Geo position
        self.radius = (self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType])*0.999
        
        # calculate distance from z-axis to latitude line
        self.eqPlane = self.radius * cos(deg2rad(lat))

        # deduct (x,y) from eqPlane. Note, we need to extend the longitude 
        # value by 180 degrees to take into account the way the earth texture
        # was applied on the sphere
        self.CurrentGeoLoc.pos[0] = 0 #self.eqPlane * cos(deg2rad(long)) #+pi)
        self.CurrentGeoLoc.pos[1] = 0 #self.eqPlane * sin(deg2rad(long)) #+pi)
        self.CurrentGeoLoc.pos[2] = self.radius * sin(deg2rad(lat))

    def makeSunAxisNEW(self, locIndex):
        loc = None
        if locIndex != -1:
            loc = self.Planet.SolarSystem.locationInfo.getLocationInfo(locIndex)

        self.setNoonPosition(loc)
        self.SunAxisFrame = frame()
        self.SunAxisFrame.pos = self.Origin.frame_to_world(self.CurrentGeoLoc.pos)
        # create first vertex in sun at z coordinate = eareth latitude to create an axis parallel to ecliptic
#        self.SunAxis = curve(frame=self.SunAxisFrame, pos=[(0,0,self.CurrentGeoLoc.pos[2])], color=Color.green, visible=False,  material=materials.emissive, radius=0)
        self.SunAxis = curve(frame=self.SunAxisFrame, color=Color.green, visible=False,  material=materials.emissive, radius=0)

        # add point at latitude (0,0, self.radius * sin(lat)) in PCI, converted into fixed referential (frame_to_world)
#        self.SunAxis.append(pos=self.Origin.frame_to_world(self.CurrentGeoLoc.pos), color=Color.green)
        self.SunAxis.append(pos=[(0,0,self.CurrentGeoLoc.pos[2])], color=Color.green)
       

        
        #self.NodesAxis = curve( #frame=self.PCI, 
        #                        #pos=[(2 * (self.DesNode.Node.pos[0] - self.Planet.Position[0]), 0, 0), 
        #                        #    (2 * (self.AscNode.Node.pos[0] - self.Planet.Position[0]), 0, 0)], 
        #                        pos = [(self.Planet.Position[0],self.Planet.Position[1],self.Planet.Position[2]), (0,0,0)], 
        #                        color=Color.green, visible=True, radius=0, material=materials.emissive)
        #
        self.analemma = curve(frame=self.SunAxisFrame, pos=[(0,0,self.CurrentGeoLoc.pos[2])], color=Color.red, visible=False,  material=materials.emissive, radius=0)

    def makeSunAxis(self, locIndex):
        loc = None
        if locIndex != -1:
            loc = self.Planet.SolarSystem.locationInfo.getLocationInfo(locIndex)

        self.setNoonPosition(loc)
#        self.SunAxisFrame = frame()
#        self.SunAxisFrame.pos = self.Origin.frame_to_world(self.CurrentGeoLoc.pos)
        # create first vertex in sun at z coordinate = earth latitude to create an axis parallel to ecliptic
        self.SunAxis = curve(pos=[(0,0,self.CurrentGeoLoc.pos[2])], color=Color.green, visible=False,  material=materials.emissive, radius=0)
#        self.SunAxis = curve(pos=self.Origin.frame_to_world(self.CurrentGeoLoc.pos), color=Color.green, visible=False,  material=materials.emissive, radius=0)

        # add point at latitude (0,0, self.radius * sin(lat)) in PCI, converted into fixed referential (frame_to_world)
#        self.SunAxis.append(pos=self.Origin.frame_to_world(self.CurrentGeoLoc.pos), color=Color.green)
        self.SunAxis.append(pos=self.Origin.frame_to_world(self.CurrentGeoLoc.pos), color=Color.green)
    

        
        #self.NodesAxis = curve( #frame=self.PCI, 
        #                        #pos=[(2 * (self.DesNode.Node.pos[0] - self.Planet.Position[0]), 0, 0), 
        #                        #    (2 * (self.AscNode.Node.pos[0] - self.Planet.Position[0]), 0, 0)], 
        #                        pos = [(self.Planet.Position[0],self.Planet.Position[1],self.Planet.Position[2]), (0,0,0)], 
        #                        color=Color.green, visible=True, radius=0, material=materials.emissive)
        #
        self.analemma = curve(frame=self.Origin, pos=[(2*self.radius,2*self.radius,self.CurrentGeoLoc.pos[2])], color=Color.red, visible=True,  material=materials.emissive, radius=1000)
#        self.analemma = curve(frame=self.Origin, pos=[(0,0,self.CurrentGeoLoc.pos[2])], color=Color.red, visible=False,  material=materials.emissive, radius=0)

    def updateAnalemmaPosition(self):
        
        #self.sunPerspective = vector(0,0, self.radius)
        self.CurrentGeoLoc.pos[0] = 0 #self.eqPlane * cos(deg2rad(0)+pi)
        self.CurrentGeoLoc.pos[1] = 0 #self.eqPlane * sin(deg2rad(0)+pi)
        
        # update 2nd vertex position (earth)
        self.SunAxis.pos[1] = self.Origin.frame_to_world(self.CurrentGeoLoc.pos)
        #self.SunAxisFrame.pos = self.Origin.frame_to_world(self.CurrentGeoLoc.pos)

        self.Planet.SolarSystem.Dashboard.orbitalTab.TimeIncrement = TI_24_HOURS * 10 #EARTH_DAILY_MEAN_MOTION #EPHEMERIS_DAY # * 10 * 6
        self.Planet.SolarSystem.setTimeIncrement(self.Planet.SolarSystem.Dashboard.orbitalTab.TimeIncrement)

#        self.Planet.SolarSystem.Scene.forward = vector(self.Planet.Origin.pos - (0, 0, self.sunPerspective[2] + self.CurrentGeoLoc.pos[2]))
        self.Planet.SolarSystem.Scene.forward = vector(self.Planet.Origin.pos - (0, 0, self.CurrentGeoLoc.pos[2] + 5*self.radius))

        if self.zob == False:
            self.zob = True
            self.eqPlane.rotate(angle=90, axis=(getOrthogonalVector(self.Planet.SolarSystem.Scene.forward)))

        self.analemma.append(pos=self.CurrentGeoLoc.pos, color=Color.red)


    def updateAnalemmaPosition2(self):
        
        #The angular precession per orbit for an Earth orbiting satellite is given by
        #
        #delta = -(3*pi.J2.RE^2/p^2).cos(i)
        #
        #where
        #    J2 = 1.08263e-3 is the coefficient for the second zonal term related to the oblateness of the Earth,
        #    RE ~ 6378 km is the mean radius of the Earth,
        #    p is the semi-latus rectum of the orbit,
        #    i is the inclination of the orbit to the equator.        
        #
        J2 = 1.08263e-3
        precession = -3 * pi * cos(self.Planet.Inclination) * J2 * ((self.radius**2)/(self.semiLactusRectum**2)) 
        angle = precession * self.Planet.SolarSystem.Dashboard.orbitalTab.TimeIncrement/5400     
        print "increment = ", self.Planet.SolarSystem.Dashboard.orbitalTab.TimeIncrement

        self.CurrentGeoLoc.pos[0] = 0 #self.eqPlane * cos(deg2rad(0)+pi)
        self.CurrentGeoLoc.pos[1] = 0 #self.eqPlane * sin(deg2rad(0)+pi)
        self.SunAxis.pos[1] = self.Origin.frame_to_world(self.CurrentGeoLoc.pos)
        #self.SunAxis.append(pos=self.Origin.frame_to_world(self.CurrentGeoLoc.pos), color=Color.green)
        self.Planet.SolarSystem.Scene.forward = rotate(self.Planet.SolarSystem.Scene.forward, angle=-angle, axis=(0,0,1))
        
        #self.Planet.SolarSystem.Scene.forward = vector(self.Planet.SolarSystem.Scene.center)

    def display(self, trueFalse):
        self.SunAxis.visible = trueFalse
        self.CurrentGeoLoc.visible = trueFalse
"""