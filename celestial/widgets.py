from orbit3D import *
from visual import *

class makeEarthWidgets():

    def __init__(self, planet):
        self.Origin = frame()
        self.Origin.pos = planet.Origin.pos
        print ("in MakeWidgets----------> "+str(self.Origin.pos))
        self.Planet = planet
        self.visible = True
        if False:
            self.Planet = planet
            self.Color = color.red
    #        self.Trail = curve(frame=planet.Origin, color=self.Color, visible=False, radius=25)
    #        self.Equator = curve(frame=self.Origin, color=self.Color, visible=False, radius=100)
            self.visible = False
            self.Position = np.matrix([[0],[0],[0]], np.float64)
            self.AscNodePos = np.matrix([[0],[0],[0]], np.float64)
            self.DesNodePos = np.matrix([[0],[0],[0]], np.float64)

    #        self.Equator = makeEquator(self) # will tilt the frame by the same amount the planet is titlted
    #        self.EqPlane = makeEquatorialPlane(self, color.orange, opacity=0.5)
    #        self.Longs = makeTimezones(self)
    #        self.Lats = makeLatitudes(self)

    def animateWidgets(self):
        self.Origin.pos[X_COOR] = self.Planet.Position[X_COOR]
        self.Origin.pos[Y_COOR] = self.Planet.Position[Y_COOR]
        self.Origin.pos[Z_COOR] = self.Planet.Position[Z_COOR]


class makeEquator():

    def __init__(self, widgets): #planet):
        #self.Origin = planet.Origin
        self.Origin = widgets.Origin
        #self.Origin.pos = widgets.Planet.Origin.pos
        print ("in makeEquator ----------> "+str(self.Origin.pos))
        self.Planet = widgets.Planet
        self.Color = color.red
#        self.Trail = curve(frame=planet.Origin, color=self.Color, visible=False, radius=25)
        self.Trail = curve(frame=self.Origin, color=self.Color, visible=False, radius=25)
        ##########self.visible = False
        self.Position = np.matrix([[0],[0],[0]], np.float64)
        self.AscNodePos = np.matrix([[0],[0],[0]], np.float64)
        self.DesNodePos = np.matrix([[0],[0],[0]], np.float64)

#        self.Origin.pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])
        self.draw()
        self.setNodes()
        self.showNodes(False)

    def display(self, trueFalse):
        self.Trail.visible = trueFalse

    def draw(self):
        increment = pi/180
        for E in np.arange(0, 2*pi+increment, increment):
            # from R and Nu, calculate 3D coordinates and update current position
            self.updatePosition(E)

        # position equator based of planet tilt
#        self.Origin.rotate(angle=(self.Planet.TiltAngle), axis=self.Planet.XdirectionUnit, origin=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]))
        #####self.Origin.rotate(angle=(self.Planet.TiltAngle), axis=self.Planet.XdirectionUnit, origin=self.Origin.pos)

    def setCartesianCoordinates(self, angleIncr):
        radius = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]

        self.Position[X_COOR] = radius * cos(angleIncr) 
        self.Position[Y_COOR] = radius * sin(angleIncr)
        self.Position[Z_COOR] = 0

        # finally, calculate these coordinates in our arbitrary definition of the Constellation of Pisces (Vernal Equinox) referential.
#        self.Position = self.Planet.Rotation_VernalEquinox * self.Position
    

    def updatePositionXX(self, E, trace = True):
        self.setCartesianCoordinates(E)
        #self.Origin.pos = vector(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR])
        self.Origin.pos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])

        # add angular portion of equator
        self.Trail.append(pos=self.Origin.pos, color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))

    def updatePosition(self, E, trace = True):
        self.setCartesianCoordinates(E)
        #self.Origin.pos = vector(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR])
        #self.Origin.pos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])

        # add angular portion of equator
        self.Trail.append(pos= vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]), color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))

    def showNodes(self, trueFalse):
        self.AscNode.visible = trueFalse
        self.DesNode.visible = trueFalse

    def makeShape(self):
        self.Origin.pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])
        #self.BodyShape = sphere(frame=self.Origin, pos=(0,0,0), np=32, radius=self.radiusToShow/self.SizeCorrection[self.sizeType], make_trail=false)

    def updateNodesPosition(self):
        self.AscNodePos[X_COOR] = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType] + self.Planet.Position[X_COOR]
        self.AscNodePos[Y_COOR] = self.Planet.Position[Y_COOR]
        self.AscNodePos[Z_COOR] = self.Planet.Position[Z_COOR]
        self.DesNodePos[X_COOR] = -self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType] + self.Planet.Position[X_COOR]
        self.DesNodePos[Y_COOR] = self.Planet.Position[Y_COOR]
        self.DesNodePos[Z_COOR] = self.Planet.Position[Z_COOR]

    def updateWidgetsPosition(self):
        self.updateNodesPosition()
        self.refreshNodes()

    def refreshNodes(self):
        self.AscNode.pos = self.AscNodePos
        self.DesNode.pos = self.DesNodePos

    def setNodes(self):
        self.updateNodesPosition()
