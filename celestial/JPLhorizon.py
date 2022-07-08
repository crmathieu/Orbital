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

"""

$$SOE
2459767.534722222 = A.D. 2022-Jul-07 00:50:00.0000 TDB
 EC= 2.559076897709205E-01 QR= 1.475078327856763E+08 IN= 1.075237495470156E+00
 OM= 3.169157278732415E+02 W = 1.777528318988781E+02 Tp=  2459824.944332684390
 N = 7.478182344368642E-06 MA= 3.229067921452925E+02 TA= 2.999222558594676E+02
 A = 1.982386200715660E+08 AD= 2.489694073574556E+08 PR= 4.814004037640160E+07
2459768.534722222 = A.D. 2022-Jul-08 00:50:00.0000 TDB
 EC= 2.559078200773128E-01 QR= 1.475078151558300E+08 IN= 1.075237575446454E+00
 OM= 3.169157199046895E+02 W = 1.777528615887452E+02 Tp=  2459824.944345153868
 N = 7.478181720651845E-06 MA= 3.235529020827688E+02 TA= 3.008345343639385E+02
 A = 1.982386310942771E+08 AD= 2.489694470327241E+08 PR= 4.814004439151556E+07
$$EOE

RESPONSE COLUMN MEANING:
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

zob ="https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&COMMAND='2022 JO1'&CENTER='@10'&START_TIME='2022-05-09'&STOP_TIME='2022-05-10'&MAKE_EPHEM=YES&EPHEM_TYPE=ELEMENTS"

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


#QHEADER = "/horizons_batch.cgi?format=json&batch=1&COMMAND="
#QHEADER = "!$$SOF\nCOMMAND="
QHEADER = "?batch=1&COMMAND="

#%2750000001%27
QCENTER = "&CENTER='@10'&MAKE_EPHEM='YES'&EPHEM_TYPE=ELEMENTS&REF_PLANE='ECLIPTIC'"
QSTART = "&START_TIME="
#%272021/5/7%2015:52%27
QSTOP = "&STOP_TIME="
#%272021/5/6%2016:52%27
QSTEP = "&STEP_SIZE="  # 1h, 6h, ...
#%271h%27
QQUANTITIES = "" #"&QUANTITIES=%271,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46%27&FIXED_QUANTITIES=%27A%27"
QTRAILER = "&OBJ_DATA=NO&FORMAT='json'"#&TIME_TYPE=UTC" #"&REF_SYSTEM='J2000'&OUT_UNITS=%27KM-S%27&VECT_TABLE=%273%27&VECT_CORR=%27NONE%27&CAL_FORMAT=%27CAL%27&ANG_FORMAT=%27DEG%27&APPARENT=%27AIRLESS%27&TIME_TYPE=%27UTC%27&TIME_DIGITS=%27MINUTES%27&RANGE_UNITS=%27AU%27&SUPPRESS_RANGE_RATE=%27no%27&SKIP_DAYLT=%27no%27&EXTRA_PREC=%27yes%27&CSV_FORMAT=%27yes%27&VEC_LABELS=%27yes%27&ELM_LABELS=%27yes%27&TP_TYPE=%27ABSOLUTE%27&R_T_S_ONLY=%27NO%27&CA_TABLE_TYPE=%27STANDARD%27"




I_QHEADER = "batch=1&COMMAND="
#%2750000001%27
I_QCENTER = "&CENTER='@10'&MAKE_EPHEM=yes&EPHEM_TYPE=APPROACH&REF_PLANE=%27ECLIPTIC%27"
I_QSTART = "&START_TIME="
#%272021/5/7%2015:52%27
I_QSTOP = "&STOP_TIME="
#%272021/5/6%2016:52%27
I_QSTEP = "&STEP_SIZE="  # 1h, 6h, ...
#%271h%27
I_QQUANTITIES = "" #"&QUANTITIES=%271,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46%27&FIXED_QUANTITIES=%27A%27"
I_QTRAILER = "&OBJ_DATA=YES&FORMAT='json'&TIME_TYPE=UTC" #"&REF_SYSTEM='J2000'&OUT_UNITS=%27KM-S%27&VECT_TABLE=%273%27&VECT_CORR=%27NONE%27&CAL_FORMAT=%27CAL%27&ANG_FORMAT=%27DEG%27&APPARENT=%27AIRLESS%27&TIME_TYPE=%27UTC%27&TIME_DIGITS=%27MINUTES%27&RANGE_UNITS=%27AU%27&SUPPRESS_RANGE_RATE=%27no%27&SKIP_DAYLT=%27no%27&EXTRA_PREC=%27yes%27&CSV_FORMAT=%27yes%27&VEC_LABELS=%27yes%27&ELM_LABELS=%27yes%27&TP_TYPE=%27ABSOLUTE%27&R_T_S_ONLY=%27NO%27&CA_TABLE_TYPE=%27STANDARD%27"


"""
   GM= 62.6284             RAD= 469.7              ROTPER= 9.07417             
   H= 3.53                 G= .120                 B-V= .713                   
                           ALBEDO= .090            STYP= C                     
