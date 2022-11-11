"""
userLIB is a library class that allows to create a story programmatically. 
A story is a succession of actions that determine the location of the camera 
and its direction. Stories are found in the "stories" package.
"""

import time
from video import *
import orbit3D
from planetsdata import LIT_SCENE, LABELS
#from utils import sleep

"""

class userLIBXX:
    def __init__(self, solarsystem):
        self.solSystem = solarsystem
        #self.setRecorder(recorder)


    def setRecorder(self, trueFalse):
        self.recorder = trueFalse
        if self.recorder == True:
            self.solSystem.Dashboard.orbitalTab.RecorderOn = True
            if self.solSystem.Dashboard.orbitalTab.VideoRecorder == None:
                self.solSystem.Dashboard.orbitalTab.VideoRecorder = setVideoRecording(framerate = 20, filename = "output.avi")
        else:
            self.solSystem.Dashboard.orbitalTab.RecorderOn = False
            if self.solSystem.Dashboard.orbitalTab.VideoRecorder != None:
                stopRecording(self.solSystem.Dashboard.orbitalTab.VideoRecorder)
                self.solSystem.Dashboard.orbitalTab.VideoRecorder = None

    def setCameraTarget(self, bodyName):
        
        body = self.solSystem.getBodyFromName(bodyName)
        if body != None:
            inx = self.solSystem.Dashboard.focusTab.getBodyIndexInList(bodyName)
            self.solSystem.Dashboard.focusTab.setCurrentBodyFocusManually(body, inx)
        else:
            print ("Unknown Body Name:", bodyName)

    ### transition primitives ###
    
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

    ### Transition Control ###

    def setSmoothTransition(self, trueFalse):
        self.solSystem.Dashboard.focusTab.smoothTransition = trueFalse
        self.solSystem.Dashboard.focusTab.cbst.SetValue(trueFalse) 
    
    def setTransitionVelocityFactor(self, factor):
        self.solSystem.Dashboard.focusTab.setTransitionVelocity(factor)

    ### Widgets ###

    def showEquator(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.eqcb.SetValue(trueFalse)
        self.solSystem.EarthRef.PlanetWidgets.showEquator(self.solSystem.Dashboard.widgetsTab.eqcb.GetValue())        

    def showLatitudes(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.latcb.SetValue(trueFalse)
        self.solSystem.EarthRef.PlanetWidgets.showLatitudes(self.solSystem.Dashboard.widgetsTab.latcb.GetValue())

    def showLongitudes(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.mrcb.SetValue(trueFalse)
        self.solSystem.EarthRef.PlanetWidgets.showLongitudes(self.solSystem.Dashboard.widgetsTab.mrcb.GetValue())

    def showTZLines(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.tzcb.SetValue(trueFalse)        
        self.solSystem.EarthRef.PlanetWidgets.showTimezones(self.solSystem.Dashboard.widgetsTab.tzcb.GetValue())

    def showTropics(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.trcb.SetValue(trueFalse)        
        self.solSystem.EarthRef.PlanetWidgets.showTropics(self.solSystem.Dashboard.widgetsTab.trcb.GetValue())

    def showEquatorialPlane(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.eqpcb.SetValue(trueFalse)        
        self.solSystem.EarthRef.PlanetWidgets.showEquatorialPlane(self.solSystem.Dashboard.widgetsTab.eqpcb.GetValue())

    def showNodes(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.ncb.SetValue(trueFalse)        
        self.solSystem.EarthRef.PlanetWidgets.showNodes(self.solSystem.Dashboard.widgetsTab.ncb.GetValue())

    def showLocalRef(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.lrcb.SetValue(trueFalse)
        self.solSystem.Dashboard.focusTab.cb.SetValue(self.solSystem.Dashboard.widgetsTab.lrcb.GetValue())
        self.solSystem.setFeature(orbit3D.LOCAL_REFERENTIAL, (self.solSystem.Dashboard.widgetsTab.lrcb.GetValue()))
        orbit3D.glbRefresh(self.solSystem, (self.solSystem.Dashboard.orbitalTab.AnimationInProgress))

    def showPlanet(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.hpcb.SetValue(not trueFalse)   
        self.solSystem.EarthRef.Origin.visible = not self.solSystem.Dashboard.widgetsTab.hpcb.GetValue()
    """

