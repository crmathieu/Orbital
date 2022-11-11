
from vpython_interface import Color
from objects import simpleArrow
import numpy as np
from visual import *

class makeBasicReferential:

    def  __init__(self, params):
        # axisLock is used when the referential needs to have its axis linked to the frame
        self.referential        = frame()
        self.body               = None
        self.tiltAngle          = params['tiltangle']
        self.referential.pos    = (0,0,0)
#        self.defaultZAxis    = params['default_zaxis']

        #self.frame              = self.referential #if axisLock == True else None
        #cosv = cos(tiltAngle)
        #sinv = sin(tiltAngle)
        
        #self.Rotation_Obliquity = np.matrix([
        #    [1,			0,		0	],
        #    [0,			cosv,   sinv],
        #    [0,			-sinv, 	cosv]]
        #)

        #cosv = cos(self.tiltAngle)
        #sinv = sin(self.tiltAngle)
        #self.defaultZaxis = vector(0, sin(self.tiltAngle), cos(self.tiltAngle))

        if False:
            # this rotation happens around the x-axis
            self.Rotation_Obliquity = np.matrix([
                [1,			0,		0	],
                [0,			cosv,   sinv],
                [0,			-sinv, 	cosv]]
            )

    #		directions = [vector(1, 0, 0), vector(0, 1, 0), vector(0, 0, 1)]
    #		for i in range (3)
    #			A = np.matrix([[directions[i][0]],[directions[i][1]],directions[i][2]]], np.float64)
    #			directions[i] = self.Rotation_Obliquity * A

    #		return directions[2]
            A = np.matrix([[0],[0],[1]], np.float64)
            self.defaultZaxis = self.Rotation_Obliquity * A
            self.defaultZaxis = self.defaultZaxis/mag(self.defaultZaxis)
            print "default Z-AXIS = ", self.defaultZaxis
            print "MANUALLY: = ",[0, sinv, cosv]

        if params['body'] is not None:
            self.body               = params['body']
#            radius                  = self.body.radiusToShow/self.body.SizeCorrection[self.body.sizeType]
            self.referential.pos    = self.body.Position
            #if body.Name.lower() not in objects_data.keys():
            #    return


        # based on whether or not we want our 3 axis locked with frame, set position absolutely or relatively
#        position = self.referential.pos# if self.frame == None else vector(0,0,0)

#        self.referential.rotate(angle=(initialRotation), axis=(1,0,0))

#        size = radius * 2
#        self.directions = [vector(size*params['ratio'][0], 0, 0), vector(0, size*params['ratio'][1], 0), vector(0, 0, size*params['ratio'][2])]
#        ve = 0.2
#        if size < radius:
#            ve = 0.4

#        if tilt:
#            #self.referential.rotate(angle=(-body.TiltAngle), axis=(1,0,0))
#            self.referential.rotate(angle=(-body.TiltAngle), axis=(1,0,0))
#        if self.makeAxis ==  True:
#            position = vector(0,0,0)
#            for i in range (3): # Each direction
                #A = np.matrix([[self.directions[i][0]],[self.directions[i][1]],[self.directions[i][2]]], np.float64)
                #self.directions[i] = self.Rotation_Obliquity * A

#                self.Axis[i] = simpleArrow(params['color'], 0, 20, position, axisp = self.directions[i], context=self.referential)
#                self.Axis[i].display(False) # allows axis visibility to be dependent upon their frame visibility when axisLock = True
#                self.AxisLabel[i] = label( frame = self.referential, color = params['color'],  text = params['legend'][i],
                                            #pos = self.referential.pos+self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=show )
#                                            pos = position+self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=False )
#                ve = 0.07 #####

            #ZdirectionVec = self.Axis[2].pos[1]-self.Axis[2].pos[0]
            #YdirectionVec = self.Axis[1].pos[1]-self.Axis[1].pos[0]
            #XdirectionVec = self.Axis[0].pos[1]-self.Axis[0].pos[0]

            #self.ZdirectionUnit = ZdirectionVec/mag(ZdirectionVec)
            #self.YdirectionUnit = YdirectionVec/mag(YdirectionVec)
            #self.XdirectionUnit = XdirectionVec/mag(XdirectionVec)

            #self.RotAxis = self.ZdirectionUnit

        self.display(params['show'])

    def display(self, trueFalse):
        self.referential.visible = trueFalse

    def setAxisTilt(self):
        self.referential.rotate(angle=(self.tiltAngle), axis=(1,0,0))
        self.ZdirectionUnit = self.RotAxis = self.body.getRotAxis() #vector(0, sin(self.tiltAngle), cos(self.tiltAngle))

    def updateReferential(self):
        self.referential.pos = self.body.Position

    def rotate(self, angle):
        self.referential.rotate(angle=(angle), axis=self.RotAxis) #ZdirectionUnit) #rotAxis)


class make3DaxisReferential:

    def  __init__(self, params):
        # axisLock is used when the referential needs to have its axis linked to the frame
        self.referential        = frame()
        self.Axis 		        = [None,None,None]
        self.AxisLabel 	        = ["","",""]
        radius                  = params['radius']
        self.body               = None
        self.tiltAngle          = params['tiltangle']
        self.referential.pos    = (0,0,0)
        self.rotMatrix          = None

        if 'initial_rotation' in params:
            cosv = cos(params['initial_rotation'])
            sinv = sin(params['initial_rotation'])

            self.rotMatrix = np.matrix([
            [cosv,		-sinv,	0],
            [sinv,		cosv,   0],
            [0,			0, 	    1]])

