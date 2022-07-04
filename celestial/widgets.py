from orbit3D import *
from visual import *
from objects import circle

class makePlanetWidgets():

    def __init__(self, planet):

        self.Planet = planet
        self.visible = True
        self.makeECEFref()
        self.Eq = self.eqPlane = self.Lons = self.Lats = None
        self.Psi = 0.0
        self.NumberOfSiderealDaysPerYear = 0.0
        self.SiderealCorrectionAngle = 0.0
        self.Loc = []
        self.initWidgets()

    def makeECEFref(self):
        # this is the ECEF referential or GeoCentric referential 
        # The "Earth-centered, Earth-fixed coordinate system": fixed to the earth (moves with its rotation)
        # is a cartesian spatial reference system that represents locations in the vicinity of the 
        # Earth (including its surface, interior, atmosphere, and surrounding outer space) as X, Y, and Z 
        # measurements from its center of mass.[1][2] Its most common use is in tracking the orbits of 
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

    def resetWidgetsRefFromSolarTime_SAVE(self):

        if self.SiderealCorrectionAngle != 0.0:
            self.ECEF.rotate(angle=(-self.SiderealCorrectionAngle), axis=self.Planet.RotAxis) #, origin=(0,0,0))
            self.SiderealCorrectionAngle = 0.0

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
        #self.makeLocation(TZ_CAPE)
        self.makeMultipleLocations(TZ_CAPE)
         
        # align widgets origin with planet tilt
        self.ECEF.rotate(angle=(-self.Planet.TiltAngle), axis=self.Planet.XdirectionUnit) #, origin=(0,0,0))

        # align longitude to greenwich when the planet is Earth
        if self.Planet.Name.upper() == "EARTH":

            # adjust widgets positions in relation with earth texture at current time
            self.resetWidgetsRefFromSolarTime()
             
            # align GMT: the initial position of the GMT meridian on the texture is 6 hours
            # off its normal position. Ajusting by 6 hours x 15 degres = 90 degres
            self.ECEF.rotate(angle=(deg2rad(6*15)), axis=self.Planet.RotAxis) #ZdirectionUnit)
            
            # init position in ecliptic referential
            #self.updateCurrentLocationEcliptic()
            if self.currentLocation >= 0:
                self.Loc[self.currentLocation].updateEclipticPosition()


    def shiftLocation(self):
        #print "going from ",self.Loc[self.defaultLocation].GeoLoc.pos , "to", self.Loc[TZ_PARIS].GeoLoc.pos
        print "BEFORE: Forward=", self.Planet.SolarSystem.Scene.forward
        gradNorm = mag(self.Loc[self.defaultLocation].Grad) # + self.Loc[self.defaultLocation].EclipticPosition)
        print "BEFORE: NORMAL=", self.Loc[self.defaultLocation].Grad+ self.Loc[self.defaultLocation].EclipticPosition, "Normalized:", (self.Loc[self.defaultLocation].Grad + self.Loc[self.defaultLocation].EclipticPosition)/gradNorm
        X = (self.Planet.SolarSystem.Scene.forward[0]-self.Loc[self.defaultLocation].Grad[0])/(100*gradNorm)
        Y = (self.Planet.SolarSystem.Scene.forward[1]-self.Loc[self.defaultLocation].Grad[1])/(100*gradNorm)
        Z = (self.Planet.SolarSystem.Scene.forward[2]-self.Loc[self.defaultLocation].Grad[2])/(100*gradNorm)

#        X = (self.Planet.SolarSystem.Scene.forward[0]-((self.Loc[self.defaultLocation].Grad[0]+self.Loc[self.defaultLocation].EclipticPosition[0])/gradNorm))/100
#        Y = (self.Planet.SolarSystem.Scene.forward[1]-((self.Loc[self.defaultLocation].Grad[1]+self.Loc[self.defaultLocation].EclipticPosition[1])/gradNorm))/100
#        Z = (self.Planet.SolarSystem.Scene.forward[2]-((self.Loc[self.defaultLocation].Grad[2]+self.Loc[self.defaultLocation].EclipticPosition[2])/gradNorm))/100


#        for i in np.arange(0, self.Planet.SolarSystem.Scene.forward[0], self.Planet.SolarSystem.Scene.forward[0]/100):
        print "X=", X, ", Y=", Y,", Z=", Z
        X0 = self.Planet.SolarSystem.Scene.forward[0]
        Y0 = self.Planet.SolarSystem.Scene.forward[1]
        Z0 = self.Planet.SolarSystem.Scene.forward[2]
        print "X0=", X0, ", Y0=", Y0,", Z0=", Z0
        for i in np.arange(0, 100, 1):
            g = mag(vector( X0 + 100*i*X, Y0 + 100*i*Y, Z0 + 100*i*Z))
            self.Planet.SolarSystem.Scene.forward = vector( (X0 + 100*i*X)/g,
                                                            (Y0 + 100*i*Y)/g,
                                                            (Z0 + 100*i*Z)/g)
            sleep(1e-2)
            #self.Planet.SolarSystem.camera.cameraRefresh()
            #print "forward=", self.Planet.SolarSystem.Scene.forward

        raw_input()
#        self.Planet.SolarSystem.Scene.forward = (self.Loc[self.defaultLocation].Grad + self.Loc[self.defaultLocation].EclipticPosition)/mag(self.Loc[self.defaultLocation].Grad + self.Loc[self.defaultLocation].EclipticPosition)
        self.Planet.SolarSystem.Scene.forward = -(self.Loc[self.defaultLocation].Grad)/mag(self.Loc[self.defaultLocation].Grad)
        sleep(1e-2)
        raw_input()
