class storyBase:
    def __init__(self, solSystem, lib):
        self.solSystem = solSystem
        self.lib = lib

        self.solSystem._set_autoMovement(True)
        self.play(lib)
        self.solSystem._set_autoMovement(False)
        # make sure we stopped potential video recording
        self.lib.setRecorder(False)

    def play(self, lib):
        pass