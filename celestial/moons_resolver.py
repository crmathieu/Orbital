# moons_resolver.py

from constants import *

MOONS = {
	"moon": {
    "Id": {
      "name": "moon",
      "iau_name": "Moon",
      "jpl_designation": "301",
      "horizons_id": "301",
      "spk_id": "301",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "earth",
      "center": "500@399",
      "synonyms": ["moon", "luna", "earth moon"]
    },

    "physical": {
      "texture": "./img/moon",
      "mass_kg": 7.342e22,
      "radius_m": 1737400.0,
      "GM": 4902800066.0,
      "rotation_period_in_solar_d": 27.321661,
      "axial_tilt_deg": 6.687
    },

    "rotation": {
      "pole_ra": 269.9949,
      "pole_dec": 66.5392,
      "prime_meridian": 38.3213
    }
  },

  "phobos": {
    "Id": {
      "name": "phobos",
      "iau_name": "Phobos",
      "jpl_designation": "401",
      "horizons_id": "401",
      "spk_id": "401",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "mars",
      "center": "500@499",
      "synonyms": ["phobos"]
    },

    "physical": {
      "texture": "./img/phobos",
      "mass_kg": 1.0659e16,
      "radius_m": 11266.7,
      "GM": 7.087e5,
      "rotation_period_in_solar_d": 0.31891023,
      "axial_tilt_deg": 0.0
    },

    "rotation": {
      "pole_ra": 317.68,
      "pole_dec": 52.90,
      "prime_meridian": 35.06
    }
  },

  "deimos": {
    "Id": {
      "texture": "./img/deimos",
      "name": "deimos",
      "iau_name": "Deimos",
      "jpl_designation": "402",
      "horizons_id": "402",
      "spk_id": "402",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "mars",
      "center": "500@499",
      "synonyms": ["deimos"]
    },

    "physical": {
      "mass_kg": 1.4762e15,
      "radius_m": 6200.0,
      "GM": 9.615e4,
      "rotation_period_in_solar_d": 1.26244,
      "axial_tilt_deg": 0.0
    },

    "rotation": {
      "pole_ra": 316.65,
      "pole_dec": 53.52,
      "prime_meridian": 79.41
    }
  },

  "io": {
    "Id": {
      "name": "io",
      "iau_name": "Io",
      "jpl_designation": "501",
      "horizons_id": "501",
      "spk_id": "501",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "jupiter",
      "center": "500@599",
      "synonyms": ["io"]
    },
    "physical": {
      "texture": "./img/io",
      "mass_kg": 8.931938e22,
      "radius_m": 1821500.0,
      "GM": 5959.916e9,
      "rotation_period_in_solar_d": 1.769137786,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 268.05,
      "pole_dec": 64.50,
      "prime_meridian": 200.39
    }
  },

  "europa": {
    "Id": {
      "name": "europa",
      "iau_name": "Europa",
      "jpl_designation": "502",
      "horizons_id": "502",
      "spk_id": "502",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "jupiter",
      "center": "500@599",
      "synonyms": ["europa"]
    },
    "physical": {
      "texture": "./img/europa",
      "mass_kg": 4.799844e22,
      "radius_m": 1560800.0,
      "GM": 3202.719e9,
      "rotation_period_in_solar_d": 3.551181,
      "axial_tilt_deg": 0.1
    },
    "rotation": {
      "pole_ra": 268.08,
      "pole_dec": 64.51,
      "prime_meridian": 36.022
    }
  },

  "ganymede": {
    "Id": {
      "name": "ganymede",
      "iau_name": "Ganymede",
      "jpl_designation": "503",
      "horizons_id": "503",
      "spk_id": "503",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "jupiter",
      "center": "500@599",
      "synonyms": ["ganymede"]
    },
    "physical": {
      "texture": "./img/ganymede",
      "mass_kg": 1.4819e23,
      "radius_m": 2634100.0,
      "GM": 9887.834e9,
      "rotation_period_in_solar_d": 7.154553,
      "axial_tilt_deg": 0.33
    },
    "rotation": {
      "pole_ra": 268.20,
      "pole_dec": 64.57,
      "prime_meridian": 44.064
    }
  },

  "callisto": {
    "Id": {
      "name": "callisto",
      "iau_name": "Callisto",
      "jpl_designation": "504",
      "horizons_id": "504",
      "spk_id": "504",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "jupiter",
      "center": "500@599",
      "synonyms": ["callisto"]
    },
    "physical": {
      "texture": "./img/callisto",
      "mass_kg": 1.075938e23,
      "radius_m": 2410300.0,
      "GM": 7179.289e9,
      "rotation_period_in_solar_d": 16.689018,
      "axial_tilt_deg": 0.4
    },
    "rotation": {
      "pole_ra": 268.72,
      "pole_dec": 64.83,
      "prime_meridian": 259.51
    }
  },

  "metis": {
    "Id": {
      "name": "metis",
      "iau_name": "Metis",
      "jpl_designation": "516",
      "horizons_id": "516",
      "spk_id": "516",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "jupiter",
      "center": "500@599",
      "synonyms": ["metis"]
    },
    "physical": {
      "mass_kg": 9.56e16,
      "radius_m": 21500.0,
      "GM": 0.0203e9,
      "rotation_period_in_solar_d": 0.294780,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 268.05,
      "pole_dec": 64.50,
      "prime_meridian": 200.39
    }
  },

  "adrastea": {
    "Id": {
      "name": "adrastea",
      "iau_name": "Adrastea",
      "jpl_designation": "515",
      "horizons_id": "515",
      "spk_id": "515",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "jupiter",
      "center": "500@599",
      "synonyms": ["adrastea"]
    },
    "physical": {
      "mass_kg": 7.49e15,
      "radius_m": 8200.0,
      "GM": 0.0010e9,
      "rotation_period_in_solar_d": 0.298260,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 268.05,
      "pole_dec": 64.50,
      "prime_meridian": 200.39
    }
  },

  "amalthea": {
    "Id": {
      "name": "amalthea",
      "iau_name": "Amalthea",
      "jpl_designation": "505",
      "horizons_id": "505",
      "spk_id": "505",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "jupiter",
      "center": "500@599",
      "synonyms": ["amalthea"]
    },
    "physical": {
      "mass_kg": 2.08e18,
      "radius_m": 83000.0,
      "GM": 0.140e9,
      "rotation_period_in_solar_d": 0.498179,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 268.05,
      "pole_dec": 64.50,
      "prime_meridian": 200.39
    }
  },

  "thebe": {
    "Id": {
      "name": "thebe",
      "iau_name": "Thebe",
      "jpl_designation": "514",
      "horizons_id": "514",
      "spk_id": "514",
      "object_class": MOON,
      "moon_class": "ASYNCHRONOUS",
      "orbiting": "jupiter",
      "center": "500@599",
      "synonyms": ["thebe"]
    },
    "physical": {
      "mass_kg": 4.3e17,
      "radius_m": 49000.0,
      "GM": 0.043e9,
      "rotation_period_in_solar_d": None,
      "axial_tilt_deg": None
    },
    "rotation": {
      "pole_ra": None,
      "pole_dec": None,
      "prime_meridian": None
    }
  },


  "mimas": {
    "Id": {
      "name": "mimas",
      "iau_name": "Mimas",
      "jpl_designation": "601",
      "horizons_id": "601",
      "spk_id": "601",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "saturn",
      "center": "500@699",
      "synonyms": ["mimas"]
    },
    "physical": {
      "mass_kg": 3.7493e19,
      "radius_m": 198200.0,
      "GM": 2.503e9,
      "rotation_period_in_solar_d": 0.9424218,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 40.66,
      "pole_dec": 83.52,
      "prime_meridian": 331.45
    }
  },

  "enceladus": {
    "Id": {
      "name": "enceladus",
      "iau_name": "Enceladus",
      "jpl_designation": "602",
      "horizons_id": "602",
      "spk_id": "602",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "saturn",
      "center": "500@699",
      "synonyms": ["enceladus"]
    },
    "physical": {
      "mass_kg": 1.08022e20,
      "radius_m": 252100.0,
      "GM": 7.210e9,
      "rotation_period_in_solar_d": 1.370218,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 40.66,
      "pole_dec": 83.52,
      "prime_meridian": 2.82
    }
  },

  "tethys": {
    "Id": {
      "name": "tethys",
      "iau_name": "Tethys",
      "jpl_designation": "603",
      "horizons_id": "603",
      "spk_id": "603",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "saturn",
      "center": "500@699",
      "synonyms": ["tethys"]
    },
    "physical": {
      "mass_kg": 6.17449e20,
      "radius_m": 531100.0,
      "GM": 41.210e9,
      "rotation_period_in_solar_d": 1.887802,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 40.66,
      "pole_dec": 83.52,
      "prime_meridian": 10.45
    }
  },

  "dione": {
    "Id": {
      "name": "dione",
      "iau_name": "Dione",
      "jpl_designation": "604",
      "horizons_id": "604",
      "spk_id": "604",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "saturn",
      "center": "500@699",
      "synonyms": ["dione"]
    },
    "physical": {
      "mass_kg": 1.095452e21,
      "radius_m": 561400.0,
      "GM": 73.112e9,
      "rotation_period_in_solar_d": 2.736915,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 40.66,
      "pole_dec": 83.52,
      "prime_meridian": 357.6
    }
  },

  "rhea": {
    "Id": {
      "name": "rhea",
      "iau_name": "Rhea",
      "jpl_designation": "605",
      "horizons_id": "605",
      "spk_id": "605",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "saturn",
      "center": "500@699",
      "synonyms": ["rhea"]
    },
    "physical": {
      "mass_kg": 2.306518e21,
      "radius_m": 763800.0,
      "GM": 153.94e9,
      "rotation_period_in_solar_d": 4.518212,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 40.38,
      "pole_dec": 83.55,
      "prime_meridian": 235.16
    }
  },

  "titan": {
    "Id": {
      "name": "titan",
      "iau_name": "Titan",
      "jpl_designation": "606",
      "horizons_id": "606",
      "spk_id": "606",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "saturn",
      "center": "500@699",
      "synonyms": ["titan"]
    },
    "physical": {
      "texture": "./img/titan",    
      "mass_kg": 1.34553e23,
      "radius_m": 2575000.0,
      "GM": 8978.138e9,
      "rotation_period_in_solar_d": 15.945421,
      "axial_tilt_deg": 0.3
    },
    "rotation": {
      "pole_ra": 36.41,
      "pole_dec": 83.94,
      "prime_meridian": 186.5855
    }
  },

  "iapetus": {
    "Id": {
      "name": "iapetus",
      "iau_name": "Iapetus",
      "jpl_designation": "608",
      "horizons_id": "608",
      "spk_id": "608",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "saturn",
      "center": "500@699",
      "synonyms": ["iapetus"]
    },
    "physical": {
      "mass_kg": 1.805635e21,
      "radius_m": 734500.0,
      "GM": 120.503e9,
      "rotation_period_in_solar_d": 79.330183,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 318.16,
      "pole_dec": 75.03,
      "prime_meridian": 355.2
    }
  },

  "hyperion": {
    "Id": {
      "name": "hyperion",
      "iau_name": "Hyperion",
      "jpl_designation": "607",
      "horizons_id": "607",
      "spk_id": "607",
      "object_class": MOON,
      "moon_class": "ASYNCHRONOUS",
      "orbiting": "saturn",
      "center": "500@699",
      "synonyms": ["hyperion"]
    },
    "physical": {
      "mass_kg": 5.6e18,
      "radius_m": 135000.0,
      "GM": 0.372e9,
      "rotation_period_in_solar_d": None,
      "axial_tilt_deg": None
    },
    "rotation": {
      "pole_ra": None,
      "pole_dec": None,
      "prime_meridian": None
    }
  },


  "miranda": {
    "Id": {
      "name": "miranda",
      "iau_name": "Miranda",
      "jpl_designation": "701",
      "horizons_id": "701",
      "spk_id": "701",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "uranus",
      "center": "500@799",
      "synonyms": ["miranda"]
    },
    "physical": {
      "mass_kg": 6.59e19,
      "radius_m": 235800.0,
      "GM": 4.4e9,
      "rotation_period_in_solar_d": 1.413479,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 257.43,
      "pole_dec": -15.08,
      "prime_meridian": 30.70
    }
  },

  "ariel": {
    "Id": {
      "name": "ariel",
      "iau_name": "Ariel",
      "jpl_designation": "702",
      "horizons_id": "702",
      "spk_id": "702",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "uranus",
      "center": "500@799",
      "synonyms": ["ariel"]
    },
    "physical": {
      "mass_kg": 1.353e21,
      "radius_m": 578900.0,
      "GM": 90.0e9,
      "rotation_period_in_solar_d": 2.520379,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 257.43,
      "pole_dec": -15.10,
      "prime_meridian": 32.62
    }
  },

  "umbriel": {
    "Id": {
      "name": "umbriel",
      "iau_name": "Umbriel",
      "jpl_designation": "703",
      "horizons_id": "703",
      "spk_id": "703",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "uranus",
      "center": "500@799",
      "synonyms": ["umbriel"]
    },
    "physical": {
      "mass_kg": 1.172e21,
      "radius_m": 584700.0,
      "GM": 75.0e9,
      "rotation_period_in_solar_d": 4.144177,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 257.43,
      "pole_dec": -15.10,
      "prime_meridian": 314.90
    }
  },

  "titania": {
    "Id": {
      "name": "titania",
      "iau_name": "Titania",
      "jpl_designation": "704",
      "horizons_id": "704",
      "spk_id": "704",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "uranus",
      "center": "500@799",
      "synonyms": ["titania"]
    },
    "physical": {
      "mass_kg": 3.527e21,
      "radius_m": 788900.0,
      "GM": 228.2e9,
      "rotation_period_in_solar_d": 8.706234,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 257.43,
      "pole_dec": -15.10,
      "prime_meridian": 99.77
    }
  },

  "oberon": {
    "Id": {
      "name": "oberon",
      "iau_name": "Oberon",
      "jpl_designation": "705",
      "horizons_id": "705",
      "spk_id": "705",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "uranus",
      "center": "500@799",
      "synonyms": ["oberon"]
    },
    "physical": {
      "mass_kg": 3.014e21,
      "radius_m": 761400.0,
      "GM": 192.4e9,
      "rotation_period_in_solar_d": 13.463234,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 257.43,
      "pole_dec": -15.10,
      "prime_meridian": 279.06
    }
  },

  "triton": {
    "Id": {
      "name": "triton",
      "iau_name": "Triton",
      "jpl_designation": "801",
      "horizons_id": "801",
      "spk_id": "801",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "neptune",
      "center": "500@899",
      "synonyms": ["triton"]
    },
    "physical": {
      "mass_kg": 2.139e22,
      "radius_m": 1353400.0,
      "GM": 1427.6e9,
      "rotation_period_in_solar_d": 5.876854,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 299.36,
      "pole_dec": 41.17,
      "prime_meridian": 296.53
    }
  },

  "proteus": {
    "Id": {
      "name": "proteus",
      "iau_name": "Proteus",
      "jpl_designation": "808",
      "horizons_id": "808",
      "spk_id": "808",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "neptune",
      "center": "500@899",
      "synonyms": ["proteus"]
    },
    "physical": {
      "mass_kg": 4.4e19,
      "radius_m": 210000.0,
      "GM": 2.9e9,
      "rotation_period_in_solar_d": 1.122314,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 299.36,
      "pole_dec": 41.17,
      "prime_meridian": 296.53
    }
  },

  "nereid": {
    "Id": {
      "name": "nereid",
      "iau_name": "Nereid",
      "jpl_designation": "802",
      "horizons_id": "802",
      "spk_id": "802",
      "object_class": MOON,
      "moon_class": "ASYNCHRONOUS",
      "orbiting": "neptune",
      "center": "500@899",
      "synonyms": ["nereid"]
    },
    "physical": {
      "mass_kg": 3.1e19,
      "radius_m": 170000.0,
      "GM": 2.06e9,
      "rotation_period_in_solar_d": None,
      "axial_tilt_deg": None
    },
    "rotation": {
      "pole_ra": None,
      "pole_dec": None,
      "prime_meridian": None
    }
  },

  "larissa": {
    "Id": {
      "name": "larissa",
      "iau_name": "Larissa",
      "jpl_designation": "807",
      "horizons_id": "807",
      "spk_id": "807",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "neptune",
      "center": "500@899",
      "synonyms": ["larissa"]
    },
    "physical": {
      "mass_kg": 4.9e18,
      "radius_m": 97000.0,
      "GM": 0.32e9,
      "rotation_period_in_solar_d": 0.554654,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 299.36,
      "pole_dec": 41.17,
      "prime_meridian": 296.53
    }
  },

  "galatea": {
    "Id": {
      "name": "galatea",
      "iau_name": "Galatea",
      "jpl_designation": "806",
      "horizons_id": "806",
      "spk_id": "806",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "neptune",
      "center": "500@899",
      "synonyms": ["galatea"]
    },
    "physical": {
      "mass_kg": 2.12e18,
      "radius_m": 88000.0,
      "GM": 0.14e9,
      "rotation_period_in_solar_d": 0.428745,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 299.36,
      "pole_dec": 41.17,
      "prime_meridian": 296.53
    }
  },

  "despina": {
    "Id": {
      "name": "despina",
      "iau_name": "Despina",
      "jpl_designation": "805",
      "horizons_id": "805",
      "spk_id": "805",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "neptune",
      "center": "500@899",
      "synonyms": ["despina"]
    },
    "physical": {
      "mass_kg": 2.1e18,
      "radius_m": 75000.0,
      "GM": 0.14e9,
      "rotation_period_in_solar_d": 0.335002,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 299.36,
      "pole_dec": 41.17,
      "prime_meridian": 296.53
    }
  },

  "thalassa": {
    "Id": {
      "name": "thalassa",
      "iau_name": "Thalassa",
      "jpl_designation": "804",
      "horizons_id": "804",
      "spk_id": "804",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "neptune",
      "center": "500@899",
      "synonyms": ["thalassa"]
    },
    "physical": {
      "mass_kg": 3.5e17,
      "radius_m": 40000.0,
      "GM": 0.02e9,
      "rotation_period_in_solar_d": 0.311485,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 299.36,
      "pole_dec": 41.17,
      "prime_meridian": 296.53
    }
  },

  "naiad": {
    "Id": {
      "name": "naiad",
      "iau_name": "Naiad",
      "jpl_designation": "803",
      "horizons_id": "803",
      "spk_id": "803",
      "object_class": MOON,
      "moon_class": "SYNCHRONOUS",
      "orbiting": "neptune",
      "center": "500@899",
      "synonyms": ["naiad"]
    },
    "physical": {
      "mass_kg": 1.9e17,
      "radius_m": 33000.0,
      "GM": 0.012e9,
      "rotation_period_in_solar_d": 0.294396,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 299.36,
      "pole_dec": 41.17,
      "prime_meridian": 296.53
    }
  },

  "charon": {
    "Id": {
      "name": "charon",
      "iau_name": "Charon",
      "jpl_designation": "901",
      "horizons_id": "901",
      "spk_id": "901",
      "object_class": MOON,
      "object_role": BARYCENTER_MEMBER,
      "object_parent": 'pluto',
      "moon_class": "SYNCHRONOUS",
      "orbiting": "pluto-barycenter",
      "center": PLUTO_BARYCENTER,
      "synonyms": ["charon"]
    },
    "physical": {
      "texture": "./img/charon",
      "mass_kg": 1.586e21,
      "radius_m": 606000.0,
      "GM": 105.88e9,
      "rotation_period_in_solar_d": -6.387230,
      "axial_tilt_deg": 0.0
    },
    "rotation": {
      "pole_ra": 132.993,
      "pole_dec": -6.163,
      "prime_meridian": 122.695
    }
  },

  "nix": {
    "Id": {
      "name": "nix",
      "iau_name": "Nix",
      "jpl_designation": "902",
      "horizons_id": "902",
      "spk_id": "902",
      "object_class": MOON,
      "object_role": BARYCENTER_MEMBER,
      "object_parent": 'pluto',
      "moon_class": "ASYNCHRONOUS",
      "orbiting": "pluto-barycenter",
      "center": PLUTO_BARYCENTER,
      "synonyms": ["nix"]
    },
    "physical": {
      "mass_kg": 4.5e16,
      "radius_m": 25000.0,
      "GM": 0.003e9,
      "rotation_period_in_solar_d": None,
      "axial_tilt_deg": None
    },
    "rotation": {
      "pole_ra": None,
      "pole_dec": None,
      "prime_meridian": None
    }
  },

  "hydra": {
    "Id": {
      "name": "hydra",
      "iau_name": "Hydra",
      "jpl_designation": "903",
      "horizons_id": "903",
      "spk_id": "903",
      "object_class": MOON,
      "object_role": BARYCENTER_MEMBER,
      "object_parent": 'pluto',
      "moon_class": "ASYNCHRONOUS",
      "orbiting": "pluto-barycenter",
      "center": PLUTO_BARYCENTER,
      "synonyms": ["hydra"]
    },
    "physical": {
      "mass_kg": 4.8e16,
      "radius_m": 32000.0,
      "GM": 0.0032e9,
      "rotation_period_in_solar_d": None,
      "axial_tilt_deg": None
    },
    "rotation": {
      "pole_ra": None,
      "pole_dec": None,
      "prime_meridian": None
    }
  },

  "kerberos": {
    "Id": {
      "name": "kerberos",
      "iau_name": "Kerberos",
      "jpl_designation": "904",
      "horizons_id": "904",
      "spk_id": "904",
      "object_class": MOON,
      "object_parent": 'pluto',
      "object_role": BARYCENTER_MEMBER,
      "moon_class": "ASYNCHRONOUS",
      "orbiting": "pluto-barycenter",
      "center": PLUTO_BARYCENTER,
      "synonyms": ["kerberos"]
    },
    "physical": {
      "mass_kg": 1.6e16,
      "radius_m": 19000.0,
      "GM": 0.0011e9,
      "rotation_period_in_solar_d": None,
      "axial_tilt_deg": None
    },
    "rotation": {
      "pole_ra": None,
      "pole_dec": None,
      "prime_meridian": None
    }
  },

  "styx": {
    "Id": {
      "name": "styx",
      "iau_name": "Styx",
      "jpl_designation": "905",
      "horizons_id": "905",
      "spk_id": "905",
      "object_class": MOON,
      "object_parent": 'pluto',
      "object_role": BARYCENTER_MEMBER,
      "moon_class": "ASYNCHRONOUS",
      "orbiting": "pluto-barycenter",
      "center": PLUTO_BARYCENTER,
      "synonyms": ["styx"]
    },
    "physical": {
      "mass_kg": 7.5e15,
      "radius_m": 16000.0,
      "GM": 0.0005e9,
      "rotation_period_in_solar_d": None,
      "axial_tilt_deg": None
    },
    "rotation": {
      "pole_ra": None,
      "pole_dec": None,
      "prime_meridian": None
    }
  }
}




