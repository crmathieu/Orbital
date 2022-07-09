"""
COMMAND = '50000001'
CENTER = '@10'
OBJ_DATA = 'yes'
MAKE_EPHEM = 'yes'
TABLE_TYPE = 'ELEMENTS'
REF_PLANE = 'ECLIPTIC'
COORD_TYPE = 'GEODETIC'
START_TIME = '2021/5/6 15:52'
STOP_TIME = '2021/5/7 15:52'
STEP_SIZE = '1h'
QUANTITIES = '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46'
FIXED_QUANTITIES = 'A'
REF_SYSTEM = 'J2000'
OUT_UNITS = 'KM-S'
VECT_TABLE = '3'
VECT_CORR = 'NONE'
CAL_FORMAT = 'CAL'
ANG_FORMAT = 'DEG'
APPARENT = 'AIRLESS'
TIME_TYPE = 'UTC'
TIME_DIGITS = 'MINUTES'
RANGE_UNITS = 'AU'
SUPPRESS_RANGE_RATE = 'no'
SKIP_DAYLT = 'no'
EXTRA_PREC = 'yes'
CSV_FORMAT = 'yes'
VEC_LABELS = 'yes'
ELM_LABELS = 'yes'
TP_TYPE = 'ABSOLUTE'
R_T_S_ONLY = 'NO'
CA_TABLE_TYPE = 'STANDARD'
"""

JDTDB = 0					# in Julian day number, Barycentric Dynamical Time
DATETIME = 1				# string
EC_ECCENTRICITY = 2			# e no unit
QR_PERIAPSIS = 3			# q in km
IN_INCLINATION = 4			# i in degrees
OM_LONG_OF_ASCNODE = 5		# Omega in degrees
W_ARG_OF_PERIFOCUS = 6		# w in degrees
TP_TIME_OF_PERIAPSIS = 7	# in Julian day number
N_MEAN_MOTION = 8			# n in degrees/second
MA_MEAN_ANOMALY = 9			# M in degrees
TA_TRUE_ANOMALY = 10		# Nu in degrees
A_SEMI_MAJOR = 11			# a in km
AD_APOAPSIS = 12			# in km
PR_SIDERAL_ORBIT = 13 		# in seconds
#/horizons_batch.cgi?batch=1&COMMAND=%2750000001%27&CENTER=%27@10%27&OBJ_DATA=%27yes%27&MAKE_EPHEM=%27yes%27&TABLE_TYPE=%27ELEMENTS%27&REF_PLANE=%27ECLIPTIC%27&COORD_TYPE=%27GEODETIC%27&START_TIME=%272021/5/6%2015:52%27&STOP_TIME=%272021/5/7%2015:52%27&STEP_SIZE=%271h%27&QUANTITIES=%271,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46%27&FIXED_QUANTITIES=%27A%27&REF_SYSTEM=%27J2000%27&OUT_UNITS=%27KM-S%27&VECT_TABLE=%273%27&VECT_CORR=%27NONE%27&CAL_FORMAT=%27CAL%27&ANG_FORMAT=%27DEG%27&APPARENT=%27AIRLESS%27&TIME_TYPE=%27UTC%27&TIME_DIGITS=%27MINUTES%27&RANGE_UNITS=%27AU%27&SUPPRESS_RANGE_RATE=%27no%27&SKIP_DAYLT=%27no%27&EXTRA_PREC=%27yes%27&CSV_FORMAT=%27yes%27&VEC_LABELS=%27yes%27&ELM_LABELS=%27yes%27&TP_TYPE=%27ABSOLUTE%27&R_T_S_ONLY=%27NO%27&CA_TABLE_TYPE=%27STANDARD%27


import urllib2

import requests

import urllib
import httplib
import StringIO
from datetime import datetime, timedelta
#from urllib import quote
import json

#zob ="https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&COMMAND='2022 JO1'&CENTER='@10'&START_TIME='2022-05-09'&STOP_TIME='2022-05-10'&MAKE_EPHEM=YES&EPHEM_TYPE=ELEMENTS"