#        self.makeAxis           = params['make_axis']
#        self.defaultZAxis       = None
#        if 'default_zaxis' in params:
            # this is normally provided when no referential axis are generated so that 
            # a default rotation axis is defined for each dimension  
#            self.defaultZAxis    = params['default_zaxis']

        #self.frame              = self.referential #if axisLock == True else None
        #cosv = cos(tiltAngle)
        #sinv = sin(tiltAngle)
        
        #self.Rotation_Obliquity = np.matrix([
        #    [1,			0,		0	],
        #    [0,			cosv,   sinv],
        #    [0,			-sinv, 	cosv]]
        #)

        if params['body'] is not None:
            self.body               = params['body']
#            radius                  = self.body.radiusToShow/self.body.SizeCorrection[self.body.sizeType]
            radius                  = self.body.getBodyRadius()
            self.referential.pos    = (self.body.Position[0]+self.body.Foci[0], self.body.Position[1]+self.body.Foci[1], self.body.Position[2]+self.body.Foci[2])
            #if body.Name.lower() not in objects_data.keys():
            #    return


        # based on whether or not we want our 3 axis locked with frame, set position absolutely or relatively
#        position = self.referential.pos# if self.frame == None else vector(0,0,0)

#        self.referential.rotate(angle=(initialRotation), axis=(1,0,0))

        size = radius * 2
        self.directions = [vector(size*params['ratio'][0], 0, 0), vector(0, size*params['ratio'][1], 0), vector(0, 0, size*params['ratio'][2])]
        ve = 0.2
#        if size < radius:
#            ve = 0.4

#        if tilt:
#            #self.referential.rotate(angle=(-body.TiltAngle), axis=(1,0,0))
#            self.referential.rotate(angle=(-body.TiltAngle), axis=(1,0,0))
#        if self.makeAxis ==  True:
            #position = vector(0,0,0) 
        for i in range (3): # Each direction
            if self.rotMatrix is not None:
                A = np.matrix([[self.directions[i][0]],[self.directions[i][1]],[self.directions[i][2]]], np.float64)
                self.directions[i] = self.rotMatrix * A


            self.Axis[i] = simpleArrow(params['color'], 0, 20, vector(0,0,0), axisp = self.directions[i], context=self.referential)
            self.Axis[i].display(True) # allows axis visibility to be dependent upon their frame visibility when axisLock = True
            self.AxisLabel[i] = label( frame = self.referential, color = params['color'],  text = params['legend'][i],
                                        #pos = self.referential.pos+self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=show )
                                        pos = self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=True )

#                self.Axis[i] = simpleArrow(params['color'], 0, 20, position, axisp = self.directions[i], context=self.referential)
#                self.Axis[i].display(False) # allows axis visibility to be dependent upon their frame visibility when axisLock = True
#                self.AxisLabel[i] = label( frame = self.referential, color = params['color'],  text = params['legend'][i],
#                                            #pos = self.referential.pos+self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=show )
#                                            pos = position+self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=False )


            ve = 0.07 #####

        self.display(params['show'])

    def display(self, trueFalse):
        #self.referential.visible = trueFalse
        for i in range(3):
            self.Axis[i].display(trueFalse)
            self.AxisLabel[i].visible = trueFalse

    def getAbsoluteAxisVector(self, n):
        if n < 0 or n > 2:
            return None
        return self.referential.frame_to_world(self.Axis[n].pos[1])-self.referential.frame_to_world(self.Axis[n].pos[0])

    def setAxisTilt(self):
        # rotate referential first
        self.referential.rotate(angle=(self.tiltAngle), axis=(1,0,0))

        # determine unit vector for each direction
        ZdirectionVec = self.referential.frame_to_world(self.Axis[2].pos[1])-self.referential.frame_to_world(self.Axis[2].pos[0])
        YdirectionVec = self.referential.frame_to_world(self.Axis[1].pos[1])-self.referential.frame_to_world(self.Axis[1].pos[0])
        XdirectionVec = self.referential.frame_to_world(self.Axis[0].pos[1])-self.referential.frame_to_world(self.Axis[0].pos[0])

        self.ZdirectionUnit = ZdirectionVec/mag(ZdirectionVec)
        self.YdirectionUnit = YdirectionVec/mag(YdirectionVec)
        self.XdirectionUnit = XdirectionVec/mag(XdirectionVec)

        self.RotAxis = self.ZdirectionUnit

    def updateReferential(self):
        self.referential.pos = (self.body.Position[0]+self.body.Foci[0], self.body.Position[1]+self.body.Foci[1], self.body.Position[2]+self.body.Foci[2])
        return 


        # based on whether or not our 3 axis is locked with frame, set position absolutely or relatively
        #position = self.referential.pos #if self.frame == None else vector(0,0,0)
        position = vector(0,0,0)
        
#        self.updateAxis()
#        if self.makeAxis == True:
        ve = 0.2
        for i in range (3): # Each direction
            self.Axis[i].setPosition((0,0,0), self.directions[i])
            self.AxisLabel[i].pos = self.directions[i]*(1.07+ve)
            ve = 0.07 
#        for i in range (3): # Each direction
#            self.Axis[i].setPosition(position, position+self.directions[i])
#            self.AxisLabel[i].pos = position+self.directions[i]*(1.07+ve)
#            ve = 0.07 

    def rotate(self, angle):
        self.referential.rotate(angle=(angle), axis=self.RotAxis)
        #self.updateReferential()


