from orbit3D import *
from visual import *

class makePlanetWidgets():

    def __init__(self, planet):
        self.Origin = frame()
        self.Origin.pos = planet.Origin.pos
        self.Planet = planet
        self.visible = True
        self.Eq = self.eqPlane = self.Lons = self.Lats = None

        self.initWidgets()


    def initWidgets(self):

        self.Eq = makeEquator(self)
        self.EqPlane = makeEquatorialPlane(self, color.orange, opacity=self.Planet.Opacity)
        self.Lons = makeLongitudes(self)
        self.Lats = makeLatitudes(self)

        # align with planet tilt
        self.Origin.rotate(angle=(self.Planet.TiltAngle), axis=self.Planet.XdirectionUnit) #, origin=(0,0,0))

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
        self.Eq.refreshNodes()	
        self.EqPlane.updateEquatorialPlanePosition()	

    def showEquatorialPlane(self, value):
        self.EqPlane.display(value)

    def showEquator(self, value):
        self.Eq.display(value)

    def showLatitudes(self, value):
        self.Lats.display(value)

    def showLongitudes(self, value):
        self.Lons.display(value)

    def showNodes(self, value):
        self.Eq.showNodes(value)

class makeEquator():

    def __init__(self, widgets): #planet):
        self.Origin = widgets.Origin
        self.Planet = widgets.Planet
        self.Color = color.red

        self.Trail = curve(frame=self.Origin, color=self.Color, visible=False, radius=25)
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


class makeLongitude():
    def __init__(self, widgets, longitudeAngle):
        self.longAngle = longitudeAngle
        self.Origin = widgets.Origin

        self.Planet = widgets.Planet
        self.Trail = curve(frame=self.Origin, color=color.cyan, visible=False)
        self.Position = np.matrix([[0],[0],[0]], np.float64)
        self.Color = color.cyan
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
        for i in np.arange(0, pi, deg2rad(10)):
            # build TZ by longitude circles
            self.Lons.append(makeLongitude(self.Widgets, i))


class doLatitude():
    def __init__(self, widgets, latitudeAngle):
        self.latAngle = latitudeAngle
        self.Origin = widgets.Origin

        self.Planet = widgets.Planet
        self.Trail = curve(frame=self.Origin, color=color.cyan, visible=False)
        self.Position = np.matrix([[0],[0],[0]], np.float64)
        self.Color = color.cyan
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
            self.lats.append(doLatitude(self.Widgets, i))
