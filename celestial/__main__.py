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
""" main module  """

from rate_func import *	

from orbit3D import *
import planetsdata as pd
from controls import *

#from controls import *

def bootSolarSystem():
	# determine where this program runs 
	#locationInfo = location()
	

	solSystem = makeSolarSystem()

	# set what is displayed by default
	bodySet = pd.INNERPLANET|pd.ORBITS|pd.SATELLITE|pd.LABELS|pd.OUTERPLANET
	solSystem.setDefaultFeatures(bodySet) #pd.INNERPLANET|pd.OUTERPLANET|pd.ORBITS|pd.SATELLITE|pd.KUIPER_BELT|pd.ASTEROID_BELT|pd.JTROJANS|pd.LABELS|pd.CELESTIAL_SPHERE)
#	solSystem.setDefaultFeatures(pd.INNERPLANET|pd.OUTERPLANET|pd.ORBITS|pd.SATELLITE|pd.KUIPER_BELT|pd.ASTEROID_BELT|pd.JTROJANS|pd.LABELS|pd.CELESTIAL_SPHERE)
#	solSystem.setDefaultFeatures(pd.INNERPLANET|pd.OUTERPLANET|pd.ORBITS)

	# make bodyies we have satellites for
	earth = makeEarth(solSystem, color.cyan, pd.INNERPLANET, pd.INNERPLANET, pd.PLANET_SZ_CORRECTION)
	solSystem.addTo(earth)

	pluto = planet(solSystem, 'pluto', color.green, pd.DWARFPLANET, pd.DWARFPLANET, pd.DWARFPLANET_SZ_CORRECTION) #pd.OUTERPLANET, DWARFPLANET)
	solSystem.addTo(pluto)

	mars = planet(solSystem, 'mars', color.red, pd.INNERPLANET, pd.INNERPLANET, pd.PLANET_SZ_CORRECTION)
	solSystem.addTo(mars)

	
	# generate pd.SATELLITE
	#solSystem.addTo(satellite(solSystem, 'charon', color.white, pluto))
	#solSystem.addTo(satellite(solSystem, 'moon', color.white, earth))
	solSystem.addTo(satellite(solSystem, 'phobos', color.red, mars))
	solSystem.addTo(satellite(solSystem, 'deimos', color.white, mars))

	solSystem.addTo(makeEcliptic(solSystem, color.cyan, 0.4))

	solSystem.addTo(planet(solSystem, 'mercury', color.green, pd.INNERPLANET, pd.INNERPLANET, pd.PLANET_SZ_CORRECTION))
	solSystem.addTo(planet(solSystem, 'venus', color.yellow, pd.INNERPLANET, pd.INNERPLANET, pd.PLANET_SZ_CORRECTION))
	solSystem.addTo(planet(solSystem, 'jupiter', color.magenta, pd.OUTERPLANET, pd.GASGIANT, pd.PLANET_SZ_CORRECTION))
	solSystem.addTo(planet(solSystem, 'saturn', color.cyan, pd.OUTERPLANET, pd.GASGIANT, pd.PLANET_SZ_CORRECTION))
	solSystem.addTo(planet(solSystem, 'uranus', color.yellow, pd.OUTERPLANET, pd.GASGIANT, pd.PLANET_SZ_CORRECTION))
	solSystem.addTo(planet(solSystem, 'neptune', color.orange, pd.OUTERPLANET, pd.GASGIANT, pd.PLANET_SZ_CORRECTION))

	
#	solSystem.setRings(solSystem, "saturn") #, [((0.8,0.8,0.8), 0.9), ((0.5,0.5,0.5), 0.2)]) 
#	solSystem.setRings(solSystem, "uranus") #, [((0.1,0.1,0.8), 0.1), ((0.2,0.2,0.7), 0.3)])

	# generate DWARF planets
	solSystem.addTo(dwarfPlanet(solSystem, 'eris', color.yellow))
	solSystem.addTo(dwarfPlanet(solSystem, 'makemake', color.magenta))
	solSystem.addTo(dwarfPlanet(solSystem, 'sedna', color.orange))
	solSystem.addTo(dwarfPlanet(solSystem, 'haumea', color.white))


	# generate Belts
	solSystem.addTo(makeBelt(solSystem, 'kuiper', 'Kuiper Belt', pd.KUIPER_BELT, color.cyan, 2, 4))
	solSystem.addTo(makeBelt(solSystem, 'asteroid', 'Asteroid Belt', pd.ASTEROID_BELT, color.white, 2, 2))
	solSystem.addTo(makeBelt(solSystem, 'inneroort', 'Inner Oort Cloud', pd.INNER_OORT_CLOUD, color.white, 2, 5))

	solSystem.addJTrojans(makeJtrojan(solSystem, 'jupiterTrojan', 'Jupiter Trojans', pd.JTROJANS, color.green, 2, 5, 'jupiter'))

	MAX_OBJECTS = 1000

	# !!!!!!!!!!!!!!!!!!!!!!!!!! test
#	solSystem.drawAllBodiesTrajectory()
	print "LOADING bodies orbital elements and trajectories ..."
	loadBodies(solSystem, PHA, "data/200m+PHA_orbital_elements.txt.json", MAX_OBJECTS)
	loadBodies(solSystem, BIG_ASTEROID,"data/200km+asteroids_orbital_elements.txt.json", MAX_OBJECTS)
	loadBodies(solSystem, COMET, "data/200m+comets_orbital_elements.txt.json", MAX_OBJECTS)
	loadBodies(solSystem, TRANS_NEPT, "data/transNeptunian_objects.txt.json", MAX_OBJECTS)
	loadBodies(solSystem, SPACECRAFT, "data/spacecrafts_orbital_elements.txt.json", MAX_OBJECTS)
	print "FINISHED ..."


	
	solSystem.drawAllBodiesTrajectory()
	
	#solSystem.makeCelestialSphere()

	glbRefresh(solSystem, False)

	# Start control window
	print (wx.version())
	#print julian(1, 1, 2000)


	# start wxPython application
	ex = wx.App(False)
	db = DashBoard(solSystem)
	db.focusTab.setCurrentBodyFocusManually(earth, 2)
	db.Show()

	solSystem.introZoomIn(38)

	#ex.MainLoop()

	#solSystem.camera.cameraZoom(10)

	while True:
		sleep(2)
	#	earth.updateStillPosition(cw.orbitalBox, 2)


def main():
	bootSolarSystem()

#if __name__ == '__main__' :
#	bootSolarSystem()
