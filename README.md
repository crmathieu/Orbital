# Orbital

"Orbital" is an accurate interactive 3D representation of the solar system featuring inner and outer planets, asteroids, comets and Trans-Neptunian objects. It also includes the asteroid belt, Jupiter Trojans, Kuiper belt and daily "Close Approach" bodies from the Jet Propulsion Laboratory database. In addition, the orbital elements of any object listed in the JPL small-body database can be retrieved using the "Search" tab.

3D orbits of major objects in the solar system are rendered and because the window is interactive, the user can zoom in and out as well as rotate the scene. Each object is located on its actual orbit position at the time of rendering. For a demo of the simulation go to https://youtu.be/WjiwySvZY3g. (Note: When the video was made, body rotation was not implemented yet, hence you won't see the planets spinning, but this repository includes the code that implements body rotation).

# Interacting with the simulation:

To zoom in/out: click on both mouse buttons and drag the mouse forward or backward.
To rotate the scene: click on the mouse left button only and drag the mouse sideways.

Objects listed in the drop down were collected from the JPL Small-Body Database Search Engine and the Nasa planetary factsheets. The Celestial mechanic concepts required to develop this program can be found in the Roger Bates's book "Introduction to Astrodynamics", as well as the document "Keplerian Elements for Approximate Positions of the Major Planets" (E.M. Standish from JPL Caltech).

Keep in mind that

	- Distances between each object and the sun are proportional to the actual distance.
	- Objects sizes are NOT proportional to their actual size (this is by design in order to
	  view all objects properly).
	- Asteroid belt, Kuiper belt, Jupiter Trojans are included for illustration purpose
	  only. Even though their size and thickness is somehow proportional to their actual dimension, the
	  distribution pattern within the belt is purely random/aesthetic.

# Platform:

	python 2.7.9
	vpython 6
	wxpython 3.0

you will also need the following libraries:

	numpy
	scipy

To launch the application, go to the folder where the project was downloaded and type:

	> python2.7.exe orbital.py

The vpython display window and the Orbital control modal window will take only a few seconds to load. PHA, Asteroids, Comets and trans-Neptunian objects orbits get calculated and rendered as needed, but inner and outter planets orbits are displayed right away and can be interacted with. The constant MAX_OBJECTS in solarsys.py specifies the upper limit of objects to load per data file.

<img src="./screenshot-1.jpg">

Once the Orbital Control modal pops up, you may visualize the other major bodies in the solar system: dwarf planets, Asteroid, Kuiper belts etc... All PHAs, Major Asteroids, Comets and Trans-Neptunian objects orbits can be displayed with the slideshow feature. You may pause at any time to take a closer look at trajectories by zooming in/out and rotate, and then resume. You may also animate the current object from the slideshow along with other visible objects by using the ">" play button. You may also do it frame by frame using the "+" button. The animation minimum increment is 10 minutes between frames.

Animations can be played at increased or decreased speed between - x24 to + x24, allowing to go back in time or move to the future. The time increment may vary from 10 minutes to 240 minutes (4 hours) between frames. Specific dates can also be entered directly to examin orbits relative positions. This is an interesting feature to verify passed or future events, such as close encounters between earth and PHAs (ie, Asteroid Toutatis on December 12, 2012 -or- Asteroid Midas on March 21st 2018). Remember that planets, comets or asteroids sizes are not realistic (they are much bigger than their actual size), so even though objects may look sometime very close to each other, the actual distance that separate them is much larger. A good way to figure that out is to look at the Earth MOID parameter that displays the closest distance between the object's orbit and the earth's orbit. To have a better idea of how close objects are from each other, use the checkbox "Adjust objects size" which will render a size closer to reality.

You may also pick individual objects from the dropdown box to display and animate their trajectories in orbit. When an animation or a slideshow is in progress, the drop down box is disabled and picking an object from it will have no effect. A slideshow must be fully stopped (not just paused) to enabled the drop down box again.

The current object orbital elements are displayed at the bottom of the Orbital Control dialog.
Legend is:

	i: Orbital Inclinaison
	N: Longitude of Ascending node
	w: Argument of Perihelion
	e: Orbit Eccentricity
	q: Perihelion distance to the sun

	M: Mass in kg
	R: Average radius in km
	P: Orbital Period in years

	Moid: Minimum Orbital Intersection Distance (in this case with Earth) in Astronomical Units (AU)
	Velocity: The current velocity on orbit (this will be updated during animation) in kilometers/sec
	DTE: The current Distance To Earth in AU

# POV:

You have the ability to change the Point Of View (POV) to reset the center of the scene on any object of your choice. By default, the POV is focused on the Sun, but it can be set on any of the major inner / outer planets, the dwarf planets - or - on the body that you are currently studying.

<img src="./screenshot-3.jpg">

# Most important Files:
```text
	orbital.py ....................... Orbital entry point
	celestial/__main__.py ............ bootloader
	celestial/camera.py .............. Camera movements
	celestial/controls.py ............ Orbital controller class used in the "Orbital Control" user interface
	celestial/location.py ............ Earth location functions
	celestial/numberfmt.py ........... String precision formatting
	celestial/objects.py ............. Library of 3D objects
	celestial/orbit3D.py ............. Orbit trajectories and belts calculations classes
	celestial/orbitalLIB.py .......... library class allowing to create an animation (story) programmatically
	celestial/planetsdata.py ......... Orbital elements for major planets and belts
	celestial/rate_func.py ........... Rate functions defined for animations
	celestial/referentials.py ........ Planet Referentials classes
	celestial/utils.py ............... Linear Algebra utility functions
	celestial/video.py ............... Animation recording class
	celestial/vpython_interface.py ... Modify vpython "display" class
	celestial/widgets.py ............. Earth widgets classes
```

