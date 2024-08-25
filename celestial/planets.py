""" planets.py  """

from orbit3D import *
import planetsdata as pd
from controls import *
from celestial.orbitalLIB import Api

class makeMercury(makePlanet):
	
	def __init__(self, system, Color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "mercury", Color, ptype, sizeCorrectionType, defaultSizeCorrection)

	def setNorthPoleDirection(self):
		# for now the method is just like the defaut method, but it should be upgraded 
		# to refect the the complexity of the calculation
		if "rotationalElts" in self.SolarSystem.objects_data[self.ObjectIndex]:

			T = daysSinceJ2000UTC(self.locationInfo)/EARTH_CENTURY #36525. # T is in centuries
			D = daysSinceJ2000UTC(self.locationInfo)
			RE = self.SolarSystem.objects_data[self.ObjectIndex]["rotationalElts"]

			ra = RE["ra_1"] + RE["ra_2"] * T
			decl = RE["dc_1"] + RE["dc_2"] * T
			primeM = RE["W_1"] + RE["W_2"] * D + RE["W_C"]
			return ra % 360, decl, primeM

			#return RE["W_1"] + RE["W_2"] * D + RE["W_C"]

		return 0,0,0

class makeVenus(makePlanet):
	
	def __init__(self, system, Color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "venus", Color, ptype, sizeCorrectionType, defaultSizeCorrection)


class makeMars(makePlanet):
	
	def __init__(self, system, Color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "mars", Color, ptype, sizeCorrectionType, defaultSizeCorrection)

class makeSaturn(makePlanet):
	
	def __init__(self, system, Color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "saturn", Color, ptype, sizeCorrectionType, defaultSizeCorrection)

class makeUranus(makePlanet):
	
	def __init__(self, system, Color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "uranus", Color, ptype, sizeCorrectionType, defaultSizeCorrection)

class makeJupiter(makePlanet):
	
	def __init__(self, system, Color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "jupiter", Color, ptype, sizeCorrectionType, defaultSizeCorrection)

class makeNeptune(makePlanet):
	
	def __init__(self, system, Color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "neptune", Color, ptype, sizeCorrectionType, defaultSizeCorrection)

	def setNorthPoleDirection(self):
		if "rotationalElts" in self.SolarSystem.objects_data[self.ObjectIndex]:

			T = daysSinceJ2000UTC(self.locationInfo)/EARTH_CENTURY #36525. # T is in centuries
			D = daysSinceJ2000UTC(self.locationInfo)
			RE = self.SolarSystem.objects_data[self.ObjectIndex]["rotationalElts"]

			N = deg2rad(RE["N_1"] + RE["N_2"]*T)
			ra = RE["ra_1"] + RE["ra_2"] * T
			decl = RE["dc_1"] + RE["dc_2"] * T
			primeM = RE["W_1"] + RE["W_2"] * D + RE["W_3"]*sin(N)

			#print "NEPTUNE !!!!!!!!!!!!!!!!!!!!!!!!", toto  % 360
			#return raw % 360
			return ra % 360, decl, primeM
		return 0,0,0
