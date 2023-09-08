#from scipy.sparse.csgraph import _validation
import urllib2
#import httplib
#import re
import json
#import sys
import math
from planetsdata import EARTH_PERIOD
import pytz
import datetime as dt
import time
from orbit3D import deg2rad
from dateutil.relativedelta import relativedelta

"""
EarthLocations - time management of earth locations

"""

class locList:
	TZ_YOUR_LOCATION = 0
	TZ_US_VANCOUVER = 0
	TZ_LOCAL = 0
	TZ_UTC = TZ_LOCAL+1
	TZ_EG_CAIRO = TZ_UTC+1
	TZ_FR_PARIS = TZ_EG_CAIRO+1
	TZ_FR_KOUR = TZ_FR_PARIS+1
	TZ_ICE_REK = TZ_FR_KOUR+1
	TZ_AUS_SYD = TZ_ICE_REK+1
	TZ_CHL_SAN = TZ_AUS_SYD+1
	TZ_US_HONO = TZ_CHL_SAN+1

	# spaceports start here
	TZ_US_CAPE = TZ_US_HONO+1
	TZ_US_KOD = TZ_US_CAPE+1
	TZ_US_WAL = TZ_US_KOD+1
	TZ_US_VDBERG = TZ_US_WAL+1
	TZ_RUS_BAIK = TZ_US_VDBERG+1
	TZ_IND_THI = TZ_RUS_BAIK+1
	TZ_NZ_MAH = TZ_IND_THI+1
	TZ_JP_TAN = TZ_NZ_MAH+1
	TZ_CHN_HONG = TZ_JP_TAN+1
	TZ_CHN_XI = TZ_CHN_HONG+1
	TZ_CHN_WE = TZ_CHN_XI+1
	TZ_CHN_JIU = TZ_CHN_WE+1
	TZ_CHN_TAI = TZ_CHN_JIU+1
	TZ_CHN_JIN = TZ_CHN_TAI+1

	# geo locations
	TZ_NORTH_P = TZ_CHN_JIN+1
	TZ_SOUTH_P = TZ_NORTH_P+1
	TZ_EQUANT = TZ_SOUTH_P+1

