# simulate the solar system
# Author: Ryan Brigden
# 33-151: M&I I

# planet and orbital data from: 
# http://nssdc.gsfc.nasa.gov/planetary/factsheet/planet_table_ratio.html
# http://education.nationalgeographic.com/activity/planetary-size-and-distance-comparison/
# http://www.sjsu.edu/faculty/watkins/orbital.htm

from visual import *

planets = []

# mass, orbital velocity & radius of the earth
# initial momentum of earth = me * vE
# distance of the earth from the sun is dE
mE = 5.97e24
vE = 30e3
rE = 2
dE = 149.6e9



# create the solar system
sun = sphere(pos=(0,0,0), radius=696e6, color=color.yellow, mass=333000 * mE)
mercury = sphere(pos=(0,0,0.387 * dE), radius=696e6, color=color.blue, mass=0.0553 * mE)
venus = sphere(pos=(0,0,0.723 * dE), radius=696e6, color=color.cyan, mass=0.815 * mE)
earth = sphere(pos=(0,0,dE), radius=696e6, color=color.green, mass=mE)
mars = sphere(pos=(0,0,1.52 * dE), radius=696e6, color=color.red, mass=0.107 * mE)
jupiter = sphere(pos=(0,0,5.20 * dE), radius=696e6, color=color.yellow, mass=317.8 * mE)
saturn = sphere(pos=(0,0,9.58 * dE), radius=696e6, color=color.white, mass=95.2 * mE)
uranus = sphere(pos=(0,0,19.20 * dE), radius=696e6, color=color.orange, mass=14.5 * mE)
neptune = sphere(pos=(0,0,30.05 * dE), radius=696e6, color=color.magenta, mass=17.1 * mE)

# add initial velocities
sun.velocity = vector(0, 0, 0)
mercury.velocity = vector(1.607 * vE, 0, 0)
venus.velocity = vector(1.174 * vE, 0, 0)
earth.velocity = vector(vE, 0, 0)
mars.velocity = vector(0.802 * vE, 0, 0)
jupiter.velocity = vector(0.434 * vE, 0, 0)
saturn.velocity = vector(0.323 * vE, 0, 0)
uranus.velocity = vector(0.228 * vE, 0, 0)
neptune.velocity = vector(0.182 * vE, 0, 0)

planets.extend((sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune))

# add trails
for planet in planets:
	planet.trail = curve(color=planet.color)

# add arrows
vscale = 10000
varrows = []
for planet in planets:
	varrows.append(arrow(pos=planet.pos, axis=planet.velocity * vscale, color=color.red, planet=planet)) 

dt = 100
t = 0

GRAVC = 6.67e-11


def gravAcc(obj, other):
	""" acceleration of an object due to gravitational force """
	rVector = obj.pos - other.pos
	acc = -((GRAVC * other.mass) / rVector.mag2 )
	acc *= rVector.norm()
	return acc

 # def tell_time(seconds):
 # 	years = int(seconds / 3.15569e7)
 # 	months = int((seconds % 3.15569e7) / 2.62974e6)
 # 	days = int(((seconds % 3.15569e7) % 2.62974e6) / 86400 )
 # 	print "Years: ", years, "Months: ", months, "Days: ", days


while t < 3.15569e7:
	rate(1e50)
	print t	
	for planet1 in planets:
		for planet2 in planets:
			if planet1 != planet2:
				planet1.velocity += gravAcc(planet1, planet2) * dt

	# update the position of the objects
	for planet in planets:
		planet.pos += planet.velocity * dt

	# update the trail and arrows following the objects
	for planet in planets:
		planet.trail.append(pos=planet.pos)

	for varrow in varrows:
		varrow.pos = varrow.planet.pos
		varrow.axis = varrow.planet.velocity * vscale	

	t += dt



# 3.15569e7 in a year