"""

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
	url = "https://ssd.jpl.nasa.gov/horizons_batch.cgi"

	#url = "https://ssd-api.jpl.nasa.gov/sbdb.api?des="

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

	def fetchElements(self, target):
		startdate = datetime.utcnow().strftime('%Y/%m/%d %H:%M')
		enddate = (datetime.utcnow()+timedelta(days=1)).strftime('%Y/%m/%d %H:%M')
		par = self.urlBuilder(target, startdate, enddate, "24h")
		print "TARGET=", self.url+par
		#exit(-1)
		self.fetchJPL(par, target)
		#self.fetchJPL(target) #urllib.urlencode(target))

	def urlBuilder(self, targetid, starttime, endtime, step):
		return QHEADER+"'"+targetid+"'"+QCENTER+QSTART+"'"+starttime+"'"+QSTOP+"'"+endtime+"'"+QSTEP+"'"+step+"'"+QTRAILER

	def extractParams(self, target):
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


	def fetchJPL(self, param, target):
		#url = url+"&start_date="+self.fetchDateStr
		query = self.url + param+"\n"
		#query = zob
		try:
			headers = {"Content-Type": "application/json; charset=utf-8"}

			self.response = requests.get(url = query, headers=headers) #, data = param)
			self.rawResp = self.response.text

			"""opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36')]
			print "REQUESTING:", query #self.url+"/"+target
			response = opener.open(query) #self.url+target)"""

		except requests.HTTPError as err:
		#except urllib2.HTTPError as err:
			print "Exception...\n\nError: " + str(err) #.code)+" - "+str(err.message)
			raise
			return