#        self.AscNode = sphere(frame=self.Planet.Origin, pos=self.AscNodePos, np=32, radius=100, make_trail=false, color=color.green) 
#        self.DesNode = sphere(frame=self.Planet.Origin, pos=self.DesNodePos, np=32, radius=100, make_trail=false, color=color.red) 
        self.AscNode = sphere(pos=self.AscNodePos, np=32, radius=100, make_trail=false, color=color.green) 
        self.DesNode = sphere(pos=self.DesNodePos, np=32, radius=100, make_trail=false, color=color.red) 
#        self.AscNode = sphere(frame=self.Origin, pos=self.AscNodePos, np=32, radius=100, make_trail=false, color=color.green) 
#        self.DesNode = sphere(frame=self.Origin, pos=self.DesNodePos, np=32, radius=100, make_trail=false, color=color.red) 


class makeEquatorialPlane():
    def __init__(self, widgets, color, opacity): #planet, color, opacity):
        
#        self.Origin = planet.Origin
#        self.Planet = planet
        self.Origin = widgets.Origin
        print ("in makeEquatorialPlane ----------> "+str(self.Origin.pos))

        self.Planet = widgets.Planet
        self.Opacity = opacity
        self.Color = color 
       
#        self.Trail = curve(frame=planet.Origin, color=color.cyan, visible=False)
        ###########self.visible = True
        #self.Position = np.matrix([[0],[0],[0]], np.float64)
        #        self.Origin.pos=(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])
        #self.Color = color.cyan

        side = 0.5*AU*DIST_FACTOR
        #####self.eqPlane = cylinder(frame=self.Origin, pos=vector(0,0,0), radius=side/2, color=self.Color, length=0.1, opacity=self.Opacity, axis=(0,0,1), material=materials.emissive, visible=False)
        #self.eqPlane.rotate(angle=self.Planet.TiltAngle, axis=self.Planet.XdirectionUnit, origin=self.Planet.Origin.pos)
        self.eqPlane = box(frame=self.Origin, pos=vector(0, 0, 0), length=side, width=0.0001, height=side, material=materials.emissive, color=self.Color, opacity=0.1) #, axis=(0, 0, 1), opacity=0.8) #opacity=self.Opacity)

    def display(self, trueFalse):
        self.eqPlane.visible = trueFalse


class makeLongitude():
    def __init__(self, widgets, longitudeAngle): #planet, longitudeAngle):
        self.longAngle = longitudeAngle
#        self.Origin = frame() #planet.Origin
#        self.Origin.pos = planet.Origin.pos
        self.Origin = widgets.Origin
#        self.Origin.pos = planet.Origin.pos
        print ("in makelongitude ----------> "+str(self.Origin.pos))

        self.Planet = widgets.Planet
#        self.Trail = curve(frame=planet.Origin, color=color.cyan, visible=False)
        self.Trail = curve(frame=self.Origin, color=color.cyan, visible=False)
        #self.visible = True
        self.Position = np.matrix([[0],[0],[0]], np.float64)
        self.Color = color.cyan
        self.draw()

    def display(self, trueFalse):
        self.Trail.visible = trueFalse

    def draw(self):
        increment = pi/180
        for E in np.arange(0, 2*pi+increment, increment):
            # from R and Nu, calculate 3D coordinates and update current position
            self.updatePosition(E)


    def setCartesianCoordinatesLatitudesXX(self, angleIncr):
        radius = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]

        self.Position[X_COOR] = radius * cos(self.longAngle) * sin(angleIncr)
        self.Position[Y_COOR] = radius * cos(self.longAngle) * cos(angleIncr)
        self.Position[Z_COOR] = radius * sin(angleIncr)

    def setCartesianCoordinates(self, angleIncr):
        radius = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]
        projection = radius * cos(angleIncr)
        self.Position[X_COOR] = projection * cos(self.longAngle)
        self.Position[Y_COOR] = projection * sin(self.longAngle)
        self.Position[Z_COOR] = radius * sin(angleIncr)

    def updatePosition(self, E, trace = True):
        self.setCartesianCoordinates(E)
        #self.Origin.pos = vector(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR])
