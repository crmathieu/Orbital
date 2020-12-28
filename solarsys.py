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
#from scipy.sparse.csgraph import _validation
from controls import *

def main():
	# determine where this program runs 
	#locationInfo = location()

	solarsystem = solarSystem()
	# set what is displayed by default
	solarsystem.setDefaultFeatures(INNERPLANET|ORBITS|SATELLITE|LABELS|OUTERPLANET|LIT_SCENE|CELESTIAL_SPHERE)

	solarsystem.addTo(makeEcliptic(solarsystem, color.white))
	solarsystem.addTo(planet(solarsystem, 'mercury', color.green, INNERPLANET, INNERPLANET, PLANET_SZ_CORRECTION))
	solarsystem.addTo(planet(solarsystem, 'venus', color.yellow, INNERPLANET, INNERPLANET, PLANET_SZ_CORRECTION))
	#earth = planet(solarsystem, 'earth', color.cyan, INNERPLANET, INNERPLANET, PLANET_SZ_CORRECTION)
	earth = makeEarth(solarsystem, color.cyan, INNERPLANET, INNERPLANET, PLANET_SZ_CORRECTION)

	solarsystem.addTo(earth)
	mars = planet(solarsystem, 'mars', color.red, INNERPLANET, INNERPLANET, PLANET_SZ_CORRECTION)
	solarsystem.addTo(mars)
	solarsystem.addTo(planet(solarsystem, 'jupiter', color.magenta, OUTERPLANET, GASGIANT, PLANET_SZ_CORRECTION))
	solarsystem.addTo(planet(solarsystem, 'saturn', color.cyan, OUTERPLANET, GASGIANT, PLANET_SZ_CORRECTION))
	solarsystem.addTo(planet(solarsystem, 'uranus', color.yellow, OUTERPLANET, GASGIANT, PLANET_SZ_CORRECTION))
	solarsystem.addTo(planet(solarsystem, 'neptune', color.orange, OUTERPLANET, GASGIANT, PLANET_SZ_CORRECTION))
	pluto = planet(solarsystem, 'pluto', color.green, DWARFPLANET, DWARFPLANET, DWARFPLANET_SZ_CORRECTION) #OUTERPLANET, DWARFPLANET)
	solarsystem.addTo(pluto)

	solarsystem.setRings(solarsystem, "saturn", [((0.8,0.8,0.8), 0.9), ((0.5,0.5,0.5), 0.2)]) #[color.gray(0.7), (0.5,0.5,0.5)])
	solarsystem.setRings(solarsystem, "uranus", [((0.1,0.1,0.8), 0.1), ((0.2,0.2,0.7), 0.3)])

	# generate DWARF planets
	solarsystem.addTo(dwarfPlanet(solarsystem, 'eris', color.yellow))
	solarsystem.addTo(dwarfPlanet(solarsystem, 'makemake', color.magenta))
	solarsystem.addTo(dwarfPlanet(solarsystem, 'sedna', color.orange))
	solarsystem.addTo(dwarfPlanet(solarsystem, 'haumea', color.white))

	# generate satellites
	solarsystem.addTo(satellite(solarsystem, 'moon', color.white, earth))
	solarsystem.addTo(satellite(solarsystem, 'phobos', color.red, mars))
	solarsystem.addTo(satellite(solarsystem, 'deimos', color.white, mars))
	solarsystem.addTo(satellite(solarsystem, 'charon', color.white, pluto))

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
	#loadBodies(solarsystem, SATELLITE, "satellites.txt", MAX_OBJECTS)

	solarsystem.drawAllBodiesTrajectory()
	glbRefresh(solarsystem, False)

	# Start control window
	print wx.version()
	#print julian(1, 1, 2000)

	ex = wx.App(False)
	cw = controlWindow(solarsystem)
	cw.Show()


	while True:
		sleep(2)
		earth.updateStillPosition(2)


if __name__ == '__main__' :
	main()