if False:
	params = "/horizons_batch.cgi?batch=1&COMMAND=50000001&CENTER=@10&OBJ_DATA=yes&MAKE_EPHEM=yes&TABLE_TYPE=ELEMENTS&REF_PLANE=ECLIPTIC&COORD_TYPE=GEODETIC&STEP_SIZE=1h&QUANTITIES=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46&FIXED_QUANTITIES=A&REF_SYSTEM=J2000&OUT_UNITS=KM-S&VECT_TABLE=3&VECT_CORR=NONE&CAL_FORMAT=CAL&ANG_FORMAT=DEG&APPARENT=AIRLESS&TIME_TYPE=UTC&TIME_DIGITS=MINUTES&RANGE_UNITS=AU&SUPPRESS_RANGE_RATE=no&SKIP_DAYLT=no&EXTRA_PREC=yes&CSV_FORMAT=yes&VEC_LABELS=yes&ELM_LABELS=yes&TP_TYPE=ABSOLUTE&R_T_S_ONLY=NO&CA_TABLE_TYPE=STANDARD&START_TIME=%272021/5/6%2015:52%27&STOP_TIME=%272021/5/7%2015:52%27"
	#params = "/horizons_batch.cgi?batch=1&COMMAND=
	QHEADER = "/horizons_batch.cgi?format=json&batch=1&COMMAND="
	#%2750000001%27
	QCENTER = "&CENTER=%27@10%27&OBJ_DATA=%27yes%27&MAKE_EPHEM=%27yes%27&TABLE_TYPE=%27ELEMENTS%27&REF_PLANE=%27ECLIPTIC%27&COORD_TYPE=%27GEODETIC%27"
	QSTART = "&START_TIME="
	#%272021/5/7%2015:52%27
	QSTOP = "&STOP_TIME="
	#%272021/5/6%2016:52%27
	QSTEP = "&STEP_SIZE="  # 1h, 6h, ...
	#%271h%27
	QQUANTITIES = "&QUANTITIES=%271,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46%27&FIXED_QUANTITIES=%27A%27"
	QTRAILER = "&REF_SYSTEM=%27J2000%27&OUT_UNITS=%27KM-S%27&VECT_TABLE=%273%27&VECT_CORR=%27NONE%27&CAL_FORMAT=%27CAL%27&ANG_FORMAT=%27DEG%27&APPARENT=%27AIRLESS%27&TIME_TYPE=%27UTC%27&TIME_DIGITS=%27MINUTES%27&RANGE_UNITS=%27AU%27&SUPPRESS_RANGE_RATE=%27no%27&SKIP_DAYLT=%27no%27&EXTRA_PREC=%27yes%27&CSV_FORMAT=%27yes%27&VEC_LABELS=%27yes%27&ELM_LABELS=%27yes%27&TP_TYPE=%27ABSOLUTE%27&R_T_S_ONLY=%27NO%27&CA_TABLE_TYPE=%27STANDARD%27"

INPUT = "!$$SOF" 
MAKE_EPHEM='YES'
COMMAND=-143205
EPHEM_TYPE='ELEMENTS'
CENTER='500@10'
START_TIME='2022-07-06'
STOP_TIME='2022-07-07'
STEP_SIZE='1 DAYS'
REF_SYSTEM='ICRF'
REF_PLANE='ECLIPTIC'
OUT_UNITS='KM-S'
ELM_LABELS='YES'
TP_TYPE='ABSOLUTE'
CSV_FORMAT='YES'
OBJ_DATA='NO'


QHEADER = "?batch=1&COMMAND="
QCENTER = "&CENTER='@10'&MAKE_EPHEM='YES'&EPHEM_TYPE=ELEMENTS&REF_PLANE='ECLIPTIC'"
QSTART = "&START_TIME="
QSTOP = "&STOP_TIME="
QSTEP = "&STEP_SIZE="  # 1h, 6h, ...
QQUANTITIES = "" #"&QUANTITIES=%271,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46%27&FIXED_QUANTITIES=%27A%27"
QTRAILER = "&OBJ_DATA='YES'&FORMAT='json'" #&TIME_TYPE=UTC" #"&REF_SYSTEM='J2000'&OUT_UNITS=%27KM-S%27&VECT_TABLE=%273%27&VECT_CORR=%27NONE%27&CAL_FORMAT=%27CAL%27&ANG_FORMAT=%27DEG%27&APPARENT=%27AIRLESS%27&TIME_TYPE=%27UTC%27&TIME_DIGITS=%27MINUTES%27&RANGE_UNITS=%27AU%27&SUPPRESS_RANGE_RATE=%27no%27&SKIP_DAYLT=%27no%27&EXTRA_PREC=%27yes%27&CSV_FORMAT=%27yes%27&VEC_LABELS=%27yes%27&ELM_LABELS=%27yes%27&TP_TYPE=%27ABSOLUTE%27&R_T_S_ONLY=%27NO%27&CA_TABLE_TYPE=%27STANDARD%27"


