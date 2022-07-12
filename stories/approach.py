# approach.py
# example of story file containing stories to play as introduction.
# to play the story earthApproach, enter:
# > python2.7 orbital.py stories.approach earthApproach
# to dislay a playlist, do not specify the story to play.
# > python2.7 orbital.py stories.approach 
# will list:
# (1) earthApproach
# (2) jupiterApproach

from story import storyBase

class earthApproach(storyBase):

    def play(self):
        api = self.api
        api.setCurrentBody("earth")
        api.zoomIn(75)
        api.rotateDown(60)
        api.rotateLeft(120)
        api.pause(0.2)
        api.rotateUp(30)
        api.zoomOut(20)
        api.setSmoothTransition(True)
        api.setCurrentBody("jupiter")

        api.pause(0.2)
        api.setCurrentBody("mercury")

        api.pause(0.2)
        api.setCurrentBody("mars")

        api.pause(0.2)
        api.setCurrentBody("saturn")

        api.pause(0.2)
        api.setCurrentBody("Neptune")

        api.pause(0.2)
        api.setCurrentBody("venus")

        api.pause(0.2)
        api.setCurrentBody("sedna")


class jupiterApproach(storyBase):

    def play(self):
        api = self.api #userAPI(self.solSystem)
        api.setCurrentBody("jupiter")
        api.zoomIn(50)
        api.rotateDown(140)
