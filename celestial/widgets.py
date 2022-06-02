from orbit3D import *
from visual import *

class makePlanetWidgets():

    def __init__(self, planet):
        self.Origin = frame()
        self.Origin.pos = planet.Origin.pos
        self.Planet = planet
        self.visible = True
        self.Eq = self.eqPlane = self.Lons = self.Lats = None
        self.Psi = 0.0
        self.initWidgets()

    def alignWidgetsReferences(self):
        self.Origin.rotate(angle=(-self.Psi), axis=self.Planet.RotAxis) #, origin=(0,0,0))
        self.Origin.rotate(angle=(self.Planet.Psi), axis=self.Planet.RotAxis) #, origin=(0,0,0))
        
        # Psi is the initial rotation to apply on the sphere texture to match the solar Time
        self.Psi = self.Planet.Psi
        print "alignWidgetsReferences: Psi =", self.Psi


    def initWidgets(self):

        self.Eq = makeEquator(self)
        self.Tr = makeTropics(self)
        self.EqPlane = makeEquatorialPlane(self, color.orange, opacity=self.Planet.Opacity)
        self.Lons = makeLongitudes(self)
        self.Lats = makeLatitudes(self)

        # align with planet tilt
        self.Origin.rotate(angle=(self.Planet.TiltAngle), axis=self.Planet.XdirectionUnit) #, origin=(0,0,0))

        # align longitude to greenwich when the planet is Earth
        if self.Planet.Name.upper() == "EARTH":
            # add equivalent texture rotation to map current time
            ##########self.Origin.rotate(angle=(self.Planet.Psi), axis=self.Planet.RotAxis) #, origin=(0,0,0))
            ##########print "LOCAL initial Angle =", self.Planet.Psi
            self.alignWidgetsReferences()

            # align GMT: the initial position of the GMT meridian on the texture is 6 hours
            # off its normal position. Ajusting by 6 hours x 15 degres = 90 degres
            self.Origin.rotate(angle=(deg2rad(6*15)), axis=self.Planet.ZdirectionUnit)


#            self.Origin.rotate(angle=(self.Planet.LocalInitialAngle), axis=self.Planet.RotAxis) #, origin=(0,0,0))
#            print "LOCAL initial Angle =", self.Planet.LocalInitialAngle
            # adjust local time with daylight saving info to calculate how much 
            # we have to rotate our frame to match greenwitch as meridian zero 
            if False:
                delta = -1
                if locationInfo.longitude < 0:
                    delta = 12 - (locationInfo.TimeToEASTdateline/3600 + 1 if bool(locationInfo.localdatetime.dst()) else 0)
                else:
                    delta = (locationInfo.TimeToEASTdateline/3600 + 1 if bool(locationInfo.localdatetime.dst()) else 0)

                # convert hours in degres (an hour is 15 degres)
                print ("delta LONG ROT={0}".format(delta))
                self.Origin.rotate(angle=(deg2rad(-delta*15)), axis=self.Planet.ZdirectionUnit)

            """
            delta = self.Planet.iDelta/15 # initial angle between orbital curve tg and x axis
            if locationInfo.longitude < 0:
                delta = delta + 12 - locationInfo.TimeToWESTdateline
            else:
                delta = delta + locationInfo.TimeToWESTdateline
            print "DELTA ..........................", delta, "hours,", delta*15, "degrees"
            #delta = locationInfo.TimeToWESTdateline + locationInfo.angTime * locationInfo.longitudeSign
            #delta = locationInfo.angTime * locationInfo.longitudeSign
            print "time to date line .... ", locationInfo.TimeToWESTdateline
            print "time to UTC .......... ", locationInfo.angTime
            print ("delta LONG ROT={0}".format(delta))
            #self.Origin.rotate(angle=(deg2rad(-delta*15)), axis=self.Planet.ZdirectionUnit)
            self.Origin.rotate(angle=(deg2rad(delta*15)), axis=self.Planet.ZdirectionUnit)
            """

    def updateWidgetsRotation(self):
        ti = self.Planet.SolarSystem.getTimeIncrement()
        RotAngle = (2*pi/self.Planet.Rotation)*ti
        # if polar axis inverted, reverse rotational direction
        if self.Planet.ZdirectionUnit[2] < 0:
            RotAngle *= -1

        # follow planet rotation
        self.Origin.rotate(angle=RotAngle, axis=self.Planet.RotAxis, origin=self.Origin.pos) #(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR]))


    def updateWidgetsPosition(self):
        self.Origin.pos = self.Planet.Origin.pos

    def animate(self):
        self.updateWidgetsPosition()
        self.updateWidgetsRotation()
        self.Eq.updateNodesPosition()
        #self.Eq.refreshNodes()	
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

    def showNodes(self, value):
        self.Eq.showNodes(value)

