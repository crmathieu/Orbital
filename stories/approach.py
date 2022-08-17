# approach.py
# example of story file containing stories to play as introduction.
# A story is defined as a python class deriving from a storyBase class.
# a 'play' method must be defined for the story to play when called by the
# solar system loader. The play method has only one parameter: Api, which
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

    def play(self, Api):
        Api.camera.setCameraTarget("earth")
        Api.displaySolarSystem()

        Api.camera.zoomIn(75)
        #self.solSystem.camera.newCameraRotation(360)
        #Api.rotateDown(60)
#        Api.camera.rotateDown(45)
        Api.camera.rotateLeft(80)
        #Api.camera.pause(0.2)
        #Api.widgets.showEquator(True)
        """
        Api.camera.rotateUp(180)
        Api.widgets.showLatitudes(True)
        Api.camera.rotateLeft(90)
        Api.widgets.showLongitudes(True)
        Api.camera.rotateRight(90)
        Api.camera.pause(1)
        Api.widgets.showLocalRef(True)
        Api.camera.rotateDown(30)
#        Api.widgets.showLocalRef(True)
#        Api.widgets.showEquator(False)
        """
        #Api.camera.zoomOut(30)
        #Api.camera.zoomIn(35)
        #Api.widgets.showNodes(True)
        #Api.camera.pause(1)
        Api.camera.rotateRight(120)
        #Api.widgets.showEquatorialPlane(True)
        Api.camera.pause(1)

        Api.camera.setSmoothTransition(True)
        Api.camera.setTransitionVelocityFactor(1.0)
        Api.camera.litScene(True)
        Api.camera.pause(1)
        
        Api.camera.gotoEarthLocation(self.locList.TZ_RUS_BAIK)
        Api.camera.gotoEarthLocation(self.locList.TZ_CHN_XI)
        Api.camera.gotoEarthLocation(self.locList.TZ_FR_KOUR)
        Api.camera.gotoEarthLocation(self.locList.TZ_FR_PARIS)
        Api.camera.gotoEarthLocation(self.locList.TZ_JP_TAN)
        Api.camera.gotoEarthLocation(self.locList.TZ_EG_CAIRO)
        Api.camera.gotoEarthLocation(self.locList.TZ_US_VDBERG)

        Api.camera.zoomOut(20)
        Api.camera.setCameraTarget("jupiter")
        Api.camera.pause(1)

        """"
        Api.camera.setCameraTarget("mercury")
        Api.camera.zoomIn(20)
        Api.pause(1)

        Api.camera.setCameraTarget("mars")
        Api.pause(1)

        Api.camera.zoomOut(20)
        Api.camera.setCameraTarget("saturn")
        Api.pause(1)

        Api.camera.setCameraTarget("neptune")
        Api.camera.zoomIn(15)
        Api.pause(1)

        Api.camera.setCameraTarget("venus")

#        Api.pause(1)
#        Api.camera.setCameraTarget("sedna")
        """

class story_jupiterApproach(storyBase):

    def play2(self, Api):
        Api.camera.setCameraTarget("jupiter")
        Api.camera.zoomIn(50)
        Api.camera.rotateDown(140)
