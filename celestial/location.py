#from scipy.sparse.csgraph import _validation
import urllib2
import httplib
import re
import json
import sys
import math

import pytz
import datetime as dt
#from datetime import timedelta
import time
#from dateutil import tz

"""
TimeLoc - time management

"""
tz = [
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
]
TZ_CAIRO = 0
TZ_PARIS = 1
TZ_COUVE = 2
TZ_ICE = 3
TZ_HONG = 4
TZ_AUSTRA = 5
TZ_CHILI = 6

class Timeloc:
	def __init__(self):
		index = -1  #TZ_ICE
		self.getLocationFromIPaddress(index)

		self.UTCtime 	 	= dt.datetime.utcnow()

		# make date dst aware. This pattern should be use any time we need to convert naive to aware
		self.UTCtime 	 	= self.UTCtime.replace(tzinfo=pytz.utc)

		# deduct local time ...
		self.localdatetime 	= self.UTCtime.astimezone(pytz.timezone(self.timezoneStr))
		# ... and determine if daylight saving is in use
		self.dst = bool(self.localdatetime.dst())

		print "-------------------------"
		print "Time in ", self.city
		print "-------------------------"
		print "Local datetime: ............ ", self.localdatetime
		print "Daylight Saving Time date .. ", self.dst
		print "\nUTC datetime: ............ ", self.UTCtime

		# determine the difference between local TZ and UTC in seconds. The datetime.now() provides
		# a naive from which we can to figure out the exact time difference in second depending on 
		# whether or not DST is in effect (based on time of year)

		naiveDate = dt.datetime.now()
		self.timezoneInSec = self.tz_diff(naiveDate, self.localTZ, self.utcTZ) 
		#self.timezoneInSec = (self.localTZ.localize(naiveDate) - self.utcTZ.localize(naiveDate)).total_seconds()
		self.longitudeSign = -1 if self.longitude < 0  else 1

		self.timezoneInSec = self.timezoneInSec * self.longitudeSign

		print ("local time and UTC offset .... ", self.timezoneInSec, "sec")

		# extra info can be calculated. Keep in mind 15 degrees -> 3600s
		self.angTime  = self.longitude / 15
		int_ang = int(self.angTime)
		if self.angTime - int_ang > 0.5:
			self.angTime = int_ang+1
		else:
			self.angTime = int_ang

		# establish time to date line in hours, relative and absolute
		self.RelativeTimeToDateline = 86400/2 - abs(self.timezoneInSec)
		self.AbsoluteTimeToDateline = 12 + self.angTime 
		self.initSolarTime()

		print "time zone from UTC ......... ", self.timezoneInSec/3600, "DST=", self.dst
		print "time zone to W dateline .... ", self.RelativeTimeToDateline/3600, "DST=", self.dst, ", This parameter is bogus" 
		print "#Timezones to W dateline .. ", self.AbsoluteTimeToDateline
		print "#Timezones to E dateline .. ", 24 - self.AbsoluteTimeToDateline
		print "Angular time with UTC ...... ", self.angTime, "hours"
		print "Solar time ................. ", self.getSolarTime(), "This is the angle between vertical and sun current position"


	def toto(self): #__init__(self):

		self.getLocationFromIPaddress(TZ_PARIS)

		self.UTCtime 	 	= dt.datetime.now(pytz.utc)
		#self.UTCtime 	 	= dt.datetime.now(tz=pytz.utc)
		#self.UTCtime = self.UTCtime.replace(tzinfo=pytz.utc)

		print "TZ={0}".format(pytz.timezone(self.timezoneStr))

	#		self.localdatetime 	= dt.datetime.now(tz=pytz.timezone(self.timezoneStr))
		#####self.localdatetime 	= self.UTCtime + dt.timedelta(hours=2)
		self.localdatetime = self.UTCtime.astimezone(self.localTZ)
		
		"""
		if self.longitude < 0:
			self.localdatetime 	= dt.datetime.now(tz=pytz.timezone(self.timezoneStr))
		"""

		print "++++++++++++++"
		print bool(self.localdatetime.dst())
		print "local datetime:{0}".format(self.localdatetime)
		print "UTC is: {0}".format(self.UTCtime)	

		# determine the difference between local TZ and UTC in seconds. The datetime.now() provides
		# a aware date time containing daylight saving time (dst) information, to figure out the exact
		# time difference depending on the time of year

		self.timezoneInSec = self.tz_diff(dt.datetime.now(), self.localTZ, self.utcTZ) 
		#self.timezoneInSec = self.tz_diff(dt.datetime.now(), self.utcTZ, self.localTZ) 
		print "TimezoneDiff-in-seconds=", self.timezoneInSec

		# get timezone in seconds from GT to current location. When longitude is negative 
		# (west of GT), we need to change the sign of timezoneInSec
		
		if self.longitude < 0:
			self.timezoneInSec *= -1

		self.utcDeltaInSecondsFromLocal = - self.timezoneInSec
		
		#self.utcDeltaInSecondsFromLocal = self.timezoneInSec

		print "seconds from local to UTC =", self.utcDeltaInSecondsFromLocal

		self.UTCoffsetInSeconds = self.timezoneInSec  # in seconds
		print self.timezoneInSec/3600, " hours from UTC"

		self.RelativeTimeToDateline = 86400/2 - abs(self.timezoneInSec)
		self.AbsoluteTimeToDateline = 86400/2 - self.timezoneInSec

		print "time zone from UTC=", self.UTCoffsetInSeconds/3600
		print "time zone to dateline=", self.RelativeTimeToDateline/3600 

		print self.setSolarTime()


	def tz_diff(self, date, tz_from, tz_to):
		'''
		Returns the difference in seconds between tz_from and tz_to
		for a given date. 
			- If tz_from is West of tz_to, the # of hours is correct.
			- If tz_from is East of tz_to, the # of hours is augmented with 12 hours.

		'''
		#return (tz_from.localize(date) - tz_to.localize(date)).seconds

		if self.longitude < 0:
			# west of UTC
			return (tz_from.localize(date) - tz_to.localize(date)).seconds
		else: 
			# east of UTC
			return (tz_to.localize(date) - tz_from.localize(date)).seconds


	def initSolarTime(self):
		# to set solar time, we need a struct of type time.struct_time, hence we pass time.localtime()
		self.solarT = self.setSolarTime(self.datetime_to_StructTime(self.localdatetime), self.longitude)

	def structTime_to_DateTime(self, structTimeObj):
		return dt.datetime(*structTimeObj[:6])

	def datetime_to_StructTime(self, datetimeObj):
		return datetimeObj.timetuple()

	def getSolarTime(self):
		return self.solarT

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

