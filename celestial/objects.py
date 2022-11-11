from orbit3D import *
from visual import *

class simpleArrow:

    def __init__(self, color, radius, dtype, start, axisp, context = None):
        #self.Origin = frame() if context == None else context
        self.Radius = radius if radius > 0 else dtype
        self.Color = color
        self.Context = context
        self.pos = [start, start+axisp]
        self.axis = axisp/mag(axisp)
        self.Trail  = curve(frame=context, pos= [ start, start + axisp], material=materials.emissive, color=self.Color, radius=radius,   visible=False)
        self.Tip    = cone(frame=context,  pos= (start + axisp),         material=materials.emissive, color=self.Color, radius=self.Radius*4, visible=False, length=15*self.Radius, axis=axisp)
#        self.Trail  = curve(frame=None, pos= [ start, start + axisp], material=materials.emissive, color=self.Color, radius=radius,   visible=False)
#        self.Tip    = cone(frame=None,  pos= (start + axisp),         material=materials.emissive, color=self.Color, radius=self.Radius*4, visible=False, length=15*self.Radius, axis=axisp)

    def display(self, trueFalse):
        self.Trail.visible = trueFalse
        self.Tip.visible = trueFalse

    def setPosition(self, start, end):
        # Note 
        self.Trail.pos = [start, end]
        self.Tip.pos = end

class circle:
    def  __init__(self, color, radius, pos, normalAxis, context = None):
        self.Origin = frame() if context is None else context
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

"""
class makeReferential:

    def  __init__(self, body, radius, tiltAngle, show = False, color = Color.white, ratio = [1,1,1], legend = ["x", "y", "z"], axisLock = False):
        # axisLock is used when the referential needs to have its axis linked to the frame
        self.referential        = frame()
        self.Axis 		        = [None,None,None]
        self.AxisLabel 	        = ["","",""]
        radius                  = radius
        self.body               = None
        self.tiltAngle          = tiltAngle
        self.referential.pos    = (0,0,0)
        self.frame              = self.referential if axisLock == True else None
        cosv = cos(tiltAngle)
        sinv = sin(tiltAngle)
        
        self.Rotation_Obliquity = np.matrix([
            [1,			0,		0	],
            [0,			cosv,   sinv],
            [0,			-sinv, 	cosv]]
        )

        if body != None:
            self.body               = body
            radius                  = body.radiusToShow/body.SizeCorrection[body.sizeType]
            self.referential.pos    = body.Position
            if body.Name.lower() not in objects_data.keys():
                return

        # based on whether or not we want our 3 axis locked with frame, set position absolutely or relatively
        position = self.referential.pos if self.frame == None else vector(0,0,0)

#        self.referential.rotate(angle=(initialRotation), axis=(1,0,0))

        size = radius * 2
        self.directions = [vector(size*ratio[0], 0, 0), vector(0, size*ratio[1], 0), vector(0, 0, size*ratio[2])]
        ve = 0.2
#        if size < radius:
#            ve = 0.4

#        if tilt:
#            #self.referential.rotate(angle=(-body.TiltAngle), axis=(1,0,0))
#            self.referential.rotate(angle=(-body.TiltAngle), axis=(1,0,0))

        for i in range (3): # Each direction
            A = np.matrix([[self.directions[i][0]],[self.directions[i][1]],[self.directions[i][2]]], np.float64)
            self.directions[i] = self.Rotation_Obliquity * A

            self.Axis[i] = simpleArrow(color, 0, 20, position, axisp = self.directions[i], context=self.frame)
            self.Axis[i].display(False) # allows axis visibility to be dependent upon their frame visibility when axisLock = True
            self.AxisLabel[i] = label( frame = self.frame, color = color,  text = legend[i],
                                        #pos = self.referential.pos+self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=show )
                                        pos = position+self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=False )
            ve = 0.07 #####

        ZdirectionVec = self.Axis[2].pos[1]-self.Axis[2].pos[0]
        YdirectionVec = self.Axis[1].pos[1]-self.Axis[1].pos[0]
        XdirectionVec = self.Axis[0].pos[1]-self.Axis[0].pos[0]

        self.ZdirectionUnit = ZdirectionVec/mag(ZdirectionVec)
        self.YdirectionUnit = YdirectionVec/mag(YdirectionVec)
        self.XdirectionUnit = XdirectionVec/mag(XdirectionVec)

        self.RotAxis = self.ZdirectionUnit

        self.display(show)
"""

