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

    def play(self, lib):
        #lib = self.lib
        #lib.setRecorder(True)
        lib.setCurrentBody("earth")
        lib.zoomIn(75)
        lib.rotateDown(60)
        lib.rotateLeft(120)
        lib.pause(0.2)
        lib.rotateUp(30)
        lib.zoomOut(20)
        lib.setSmoothTransition(True)
        lib.setCurrentBody("jupiter")
        return 

        lib.pause(0.2)
        lib.setCurrentBody("mercury")

        lib.pause(0.2)
        lib.setCurrentBody("mars")

        lib.pause(0.2)
        lib.setCurrentBody("saturn")

        lib.pause(0.2)
        lib.setCurrentBody("Neptune")

        lib.pause(0.2)
        lib.setCurrentBody("venus")

        lib.pause(0.2)
        lib.setCurrentBody("sedna")
        #lib.setRecorder(False)


class jupiterApproach(storyBase):

    def play(self, lib):
        lib.setCurrentBody("jupiter")
        lib.zoomIn(50)
        lib.rotateDown(140)