# use a 24h interval
Q_interval = "'24h'"
objects_data = {}

G = 6.67384e-11	# Universal gravitational constant



target_name_pairs = {

    'Solar Orbiter (spacecraft) [Solo]': -144,
    'Solidaridad-1 (spacecraft)': -122911,
    'SpaceX Roadster (spacecraft) (Tesla)': -143205,
    'Spektr-R Observatory (spacecraft)': -557,
}

def is_float(string):
  try:
    return float(string) and '.' in string  # True if string is a number contains a dot
  except ValueError:  # String is not a number
    return False


class JPLsearch:

	#url = "https://ssd.jpl.nasa.gov/api/horizons_file.api"
	#url = "https://ssd-api.jpl.nasa.gov/sbdb.api?des="
	url = "https://ssd.jpl.nasa.gov/horizons_batch.cgi"

	GM_marker = "GM= "
	GM_token = "GM="
	RAD_token = "RAD="
	ROT_token = "ROTPER="			# Rotational period in hours
	ALBEDO_token = "ALBEDO="
	HSIGMA_token = "H="
	M1SIGMA_token = "M1="
	SEP_marker = "*********"

	objects_data = {}
	startMarker = "$$SOE"
	endMarker = "$$EOE"
	nameMarker = "Target body name:"

	def urlBuilder(self, targetid, starttime, endtime, step):
		return QHEADER+"'"+targetid+"'"+QCENTER+QSTART+"'"+starttime+"'"+QSTOP+"'"+endtime+"'"+QSTEP+"'"+step+"'"+QTRAILER


	def fetchElements(self, target):
		startdate = datetime.utcnow().strftime('%Y/%m/%d %H:%M')
		enddate = (datetime.utcnow()+timedelta(days=1)).strftime('%Y/%m/%d %H:%M')
		parameters = self.urlBuilder(target, startdate, enddate, "24h")
		#print "TARGET=", self.url+parameters
		if self.fetchJPL(parameters) == True:
			self.extractGeometry(target)
			self.extractAppearence(target)
			print objects_data


	def extractGeometry(self, target):

		# parse response using start and end markers
		
		print self.rawResp	

		# Extract body or spacecraft name
		name = ""
		nameStart = self.rawResp.find(self.nameMarker, 0, len(self.rawResp))
		if nameStart != -1:
			nameStart = nameStart + len(self.nameMarker) + 1
			nameEnd = self.rawResp.find("\n", nameStart, len(self.rawResp))
			name = self.rawResp[nameStart: nameEnd]
			parenthO = name.find("(", 0, len(name))
			if parenthO != -1:
				parenthC = name.find(")", parenthO, len(name))
				if parenthC != -1:
					name = name[:parenthC+1]
		else:
			name = "Unknown"
		name = name.encode('latin1')

		# Extract orbit geometry and dynamics 
		#print "Extracting ", name
		start = self.rawResp.find(self.startMarker, 0, len(self.rawResp))
		if start != -1:
			start = start + len(self.startMarker) + 1
			# then find end marker
			end = self.rawResp.find(self.endMarker, start, len(self.rawResp))
			if end != -1:
				cvs = self.rawResp[start:end]
				print cvs
				# read line by line
				line = StringIO.StringIO(cvs)
				rec = line.readline()
				"""
				we have 5 lines like so...
				FOR ASTEROID/Spacecraft
				2459767.547222222 = A.D. 2022-Jul-07 01:08:00.0000 TDB
				 EC= 2.559076913790752E-01 QR= 1.475078325645969E+08 IN= 1.075237496397935E+00
				 OM= 3.169157277789936E+02 W = 1.777528322639769E+02 Tp=  2459824.944332839455
				 N = 7.478182336937578E-06 MA= 3.229148685189527E+02 TA= 2.999336242914953E+02
				 A = 1.982386202028923E+08 AD= 2.489694078411878E+08 PR= 4.814004042423832E+07	

				 0- epoch
				 1->4 elements  

				FOR COMETS
				2459771.275000000 = A.D. 2022-Jul-10 18:36:00.0000 TDB 
				 EC= 1.000765215764738E+00 QR= 2.688045091983787E+08 IN= 8.756157502449179E+01
				 OM= 8.823504289230128E+01 W = 2.362002075701076E+02 Tp=  2459933.184257947374
				 N = 1.002534871705570E-10 MA=-1.402442010527421E-03 TA= 2.898425843946303E+02
				 A =-3.512793666638310E+11 AD= 9.999999999999998E+99 PR= 9.999999999999998E+99				 			
				"""
				k = 0

				"""
				JDTDB = 0					# in Julian day number, Barycentric Dynamical Time
				DATETIME = 1				# string
				EC_ECCENTRICITY = 2			# e no unit
				QR_PERIAPSIS = 3			# q in km
				IN_INCLINATION = 4			# i in degrees
				OM_LONG_OF_ASCNODE = 5		# Omega in degrees
				W_ARG_OF_PERIFOCUS = 6		# w in degrees
				TP_TIME_OF_PERIAPSIS = 7	# in Julian day number
				N_MEAN_MOTION = 8			# n in degrees/second
				MA_MEAN_ANOMALY = 9			# M in degrees
				TA_TRUE_ANOMALY = 10		# Nu in degrees
				A_SEMI_MAJOR = 11			# a in km
				AD_APOAPSIS = 12			# in km
				PR_SIDERAL_ORBIT = 13 		# in seconds"""
				elements = ["" for x in range(14)]

				#epoch, IN, EC, QR, QM, W, TP, N, MA, TA, A, AD, PR = "", "", "", "", "", "", "", "", "", "", "", "", ""
				chSplit = " "
				while len(rec) > 0:
					# break down in tokens
					arr = rec.split(chSplit) #" ")
					chSplit = "="
					print arr
					if k == 0:
						elements[JDTDB] = arr[0]
						elements[DATETIME] = arr[3] +" "+arr[4]
					elif k == 1:
				 		# EC= 1.000765215764738E+00 QR= 2.688045091983787E+08 IN= 8.756157502449179E+01
						elements[EC_ECCENTRICITY] = arr[1][1:-3]
						elements[QR_PERIAPSIS] =arr[2][1:-3] 
						elements[IN_INCLINATION] =arr[3][1:-1]
					elif k == 2:
						elements[OM_LONG_OF_ASCNODE] = arr[1][1:-3]
						elements[W_ARG_OF_PERIFOCUS] = arr[2][1:-3] 
						elements[TP_TIME_OF_PERIAPSIS] =arr[3][1:-1]
					elif k == 3:
						elements[N_MEAN_MOTION] = arr[1][1:-3]
						elements[MA_MEAN_ANOMALY] =arr[2][1:-3] 
						elements[TA_TRUE_ANOMALY] =arr[3][1:-1]
					elif k == 4:
						elements[A_SEMI_MAJOR] = arr[1][1:-3]
						elements[AD_APOAPSIS] =arr[2][1:-3] 
						elements[PR_SIDERAL_ORBIT] =arr[3][1:-1]
					else:
						break
					k += 1
					rec = line.readline()

				#print "----------"
				#print elements

				self.loadBodyInfo(target, name, elements)


	def extractAppearence(self, target):

		# For non-spacecraft bodies (asteroids, comets), we can also recover 
		# elements relative to the body appearence, shiness, self-rotation etc...
		# Non-spacecraft results incorporate these additional parameters that we can
		# also extract...

		GM = self.rawResp.find(self.GM_marker, 0, len(self.rawResp))
		if GM != -1:
			# then find separator marker
			sep = self.rawResp.find(self.SEP_marker, GM+len(self.GM_marker), len(self.rawResp))
			if sep != -1:
				objparams = self.rawResp[GM:sep]
				block = StringIO.StringIO(objparams)

				# read first line in block
				line = " ".join(block.readline().split())

				while len(line) > 0:
					# break down in tokens
					arr = line.split(" ")
					if len(arr) > 1:
						print arr
						for i in range(len(arr)):

							if arr[i] == self.GM_token:
								if is_float(arr[i+1]):
									objects_data[target]["mass"] = (float(arr[i+1])*1.e+9)/G
							else:
								if arr[i] == self.RAD_token:
									if is_float(arr[i+1]):
										print arr[i+1]
										objects_data[target]["radius"] = float(arr[i+1])
								else:
									if arr[i] == self.ROT_token:
										if is_float(arr[i+1]):
											objects_data[target]["rotation"] = float(arr[i+1])/24 # convert hours -> days
									else:
										if arr[i] == self.ALBEDO_token:
											if is_float(arr[i+1]):
												objects_data[target]["albedo"] = float(arr[i+1])
										else:
											if arr[i] == self.HSIGMA_token:
												if is_float(arr[i+1]):
													objects_data[target]["absolute_mag"] = float(arr[i+1])
											else:
												if arr[i] == self.M1SIGMA_token:
													if is_float(arr[i+1]):
														objects_data[target]["absolute_mag"] = float(arr[i+1])
					# check next line in block
					line = " ".join(block.readline().split())

	def loadBodyInfo(self, target, name, arr):

			objects_data[target] = {
				"profile": "",
				"material": 0,
				"name": name,
				"iau_name": name,
				"jpl_designation": target,
				"QR_perihelion": float(arr[QR_PERIAPSIS].strip()),
				"EC_e": float(arr[EC_ECCENTRICITY].strip()),
				
				"PR_revolution": float(arr[PR_SIDERAL_ORBIT].strip()),
				
				"IN_orbital_inclination": float(arr[IN_INCLINATION].strip()),

				"OM_longitude_of_ascendingnode":float(arr[OM_LONG_OF_ASCNODE].strip()),
				"W_argument_of_perihelion": float(arr[W_ARG_OF_PERIFOCUS].strip()),
				"longitude_of_perihelion": float(arr[OM_LONG_OF_ASCNODE].strip())+float(arr[W_ARG_OF_PERIFOCUS].strip()),

				"Tp_Time_of_perihelion_passage_JD": float(arr[TP_TIME_OF_PERIAPSIS].strip()),
				"N_mean_motion": float(arr[N_MEAN_MOTION].strip()),
				"MA_mean_anomaly": float(arr[MA_MEAN_ANOMALY].strip()),

				"epochJD": float(arr[JDTDB].strip()),

				"earth_moid": 0, #float(entry["orbital_data"]["minimum_orbit_intersection"]) * AU,
				"orbit_class": "N/A",
				"axial_tilt": 0.0,
				"utc": "", #utc_close_approach.strftime('%Y-%m-%d %H:%M:%S'),
				"local": "", #orbit3D.datetime_from_utc_to_local(utc_close_approach)

				"mass": 0.0,
				"radius": 0, #float(entry["estimated_diameter"]["kilometers"]["estimated_diameter_max"])*0.5, # if float(entry["estimated_diameter"]["kilometers"]["estimated_diameter_max"])/2 > DEFAULT_RADIUS else DEFAULT_RADIUS,
				"rotation": 0.0,
				"albedo": 0.0,
				"absolute_mag": 0 #float(entry["absolute_magnitude_h"]),
			}

			# CLose approach objects are considered as PHAs
			if 0:
				body = orbit3D.pha(self.SolarSystem, entry["neo_reference_id"], orbit3D.getColor())
				self.SolarSystem.addTo(body)
				return "" #entry["neo_reference_id"]

	def fetchJPL(self, param):
		query = self.url + param #+"\n"
		try:
			headers = {"Content-Type": "application/json; charset=utf-8"}

			self.response = requests.get(url = query, headers=headers) #, data = param)
			self.rawResp = self.response.text
			return True

			"""opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36')]
			print "REQUESTING:", query #self.url+"/"+target
			response = opener.open(query) #self.url+target)"""

		except requests.HTTPError as err:
		#except urllib2.HTTPError as err:
			print "Exception...\n\nError: " + str(err) #.code)+" - "+str(err.message)
			raise
			return False


