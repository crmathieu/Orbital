from planetsdata import EPOCH_2000_JD, EPOCH_1970_JD
import datetime

# given a year, returns the Vernal equinox date
def Vernal(year):
	delta_y = year-2000
	julian_timestamp = EPOCH_2000_JD + 78.814 + 365.24236 * delta_y + 5.004e-8 * (delta_y)**2 - 2.87e-12 * (delta_y)**3 - 4.6e-16 * (delta_y)**4
	# we need to convert Julian to Unix timestamp before using the "fromtimestamp" function
	unix_timestamp = julian2unix(julian_timestamp)
	vernal_date = datetime.datetime.fromtimestamp(unix_timestamp)
	print julian_timestamp, vernal_date
	return vernal_date

def Vernal2(year):
    julian_timestamp = initialGuess(0, year)
    unix_timestamp = julian2unix(julian_timestamp)
    vernal_date = datetime.datetime.fromtimestamp(unix_timestamp)
    print julian_timestamp, vernal_date
    return vernal_date


def unix2julian(unix):
	return (unix / 86400) + EPOCH_1970_JD

def julian2unix(julian):
	return (julian - EPOCH_1970_JD) * 86400.0


# Calculate initial guess for the Julian Date of the Equinox or Solstice of a Given Year
# (Meeus Astronmical Algorithms Chapter 27)
def initialGuess(dtype, year): # Valid for years 1000 to 3000

    Y = (year-2000)/1000
    if dtype == 0:      # Vernal Equinox    (VE)
        return 2451623.80984 + 365242.37404 * Y + 0.05169 * Y**2 - 0.00411 * Y**3 - 0.00057 * Y**4
    elif dtype == 1:    # Summer Solstice   (SS)
        return 2451716.56767 + 365241.62603 * Y + 0.00325 * Y**2 + 0.00888 * Y**3 - 0.00030 * Y**4
    elif dtype == 2:    # Autumn Equinox    (AE)
        return 2451810.21715 + 365242.01767 * Y - 0.11575 * Y**2 + 0.00337 * Y**3 + 0.00078 * Y**4
    elif dtype == 3:    # Winter Solstice   (WS)
        return 2451900.05952 + 365242.74049 * Y - 0.06223 * Y**2 - 0.00823 * Y**3 + 0.00032 * Y**4
    return 0