class widgets():
    ### Widgets ###
    def __init__(self, solSystem):
        self.solSystem = solSystem

    def showEquator(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.eqcb.SetValue(trueFalse)
        self.solSystem.EarthRef.PlanetWidgets.showEquator(self.solSystem.Dashboard.widgetsTab.eqcb.GetValue())        

    def showLatitudes(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.latcb.SetValue(trueFalse)
        self.solSystem.EarthRef.PlanetWidgets.showLatitudes(self.solSystem.Dashboard.widgetsTab.latcb.GetValue())

    def showLongitudes(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.mrcb.SetValue(trueFalse)
        self.solSystem.EarthRef.PlanetWidgets.showLongitudes(self.solSystem.Dashboard.widgetsTab.mrcb.GetValue())

    def showTZLines(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.tzcb.SetValue(trueFalse)        
        self.solSystem.EarthRef.PlanetWidgets.showTimezones(self.solSystem.Dashboard.widgetsTab.tzcb.GetValue())

    def showTropics(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.trcb.SetValue(trueFalse)        
        self.solSystem.EarthRef.PlanetWidgets.showTropics(self.solSystem.Dashboard.widgetsTab.trcb.GetValue())

    def showEquatorialPlane(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.eqpcb.SetValue(trueFalse)    ## added    
        self.solSystem.EarthRef.PlanetWidgets.showEquatorialPlane(trueFalse) #self.solSystem.Dashboard.widgetsTab.eqpcb.GetValue())
        #self.solSystem.EarthRef.PlanetWidgets.EqPlane.display(trueFalse)
        #orbit3D.glbRefresh(self.solSystem, (self.solSystem.Dashboard.orbitalTab.AnimationInProgress))

    def showNodes(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.ncb.SetValue(trueFalse)        
        self.solSystem.EarthRef.PlanetWidgets.showNodes(self.solSystem.Dashboard.widgetsTab.ncb.GetValue())

    def showLocalRef(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.lrcb.SetValue(trueFalse)
        self.solSystem.Dashboard.focusTab.cb.SetValue(self.solSystem.Dashboard.widgetsTab.lrcb.GetValue())
        self.solSystem.setFeature(orbit3D.LOCAL_REFERENTIAL, (self.solSystem.Dashboard.widgetsTab.lrcb.GetValue()))
        orbit3D.glbRefresh(self.solSystem, (self.solSystem.Dashboard.orbitalTab.AnimationInProgress))

    def showPlanet(self, trueFalse):
        self.solSystem.Dashboard.widgetsTab.hpcb.SetValue(not trueFalse)   
        self.solSystem.EarthRef.Origin.visible = not self.solSystem.Dashboard.widgetsTab.hpcb.GetValue()

class camera():
    def __init__(self, solSystem, recorder = False):
        self.solSystem = solSystem
        self.recorder = recorder
#        self.setRecorder(recorder)

    def litScene(self, trueFalse):
        self.setFeatures(LIT_SCENE, trueFalse)
        self.solSystem.Dashboard.orbitalTab.checkboxList[LIT_SCENE].SetValue(trueFalse)
        self.solSystem.refresh()

    def setFeatures(self, flags, trueFalse):
        return self.solSystem.setFeature(flags, trueFalse)

    def pause(self, seconds):
        #ticks = int(float(seconds) / 1e-2) 
        ticks = int(seconds * 25) # 25 = frames / sec
        #print "PAUSE ticks=", ticks, ", param was: ",seconds
        for i in range(ticks):
            #time.sleep(1e-2)
            sleep(1e-2)

            if self.recorder == True:
                #print "Pause: Record Frame"
                recOneFrame(self.solSystem.Dashboard.orbitalTab.VideoRecorder)

    ### transition primitives ###

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

    ### Transition Control ###

    def setSmoothTransition(self, trueFalse):
        self.solSystem.Dashboard.focusTab.smoothTransition = trueFalse
        self.solSystem.Dashboard.focusTab.cbst.SetValue(trueFalse) 
    
    def setTransitionVelocityFactor(self, factor):
#        self.solSystem.Dashboard.focusTab.setTransitionVelocity(factor)
        self.solSystem.camera.setTransitionVelocity(factor)
    
    def setCameraTarget(self, bodyName):
        body = self.solSystem.getBodyFromName(bodyName)
        if body is not None:
            inx = self.solSystem.Dashboard.focusTab.getBodyIndexInList(bodyName)
            self.solSystem.Dashboard.focusTab.setCurrentBodyFocusManually(body, inx)
        else:
            print ("Unknown Body Name:", bodyName)

    def gotoEarthLocation(self, locationID):
     	return self.solSystem.camera.gotoEarthLocationVertical(locationID)


    ### camera recording ###



class Api():
    def __init__(self, solarsystem, recorder = False):
        self.solSystem = solarsystem
        self.setRecorder(recorder)
        self.camera = camera(solarsystem, recorder)
        self.widgets = widgets(solarsystem)        

    def displaySolarSystem(self):
        self.solSystem.displaySolarSystem()

    def setRecorder(self, trueFalse):
        self.recorder = trueFalse
        if self.recorder == True:
            self.solSystem.Dashboard.orbitalTab.RecorderOn = True
            if self.solSystem.Dashboard.orbitalTab.VideoRecorder is None:
                self.solSystem.Dashboard.orbitalTab.VideoRecorder = setVideoRecording(framerate = 20, filename = "output.avi")
        else:
            self.solSystem.Dashboard.orbitalTab.RecorderOn = False
            if self.solSystem.Dashboard.orbitalTab.VideoRecorder is not None:
                stopRecording(self.solSystem.Dashboard.orbitalTab.VideoRecorder)
                self.solSystem.Dashboard.orbitalTab.VideoRecorder = None
