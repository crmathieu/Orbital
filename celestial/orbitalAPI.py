import time

class userAPI:
    def __init__(self, solarsystem):
        self.solSystem = solarsystem

    def pause(self, seconds):
        time.sleep(seconds)

    def setCurrentBody(self, bodyName):
        body = self.solSystem.getBodyFromName(bodyName)
        if body != None:
            inx = self.solSystem.Dashboard.focusTab.getBodyIndexInList(bodyName)
            self.solSystem.Dashboard.focusTab.setCurrentBodyFocusManually(body, inx)
        else:
            print "Unknown Body Name:", bodyName

    def zoomIn(self, velocity):
        self.solSystem.introZoomIn(velocity)

    def zoomOut(self, velocity):
        self.solSystem.camera.cameraZoom(duration = 1, velocity = velocity, zoom = self.solSystem.camera.ZOOM_OUT)

    def rotateDown(self, angle):
        self.solSystem.camera.cameraRotateDown(angle)

    def rotateUp(self, angle):
        self.solSystem.camera.cameraRotateUp(angle)

    def rotateLeft(self, angle):
        self.solSystem.camera.cameraRotateLeft(angle)

    def rotateRight(self, angle):
        self.solSystem.camera.cameraRotateRight(angle)

    def setSmoothTransition(self, trueFalse):
        self.solSystem.Dashboard.focusTab.smoothTransition = trueFalse