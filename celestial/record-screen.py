from video import VideoRecorder

# screen resolution
SCREEN_SIZE = (1920, 1080)

# define the codec
"""
In Fedora: DIVX, XVID, MJPG, X264, WMV1, WMV2. (XVID is more preferable. MJPG results in high size video. X264 gives very small size video)
In Windows: DIVX (More to be tested and added)
In OSX : (I don't have access to OSX. Can some one fill this?)

"""

vr = VideoRecorder(SCREEN_SIZE, "XVID", 20.0)
vr.setVideoOutput("output.avi")
total = 0
while True:
    vr.takeAshot()
    vr.showFrame()
    vr.recordFrame()

    k = vr.waitKey(1)  
    #if k == ord("q"):
    #    break
    total = total + 1
    if total > 100:
        break

vr.closeVideo()


#////////////////////////////////////////////////
"""
codec = cv2.VideoWriter_fourcc(*"XVID")

# create video write object
out = cv2.VideoWriter("output.avi", codec, 25.0, (SCREEN_SIZE))

while True:
    # make a screenshot
    img = pyautogui.screenshot() #region=(0, 0, 300, 400))
    # convert pixels to a numpy array to work with opencv
    frame = np.array(img)

    # convert colors from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # write the frame
    out.write(frame)

    #show the frame
    #cv2.imshow("screenshot", frame)

    # if user click "q", exit loop. The parameter passed is the time in milliseconds we wait to detect an keystroke
    k = cv2.waitKey(10) & 0xFF  
    if k == ord("q"):
        break

    #time.sleep(1)

# make sure everything is closed when exiting
cv2.destroyAllWindows()
out.release()

"""