#

		# parse response using start and end markers
		print self.rawResp	
		name = ""
		nameMarker = "Target body name:" 
		nameStart = self.rawResp.find(nameMarker, 0, len(self.rawResp))
		if nameStart != -1:
			nameStart = nameStart + len(nameMarker) + 1
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

		print "Extracting ", name
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
				2459767.547222222 = A.D. 2022-Jul-07 01:08:00.0000 TDB
				 EC= 2.559076913790752E-01 QR= 1.475078325645969E+08 IN= 1.075237496397935E+00
				 OM= 3.169157277789936E+02 W = 1.777528322639769E+02 Tp=  2459824.944332839455
				 N = 7.478182336937578E-06 MA= 3.229148685189527E+02 TA= 2.999336242914953E+02
				 A = 1.982386202028923E+08 AD= 2.489694078411878E+08 PR= 4.814004042423832E+07	

				 0- epoch
				 1->4 elements  			
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

				epoch, IN, EC, QR, QM, W, TP, N, MA, TA, A, AD, PR = "", "", "", "", "", "", "", "", "", "", "", "", ""
				while len(rec) > 0:
					# break down in tokens
					arr = rec.split(" ")
					print arr
					if k == 0:
						elements[JDTDB] = arr[0]
						elements[DATETIME] = arr[3] +" "+arr[4]
					elif k == 1:
						elements[EC_ECCENTRICITY] = arr[2]
						elements[QR_PERIAPSIS] =arr[4] 
						elements[IN_INCLINATION] =arr[6][:-1]
					elif k == 2:
						elements[OM_LONG_OF_ASCNODE] = arr[2]
						elements[W_ARG_OF_PERIFOCUS] =arr[5]
						elements[TP_TIME_OF_PERIAPSIS] =arr[8][:-1]
					elif k == 3:
						elements[N_MEAN_MOTION] = arr[3]
						elements[MA_MEAN_ANOMALY] =arr[5]
						elements[TA_TRUE_ANOMALY] =arr[7][:-1]
					elif k == 4:
						elements[A_SEMI_MAJOR] = arr[3]
						elements[AD_APOAPSIS] =arr[5]
						elements[PR_SIDERAL_ORBIT] =arr[7][:-1]
					else:
						break
					k += 1


					"""print arr
					if len(arr) > 1:
						print arr[DATETIME].strip(), arr[JDTDB].strip(), arr[EC_ECCENTRICITY].strip()
						# load the elements and bail
						self.loadBodyInfo(target, "zob", arr)
						break
					"""
					rec = line.readline()
				print "----------"
				print elements
				self.loadBodyInfo(target, name, elements)

				"""
				using the target criteria -143205, I am getting
				{
					"-143205":{
						"epochJD":2459767.601388889,
						"Tp_Time_of_perihelion_passage_JD":2459824.944333511,
						"radius":0,
						"albedo":0.0,
						"orbit_class":"N/A",
						"iau_name":"SpaceX Roadster (spacecraft) (-143205) {source: tesla_s10}",
						"W_argument_of_perihelion":177.7528338477557,
						"earth_moid":0,
						"local":"",
						"profile":"",
						"IN_orbital_inclination":1.075237500438736,
						"material":0,
						"N_mean_motion":7.478182304622464e-06,
						"jpl_designation":"-143205",
						"EC_e":0.2559076983542581,
						"rotation":0.0,
						"QR_perihelion":147507831.6067919,
						"utc":"",
						"name":"SpaceX Roadster (spacecraft) (-143205) {source: tesla_s10}",
						"longitude_of_perihelion":494.6685612167926,
						"OM_longitude_of_ascendingnode":316.9157273690369,
						"absolute_mag":0,
						"mass":0.0,
						"axial_tilt":0.0,
						"MA_mean_anomaly":322.9498661383985,
						"PR_revolution":48140040.63226359
					}
				}
				"""

		"""rawResp = response.read()
		self.jsonResp = json.loads(rawResp)
		print self.jsonResp
		return
		"""

		# parse response using start and end markers

		# next try to grab mass, radius and other info
		self.extractParams(target)
		print ("PARSED results ...")
		print objects_data #[target]

	def fetchJPLSAVE(self, param, target):
		#url = url+"&start_date="+self.fetchDateStr
		query = self.url + param+"\n"
		#query = zob
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36')]
			print "REQUESTING:", query #self.url+"/"+target
			response = opener.open(query) #self.url+target)

		except urllib2.HTTPError as err:
			print "Exception...\n\nError: " + str(err) #.code)+" - "+str(err.message)
			raise
