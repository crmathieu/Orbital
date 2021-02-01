import cv2
import numpy as np 
import pyautogui
import time

class VideoRecorder:
    def __init__(self, screen, codectype, framerate):
        self.screen = screen
        self.framerate = framerate
        self.codec = cv2.VideoWriter_fourcc(*codectype)

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
