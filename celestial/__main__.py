""" main module  """

from re import I
from rate_func import *	
from orbit3D import *
from planets import *
#import planetsdata as pd
from planetsdata import *
from controls import *
from celestial.orbitalLIB import Api
from eqsols_calculator import Vernal, Vernal2
from moons import makePlanetMoon, makeLuna
from objects_loader import load_objects_catalog
from moons_loader import load_moon_catalog

#from utils import sleep

def createSolarSystem():
		
	# LOAD CATALOGS
	moons_catalog = load_moon_catalog()
	objects_data.update(moons_catalog)
	
	objects_catalog = load_objects_catalog()
	objects_data.update(objects_catalog)

	# CREATE SOLAR SYSTEM REFERENTIAL
	ssys = makeSolarSystem()
	
	# set what is displayed by default
	ssys.setDefaultFeatures(INNER_PLANET|ORBITS|SPACECRAFT|MOON|OUTER_PLANET|SUN) 

	sun = makeSun(ssys, color=color.yellow, ptype=SUN, sizeCorrectionType=SUN, defaultSizeCorrection=SUN_SZ_CORRECTION)
	ssys.register(sun)

	print Frame_Intervals

	#glbRefresh(ssys, False)

	#raw_input("type something ...")

	#ssys.addTo(sun)
	
	# make first the bodies we have Moon(s) defined for

	# generate planets and moons ...
	print "GENERATING PLANETS and MOONS ....."

	ssys.addTo(makeMercury(ssys, color=color.green, ptype=INNER_PLANET, sizeCorrectionType=INNER_PLANET, defaultSizeCorrection=PLANET_SZ_CORRECTION))
	ssys.addTo(makeVenus(ssys, color=color.yellow, ptype=INNER_PLANET, sizeCorrectionType=INNER_PLANET, defaultSizeCorrection=PLANET_SZ_CORRECTION))
	
	# EARTH	
	earth = makeEarth(ssys, color=color.cyan, ptype=INNER_PLANET, sizeCorrectionType=INNER_PLANET, defaultSizeCorrection=PLANET_SZ_CORRECTION)
	ssys.addTo(earth)

	ssys.addTo(makeLuna(ssys, color=color.white, centralbody=earth))

	# MARS
	mars = makeMars(ssys, color=color.red, ptype=INNER_PLANET, sizeCorrectionType=INNER_PLANET, defaultSizeCorrection=PLANET_SZ_CORRECTION)
	ssys.addTo(mars)

	ssys.addTo(makePlanetMoon(ssys, key='phobos', color=color.red, sizeCorrectionType=SMALL_MOON, centralbody=mars))
	ssys.addTo(makePlanetMoon(ssys, key='deimos', color=color.white, sizeCorrectionType=SMALL_MOON, centralbody=mars))

	# JUPITER
	jupiter = makeJupiter(ssys, color=color.magenta, ptype=OUTER_PLANET, sizeCorrectionType=GAS_GIANT, defaultSizeCorrection=PLANET_SZ_CORRECTION)
	ssys.addTo(jupiter)

	ssys.addTo(makePlanetMoon(ssys, key='ganymede', color=color.green, sizeCorrectionType=MOON, centralbody=jupiter))
	ssys.addTo(makePlanetMoon(ssys, key='callisto', color=color.orange, sizeCorrectionType=MOON, centralbody=jupiter))
	ssys.addTo(makePlanetMoon(ssys, key='io', color=color.cyan, sizeCorrectionType=MOON, centralbody=jupiter))
	ssys.addTo(makePlanetMoon(ssys, key='adrastea', color=color.yellow, sizeCorrectionType=TINY_MOON, centralbody=jupiter))
	ssys.addTo(makePlanetMoon(ssys, key='amalthea', color=Color.pink, sizeCorrectionType=SMALL_MOON, centralbody=jupiter))

	# SATURN 
	saturn = makeSaturn(ssys, color=color.cyan, ptype=OUTER_PLANET, sizeCorrectionType=GAS_GIANT, defaultSizeCorrection=PLANET_SZ_CORRECTION)
	ssys.addTo(saturn)

	ssys.addTo(makePlanetMoon(ssys, key='mimas', color=color.green, sizeCorrectionType=SMALL_MOON, centralbody=saturn))
	ssys.addTo(makePlanetMoon(ssys, key='titan', color=color.yellow, sizeCorrectionType=MOON, centralbody=saturn))
	ssys.addTo(makePlanetMoon(ssys, key='iapetus', color=color.red, sizeCorrectionType=MOON, centralbody=saturn))
	ssys.addTo(makePlanetMoon(ssys, key='rhea', color=color.magenta, sizeCorrectionType=MOON, centralbody=saturn))
	ssys.addTo(makePlanetMoon(ssys, key='dione', color=Color.pink, sizeCorrectionType=MOON, centralbody=saturn))
	ssys.addTo(makePlanetMoon(ssys, key='tethys', color=Color.lightgrey, sizeCorrectionType=MOON, centralbody=saturn))
	ssys.addTo(makePlanetMoon(ssys, key='enceladus', color=color.orange, sizeCorrectionType=SMALL_MOON, centralbody=saturn))
	ssys.addTo(makePlanetMoon(ssys, key='hyperion', color=Color.cyanish, sizeCorrectionType=SMALL_MOON, centralbody=saturn))

	# URANUS
	uranus = makeUranus(ssys, color=color.yellow, ptype=OUTER_PLANET, sizeCorrectionType=GAS_GIANT, defaultSizeCorrection=PLANET_SZ_CORRECTION)
	ssys.addTo(uranus)

	# NEPTUNE
	neptune = makeNeptune(ssys, color=color.orange, ptype=OUTER_PLANET, sizeCorrectionType=GAS_GIANT, defaultSizeCorrection=PLANET_SZ_CORRECTION)
	ssys.addTo(neptune)

	# PLUTO
	pluto = makePluto(ssys, color=color.green, ptype=OUTER_PLANET, sizeCorrectionType=INNER_PLANET, defaultSizeCorrection=PLANET_SZ_CORRECTION) #OUTER_PLANET, DWARF_PLANET)
	ssys.addTo(pluto)

	ssys.addTo(makePlanetMoon(ssys, key='charon', color=color.white, sizeCorrectionType=MOON, centralbody=pluto))

	# ECLIPTIC
	ssys.addTo(makeEcliptic(ssys, color.white, 0.4))
	
	# DWARF PLANETS
	ssys.addTo(makeDwarfPlanet(ssys, key='eris', color=color.yellow))
	ssys.addTo(makeDwarfPlanet(ssys, key='makemake', color=color.magenta))
	ssys.addTo(makeDwarfPlanet(ssys, key='sedna', color=color.orange))
	ssys.addTo(makeDwarfPlanet(ssys, key='haumea', color=color.white))

	# BELTS
	ssys.addTo(makeBelt(ssys, key='kuiper', name='Kuiper Belt', ptype=KUIPER_BELT, color=color.cyan, size=2, density=4))
	ssys.addTo(makeBelt(ssys, key='asteroid', name='Asteroid Belt', ptype=ASTEROID_BELT, color=color.white, size=2, density=2))
	ssys.addTo(makeBelt(ssys, key='inneroort', name='Inner Oort Cloud', ptype=INNER_OORT_CLOUD, color=color.white, size=2, density=5))

	# JUPITER TROJANS
	ssys.addJTrojans(makeJtrojan(ssys, key='jupiterTrojan', name='Jupiter Trojans', ptype=JTROJANS, color=color.green, size=2, density=5, planetname='jupiter'))
	
	MAX_OBJECTS = 1000
	# ----> 2026/02/23 commented this out: loadBodies(ssys, PHA, "data/test.json", MAX_OBJECTS)

	if False:
		print "LOADING bodies orbital elements and trajectories ..."
		loadBodies(ssys, PHA, "data/200m+PHA_orbital_elements.txt.json", MAX_OBJECTS)
		loadBodies(ssys, BIG_ASTEROID,"data/200km+asteroids_orbital_elements.txt.json", MAX_OBJECTS)
		loadBodies(ssys, COMET, "data/200m+comets_orbital_elements.txt.json", MAX_OBJECTS)
		loadBodies(ssys, TRANS_NEPT, "data/transNeptunian_objects.txt.json", MAX_OBJECTS)
		loadBodies(ssys, SPACECRAFT, "data/spacecrafts_orbital_elements.txt.json", MAX_OBJECTS)
		print "FINISHED ..."

	# ----> 2026/02/23 commented this out: loadBodies(ssys, SPACECRAFT, "data/spacecrafts_orbital_elements.txt.json", MAX_OBJECTS)

	ssys.drawAllBodiesTrajectory()

	glbRefresh(ssys, False)
#	return ssys, moon
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
			ssys.introZoomIn(135) #75)
			#ssys.rotateSolarSystemReferential(axis=vector(0,1,0))
			#ssys.Scene.fov = pi

		# we only show the dashboard after the story has finished.
		ssys.getDashboard().Show()
		ssys.setAutoScale(False)
		#ssys.getDashboard().showInfoWindow(False)

		print "Calculate equinox/solstyce"
		Vernal(2023) ### a test ...
		Vernal2(2023)

#		print "Moon Coordinates are", 
#
#		print moon.Position
#		print
		I = 0
		while True:
			#print I
			#I += 1
			rate(60)
			sleep(1) #2)
		#	earth.updateStillPosition(cw.orbitalBox, 2)

	except RuntimeError as err:
		print ("Exception...\n\nError: " + str(err)) #.code))
		raise

	