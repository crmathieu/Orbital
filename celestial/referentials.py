
from vpython_interface import Color
from objects import simpleArrow
from visual import *

class makeReferential:

    def  __init__(self, params):
        # axisLock is used when the referential needs to have its axis linked to the frame
        self.referential        = frame()
        self.Axis 		        = [None,None,None]
        self.AxisLabel 	        = ["","",""]
        radius                  = params['radius']
        self.body               = None
        self.axisLock           = params['axislock']
        self.tiltAngle          = params['tiltangle']
        self.referential.pos    = (0,0,0)
        self.frame              = self.referential #if axisLock == True else None
        #cosv = cos(tiltAngle)
        #sinv = sin(tiltAngle)
        
        #self.Rotation_Obliquity = np.matrix([
        #    [1,			0,		0	],
        #    [0,			cosv,   sinv],
        #    [0,			-sinv, 	cosv]]
        #)

        if params['body'] != None:
            self.body               = params['body']
            radius                  = self.body.radiusToShow/self.body.SizeCorrection[self.body.sizeType]
            self.referential.pos    = self.body.Position
            #if body.Name.lower() not in objects_data.keys():
            #    return

        # based on whether or not we want our 3 axis locked with frame, set position absolutely or relatively
        position = self.referential.pos if self.frame == None else vector(0,0,0)

#        self.referential.rotate(angle=(initialRotation), axis=(1,0,0))

        size = radius * 2
        self.directions = [vector(size*params['ratio'][0], 0, 0), vector(0, size*params['ratio'][1], 0), vector(0, 0, size*params['ratio'][2])]
        ve = 0.2
#        if size < radius:
#            ve = 0.4

#        if tilt:
#            #self.referential.rotate(angle=(-body.TiltAngle), axis=(1,0,0))
#            self.referential.rotate(angle=(-body.TiltAngle), axis=(1,0,0))

        for i in range (3): # Each direction
            #A = np.matrix([[self.directions[i][0]],[self.directions[i][1]],[self.directions[i][2]]], np.float64)
            #self.directions[i] = self.Rotation_Obliquity * A

            self.Axis[i] = simpleArrow(params['color'], 0, 20, position, axisp = self.directions[i], context=self.frame)
            self.Axis[i].display(False) # allows axis visibility to be dependent upon their frame visibility when axisLock = True
            self.AxisLabel[i] = label( frame = self.frame, color = params['color'],  text = params['legend'][i],
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

        self.display(params['show'])
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
        self.frame              = self.referential #if axisLock == True else None
        #cosv = cos(tiltAngle)
        #sinv = sin(tiltAngle)
        
        #self.Rotation_Obliquity = np.matrix([
        #    [1,			0,		0	],
        #    [0,			cosv,   sinv],
        #    [0,			-sinv, 	cosv]]
        #)

        if body != None:
            self.body               = body
            radius                  = body.radiusToShow/body.SizeCorrection[body.sizeType]
            self.referential.pos    = body.Position
            #if body.Name.lower() not in objects_data.keys():
            #    return

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
    """

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
        position = self.referential.pos if self.frame == None else vector(0,0,0)

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
        #if self.body != None and self.body.Name.lower() == EARTH_NAME:
        #    print self.RotAxis
#####        self.referential.rotate(angle=(angle), axis=rotAxis) #self.RotAxis) #rotAxis)
        self.referential.rotate(angle=(angle), axis=self.RotAxis) #ZdirectionUnit) #rotAxis)
        #self.updateReferential()

    def display(self, trueFalse):
        if self.axisLock == True:
            for i in range(3):
                self.Axis[i].display(trueFalse)
                self.AxisLabel[i].visible = trueFalse

