#from scipy.sparse.csgraph import _validation
import urllib2
import httplib
import re
import json
import sys
import math

import pytz
import datetime as dt
import time

"""
TimeLoc - time management

"""
class Timeloc:
	def __init__(self):
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

		# initialize IP and lat/long info
		self.IP			 = data['ip']
		self.org		 = data['org']
		self.city 		 = data['city']
		self.country	 = data['country']
		self.region		 = data['region']
		self.coordinates = data['loc']      # 47.6104,-122.2007
		coord = self.coordinates.split(',')
		self.latitude = float(coord[0])
		self.longitude = float(coord[1])
		# determine timezone and delta between local time and UTC
		self.timezoneStr	 = data['timezone']

		# initialize local and UTC time zones
		self.utcTZ 		= pytz.timezone('UTC')
		self.localTZ 	= pytz.timezone(self.timezoneStr)

		print 'Your IP detail\n '
		print 'IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0} \ncoordinates : {5} \nTimeZone : {6}'.format(self.org,self.region,self.country,self.city,self.IP,self.coordinates,self.timezoneStr)
		print self.latitude
		print self.longitude


		self.UTCtime 	 	= dt.datetime.utcnow()
		self.localdatetime 	= dt.datetime.now(tz=pytz.timezone(self.timezoneStr))
		#self.UTCtime 	 = time.gmtime()

		# determine the difference between local TZ and UTC in seconds. The datetime.now() provides
		# a aware date time containing daylight saving time (dst) information, to figure out the exact
		# time difference depending on the time of year
		self.timezoneInSec = self.tz_diff(dt.datetime.now(), self.localTZ, self.utcTZ) 


		# /////////////////////////
		# get timezone in seconds from GT to current location. 
		# When longitude is negative (west of GT), we need to change the sign
		#self.timezoneInSec = #time.timezone

		if self.longitude < 0:
			self.timezoneInSec *= -1

		self.utcDeltaInSecondsFromLocal = - self.timezoneInSec
		print "seconds from local to UTC", self.utcDeltaInSecondsFromLocal

		self.UTCoffsetInSeconds = self.timezoneInSec  # in seconds
		print self.timezoneInSec/3600, " hours from UTC"

		self.RelativeTimeToDateline = 86400/2 - abs(self.timezoneInSec)
		self.AbsoluteTimeToDateline = 86400/2 - self.timezoneInSec

		print "time zone from UTC=", self.UTCoffsetInSeconds/3600
		print "time zone to dateline=", self.RelativeTimeToDateline/3600 

		# /////////////////////////

		#self.localtime = time.localtime(time.time())
		#print "Local current time :", self.localtime
		#print self.solar_time(self.localtime, self.longitude)
		print self.setSolarTime()

		#dt = datetime.strptime("2020/04/03 7:30:00", '%Y/%m/%d %H:%M:%S')
		#dt = datetime.now()
		#date_time = dt.strftime("%Y/%m/%d %H:%M:%S")
		#print self.solar_timestr(date_time, self.longitude)

		#now = datetime.now()
		#date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
		#print("date and time:",date_time)	

		#utc = pytz.timezone('UTC')
		#vancouver=pytz.timezone(self.timezoneStr)

		#print "~~~~~~~~~~~~~~~TIME-DIFFF", self.tz_diff(dt.datetime.now(),vancouver, utc)
		#d = dt.datetime.now()
		#print "ZZZZZZZZZZZZZZZZZZZZ TIME-DIFF", (utc.localize(d) - vancouver.localize(d)).seconds/3600.0

	def tz_diff(self, date, tz_from, tz_to):
		'''
		Returns the difference in seconds between tz_from and tz_to
		for a given date. 
			- If tz_from is West of tz_to, the # of hours is correct.
			- If tz_from is East of tz_to, the # of hours is augmented with 12 hours.

		'''
		if self.longitude < 0:
			# west of UTC
			return (tz_from.localize(date) - tz_to.localize(date)).seconds
		else: 
			# east of UTC
			return (tz_to.localize(date) - tz_from.localize(date)).seconds

	    #d = pd.to_datetime(date)

	def utc2localXX(self, utc):
	    epoch = time.mktime(utc.timetuple())
	    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
	    return utc + offset

	def setSolarTime(self):
		#self.localdatetime = dt.datetime.now()  #time.localtime() #time.time())
		print "Local current time :", self.localdatetime
		# to set solar time, we need a struct of type time.struct_time, hence we pass time.localtime()
		#return self.getSolarTime(time.localtime(), self.longitude) #self.localtime, self.longitude)
		return self.getSolarTime(self.datetime_to_StructTime(self.localdatetime), self.longitude) #self.localtime, self.longitude)

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

		time_offset = eqtime + (4 * longitude)  - (self.timezoneInSec/60)
		print "Time Offset = ", time_offset

		tst = localtime.tm_hour * 60 + localtime.tm_min + localtime.tm_sec / 60 + time_offset
		#self.solar_time = dt.datetime.combine(dt.date(), time(0)) + timedelta(minutes=tst)
		#self.solar_time = dt.datetime.combine(dt.datetime.date(), time(0)) + timedelta(minutes=tst)
		self.solarT = (tst / 4) - 180

		print "solar Time=", self.solarT, "day"
		return self.solarT

	def getSolarTimeSAVE(self, dt, longit):
		"""
    	return ha

		if len(sys.argv) != 4:
			print 'Usage: hour_angle.py [YYYY/MM/DD] [HH:MM:SS] [longitude]'
			sys.exit()
		else:
			dt = datetime.strptime(sys.argv[1] + ' ' + sys.argv[2], '%Y/%m/%d %H:%M:%S')
			longit = float(sys.argv[3])
		"""

		#gamma = 2 * pi / 365 * (dt.timetuple().tm_yday - 1 + float(dt.hour - 12) / 24)
		gamma = 2 * math.pi / 365 * (dt.tm_yday - 1 + float(dt.tm_hour - 12) / 24)
		eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma) \
				- 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))
		decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) \
			- 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma) \
			- 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma)

		# get timezone in seconds from GT to current location. 
		# When longitude is negative (west of GT), we need to change the sign
		tz = time.timezone
		if longit < 0:
			tz = -tz

		self.utcDeltaInSecondsFromLocal = -tz
		print "seconds from local to UTC", self.utcDeltaInSecondsFromLocal

		time_offset = eqtime + (4 * longit)  - (tz/60)
		self.UTCoffsetInSeconds = tz  # in seconds
		print time.timezone/3600, " hours from UTC"
		self.RelativeTimeToDateline = 86400/2 - abs(tz)
		self.AbsoluteTimeToDateline = 86400/2 - tz

		#tst = dt.hour * 60 + dt.minute + dt.second / 60 + time_offset
		tst = dt.tm_hour * 60 + dt.tm_min + dt.tm_sec / 60 + time_offset
		#self.solar_time = dt.datetime.combine(dt.date(), time(0)) + timedelta(minutes=tst)
		#self.solar_time = dt.datetime.combine(dt.datetime.date(), time(0)) + timedelta(minutes=tst)
		self.solarT = (tst / 4) - 180

		print "time zone=", self.UTCoffsetInSeconds/3600
		print "time-to-dateline=", self.RelativeTimeToDateline/3600 
		print "solar Time=", self.solarT
		return self.solarT

	def RelativeTimeToUtcInSec(self):
		return self.utcDeltaInSecondsFromLocal

	def Time2degree(self, time_in_sec):
		# 15 deg corresponds to 1hour (3600s). 1s -> 15/3600
		return time_in_sec * 15/3600

	# returns local time as a structure:
	# time.struct_time(tm_year=2021, tm_mon=4, tm_mday=15, tm_hour=13, tm_min=34, tm_sec=41, tm_wday=3, tm_yday=105, tm_isdst=1) 
	def getLocalDateTime(self):
		print "GETlocaltime=", self.localdatetime
		return self.localdatetime

	def setLocaltimeFromUTC(self, utcTime): # utcTime must a datetime class
		self.localdatetime = utcTime + something

	def setUTCDateTime(self, utcTime):
		self.UTCtime = utcTime

	def getUTCDateTime(self):
		print "GETutctime=", self.UTCtime
		return self.UTCtime

	def updateUTCtime(self):
		#self.UTCtime = time.gmtime()
		self.UTCtime = dt.datetime.utcnow()
		print "GETutctime=", self.UTCtime
		return self.UTCtime

	def getTZ(self):
		return self.timezoneStr
		
	def getPytzValue(self):
		print "TZ INFO: timezoneSTR=", self.timezoneStr, "timezoneINT=", pytz.timezone(self.timezoneStr)
		return pytz.timezone(self.timezoneStr)

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


