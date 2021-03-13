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
#from celestial import orbit3D, planetsdata as pd
from celestial.orbit3D import *
import celestial.planetsdata as pd
from celestial.controls import *

#from controls import *

def main():
	# determine where this program runs 
	#locationInfo = location()
	
	solarsystem = solarSystem()
	# set what is displayed by default
	bodySet = pd.INNERPLANET|pd.OUTERPLANET|pd.ORBITS|pd.SATELLITE|pd.KUIPER_BELT|pd.ASTEROID_BELT|pd.JTROJANS|pd.LABELS
	solarsystem.setDefaultFeatures(bodySet) #pd.INNERPLANET|pd.OUTERPLANET|pd.ORBITS|pd.SATELLITE|pd.KUIPER_BELT|pd.ASTEROID_BELT|pd.JTROJANS|pd.LABELS|pd.CELESTIAL_SPHERE)
#	solarsystem.setDefaultFeatures(pd.INNERPLANET|pd.OUTERPLANET|pd.ORBITS|pd.SATELLITE|pd.KUIPER_BELT|pd.ASTEROID_BELT|pd.JTROJANS|pd.LABELS|pd.CELESTIAL_SPHERE)
#	solarsystem.setDefaultFeatures(pd.INNERPLANET|pd.OUTERPLANET|pd.ORBITS)

	solarsystem.addTo(makeEcliptic(solarsystem, color.white))
	solarsystem.addTo(planet(solarsystem, 'mercury', color.green, pd.INNERPLANET, pd.INNERPLANET, pd.PLANET_SZ_CORRECTION))
	solarsystem.addTo(planet(solarsystem, 'venus', color.yellow, pd.INNERPLANET, pd.INNERPLANET, pd.PLANET_SZ_CORRECTION))

	earth = makeEarth(solarsystem, color.cyan, pd.INNERPLANET, pd.INNERPLANET, pd.PLANET_SZ_CORRECTION)
	solarsystem.addTo(earth)

	mars = planet(solarsystem, 'mars', color.red, pd.INNERPLANET, pd.INNERPLANET, pd.PLANET_SZ_CORRECTION)
	solarsystem.addTo(mars)
	
	solarsystem.addTo(planet(solarsystem, 'jupiter', color.magenta, pd.OUTERPLANET, GASGIANT, pd.PLANET_SZ_CORRECTION))
	solarsystem.addTo(planet(solarsystem, 'saturn', color.cyan, pd.OUTERPLANET, GASGIANT, pd.PLANET_SZ_CORRECTION))
	solarsystem.addTo(planet(solarsystem, 'uranus', color.yellow, pd.OUTERPLANET, GASGIANT, pd.PLANET_SZ_CORRECTION))
	solarsystem.addTo(planet(solarsystem, 'neptune', color.orange, pd.OUTERPLANET, GASGIANT, pd.PLANET_SZ_CORRECTION))

	pluto = planet(solarsystem, 'pluto', color.green, DWARFPLANET, DWARFPLANET, pd.DWARFPLANET_SZ_CORRECTION) #pd.OUTERPLANET, DWARFPLANET)
	solarsystem.addTo(pluto)

#	solarsystem.setRings(solarsystem, "saturn") #, [((0.8,0.8,0.8), 0.9), ((0.5,0.5,0.5), 0.2)]) 
#	solarsystem.setRings(solarsystem, "uranus") #, [((0.1,0.1,0.8), 0.1), ((0.2,0.2,0.7), 0.3)])

	# generate DWARF planets
	solarsystem.addTo(dwarfPlanet(solarsystem, 'eris', color.yellow))
	solarsystem.addTo(dwarfPlanet(solarsystem, 'makemake', color.magenta))
	solarsystem.addTo(dwarfPlanet(solarsystem, 'sedna', color.orange))
	solarsystem.addTo(dwarfPlanet(solarsystem, 'haumea', color.white))

	# generate pd.SATELLITEs
	solarsystem.addTo(satellite(solarsystem, 'moon', color.white, earth))
	solarsystem.addTo(satellite(solarsystem, 'phobos', color.red, mars))
	solarsystem.addTo(satellite(solarsystem, 'deimos', color.white, mars))
	solarsystem.addTo(satellite(solarsystem, 'charon', color.white, pluto))

	# generate Belts
	solarsystem.addTo(makeBelt(solarsystem, 'kuiper', 'Kuiper Belt', pd.KUIPER_BELT, color.cyan, 2, 4))
	solarsystem.addTo(makeBelt(solarsystem, 'asteroid', 'Asteroid Belt', pd.ASTEROID_BELT, color.white, 2, 2))
	solarsystem.addTo(makeBelt(solarsystem, 'inneroort', 'Inner Oort Cloud', pd.INNER_OORT_CLOUD, color.white, 2, 5))

	solarsystem.addJTrojans(makeJtrojan(solarsystem, 'jupiterTrojan', 'Jupiter Trojans', pd.JTROJANS, color.green, 2, 5, 'jupiter'))

	MAX_OBJECTS = 1000

	"""
	loadBodies(solarsystem, PHA, "data/200m+PHA_orbital_elements.txt.json", MAX_OBJECTS)
	loadBodies(solarsystem, BIG_ASTEROID,"data/200km+asteroids_orbital_elements.txt.json", MAX_OBJECTS)
	loadBodies(solarsystem, COMET, "data/200m+comets_orbital_elements.txt.json", MAX_OBJECTS)
	loadBodies(solarsystem, TRANS_NEPT, "data/transNeptunian_objects.txt.json", MAX_OBJECTS)
	loadBodies(solarsystem, SPACECRAFT, "data/spacecrafts_orbital_elements.txt.json", MAX_OBJECTS)
	"""

	#loadBodies(solarsystem, pd.SATELLITE, "pd.SATELLITEs.txt", MAX_OBJECTS)

	solarsystem.drawAllBodiesTrajectory()
	#solarsystem.updateCameraPOV(earth)
	#print solarsystem.currentPOV.Name
	
	glbRefresh(solarsystem, False)

	# Start control window
	print wx.version()
	#print julian(1, 1, 2000)


	#flyingC = flyingCamera(solarsystem)
	#flyingC.MT.OnFakeLeftMouseDown()

	ex = wx.App(False)
	cw = controlWindow(solarsystem)
	cw.povBox.setCurrentBodyFocusManually(earth, 2)
	cw.Show()


	while True:
		sleep(2)
		earth.updateStillPosition(2)


if __name__ == '__main__' :
	main()
