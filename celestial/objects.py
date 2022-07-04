from orbit3D import *
from visual import *

class simpleArrow:

    def __init__(self, color, radius, dtype, start, axisp, context = None):
        #self.Origin = frame() if context == None else context
        self.Radius = radius if radius > 0 else dtype
        self.Color = color
        self.pos = [start, start+axisp]
        self.Trail  = curve(frame=context, pos= [ start, start + axisp], material=materials.emissive, color=self.Color, radius=radius,   visible=False)
        self.Tip    = cone(frame=context,  pos= (start + axisp),         material=materials.emissive, color=self.Color, radius=self.Radius*4, visible=False, length=15*self.Radius, axis=axisp)
#        self.Trail  = curve(frame=None, pos= [ start, start + axisp], material=materials.emissive, color=self.Color, radius=radius,   visible=False)
#        self.Tip    = cone(frame=None,  pos= (start + axisp),         material=materials.emissive, color=self.Color, radius=self.Radius*4, visible=False, length=15*self.Radius, axis=axisp)

    def display(self, trueFalse):
        self.Trail.visible = trueFalse
        self.Tip.visible = trueFalse

    def setPosition(self, start, end):
        self.Trail.pos = [start, end]
        self.Tip.pos = end

class circle:
    def  __init__(self, color, radius, pos, normalAxis, context = None):
        self.Origin = frame() if context == None else context
        self.Radius = radius if radius > 0 else 30
        self.Color = color
        self.pos = vector(pos)
        #self.Position = vector(pos)

        #self.Ring = ring(pos=pos, axis=normalAxis, radius=radius, thickness=1, visible=False, material=materials.emissive)
        #self.Trail  = curve(frame=context, pos= [ start, start + axisp], material=materials.emissive, color=self.Color, radius=radius,   visible=False)
        self.Trail = curve(frame=context, pos=self.pos, color=self.Color, visible=False, radius=radius, material=materials.emissive)

        increment = pi/32
        for E in np.arange(0, 2*pi+increment, increment):
            # build Equator line using angular segments of increments degres
            # radius = self.Planet.radiusToShow/self.Planet.SizeCorrection[self.Planet.sizeType]

            X = self.Radius * cos(E) 
            Y = self.Radius * sin(E)
            Z = 0
            # add angular portion of equator
#            self.Trail.append(pos= vector(self.Position[X_COOR],self.Position[Y_COOR],self.Position[Z_COOR]), color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))
            self.Trail.append(pos= vector(X,Y,Z), color=(self.Color[0]*0.6, self.Color[1]*0.6, self.Color[2]*0.6))

    def display(self, trueFalse):
        self.Trail.visible = trueFalse

    def rotate(self, angle, axis):
        self.Origin.rotate(angle=angle, axis=axis)

    def setPosition(self, start, end):
        self.Trail.pos = [start, end]


class arrow:

    def __init__(self, color, length, radius, materialType, label, textborder=False, axisp = vector(1,0,0)):
        self.Origin = frame()
        self.Length = length
        self.Radius = radius
        self.Color = color
        self.Label = label

        #axisp = axisp * length
#        self.Trail = cylinder(frame=self.Origin, pos=[(0,0,0), axisp], color=self.Color, visible=True, radius=5, material=materials.emissive)
        self.Trail = cylinder(frame=self.Origin, pos=vector(0,0,0), material=materialType, radius=radius, color=self.Color, length=length, opacity=1.0, axis=axisp)
        self.Tip = cone(frame=self.Origin, pos=length*axisp, material=materialType, length=6*self.Radius, axis=axisp, radius=radius*2, color=self.Color)
        self.Text = text(frame=self.Origin, pos=self.Tip.pos+axisp*floor(length/10+5), axis=(1,0,0), text=self.Label, xoffset=0, yoffset=0, space=0, height=5, border=6, box=textborder) #height=self.Radius*10, box=True)
        print "arrow point pos=", self.Tip.pos

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

def main2():
    a = arrow(color.red, 40, 1, materials.emissive, "FP Aries", True)
    b = arrow(color.yellow, 40, 1, materials.emissive,"y", axisp = vector(0,1,0))
    d = arrow(color.green, 40, 1, materials.emissive,"z", axisp = vector(0,0,1))

