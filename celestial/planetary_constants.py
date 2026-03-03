# -*- coding: utf-8 -*-

# Authoritative planetary constants for the Solar System.
# Keys are planet names (your canonical identity).
# All values are SI-native.

# -*- coding: utf-8 -*-

# Authoritative planetary constants for the Solar System.
# Keys are planet names (canonical identity).
# All values are SI-native unless noted.
# Drift coefficients follow Meeus Chapter 31 (low precision, 1800–2050).


"""
    "mercury":  "mercury",
    "venus":    "venus",
    "earth":    "highres-earth-8192x4096-clouds",
    "mars":     "mars",
    "jupiter":  "source/2k_jupiter-PM-normalized",
    "saturn":   "saturn",
    "uranus":   "uranus",
    "neptune":  "source/2k_neptune-PM-normalized",

"""
PLANET_CONSTANTS = {

    "sun": {
        "object_id": "10",
        "GM": 1.32712440018e20,
        "J2": 0.0,
        "radius_m": 695700e3,
        "texture": "sun",
        "drift_coef": {
            "a": 0.0, "ar": 0.0,
            "e": 0.0, "er": 0.0,
            "i": 0.0, "ir": 0.0,
            "L": 0.0, "Lr": 0.0,
            "W": 0.0, "Wr": 0.0,
            "N": 0.0, "Nr": 0.0,
            "b": 0.0, "c": 0.0, "s": 0.0, "f": 0.0
        },
        "precession": {
            "pole_ra_deg": 286.13,
            "pole_ra_rate_deg_day": 0.0,
            "pole_dec_deg": 63.87,
            "pole_dec_rate_deg_day": 0.0,
            "prime_meridian_deg": 84.176,
            "prime_meridian_rate_deg_day": 14.1844000
        }


    },

    "mercury": {
        "object_id": "199",
        "GM": 2.2032e13,
        "J2": 0.0,
        "radius_m": 2439.7e3,
        "texture": "mercury",
        "drift_coef": {
            "a": 0.38709843, "ar": 0.0,
            "e": 0.20563661, "er": 0.00002123,
            "i": 7.00559432, "ir": -0.00590158,
            "L": 252.25166724, "Lr": 149472.67486623,
            "W": 77.45771895, "Wr": 0.15940013,
            "N": 48.33961819, "Nr": -0.12214182,
            "b": 0.0, "c": 0.0, "s": 0.0, "f": 0.0
        },
        "precession": {
            "pole_ra_deg": 281.0097,
            "pole_ra_rate_deg_day": -0.0328,
            "pole_dec_deg": 61.4143,
            "pole_dec_rate_deg_day": -0.0049,
            "prime_meridian_deg": 329.5469,
            "prime_meridian_rate_deg_day": 6.1385025
        },
        "orbital_plane": {
            "inclination": 7.00487, 
            "long_ascending_node": 48.33167
        }
    },

    "venus": {
        "object_id": "299",
        "GM": 3.24859e14,
        "J2": 0.0,
        "radius_m": 6051.8e3,
        "texture": "venus",
        "drift_coef": {
            "a": 0.72332102, "ar": -0.00000026,
            "e": 0.00676399, "er": -0.00005107,
            "i": 3.39777545, "ir": 0.00043494,
            "L": 181.97970850, "Lr": 58517.81560260,
            "W": 131.76755713, "Wr": 0.05679648,
            "N": 76.67261496, "Nr": -0.27274174,
            "b": 0.0, "c": 0.0, "s": 0.0, "f": 0.0
        },
        "precession": {
            "pole_ra_deg": 272.76,
            "pole_ra_rate_deg_day": 0.0,
            "pole_dec_deg": 67.16,
            "pole_dec_rate_deg_day": 0.0,
            "prime_meridian_deg": 160.20,
            "prime_meridian_rate_deg_day": -1.4813688
        },
        "orbital_plane": {
            "inclination": 3.39471,  
            "long_ascending_node": 76.68069
        }        
    },

    "earth": {
        "object_id": "399",
        "GM": 3.98600435436e14,
        "J2": 1.08262668e-3,
        "radius_m": 6378.1363e3,
        "texture": "highres-earth-8192x4096-clouds",
        "drift_coef": {
            "a": 1.00000018, "ar": -0.00000003,
            "e": 0.01673163, "er": -0.00003661,
            "i": -0.00054346, "ir": -0.01337178,
            "L": 100.46691572, "Lr": 35999.37306329,
            "W": 102.93005885, "Wr": 0.31795260,
            "N": -5.11260389, "Nr": -0.24123856,
            "b": 0.0, "c": 0.0, "s": 0.0, "f": 0.0
        },
        "precession": {
            "pole_ra_deg": 0.00,
            "pole_ra_rate_deg_day": -0.641,
            "pole_dec_deg": 90.00,
            "pole_dec_rate_deg_day": -0.557,
            "prime_meridian_deg": 190.147,
            "prime_meridian_rate_deg_day": 360.9856235
        },        
        "orbital_plane": {
            "inclination": 0.00005,   
            "long_ascending_node": -11.26064
        }        
    },

    "mars": {
        "object_id": "499",
        "GM": 4.2828375214e13,
        "J2": 1.96045e-3,
        "radius_m": 3396.19e3,
        "texture": "mars",
        "drift_coef": {
            "a": 1.52371243, "ar": 0.00000097,
            "e": 0.09336511, "er": 0.00009149,
            "i": 1.85181869, "ir": -0.00724757,
            "L": -4.56813164, "Lr": 19140.29934243,
            "W": -23.91744784, "Wr": 0.45223625,
            "N": 49.71320984, "Nr": -0.26852431,
            "b": 0.0, "c": 0.0, "s": 0.0, "f": 0.0
        },
        "precession": {
            "pole_ra_deg": 317.68143,
            "pole_ra_rate_deg_day": -0.1061,
            "pole_dec_deg": 52.88650,
            "pole_dec_rate_deg_day": -0.0609,
            "prime_meridian_deg": 176.630,
            "prime_meridian_rate_deg_day": 350.89198226
        },
        "orbital_plane": {
            "inclination": 1.85061,    
            "long_ascending_node": 49.57854
        }        

    },

    "jupiter": {
        "object_id": "599",
        "GM": 1.266865349e17,
        "J2": 1.4697e-2,
        "radius_m": 71492e3,
        "texture": "source/2k_jupiter-PM-normalized",
        "drift_coef": {
            "a": 5.20248019, "ar": -0.00002864,
            "e": 0.04853590, "er": 0.00018026,
            "i": 1.29861416, "ir": -0.00322699,
            "L": 34.33479152, "Lr": 3034.90371757,
            "W": 14.27495244, "Wr": 0.18199196,
            "N": 100.29282654, "Nr": 0.13024619,
            "b": 0.0, "c": 0.0, "s": 0.0, "f": 0.0
        },
        "precession": {
            "pole_ra_deg": 268.056595,
            "pole_ra_rate_deg_day": -0.006499,
            "pole_dec_deg": 64.495303,
            "pole_dec_rate_deg_day": 0.008391,
            "prime_meridian_deg": 284.95,
            "prime_meridian_rate_deg_day": 870.536
        },
        "orbital_plane": {
            "inclination": 1.30530,     
            "long_ascending_node": 100.55615
        }        
    },

    "saturn": {
        "object_id": "699",
        "GM": 3.7931208e16,
        "J2": 1.6298e-2,
        "radius_m": 60268e3,
        "texture": "saturn",
        "drift_coef": {
            "a": 9.54149883, "ar": -0.00003065,
            "e": 0.05550825, "er": -0.00032044,
            "i": 2.49424102, "ir": 0.00451969,
            "L": 50.07571329, "Lr": 1222.11494724,
            "W": 92.86136063, "Wr": 0.54179478,
            "N": 113.63998702, "Nr": -0.25015002,
            "b": 0.0, "c": 0.0, "s": 0.0, "f": 0.0
        },
        "precession": {
            "pole_ra_deg": 40.589,
            "pole_ra_rate_deg_day": -0.036,
            "pole_dec_deg": 83.537,
            "pole_dec_rate_deg_day": -0.004,
            "prime_meridian_deg": 38.90,
            "prime_meridian_rate_deg_day": 810.7939024
        },
        "orbital_plane": {
            "inclination": 2.48446,     
            "long_ascending_node": 113.71504
        }        
 
    },

    "uranus": {
        "object_id": "799",
        "GM": 5.793939e15,
        "J2": 1.012e-2,
        "radius_m": 25559e3,
        "texture": "uranus",
        "drift_coef": {
            "a": 19.18797948, "ar": -0.00020455,
            "e": 0.04685740, "er": -0.00001550,
            "i": 0.77298127, "ir": -0.00180155,
            "L": 314.20276625, "Lr": 428.49512595,
            "W": 172.43404441, "Wr": 0.09266985,
            "N": 73.96250215, "Nr": 0.05739699,
            "b": 0.0, "c": 0.0, "s": 0.0, "f": 0.0
        },
        "precession": {
            "pole_ra_deg": 257.311,
            "pole_ra_rate_deg_day": 0.0,
            "pole_dec_deg": -15.175,
            "pole_dec_rate_deg_day": 0.0,
            "prime_meridian_deg": 203.81,
            "prime_meridian_rate_deg_day": -501.1600928
        },
        "orbital_plane": {
            "inclination": 0.76986,      
            "long_ascending_node": 74.22988
        }        

    },

    "neptune": {
        "object_id": "899",
        "GM": 6.836529e15,
        "J2": 4.0e-3,
        "radius_m": 24764e3,
        "texture": "source/2k_neptune-PM-normalized",
        "drift_coef": {
            "a": 30.06952752, "ar": 0.00006447,
            "e": 0.00895439, "er": 0.00000818,
            "i": 1.77005520, "ir": 0.00022400,
            "L": 304.22289287, "Lr": 218.46515314,
            "W": 46.68158724, "Wr": 0.01009938,
            "N": 131.78635853, "Nr": -0.00606302,
            "b": 0.0, "c": 0.0, "s": 0.0, "f": 0.0
        },
        "precession": {
            "pole_ra_deg": 299.36,
            "pole_ra_rate_deg_day": 0.70,
            "pole_dec_deg": 43.46,
            "pole_dec_rate_deg_day": 0.0,
            "prime_meridian_deg": 253.18,
            "prime_meridian_rate_deg_day": 536.3128492
        },
        "orbital_plane": {
            "inclination": 1.76917,       
            "long_ascending_node": 131.72169
        }        


    },

    "pluto": {
        "object_id": "999",
        "GM": 8.703e11,
        "J2": 0.0,
        "radius_m": 1188.3e3,
        "texture": "pluto3",
        "drift_coef": {
            "a": 39.48686035, "ar": 0.00449751,
            "e": 0.24885238, "er": 0.00006016,
            "i": 17.14104260, "ir": 0.00000501,
            "L": 238.96535011, "Lr": 145.20780515,
            "W": 224.09702598, "Wr": -0.00968827,
            "N": 110.30167986, "Nr": -0.00809981,
            "b": -0.01262724, "c": 0.0, "s": 0.0, "f": 0.0
        },
        "precession": {
            "pole_ra_deg": 313.02,
            "pole_ra_rate_deg_day": -0.001,
            "pole_dec_deg": 9.09,
            "pole_dec_rate_deg_day": 0.005,
            "prime_meridian_deg": 313.02,
            "prime_meridian_rate_deg_day": 56.3625225
        },        
        "orbital_plane": {
            "inclination": 17.14175,     
            "long_ascending_node": 110.30347
        }        
    }
}
