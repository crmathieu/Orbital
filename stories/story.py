class storyBase:
    def __init__(self, solSystem, api):
        self.solSystem = solSystem
        self.api = api

        self.solSystem._set_autoMovement(True)
        self.play(api)
        self.solSystem._set_autoMovement(False)

    def play(self, api):
        pass