# ------------------------------------------------------------
# calculate J2 prcessession rates
# ------------------------------------------------------------
def j2_precession_rates(a_m, e, i_rad, planet):
    """
    Returns (Omega_dot_rad_day, omega_dot_rad_day) for J2 precession.

    Parameters
    ----------
    a_m : float
        Semi-major axis in meters (SI)
    e : float
        Eccentricity
    i_rad : float
        Inclination in radians (relative to planet's equator)
    planet : str
        Planet name ("Mars", "Jupiter", etc.)

    Returns
    -------
    (Omega_dot, omega_dot) in rad/day
    """

    import math
    from planetary_constants import PLANET_CONSTANTS

    if planet not in PLANET_CONSTANTS:
        return 0.0, 0.0

    # All SI-native
    J2 = PLANET_CONSTANTS[planet]["J2"]          # dimensionless
    R  = PLANET_CONSTANTS[planet]["radius_m"]    # meters
    mu = PLANET_CONSTANTS[planet]["GM"]          # m^3/s^2

    # Mean motion in rad/s (SI)
    n_rad_s = math.sqrt(mu / (a_m**3))

    # Convert to rad/day
    n = n_rad_s * 86400.0

    # J2 factor
    factor = J2 * (R / a_m)**2 / (1.0 - e*e)**2
    cosi = math.cos(i_rad)

    # Secular J2 precession rates (rad/day)
    Omega_dot = -1.5 * n * factor * cosi
    omega_dot =  0.75 * n * factor * (5.0*cosi*cosi - 1.0)

    return Omega_dot, omega_dot
    