#        self.Origin.pos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])
        newpos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])

        # add angular portion of longitude curve
        self.Trail.append(pos=newpos, color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))

class makeTimezones():
        
    def __init__(self, widgets): #planet):
#        self.Origin = planet.Origin
        self.Origin = widgets.Origin
        print ("in maketimezones ----------> "+str(self.Origin.pos))

        self.Planet = widgets.Planet
        self.Widgets = widgets
        self.Origin.visible = True
        self.tz = []
        self.Color = color.cyan
        self.draw()

    def display(self, trueFalse):
        for tz in self.tz:
            tz.display(trueFalse)

    def displayXX(self, trueFalse):
        self.Origin.visible = trueFalse

    def draw(self):
        k = j = 0		
        for i in np.arange(0, pi, deg2rad(15)):
            self.tz.append(makeLongitude(self.Widgets, i))
#            self.tz.append(makeLongitude(self.Planet, i))


class doLatitude():
    def __init__(self, widgets, latitudeAngle): #planet, latitudeAngle):
        self.latAngle = latitudeAngle
#        self.Origin = frame() #planet.Origin
#        self.Origin.pos = planet.Origin.pos

        self.Origin = widgets.Origin
        print ("in doLatitude ----------> "+str(self.Origin.pos))

        self.Planet = widgets.Planet
#        self.Trail = curve(frame=planet.Origin, color=color.cyan, visible=False)
        self.Trail = curve(frame=self.Origin, color=color.cyan, visible=False)
        self.Position = np.matrix([[0],[0],[0]], np.float64)
        self.Color = color.cyan
        self.draw()

    def display(self, trueFalse):
        self.Trail.visible = trueFalse

    def draw(self):
        increment = pi/180
        for E in np.arange(0, 2*pi+increment, increment):
            # from R and Nu, calculate 3D coordinates and update current position
            self.updatePosition(E)


    def setCartesianCoordinates(self, angleIncr):
        radius = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]
        projection = radius * cos(self.latAngle)

        self.Position[X_COOR] = projection * sin(angleIncr)
        self.Position[Y_COOR] = projection * cos(angleIncr)
        self.Position[Z_COOR] = radius * sin(self.latAngle)

    def setCartesianCoordinatesXX(self, angleIncr):
        radius = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]
        projection = radius * cos(angleIncr)
        self.Position[X_COOR] = projection * cos(self.longAngle)
        self.Position[Y_COOR] = projection * sin(self.longAngle)
        self.Position[Z_COOR] = radius * sin(angleIncr)

    def updatePosition(self, E, trace = True):
        self.setCartesianCoordinates(E)
        #self.Origin.pos = vector(self.Position[X_COOR]+self.Foci[X_COOR],self.Position[Y_COOR]+self.Foci[Y_COOR],self.Position[Z_COOR]+self.Foci[Z_COOR])
#        self.Origin.pos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])
        newpos = vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR])

        # add angular portion of longitude curve
        self.Trail.append(pos=newpos, color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))


class makeLatitudes():
        
    def __init__(self, widgets): # planet):
#        self.Origin = planet.Origin
        self.Origin = widgets.Origin
        print ("in makeLatitudes ----------> "+str(self.Origin.pos))
        self.Planet = widgets.Planet
        self.Widgets = widgets
        #self.Origin.visible = True
        self.lats = []
        self.Color = color.cyan
        self.draw()

    def display(self, trueFalse):
        for lat in self.lats:
            lat.display(trueFalse)

    def draw(self):
        for i in np.arange(-pi/2, pi/2, deg2rad(10)):
#            self.lats.append(doLatitude(self.Planet, i))
            self.lats.append(doLatitude(self.Widgets, i))
