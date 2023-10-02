
from vpython_interface import Color
from objects import simpleArrow
import numpy as np
from visual import *

class makeBasicReferential:

    def  __init__(self, params):
        self.referential        = frame()
        self.body               = None
        self.tiltAngle          = params['tiltangle']
        self.referential.pos    = (0,0,0)

        if params['body'] is not None:
            self.body               = params['body']
            self.referential.pos    = self.body.Position

        self.display(params['show'])

    def display(self, trueFalse):
        self.referential.visible = trueFalse

    def setAxisTilt(self, rightAscension):

        self.referential.rotate(angle=(self.tiltAngle), axis=(1,0,0))
        if rightAscension != 0:
            print "Basic: Adjusting axis direction by ", rightAscension%360, " degrees"
            self.referential.rotate(angle=deg2rad(rightAscension), axis=(0,0,1), origin=(self.body.Position[0]+self.body.Foci[0],self.body.Position[1]+self.body.Foci[1],self.body.Position[2]+self.body.Foci[2]))

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


        if params['body'] is not None:
            self.body               = params['body']
            radius                  = self.body.getBodyRadius()
            self.referential.pos    = (self.body.Position[0]+self.body.Foci[0], self.body.Position[1]+self.body.Foci[1], self.body.Position[2]+self.body.Foci[2])

        size = radius * 2
        self.directions = [vector(size*params['ratio'][0], 0, 0), vector(0, size*params['ratio'][1], 0), vector(0, 0, size*params['ratio'][2])]

        for i in range (3): # Each direction
            if self.rotMatrix is not None:
                A = np.matrix([[self.directions[i][0]],[self.directions[i][1]],[self.directions[i][2]]], np.float64)
                self.directions[i] = self.rotMatrix * A


            self.Axis[i] = simpleArrow(params['color'], 0, 20, vector(0,0,0), axisp = self.directions[i], context=self.referential)
            self.Axis[i].display(True) # allows axis visibility to be dependent upon their frame visibility when axisLock = True
            self.AxisLabel[i] = label( frame = self.referential, color = params['color'],  text = params['legend'][i],
                                        pos = self.directions[i]*(1.07), opacity = 0, box = False, visible=True )

        self.display(params['show'])

    def display(self, trueFalse):
        for i in range(3):
            self.Axis[i].display(trueFalse)
            self.AxisLabel[i].visible = trueFalse

    def getAbsoluteAxisVector(self, n):
        if n < 0 or n > 2:
            return None
        return self.referential.frame_to_world(self.Axis[n].pos[1])-self.referential.frame_to_world(self.Axis[n].pos[0])

    def setAxisTilt(self, rightAscension):

        # rotate referential first
        self.referential.rotate(angle=(self.tiltAngle), axis=(1,0,0))
        if rightAscension != 0:
            #print "3Dref: Adjusting axis direction by ", rightAscension%360, " degrees"
            self.referential.rotate(angle=deg2rad(rightAscension % 360), axis=(0,0,1), origin=(self.body.Position[0]+self.body.Foci[0],self.body.Position[1]+self.body.Foci[1],self.body.Position[2]+self.body.Foci[2]))


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

    def rotate(self, angle):
        self.referential.rotate(angle=(angle), axis=self.RotAxis)
        #self.updateReferential()