test = JPLsearch()
#test.fetchElements(urllib.quote("toutatis"))
test.fetchElements(urllib.quote("C/2017 K2"))

# Example of output for an asteroid/comet (Ceres)

"""
*******************************************************************************
Ephemeris / WWW_USER Thu Jul  7 19:45:41 2022 Pasadena, USA      / Horizons
*******************************************************************************
Target body name: 1 Ceres (A801 AA)               {source: JPL#48}
Center body name: Sun (10)                        {source: DE441}
Center-site name: BODY CENTER
*******************************************************************************
Start time      : A.D. 2022-Jul-08 02:43:00.0000 TDB
Stop  time      : A.D. 2022-Jul-09 02:43:00.0000 TDB
Step-size       : 1440 minutes
*******************************************************************************
Center geodetic : 0.00000000,0.00000000,0.0000000 {E-lon(deg),Lat(deg),Alt(km)}
Center cylindric: 0.00000000,0.00000000,0.0000000 {E-lon(deg),Dxy(km),Dz(km)}
Center radii    : 696000.0 x 696000.0 x 696000.0 k{Equator, meridian, pole}    
Keplerian GM    : 1.3271244004127939E+11 km^3/s^2
Small perturbers: Yes                             {source: SB441-N16}
Output units    : KM-S, deg, Julian Day Number (Tp)
Output type     : GEOMETRIC osculating elements
Output format   : 10
Reference frame : Ecliptic of J2000.0
*******************************************************************************
Initial IAU76/J2000 heliocentric ecliptic osculating elements (au, days, deg.):
  EPOCH=  2458849.5 ! 2020-Jan-01.00 (TDB)         Residual RMS= .24563        
   EC= .07687465013145245  QR= 2.556401146697176   TP= 2458240.1791309435      
   OM= 80.3011901917491    W=  73.80896808746482   IN= 10.59127767086216       
  Equivalent ICRF heliocentric cartesian coordinates (au, au/d):
   X= 1.007608869613381E+00  Y=-2.390064275223502E+00  Z=-1.332124522752402E+00
  VX= 9.201724467227128E-03 VY= 3.370381135398406E-03 VZ=-2.850337057661093E-04
Asteroid physical parameters (km, seconds, rotational period in hours):        
   GM= 62.6284             RAD= 469.7              ROTPER= 9.07417             
   H= 3.33                 G= .120                 B-V= .713                   
                           ALBEDO= .090            STYP= C                     
*******************************************************************************
JDTDB
   EC    QR   IN
   OM    W    Tp
   N     MA   TA
   A     AD   PR
*******************************************************************************
$$SOE
2459768.613194444 = A.D. 2022-Jul-08 02:43:00.0000 TDB 
 EC= 7.860208007892644E-02 QR= 3.813312910696579E+08 IN= 1.058696125971198E+01
 OM= 8.026718420678449E+01 W = 7.354960528285878E+01 Tp=  2459920.441594440024
 N = 2.479109017019912E-06 MA= 3.274791129674673E+02 TA= 3.222086858597391E+02
 A = 4.138616799811341E+08 AD= 4.463920688926102E+08 PR= 1.452134607750122E+08
2459769.613194444 = A.D. 2022-Jul-09 02:43:00.0000 TDB 
 EC= 7.860317276002483E-02 QR= 3.813314220906712E+08 IN= 1.058695548303686E+01
 OM= 8.026716146345946E+01 W = 7.354894042174934E+01 Tp=  2459920.438798953779
 N = 2.479103329390212E-06 MA= 3.276939808831380E+02 TA= 3.224533078275508E+02
 A = 4.138623129764203E+08 AD= 4.463932038621694E+08 PR= 1.452137939278834E+08
$$EOE
*******************************************************************************
 
TIME

  Barycentric Dynamical Time ("TDB" or T_eph) output was requested. This
continuous relativistic coordinate time is equivalent to the relativistic
proper time of a clock at rest in a reference frame comoving with the
solar system barycenter but outside the system's gravity well. It is the
independent variable in the solar system relativistic equations of motion.

  TDB runs at a uniform rate of one SI second per second and is independent
of irregularities in Earth's rotation.

  Calendar dates prior to 1582-Oct-15 are in the Julian calendar system.
Later calendar dates are in the Gregorian system.

REFERENCE FRAME AND COORDINATES

  Ecliptic at the standard reference epoch

    Reference epoch: J2000.0
    X-Y plane: adopted Earth orbital plane at the reference epoch
               Note: IAU76 obliquity of 84381.448 arcseconds wrt ICRF X-Y plane
    X-axis   : ICRF
    Z-axis   : perpendicular to the X-Y plane in the directional (+ or -) sense
               of Earth's north pole at the reference epoch.

  Symbol meaning:

    JDTDB    Julian Day Number, Barycentric Dynamical Time
      EC     Eccentricity, e
      QR     Periapsis distance, q (km)
      IN     Inclination w.r.t X-Y plane, i (degrees)
      OM     Longitude of Ascending Node, OMEGA, (degrees)
      W      Argument of Perifocus, w (degrees)
      Tp     Time of periapsis (Julian Day Number)
      N      Mean motion, n (degrees/sec)
      MA     Mean anomaly, M (degrees)
      TA     True anomaly, nu (degrees)
      A      Semi-major axis, a (km)
      AD     Apoapsis distance (km)
      PR     Sidereal orbit period (sec)

ABERRATIONS AND CORRECTIONS

 Geometric osculating elements have NO corrections or aberrations applied.

Computations by ...

    Solar System Dynamics Group, Horizons On-Line Ephemeris System
    4800 Oak Grove Drive, Jet Propulsion Laboratory
    Pasadena, CA  91109   USA

    General site: https://ssd.jpl.nasa.gov/
    Mailing list: https://ssd.jpl.nasa.gov/email_list.html
    System news : https://ssd.jpl.nasa.gov/horizons/news.html
    User Guide  : https://ssd.jpl.nasa.gov/horizons/manual.html
    Connect     : browser        https://ssd.jpl.nasa.gov/horizons/app.html#/x
                  API            https://ssd-api.jpl.nasa.gov/doc/horizons.html
                  command-line   telnet ssd.jpl.nasa.gov 6775
                  e-mail/batch   https://ssd.jpl.nasa.gov/ftp/ssd/hrzn_batch.txt
                  scripts        https://ssd.jpl.nasa.gov/ftp/ssd/SCRIPTS
    Author      : Jon.D.Giorgini@jpl.nasa.gov
*******************************************************************************

!$$SOF
COMMAND = 'ceres'
CENTER = '@10'
MAKE_EPHEM = 'YES'
EPHEM_TYPE = ELEMENTS
REF_PLANE = 'ECLIPTIC'
START_TIME = '2022/07/08 02:43'
STOP_TIME = '2022/07/09 02:43'
STEP_SIZE = '24h'
OBJ_DATA = NO
FORMAT = 'json'

2459768.613194444 = A.D. 2022-Jul-08 02:43:00.0000 TDB 
 EC= 7.860208007892644E-02 QR= 3.813312910696579E+08 IN= 1.058696125971198E+01
 OM= 8.026718420678449E+01 W = 7.354960528285878E+01 Tp=  2459920.441594440024
 N = 2.479109017019912E-06 MA= 3.274791129674673E+02 TA= 3.222086858597391E+02
 A = 4.138616799811341E+08 AD= 4.463920688926102E+08 PR= 1.452134607750122E+08
2459769.613194444 = A.D. 2022-Jul-09 02:43:00.0000 TDB 
 EC= 7.860317276002483E-02 QR= 3.813314220906712E+08 IN= 1.058695548303686E+01
 OM= 8.026716146345946E+01 W = 7.354894042174934E+01 Tp=  2459920.438798953779
 N = 2.479103329390212E-06 MA= 3.276939808831380E+02 TA= 3.224533078275508E+02
 A = 4.138623129764203E+08 AD= 4.463932038621694E+08 PR= 1.452137939278834E+08
"""