# Close Approach Data:

"Orbital" allows you to find out which asteroids "close encounters" with earth are happening on a daily basis. If you click on the "Search" tab, the "Close Approach Data" section will directly fetch from the JPL database the list of objects that are at their closest position to earth for the current day (If you would rather look for information on a particular object, use the Search input field in the lower section).

<img src="./screenshot-2.jpg">

Once the list has been downloaded, you may also get the list from the previous or the next day. Double clicking on a row in that list will automatically display the orbit and position of the corresponding object, as well as switch back to the "Main" tab to detail its orbital elements.

Note: The autoscale feature in vpython is a bit erratic. If you are in a very expansive view that includes far objects such as dwarf planets and also closer to the sun objects like inner planets, unchecking the far objects and refreshing the scene may "autoscale" you back inside the sun (even though everything looks black). To eliminate the problem, simply perform a zoom out.

The planets and the sun rotate on their axis in a realistic way, according to their rotation rate. You may note that Venus and Pluto have a retrograde motion and it is because of their north pole reversion. A good way to clarify what is happening is to check the "Show Local Referential" checkbox in the"Animation POV" tab. Also note the great range of rotation rates among the planets, from really fast (the outter planets) to really slow (Venus).

List of a few close encounters between Potentially Harzardous Asteroids and earth:

	YU55	 	11/08/2011
	TOUTATIS 	12/12/2012
	MIDAS    	03/21/2018
	2004 XK50 	12/24/2025


# How to install the platform on Windows computer:

	1) Install python2.7 64 bits:
	go to "https://www.python.org/downloads/release/python-279/" and under "Files",
	click on "Windows x86-64 MSI installer". Download the installer and run it.

	use the default install configuration. Your python folder should be
	in c:\python27

	If you get the error "error: Microsoft Visual C++ 9.0 is required. Get it from http://aka.ms/vcpython27"
	then from "https://www.microsoft.com/en-us/download/confirmation.aspx?id=44266" download the VC runtime
	installer: VCForPython27.msi and run it to install the missing runtime library. Then try to run the python27
	installer again to finish installing python.

	Add "c:\python27" and "c:\python27\scripts" to your PATH environment variable

	2) Install Numpy and Scipy libraries:
	go to http://www.lfd.uci.edu/~gohlke/pythonlibs
	- download numpy+mkl: "numpy-1.13.1+mkl-cp27-cp27m-win_amd64.whl"
	- download scipy: "scipy-0.19.1-cp27-cp27m-win_amd64.whl"

	3) In order to have a smooth library install, first make sure the program "pip.exe" is up to date.
	"pip.exe" is under c:\python27\Scripts. From the command prompt type:

	"python -m pip install --upgrade pip"

	4) then install the modules you previously downloaded using the pip program:

	pip install -U numpy-1.13.1+mkl-cp27-cp27m-win_amd64.whl
	pip install -U scipy-0.19.1-cp27-cp27m-win_amd64.whl

	if you get a message "<wheelname> is not a supported wheel on this platform", despite the
	fact that you already updated pip, it means you probably downloaded the wrong library for this
	version of python. Make sure the library is the correct one.

	5) Install vPython:
	go to http://vpython.org/contents/download_windows.html
	and download the installer: "VPython-Win-64-Py2.7-6.11"

	Once downloaded, run it. This installer will also install the wxPython 3.0 library.
	That's it!

# How to install on a Mac

	If you already have a version of VPython 6, it's a good idea to uninstall it before installing
	the new VPython 6.11. (If you have VPython 5 installed, you need to delete the old folders visual,
	vis, and vidle from /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages.)

	First, download and install Python-2.7.9 from python.org.
	(https://www.python.org/ftp/python/2.7.9/python-2.7.9-macosx10.6.pkg)

	Second, install VPython-Mac-Py2.7-6.11
	(http://sourceforge.net/projects/vpythonwx/files/6.11-release/VPython-Mac-Py2.7-6.11.dmg/download)

	This version of VPython requires Python 2.7.x from python.org. VPython will not work with the version
	of Python 2.7 that is part of the standard OSX, nor will it work with versions of Python other than the
	one from python.org.

	Open the VPython installer (Doubleclick VPython-Mac-Py2.7-6.11.pkg.)


Enjoy the simulation!

### Share
[<img src="./twitter.png">](https://twitter.com/intent/tweet?text=Download+Orbital,+the+Solar+System+Simulation&url=https://github.com/crmathieu/Orbital)
[<img src="./fb.png">](https://www.facebook.com/sharer/sharer.php?t=Download+Orbital,+the+Solar+System+Simulation&u=https://github.com/crmathieu/Orbital)
[<img src="./linkedin.png">](https://linkedin.com/shareArticle?mini=true&title=Download+Orbital,+the+Solar+System+Simulation&url=https://github.com/crmathieu/Orbital)
