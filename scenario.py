import celestial.__main__

class runScenario:
    def play(self, solSystem):
        solSystem.Dashboard.focusTab.setCurrentBodyFocusManually(solSystem.EarthRef, 2)
        solSystem.introZoomIn(75) #38)
        ###	solSystem.camera.cameraPanUp(1, 20)
        ###	solSystem.camera.cameraLeft(1, 20)
        solSystem.camera.cameraRotateDown(140)
        