# example of output for spacecraft (spaceX Roadster)
"""
*******************************************************************************
Ephemeris / WWW_USER Thu Jul  7 19:51:52 2022 Pasadena, USA      / Horizons
*******************************************************************************
Target body name: SpaceX Roadster (spacecraft) (-143205) {source: tesla_s10}
Center body name: Sun (10)                        {source: DE441}
Center-site name: BODY CENTER
*******************************************************************************
Start time      : A.D. 2022-Jul-08 02:49:00.0000 TDB
Stop  time      : A.D. 2022-Jul-09 02:49:00.0000 TDB
Step-size       : 1440 minutes
*******************************************************************************
Center geodetic : 0.00000000,0.00000000,0.0000000 {E-lon(deg),Lat(deg),Alt(km)}
Center cylindric: 0.00000000,0.00000000,0.0000000 {E-lon(deg),Dxy(km),Dz(km)}
Center radii    : 696000.0 x 696000.0 x 696000.0 k{Equator, meridian, pole}    
Keplerian GM    : 1.3271244004127939E+11 km^3/s^2
Output units    : KM-S, deg, Julian Day Number (Tp)
Output type     : GEOMETRIC osculating elements
Output format   : 10
Reference frame : Ecliptic of J2000.0
*******************************************************************************
JDTDB
   EC    QR   IN
   OM    W    Tp
   N     MA   TA
   A     AD   PR
*******************************************************************************
$$SOE
2459768.617361111 = A.D. 2022-Jul-08 02:49:00.0000 TDB 
 EC= 2.559078309823242E-01 QR= 1.475078137041219E+08 IN= 1.075237582593092E+00
 OM= 3.169157192069072E+02 W = 1.777528640879490E+02 Tp=  2459824.944346193224
 N = 7.478181666653130E-06 MA= 3.236062958917581E+02 TA= 3.009101780825709E+02
 A = 1.982386320485760E+08 AD= 2.489694503930301E+08 PR= 4.814004473912687E+07
2459769.617361111 = A.D. 2022-Jul-09 02:49:00.0000 TDB 
 EC= 2.559079642829365E-01 QR= 1.475077962049002E+08 IN= 1.075237675909757E+00
 OM= 3.169157102835372E+02 W = 1.777528949181755E+02 Tp=  2459824.944358906243
 N = 7.478180987864605E-06 MA= 3.242524058183188E+02 TA= 3.018286041467213E+02
 A = 1.982386440445509E+08 AD= 2.489694918842016E+08 PR= 4.814004910876034E+07
$$EOE
*******************************************************************************
 
TIME

  Barycentric Dynamical Time ("TDB" or T_eph) output was requested. This
continuous relativistic coordinate time is equivalent to the relativistic
proper time of a clock at rest in a reference frame comoving with the
solar system barycenter but outside the system's gravity well. It is the
independent variable in the solar system relativistic equations of motion.

  TDB runs at a uniform rate of one SI second per second and is independent
of irregularities in Earth's rotation.

  Calendar dates prior to 1582-Oct-15 are in the Julian calendar system.
Later calendar dates are in the Gregorian system.

REFERENCE FRAME AND COORDINATES

  Ecliptic at the standard reference epoch

    Reference epoch: J2000.0
    X-Y plane: adopted Earth orbital plane at the reference epoch
               Note: IAU76 obliquity of 84381.448 arcseconds wrt ICRF X-Y plane
    X-axis   : ICRF
    Z-axis   : perpendicular to the X-Y plane in the directional (+ or -) sense
               of Earth's north pole at the reference epoch.

  Symbol meaning:

    JDTDB    Julian Day Number, Barycentric Dynamical Time
      EC     Eccentricity, e
      QR     Periapsis distance, q (km)
      IN     Inclination w.r.t X-Y plane, i (degrees)
      OM     Longitude of Ascending Node, OMEGA, (degrees)
      W      Argument of Perifocus, w (degrees)
      Tp     Time of periapsis (Julian Day Number)
      N      Mean motion, n (degrees/sec)
      MA     Mean anomaly, M (degrees)
      TA     True anomaly, nu (degrees)
      A      Semi-major axis, a (km)
      AD     Apoapsis distance (km)
      PR     Sidereal orbit period (sec)

ABERRATIONS AND CORRECTIONS

 Geometric osculating elements have NO corrections or aberrations applied.

Computations by ...

    Solar System Dynamics Group, Horizons On-Line Ephemeris System
    4800 Oak Grove Drive, Jet Propulsion Laboratory
    Pasadena, CA  91109   USA

    General site: https://ssd.jpl.nasa.gov/
    Mailing list: https://ssd.jpl.nasa.gov/email_list.html
    System news : https://ssd.jpl.nasa.gov/horizons/news.html
    User Guide  : https://ssd.jpl.nasa.gov/horizons/manual.html
    Connect     : browser        https://ssd.jpl.nasa.gov/horizons/app.html#/x
                  API            https://ssd-api.jpl.nasa.gov/doc/horizons.html
                  command-line   telnet ssd.jpl.nasa.gov 6775
                  e-mail/batch   https://ssd.jpl.nasa.gov/ftp/ssd/hrzn_batch.txt
                  scripts        https://ssd.jpl.nasa.gov/ftp/ssd/SCRIPTS
    Author      : Jon.D.Giorgini@jpl.nasa.gov
*******************************************************************************

!$$SOF
COMMAND = '-143205'
CENTER = '@10'
MAKE_EPHEM = 'YES'
EPHEM_TYPE = ELEMENTS
REF_PLANE = 'ECLIPTIC'
START_TIME = '2022/07/08 02:49'
STOP_TIME = '2022/07/09 02:49'
STEP_SIZE = '24h'
OBJ_DATA = NO
FORMAT = 'json'

2459768.617361111 = A.D. 2022-Jul-08 02:49:00.0000 TDB 
 EC= 2.559078309823242E-01 QR= 1.475078137041219E+08 IN= 1.075237582593092E+00
 OM= 3.169157192069072E+02 W = 1.777528640879490E+02 Tp=  2459824.944346193224
 N = 7.478181666653130E-06 MA= 3.236062958917581E+02 TA= 3.009101780825709E+02
 A = 1.982386320485760E+08 AD= 2.489694503930301E+08 PR= 4.814004473912687E+07
2459769.617361111 = A.D. 2022-Jul-09 02:49:00.0000 TDB 
 EC= 2.559079642829365E-01 QR= 1.475077962049002E+08 IN= 1.075237675909757E+00
 OM= 3.169157102835372E+02 W = 1.777528949181755E+02 Tp=  2459824.944358906243
 N = 7.478180987864605E-06 MA= 3.242524058183188E+02 TA= 3.018286041467213E+02
 A = 1.982386440445509E+08 AD= 2.489694918842016E+08 PR= 4.814004910876034E+07


"""