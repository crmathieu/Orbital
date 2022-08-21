from celestial.utils import getAngleBetweenVectors, getOrthogonalVector, getVectorOrthogonalToPlane, getXYprojection, getYZprojection
from orbit3D import *
from visual import *
#from objects import circle
from location import locList
from video import *
import rate_func

class makePlanetWidgets():

    ROT_CLKW = 64
    ROT_CCLKW = 128

    def __init__(self, planet):

        self.Planet = planet
        self.visible = True
        self.makeECEFref()
        self.Eq = self.eqPlane = self.Lons = self.Lats = None
        self.Psi = 0.0
        self.NumberOfSiderealDaysPerYear = 0.0
        self.SiderealCorrectionAngle = 0.0
        self.zoomToLocation = False
        self.Loc = []
        self.initWidgets()

    def makeECEFref(self):
        # this is the ECEF referential or GeoCentric referential 
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
        # Conversions between ECEF and geodetic coordinates (latitude and longitude) are discussed at 
        # geographic coordinate conversion. 

        self.ECEF = frame()     
        self.ECEF.pos = self.Planet.Origin.pos


    def resetWidgetsRefFromSolarTime(self):

        print "RESET WIDGET FROM SOLAR-TIME"
        if self.SiderealCorrectionAngle != 0.0:
            self.ECEF.rotate(angle=(-self.SiderealCorrectionAngle), axis=self.Planet.RotAxis) #, origin=(0,0,0))
            self.SiderealCorrectionAngle = 0.0

        print "Planet.Psi ....... ", self.Planet.Psi
        print "widgets.Psi ...... ", self.Psi
        self.ECEF.rotate(angle=(self.Planet.Psi-self.Psi), axis=self.Planet.RotAxis) #, origin=(0,0,0))


        # Psi is the initial rotation to apply on the sphere texture to match the solar Time
        self.Psi = self.Planet.Psi
        print "resetWidgetsRefFromSolarTime: Psi =", self.Psi


    def resetWidgetsReferencesFromNewDate(self): #, fl_diff_in_days):
        print "RESET WIDGETS REF"
        if self.SiderealCorrectionAngle != 0.0:
            # there has been a previous manual reset of the UTC date which has resulted in a sidereal 
            # correction. We need to undo it prior to reposition the texture for the new date
            self.ECEF.rotate(angle=(-self.SiderealCorrectionAngle), axis=self.Planet.RotAxis)

        self.SiderealCorrectionAngle = self.Planet.SiderealCorrectionAngle #(2 * pi / self.NumberOfSiderealDaysPerYear) * fl_diff_in_days
        self.ECEF.rotate(angle=(self.SiderealCorrectionAngle), axis=self.Planet.RotAxis) #, origin=(0,0,0))

    def initWidgets(self):
        self.NumberOfSiderealDaysPerYear = self.Planet.NumberOfSiderealDaysPerYear
        self.Eq = makeEquator(self)
        self.Tr = makeTropics(self)
        self.EqPlane = makeEquatorialPlane(self, color.orange, opacity=self.Planet.Opacity)
        self.Lons = makeLongitudes(self)
        self.Lats = makeLatitudes(self)
        self.tz = makeTimezones(self)
        self.Loc = []
        self.currentLocation = -1
        self.defaultLocation = -1
        #self.makeLocation(TZ_US_CAPE)
        self.makeMultipleLocations(locList.TZ_US_CAPE)
         
        # align widgets origin with planet tilt
        self.ECEF.rotate(angle=(-self.Planet.TiltAngle), axis=self.Planet.XdirectionUnit) #, origin=(0,0,0))

        # align longitude to greenwich when the planet is Earth
        if self.Planet.Name.lower() == EARTH_NAME:

            # adjust widgets positions in relation with earth texture at current time
            self.resetWidgetsRefFromSolarTime()
             
            # align GMT: the initial position of the GMT meridian on the texture is 6 hours
            # off its normal position. Ajusting by 6 hours x 15 degres = 90 degres
            self.ECEF.rotate(angle=(deg2rad(6*15)), axis=self.Planet.RotAxis) #ZdirectionUnit)
            
            # init position in ecliptic referential
            #self.updateCurrentLocationEcliptic()
            if self.currentLocation >= 0:
                self.Loc[self.currentLocation].updateEclipticPosition()

    

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
                self.Planet.SolarSystem.Dashboard.orbitalTab.VideoRecorder = setVideoRecording(25, "output.avi")


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
            self.C =  simpleArrow(color.yellow, 0, 20, self.Loc[self.defaultLocation].getEclipticPosition(), axisp = 0.1*vector(x,y,z), context = self.Loc[locationID].Origin) #, context = self.Planet.Origin) #self.Loc[self.defaultLocation].Origin)
            self.C =  simpleArrow(color.yellow, 0, 20, self.Planet.SolarSystem.Scene.mouse.camera, axisp = 1e4*self.Planet.SolarSystem.Scene.forward, context = None) #self.Loc[locationID].Origin) #, context = self.Planet.Origin) #self.Loc[self.defaultLocation].Origin)
            self.C.display(True)

            ortho = getOrthogonalVector(self.Planet.SolarSystem.Scene.forward)
            self.C =  simpleArrow(color.red, 0, 20, self.Planet.SolarSystem.Scene.mouse.camera, axisp = 1e4*ortho, context = None) #self.Loc[locationID].Origin)
            self.C.display(True)
            x = self.Planet.SolarSystem.Scene.forward[0]
            y = self.Planet.SolarSystem.Scene.forward[1]
            z = self.Planet.SolarSystem.Scene.forward[2]
            print "(XF,YF,ZF)=(",x,",",y,",",z,")"

            self.C =  simpleArrow(color.red, 0, 20, curPos, axisp = 20*vector(x,y,z), context = self.Planet.Origin) #, context = self.Loc[self.defaultLocation].Origin)
            self.C.display(True)


        self.V =  simpleArrow(color.green, 0, 20, nextPos, axisp = self.Loc[locationID].Grad/10, context = self.Loc[locationID].Origin) #self.Loc[self.defaultLocation].Origin)
        self.V.display(True)

        EC = self.Loc[locationID].getEclipticPosition()
        A = EC[0] - self.Planet.Origin.pos[0] #self.Planet.Origin.pos[0]
        B = EC[1] - self.Planet.Origin.pos[1] #self.Planet.Origin.pos[1]
        C = EC[2] - self.Planet.Origin.pos[2] #self.Planet.Origin.pos[2] 

        #self.D =  simpleArrow(color.white, 0, 20, self.Planet.Origin.pos, axisp = 5*vector(A,B,C), context = None) #self.Loc[locationID].Origin) #self.Loc[self.defaultLocation].Origin)
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
                self.Planet.SolarSystem.Dashboard.orbitalTab.VideoRecorder = setVideoRecording(25, "output.avi")

        # Calculate number of steps based on current transition velocity factor (default is 1.0)
        total_steps = int(100) * self.Planet.SolarSystem.camera.transitionVelocityFactor
        #print ("Smooth Focus TOTAL_STEPS=", total_steps)

        #dX = (self.Planet.SolarSystem.Scene.forward[0] - A)
        #dY = (self.Planet.SolarSystem.Scene.forward[1] - B)
        #dZ = (self.Planet.SolarSystem.Scene.forward[2] - C)
        Initial = -self.Planet.SolarSystem.Scene.forward


        rotAxis = getVectorOrthogonalToPlane(Initial, vector(A,B,C))
        self.K =  simpleArrow(color.cyan, 0, 20, self.Planet.SolarSystem.Scene.mouse.camera, axisp = 1e4*rotAxis, context = None) #self.Loc[locationID].Origin)
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
        la_dangle = 0.0
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

        # set current and next coordinates in ICE referential

        curPos = self.Loc[self.defaultLocation].getGeoPosition()
        nextPos = self.Loc[locationID].getGeoPosition()

        # calculate angle between normal of camera location and normal vector in next location. 
        # Here (x,y,z) is the vector between camera location and center of earth
        
        x = self.Planet.SolarSystem.Scene.mouse.camera[0] - self.Planet.Origin.pos[0]
        y = self.Planet.SolarSystem.Scene.mouse.camera[1] - self.Planet.Origin.pos[1]
        z = self.Planet.SolarSystem.Scene.mouse.camera[2] - self.Planet.Origin.pos[2] 

        long_diff = getAngleBetweenVectors(self.Loc[locationID].Grad, -vector(x,y,z))

        self.B =  simpleArrow(color.green, 0, 20, nextPos, axisp = self.Loc[locationID].Grad/10, context = self.Loc[locationID].Origin) #self.Loc[self.defaultLocation].Origin)
        self.B.display(True)

        if False:
            self.Z =  simpleArrow(color.magenta, 20, 20, self.Planet.Origin.pos, axisp = vector(x,y,z), context =None)
            if self.Z != None:
                self.Z.display(True)

            self.A =  simpleArrow(color.yellow, 0, 20, nextPos, axisp = self.Loc[self.defaultLocation].Grad/10, context = self.Loc[self.defaultLocation].Origin) #self.Loc[self.defaultLocation].Origin)
            self.A.display(True)
            self.B =  simpleArrow(color.green, 0, 20, nextPos, axisp = self.Loc[locationID].Grad/10, context = self.Loc[locationID].Origin) #self.Loc[self.defaultLocation].Origin)
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
        self.defaultLocation = 0
        #self.currentLocation = 0
        self.Loc.append(makeEarthLocation(self, locIndex))

    def updateWidgetsFrameRotation(self, timeIncrement):
        # here we rotate the widgets by the same amount the earth texture is rotated
        ti = self.Planet.SolarSystem.getTimeIncrement()
        RotAngle = (2*pi/self.Planet.Rotation)*ti
        #RotAngle = (2*pi/self.Planet.Rotation)*timeIncrement
        # if polar axis inverted, reverse rotational direction
        if self.Planet.ZdirectionUnit[2] < 0:
            RotAngle *= -1

        # follow planet rotation
        self.ECEF.rotate(angle=RotAngle, axis=self.Planet.RotAxis, origin=self.ECEF.pos) #(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]))


    def updateWidgetsFramePosition(self):
        self.ECEF.pos = self.Planet.Origin.pos

    def updateCurrentLocationEcliptic(self):
        if self.currentLocation >= 0: 
            self.Loc[self.currentLocation].updateEclipticPosition()

    def animate(self, timeIncrement):
        self.updateWidgetsFramePosition()
        self.updateWidgetsFrameRotation(timeIncrement)
        self.Eq.updateNodesPosition()
        self.updateCurrentLocationEcliptic()
        self.EqPlane.updateEquatorialPlanePosition()	

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
    def __init__(self, widgets, tz_index):
        self.Origin = widgets.ECEF
        self.Planet = widgets.Planet
        self.Color = color.red
        self.EclipticPosition = vector(0,0,0)
        self.lat = self.long = 0
        self.GeoLoc = sphere(frame=self.Origin, pos=(0,0,0), np=32, radius=20, material = materials.emissive, make_trail=false, color=self.Color, visible=True) 
        #self.GeoLoc = cylinder(frame=self.Origin, pos=vector(0,0,0), radius=10, color=self.Color, material = materials.emissive, opacity=1.0, axis=(0,0,1))


        #self.GeoLoc = circle(color=self.Color, radius=10, pos=(0,0,0), normalAxis=(0,0,1), context=self.Origin)        
        self.Origin.axis.visible = True

        # obtain location info. Earthloc is a tuple (lat, long, timezone)
        earthLoc = self.Planet.SolarSystem.locationInfo.getLocationInfo(tz_index)
        if earthLoc != {}:
            print earthLoc
            self.Name = earthLoc["name"]
            self.lat = earthLoc["lat"]
            self.long = earthLoc["long"]
            self.setPosition() #earthLoc)
            self.setNormalToSurface()
            self.setOrientation(self.Grad)

        else:
            self.Name = "None"
    """
    def setPositionSAVE(self, locInfo):
        # set the Geo position
        radius = (self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType])*0.999
        
        # calculate distance from z-axis to latitude line
        eqPlane = radius * cos(deg2rad(locInfo["lat"]))

        # deduct (x,y) from eqPlane. Note, we need to extend the longitude 
        # value by 180 degrees to take into account the way the earth texture
        # was applied on the sphere
        self.GeoLoc.pos[X_COOR] = eqPlane * cos(deg2rad(locInfo["long"])+pi)
        self.GeoLoc.pos[Y_COOR] = eqPlane * sin(deg2rad(locInfo["long"])+pi)
        self.GeoLoc.pos[Z_COOR] = radius * sin(deg2rad(locInfo["lat"]))
    """

    def setPosition(self):
        # set the Geo position
        radius = (self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType])*0.999
        
        # calculate distance from z-axis to latitude line
        eqPlane = radius * cos(deg2rad(self.lat))

        # deduct (x,y) from eqPlane. Note, we need to extend the longitude 
        # value by 180 degrees to take into account the way the earth texture
        # was applied on the sphere
        self.GeoLoc.pos[0] = eqPlane * cos(deg2rad(self.long)+pi)
        self.GeoLoc.pos[1] = eqPlane * sin(deg2rad(self.long)+pi)
        self.GeoLoc.pos[2] = radius * sin(deg2rad(self.lat))

    def getPosition(self):
        return self.GeoLoc.pos

    def updateEclipticPosition(self):
        # init position in ecliptic referential
        self.EclipticPosition = self.Origin.frame_to_world(self.GeoLoc.pos)

    def getEclipticPosition(self):
        # return ecliptic coordinates
        return self.EclipticPosition

    def getGeoPosition(self):
        # return ECEF coordinates
        return self.GeoLoc.pos

    def display(self, trueFalse):
        self.GeoLoc.visible = trueFalse

    def setNormalToSurface(self):
        # the equation of the earth surface is S: (x-xcenter)^2 + (y-ycenter)^2 + (z-zcenter)^2 = R^2
        # the coordinates of a vector normal to the earth surface is given by the earth's surface gradient:
        #   Gradient(S) = (DS/Dx, DS/Dy, DS/Dz)
        # DS/Dx = 2(x-xcenter) partial derivative of surface for x
        # DS/Dy = 2(y-ycenter) partial derivative of surface for y 
        # DS/Dz = 2(z-zcenter) partial derivative of surface for z
        # the normal vector in our location is given by [xloc+DS/Dx(loc)]
        self.updateEclipticPosition()
        self.GradientX = 2*(self.EclipticPosition[0]-self.Origin.pos[0])
        self.GradientY = 2*(self.EclipticPosition[1]-self.Origin.pos[1])
        self.GradientZ = 2*(self.EclipticPosition[2]-self.Origin.pos[2])
        self.Grad = vector(self.GradientX, self.GradientY, self.GradientZ)
        
        self.NormalVec = simpleArrow(color.white, 0, 10, self.GeoLoc.pos, axisp = (self.Grad/10), context = self.Origin)
        self.NormalVec.display(False)

    def setOrientation(self, axis):
        self.GeoLoc.axis = axis * (1 / mag(axis))

    def show(self, trueFalse):
        self.NormalVec.display(trueFalse)



