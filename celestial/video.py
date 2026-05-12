# video.py

import cv2
import numpy as np
import pyautogui
import datetime
import os
import subprocess
import shutil

print "cv2 ==", cv2.__version__
print "numpy ==",np.__version__
print "pyautogui ==", pyautogui.__version__

def initialize_environment():
    import platform
    import ctypes
    
    # Only run DPI awareness if we are on Windows
    if platform.system() == "Windows":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass 
            
    # Add other OS-specific startup tweaks here

class VideoRecorder:
    SCREEN_SIZE = (1920, 1080)

    def __init__(self, ssys, screen, framerate):
        """
        Make sure pyautogui and wxPython (VPython 6) see 
        the same pixel grid, for a consistent ClientToScreen 
        call every time.
        """
        initialize_environment()

        self.Exclusive = False
        self.ssys = ssys
        self.screen = screen
        self.framerate = framerate
        self.frame_count = 0
        self.temp_dir = "temp_frames_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)


        # 1. Check for Maximized state to avoid the Taskbar
        # In Windows 11, the taskbar is usually ~48-60 pixels high.

        if self.ssys.Scene.win.IsMaximized():
            import wx

            # 1. Remove the title bar and borders (the 'decorations')
            current_style = self.ssys.Scene.win.GetWindowStyle()
            # Subtracting the caption and border styles
            borderless_style = current_style & ~(wx.CAPTION | wx.RESIZE_BORDER | wx.SYSTEM_MENU)
            self.ssys.Scene.win.SetWindowStyle(borderless_style)
            
            # 2. Maximize it
            self.ssys.Scene.win.Maximize(True)
            
            # 3. Force it to the top to cover the Taskbar
            self.ssys.Scene.win.Raise()

            if False:    
                # We can ask Windows for the 'Work Area' (screen minus taskbar)
                import wx
                work_area = wx.GetClientDisplayRect()
                
                # If the bottom of our canvas (y + h) is lower than the work area,
                # we clip the height so it doesn't 'see' the taskbar.
                if (self.y + self.h) > work_area.height:
                    self.h = work_area.height - self.y

             
        # Final sanitized dimensions
        self.set_capture_region()


    def OnMove(self, event):
        # This tells wx to process 'pending' events (like drawing) 
        # even though we are in a modal move loop.
        wx.GetApp().Yield()
        event.Skip() # Continue the normal move process

    def set_capture_region(self):
        """
        Calculates screen coordinates, clipping to the OS Work Area.
        Includes an 8px 'safety shave' to fully clear Windows 11 taskbar glow.
        """
        import wx
        
        # bind onMove
        self.ssys.Scene.win.Bind(wx.EVT_MOVE, self.OnMove)


        # 1. Get the current canvas position and size
        target_canvas = self.ssys.Scene.canvas
        pos = target_canvas.ClientToScreen((0, 0))
        self.x, self.y = pos.Get()
        self.w, self.h = target_canvas.GetSize().Get()

        # 2. Get the OS 'Work Area' (Screen minus Taskbar/Dock)
        work_area = wx.GetClientDisplayRect()

        # 3. Vertical Clipping with the 'Magic 8'
        # If the bottom of the canvas touches or exceeds the work area height:
        if (self.y + self.h) > work_area.height:
            # We stop exactly at the work area and then subtract 8 pixels 
            # to guarantee the taskbar is not visible.
            self.h = (work_area.height - self.y) - 8

        # 4. Horizontal Clipping (just in case of side-border bleed)
        if (self.x + self.w) > work_area.width:
            self.w = work_area.width - self.x

        # Ensure dimensions stay positive to prevent PyAutoGUI crashes
        self.w = max(0, self.w)
        self.h = max(0, self.h)
        
        print "Region Synchronized: {}x{} at ({}, {}) [8px Trim Applied]".format(
            self.w, self.h, self.x, self.y)

    def setVideoOutput(self, name):
        self.output_name = name

    def takeAshot(self):

        # Capture the exact region determined in the constructor
        img = pyautogui.screenshot(region=(self.x, self.y, self.w, self.h))
       
        # Convert RGB (pyautogui) to BGR (OpenCV)
        frame = np.array(img)
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Force the captured frame to match the VideoWriter's dimensions
        # This prevents the video from breaking if you resize the window mid-simulation.
        self.frame = cv2.resize(bgr_frame, self.screen, interpolation=cv2.INTER_AREA)

    def recordFrame(self):
        # Save frame as a physical PNG file in the temp directory instead of writing to a stream
        # Using PNG ensures no quality loss before the final FFmpeg encode

        file_path = os.path.join(self.temp_dir, "frame_{:05d}.png".format(self.frame_count))
        cv2.imwrite(file_path, self.frame)
        self.frame_count += 1    

    def closeVideo2(self):
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



    def closeVideo(self):
        import threading
    
        print "Recording stopped. Stitching started in background..."

        # 2. Define the background worker
        def stitch_worker():

            # Wait for any lingering frame-writes to finish
            while self.Exclusive:
                pass
                
            print "FFmpeg thread: Stitching frames..."

            # build set of frames to stictch together
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
            

            import platform
            import subprocess
            
            # Only use the 'No Window' flag if we are on Windows
            c_flags = 0
            if platform.system() == "Windows":
                c_flags = 0x08000000 # CREATE_NO_WINDOW literal
            
            # ... setup cmd ...

            try:

                # subprocess.call is blocking, which is fine inside a thread
                subprocess.call(cmd, creationflags=c_flags)
                print "Video saved successfully: " + self.output_name
                shutil.rmtree(self.temp_dir)
            
            except Exception as e:
                print "FFmpeg background thread failed: " + str(e)
            
            finally:

                # Optional: Clear a flag so the UI knows it's safe to record again
                self.is_stitching = False

        # 3. Launch the thread
        self.is_stitching = True
        threading.Thread(target=stitch_worker).start()


# Simplified helper functions for your OnAnimate loop
def setVideoRecording(solarSystem, framerate=20, filename="output.mp4"):
    # Note: We use .mp4 now because libx264 is better than XVID
    vr = VideoRecorder(solarSystem, VideoRecorder.SCREEN_SIZE, framerate)
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

"""
TO INSTALL PYAUTOGUI and its dependencies for python 2.7:
Install in this order:
pip install pillow==6.2.2
pip install pyscreeze==0.1.21
pip install pymsgbox==1.0.6
pip install pytweening==1.0.3
pip install pyrect==0.1.4
pip install pygetwindow==0.0.4
pip install pyperclip==1.5.27
pip install mouseinfo==0.1.2
pip install pyautogui==0.9.38
"""
