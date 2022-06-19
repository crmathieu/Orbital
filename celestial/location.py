#from scipy.sparse.csgraph import _validation
import urllib2
#import httplib
#import re
import json
#import sys
import math

import pytz
import datetime as dt
import time
from orbit3D import deg2rad

"""
TimeLoc - time management

"""

TZ_UTC = 0
TZ_CAIRO = 1
TZ_PARIS = 2
TZ_COUVE = 3
TZ_ICE = 4
TZ_HONG = 5
TZ_AUSTRA = 6
TZ_CHILI = 7
TZ_HONO = 8
TZ_CAPE = 9
TZ_KOUR = 10
TZ_BAIK = 11
TZ_CHINA = 12
TZ_INDIA = 13

class Timeloc:
	tzEarthLocations = [
    {
        "tzname": "Africa/Abidjan",
        "lat": 51.4934,
        "long": 0.0098,
        "name": "Greenwich"
    },
    {
        "tzname": "Africa/Cairo",
        "lat": 30.0444,
        "long": 31.2357,
        "name": "Cairo"
    },
    {
        "tzname": "Europe/Paris",
        "lat": 48.8566,
        "long": 2.3522,
        "name": "Paris"
    },
    {
        "tzname": "America/Los_Angeles",
        "lat": 45.6418,
        "long": -122.6801,
        "name": "Vancouver"
    },
    {
        "tzname": "Iceland",
        "lat": 64.1466,
        "long": -21.9426,
        "name": "Reykjavik"
    },
    {
        "tzname": "Hongkong",
        "lat": 22.3193,
        "long": 114.1694,
        "name": "Hong Kong"
    },
    {
        "tzname": "Australia/Sydney",
        "lat": -33.8688,
        "long": 151.2093,
        "name": "Sydney"
    },
    {
        "tzname": "America/Santiago",
        "lat": -33.4489,
        "long": -70.6693,
        "name": "Santiago"
    },
    {
        "tzname": "Pacific/Honolulu",
        "lat": 19.8968,
        "long": -155.5828,
        "name": "Honolulu"
    },
	{
        "tzname": "America/New_York",
        "lat": 28.3922,
        "long": -80.6077,
        "name": "Cape Canaveral"
    },
 	{
        "tzname": "America/Guyana",
        "lat": 5.1611,
        "long": -52.6493,
        "name": "Kourou Spaceport"
    },
 	{
        "tzname": "Asia/Oral",
        "lat": 45.6232,
        "long": 63.3140,
        "name": "Baikonur Cosmodrome"
    },
	{
        "tzname": "Asia/Chungking",
        "lat": 19.614492,
        "long": 110.951133,
        "name": "Wenchang Spaceport"
    },
	{
        "tzname": "Asia/Kolkata",
        "lat": 8.5241,
        "long": 76.9366,
        "name": "Thiruvananthapuram IND Spaceport"
    },
	{
        "tzname": "America/Los_Angeles",
        "lat": 34.7420,
        "long": -120.5724,
        "name": "Vandenberg Air Force Base"
    },
	{
        "tzname": "Pacific/Auckland",
        "lat": -39.0806,
        "long": 177.8749,
        "name": "Mahia NZL Spaceport"
    },
	{
        "tzname": "Japan",
        "lat": 30.3999984,
        "long": 130.968662792,
        "name": "Tanegashima JPN Spaceport"
    },
	{
        "tzname": "Asia/Shanghai",
        "lat": 27.8945,
        "long": 102.2631,
        "name": "Xichang CHN Spaceport"
    },

]
	def __init__(self, index = -1):
		#index = TZ_COUVE
		self.getLocationInfoFromIPaddress(index)
		self.InitLocalTimezoneData()
		self.InitGeometryData()
		#self.Psi = 0.0

	def getLocationInfo(self, tzindex = -1):
		if tzindex >= 0:
			if tzindex > len(self.tzEarthLocations):
				return {}

			return {
				"lat": self.tzEarthLocations[tzindex]["lat"],
				"long": self.tzEarthLocations[tzindex]["long"],
				"timezone": self.tzEarthLocations[tzindex]["tzname"],
				"name": self.tzEarthLocations[tzindex]["name"]
			}

		return {
			"lat": self.latitude,
			"long": self.longitude,
			"timezone": self.timezoneStr,
			"name": self.city
		}

	def getLocationInfoFromIPaddress(self, tzindex):
		if tzindex >= 0:
			k = tzindex
			self.latitude 		= self.tzEarthLocations[k]["lat"]
			self.longitude 		= self.tzEarthLocations[k]["long"]
			self.timezoneStr	= self.tzEarthLocations[k]["tzname"]
			self.city 			= self.tzEarthLocations[k]["name"]
			#print ("Time Zone for {0}".format(self.city))
			self.utcTZ 		= pytz.timezone('UTC')
			self.localTZ 	= pytz.timezone(self.timezoneStr)
			return

		url = 'http://ipinfo.io/json'
		print url+"\n"
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36')]
			response = opener.open(url)
			print response
		except urllib2.HTTPError as err:
			print "Exception...\n\nError: " + str(err.code)
			raise

		rawResp = response.read()
		data = json.loads(rawResp)

		self.IP			 = data['ip']
		self.org		 = data['org']
		self.city 		 = data['city']
		self.country	 = data['country']
		self.region		 = data['region']
		self.coordinates = data['loc']
		coord 			 = self.coordinates.split(',')
		self.latitude 	 = float(coord[0])
		self.longitude 	 = float(coord[1])
		self.timezoneStr = data['timezone']

		# initialize local and UTC time zones
		self.utcTZ 		 = pytz.timezone('UTC')
		self.localTZ 	 = pytz.timezone(self.timezoneStr)
		 
		#print 'UTC tz: {0}\nLOCAL tz: {1}\n\n'.format(self.utcTZ, self.localTZ)
		print 'Your IP detail\n '
		print 'IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0} \ncoordinates : {5} \nTimeZone : {6}'.format(self.org,self.region,self.country,self.city,self.IP,self.coordinates,self.timezoneStr)
		print 'Latitude={0}'.format(self.latitude)
		print 'Longitude={0}'.format(self.longitude)


	def InitLocalTimezoneData(self):
		# start with a naive UTC datetime
		self.UTCtime 	 	= dt.datetime.utcnow()

		# make datetime dst aware. This pattern should be use any time we need to convert naive to aware
		self.UTCtime 	 	= self.UTCtime.replace(tzinfo=pytz.utc)

		# deduct local time ...
		self.localdatetime 	= self.UTCtime.astimezone(pytz.timezone(self.timezoneStr))

		# ... and determine if daylight saving is in use
		self.dst = bool(self.localdatetime.dst())

		print "------------------------------------"
		print "Local Timezone data for ", self.city
		print "------------------------------------"
		print "UTC datetime: .............. ", self.UTCtime
		print "Local datetime: ............ ", self.localdatetime, "DST=", self.dst

		# determine the difference between local TZ and UTC in seconds. The datetime.now() provides
		# a naive date from which we can figure out the exact time difference in second depending on 
		# whether or not DST is in effect (based on time of year)

		naiveDate = dt.datetime.now()
		# determine how many secs separate local time and UTC. 
		# the return value is always < 0
		"""
		# When returned value is < 0, it means we 
		# are WEST of UTC, and a value > 0 means we are East of UTC 
		"""
		self.AbsoluteTimeDiffInSec = self.tz_diff(naiveDate, self.localTZ, self.utcTZ) 
		self.longitudeSign = -1 if self.longitude < 0  else 1

	def InitGeometryData(self):

		# extra info can be calculated. Keep in mind 15 degrees -> 3600s
		# we round up to the lower or upper value based on whether the
		# difference between the actual float value and its integer value is > 0.5 

		self.angTime  = self.longitude / 15
		int_ang = int(self.angTime)
		if self.angTime - int_ang > 0.5:
			self.angTime = int_ang+1
		else:
			self.angTime = int_ang

		# from angular time, deduct True timezone difference in seconds:
		# (here we only care about the true angular difference)

		self.timezoneInSec = self.angTime * 3600
		self.TimeToWESTdateline = 12 + self.angTime
				
		# establish time to date line in hours, relative and absolute
		#self.TimeToWESTdateline = 12 - self.timezoneInSec/3600 + (1 if self.dst else 0)
		
		#self.TimeToEASTdateline = 86400/2 - abs(self.timezoneInSec)
		self.TimeToEASTdateline = 24 - self.TimeToWESTdateline
		
		self.initSolarTime()

		print "Angular time with UTC ...... ", self.angTime, "hours"
		print "#timezones to UTC .......... ", self.timezoneInSec/3600
		print "#Timezones to E dateline ... ", self.TimeToEASTdateline
		print "#Timezones to W dateline ... ", self.TimeToWESTdateline 	#24 - self.TimeToWESTdateline
		print "Time from E dateline ....... ", 12 - self.timezoneInSec/3600 + (1 if self.dst else 0)
		print "\nSolar time ................. ", self.getSolarTime(), "This is the angle between vertical and sun current position"


	def tz_diff(self, date, tz_from, tz_to):
		'''
		Returns the difference in seconds between tz_from and tz_to
		for a given date. 
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

	def initSolarTime(self):
		# to set solar time, we need a struct of type time.struct_time, hence we pass time.localtime()
		self.solarT = self.setSolarTime(self.datetime_to_StructTime(self.localdatetime), self.longitude)

	def computeUTCSolarTime(self, UTCdatetime):
		# calculate a solar time for a given date time. we need a struct of type time.struct_time, 
		# hence we pass time.localtime()
		return self.setSolarTime(self.datetime_to_StructTime(UTCdatetime), 0)

	def computeSolarTime(self, localdatetime):
		# calculate a solar time for a given date time. we need a struct of type time.struct_time, 
		# hence we pass time.localtime()
		return self.setSolarTime(self.datetime_to_StructTime(localdatetime), self.longitude)

	def setSolarTime(self, localtime, longitude):

		"""
		Solar time is a calculation of the passage of time based on the position of the Sun in the sky. 
		The fundamental unit of solar time is the day, based on the synodic rotation period. Two types 
		of solar time are apparent solar time (sundial time) and mean solar time (clock time).		
		"""
		gamma = 2 * math.pi / 365 * (localtime.tm_yday - 1 + float(localtime.tm_hour - 12) / 24)
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
		return self.AbsoluteTimeDiffInSec

	def TimeInSec2degree(self, time_in_sec):
		# 15 deg corresponds to 1hour (3600s). 1s -> 15/3600
		return time_in_sec * 15/3600

	def Time2degree(self, time_in_hour):
		# 15 deg corresponds to 1hour (3600s). 1s -> 15/3600
		return time_in_hour * 15

	def getLocalDateTime(self):
		# returns local time as a structure:
		# time.struct_time(tm_year=2021, tm_mon=4, tm_mday=15, tm_hour=13, tm_min=34, tm_sec=41, tm_wday=3, tm_yday=105, tm_isdst=1) 
		return self.localdatetime

	def setUTCDateTime(self, utcTime):
		self.UTCtime = utcTime

	def getUTCDateTime(self):
		return self.UTCtime

	def getTZ(self):
		return self.timezoneStr
		
	def getPytzValue(self):
		print "TZ INFO: timezoneSTR=", self.timezoneStr, "timezoneINT=", pytz.timezone(self.timezoneStr)
		return pytz.timezone(self.timezoneStr)




