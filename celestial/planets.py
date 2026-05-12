""" planets.py  """

from orbit3D import *
import planetsdata as pd
from controls import *
from celestial.orbitalLIB import Api

class makeMercury(makePlanet):
	
	def __init__(self, system, color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "mercury", color, ptype, sizeCorrectionType, defaultSizeCorrection)

	def AdjustPMforPeriodicTerms(self, T, d):
		# return a value that needs to be added to
		# the current standard calculation of the PM
		# to apply a corrective factor

		# For Mercury, we need to adjust the prime meridien for extra periodic terms:
    	# W += sum(A_i * sin(M_i))
    	# M_i are arguments of periodic terms.

		periodicTerms = [ # A_i, M_i
            ( 0.00993822, 174.7948 + 17179159.230*d/360.0), # M1
            (-0.00104581, 349.5896 + 34358318.460*d/360.0), # M2
            (-0.00010280, 164.3844 + 51537477.690*d/360.0), # M3
            (-0.00002364, 339.1792 + 68716636.920*d/360.0), # M4
            (-0.00000532, 153.9740 + 85895796.150*d/360.0)  # M5
        ]		

		adjustment = 0.0

		# take into account periodic terms in the W calculation
		for amplitude, argument_deg_per_cycle in periodicTerms:
			adjustment += amplitude * np.sin(np.radians(argument_deg_per_cycle))

		return adjustment


	def AdjustPMforPeriodicTermsXX(self, W, T, d):

		# For Mercury, we need to adjust the prime meridien for extra periodic terms:
    	# W += sum(A_i * sin(M_i))
    	# M_i are arguments of periodic terms.

		periodicTerms = [ # A_i, M_i
            ( 0.00993822, 174.7948 + 17179159.230*d/360.0), # M1
            (-0.00104581, 349.5896 + 34358318.460*d/360.0), # M2
            (-0.00010280, 164.3844 + 51537477.690*d/360.0), # M3
            (-0.00002364, 339.1792 + 68716636.920*d/360.0), # M4
            (-0.00000532, 153.9740 + 85895796.150*d/360.0)  # M5
        ]		

		# take into account periodic terms in the W calculation
		for amplitude, argument_deg_per_cycle in periodicTerms:
			W += amplitude * np.sin(np.radians(argument_deg_per_cycle))

		# Normalize W (ensure its value is within 0-360 degrees)
		W = W % 360.0
		if W < 0:
			W += 360.0
		#print "Mercury: adjusting W to ", W
		return W

class makeVenus(makePlanet):
	
	def __init__(self, system, color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "venus", color, ptype, sizeCorrectionType, defaultSizeCorrection)


class makeMars(makePlanet):
	
	def __init__(self, system, color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "mars", color, ptype, sizeCorrectionType, defaultSizeCorrection)
		#print "****** MARS W = ", self.W_angle


class makeSaturn(makePlanet):
	
	def __init__(self, system, color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "saturn", color, ptype, sizeCorrectionType, defaultSizeCorrection)


class makeUranus(makePlanet):
	
	def __init__(self, system, color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "uranus", color, ptype, sizeCorrectionType, defaultSizeCorrection)


class makeJupiter(makePlanet):
	
	def __init__(self, system, color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "jupiter", color, ptype, sizeCorrectionType, defaultSizeCorrection)


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
	
	def __init__(self, system, color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "neptune", color, ptype, sizeCorrectionType, defaultSizeCorrection)


	def AdjustNPforPeriodicTerms(self, RA, decl, T, d):
		# For neptune, we need to start from scratch because the 
		# general calculation doesn't apply for its RA and Decl

		N = 357.85 + 52.316 * T
		N_rad = np.radians(N)

		RA = 299.36 + 0.70 * np.sin(N_rad)
		decl = 43.46 - 0.51 * np.cos(N_rad)
		return RA, decl

	def AdjustPMforPeriodicTerms(self, T, d):
		# return a value that needs to be added to
		# the current standard calculation of the PM
		# to apply a corrective factor

		N = 357.85 + 52.316 * T
		N_rad = np.radians(N)

		return - 0.48 * np.sin(N_rad)


	def AdjustPMforPeriodicTermsXX(self, W, T, d):
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
	
	def __init__(self, system, color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, "pluto", color, ptype, sizeCorrectionType, defaultSizeCorrection)


