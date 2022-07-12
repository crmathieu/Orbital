# approach.py
# example of story file containing stories to play as introduction.
# A story is defined as a python class deriving from a storyBase class.
# a 'play' method must be defined for the story to play when called by the
# solar system loader. The play method has only one parameter: lib, which
# gives it access to the set of userLIB methods that can be used to create a
# story.
#  
# to play the story 'earthApproach' defined in the approach.py module, enter:
# > python2.7 orbital.py stories.approach earthApproach
# to dislay a playlist, do not specify the story to play.
# > python2.7 orbital.py stories.approach 
# will list:
# (1) earthApproach
# (2) jupiterApproach

from story import storyBase

class earthApproach(storyBase):

    def play(self, lib):
        lib.setCurrentBody("earth")
        lib.zoomIn(75)
        lib.rotateDown(60)
        lib.rotateLeft(120)
        lib.pause(0.2)
        lib.rotateUp(30)
        lib.zoomOut(20)
        lib.setSmoothTransition(True)
        lib.setCurrentBody("jupiter")
        
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


class jupiterApproach(storyBase):

    def play(self, lib):
        lib.setCurrentBody("jupiter")
        lib.zoomIn(50)
        lib.rotateDown(140)