#
		rawResp = response.read()
		self.jsonResp = json.loads(rawResp)
		print self.jsonResp
		return




		# parse response using start and end markers
		start = self.rawResp.find(self.startMarker, 0, len(self.rawResp))
		if start != -1:
			# then find end marker
			end = self.rawResp.find(self.endMarker, start+len(self.startMarker), len(self.rawResp))
			if end != -1:
				cvs = self.rawResp[start:end]
				# read line by line
				line = StringIO.StringIO(cvs)
				rec = line.readline()

				while len(rec) > 0:
					# break down in tokens
					arr = rec.split(",")
					if len(arr) > 1:
						#print arr[DATETIME].strip(), arr[JDTDB].strip(), arr[EC_ECCENTRICITY].strip()
						# load the elements and bail
						self.loadBodyInfo(target, "zob", arr)
						break

					rec = line.readline()

		# next try to grab mass, radius and other info
		self.extractParams(target)
		print ("PARSED results ...")
		print objects_data[target]

		#print rawResp
		"""
		self.jsonResp = json.loads(rawResp)

		# use if "prev" not in "links"  
		self.nextUrl = self.jsonResp["links"]["next"] if "next" in self.jsonResp["links"] else ""
		self.prevUrl = self.jsonResp["links"]["prev"] if "prev" in self.jsonResp["links"] else ""
		self.selfUrl = self.jsonResp["links"]["self"] if "self" in self.jsonResp["links"] else ""

		if self.ListIndex != 0:
			self.list.DeleteAllItems()

			#print "*****PREV "+self.prevUrl
			#print "*****CURR "+self.selfUrl
			#print "*****NEXT "+self.nextUrl

		self.ListIndex = 0
		if self.jsonResp["element_count"] > 0:
	#			for i in range(0, len(self.jsonResp[self.fetchDateStr])-1):
			today = self.jsonResp["near_earth_objects"][self.fetchDateStr]
			for entry in today:
				if entry["close_approach_data"][0]["orbiting_body"].upper() == 'EARTH':
					self.list.InsertStringItem(self.ListIndex, entry["name"])
					if entry["is_potentially_hazardous_asteroid"] == True:
							ch = "Y"
					else:
							ch = "N"
					self.list.SetStringItem(self.ListIndex, 1, ch)
					self.list.SetStringItem(self.ListIndex, 2, entry["neo_reference_id"])
					self.list.SetStringItem(self.ListIndex, 3, str(round(float(entry["close_approach_data"][0]["miss_distance"]["lunar"]) * 100)/100)  +
											" LD | " + str(round(float(entry["close_approach_data"][0]["miss_distance"]["astronomical"]) * 100)/100) + " AU ")
					#self.list.SetStringItem(self.ListIndex, 3, entry["close_approach_data"][0]["miss_distance"]["astronomical"] + " AU ")
					# record the spk-id corresponding to this row
					self.BodiesSPK_ID.append(entry["neo_reference_id"])
					self.ListIndex += 1
		"""

	"""
	{
	'epochJD': 2459348.379861111, 
	'Tp_Time_of_perihelion_passage_JD': 2452040.574368465, 
	'radius': 0, 
	'orbit_class': 'N/A', 
	'iau_name': 'zob', 
	'W_argument_of_perihelion': 344.4660478781688, 
	'earth_moid': 0, 
	'local': '', 
	'IN_orbital_inclination': 19.11981139500138, 
	'material': 0, 
	'N_mean_motion': 1.747915814771269e-07, 
	'jpl_designation': 'CINEOS', 
	'EC_e': 0.2721601205693517, 
	'QR_perihelion': 1764985489.805037, 
	'utc': '', 
	'name': 'zob', 
	'longitude_of_perihelion': 640.126840223674, 
	'OM_longitude_of_ascendingnode': 295.6607923455051, 
	'absolute_mag': 0, 
	'mass': 0.0, 
	'axial_tilt': 0.0, 
	'MA_mean_anomaly': 110.3624247617465, 
	'PR_revolution': 2059595759.462302}
	"""	
	def loadBodyInfo(self, target, name, arr): # name, arr):
			#entry = self.jsonResp["near_earth_objects"][self.fetchDateStr][index]
			#utc_close_approach = datetime.datetime.utcfromtimestamp(entry["close_approach_data"][0]["epoch_date_close_approach"]*0.001)
			#print "**** ", utc_close_approach

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
			"""
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

			"""			
			# otherwise add data to dictionary
			objects_data[entry["neo_reference_id"]] = {
				"material": 0,
				# epoch_date_close_approach comes as the number of milliseconds in unix TT
				"epoch_date_close_approach": utc_close_approach, # in seconds using J2000
				"name": entry["name"],
				"iau_name": entry["name"],
				"jpl_designation": entry["neo_reference_id"],
				"mass": 0.0,
				"radius": float(entry["estimated_diameter"]["kilometers"]["estimated_diameter_max"])*0.5, # if float(entry["estimated_diameter"]["kilometers"]["estimated_diameter_max"])/2 > DEFAULT_RADIUS else DEFAULT_RADIUS,
				"QR_perihelion": float(entry["orbital_data"]["perihelion_distance"]) * AU,
				"EC_e": float(entry["orbital_data"]["eccentricity"]),
				"PR_revolution": float(entry["orbital_data"]["orbital_period"]),
				"IN_orbital_inclination": float(entry["orbital_data"]["inclination"]),
				"OM_longitude_of_ascendingnode":float(entry["orbital_data"]["ascending_node_longitude"]),
				"W_argument_of_perihelion": float(entry["orbital_data"]["perihelion_argument"]),
				"longitude_of_perihelion": float(entry["orbital_data"]["ascending_node_longitude"])+float(entry["orbital_data"]["perihelion_argument"]),
				"Tp_Time_of_perihelion_passage_JD": float(entry["orbital_data"]["perihelion_time"]),
				"N_mean_motion": float(entry["orbital_data"]["mean_motion"]),
				"MA_mean_anomaly": float(entry["orbital_data"]["mean_anomaly"]),
				"epochJD": float(entry["orbital_data"]["epoch_osculation"]),
				"earth_moid": float(entry["orbital_data"]["minimum_orbit_intersection"]) * AU,
				"orbit_class": "N/A",
				"absolute_mag": float(entry["absolute_magnitude_h"]),
				"axial_tilt": 0.0,
				"utc": utc_close_approach.strftime('%Y-%m-%d %H:%M:%S'),
				"local": orbit3D.datetime_from_utc_to_local(utc_close_approach)
			}
			print objects_data[entry["neo_reference_id"]]
			# print time of closest approach on this date
			#utc = datetime.datetime.utcfromtimestamp(objects_data[entry["neo_reference_id"]]["epoch_date_close_approach"])
			print "Local Time of approach: ", orbit3D.datetime_from_utc_to_local(utc_close_approach).strftime('%Y-%m-%d %H:%M:%S')
			"""

			# CLose approach objects are considered as PHAs
			if 0:
				body = orbit3D.pha(self.SolarSystem, entry["neo_reference_id"], orbit3D.getColor())
				self.SolarSystem.addTo(body)
				return "" #entry["neo_reference_id"]
			

test = JPLsearch()
#test.fetchJPL(urllib.quote_plus("-226")) #"2022 JO1")) #167P") #"CINEOS") #target_name_pairs['SpaceX Roadster (spacecraft) (Tesla)'])
test.fetchElements(urllib.quote("-143205")) #167P") #"CINEOS") #target_name_pairs['SpaceX Roadster (spacecraft) (Tesla)'])

"""
#%272021/5/6%2016:52%27
#strftime('%Y/%m/%d %H:%M')

