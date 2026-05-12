""" main module  """

from re import I
import re as RE
from rate_func import *	
from orbit3D import *
from planets import *
#import planetsdata as pd
from planetsdata import *
from controls import *
from celestial.orbitalLIB import Api
from eqsols_calculator import Vernal, Vernal2
from moons import makePlanetMoon, makeLuna, makeSystemBarycenterMember, makeSystemBarycenterMain
from objects_loader import load_objects_catalog
from moons_loader import load_moon_catalog

#from utils import sleep
print "re ==",RE.__version__

def createSolarSystem():
		
	# LOAD CATALOGS
	moons_catalog = load_moon_catalog()
	objects_data.update(moons_catalog)
	
	objects_catalog = load_objects_catalog()
	objects_data.update(objects_catalog)

	# CREATE SOLAR SYSTEM REFERENTIAL
	ssys = makeSolarSystem()
	
	# set what is displayed by default
	ssys.setDefaultFeatures(INNER_PLANET|OUTER_PLANET|ORBITS|SPACECRAFT|MOON|SUN) 

#	sun_barycenter = makeBarycenter(ssys, key='sun-barycenter', color=color.green, ptype=BARYCENTER, sizeCorrectionType=SUN, defaultSizeCorrection=SUN_SZ_CORRECTION)
#	sun = makeBarycenterMember(ssys, key='sun', color=color.white, ptype=SUN, sizeCorrectionType=MOON, realisticCorrectionSize=SUN_SZ_CORRECTION, barycenter=sun_barycenter)	
	

	sun = makeSun(ssys, color=color.black, ptype=SUN, sizeCorrectionType=SUN, defaultSizeCorrection=SUN_SZ_CORRECTION)
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

	# we need a special moon class for Luna, as it is a highly irregular moon
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
	ssys.addTo(makePlanetMoon(ssys, key='adrastea', color=color.yellow, sizeCorrectionType=SMALL_MOON, centralbody=jupiter))
	ssys.addTo(makePlanetMoon(ssys, key='amalthea', color=Color.pink, sizeCorrectionType=SMALL_MOON, centralbody=jupiter))
	ssys.addTo(makePlanetMoon(ssys, key='europa', color=Color.grey, sizeCorrectionType=MOON, centralbody=jupiter))

	# SATURN 
	saturn = makeSaturn(ssys, color=color.cyan, ptype=OUTER_PLANET, sizeCorrectionType=GAS_GIANT, defaultSizeCorrection=PLANET_SZ_CORRECTION)
	ssys.addTo(saturn)

	ssys.addTo(makePlanetMoon(ssys, key='mimas', color=color.green, sizeCorrectionType=MOON, centralbody=saturn))
	ssys.addTo(makePlanetMoon(ssys, key='titan', color=color.yellow, sizeCorrectionType=MOON, centralbody=saturn))
	ssys.addTo(makePlanetMoon(ssys, key='iapetus', color=color.red, sizeCorrectionType=MOON, centralbody=saturn))
	ssys.addTo(makePlanetMoon(ssys, key='rhea', color=color.magenta, sizeCorrectionType=MOON, centralbody=saturn))
	ssys.addTo(makePlanetMoon(ssys, key='dione', color=Color.pink, sizeCorrectionType=MOON, centralbody=saturn))
	ssys.addTo(makePlanetMoon(ssys, key='tethys', color=Color.lightgrey, sizeCorrectionType=MOON, centralbody=saturn))
	ssys.addTo(makePlanetMoon(ssys, key='enceladus', color=color.orange, sizeCorrectionType=SMALLER_MOON, centralbody=saturn))
	ssys.addTo(makePlanetMoon(ssys, key='hyperion', color=Color.cyanish, sizeCorrectionType=SMALL_MOON, centralbody=saturn))

	# URANUS
	uranus = makeUranus(ssys, color=color.yellow, ptype=OUTER_PLANET, sizeCorrectionType=GAS_GIANT, defaultSizeCorrection=PLANET_SZ_CORRECTION)
	ssys.addTo(uranus)

	ssys.addTo(makePlanetMoon(ssys, key='umbriel', color=Color.orange, sizeCorrectionType=SMALLER_MOON, centralbody=uranus))


	# NEPTUNE
	neptune = makeNeptune(ssys, color=color.orange, ptype=OUTER_PLANET, sizeCorrectionType=GAS_GIANT, defaultSizeCorrection=PLANET_SZ_CORRECTION)
	ssys.addTo(neptune)

	ssys.addTo(makePlanetMoon(ssys, key='despina', color=Color.orange, sizeCorrectionType=SMALL_MOON, centralbody=neptune))
	ssys.addTo(makePlanetMoon(ssys, key='thalassa', color=Color.yellow, sizeCorrectionType=SMALL_MOON, centralbody=neptune))
	ssys.addTo(makePlanetMoon(ssys, key='nereid', color=Color.blue, sizeCorrectionType=SMALL_MOON, centralbody=neptune))
	ssys.addTo(makePlanetMoon(ssys, key='larissa', color=Color.red, sizeCorrectionType=SMALLER_MOON, centralbody=neptune))
	ssys.addTo(makePlanetMoon(ssys, key='naiad', color=Color.cyanish, sizeCorrectionType=SMALL_MOON, centralbody=neptune))
	ssys.addTo(makePlanetMoon(ssys, key='proteus', color=Color.lightgrey, sizeCorrectionType=SMALLER_MOON, centralbody=neptune))
	ssys.addTo(makePlanetMoon(ssys, key='galatea', color=Color.pink, sizeCorrectionType=SMALL_MOON, centralbody=neptune))
	ssys.addTo(makePlanetMoon(ssys, key='triton', color=Color.green, sizeCorrectionType=BIG_MOON, centralbody=neptune))


	# DWARF PLANETS
	# PLUTO
	useBarycenter = True
	if useBarycenter == False:
		pluto = makePluto(ssys, color=color.green, ptype=DWARF_PLANET, sizeCorrectionType=INNER_PLANET, defaultSizeCorrection=PLANET_SZ_CORRECTION) #OUTER_PLANET, DWARF_PLANET)
		ssys.addTo(pluto)
		ssys.addTo(makePlanetMoon(ssys, key='charon', color=color.white, sizeCorrectionType=MOON, centralbody=pluto))
	else:
		
		# when creating a barycenter system, the main body of the system should be created
		# immediately after the barycenter

		pluto_barycenter = makeSystemBarycenter(ssys, key='pluto-barycenter', color=color.green, ptype=BARYCENTER, sizeCorrectionType=INNER_PLANET, defaultSizeCorrection=PLANET_SZ_CORRECTION) #OUTER_PLANET, DWARF_PLANET)
		pluto = makeSystemBarycenterMain(ssys, key='pluto', color=color.white, ptype=DWARF_PLANET, sizeCorrectionType=MOON, realisticCorrectionSize=PLANET_SZ_CORRECTION, barycenter=pluto_barycenter)
		ssys.addTo(pluto)
		ssys.addTo(makeSystemBarycenterMember(ssys, key='charon', color=color.yellow, ptype=MOON, sizeCorrectionType=MOON, realisticCorrectionSize=MOON_SZ_CORRECTION, barycenter=pluto_barycenter))

	# ECLIPTIC
	ssys.addTo(makeEcliptic(ssys, color.white, 0.4))
	
	#ssys.addTo(makeDwarfPlanet(ssys, key='eris', color=color.yellow))
	#ssys.addTo(makeDwarfPlanet(ssys, key='makemake', color=color.magenta))
	#ssys.addTo(makeDwarfPlanet(ssys, key='sedna', color=color.orange))
	#ssys.addTo(makeDwarfPlanet(ssys, key='haumea', color=color.white))

	# TNOs
	ssys.addTo(makeTNO(ssys, key='eris', color=color.yellow, centralbody=None))
	ssys.addTo(makeTNO(ssys, key='makemake', color=color.magenta, centralbody=None))
	ssys.addTo(makeTNO(ssys, key='sedna', color=color.orange, centralbody=None))
	ssys.addTo(makeTNO(ssys, key='haumea', color=color.white, centralbody=None))

	# BELTS
	ssys.addTo(makeBelt(ssys, key='kuiper', name='Kuiper Belt', ptype=KUIPER_BELT, color=Color.lightgrey, size=2, density=4))
	ssys.addTo(makeBelt(ssys, key='asteroid', name='Asteroid Belt', ptype=ASTEROID_BELT, color=color.white, size=2, density=2))