class makeNode():
    def __init__(self, widgets, colr, ascending = true):
        #self.Origin = widgets.ECEF
        self.Planet = widgets.Planet
        self.Color = colr
        self.ascending = -1 if ascending else 1

        # Note: the nodes can't be attached to the widgets frame, as we don't 
        # want the nodes to rotate with the frame during an animation. That's
        # why their position needs to be updated by an external animation
        # routine using the "updateNodesPosition" method.

        self.Node = sphere(pos=(0,0,0), np=32, radius=100, make_trail=false, color=self.Color, visible=False) 
        self.updatePosition()


    def updatePosition(self):
        self.Node.pos[X_COOR] = self.ascending * self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType] + self.Planet.Position[X_COOR]
        self.Node.pos[Y_COOR] = self.Planet.Position[Y_COOR]
        self.Node.pos[Z_COOR] = self.Planet.Position[Z_COOR]


    def display(self, trueFalse):
        self.Node.visible = trueFalse


class makeEquator():

    def __init__(self, widgets): #planet):
        self.Origin = widgets.ECEF
        self.Planet = widgets.Planet
        self.Color = color.red

        self.Trail = curve(frame=self.Origin, color=self.Color, visible=False, radius=25, material=materials.emissive)
        self.Position = np.matrix([[0],[0],[0]], np.float64)

        # The equator holds the Asc and Des objects as they are always along the equator line
        self.AscNode = makeNode(widgets, color.green, ascending=True)
        self.DesNode = makeNode(widgets, color.red, ascending=False)

        self.draw()


    def display(self, trueFalse):
        self.Trail.visible = trueFalse

    def draw(self):
        increment = pi/180
        for E in np.arange(0, 2*pi+increment, increment):
            # build Equator line using angular segments of increments degres
            self.drawSegment(E)


    def drawSegment(self, E, trace = True):
        self.setCartesianCoordinates(E)

        # add angular portion of equator
        self.Trail.append(pos= vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]), color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))


    def setCartesianCoordinates(self, angleIncr):
        radius = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]

        self.Position[X_COOR] = radius * cos(angleIncr) 
        self.Position[Y_COOR] = radius * sin(angleIncr)
        self.Position[Z_COOR] = 0


    def showNodes(self, trueFalse):
        self.AscNode.display(trueFalse)
        self.DesNode.display(trueFalse)


    def updateNodesPosition(self):
        self.AscNode.updatePosition()
        self.DesNode.updatePosition()