#		time_offset = eqtime + (4 * longitude)  - (self.timezoneInSec/60)
		time_offset = eqtime + (4 * longitude)  - (self.timezoneInSec/60)

		#print "Time Offset = ", time_offset

		tst = localtime.tm_hour * 60 + localtime.tm_min + localtime.tm_sec / 60 + time_offset
		solarT = (tst / 4) - 180

		return solarT

	def RelativeTimeToUtcInSec(self):
		return self.timezoneInSec
		return self.utcDeltaInSecondsFromLocal


	def Time2degree(self, time_in_sec):
		# 15 deg corresponds to 1hour (3600s). 1s -> 15/3600
		return time_in_sec * 15/3600

	def getLocalDateTime(self):
		# returns local time as a structure:
		# time.struct_time(tm_year=2021, tm_mon=4, tm_mday=15, tm_hour=13, tm_min=34, tm_sec=41, tm_wday=3, tm_yday=105, tm_isdst=1) 
		return self.localdatetime

	def setLocaltimeFromUTCXX(self, utcTime): # utcTime must a datetime class
		self.localdatetime = utcTime + something

	def setUTCDateTime(self, utcTime):
		self.UTCtime = utcTime

	def getUTCDateTime(self):
		return self.UTCtime

	def getTZ(self):
		return self.timezoneStr
		
	def getPytzValue(self):
		print "TZ INFO: timezoneSTR=", self.timezoneStr, "timezoneINT=", pytz.timezone(self.timezoneStr)
		return pytz.timezone(self.timezoneStr)

	def getLocationFromIPaddress(self, tzindex):
		if tzindex >= 0:
			k = tzindex
			self.latitude 		= tz[k]["lat"]
			self.longitude 		= tz[k]["long"]
			self.timezoneStr	= tz[k]["tzname"]
			self.city 			= tz[k]["name"]
			print ("Time Zone for {0}".format(self.city))
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


		#response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})

		rawResp = response.read()
		data = json.loads(rawResp)

		self.IP			 = data['ip']
		self.org		 = data['org']
		self.city 		 = data['city']
		self.country	 = data['country']
		self.region		 = data['region']
		self.coordinates = data['loc']
		coord = self.coordinates.split(',')
		self.latitude = float(coord[0])
		self.longitude = float(coord[1])
		# determine timezone and delta between local time and UTC
		self.timezoneStr	 = data['timezone']

		# initialize local and UTC time zones
		self.utcTZ 		= pytz.timezone('UTC')
		self.localTZ 	= pytz.timezone(self.timezoneStr)
		 
		#print 'UTC tz: {0}\nLOCAL tz: {1}\n\n'.format(self.utcTZ, self.localTZ)
		print 'Your IP detail\n '
		print 'IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0} \ncoordinates : {5} \nTimeZone : {6}'.format(self.org,self.region,self.country,self.city,self.IP,self.coordinates,self.timezoneStr)
		print 'Latitude={0}'.format(self.latitude)
		print 'Longitude={0}'.format(self.longitude)



