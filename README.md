# Orbital
An accurate interactive 3D representation of the solar system featuring inner and outter planets, asteroids and 
comets. Also includes the asteroid belt, Kuiper belt and inner Oort cloud.

3D orbit of major objects in the solar system are rendered and can be zoomed in and out as well as rotated. Each 
object, is located at its actual orbit position at the time of rendering. 

Interacting with the simulation:

To zoom in/out: click on both mouse buttons and drag the mouse forward or backward.
To rotate the scene: click on the mouse left button only and drag the mouse sideways.

PHA (Potentially Hazardous Asteroids), comets and Big Asteroids data was collected from the JPL Small-Body Database 
Search Engine.

Keep in mind that

	- All distances between each object and the sun are proportional to the actual distance.
	- Objects sizes are NOT proportional to their actual size (this is by design in order to 
	  view all objects properly).
	- Asteroid belt, Kuiper belt and Oort Cloud are included for illustration purpose only. Even though their 
	  size and thickness is proportional to their actual size and thickness, the distribution pattern within 
	  the belt is purely random/aesthetic.
	- This code is a work in progress, so you may see some under development portions of the script that are 
	  unused at this moment.

Platform:

	python 2.7.9
	vpython 6
	wxpython 3.0

you will also need the following libraries:

	numpy
	scipy

The Orbital control modal window will take about 30sec to load as PHA, Asteroids and Comets orbits get calculated 
and rendered during this initial phase, but inner planets are rendered right away and can be interacted with.

Once the Orbital Control modal pops up, you may visualize the other major bodies in the solar system: Gas giants, 
dwarf planets or Asteroid and Kuiper belts. All PHAs, Big Asteroids and Comets orbits can be rendered by using the 
Animate feature. You may pause at any time to take a closer look at trajectories by zooming in/out and rotate, and 
then resume.

You can also examine the current object details displayed at the bottom of the Orbital Control window. 
Legend is:

	i: Orbital Inclinaison
	N: Longitude of Ascending node
	w: Augument of Perihelion
	e: Orbit Eccentricity
	q: Perihelion distance to the sun

	M: mass in kg
	R: Average radius in Km
	P: Orbital Period in years

	Moid: Minimum Orbital Intersection Distance (in this case with Earth)

Note: there is a bug in the autoscale feature in vpython. If you are in a very comprehensive view that includes far objects like
dwarf planets and also closer to the sun objects like inner planets, unchecking the far objects and refresh the scene may "autoscale" you back inside the sun (even though everything looks black). To get out, simply zoom out of it.


