""" main module  """

from rate_func import *	
from orbit3D import *
import planetsdata as pd
from controls import *
from celestial.orbitalLIB import Api

def bootLoader(story, recorder): 
	
	solSystem = makeSolarSystem()

	# set what is displayed by default
	bodySet = pd.INNERPLANET|pd.ORBITS|pd.SATELLITE|pd.LABELS|pd.OUTERPLANET
	solSystem.setDefaultFeatures(bodySet) 

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

	print "LOADING bodies orbital elements and trajectories ..."
	loadBodies(solSystem, PHA, "data/200m+PHA_orbital_elements.txt.json", MAX_OBJECTS)
	loadBodies(solSystem, BIG_ASTEROID,"data/200km+asteroids_orbital_elements.txt.json", MAX_OBJECTS)
	loadBodies(solSystem, COMET, "data/200m+comets_orbital_elements.txt.json", MAX_OBJECTS)
	loadBodies(solSystem, TRANS_NEPT, "data/transNeptunian_objects.txt.json", MAX_OBJECTS)
	loadBodies(solSystem, SPACECRAFT, "data/spacecrafts_orbital_elements.txt.json", MAX_OBJECTS)
	print "FINISHED ..."
	
	solSystem.drawAllBodiesTrajectory()
	glbRefresh(solSystem, False)

	# Start control window
	print (wx.version())


	# start wxPython application
	ex = wx.App(False)
	solSystem.setEarthLocations(makeDashBoard(solSystem))

	# play story when provided
	api = Api(solSystem, recorder = recorder)
	if story != None:
		try:
			# instantiate story and play it
			st = story(solSystem, api)
			del st
		except RuntimeError as err:
			print ("Exception...\n\nError: " + str(err.code))
			raise
	else:
		solSystem.setAutoScale(False)
		api.camera.setCameraTarget(EARTH_NAME)
		solSystem.displaySolarSystem()
		solSystem.introZoomIn(75)

	# we only show the dashboard after the story has finished.
	solSystem.getDashboard().Show()
	solSystem.setAutoScale(False)

	while True:
		sleep(2)
	#	earth.updateStillPosition(cw.orbitalBox, 2)

