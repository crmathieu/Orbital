# Orbital
An accurate interactive 3D representation of the solar system featuring inner and outter planets, asteroids, 
comets and Trans-Neptunian objects. Also includes the asteroid belt, Jupiter Trojans, Kuiper belt and inner 
Oort cloud.

3D orbits of major objects in the solar system are rendered and can be zoomed in and out as well as rotated. Each 
object is located on its actual orbit position at the time of rendering.

Interacting with the simulation:

To zoom in/out: click on both mouse buttons and drag the mouse forward or backward.
To rotate the scene: click on the mouse left button only and drag the mouse sideways.

All data was collected from the JPL Small-Body Database Search Engine and the Nasa planetary factsheets.

Keep in mind that

	- All distances between each object and the sun are proportional to the actual distance.
	- Objects sizes are NOT proportional to their actual size (this is by design in order to 
	  view all objects properly).
	- Asteroid belt, Kuiper belt, Jupiter Trojans and Oort Cloud are included for illustration purpose only. 
	  Even though their size and thickness is somehow proportional to their actual dimension, the distribution 
	  pattern within the belt is purely random/aesthetic.
	
Platform:

	python 2.7.9
	vpython 6
	wxpython 3.0

you will also need the following libraries:

	numpy
	scipy

To launch the application, go to the folder where the project was downloaded and type:

	> python2.7.exe solarsys.py
	
The vpython display window and the Orbital control modal window will take a few second to load. PHA, Asteroids, Comets and trans-Neptunian objects orbits get calculated and rendered as needed, but inner and outter planets orbits are displayed right away and can be interacted with. The constant MAX_OBJECTS in solarsys.py specifies the upper limit of objects to load per data file.

Once the Orbital Control modal pops up, you may visualize the other major bodies in the solar system: dwarf planets, Asteroid / Kuiper belts etc... All PHAs, Major Asteroids, Comets and Trans-Neptunian objects' orbits can be displayed with the slideshow feature. You may pause at any time to take a closer look at trajectories by zooming in/out and rotate, and then resume. You may also animate the current object from the slideshow along with other visible objects by using the ">" play button. You may also do it step by step using the "+" button. 

Animations can be played at increased or decreased speeds between - x20 to + x20, allowing to go back in time as well as in the future. Specific dates can also be entered directly to examin orbits relative positions. That is an interesting feature to verify passed or future events, such as close encounters between earth and PHAs (ie, Asteroid Toutatis on December 12, 2012 -or- Asteroid Midas on March 21st 2018). Remember that planets, comets or asteroids sizes are not realistic (they are much bigger than their actual size), so even though objects may look sometime very close to each other, the actual distance that separate them is much larger. A good way to figure that out is to look at the Earth MOID parameter that displays the closest distance between the object's orbit and the earth's orbit.

You may also pick individual objects from the drop down box to display and animate their trajectories on orbit. When an animation or a slideshow is in progress, the drop down box is disabled and picking an object will have no effect. A slideshow must be fully stopped (not just paused) to enabled the drop down box again.

The current object orbital elements are displayed at the bottom of the Orbital Control dialog. 
Legend is:

	i: Orbital Inclinaison
	N: Longitude of Ascending node
	w: Argument of Perihelion
	e: Orbit Eccentricity
	q: Perihelion distance to the sun

	M: Mass in kg
	R: Average radius in Km
	P: Orbital Period in years

	Moid: Minimum Orbital Intersection Distance (in this case with Earth) in Astronomical Units (AU)
	Velocity: The current velocity on orbit (this will be updated during animation) in kilometers/sec

Files:

	solarsys.py: 	Main file
	orbital.py:  	Orbits trajectory and belts calculations classes
	controls.py:	Orbital controller class used in the "Orbital Control" user interface
	planetsdata.py:	Orbital elements for major planets and belts
	

	
Note: There is a bug in the autoscale feature in vpython. If you are in a very expansive view that includes far objects such as dwarf planets and also closer to the sun objects like inner planets, unchecking the far objects and refreshing the scene may "autoscale" you back inside the sun (even though everything looks black). To eliminate the problem, simply perform a zoom out.

One Last thing: Planets do not rotate on their axis during animation. Since the time increment is always a multiple of 1 earth day, 
the earth does not rotate on its axis, so to keep things as simple as possible, there is no planet spin.

