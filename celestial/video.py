# video.py

import cv2
import numpy as np
import pyautogui
import datetime
import os
import subprocess
import shutil

class VideoRecorder:
    SCREEN_SIZE = (1920, 1080)

    def __init__(self, screen, framerate):
        self.Exclusive = False
        self.screen = screen
        self.framerate = framerate
        self.frame_count = 0
        self.temp_dir = "temp_frames_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def setVideoOutput(self, name):
        self.output_name = name

    def takeAshot(self):
            # Capture the actual screen
            img = pyautogui.screenshot()
            frame = np.array(img)
            
            # Convert RGB (pyautogui) to BGR (OpenCV)
            bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # IMPORTANT: Resize the frame to match the expected video resolution
            # This prevents the "empty video" bug caused by resolution mismatches.
            self.frame = cv2.resize(bgr_frame, self.screen, interpolation=cv2.INTER_AREA)

    def takeAshot2(self):
        # Capture screenshot
        img = pyautogui.screenshot()
        frame = np.array(img)
        # Convert RGB to BGR for OpenCV consistency if needed, 
        # but for direct saving to PNG, RGB is fine.
        self.frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    def recordFrame(self):
        # Save frame as a physical PNG file in the temp directory instead of writing to a stream
        # Using PNG ensures no quality loss before the final FFmpeg encode

        file_path = os.path.join(self.temp_dir, "frame_{:05d}.png".format(self.frame_count))
        cv2.imwrite(file_path, self.frame)
        self.frame_count += 1    

    def closeVideo(self):
        # 1. Wait for any threads
        while self.Exclusive:
            pass
            
        # 2. Call FFmpeg to stitch images
        print "Stitching frames with FFmpeg..."
        input_pattern = os.path.join(self.temp_dir, "frame_%05d.png")
        
        cmd = [
            'ffmpeg', '-y', 
            '-framerate', str(self.framerate), 
            '-i', input_pattern, 
            '-c:v', 'libx264', 
            '-pix_fmt', 'yuv420p', 
            '-crf', '18', 
            self.output_name
        ]
        
        try:
            subprocess.call(cmd)
            print "Video saved successfully: " + self.output_name
            # 3. Clean up temporary frames
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            print "FFmpeg failed. Frames are preserved in: " + self.temp_dir
            print str(e)

# Simplified helper functions for your OnAnimate loop
def setVideoRecording(framerate=20, filename="output.mp4"):
    # Note: We use .mp4 now because libx264 is better than XVID
    vr = VideoRecorder(VideoRecorder.SCREEN_SIZE, framerate)
    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    full_path = "video-recordings/" + dt + "-" + filename
    
    if not os.path.exists("video-recordings"):
        os.makedirs("video-recordings")
        
    vr.setVideoOutput(full_path)
    return vr

def recOneFrame(videoRecorder):
    videoRecorder.Exclusive = True

    videoRecorder.takeAshot()
    videoRecorder.recordFrame()
    videoRecorder.Exclusive = False

def stopRecording(videoRecorder):
    print "video recording STOPPED"
    videoRecorder.closeVideo()
