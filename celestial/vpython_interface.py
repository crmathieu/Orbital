from visual import display, set_cursor
import platform

# ViewPort, a subclass of cvisual.display, is provided as a way to override certain
# display methods related to mouse event handling, when it comes to interacting with 
# the scene elements (zoom, rotations etc...)
class ViewPort(display):
    def __init__(self, **keywords):
        # invoke normal display constructor ...
        super(ViewPort, self).__init__(**keywords)

        # ... and add a few more information:
        # Indicates when an animation automatically zooms in an pans around a focus point
        self._auto_movement = False 
        self.plat = platform.system()

    def getDisplay(self):
        return super

    # method to change the status of _auto_movement
    def _set_autoMovement(self, is_movement):
        self._auto_movement = is_movement
        if is_movement == False:
            self._resetMouse()

    def _resetMouse(self):
        self._mt.leftIsDown = self._mt.rightIsDown = self._mt.middleIsDown = 0
        self._mt.lastSpinning = self._mt.lastZooming = 0
        self._mt.macCtrl = 0

    def _report_mouse_state(self, evt, defx=20, defy=20): # wx gives x,y relative to upper left corner
        # this method is directly taken from the display class and modified to get the desired effect
        x, y = defx, defy
        if evt != None:
            x, y = evt.GetPosition()

        if self._lastx is None:
            self._lastx = x
            self._lasty = y

        zooming = self._mt.isZooming(evt, self.userzoom, self.userspin)
        spinning = self._mt.isSpinning(evt, self.userzoom, self.userspin, zooming)
        lock = self._mt.checkLock(spinning, zooming)
        
        if lock and not self._captured:
            self.cursor_state = self.cursor.visible
            set_cursor(self.canvas, False)
            if self.fillswindow:
                self._cursorx, self._cursory = (x, y)
            else:
                # cursor is based on (0,0) of the window; our (x,y) is based on (0,0) of the 3D display
                self._cursorx, self._cursory = (int(self._x)+x, int(self._y)+y)
            self._canvas.CaptureMouse()
            self._captured = True
        elif self._captured and not (spinning or zooming):
            self.win.WarpPointer(self._cursorx, self._cursory)
            self._lastx = x = self._cursorx
            self._lasty = y = self._cursory
            set_cursor(self.canvas, self.cursor_state)
            self._canvas.ReleaseMouse()          
            self._captured = False
        
        
        #
        # So... we're going to report left/right/middle
        #

        left = self._mt.leftIsDown and not spinning and not zooming
        right = spinning or self._mt.rightIsDown
        middle = zooming or self._mt.middleIsDown
        shift = evt.ShiftDown()
        ctrl = evt.ControlDown()
        alt = evt.AltDown()
        cmd = evt.CmdDown()
                
        if self.plat == 'Macintosh' and ctrl and cmd:
            #
            # Weird... if the user holds the cmd key, evt.ControlDown() returns True even if it's a lie.
            # So... we don't know if it's *really* down or not. ;-(
            #
            ctrl = False
        
#         labels = [s.strip() for s in "x, y, left, middle, right, shift, ctrl, alt, cmd, spin, zoom, lock, cap".split(',')]
#         vals = (x, y, left, middle, right, shift, ctrl, alt, cmd, spinning, zooming, lock, self._captured)
#         fmts = ["%9s"]*len(vals)
#         for l,f in zip(labels,fmts):
#             print(f % l, end='')
#         print()
#         for v,f in zip(vals,fmts):
#             print(f % `v`, end='')
#         print()
##        if trigger == 'leftdown' and not self._rightdown:
##            if ctrl:
##                right = 1
##                left = 0
##            elif alt:
##                middle = 1
##                left = 0

#        if (spinning or zooming) and (x == self._lastx) and (y == self._lasty): return

        # CM: whenever there is an auto_movement, do not call report_mouse_state as it 
        # could interfer with camera methods that also call the "report_mouse_state"
        # from the display class 

        if self._auto_movement == True:
            self._resetMouse()
            return 

        self.report_mouse_state([left, right, middle],
                self._lastx, self._lasty, x, y,
                [shift, ctrl, alt, cmd])


        # For some reason, handling spin/zoom in terms of movements away
        # from a fixed cursor position fails on the Mac. As you drag the
        # mouse, repeated move mouse events mostly give the fixed cursor position.
        # Hence, for now, dragging off-screen stops spin/zoom on the Mac.
        # Similar problems on Ubuntu 12.04, plus wx.CURSOR_BLANK not available on Linux.
        
        if (spinning or zooming) and (self.plat != 'Macintosh'): # reset mouse to original location
            self.win.WarpPointer(self._cursorx, self._cursory)
            if self.fillswindow:
                self._lastx = self._cursorx
                self._lasty = self._cursory
            else:
                # cursor is based on (0,0) of the window; our (x,y) is based on (0,0) of the 3D display
                self._lastx = self._cursorx - int(self._x)
                self._lasty = self._cursory - int(self._y)
        else: 
            self._lastx = x
            self._lasty = y
        


class Color:
    black = (0,0,0)
    white = (1,1,1)
    whiteish = (0.9, 0.9, 0.9)
    grey = (0.5,0.5,0.5)
    deepgrey = (0.32, 0.32, 0.32)
    darkgrey = (0.04, 0.04, 0.04)
    lightgrey = (0.75,0.75,0.75)

    red = (1,0,0)
    redish = (0.5, 0, 0)
    green = (0,1,0)
    greenish = (0, 0.5, 0)
    blue = (0,0,1)
    blueish = (0, 0, 0.5)
    darkblue = (0, 0, 0.2)

    yellow = (1,1,0)
    yellowish = (0.5, 0.5, 0)
    cyan = (0,1,1)
    cyanish = (0, 0.5, 0.5)
    magenta = (1,0,1)
    magentish = (0.5, 0, 0.5)
    dirtyYellow = (0.5,0.5,0)
    orange = (1,0.6,0)
    #nightshade = (0.12, 0.12, 0.12)
    nightshade = (0.05, 0.05, 0.05)

