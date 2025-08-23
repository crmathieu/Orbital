
from vpython_interface import Color
from objects import simpleArrow
import numpy as np
from visual import *


class makeBasicReferential:

    # basic referentials are used to display PCPF referentials
    # which rotate with the planet. There is no visible axis to display, 
    # but we still need to know what the North Pole direction is in 
    # order to rotate the body's texture properly. For Planets and the 
    # Sun, the North Pole vector is calculated from tables provided by 
    # the IAU working group. For other bodies, the North Pole is 
    # arbitrarily the J2000 Ecliptic North Pole.

    def  __init__(self, params):
        # axisLock is used when the referential needs to have its axis linked to the frame
        self.referential        = None
        self.body               = None
        #self.tiltAngle          = params['tiltangle']

        self.NPole              = vector(0,0,1)
        self.W                  = 0
        self.Omega              = 0
        self.RotAxis            = self.NPole

        # create a frame for this referential. This frame should be linked to the J2000
        # ecliptic ref if it is a normal body, or a planet trackingFrame referential if 
        # is orbiting a central body

        if 'parent_frame' in params and params['parent_frame'] != None:
            self.referential = frame(pos=(0,0,0), frame=params['parent_frame'])
        else:
            # that should not happen
            self.referential = frame(pos=(0,0,0))

        if 'name' in params:
            print "creating "+ params['name']

        if 'orientation' in params:
            self.NPole = params['orientation']['pole_vec']
            self.W     = params['orientation']['w_angle']
            self.Omega = params['orientation']['omega_angle']

        if params['body'] is not None:
            self.body               = params['body']
            self.referential.pos    = self.body.Position
        else:
            raise ValueError("Missing body object in parameter call")


        self.display(params['show'])


    def display(self, trueFalse):
        self.referential.visible = trueFalse

    def setAxisOrientation(self, pole_vec):
        pass

    def setAxisTilt(self): 
        # determine north pole to set axis of rotation
        if is_zero_vector_epsilon(self.NPole) == False:

            self.setNorthPole(self.NPole)
            return
        else:
            print "BASIC-REF::setAxisTilt: No North Pole"


    def updateReferential(self):
        self.referential.pos = self.body.Position

    def rotate(self, angle):
        self.referential.rotate(angle=(angle), axis=self.RotAxis) #ZdirectionUnit) #rotAxis)

    def setNorthPole(self, NorthPoleVector):

        J2000_Ecliptic_North = np.array([0, 0, 1])

        # initialize the direction of North Pole for this body
        # the original position is assumed to be vertical on 
        # J2000 ecliptic with the vector [0,0,1] 

        # first let's normalize the north Pole vector
        normalizedNpole = NorthPoleVector / np.linalg.norm(NorthPoleVector)

        # then Calculate the cross product to find the rotation axis to tilt the texture
        cross_product = np.cross(J2000_Ecliptic_North, normalizedNpole)

        # Calculate the dot product to figure out the angle between the vectors which
        # corresponds to how many degrees do we need to tilt the axis, around the tilt rotation axis
        dot_product = np.dot(J2000_Ecliptic_North, normalizedNpole)

        # Handle cases where vectors are nearly collinear (dot_product close to 1 or -1)
        # If vectors are almost identical, return identity matrix
        if np.isclose(dot_product, 1.0):
            return  # we are done, nothing to rotate here 

        # If vectors are almost opposite, rotate by 180 degrees around an arbitrary perpendicular axis
        elif np.isclose(dot_product, -1.0):
            axis = np.array([1,0,0])
            theta = np.pi # 180 degrees
        else:
            # Normalize the rotation axis
            axis = cross_product / np.linalg.norm(cross_product)

            # Calculate the angle
            # since V1.V2 = |V1|.|V2|.cos(theta)
            # and V1 and V2 are unit vectors, hence |V1| = |V2| = 1
            # then cos(theta) = V1.V2, hence theta = arccos(V1.V2)
            theta = np.arccos(dot_product) 


        # perform rotation to align tilt with planet North Pole
        self.referential.rotate(angle=theta, axis=axis) #, origin=(self.body.Position[0]+self.body.Foci[0],self.body.Position[1]+self.body.Foci[1],self.body.Position[2]+self.body.Foci[2]))
       
        # set axis of rotation
        #self.ZdirectionUnit = normalizedNpole[2]
        #self.YdirectionUnit = normalizedNpole[1]
        #self.XdirectionUnit = normalizedNpole[0]

        self.RotAxis = normalizedNpole