#        self.zob =  simpleArrow(color.red, 70, 20, self.Loc[self.defaultLocation].GeoLoc.pos, axisp = 1e5*(self.Planet.SolarSystem.Scene.forward), context = self.Loc[self.defaultLocation].Origin)
        self.zob =  simpleArrow(color.red, 70, 20, self.Planet.SolarSystem.Scene.center, axisp = 1e5*(self.Planet.SolarSystem.Scene.forward), context = None) #self.Loc[self.defaultLocation].Origin)
        self.zob.display(True)
        #self.Planet.SolarSystem.Scene.forward = self.Loc[self.defaultLocation].Grad
        """
        print "Forward=", self.Planet.SolarSystem.Scene.forward
        raw_input()
        self.Planet.SolarSystem.Scene.forward = vector(0,1,0)
        print "Forward=", self.Planet.SolarSystem.Scene.forward
        raw_input()
        self.Planet.SolarSystem.Scene.forward = vector(1,0,0)
        print "Forward=", self.Planet.SolarSystem.Scene.forward
        raw_input()
        self.Planet.SolarSystem.Scene.forward = vector(0,0,1)
        print "Forward=", self.Planet.SolarSystem.Scene.forward

        #zob = self.Planet.SolarSystem.Scene.forward[0]/100
        #for i in np.arange(0, self.Planet.SolarSystem.Scene.forward[0], self.Planet.SolarSystem.Scene.forward[0]/100):
        
        #self.Planet.SolarSystem.Scene.forward = vector(0,1,1)
        """
        print "AFTER: Forward=", self.Planet.SolarSystem.Scene.forward
       # raw_input()

    def makeMultipleLocations(self, defaultLoc):
        self.defaultLocation = defaultLoc
        #self.currentLocation = defaultLoc
        for i in np.arange(0, len(locationInfo.tzEarthLocations), 1):
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
        self.GeoLoc = sphere(frame=self.Origin, pos=(0,0,0), np=32, radius=2, material = materials.emissive, make_trail=false, color=self.Color, visible=True) 
        #self.GeoLoc = cylinder(frame=self.Origin, pos=vector(0,0,0), radius=10, color=self.Color, material = materials.emissive, opacity=1.0, axis=(0,0,1))


        #self.GeoLoc = circle(color=self.Color, radius=10, pos=(0,0,0), normalAxis=(0,0,1), context=self.Origin)        
        self.Origin.axis.visible = True

        # obtain location info. Earthloc is a tuple (lat, long, timezone)
        earthLoc = locationInfo.getLocationInfo(tz_index)
        if earthLoc != {}:
            print earthLoc
            self.Name = earthLoc["name"]
            self.lat = earthLoc["lat"]
            self.long = earthLoc["long"]
            self.setPosition() #earthLoc)
            self.setGradient()
            self.setOrientation(self.Grad)

        else:
            self.Name = "None"

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

    def setPosition(self):
        # set the Geo position
        radius = (self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType])*0.999
        
        # calculate distance from z-axis to latitude line
        eqPlane = radius * cos(deg2rad(self.lat))

        # deduct (x,y) from eqPlane. Note, we need to extend the longitude 
        # value by 180 degrees to take into account the way the earth texture
        # was applied on the sphere
        self.GeoLoc.pos[X_COOR] = eqPlane * cos(deg2rad(self.long)+pi)
        self.GeoLoc.pos[Y_COOR] = eqPlane * sin(deg2rad(self.long)+pi)
        self.GeoLoc.pos[Z_COOR] = radius * sin(deg2rad(self.lat))

    def updateEclipticPosition(self):
        # init position in ecliptic referential
        self.EclipticPosition = self.Origin.frame_to_world(self.GeoLoc.pos)

    def getEclipticPosition(self):
        # return ecliptic coordinates
        return self.EclipticPosition

    def getGeo(self):
        # return ecliptic coordinates
        return self.GeoLoc.pos

    def display(self, trueFalse):
        self.GeoLoc.visible = trueFalse

    def setGradient(self):
        # the equation of the earth surface is S: (x-xcenter)^2 + (y-ycenter)^2 + (z-zcenter)^2 = R^2
        # DS/Dx = 2(x-xcenter) 
        # DS/Dy = 2(y-ycenter)  
        # DS/Dz = 2(z-zcenter)
        # the normal vector in our location is given by [xloc+DS/Dx(loc)]
        self.updateEclipticPosition()
        self.GradientX = 2*(self.EclipticPosition[X_COOR]-self.Origin.pos[X_COOR])
        self.GradientY = 2*(self.EclipticPosition[Y_COOR]-self.Origin.pos[Y_COOR])
        self.GradientZ = 2*(self.EclipticPosition[Z_COOR]-self.Origin.pos[Z_COOR])
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
        self.eqPlane = box(pos=self.Planet.Position, length=side, width=0.0001, height=side, material=materials.emissive, visible=False, color=self.Color, opacity=0.9) #, axis=(0, 0, 1), opacity=0.8) #opacity=self.Opacity)
        self.eqPlane.rotate(angle=(-self.Planet.TiltAngle), axis=self.Planet.XdirectionUnit) #, origin=(0,0,0))


    def updateEquatorialPlanePosition(self):
        self.eqPlane.pos[X_COOR] = self.Planet.Position[X_COOR]
        self.eqPlane.pos[Y_COOR] = self.Planet.Position[Y_COOR]
        self.eqPlane.pos[Z_COOR] = self.Planet.Position[Z_COOR]


    def display(self, trueFalse):
        self.eqPlane.visible = trueFalse


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