class makeEquatorialPlane():

    def __init__(self, widgets, color, opacity): #planet, color, opacity):
        
        self.Planet = widgets.Planet
        self.Opacity = opacity
        self.Color = color 

        side = 2.5*AU*DIST_FACTOR
        self.eqPlane = box(pos=self.Planet.Position, length=side, width=0.0001, height=side, material=materials.emissive, visible=True, color=self.Color, opacity=0) #, axis=(0, 0, 1), opacity=0.8) #opacity=self.Opacity)
        self.eqPlane.rotate(angle=(-self.Planet.TiltAngle), axis=self.Planet.XdirectionUnit) #, origin=(0,0,0))


    def updateEquatorialPlanePosition(self):
        self.eqPlane.pos[X_COOR] = self.Planet.Position[X_COOR]
        self.eqPlane.pos[Y_COOR] = self.Planet.Position[Y_COOR]
        self.eqPlane.pos[Z_COOR] = self.Planet.Position[Z_COOR]


    def display(self, trueFalse):
        STEPS = 10
        if trueFalse == True:
            bound = 0
        else:
            bound = STEPS-1
        
        for i in range(STEPS):
            self.eqPlane.opacity = float(abs(bound-i))/STEPS
            sleep(1e-2)


class doMeridian():

    def __init__(self, widgets, colr, longitudeAngle):
        self.longAngle = longitudeAngle
        self.Origin = widgets.ECEF

        self.Planet = widgets.Planet
        #Radius = 25 if longitudeAngle == 0 else 0
        self.Trail = curve(frame=self.Origin, color=colr, visible=False,  material=materials.emissive, radius=(25 if longitudeAngle == 0 else 0))
        self.Position = np.matrix([[0],[0],[0]], np.float64)
        self.Color = colr #color.cyan
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
        self.Position[X_COOR] = projectionOnXYplane * cos(self.longAngle)
        self.Position[Y_COOR] = projectionOnXYplane * sin(self.longAngle)
        self.Position[Z_COOR] = radius * sin(angleIncr)


    def drawSegment(self, E, trace = True):
        self.setCartesianCoordinates(E)
        newpos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])

        # add angular portion of longitude curve
        self.Trail.append(pos=newpos, color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))

