
class userAPI:
    def __init__(self, solarsystem):
        self.solSystem = solarsystem

    def setCurrentBody(self, bodyName):
        body = self.solSystem.getBodyFromName(bodyName)
        if body != None:
            inx = self.solSystem.Dashboard.focusTab.getBodyIndexInList(bodyName)
            self.solSystem.Dashboard.focusTab.setCurrentBodyFocusManually(body, inx)
        else:
            print "Unknown Body Name:", bodyName

    def zoomIn(self, velocity):
        self.solSystem.introZoomIn(velocity)

    def rotateDown(self, angle):
        self.solSystem.camera.cameraRotateDown(angle)


