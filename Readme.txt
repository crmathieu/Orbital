This is version 1.0. This version simply displays the accurate 3D orbit of major objects in the solar system. Each object, 
except for Earth, Mercury and Saturn, is located at its perihelion (closest distance to the sun) which does not correspond 
to their actual orbit location when your start the simulation. 

PHA (Potentially Hazardous Asteroids), comets and Big Asteroids data was collected from the JPL Small-Body Database 
Search Engine

Keep in mind that:

	- All distances between each object and the sun are proportional to the actual distance
	- The size of objects is NOT proportional to their actual size (this is by design in order to view all objects properly)
	- Asteroid belt, Kuiper belt and Oort Cloud are there for illustration purpose only. Even though their size and thickness
	is proportional to their actual size and thickness, the distribution pattern within the belt is purely random/cosmetic.
	- This code is far from being finished. Some portions of the script are still under development and are not being used
	at this time.

Platform:
	python 2.7.9
	vpython 6
	wxpython 3.0

you will also need the following libraries
	numpy
	scipy

The orbital control modal window will take about 30sec to appear as lots of space objects information need to load first.

You may visualize all PHAs, Big Asteroids and Comets by checking the corresponding checkbox -but- since there are so many 
of them, you also may want to see them one by one using the Animate feature. You may pause at any time to take a closer look 
at trajectories by zooming in/out and rotate, and then resume.

You can also examin the objects details displayed at the bottom of the Orbital Control window. 
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
dwarf planets and you want to refresh after only keeping the inner rocky planets, the autoscale will sometime send you inside 
the sun (even though everything looks black). To get out, simply zoom out of it.

