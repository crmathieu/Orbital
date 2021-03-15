import cv2
import numpy as np 
import pyautogui
import time
import datetime

"""
IMPORTANT NOTE:
When possible, it is preferable to stop the animation first before stopping the
recording, otherwise some packet corruption may occur in the video stream.
If this is the case, the corruption can be fixed by using the video tool "ffmpeg", 
using the command line:

> ffmepg -i filename.avi filename.mp4

Where filename.avi is the corrupted file. Corrupted files may still play ok but when loaded
into a video editor, they will likely be rejected.
"""

def setVideoRecording(frameRate = 20, filename = "output.avi"):
    vr = VideoRecorder(VideoRecorder.SCREEN_SIZE, "XVID", frameRate)
    dt = datetime.datetime.now()
    date_time = dt.strftime("%Y%m%d-%H%M%S")
    print "video-recordings/"+date_time+"-"+str(frameRate)+"fr/s"+"-"+filename
    vr.setVideoOutput("video-recordings/"+date_time+"-"+str(frameRate)+"frps"+"-"+filename)
    return vr

def recOneFrame(videoRecorder):
    videoRecorder.takeAshot()
#    videoRecorder.showFrame()
    videoRecorder.recordFrame()

def stopRecording(videoRecorder):
    videoRecorder.closeVideo()

class VideoRecorder:
    SCREEN_SIZE = (1920, 1080)

    def __init__(self, screen, codectype, framerate):
        self.screen = screen
        self.framerate = framerate
        self.codec = cv2.VideoWriter_fourcc(*codectype)
        # screen resolution

    def setVideoOutput(self, name):
        self.name = name
        self.out = cv2.VideoWriter(name, self.codec, self.framerate, (self.screen))
    
    def takeAshot(self):
        # make a screenshot
        img = pyautogui.screenshot() #region=(10, 10, 1900, 1060))
        # convert pixels to a numpy array to work with opencv
        frame = np.array(img)
        # convert colors from BGR to RGB
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def showFrame(self):
        cv2.imshow("screenshot", self.frame)

    def recordFrame(self):
        self.out.write(self.frame)
    
    def closeVideo(self):
        cv2.destroyAllWindows()
        self.out.release()

    def waitKey(self, t):
        return cv2.waitKey(t) & 0xFF