class makeReferentialXX:

    def  __init__(self, body, radius, tiltAngle, show = False, color = Color.white, ratio = [1,1,1], legend = ["x", "y", "z"], axisLock = False):
        # axisLock is used when the referential needs to have its axis linked to the frame
        self.referential        = frame()
        self.Axis 		        = [None,None,None]
        self.AxisLabel 	        = ["","",""]
        radius                  = radius
        self.body               = None
        self.tiltAngle          = tiltAngle
        self.referential.pos    = (0,0,0)
        self.frame              = self.referential #if axisLock == True else None
        #cosv = cos(tiltAngle)
        #sinv = sin(tiltAngle)
        
        #self.Rotation_Obliquity = np.matrix([
        #    [1,			0,		0	],
        #    [0,			cosv,   sinv],
        #    [0,			-sinv, 	cosv]]
        #)

        if body is not None:
            self.body               = body
            radius                  = body.radiusToShow/body.SizeCorrection[body.sizeType]
            self.referential.pos    = body.Position
            if body.Name.lower() not in objects_data.keys():
                return

        # based on whether or not we want our 3 axis locked with frame, set position absolutely or relatively
        position = self.referential.pos if self.frame is None else vector(0,0,0)

#        self.referential.rotate(angle=(initialRotation), axis=(1,0,0))

        size = radius * 2
        self.directions = [vector(size*ratio[0], 0, 0), vector(0, size*ratio[1], 0), vector(0, 0, size*ratio[2])]
        ve = 0.2
#        if size < radius:
#            ve = 0.4

#        if tilt:
#            #self.referential.rotate(angle=(-body.TiltAngle), axis=(1,0,0))
#            self.referential.rotate(angle=(-body.TiltAngle), axis=(1,0,0))

        for i in range (3): # Each direction
            #A = np.matrix([[self.directions[i][0]],[self.directions[i][1]],[self.directions[i][2]]], np.float64)
            #self.directions[i] = self.Rotation_Obliquity * A

            self.Axis[i] = simpleArrow(color, 0, 20, position, axisp = self.directions[i], context=self.frame)
            self.Axis[i].display(False) # allows axis visibility to be dependent upon their frame visibility when axisLock = True
            self.AxisLabel[i] = label( frame = self.frame, color = color,  text = legend[i],
                                        #pos = self.referential.pos+self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=show )
                                        pos = position+self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=False )
            ve = 0.07 #####

        #ZdirectionVec = self.Axis[2].pos[1]-self.Axis[2].pos[0]
        #YdirectionVec = self.Axis[1].pos[1]-self.Axis[1].pos[0]
        #XdirectionVec = self.Axis[0].pos[1]-self.Axis[0].pos[0]

        #self.ZdirectionUnit = ZdirectionVec/mag(ZdirectionVec)
        #self.YdirectionUnit = YdirectionVec/mag(YdirectionVec)
        #self.XdirectionUnit = XdirectionVec/mag(XdirectionVec)

        #self.RotAxis = self.ZdirectionUnit

        self.display(show)

    def initTilt(self):
        self.referential.rotate(angle=(self.tiltAngle), axis=(1,0,0))
        self.initAxisTilt()

    def initAxisTilt(self):
        
        ZdirectionVec = self.referential.frame_to_world(self.Axis[2].pos[1])-self.referential.frame_to_world(self.Axis[2].pos[0])
        YdirectionVec = self.referential.frame_to_world(self.Axis[1].pos[1])-self.referential.frame_to_world(self.Axis[1].pos[0])
        XdirectionVec = self.referential.frame_to_world(self.Axis[0].pos[1])-self.referential.frame_to_world(self.Axis[0].pos[0])

        self.ZdirectionUnit = ZdirectionVec/mag(ZdirectionVec)
        self.YdirectionUnit = YdirectionVec/mag(YdirectionVec)
        self.XdirectionUnit = XdirectionVec/mag(XdirectionVec)

        self.RotAxis = self.ZdirectionUnit


    def updateReferential(self):
        self.referential.pos = self.body.Position

        # based on whether or not our 3 axis is locked with frame, set position absolutely or relatively
        position = self.referential.pos if self.frame is None else vector(0,0,0)

