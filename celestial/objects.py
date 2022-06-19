from visual import *

class arrow:

    def __init__(self, clor, length, axis = vector(1,0,0)):
        self.Origin = frame()
        self.Length = length
        self.Color = clor

        self.Trail = curve(frame=self.Origin, pos=(vector(0,0,0), axisEnd*size), color=self.Color, visible=True, radius=5, material=materials.emissive)
        self.Position = np.matrix([[0],[0],[0]], np.float64)
        #        self.draw()


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

a = arrow(color.red, 10)
raw_input("press any key")
