# approach.py
# example of story file containing stories to play as introduction.
# A story is defined as a python class deriving from a storyBase class.
# a 'play' method must be defined for the story to play when called by the
# solar system loader. The play method has only one parameter: lib, which
# gives it access to the set of userLIB methods that can be used to create 
# the actions that define the story.
#  
# The generic way to play a story is:
# > python2.7 orbital.py stories.<story_module> <story_name>
# 
# Where:
#   - <story_module> is a python file where stories can be found. Do not use the ".py"
#     file extension when you specify a story module.
#   - <story_name> is a python class containing a "play" method. This python class must 
#     be defined in the <story_module>.
#
# to play the story 'story_earthApproach' defined in the approach.py module, enter:
# > python2.7 orbital.py stories.approach story_earthApproach
#
# to dislay a playlist, do not specify the story to play.
# > python2.7 orbital.py stories.approach 
# will list:
# (1) story_earthApproach
# (2) story_jupiterApproach

from story import storyBase

class story_earthApproach(storyBase):

    def play(self, lib):
        lib.setCurrentBody("earth")
        lib.zoomIn(75)
        #self.solSystem.camera.newCameraRotation(360)
        #lib.rotateDown(60)
        lib.rotateDown(45)
        lib.rotateLeft(120)
        lib.pause(0.2)
        lib.showEquator(True)
        lib.rotateUp(180)
        lib.showLatitudes(True)
        lib.rotateLeft(90)
        lib.showLongitudes(True)
        lib.rotateRight(90)
        lib.pause(1)
        lib.showLocalRef(True)
        lib.rotateDown(90)
        lib.showLocalRef(True)
        lib.showEquator(False)
        
        lib.zoomOut(30)
        lib.zoomIn(15)
        lib.showEquatorialPlane(True)
        lib.rotateRight(120)
        lib.showNodes(True)
        


        """"

        lib.setSmoothTransition(True)
        lib.setTransitionVelocityFactor(1.0)

        lib.setCurrentBody("jupiter")
        lib.pause(1)

        lib.setCurrentBody("mercury")
        lib.zoomIn(20)
        lib.pause(1)

        lib.setCurrentBody("mars")
        lib.pause(1)

        lib.zoomOut(20)
        lib.setCurrentBody("saturn")
        lib.pause(1)

        lib.setCurrentBody("neptune")
        lib.zoomIn(15)
        lib.pause(1)

        lib.setCurrentBody("venus")

#        lib.pause(1)
#        lib.setCurrentBody("sedna")
        """

class story_jupiterApproach(storyBase):

    def play(self, lib):
        lib.setCurrentBody("jupiter")
        lib.zoomIn(50)
        lib.rotateDown(140)