#        self.updateAxis()
        ve = 0.2
        for i in range (3): # Each direction
            self.Axis[i].setPosition(position, position+self.directions[i])
            self.AxisLabel[i].pos = position+self.directions[i]*(1.07+ve)
            ve = 0.07 

        #for i in range (3): # Each direction
        #    self.Axis[i].setPosition(self.referential.pos, self.referential.pos+self.directions[i])
        #    self.AxisLabel[i].pos = self.referential.pos+self.directions[i]*1.07

    def rotate(self, angle):
       # rotAxis = self.referential.frame_to_world(self.ZdirectionUnit)
        #if self.body is not None and self.body.Name.lower() == EARTH_NAME:
        #    print self.RotAxis
#####        self.referential.rotate(angle=(angle), axis=rotAxis) #self.RotAxis) #rotAxis)
        self.referential.rotate(angle=(angle), axis=self.RotAxis) #ZdirectionUnit) #rotAxis)
        self.updateReferential()

    def display(self, trueFalse):
        for i in range(3):
            self.Axis[i].display(trueFalse)
            self.AxisLabel[i].visible = trueFalse

    def updateAxis_XX(self):
        for i in range (3): # Each direction
            self.Axis[i].setPosition(self.referential.pos, self.referential.pos+self.directions[i])
            self.AxisLabel[i].pos = self.referential.pos+self.directions[i]*1.07

    def initTilt_XX(self):
        #print "before tilt:", self.referential.frame_to_world(self.ZdirectionUnit)
        self.referential.rotate(angle=(self.refTilt), axis=self.XdirectionUnit) #(1,0,0))
        #print "after tilt:", self.referential.frame_to_world(self.ZdirectionUnit)

    def setAxisLabelXX(self, legend = ["x","y","z"]):
        #pos = vector(self.body.Position)
        pos = (0,0,0)
        for i in range(3):
            self.AxisLabel[i] = label( frame = None, color = Color.white,  text = legend[i],
                                            pos = pos+self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=False )

    def updateReferentialXX(self):
        self.referential.pos = self.body.Position
        self.updateAxis()

    def updateAxisXX(self): #, body):
        return
        #pos = vector(body.Position[0]+body.Foci[0], body.Position[1]+body.Foci[1], body.Position[2]+body.Foci[2])
        pos = vector(0,0,0)
        for i in range (3): # Each direction
            self.Axis[i].setPosition(pos, pos+self.directions[i])
            #self.Axis[i].pos = [ pos, pos+self.directions[i]]
            self.AxisLabel[i].pos = pos+self.directions[i]*1.07


