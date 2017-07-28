"""
	Copyright (c) 2017 Charles Mathieu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
from scipy.sparse.csgraph import _validation  
from controls import *

def main():
	solarsystem = solarSystem()
	# set what is displayed by default
	solarsystem.ShowFeatures = INNERPLANET|ORBITS|LABELS|OUTTERPLANET

	solarsystem.addTo(makeEcliptic(solarsystem, color.white))
	solarsystem.addTo(planet(solarsystem, 'mercury', color.green, 70, INNERPLANET, INNERPLANET))
	solarsystem.addTo(planet(solarsystem, 'venus', color.yellow, 0, INNERPLANET, INNERPLANET))
	earth = planet(solarsystem, 'earth', color.cyan, 225, INNERPLANET, INNERPLANET)
	solarsystem.addTo(earth)
	solarsystem.addTo(planet(solarsystem, 'mars', color.red, 0, INNERPLANET, INNERPLANET))
	solarsystem.addTo(planet(solarsystem, 'jupiter', color.magenta, 0, OUTTERPLANET, GASGIANT))
	solarsystem.addTo(planet(solarsystem, 'saturn', color.cyan, 20, OUTTERPLANET, GASGIANT))
	solarsystem.addTo(planet(solarsystem, 'uranus', color.yellow, 0, OUTTERPLANET, GASGIANT))
	solarsystem.addTo(planet(solarsystem, 'neptune', color.orange, 0, OUTTERPLANET, GASGIANT))
	solarsystem.addTo(planet(solarsystem, 'pluto', color.green, 0, OUTTERPLANET, DWARFPLANET))

	solarsystem.makeRings(solarsystem, "saturn")

	# generate DWARF planets
	solarsystem.addTo(dwarfPlanet(solarsystem, 'eris', color.yellow, 0))
	solarsystem.addTo(dwarfPlanet(solarsystem, 'makemake', color.magenta, 0))
	solarsystem.addTo(dwarfPlanet(solarsystem, 'sedna', color.orange, 0))
	solarsystem.addTo(dwarfPlanet(solarsystem, 'haumea', color.white, 0))

	# generate Belts
	solarsystem.addTo(makeBelt(solarsystem, 'kuiper', 'Kuiper Belt', KUIPER_BELT, color.cyan, 2, 4))
	solarsystem.addTo(makeBelt(solarsystem, 'asteroid', 'Asteroid Belt', ASTEROID_BELT, color.white, 2, 2))
	solarsystem.addTo(makeBelt(solarsystem, 'inneroort', 'Inner Oort Cloud', INNER_OORT_CLOUD, color.white, 2, 5))

	solarsystem.addJTrojans(makeJtrojan(solarsystem, 'jupiterTrojan', 'Jupiter Trojans', JTROJANS, color.green, 2, 5, 'jupiter'))

	MAX_OBJECTS = 1000

	loadBodies(solarsystem, PHA, "200m+PHA_orbital_elements.txt", MAX_OBJECTS)
	loadBodies(solarsystem, BIG_ASTEROID,"200km+asteroids_orbital_elements.txt", MAX_OBJECTS)
	loadBodies(solarsystem, COMET, "200m+comets_orbital_elements.txt", MAX_OBJECTS)
	loadBodies(solarsystem, TRANS_NEPT, "transNeptunian_objects.txt", MAX_OBJECTS)
	solarsystem.drawAllBodiesTrajectory()

	# Start control window
	#print wx.version()
	ex = wx.App()
	cw = controlWindow(None, solarsystem)

	while True:
		rate(2)

if __name__ == '__main__' :
	main()