Ceres


*******************************************************************************
Ephemeris / WWW_USER Wed May 12 19:18:14 2021 Pasadena, USA      / Horizons
*******************************************************************************
Target body name: 1 Ceres (A801 AA)               {source: JPL#48}
Center body name: Sun (10)                        {source: DE441}
Center-site name: BODY CENTER
*******************************************************************************
Start time      : A.D. 2021-May-12 00:00:00.0000 TDB
Stop  time      : A.D. 2021-May-13 00:00:00.0000 TDB
Step-size       : 1440 minutes
*******************************************************************************
Center geodetic : 0.00000000,0.00000000,0.0000000 {E-lon(deg),Lat(deg),Alt(km)}
Center cylindric: 0.00000000,0.00000000,0.0000000 {E-lon(deg),Dxy(km),Dz(km)}
Center radii    : 696000.0 x 696000.0 x 696000.0 k{Equator, meridian, pole}    
Keplerian GM    : 2.9591220828411951E-04 au^3/d^2
Small perturbers: Yes                             {source: SB441-N16}
Output units    : AU-D, deg, Julian Day Number (Tp)
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
   H= 3.53                 G= .120                 B-V= .713                   
                           ALBEDO= .090            STYP= C                     
*******************************************************************************
            JDTDB,            Calendar Date (TDB),                     EC,                     QR,                     IN,                     OM,                      W,                     Tp,                      N,                     MA,                     TA,                      A,                     AD,                     PR,
**************************************************************************************************************************************************************************************************************************************************************************************************************************************************
$$SOE
2459346.500000000, A.D. 2021-May-12 00:00:00.0000,  7.835625869929473E-02,  2.548987913935589E+00,  1.058813053097302E+01,  8.026809558859739E+01,  7.373854686023802E+01,  2.459921283101395E+06,  2.142875931065045E-01,  2.368311126437671E+02,  2.297163483409848E+02,  2.765697633163799E+00,  2.982407352392010E+00,  1.679985270174154E+03,
2459347.500000000, A.D. 2021-May-13 00:00:00.0000,  7.835717731756708E-02,  2.548983965981054E+00,  1.058813209326461E+01,  8.026808276834797E+01,  7.373862547057266E+01,  2.459921282559822E+06,  2.142877705738566E-01,  2.370454144614690E+02,  2.299112411599143E+02,  2.765696106179463E+00,  2.982408246377873E+00,  1.679983878855663E+03,
$$EOE
**************************************************************************************************************************************************************************************************************************************************************************************************************************************************



starman

*******************************************************************************
Ephemeris / WWW_USER Wed May 12 19:19:34 2021 Pasadena, USA      / Horizons
*******************************************************************************
Target body name: SpaceX Roadster (spacecraft) (-143205) {source: tesla_s10}
Center body name: Sun (10)                        {source: DE441}
Center-site name: BODY CENTER
*******************************************************************************
Start time      : A.D. 2021-May-12 00:00:00.0000 TDB
Stop  time      : A.D. 2021-May-13 00:00:00.0000 TDB
Step-size       : 1440 minutes
*******************************************************************************
Center geodetic : 0.00000000,0.00000000,0.0000000 {E-lon(deg),Lat(deg),Alt(km)}
Center cylindric: 0.00000000,0.00000000,0.0000000 {E-lon(deg),Dxy(km),Dz(km)}
Center radii    : 696000.0 x 696000.0 x 696000.0 k{Equator, meridian, pole}    
Keplerian GM    : 2.9591220828411951E-04 au^3/d^2
Output units    : AU-D, deg, Julian Day Number (Tp)
Output type     : GEOMETRIC osculating elements
Output format   : 10
Reference frame : Ecliptic of J2000.0
*******************************************************************************
            JDTDB,            Calendar Date (TDB),                     EC,                     QR,                     IN,                     OM,                      W,                     Tp,                      N,                     MA,                     TA,                      A,                     AD,                     PR,
**************************************************************************************************************************************************************************************************************************************************************************************************************************************************
$$SOE
2459346.500000000, A.D. 2021-May-12 00:00:00.0000,  2.560839269681681E-01,  9.857751516999831E-01,  1.075786481433761E+00,  3.169259658258604E+02,  1.776850687558298E+02,  2.459267630209804E+06,  6.461348815193358E-01,  5.096052254412366E+01,  7.833221141463902E+01,  1.325116081552659E+00,  1.664457011405336E+00,  5.571592097821557E+02,
2459347.500000000, A.D. 2021-May-13 00:00:00.0000,  2.560838851147686E-01,  9.857756202803387E-01,  1.075786262010161E+00,  3.169259174832307E+02,  1.776852248463027E+02,  2.459267630289985E+06,  6.461344753451885E-01,  5.160657317655494E+01,  7.912085085130785E+01,  1.325116636883743E+00,  1.664457653487148E+00,  5.571595600245209E+02,
$$EOE
**************************************************************************************************************************************************************************************************************************************************************************************************************************************************
"""