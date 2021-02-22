import cv2
import numpy as np 
import pyautogui
import time
import datetime

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