class makeSystemBarycenter(makePlanet):

	# intuitively, makeSystemBarycenter must derive from makePlanet, since it is
	# IT that orbits the sun on the behalf of its underlying planet and moons.
	
	def __init__(self, system, key, color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makePlanet.__init__(self, system, key, color, ptype, sizeCorrectionType, defaultSizeCorrection, barycenter=True)

	def setMainMemberBodyType(self, ptype):
		self.MainMember_bodytype = ptype
		
	def setAspect(self, key):
		# barycenter has no texture ...
		pass

	def make_PCI_referentialXX(self):
		# barycenter has no axis ...
		pass 

	def setBodyOrientation(self):
		# barycenter has no orientation ...
		pass

	def makeShape(self):
		self.RefOrigin.pos= self.Position 

	def refresh(self):
		"""
		This is the refresh function for a barycenter system. It follows the same
		principle as for a non-barycentric system. Each member of a barycenter system
		acts as a "moon" of this system, with one member defined as the "main" member.

		When a barycenter is the focus and MOON is set, we display its member(s), but
		if the barycenter isn't the focus we do not display the member(s). We do not 
		call the refresh method for members, as their "refresh" is performed from their
		barycenter. If one of the member is the focus, then we display that member 
		only, even though the MOON flag is off, and we also display the parent planet 
		member, even if its flag should make it hidden
		"""

		bodyVisible = True if self.Object_class & self.SolarSystem.ShowFeatures != 0 else False

		showAxis = False
		if bodyVisible or self.Details == True:

			# check if barycenter is current focus
			isFocus = True if self.SolarSystem.cameraViewTargetName == self.Name else False

			# this body orbits the sun 
			# Let's see if it has moons

			displayMembers = True if self.SolarSystem.ShowFeatures & MOON != 0 else False

			print "REFRESHING ", self.Name

			# loop through each moon / spacecraft / barycenter-member
			for member_name, member_body in self.planetOrbitingBodies.items():

				if isFocus:
					if displayMembers:
						print "show member ", member_name, " for FOCUS = ", self.Name
						member_body.show()
					else:
						print "hide member ", member_name, " for FOCUS = ", self.Name
						member_body.hide()

				else:
					print self.Name, " is not the focus!"

					# check if this moon/member is the focus
					if self.SolarSystem.cameraViewTargetName == member_body.Name:
						print "show member ", member_name, " for barycenter ", self.Name
						member_body.show()

						if member_body.Object_role == BARYCENTER_MEMBER:
							parent = self.SolarSystem.getBarycenterMemberFromName(member_body.Object_parent)
							if parent != None:
								parent.show()

					else:
						if member_body.Main == False:
							print "hide member ", member_name, " for barycenter ", self.Name
							member_body.hide()


			# if this is the cameraViewTargetBody, 
			# check for local referential attribute

			if isFocus and self.SolarSystem.ShowFeatures & LOCAL_REFERENTIAL:
				showAxis = True

		else:
			# the barycenter is not visible. let's see if a member orbiting it
			# might be the focus (cameraViewTarget)

			if self.SolarSystem.cameraViewTargetName in self.planetOrbitingBodies:
				# if it is the case, force to show the body 
				self.show()
				self.setAxisVisibility(False)
				return
			else:
				for member_name, member_body in self.planetOrbitingBodies.items():
					member_body.hide()

			self.hide()

		self.setAxisVisibility(showAxis)



class makePlutoBarycenterXX(makeSystemBarycenter):
	
	def __init__(self, system, color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makeSystemBarycenter.__init__(self, system, "pluto-barycenter", color, ptype, sizeCorrectionType, defaultSizeCorrection)

	def FixPlutoEccentricityXXXX(self):
		pluto = self.SolarSystem.getBarycenterMemberFromName("pluto")
		charon = self.SolarSystem.getBarycenterMemberFromName("charon")
		pluto.e = charon.e = 0.0
		pluto.Inclination = charon.Inclination
		pluto.Longitude_of_ascendingnode = charon.Longitude_of_ascendingnode
		pluto.Argument_of_periapsis = charon.Argument_of_periapsis 
		pluto.Mean_anomaly = charon.Mean_anomaly + np.pi
		pluto.a = charon.a * (1.586e21/1.303e22)
		charon.a = charon.a * 2
		pluto.Revolution = charon.Revolution = 6.38723
		pluto.Mean_motion = charon.Mean_motion = 360/6.38723
		#pluto.Rotation = charon.Rotation = 6.38723




class makeEarth(makeEarth_and_widgets):
	
	def __init__(self, system, color, ptype, sizeCorrectionType, defaultSizeCorrection):
		makeEarth_and_widgets.__init__(self, system, color, ptype, sizeCorrectionType, defaultSizeCorrection)