class makeMeridians():
    def __init__(self, widgets, colr):
        self.Origin = widgets.ECEF
        self.Widgets = widgets
        self.Origin.visible = True
        self.Color = colr
        self.Meridians = []


    def display(self, trueFalse):
        for mrd in self.Meridians:
            mrd.display(trueFalse)


    def draw(self, angle, origColr):
        colr = origColr #color.red
        for i in np.arange(0, pi, deg2rad(angle)):
            # build Meridians by longitude circles
            self.Meridians.append(doMeridian(self.Widgets, colr, i))
            colr = self.Color


class makeLongitudes(makeMeridians):
        
    def __init__(self, widgets):

        makeMeridians.__init__(self, widgets, color.cyan)
        self.draw(10, color.red)


class makeTimezones(makeMeridians):
        
    def __init__(self, widgets):
        makeMeridians.__init__(self, widgets, color.white)
        self.draw(15, color.white)


class doLatitude():

    def __init__(self, widgets, latitudeAngle, colr, thickness=0):
        self.latAngle = latitudeAngle
        self.Origin = widgets.ECEF
        self.Color = colr

        self.Planet = widgets.Planet
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

        self.Position[X_COOR] = projection * sin(angleIncr)
        self.Position[Y_COOR] = projection * cos(angleIncr)
        self.Position[Z_COOR] = radius * sin(self.latAngle)


    def drawSegment(self, E):
        self.setCartesianCoordinates(E)
        newpos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])

        # add angular portion of latitude curve
        self.Trail.append(pos=newpos, color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))


class makeLatitudes():
        
    def __init__(self, widgets):
        self.Origin = widgets.ECEF
        self.Widgets = widgets
        self.lats = []
        self.Color = color.cyan
        self.draw()


    def display(self, trueFalse):
        for lat in self.lats:
            lat.display(trueFalse)


    def draw(self):
        for i in np.arange(-pi/2, pi/2, deg2rad(10)):
            # build latitudes levels every 10deg from -90 to +90            
            self.lats.append(doLatitude(self.Widgets, i, color.cyan))


class makeTropics():
        
    def __init__(self, widgets):
        self.Origin = widgets.ECEF
        self.Widgets = widgets
        self.Tropics = []
        self.Color = color.cyan
        self.TROPIC_ABS_LATITUDES = deg2rad(23.5)
        self.draw()


    def display(self, trueFalse):
        for trop in self.Tropics:
            trop.display(trueFalse)


    def draw(self):
        # build latitudes levels every 10deg from -90 to +90            
        self.Tropics.append(doLatitude(self.Widgets, -self.TROPIC_ABS_LATITUDES, color.yellow, thickness=25))
        self.Tropics.append(doLatitude(self.Widgets, +self.TROPIC_ABS_LATITUDES, color.yellow, thickness=25))
