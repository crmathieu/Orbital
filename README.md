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

The Orbital control modal window will take a little less than a minute to load as PHA, Asteroids, Comets and 
trans-Neptunian objects orbits get calculated and rendered during this initial phase, but inner planets are 
displayed right away and can be interacted with. If the loading time is too long for your taste, you may limit
the number of objects being loaded by updating the constant MAX_OBJECTS in solarsys.py. The constant specifies
the upper limit of objects to load per data file.

Once the Orbital Control modal pops up, you may visualize the other major bodies in the solar system: Gas giants, 
dwarf planets or Asteroid / Kuiper belts etc... All orbits of PHAs, Big Asteroids, Comets and Trans-Neptunian can 
be displayed by using the SlideShow feature. You may pause at any time to take a closer look at trajectories by 
zooming in/out and rotate, and then resume. You may also animate the current object from the slideshow along
with other visible objects by using the ">" button. You may also do it step by step using the "+" button. 

Animations can be played at speeds varying between -x20 to +x20, allowing to go back in time as well as in the future.
Specific dates can also be entered directly to examin orbits relative positions. That is an important feature to verify
passed events, such as close encounters between earth and PHAs (ie The asteroid named Toutatis on December 12, 2012).

The current object orbital elements are displayed at the bottom of the Orbital Control window. 
Legend is:

	i: Orbital Inclinaison
	N: Longitude of Ascending node
	w: Argument of Perihelion
	e: Orbit Eccentricity
	q: Perihelion distance to the sun

	M: Mass in kg
	R: Average radius in Km
	P: Orbital Period in years

	Moid: Minimum Orbital Intersection Distance (in this case with Earth)
	Velocity: The current velocity on orbit (this will be updated during animation)

Note: There is a bug in the autoscale feature in vpython. If you are in a very expansive view that includes far objects such as dwarf planets and also closer to the sun objects like inner planets, unchecking the far objects and refreshing the scene may "autoscale" you back inside the sun (even though everything looks black). To eliminate the problem, simply perform a zoom out.


