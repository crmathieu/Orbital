"""
userLIB is a library class that allows to create a story programmatically. 
A story is a succession of actions that determine the location of the camera 
and its direction. Stories are found in the "stories" package.
"""

import time
from video import *

class userLIB:
    def __init__(self, solarsystem, recorder = False):
        self.solSystem = solarsystem
        self.setRecorder(recorder)

    def setRecorder(self, trueFalse):
        self.recorder = trueFalse
        if self.recorder == True:
            self.solSystem.Dashboard.orbitalTab.RecorderOn = True
            if self.solSystem.Dashboard.orbitalTab.VideoRecorder == None:
                self.solSystem.Dashboard.orbitalTab.VideoRecorder = setVideoRecording(25, "output.avi")
        else:
            self.solSystem.Dashboard.orbitalTab.RecorderOn = False
            if self.solSystem.Dashboard.orbitalTab.VideoRecorder != None:
                stopRecording(self.solSystem.Dashboard.orbitalTab.VideoRecorder)
                self.solSystem.Dashboard.orbitalTab.VideoRecorder = None

    def pause(self, seconds):
        time.sleep(seconds)

    def setCurrentBody(self, bodyName):
        
        body = self.solSystem.getBodyFromName(bodyName)
        if body != None:
            inx = self.solSystem.Dashboard.focusTab.getBodyIndexInList(bodyName)
            self.solSystem.Dashboard.focusTab.setCurrentBodyFocusManually(body, inx)
        else:
            print ("Unknown Body Name:", bodyName)

    def zoomIn(self, velocity):
        self.solSystem.camera.cameraZoom(duration = 1, velocity = velocity, recorder = self.recorder, zoom = self.solSystem.camera.ZOOM_IN)

    def zoomOut(self, velocity):
        self.solSystem.camera.cameraZoom(duration = 1, velocity = velocity, recorder = self.recorder, zoom = self.solSystem.camera.ZOOM_OUT)

    def rotateDown(self, angle):
        self.solSystem.camera.cameraRotateDown(angle, recorder = self.recorder)

    def rotateUp(self, angle):
        self.solSystem.camera.cameraRotateUp(angle, recorder = self.recorder)

    def rotateLeft(self, angle):
        self.solSystem.camera.cameraRotateLeft(angle, recorder = self.recorder)

    def rotateRight(self, angle):
        self.solSystem.camera.cameraRotateRight(angle, recorder = self.recorder)

    def setSmoothTransition(self, trueFalse):
        self.solSystem.Dashboard.focusTab.smoothTransition = trueFalse
        self.solSystem.Dashboard.focusTab.cbst.SetValue(trueFalse) 
    
    def setTransitionVelocityFactor(self, factor):
        self.solSystem.Dashboard.focusTab.setTransitionVelocity(factor)