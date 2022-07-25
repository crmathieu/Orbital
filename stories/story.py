class storyBase:
    def __init__(self, solSystem, api):
        self.solSystem = solSystem
        self.solSystem._set_autoMovement(True)
        self.play(api)
        #api.camera.zoomOut(0.1)
        self.solSystem._set_autoMovement(False)
        # make sure we stopped potential video recording
        api.setRecorder(False)

    def play(self, api):
        pass