#	ssys.addTo(makeBelt(ssys, key='inneroort', name='Inner Oort Cloud', ptype=INNER_OORT_CLOUD, color=color.white, size=2, density=5))

	# JUPITER TROJANS
	ssys.addJTrojans(makeJtrojan(ssys, key='jupitertrojans', name='Jupiter Trojans', ptype=JTROJANS, color=color.green, size=2, density=5, planetname='jupiter'))
	
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

#	glbRefresh(ssys, False) #< ---- PUT IT BACK!!!

#	return ssys, moon
	return ssys



def bootLoader(story, recorder): 

	# Start control window
	print (wx.version())


	# start wxPython application
	try:
		ex = wx.App(False)
		ssys = createSolarSystem()

		"""
		for name, body in ssys.sunOrbiting.items():
			print("Body: {0} | Type: {1}".format(name, body.BodyType))
			if hasattr(body, 'planetOrbitingBodies'):
				for key, moon in body.planetOrbitingBodies.items():
					print("Body: {0} | Moon: {1}".format(name, moon.Name))
		"""

		ssys.setEarthLocations(makeDashBoard(ssys))
		#ssys.getDashboard().showInfoWindow(True)

		print ssys.getFocusList()

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
			ssys.introZoomIn(130, recorder) #75)
			#ssys.rotateSolarSystemReferential(axis=vector(0,1,0))
			#ssys.Scene.fov = pi

		# we only show the dashboard after the story has finished.
		ssys.getDashboard().Show()
		ssys.setAutoScale(False)
		#ssys.getDashboard().showInfoWindow(False)

		print "Calculate equinox/solstyce"
		Vernal(2026) ### a test ...
		Vernal2(2026)

#		print "Moon Coordinates are", 
#
#		print moon.Position
#		print
		I = 0
		while True:
			#print I
			#I += 1
			#rate(60)
			sleep(1) #2)
		#	earth.updateStillPosition(cw.orbitalBox, 2)

	except RuntimeError as err:
		print ("Exception...\n\nError: " + str(err)) #.code))
		raise

	