class makeNode():
    def __init__(self, widgets, colr, ascending = true):
        #self.Origin = widgets.Origin
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
        self.Origin = widgets.Origin
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
            self.updatePosition(E)

    def setCartesianCoordinates(self, angleIncr):
        radius = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]

        self.Position[X_COOR] = radius * cos(angleIncr) 
        self.Position[Y_COOR] = radius * sin(angleIncr)
        self.Position[Z_COOR] = 0

    def updatePosition(self, E, trace = True):
        self.setCartesianCoordinates(E)

        # add angular portion of equator
        self.Trail.append(pos= vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]), color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))

    def showNodes(self, trueFalse):
        self.AscNode.display(trueFalse)
        self.DesNode.display(trueFalse)

    def updateNodesPosition(self):
        self.AscNode.updatePosition()
        self.DesNode.updatePosition()


class makeEquator_SAVE():

    def __init__(self, widgets): #planet):
        self.Origin = widgets.Origin
        self.Planet = widgets.Planet
        self.Color = color.red

        self.Trail = curve(frame=self.Origin, color=self.Color, visible=False, radius=25, material=materials.emissive)
        self.Position = np.matrix([[0],[0],[0]], np.float64)
        self.AscNodePos = np.matrix([[0],[0],[0]], np.float64)
        self.DesNodePos = np.matrix([[0],[0],[0]], np.float64)


        self.draw()
        self.setNodes()
        self.showNodes(False)

    def display(self, trueFalse):
        self.Trail.visible = trueFalse

    def draw(self):
        increment = pi/180
        for E in np.arange(0, 2*pi+increment, increment):
            # build Equator line using angular segments of increments degres
            self.updatePosition(E)


    def setCartesianCoordinates(self, angleIncr):
        radius = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]

        self.Position[X_COOR] = radius * cos(angleIncr) 
        self.Position[Y_COOR] = radius * sin(angleIncr)
        self.Position[Z_COOR] = 0


    def updatePosition(self, E, trace = True):
        self.setCartesianCoordinates(E)

        # add angular portion of equator
        self.Trail.append(pos= vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]), color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))

    def showNodes(self, trueFalse):
        self.AscNode.visible = trueFalse
        self.DesNode.visible = trueFalse

    def updateNodesPosition(self):
        self.AscNodePos[X_COOR] = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType] + self.Planet.Position[X_COOR]
        self.AscNodePos[Y_COOR] = self.Planet.Position[Y_COOR]
        self.AscNodePos[Z_COOR] = self.Planet.Position[Z_COOR]
        self.DesNodePos[X_COOR] = -self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType] + self.Planet.Position[X_COOR]
        self.DesNodePos[Y_COOR] = self.Planet.Position[Y_COOR]
        self.DesNodePos[Z_COOR] = self.Planet.Position[Z_COOR]

    def refreshNodes(self):
        self.AscNode.pos = self.AscNodePos
        self.DesNode.pos = self.DesNodePos

    def setNodes(self):
        self.updateNodesPosition()

        # Note: the nodes can't be attached to the widgets frame, as we don't 
        # want the nodes to rotate with the frame during an animation. That's
        # why their position needs to be updated by an external animation
        # routine using the "updateNodesPosition" method.

        self.AscNode = sphere(pos=self.AscNodePos, np=32, radius=100, make_trail=false, color=color.green) 
        self.DesNode = sphere(pos=self.DesNodePos, np=32, radius=100, make_trail=false, color=color.red) 

        if False:
            self.NodeAxis = curve(frame=self.Origin, color=self.Color, visible=False, radius=25, material=materials.emissive)
            newpos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])

            # add angular portion of longitude curve
            self.Trail.append(pos=newpos, color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))


