""" planets.py  """

from orbit3D import *
import planetsdata as pd
from controls import *
from celestial.orbitalLIB import Api

class makeMercury(makePlanet):
	
	def __init__(self, system, Color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "mercury", Color, ptype, sizeCorrectionType, defaultSizeCorrection)


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

	def AdjustNPforPeriodicTerms(self, RA, decl, T, d):
	    # Jupiter needs to adjust the right Ascension 
	    # and declination for periodic terms
        # Jx angles are in degrees

		Ja = 99.360714 + 4850.4046 * T
		Jb = 175.895369 + 1191.9605 * T 
		Jc = 300.323162 + 262.5475 * T
		Jd = 114.012305 + 6070.2476 * T
		Je = 49.511251 + 64.3000 * T
		Ja_rad = np.radians(Ja)
		Jb_rad = np.radians(Jb)
		Jc_rad = np.radians(Jc)
		Jd_rad = np.radians(Jd)
		Je_rad = np.radians(Je)

		# adjust provided values
		RA += 0.000117 * np.sin(Ja_rad) + 0.000938 * np.sin(Jb_rad) + \
			  0.001432 * np.sin(Jc_rad) + 0.000030 * np.sin(Jd_rad) + 0.002150 * np.sin(Je)

		decl += 0.000050 * np.cos(Ja_rad) + 0.000404 * np.cos(Jb_rad) + \
			  	0.000617 * np.cos(Jc_rad) - 0.000013 * np.cos(Jd_rad) + 0.000926 * np.cos(Je)

		return RA, decl
 

class makeNeptune(makePlanet):
	
	def __init__(self, system, Color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "neptune", Color, ptype, sizeCorrectionType, defaultSizeCorrection)


	def AdjustNPforPeriodicTerms(self, RA, decl, T, d):
		# For neptune, we need to start from scratch because the 
		# general calculation doesn't apply for its RA and Decl

		N = 357.85 + 52.316 * T
		N_rad = np.radians(N)

		RA = 299.36 + 0.70 * np.sin(N_rad)
		decl = 43.46 - 0.51 * np.cos(N_rad)
		return RA, decl

	def AdjustPMforPeriodicTerms(self, W, T, d):
		# For neptune, we need to start from scratch because the 
		# general calculation doesn't apply for its W angle
		
		N = 357.85 + 52.316 * T
		N_rad = np.radians(N)

		W = 253.18 + 536.3128492 * d - 0.48 * np.sin(N_rad)

		# Normalize W (ensure its value is within 0-360 degrees)
		W = W % 360.0
		if W < 0:
			W += 360.0
		return W


class makePluto(makePlanet):
	
	def __init__(self, system, Color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "pluto", Color, ptype, sizeCorrectionType, defaultSizeCorrection)