class make3DaxisReferential:

    # 3Daxis Referentials are used to illustrate the direction of a body's
    # North Pole and other directions such as the Point of Aries. It can
    # be used for sun-synchronous or inertial referentials

    def  __init__(self, params):
        # axisLock is used when the referential needs to have its axis linked to the frame
        self.referential        = None
        self.Axis 		        = [None,None,None]
        self.AxisLabel 	        = ["","",""]
        self.body               = None

        self.rotMatrix          = None
        self.NPole              = vector(0,0,0)
        self.W                  = 0
        self.Omega              = 0
        self.RotatingSign       = 1
 
        radius                  = params['radius']

        if 'parent_frame' in params and params['parent_frame'] != None:
            self.referential = frame(pos=(0,0,0), frame=params['parent_frame'])
        else:
            # this should not happen
            self.referential = frame(pos=(0,0,0))

        if 'name' in params:
            print "creating 3D "+ params['name']



        if 'initial_rotation' in params:

            # In some instances, mostly for PCPI referentials, an initial rotation 
            # is required to position the referential based on known landmarks 
            # (ie the Greenwitch meridian)

            cosv = cos(params['initial_rotation'])
            sinv = sin(params['initial_rotation'])

            self.rotMatrix = np.matrix([
            [cosv,		-sinv,	0],
            [sinv,		cosv,   0],
            [0,			0, 	    1]])

        if 'orientation' in params:

            # For planets and the sun, we need to align the referential
            # in the direction of its north Pole. This orientation is
            # calculated during the body's initialization based on the 
            # data provided in the North Pole calculation functions found
            # in orbit3D.py
            
            self.NPole = params['orientation']['pole_vec']
            self.W     = params['orientation']['w_angle']
            self.Omega = params['orientation']['omega_angle']


        if params['body'] is not None:
            self.body               = params['body']
            # check for rotation direction
            if self.body.Rotation < 0:
                print "NEGATIVE ROTATION!\n"
                self.RotatingSign = -1

            radius                  = self.body.getBodyRadius()
            self.referential.pos    = self.body.Position



        # create an array of vectors, each for a dimension of the 3D space
        size = radius * 2
        self.directions = [ vector(size*params['ratio'][0], 0, 0), 
                            vector(0, size*params['ratio'][1], 0), 
                            vector(0, 0, size*params['ratio'][2])]

        # Set the direction of the North Pole according 
        # to the orientation of the rotation 
               
        self.directions[2] = self.RotatingSign * self.directions[2]
                      
                      
#        ve = 0.2
#        if size < radius:
#            ve = 0.4

#        if tilt:
#            #self.referential.rotate(angle=(-body.TiltAngle), axis=(1,0,0))
#            self.referential.rotate(angle=(-body.TiltAngle), axis=(1,0,0))
#        if self.makeAxis ==  True:
            #position = vector(0,0,0) 

        # Add 3D axis
        for i in range (3): # Each direction
            if self.rotMatrix is not None:
                #print ".............WE HAVE A ROTATION MATRIX................"
                A = np.matrix([[self.directions[i][0]],[self.directions[i][1]],[self.directions[i][2]]], np.float64)
                self.directions[i] = self.rotMatrix * A

            if params['ratio'][i] != 0:
                if self.body and self.body.Name == "Venus":
                    print "--------->", params['ratio'][i]

                self.Axis[i] = simpleArrow(params['color'], 0, 20, vector(0,0,0), axisp = self.directions[i], context=self.referential)
                self.Axis[i].display(True) # allows axis visibility to be dependent upon their frame visibility when axisLock = True
                self.AxisLabel[i] = label( frame = self.referential, color = params['color'],  text = params['legend'][i],
                                        #pos = self.referential.pos+self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=show )
                                        pos = self.directions[i]*(1.07), opacity = 0, box = False, visible=True )

#                self.Axis[i] = simpleArrow(params['color'], 0, 20, position, axisp = self.directions[i], context=self.referential)
#                self.Axis[i].display(False) # allows axis visibility to be dependent upon their frame visibility when axisLock = True
#                self.AxisLabel[i] = label( frame = self.referential, color = params['color'],  text = params['legend'][i],
#                                            #pos = self.referential.pos+self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=show )
#                                            pos = position+self.directions[i]*(1.07+ve), opacity = 0, box = False, visible=False )