class makeEquatorialPlane():
    def __init__(self, widgets, color, opacity): #planet, color, opacity):
        
        self.Planet = widgets.Planet
        self.Opacity = opacity
        self.Color = color 

        side = 0.5*AU*DIST_FACTOR
        self.eqPlane = box(pos=self.Planet.Position, length=side, width=0.0001, height=side, material=materials.emissive, visible=False, color=self.Color, opacity=0.1) #, axis=(0, 0, 1), opacity=0.8) #opacity=self.Opacity)
        self.eqPlane.rotate(angle=(self.Planet.TiltAngle), axis=self.Planet.XdirectionUnit) #, origin=(0,0,0))

    def updateEquatorialPlanePosition(self):
        self.eqPlane.pos[X_COOR] = self.Planet.Position[X_COOR]
        self.eqPlane.pos[Y_COOR] = self.Planet.Position[Y_COOR]
        self.eqPlane.pos[Z_COOR] = self.Planet.Position[Z_COOR]
         
    def display(self, trueFalse):
        self.eqPlane.visible = trueFalse


class doLongitude():
    def __init__(self, widgets, colr, longitudeAngle):
        self.longAngle = longitudeAngle
        self.Origin = widgets.Origin

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
            self.updatePosition(E)

    def setCartesianCoordinates(self, angleIncr):
        radius = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]
        projectionOnXYplane = radius * cos(angleIncr)
        self.Position[X_COOR] = projectionOnXYplane * cos(self.longAngle)
        self.Position[Y_COOR] = projectionOnXYplane * sin(self.longAngle)
        self.Position[Z_COOR] = radius * sin(angleIncr)

    def updatePosition(self, E, trace = True):
        self.setCartesianCoordinates(E)
        newpos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])

        # add angular portion of longitude curve
        self.Trail.append(pos=newpos, color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))

class makeLongitudes():
        
    def __init__(self, widgets):
        self.Origin = widgets.Origin
        self.Widgets = widgets
        self.Origin.visible = True
        self.Lons = []
        self.Color = color.cyan
        self.draw()

    def display(self, trueFalse):
        for tz in self.Lons:
            tz.display(trueFalse)

    def draw(self):
        colr = color.red
        for i in np.arange(0, pi, deg2rad(10)):
            # build TZ by longitude circles
            self.Lons.append(doLongitude(self.Widgets, colr, i))
            colr = self.Color

class doLatitude():
    def __init__(self, widgets, latitudeAngle, colr, thickness=0):
        self.latAngle = latitudeAngle
        self.Origin = widgets.Origin
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
            self.updatePosition(E)


    def setCartesianCoordinates(self, angleIncr):
        radius = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]
        projection = radius * cos(self.latAngle)

        self.Position[X_COOR] = projection * sin(angleIncr)
        self.Position[Y_COOR] = projection * cos(angleIncr)
        self.Position[Z_COOR] = radius * sin(self.latAngle)


    def updatePosition(self, E):
        self.setCartesianCoordinates(E)
        newpos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])

        # add angular portion of latitude curve
        self.Trail.append(pos=newpos, color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))


class makeLatitudes():
        
    def __init__(self, widgets):
        self.Origin = widgets.Origin
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
        self.Origin = widgets.Origin
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
