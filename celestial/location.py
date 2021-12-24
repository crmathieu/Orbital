#from scipy.sparse.csgraph import _validation
import urllib2
import httplib
import re
import json
import sys
import math

import pytz
import datetime
import time

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

		self.IP			 = data['ip']
		self.org		 = data['org']
		self.city 		 = data['city']
		self.country	 = data['country']
		self.region		 = data['region']
		self.coordinates = data['loc']      # 47.6104,-122.2007
		self.timezone	 = data['timezone']

		coord = self.coordinates.split(',')
		self.latitude = float(coord[0])
		self.longitude = float(coord[1])
		print 'Your IP detail\n '
		print 'IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0} \ncoordinates : {5} \nTimeZone : {6}'.format(self.org,self.region,self.country,self.city,self.IP,self.coordinates,self.timezone)
		print self.latitude
		print self.longitude

		#self.localtime = time.localtime(time.time())
		#print "Local current time :", self.localtime
		#print self.solar_time(self.localtime, self.longitude)
		print self.setSolarTime()

		#dt = datetime.datetime.strptime("2020/04/03 7:30:00", '%Y/%m/%d %H:%M:%S')
		#dt = datetime.datetime.now()
		#date_time = dt.strftime("%Y/%m/%d %H:%M:%S")
		#print self.solar_timestr(date_time, self.longitude)

		#now = datetime.now()
		#date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
		#print("date and time:",date_time)	

	def setSolarTime(self):
		self.localtime = time.localtime(time.time())
		print "Local current time :", self.localtime
		return self.getSolarTime(self.localtime, self.longitude)

	def getSolarTime(self, dt, longit):
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
		print time.timezone/3600
		self.RelativeTimeToDateline = 86400/2 - abs(tz)
		self.AbsoluteTimeToDateline = 86400/2 - tz

		#tst = dt.hour * 60 + dt.minute + dt.second / 60 + time_offset
		tst = dt.tm_hour * 60 + dt.tm_min + dt.tm_sec / 60 + time_offset
		#self.solar_time = datetime.datetime.combine(dt.date(), time(0)) + timedelta(minutes=tst)
		#self.solar_time = datetime.datetime.combine(datetime.datetime.date(), time(0)) + timedelta(minutes=tst)
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
	def getLocalTime(self):
		return self.localtime

	def getTZ(self):
		return self.timezone
		
	def getPytzValue(self):
		print "TZ INFO: timezoneSTR=", self.timezone, "timezoneINT=", pytz.timezone(self.timezone)
		return pytz.timezone(self.timezone)

"""
	def solar_timestrXX(self, strDatetime, longit):
		dt = datetime.datetime.strptime(strDatetime,  '%Y/%m/%d %H:%M:%S')

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
		self.solarT = datetime.datetime.combine(dt.date(), datetime.time(0)) + datetime.timedelta(minutes=tst)
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


