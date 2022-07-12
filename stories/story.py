class storyBase:
    def __init__(self, solSystem, api):
        self.solSystem = solSystem
        self.api = api
        self.play(api)

    def play(self, api):
        pass