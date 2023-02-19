""" main module  """

from re import I
from rate_func import *	
from orbit3D import *
from planets import *
import planetsdata as pd
from controls import *
from celestial.orbitalLIB import Api
from eqsols_calculator import Vernal, Vernal2
#from utils import sleep

def createSolarSystem():
		
	ssys = makeSolarSystem()
	
	# set what is displayed by default
	ssys.setDefaultFeatures(pd.INNERPLANET|pd.ORBITS|pd.SATELLITE|pd.OUTERPLANET|pd.SUN) 

	sun = makeSun(ssys, color.yellow, pd.SUN, pd.SUN, pd.SUN_SZ_CORRECTION)
	ssys.register(sun)

	print pd.Frame_Intervals

	#glbRefresh(ssys, False)

	#raw_input("type something ...")

	#ssys.addTo(sun)
	
	# make first the bodies we have satellites defined for
	earth = makeEarth(ssys, color.cyan, pd.INNERPLANET, pd.INNERPLANET, pd.PLANET_SZ_CORRECTION)
	ssys.addTo(earth)

	mars = makeMars(ssys, color.red, pd.INNERPLANET, pd.INNERPLANET, pd.PLANET_SZ_CORRECTION)
	ssys.addTo(mars)

	pluto = makePlanet(ssys, 'pluto', color.green, pd.DWARFPLANET, pd.DWARFPLANET, pd.DWARFPLANET_SZ_CORRECTION) #pd.OUTERPLANET, DWARFPLANET)
	ssys.addTo(pluto)

	# generate pd.SATELLITE
	#ssys.addTo(makeSatellite(ssys, 'charon', color.white, pluto))
	#ssys.addTo(makeSatellite(ssys, 'moon', color.white, earth))
	#ssys.addTo(makeSatellite(ssys, 'phobos', color.red, mars))
	#ssys.addTo(makeSatellite(ssys, 'deimos', color.white, mars))

	ssys.addTo(makeEcliptic(ssys, color.magenta, 0.4))

	ssys.addTo(makeMercury(ssys, color.green, pd.INNERPLANET, pd.INNERPLANET, pd.PLANET_SZ_CORRECTION))
	ssys.addTo(makePlanet(ssys, 'venus', color.yellow, pd.INNERPLANET, pd.INNERPLANET, pd.PLANET_SZ_CORRECTION))
	ssys.addTo(makePlanet(ssys, 'jupiter', color.magenta, pd.OUTERPLANET, pd.GASGIANT, pd.PLANET_SZ_CORRECTION))
	ssys.addTo(makePlanet(ssys, 'uranus', color.yellow, pd.OUTERPLANET, pd.GASGIANT, pd.PLANET_SZ_CORRECTION))
	ssys.addTo(makeNeptune(ssys, color.orange, pd.OUTERPLANET, pd.GASGIANT, pd.PLANET_SZ_CORRECTION))
	ssys.addTo(makePlanet(ssys, 'saturn', color.cyan, pd.OUTERPLANET, pd.GASGIANT, pd.PLANET_SZ_CORRECTION))
	
	# generate DWARF planets
	ssys.addTo(makeDwarfPlanet(ssys, 'eris', color.yellow))
	ssys.addTo(makeDwarfPlanet(ssys, 'makemake', color.magenta))
	ssys.addTo(makeDwarfPlanet(ssys, 'sedna', color.orange))
	ssys.addTo(makeDwarfPlanet(ssys, 'haumea', color.white))

	# generate Belts
	ssys.addTo(makeBelt(ssys, 'kuiper', 'Kuiper Belt', pd.KUIPER_BELT, color.cyan, 2, 4))
	ssys.addTo(makeBelt(ssys, 'asteroid', 'Asteroid Belt', pd.ASTEROID_BELT, color.white, 2, 2))
	ssys.addTo(makeBelt(ssys, 'inneroort', 'Inner Oort Cloud', pd.INNER_OORT_CLOUD, color.white, 2, 5))

	ssys.addJTrojans(makeJtrojan(ssys, 'jupiterTrojan', 'Jupiter Trojans', pd.JTROJANS, color.green, 2, 5, 'jupiter'))
	

	
	MAX_OBJECTS = 1000
	loadBodies(ssys, PHA, "data/test.json", MAX_OBJECTS)

	if False:
		print "LOADING bodies orbital elements and trajectories ..."
		loadBodies(ssys, PHA, "data/200m+PHA_orbital_elements.txt.json", MAX_OBJECTS)
		loadBodies(ssys, BIG_ASTEROID,"data/200km+asteroids_orbital_elements.txt.json", MAX_OBJECTS)
		loadBodies(ssys, COMET, "data/200m+comets_orbital_elements.txt.json", MAX_OBJECTS)
		loadBodies(ssys, TRANS_NEPT, "data/transNeptunian_objects.txt.json", MAX_OBJECTS)
		loadBodies(ssys, SPACECRAFT, "data/spacecrafts_orbital_elements.txt.json", MAX_OBJECTS)
		print "FINISHED ..."

	ssys.drawAllBodiesTrajectory()
	glbRefresh(ssys, False)
	return ssys


def bootLoader(story, recorder): 

	# Start control window
	print (wx.version())

	# start wxPython application
	try:
		ex = wx.App(False)
		ssys = createSolarSystem()
		ssys.setEarthLocations(makeDashBoard(ssys))
		#ssys.getDashboard().showInfoWindow(True)

		# play story when provided
		api = Api(ssys, recorder = recorder)
		if story != None:
			try:
				# instantiate story and play it
				st = story(ssys, api)
				del st
			except RuntimeError as err:
				print ("Exception...\n\nError: " + str(err.code))
				raise
		else:
			ssys.setAutoScale(False)
			api.camera.setCameraTarget(EARTH_NAME)
			ssys.displaySolarSystem()
			ssys.introZoomIn(75)
			#ssys.rotateSolarSystemReferential(axis=vector(0,1,0))
			#ssys.Scene.fov = pi

		# we only show the dashboard after the story has finished.
		ssys.getDashboard().Show()
		ssys.setAutoScale(False)
		#ssys.getDashboard().showInfoWindow(False)

		print "Calculate equinox/solstyce"
		Vernal(2023) ### a test ...
		Vernal2(2023)

		I = 0
		while True:
			#print I
			#I += 1
			#rate(1)
			sleep(2)
		#	earth.updateStillPosition(cw.orbitalBox, 2)

	except RuntimeError as err:
		print ("Exception...\n\nError: " + str(err)) #.code))
		raise

	