class EarthLocations:
	
	# among all earth locations, the current location (where the program is launched)
	# will always reside @ offset 0. Beside its own index zero in the tzEarhLocations 
	# table, we use additional info based on the current location to properly position 
	# the earth's texture. (see the document "data/texture-positioning.png"). If the
	# service on http://ipinfo.io/json isn't responding, we use Vancouver, WA as the 
	# default location 

	tzEarthLocations = [
    { # LOCAL or VANCOUVER
        "tzname": "America/Los_Angeles",
        "lat": 45.6418,
        "long": -122.6801,
        "name": "Vancouver-US",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
    { # UTC
        "tzname": "Africa/Abidjan",
        "lat": 51.4934,
        "long": 0.0098,
        "name": "Greenwich-UK",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
    { # CAIRO
        "tzname": "Africa/Cairo",
        "lat": 30.0444,
        "long": 31.2357,
        "name": "Cairo-EG",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
    { # PARIS
        "tzname": "Europe/Paris",
        "lat": 48.8566,
        "long": 2.3522,
        "name": "Paris-FR",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
 	{ # Kourou
        "tzname": "America/Guyana",
        "lat": 5.1611,
        "long": -52.6493,
        "name": "Kourou Spaceport-FR",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
    { # Reykjavik
        "tzname": "Iceland",
        "lat": 64.1466,
        "long": -21.9426,
        "name": "Reykjavik-ICE",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
    { # Sydney
        "tzname": "Australia/Sydney",
        "lat": -33.8688,
        "long": 151.2093,
        "name": "Sydney-AUS",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
    { # Santiago
        "tzname": "America/Santiago",
        "lat": -33.4489,
        "long": -70.6693,
        "name": "Santiago-CHI",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
    { # Hawaii
        "tzname": "Pacific/Honolulu",
        "lat": 19.8968,
        "long": -155.5828,
        "name": "Honolulu-US",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
	{ # Cape
        "tzname": "America/New_York",
        "lat": 28.40584, # 28.3922,
        "long":  -80.6077,
        "name": "Cape Canaveral-US",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
	{ # Kodiac
        "tzname": "America/Juneau",
        "lat": 57.433,
        "long": -152.33,
        "name": "Kodiak Spaceport-US",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
	{ # Wallops
        "tzname": "America/New_York",
        "lat": 37.85,
        "long": -75.46667,
        "name": "Wallops Spaceport-US",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
	{ # Vandenberg
        "tzname": "America/Los_Angeles",
        "lat": 34.7420,
        "long": -120.5724,
        "name": "Vandenberg AF Base-US",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
 	{ # Baikonur
        "tzname": "Asia/Oral",
        "lat": 45.6232,
        "long": 63.3140,
        "name": "Baikonur Cosmodrome-RUS",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
	{ # India
        "tzname": "Asia/Kolkata",
        "lat": 8.5241,
        "long": 76.9366,
        "name": "Thiruvananthapuram-IND",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
	{ # New Zealand
        "tzname": "Pacific/Auckland",
        "lat": -39.0806,
        "long": 177.8749,
        "name": "Mahia Spaceport-NZL",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
	{ # Japan
        "tzname": "Japan",
        "lat": 30.3999984,
        "long": 130.968662792,
        "name": "Tanegashima Spaceport-JPN",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
    { # Honk kong
        "tzname": "Hongkong",
        "lat": 22.3193,
        "long": 114.1694,
        "name": "Hong Kong-CHN",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
	{ # Xichang
        "tzname": "Asia/Shanghai",
        "lat": 27.8945,
        "long": 102.2631,
        "name": "Xichang Spaceport-CHN",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
	{ # Wenchang
        "tzname": "Asia/Chungking",
        "lat": 19.614492,
        "long": 110.951133,
        "name": "Wenchang Spaceport-CHN",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
	{ # Jiuquan
        "tzname": "Asia/Shanghai",
        "lat": 40.95,
        "long": 100.2833,
        "name": "Jiuquan Spaceport-CHN",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
	{ # Taiyuan
        "tzname": "Asia/Chungking",
        "lat": 38.83,
        "long": 111.6,
        "name": "Taiyuan Spaceport-CHN",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
	{ # Jingyu
        "tzname": "Asia/Chungking",
        "lat": 42.0,
        "long": 126.5,
        "name": "Jingyu Spaceport-CHN",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
	{ # NP
        "tzname": "Africa/Abidjan",
        "lat": 90,
        "long": -135,
        "name": "North Pole",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
	{ # SP
        "tzname": "Africa/Abidjan",
        "lat": -90,
        "long": 45,
        "name": "South Pole",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
	{ # Date line
        "tzname": "Pacific/Kwajalein",
        "lat": 0,
        "long": 180,
        "name": "Inter. Date Line",
		"dst": False,
		"localDatetime": None,
		"AbsoluteTimeDiffInSec": 0
    },
]


	def __init__(self, index = -1):
		self.Locations = []
		self.locationOfInterest = 0
		self.loadAllLocations()
		self.setLocal2UTCdiff()
		self.InitGeometryData()
		#self.Psi = 0.0

	# changes the index locationOfInterest value. locationOfInterest always points to
	# the location that is displayed as the "local" date & time 
	def setLocationOfInterest(self, index):
		if index >= 0 and index < len(self.tzEarthLocations):
			self.locationOfInterest = index

	def getLocationOfInterestName(self):
		return self.tzEarthLocations[self.locationOfInterest]["name"]
		
	def loadAllLocations(self):

		self.utcTZ		= pytz.timezone('UTC')				# initialize UTC: time zones.
		utcNaive		= dt.datetime.utcnow()				# start with a naive UTC datetime

		# make naive utc datetime dst aware. This pattern should 
		# be use any time we need to convert naive to aware
		self.UTCtime	= utcNaive.replace(tzinfo=pytz.utc)

		# load current location as default 
		# location, followed by all the others
		self.loadCurrentLocation()
		self.loadOtherLocations()


	def loadCurrentLocation(self):

		# load current location (always at offset 0)
		url = 'http://ipinfo.io/json'
		default = False
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36')]
			response = opener.open(url)
			#print response
		except urllib2.HTTPError as err:
			default = True
			print url+"\n"
			print "Exception...\nError: " + str(err.code)+"\nUsing Vancouver as default location!!\n"
		except urllib2.URLError as err:
			default = True
			print "Exception...\nError: " + str(err)+"\nUsing Vancouver as default location!!\n"
			#raise

		if not default:
			rawResp = response.read()
			data = json.loads(rawResp)

			self.IP			 = data['ip']
			self.org		 = data['org']
			self.city 		 = data['city']
			self.country	 = data['country']
			self.region		 = data['region']
			self.coordinates = data['loc']
			coord 			 = self.coordinates.split(',')

			self.tzEarthLocations[0]["lat"] 	= float(coord[0])
			self.tzEarthLocations[0]["long"]   	= float(coord[1])
			self.tzEarthLocations[0]["tzname"] 	= data['timezone']
			#self.tzEarthLocations[0]["localTZ"] = pytz.timezone(data['timezone'])
			print "\n------------------------------------"
			print ' Your IP detail '
			print "------------------------------------"
			print 'IP ............ {4} \nRegion ........ {1} \nCountry ....... {2} \nCity .......... {3} \nISP ........... {0} \nCoordinates ... {5} \nTimeZone ...... {6}'.format(self.org, self.region, self.country, self.city, self.IP, self.coordinates, self.tzEarthLocations[0]["tzname"])
		else:
			self.city		= self.tzEarthLocations[0]["name"]

		# initialize local time zones...
		self.localTZ 							  = pytz.timezone(self.tzEarthLocations[0]["tzname"]) #self.timezoneStr)
		# print default location info
		print 'Latitude ...... {0}'.format(self.tzEarthLocations[0]["lat"])
		print 'Longitude ..... {0}'.format(self.tzEarthLocations[0]["long"])

		return 


		# ... deduct non-naive (DST aware) local date...
		self.tzEarthLocations[0]["localDatetime"] = self.UTCtime.astimezone(self.localTZ)
		# ... and determine if daylight saving is in use
		self.tzEarthLocations[0]["dst"] 		  = bool(self.tzEarthLocations[0]["localDatetime"].dst())



	def loadOtherLocations(self):
		for i in range(0, len(self.tzEarthLocations)):
			self._setLocationDatetime(i)


	def _setLocationDatetime(self, tzidx):
		if tzidx > len(self.tzEarthLocations)-1:
			print "IDX", tzidx, " too big"
			return 

		# determine tz aware local time and daylight saving use flag
		self.tzEarthLocations[tzidx]["localDatetime"] = self.UTCtime.astimezone(pytz.timezone(self.tzEarthLocations[tzidx]["tzname"]))
		self.tzEarthLocations[tzidx]["dst"] = bool(self.tzEarthLocations[tzidx]["localDatetime"].dst())
		
		# determine how many secs separate local time and UTC. 
		"""
		# When returned value is < 0, it means we 
		# are WEST of UTC, and a value > 0 means we are East of UTC 
		"""
		self.tzEarthLocations[tzidx]["AbsoluteTimeDiffInSec"] = self.tz_diff(self.tzEarthLocations[tzidx]["localDatetime"], self.UTCtime, self.tzEarthLocations[tzidx]["long"])

		print self.tzEarthLocations[tzidx]["name"], self.tzEarthLocations[tzidx]["localDatetime"]


	def getLocationInfo(self, tzindex = -1):
		if tzindex >= 0 and tzindex < len(self.tzEarthLocations):
			return {
				"lat": self.tzEarthLocations[tzindex]["lat"],
				"long": self.tzEarthLocations[tzindex]["long"],
				"timezone": self.tzEarthLocations[tzindex]["tzname"],
				"name": self.tzEarthLocations[tzindex]["name"],
				"localDatetime": self.tzEarthLocations[tzindex]["localDatetime"],
				"AbsoluteTimeDiffInSec": self.tzEarthLocations[tzindex]["AbsoluteTimeDiffInSec"]
			}
		# for whacky index we return the default location
		return {
			"lat": self.tzEarthLocations[0]["lat"],
			"long": self.tzEarthLocations[0]["long"],
			"timezone": self.tzEarthLocations[0]["tzname"],
			"name": self.tzEarthLocations[0]["name"],
			"localDatetime": self.tzEarthLocations[0]["localDatetime"],
			"AbsoluteTimeDiffInSec": self.tzEarthLocations[0]["AbsoluteTimeDiffInSec"]
		}

	def getLocationOfInterestIndex(self):
		return self.getLocationInfo(self.locationOfInterest)

	def setLocal2UTCdiff(self):

		print "------------------------------------"
		print " Local Timezone data for", self.city
		print "------------------------------------"
		print "UTC datetime: .................. ", self.UTCtime
		print "Local datetime: ................ ", self.tzEarthLocations[0]["localDatetime"], "DST=", self.tzEarthLocations[0]["dst"]

		# determine the difference between local TZ and UTC in seconds. The datetime.now() provides
		# a naive date from which we can figure out the exact time difference in second depending on 
		# whether or not DST is in effect (based on time of year)

		self.longitude = self.tzEarthLocations[0]["long"] # hack to use the current location longitude as longitude reference to position texture
		
		# determine how many secs separate default local time and UTC. 
		"""
		# When returned value is < 0, it means we 
		# are WEST of UTC, and a value > 0 means we are East of UTC 
		"""
		self.AbsoluteTimeDiffInSec = self.tz_diff(self.tzEarthLocations[0]["localDatetime"], self.UTCtime, self.longitude) #dt.datetime.utcnow().replace(tzinfo = pytz.timezone('UTC'))) #self.localTZ, self.utcTZ) 
		print "========================>>>>>>>>>>>>", self.AbsoluteTimeDiffInSec
		print "LOCAL=", self.tzEarthLocations[0]["localDatetime"], ", UTC=", self.UTCtime

		#self.longitudeSign = -1 if self.longitude < 0  else 1
		self.longitudeSign = 1  # TODO: remove self.longitudeSign variable


	def InitGeometryData(self):

		# extra info can be calculated. Keep in mind, every 15 degrees correspond
		# to 1h -> 3600s. We round up to the lower or upper value based on whether 
		# the difference between the actual float value and its integer value is > 0.5 

		self.angTime  = self.longitude / 15
		int_ang = int(self.angTime)
		if self.angTime - int_ang > 0.5:
			self.angTime = int_ang+1
		else:
			self.angTime = int_ang

		# from angular time, deduct True timezone difference in seconds:
		# (here we only care about the true angular difference)

		self.timezoneInSec = self.angTime * 3600
		self.TimeToWESTantiMeridian = 12 + self.angTime
				
		# establish time to date line in hours, relative and absolute
		#self.TimeToWESTantiMeridian = 12 - self.timezoneInSec/3600 + (1 if self.dst else 0)
		
		#self.TimeToEASTantiMeridian = 86400/2 - abs(self.timezoneInSec)
		self.TimeToEASTantiMeridian = 24 - self.TimeToWESTantiMeridian
		
		self.initSolarTime()

		print "Angular time with UTC .......... ", self.angTime, "hours"
		print "#timezones to UTC .............. ", self.timezoneInSec/3600
		print "#Timezones to E antiMeridian ... ", self.TimeToEASTantiMeridian
		print "#Timezones to W antiMeridian ... ", self.TimeToWESTantiMeridian 	#24 - self.TimeToWESTantiMeridian
		print "Time from E antiMeridian ....... ", 12 - self.timezoneInSec/3600 + (1 if self.tzEarthLocations[0]["dst"] else 0)
		print "\nSolar time ................... ", self.getSolarTime(), "This is the angle between vertical and sun current position"


	def tz_naive_diff(self, date, tz_from, tz_to): # unused
		'''
		Returns the difference in seconds between tz_from and tz_to
		for a given naive date. 
			- If tz_from is West of tz_to, the # of hours is correct.
			- If tz_from is East of tz_to, the # of hours is augmented with 12 hours.
		The difference is always  < 0

		'''
		if self.longitude < 0:
			# west of UTC
			return (tz_from.localize(date) - tz_to.localize(date)).seconds
		else: 
			# east of UTC
			return (tz_to.localize(date) - tz_from.localize(date)).seconds


	def tz_diff(self, date_tz_from, date_tz_to, longitude):
		'''
		Returns the difference in seconds between 2 tz aware dates
		The difference is always  < 0
		'''
		return (int(date_tz_from.strftime('%z')) - int(date_tz_to.strftime('%z')))*36
		
		 
		print "LOCAL=", date_tz_from, ", UTC=", date_tz_to
		if longitude < 0:
			# west of UTC
			print "WEST: ", int(date_tz_from.strftime('%z')) - int(date_tz_to.strftime('%z'))
			#return (date_tz_from - date_tz_to).seconds
			return (int(date_tz_from.strftime('%z')) - int(date_tz_to.strftime('%z')))*36
		else: 
			# east of UTC
			print "EAST: ", int(date_tz_to.strftime('%z')) - int(date_tz_from.strftime('%z'))
			#return (date_tz_to - date_tz_from).seconds
			return (int(date_tz_to.strftime('%z')) - int(date_tz_from.strftime('%z')))*36

	def tz_diff_SAVE(self, date_tz_from, date_tz_to):
		'''
		Returns the difference in seconds between 2 tz aware dates
		The difference is always  < 0
		'''
		print "LOCAL=", date_tz_from, ", UTC=", date_tz_to
		if self.longitude < 0:
			# west of UTC
			print "WEST: ", int(date_tz_from.strftime('%z')) - int(date_tz_to.strftime('%z'))
			#return (date_tz_from - date_tz_to).seconds
			return (int(date_tz_from.strftime('%z')) - int(date_tz_to.strftime('%z')))*36
		else: 
			# east of UTC
			print "EAST: ", int(date_tz_to.strftime('%z')) - int(date_tz_from.strftime('%z'))
			#return (date_tz_to - date_tz_from).seconds
			return (int(date_tz_to.strftime('%z')) - int(date_tz_from.strftime('%z')))*36


	def initSolarTime(self):
		# to set solar time, we need a struct of type time.struct_time, hence we pass time.localtime()
		# self.solarT = self.setSolarTime(self.datetime_to_StructTime(self.localdatetime), self.longitude)
		self.solarT = self.computeLocalSolarTime(self.tzEarthLocations[0]["localDatetime"]) #self.localdatetime)


	def computeUTCSolarTime(self, UTCdatetime):
		# calculate a solar time for a given date and time. we need a struct of type time.struct_time, 
		# hence we pass time.localtime()
		# return self.setSolarTime(self.datetime_to_StructTime(UTCdatetime), 0)
		return self.computeSolarTime(UTCdatetime, 0)

	def computeLocalSolarTime(self, localdatetime):
		# calculate a solar time for a given date time. we need a struct of type time.struct_time, 
		# hence we pass time.localtime()
		# return self.setSolarTime(self.datetime_to_StructTime(localdatetime), self.longitude)
		return self.computeSolarTime(localdatetime, self.longitude)

	def computeSolarTime(self, a_datetime, longitude):
		# calculate a solar time for a given date time. we need a struct of type time.struct_time, 
		# hence we pass time.localtime()
		return self.setSolarTime(self.datetime_to_StructTime(a_datetime), longitude)

	def setSolarTime(self, localtime, longitude):

		"""
		Solar time is a calculation of the passage of time based on the position of the Sun in the sky. 
		The fundamental unit of solar time is the day, based on the synodic rotation period. Two types 
		of solar time are apparent solar time (sundial time) and mean solar time (clock time).		
		"""
#		gamma = 2 * math.pi / 365 * (localtime.tm_yday - 1 + float(localtime.tm_hour - 12) / 24)
		gamma = 2 * math.pi / EARTH_PERIOD * (localtime.tm_yday - 1 + float(localtime.tm_hour - 12) / 24)
		eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma) \
				- 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))
		decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) \
			- 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma) \
			- 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma)

		time_offset = eqtime + (4 * longitude)  - (self.timezoneInSec/60)

		tst = localtime.tm_hour * 60 + localtime.tm_min + localtime.tm_sec / 60 + time_offset
		solarT = (tst / 4) - 180
		return solarT

	def getSolarTime(self):
		return self.solarT

	def structTime_to_DateTime(self, structTimeObj):
		return dt.datetime(*structTimeObj[:6])

	def datetime_to_StructTime(self, datetimeObj):
		return datetimeObj.timetuple()

	def TimeToUtcInSec(self):
		#print "TimeToUtcInSec is ", self.AbsoluteTimeDiffInSec
		return self.tzEarthLocations[self.locationOfInterest]['AbsoluteTimeDiffInSec']
		#return self.AbsoluteTimeDiffInSec

	def TimeInSec2degree(self, time_in_sec):
		# 15 deg corresponds to 1hour (3600s). 1s -> 15/3600
		return time_in_sec * 15/3600

	def Time2degree(self, time_in_hour):
		# 15 deg corresponds to 1hour (3600s). 1s -> 15/3600
		return time_in_hour * 15

	def getLocalDateTime(self):
		# returns local time as a structure:
		# time.struct_time(tm_year=2021, tm_mon=4, tm_mday=15, tm_hour=13, tm_min=34, tm_sec=41, tm_wday=3, tm_yday=105, tm_isdst=1) 
		return self.tzEarthLocations[0]["localDatetime"]
		#return self.localdatetime

	def getLocationOfInterestDateTime(self):
		# returns local time as a structure:
		# time.struct_time(tm_year=2021, tm_mon=4, tm_mday=15, tm_hour=13, tm_min=34, tm_sec=41, tm_wday=3, tm_yday=105, tm_isdst=1) 
		return self.tzEarthLocations[self.locationOfInterest]["localDatetime"]

	def setUTCDateTime(self, utcTime):
		self.UTCtime = utcTime

	def getUTCDateTime(self):
		return self.UTCtime

	def getTZ(self):
		return self.tzEarthLocations[0]["tzname"]
		
	def getPytzValue(self):
#		print "TZ INFO: timezoneSTR=", self.timezoneStr, "timezoneINT=", pytz.timezone(self.timezoneStr)
		print "TZ INFO: timezoneSTR=", self.tzEarthLocations[0]["tzname"], "timezoneINT=", pytz.timezone(self.tzEarthLocations[0]["tzname"])
		return pytz.timezone(self.tzEarthLocations[0]["tzname"]) #self.timezoneStr)