class makeReferentialSAVE:

    def  __init__(self, body, show = False, tilt = True, color = Color.white, legend = ["x", "y", "z"]):
        
        self.referential        = frame()
        self.Axis 		        = [None,None,None]
        self.AxisLabel 	        = ["","",""]
        
        self.body               = body
        self.referential.pos    = body.Position
        radius                  = body.radiusToShow/body.SizeCorrection[body.sizeType]
        self.RotAxis    = vector(0,0,1)
        size = radius * 2

        if body.Name.lower() in objects_data.keys():
            #print "legend=", legend

            self.directions = [vector(size, 0, 0), vector(0, size, 0), vector(0, 0, size)]
            #self.B = [vector(size, 0, 0), vector(0, size, 0), vector(0, 0, size)]

            pos = vector(body.Position)
            ve = 0.2
            if size < radius:
                ve = 0.4

            if tilt:
                #self.referential.rotate(angle=(-body.TiltAngle), axis=(1,0,0))
                self.referential.rotate(angle=(-body.TiltAngle), axis=(1,0,0))

            for i in range (3): # Each direction
                A = np.matrix([[self.directions[i][0]],[self.directions[i][1]],[self.directions[i][2]]], np.float64)
                if tilt:
                    self.directions[i] = body.Rotation_Obliquity * A

                #if tilt:
                #    self.B[i] = body.Rotation_Obliquity * A

#                self.Axis[i] = simpleArrow(Color.white, 0, 20, self.referential.pos, axisp = self.directions[i])
                self.Axis[i] = simpleArrow(color, 0, 20, vector(0,0,0), axisp = self.directions[i], context=self.referential)

                self.AxisLabel[i] = label( frame = self.referential, color = color,  text = legend[i],
                                            #pos = self.referential.pos+self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=False )
                                            pos = self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=show )
                ve = 0.07 #####


            ZdirectionVec = self.Axis[2].pos[1]-self.Axis[2].pos[0]
            YdirectionVec = self.Axis[1].pos[1]-self.Axis[1].pos[0]
            XdirectionVec = self.Axis[0].pos[1]-self.Axis[0].pos[0]

#            ZdirectionVec = self.referential.frame_to_world(self.Axis[2].pos[1])-self.referential.frame_to_world(self.Axis[2].pos[0])
#            YdirectionVec = self.referential.frame_to_world(self.Axis[1].pos[1])-self.referential.frame_to_world(self.Axis[1].pos[0])
#            XdirectionVec = self.referential.frame_to_world(self.Axis[0].pos[1])-self.referential.frame_to_world(self.Axis[0].pos[0])

            self.ZdirectionUnit = ZdirectionVec/mag(ZdirectionVec)
            self.YdirectionUnit = YdirectionVec/mag(YdirectionVec)
            self.XdirectionUnit = XdirectionVec/mag(XdirectionVec)

            self.RotAxis = self.referential.frame_to_world(self.ZdirectionUnit)
#            self.ZdirectionUnit = self.B[2]/mag(self.B[2])
#            self.YdirectionUnit = self.B[1]/mag(self.B[1])
#            self.XdirectionUnit = self.B[0]/mag(self.B[0])

            #print "Z-axis for "+body.Name+" is", self.RotAxis
            self.display(show)

    def setAxisLabel(self, legend = ["x","y","z"]):
        #pos = vector(self.body.Position)
        pos = (0,0,0)
        for i in range(3):
            self.AxisLabel[i] = label( frame = None, color = Color.white,  text = legend[i],
                                            pos = pos+self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=False )

    def updateReferential(self):
        self.referential.pos = self.body.Position
        self.updateAxis()

    def updateAxis(self): #, body):
        return
        #pos = vector(body.Position[0]+body.Foci[0], body.Position[1]+body.Foci[1], body.Position[2]+body.Foci[2])
        pos = vector(0,0,0)
        for i in range (3): # Each direction
            self.Axis[i].setPosition(pos, pos+self.directions[i])
            #self.Axis[i].pos = [ pos, pos+self.directions[i]]
            self.AxisLabel[i].pos = pos+self.directions[i]*1.07

    def display(self, trueFalse):
        for i in range(3):
            self.Axis[i].display(trueFalse)
            self.AxisLabel[i].visible = trueFalse

def main2():
    a = arrow(color.red, 40, 1, materials.emissive, "FP Aries", True)
    b = arrow(color.yellow, 40, 1, materials.emissive,"y", axisp = vector(0,1,0))
    d = arrow(color.green, 40, 1, materials.emissive,"z", axisp = vector(0,0,1))


