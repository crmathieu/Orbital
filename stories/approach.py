# approach.py
# should be used as:
# > python2.7 orbital.py stories.approach earthApproach
# to dislay a playlist, do not specify the story to play.
# > python2.7 orbital.py stories.approach 


from story import storyBase

class earthApproach(storyBase):

    def play(self):
        api = self.api
        api.setCurrentBody("earth")
        api.zoomIn(75)
        api.rotateDown(140)

        """
        solSystem.Dashboard.focusTab.setCurrentBodyFocusManually(solSystem.EarthRef, 2)
        solSystem.introZoomIn(75) #38)
        ###	solSystem.camera.cameraPanUp(1, 20)
        ###	solSystem.camera.cameraLeft(1, 20)
        solSystem.camera.cameraRotateDown(140)
        """

class jupiterApproach(storyBase):

    def play(self):
        api = self.api #userAPI(self.solSystem)
        api.setCurrentBody("jupiter")
        api.zoomIn(50)
        api.rotateDown(140)