class TimelocXX:
	def __init__(self):

		self.getLocationFromIPaddress(TZ_CAIRO)

		self.UTCtime 	 	= dt.datetime.utcnow()
		#self.UTCtime 	 	= dt.datetime.now(tz=pytz.utc)
		self.UTCtime = self.UTCtime.replace(tzinfo=pytz.utc)

		print "TZ={0}".format(pytz.timezone(self.timezoneStr))

#		self.localdatetime 	= dt.datetime.now(tz=pytz.timezone(self.timezoneStr))
		self.localdatetime 	= self.UTCtime + dt.timedelta(hours=2)
		if self.longitude < 0:
			self.localdatetime 	= dt.datetime.now(tz=pytz.timezone(self.timezoneStr))


		print "++++++++++++++"
		print bool(self.localdatetime.dst())
		print "local datetime:{0}".format(self.localdatetime)
		print "UTC is: {0}".format(self.UTCtime)	

		# determine the difference between local TZ and UTC in seconds. The datetime.now() provides
		# a aware date time containing daylight saving time (dst) information, to figure out the exact
		# time difference depending on the time of year

		self.timezoneInSec = self.tz_diff(dt.datetime.now(), self.localTZ, self.utcTZ) 
		#self.timezoneInSec = self.tz_diff(dt.datetime.now(), self.utcTZ, self.localTZ) 


		# get timezone in seconds from GT to current location. When longitude is negative 
		# (west of GT), we need to change the sign of timezoneInSec
		"""
		if self.longitude < 0:
			self.timezoneInSec *= -1

		self.utcDeltaInSecondsFromLocal = - self.timezoneInSec
		"""
		self.utcDeltaInSecondsFromLocal = self.timezoneInSec

		print "seconds from local to UTC =", self.utcDeltaInSecondsFromLocal

		self.UTCoffsetInSeconds = self.timezoneInSec  # in seconds
		print self.timezoneInSec/3600, " hours from UTC"

		self.RelativeTimeToDateline = 86400/2 - abs(self.timezoneInSec)
		self.AbsoluteTimeToDateline = 86400/2 - self.timezoneInSec

		print "time zone from UTC=", self.UTCoffsetInSeconds/3600
		print "time zone to dateline=", self.RelativeTimeToDateline/3600 

		print self.setSolarTime()


	def tz_diff(self, date, tz_from, tz_to):
		'''
		Returns the difference in seconds between tz_from and tz_to
		for a given date. 
			- If tz_from is West of tz_to, the # of hours is correct.
			- If tz_from is East of tz_to, the # of hours is augmented with 12 hours.

		'''
		return (tz_from.localize(date) - tz_to.localize(date)).seconds

		if self.longitude < 0:
			# west of UTC
			return (tz_from.localize(date) - tz_to.localize(date)).seconds
		else: 
			# east of UTC
			return (tz_to.localize(date) - tz_from.localize(date)).seconds


	def setSolarTime(self):
		# to set solar time, we need a struct of type time.struct_time, hence we pass time.localtime()
		return self.getSolarTime(self.datetime_to_StructTime(self.localdatetime), self.longitude)

	def structTime_to_DateTime(self, structTimeObj):
		return dt.datetime(*structTimeObj[:6])

	def datetime_to_StructTime(self, datetimeObj):
		return datetimeObj.timetuple()

	def getSolarTime(self, localtime, longitude):

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