#            ve = 0.07 #####

        self.display(params['show'])

    def display(self, trueFalse):
        #self.referential.visible = trueFalse
        for i in range(3):
            if self.Axis[i] != None:
                self.Axis[i].display(trueFalse)
                self.AxisLabel[i].visible = trueFalse

    def getAbsoluteAxisVector(self, n):
        if n < 0 or n > 2:
            return None
        return self.referential.frame_to_world(self.Axis[n].pos[1])-self.referential.frame_to_world(self.Axis[n].pos[0])

 
    def setAxisTilt(self): #, rightAscension):

        # set North Pole for main planets and Sun, and for other objects
        # such as PHAs, Comets, Asteroids, set some arbitrary values
        Npole = vector(0,0,0)

        if is_zero_vector_epsilon(self.NPole) == False:
            print "3DAXIS-REF::setAxisTilt: NPole = ", self.NPole

            Npole = self.setNorthPole()
            #return

        else:
            print "3DAXIS-REF::setAxisTilt: No North Pole"

            # if we reach here, it means that we don't 
            # have a valid north pole information. 
            
            # rotate referential first
            """
            self.referential.rotate(angle=(self.tiltAngle), axis=(1,0,0))
            if rightAscension != 0:
                print "3Dref: Adjusting axis direction by ", rightAscension%360, " degrees"
                self.referential.rotate(angle=deg2rad(rightAscension % 360), axis=(0,0,1), origin=(self.body.Position[0]+self.body.Foci[0],self.body.Position[1]+self.body.Foci[1],self.body.Position[2]+self.body.Foci[2]))
            """

            # determine unit vector for each direction
            ZdirectionVec = self.referential.frame_to_world(self.Axis[2].pos[1])-self.referential.frame_to_world(self.Axis[2].pos[0])
            YdirectionVec = self.referential.frame_to_world(self.Axis[1].pos[1])-self.referential.frame_to_world(self.Axis[1].pos[0])
            XdirectionVec = self.referential.frame_to_world(self.Axis[0].pos[1])-self.referential.frame_to_world(self.Axis[0].pos[0])

            # Npole = vec(XdirectionVec, YdirectionVec, ZdirectionVec)
            
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


    def setNorthPole(self):

        #print "SetNP in 3Daxis REF for ", self.body.Name

        J2000_Ecliptic_North = np.array([0, 0, 1])

        # initialize the direction of North Pole for this body
        # the original position is assumed to be vertical on 
        # J2000 ecliptic with the vector [0,0,1] 

        # first let's normalize the north Pole vector
        normalizedNpole = self.NPole / np.linalg.norm(self.NPole)

        print "J2000_North=" + str(J2000_Ecliptic_North) + "NP=" + str(normalizedNpole)
        # then Calculate the cross product to find the rotation axis
        cross_product = np.cross(J2000_Ecliptic_North, normalizedNpole)

        # Calculate the dot product to figure out the angle between the vectors
        dot_product = np.dot(J2000_Ecliptic_North, normalizedNpole)

        # Handle cases where vectors are nearly collinear (dot_product close to 1 or -1)
        # If vectors are almost identical, return identity matrix
        if np.isclose(dot_product, 1.0):
            print "DING DING DING!!"
            return  normalizedNpole # we are done, nothing to rotate here 

        # If vectors are almost opposite, rotate by 180 degrees around an arbitrary perpendicular axis
        elif np.isclose(dot_product, -1.0):
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            axis = np.array([1,0,0])
            theta = np.pi # 180 degrees
        else:
            # Normalize the rotation axis
            axis = cross_product / np.linalg.norm(cross_product)

            # Calculate the angle
            # since V1.V2 = |V1|.|V2|.cos(theta)
            # and V1 and V2 are unit vectors, hence |V1| = |V2| = 1
            # then cos(theta) = V1.V2, hence theta = arccos(V1.V2)
            theta = np.arccos(dot_product) 


        # perform rotation to align tilt with planet North Pole. This
        # rotation is performed around the axis perpendicular to the
        # plane formed by the north pole vector and the J2000 ecliptic
        # north pole.

        print "------> TILT = ", rad2deg(theta)
        self.referential.rotate(angle=theta, axis=axis)        

        # check if the body has a retrograde motion, and in this case
        # reverse the North Pole vector

        if self.body != None and self.body.Rotation < 0:
            normalizedNpole = - normalizedNpole
            print self.body.Name + ": Inversing North Pole - ", normalizedNpole, "\n"
        else:
            print "\n"

        # set axis of rotation
        self.ZdirectionUnit = normalizedNpole[2]
        self.YdirectionUnit = normalizedNpole[1]
        self.XdirectionUnit = normalizedNpole[0]


        self.RotAxis = normalizedNpole

        return normalizedNpole


def is_zero_vector_epsilon(vec, epsilon=1e-9):
    """Checks if a 3D vector is approximately (0.0, 0.0, 0.0) within a tolerance."""
    return abs(vec[0]) < epsilon and abs(vec[1]) < epsilon and abs(vec[2]) < epsilon

"""
Body    North Pole Vector (J2000 Ecliptic Cartesian)    Tilt Angle (degrees)
Sun     (0.0130, 0.0468, 0.9988)                        7.25
Mercury (0.0000, -0.0039, 1.0000)                       0.01
Venus   (0.0543, 0.0000, -0.9985)                       177.36
Earth   (0.0000, 0.3978, 0.9175)                        23.44
Mars    (0.0613, 0.2598, 0.9639)                        25.19
Jupiter (-0.0381, 0.0090, 0.9992)                       3.13
Saturn  (-0.0084, 0.0560, 0.9984)                       26.73
Uranus  (0.7570, -0.6385, -0.1294)                      97.77
Neptune (-0.0706, -0.2831, 0.9566)                      28.32
Pluto   (0.5366, -0.7602, 0.3664)                       122.53 (or 57.47 to its orbit)

"""