#		time_offset = eqtime + (4 * longitude)  - (self.timezoneInSec/60)
		time_offset = eqtime + (4 * longitude)  - (self.timezoneInSec/60)

		print "Time Offset = ", time_offset

		tst = localtime.tm_hour * 60 + localtime.tm_min + localtime.tm_sec / 60 + time_offset
		self.solarT = (tst / 4) - 180

		print "solar Time=", self.solarT, "degrees"
		return self.solarT

	def RelativeTimeToUtcInSec(self):
		return self.utcDeltaInSecondsFromLocal

	def Time2degree(self, time_in_sec):
		# 15 deg corresponds to 1hour (3600s). 1s -> 15/3600
		return time_in_sec * 15/3600

	def getLocalDateTime(self):
		# returns local time as a structure:
		# time.struct_time(tm_year=2021, tm_mon=4, tm_mday=15, tm_hour=13, tm_min=34, tm_sec=41, tm_wday=3, tm_yday=105, tm_isdst=1) 
		return self.localdatetime

	def setLocaltimeFromUTC(self, utcTime): # utcTime must a datetime class
		self.localdatetime = utcTime + something

	def setUTCDateTime(self, utcTime):
		self.UTCtime = utcTime

	def getUTCDateTime(self):
		return self.UTCtime

	def getTZ(self):
		return self.timezoneStr
		
	def getPytzValue(self):
		print "TZ INFO: timezoneSTR=", self.timezoneStr, "timezoneINT=", pytz.timezone(self.timezoneStr)
		return pytz.timezone(self.timezoneStr)

	def getLocationFromIPaddress(self, tzindex):
		if True:
			k = tzindex
			self.latitude 		= tzSample[k]["lat"]
			self.longitude 		= tzSample[k]["lon"]
			self.timezoneStr	= tzSample[k]["timezoneStr"]
			print ("Time Zone for {0}".format(tzSample[k]["name"]))
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


		#response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})

		rawResp = response.read()
		data = json.loads(rawResp)

		self.IP			 = data['ip']
		self.org		 = data['org']
		self.city 		 = data['city']
		self.country	 = data['country']
		self.region		 = data['region']
		self.coordinates = data['loc']
		coord = self.coordinates.split(',')
		self.latitude = 30.0444 #52.2297 #float(coord[0])
		self.longitude = 31.2357 #21.0122  #float(coord[1])
		# determine timezone and delta between local time and UTC
		self.timezoneStr	 = data['timezone']

		self.timezoneStr = "Etc/GMT+2" #"Europe/Warsaw"		############ test

		# initialize local and UTC time zones
		self.utcTZ 		= pytz.timezone('UTC')
		self.localTZ 	= pytz.timezone(self.timezoneStr)

		#print 'UTC tz: {0}\nLOCAL tz: {1}\n\n'.format(self.utcTZ, self.localTZ)
		print 'Your IP detail\n '
		print 'IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0} \ncoordinates : {5} \nTimeZone : {6}'.format(self.org,self.region,self.country,self.city,self.IP,self.coordinates,self.timezoneStr)
		print 'Latitude={0}'.format(self.latitude)
		print 'Longitude={0}'.format(self.longitude)


"""
	def solar_timestrXX(self, strDatetime, longit):
		dt = dt.datetime.strptime(strDatetime,  '%Y/%m/%d %H:%M:%S')

		# get timezone in minutes from GT to current location. 
		# When longitude is negative (west of GT), we need to change the sign
		tz = time.timezone
		if longit < 0:
			tz = -tz

		gamma = 2 * math.pi / 365 * (dt.timetuple().tm_yday - 1 + float(dt.hour - 12) / 24)
		eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma) \
				- 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))
		decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) \
			- 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma) \
			- 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma)
		time_offset = eqtime + 4 * longit
		tst = dt.hour * 60 + dt.minute + dt.second / 60 + time_offset
		self.solarT = dt.datetime.combine(dt.date(), datetime.time(0)) + datetime.timedelta(minutes=tst)
		print "calculated solartime=", self.solarT


		#time_offset = eqtime + (4 * longit)  - (tz/60)
		self.UTCoffsetInSeconds = tz  # in seconds
		print time.timezone/3600
		self.RelativeTimeToDateline = 86400/2 - abs(tz)
		self.AbsoluteTimeToDateline = 86400/2 - tz

		print "time zone=", self.UTCoffsetInSeconds/3600
		print "time-to-dateline=", self.RelativeTimeToDateline/3600 
		return self.solarT
"""


