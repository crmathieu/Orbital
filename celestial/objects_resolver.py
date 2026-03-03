# -*- coding: utf-8 -*-
# objects_resolver.py

from constants import *

OBJECTS = {

    # -------------------------
    # Planets Objects
    # -------------------------
    "sun": {
        "synonyms": ["sun"],
        "horizons_rec_id": "10",
        "horizons_id": "10",
        "object_class": SUN,
        "iau_name": "Sun",
        "jpl_designation": "Sun",
        "center": "500@0",
        "orbiting": None,
        "end_date": None,
        "physical": {
            "texture": "./img/sun",
            "mass_kg": SUN_M,
            "radius_m": SUN_R,
            "rotation_period_in_solar_d": 25.38,
            "axial_tilt_deg": 7.25
        }
    },


    "mercury": {
        "synonyms": ["mercury"],
        "horizons_rec_id": "199",
        "horizons_id": "199",
        "object_class": INNER_PLANET,
        "iau_name": "Mercury",
        "jpl_designation": "Mercury",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "texture": "./img/mercury",
            "mass_kg": 3.3011e23,
            "radius_m": 2439700.0,
            "rotation_period_in_solar_d": 58.646,
            "axial_tilt_deg": 0.034
        }
    },

    "venus": {
        "synonyms": ["venus"],
        "horizons_rec_id": "299",
        "horizons_id": "299",
        "object_class": INNER_PLANET,
        "iau_name": "Venus",
        "jpl_designation": "Venus",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "texture": "./img/venus",
            "mass_kg": 4.8675e24,
            "radius_m": 6051800.0,
            "rotation_period_in_solar_d": -243.025,
            "axial_tilt_deg": 177.36
        }
    },
    
    "earth": {
        "synonyms": ["earth"],
        "horizons_rec_id": "399",
        "horizons_id": "399",
        "object_class": INNER_PLANET,
        "iau_name": "Earth",
        "jpl_designation": "Earth",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "texture": "./img/highres-earth-8192x4096-clouds",
            "mass_kg": 5.97219e24,
            "radius_m": 6378137.0,
            "rotation_period_in_solar_d": 0.99726968,
            "axial_tilt_deg": 23.439281
        }
    },

    "mars": {
        "synonyms": ["mars"],
        "horizons_rec_id": "499",
        "horizons_id": "499",
        "object_class": INNER_PLANET,
        "iau_name": "Mars",
        "jpl_designation": "Mars",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "texture": "./img/mars",
            "mass_kg": 6.4171e23,
            "radius_m": 3389500.0,
            "rotation_period_in_solar_d": 1.025957,
            "axial_tilt_deg": 25.19
        }
    },

    "jupiter": {
        "synonyms": ["jupiter"],
        "horizons_rec_id": "599",
        "horizons_id": "599",
        "object_class": "OUTER_PLANET",
        "iau_name": "Jupiter",
        "jpl_designation": "Jupiter",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "texture": "./img/source/2k_jupiter-PM-normalized",
            "mass_kg": 1.89813e27,
            "radius_m": 69911000.0,
            "rotation_period_in_solar_d": 0.41354,
            "axial_tilt_deg": 3.13
        }
    },

    "saturn": {
        "synonyms": ["saturn"],
        "horizons_rec_id": "699",
        "horizons_id": "699",
        "object_class": "OUTER_PLANET",
        "iau_name": "Saturn",
        "jpl_designation": "Saturn",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "texture": "./img/saturn",
            "mass_kg": 5.6834e26,
            "radius_m": 58232000.0,
            "rotation_period_in_solar_d": 0.44401,
            "axial_tilt_deg": 26.73
        }
    },

    "uranus": {
        "synonyms": ["uranus"],
        "horizons_rec_id": "799",
        "horizons_id": "799",
        "object_class": "OUTER_PLANET",
        "iau_name": "Uranus",
        "jpl_designation": "Uranus",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "texture":"./img/uranus",
            "mass_kg": 8.6810e25,
            "radius_m": 25362000.0,
            "rotation_period_in_solar_d": -0.71833,
            "axial_tilt_deg": 97.77
        }
    },

    "neptune": {
        "synonyms": ["neptune"],
        "horizons_rec_id": "899",
        "horizons_id": "899",
        "object_class": "OUTER_PLANET",
        "iau_name": "Neptune",
        "jpl_designation": "Neptune",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "texture": "./img/source/2k_neptune-PM-normalized",
            "mass_kg": 1.02413e26,
            "radius_m": 24622000.0,
            "rotation_period_in_solar_d": 0.67125,
            "axial_tilt_deg": 28.32
        }
    },

    "pluto": {
        "synonyms": ["pluto", "134340 pluto"],
        "horizons_rec_id": "134340",
        "horizons_id": "134340",
        "object_class": DWARF_PLANET,
        "iau_name": "Pluto",
        "jpl_designation": "134340 Pluto",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "texture": "./img/pluto3",
            "mass_kg": 1.303e22,
            "radius_m": 1188300.0,
            "rotation_period_in_solar_d": -6.3872,
            "axial_tilt_deg": 119.61
        }
    },


    # -------------------------
    # Trans‑Neptunian Objects
    # -------------------------

    "eris": {
        "synonyms": ["eris", "136199 eris"],
        "horizons_rec_id": "136199",
        "horizons_id": "136199",
        "object_class": DWARF_PLANET,
        "iau_name": "Eris",
        "jpl_designation": "136199 Eris",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "texture": "./img/eris",
            "mass_kg": 1.6466e22,
            "radius_m": 1163000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "haumea": {
        "synonyms": ["haumea", "136108 haumea"],
        "horizons_rec_id": "136108",
        "horizons_id": "136108",
        "object_class": DWARF_PLANET,
        "iau_name": "Haumea",
        "jpl_designation": "136108 Haumea",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "texture": "./img/haumea",
            "mass_kg": 4.006e21,
            "radius_m": 816000.0,
            "rotation_period_in_solar_d": 0.1631,
            "axial_tilt_deg": 28.0
        }
    },

    "makemake": {
        "synonyms": ["makemake", "136472 makemake"],
        "horizons_rec_id": "136472",
        "horizons_id": "136472",
        "object_class": DWARF_PLANET,
        "iau_name": "Makemake",
        "jpl_designation": "136472 Makemake",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "texture": "./img/makemake",
            "mass_kg": 3.1e21,
            "radius_m": 715000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "gonggong": {
        "synonyms": ["gonggong", "225088 gonggong"],
        "horizons_rec_id": "225088",
        "horizons_id": "225088",
        "object_class": DWARF_PLANET,
        "iau_name": "Gonggong",
        "jpl_designation": "225088 Gonggong",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 1.75e21,
            "radius_m": 615000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "quaoar": {
        "synonyms": ["quaoar", "50000 quaoar"],
        "horizons_rec_id": "50000",
        "horizons_id": "50000",
        "object_class": DWARF_PLANET,
        "iau_name": "Quaoar",
        "jpl_designation": "50000 Quaoar",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 1.4e21,
            "radius_m": 555000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "sedna": {
        "synonyms": ["sedna", "90377 sedna"],
        "horizons_rec_id": "90377",
        "horizons_id": "90377",
        "object_class": DWARF_PLANET,
        "iau_name": "Sedna",
        "jpl_designation": "90377 Sedna",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "texture": "./img/sedna",
            "mass_kg": 1e21,
            "radius_m": 497000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "orcus": {
        "synonyms": ["orcus", "90482 orcus"],
        "horizons_rec_id": "90482",
        "horizons_id": "90482",
        "object_class": DWARF_PLANET,
        "iau_name": "Orcus",
        "jpl_designation": "90482 Orcus",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 6.32e20,
            "radius_m": 458000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "salacia": {
        "synonyms": ["salacia", "120347 salacia"],
        "horizons_rec_id": "120347",
        "horizons_id": "120347",
        "object_class": ASTEROID,
        "iau_name": "Salacia",
        "jpl_designation": "120347 Salacia",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 4.66e20,
            "radius_m": 423000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "varuna": {
        "synonyms": ["varuna", "20000 varuna"],
        "horizons_rec_id": "20000",
        "horizons_id": "20000",
        "object_class": ASTEROID,
        "iau_name": "Varuna",
        "jpl_designation": "20000 Varuna",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 334000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "varda": {
        "synonyms": ["varda", "174567 varda"],
        "horizons_rec_id": "174567",
        "horizons_id": "174567",
        "object_class": ASTEROID,
        "iau_name": "Varda",
        "jpl_designation": "174567 Varda",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 2.66e20,
            "radius_m": 350000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "ixion": {
        "synonyms": ["ixion", "28978 ixion"],
        "horizons_rec_id": "28978",
        "horizons_id": "28978",
        "object_class": ASTEROID,
        "iau_name": "Ixion",
        "jpl_designation": "28978 Ixion",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 325000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "2002 MS4": {
        "synonyms": ["2002 ms4", "307261 2002 ms4"],
        "horizons_rec_id": "307261",
        "horizons_id": "307261",
        "object_class": ASTEROID,
        "iau_name": "2002 MS4",
        "jpl_designation": "2002 MS4",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 400000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "2002 AW197": {
        "synonyms": ["2002 aw197", "55565 2002 aw197"],
        "horizons_rec_id": "55565",
        "horizons_id": "55565",
        "object_class": ASTEROID,
        "iau_name": "2002 AW197",
        "jpl_designation": "2002 AW197",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 348000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },


    # -------------------------
    # Asteroids ≥ 50 km
    # -------------------------

    "ceres": {
        "synonyms": ["ceres", "1 ceres"],
        "horizons_rec_id": "2000001",
        "horizons_id": "1",
        "object_class": DWARF_PLANET,
        "iau_name": "Ceres",
        "jpl_designation": "1 Ceres",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 9.393e20,
            "radius_m": 473000.0,
            "rotation_period_in_solar_d": 0.3781,
            "axial_tilt_deg": 4.0
        }
    },

    "pallas": {
        "synonyms": ["pallas", "2 pallas"],
        "horizons_rec_id": "2000002",
        "horizons_id": "2",
        "object_class": ASTEROID,
        "iau_name": "Pallas",
        "jpl_designation": "2 Pallas",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 2.04e20,
            "radius_m": 256000.0,
            "rotation_period_in_solar_d": 0.3255,
            "axial_tilt_deg": 84.0
        }
    },

    "juno astroid": {
        "synonyms": ["juno astroid", "3 juno"],
        "horizons_rec_id": "2000003",
        "horizons_id": "3",
        "object_class": ASTEROID,
        "iau_name": "Juno",
        "jpl_designation": "3 Juno",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 2.67e19,
            "radius_m": 117000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "vesta": {
        "synonyms": ["vesta", "4 vesta"],
        "horizons_rec_id": "2000004",
        "horizons_id": "4",
        "object_class": ASTEROID,
        "iau_name": "Vesta",
        "jpl_designation": "4 Vesta",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 2.59e20,
            "radius_m": 262000.0,
            "rotation_period_in_solar_d": 0.2226,
            "axial_tilt_deg": 29.0
        }
    },

    "astraea": {
        "synonyms": ["astraea", "5 astraea"],
        "horizons_rec_id": "2000005",
        "horizons_id": "5",
        "object_class": ASTEROID,
        "iau_name": "Astraea",
        "jpl_designation": "5 Astraea",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 58000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "hebe": {
        "synonyms": ["hebe", "6 hebe"],
        "horizons_rec_id": "2000006",
        "horizons_id": "6",
        "object_class": ASTEROID,
        "iau_name": "Hebe",
        "jpl_designation": "6 Hebe",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 92000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "iris": {
        "synonyms": ["iris", "7 iris"],
        "horizons_rec_id": "2000007",
        "horizons_id": "7",
        "object_class": ASTEROID,
        "iau_name": "Iris",
        "jpl_designation": "7 Iris",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 100000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "flora": {
        "synonyms": ["flora", "8 flora"],
        "horizons_rec_id": "2000008",
        "horizons_id": "8",
        "object_class": ASTEROID,
        "iau_name": "Flora",
        "jpl_designation": "8 Flora",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 70000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "metis": {
        "synonyms": ["metis", "9 metis"],
        "horizons_rec_id": "2000009",
        "horizons_id": "9",
        "object_class": ASTEROID,
        "iau_name": "Metis",
        "jpl_designation": "9 Metis",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 90000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "hygiea": {
        "synonyms": ["hygiea", "10 hygiea"],
        "horizons_rec_id": "2000010",
        "horizons_id": "10",
        "object_class": ASTEROID,
        "iau_name": "Hygiea",
        "jpl_designation": "10 Hygiea",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 8.67e19,
            "radius_m": 217000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "parthenope": {
        "synonyms": ["parthenope", "11 parthenope"],
        "horizons_rec_id": "2000011",
        "horizons_id": "11",
        "object_class": ASTEROID,
        "iau_name": "Parthenope",
        "jpl_designation": "11 Parthenope",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 76000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "victoria": {
        "synonyms": ["victoria", "12 victoria"],
        "horizons_rec_id": "2000012",
        "horizons_id": "12",
        "object_class": ASTEROID,
        "iau_name": "Victoria",
        "jpl_designation": "12 Victoria",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 60000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "eunomia": {
        "synonyms": ["eunomia", "15 eunomia"],
        "horizons_rec_id": "2000015",
        "horizons_id": "15",
        "object_class": ASTEROID,
        "iau_name": "Eunomia",
        "jpl_designation": "15 Eunomia",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 3.12e19,
            "radius_m": 135000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "psyche": {
        "synonyms": ["psyche", "16 psyche"],
        "horizons_rec_id": "2000016",
        "horizons_id": "16",
        "object_class": ASTEROID,
        "iau_name": "Psyche",
        "jpl_designation": "16 Psyche",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 2.72e19,
            "radius_m": 113000.0,
            "rotation_period_in_solar_d": 0.1748,
            "axial_tilt_deg": None
        }
    },

    "themis": {
        "synonyms": ["themis", "24 themis"],
        "horizons_rec_id": "2000024",
        "horizons_id": "24",
        "object_class": ASTEROID,
        "iau_name": "Themis",
        "jpl_designation": "24 Themis",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 100000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "doris": {
        "synonyms": ["doris", "48 doris"],
        "horizons_rec_id": "2000048",
        "horizons_id": "48",
        "object_class": ASTEROID,
        "iau_name": "Doris",
        "jpl_designation": "48 Doris",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 110000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "cybele": {
        "synonyms": ["cybele", "65 cybele"],
        "horizons_rec_id": "2000065",
        "horizons_id": "65",
        "object_class": ASTEROID,
        "iau_name": "Cybele",
        "jpl_designation": "65 Cybele",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 118000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "eurynome": {
        "synonyms": ["eurynome", "79 eurynome"],
        "horizons_rec_id": "2000079",
        "horizons_id": "79",
        "object_class": ASTEROID,
        "iau_name": "Eurynome",
        "jpl_designation": "79 Eurynome",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 34000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "euphrosyne": {
        "synonyms": ["euphrosyne", "31 euphrosyne"],
        "horizons_rec_id": "2000031",
        "horizons_id": "31",
        "object_class": ASTEROID,
        "iau_name": "Euphrosyne",
        "jpl_designation": "31 Euphrosyne",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 133000.0,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "interamnia": {
        "synonyms": ["interamnia", "704 interamnia"],
        "horizons_rec_id": "2000704",
        "horizons_id": "704",
        "object_class": ASTEROID,
        "iau_name": "Interamnia",
        "jpl_designation": "704 Interamnia",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 3.9e19,
            "radius_m": 167000.0,
            "rotation_period_in_solar_d": 0.363,
            "axial_tilt_deg": None
        }
    },

    "davida": {
        "synonyms": ["davida", "511 davida"],
        "horizons_rec_id": "2000511",
        "horizons_id": "511",
        "object_class": ASTEROID,
        "iau_name": "Davida",
        "jpl_designation": "511 Davida",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 3.0e19,
            "radius_m": 163000.0,
            "rotation_period_in_solar_d": 0.2138,
            "axial_tilt_deg": None
        }
    },

    "camilla": {
        "synonyms": ["camilla", "107 camilla"],
        "horizons_rec_id": "2000107",
        "horizons_id": "107",
        "object_class": ASTEROID,
        "iau_name": "Camilla",
        "jpl_designation": "107 Camilla",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 1.12e19,
            "radius_m": 125000.0,
            "rotation_period_in_solar_d": 0.2017,
            "axial_tilt_deg": None
        }
    },

    "sylvia": {
        "synonyms": ["sylvia", "87 sylvia"],
        "horizons_rec_id": "2000087",
        "horizons_id": "87",
        "object_class": ASTEROID,
        "iau_name": "Sylvia",
        "jpl_designation": "87 Sylvia",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 1.48e19,
            "radius_m": 143000.0,
            "rotation_period_in_solar_d": 0.2158,
            "axial_tilt_deg": None
        }
    },

    # -------------------------
    # Comets (nucleus radii)
    # -------------------------
    "halley": {
        "synonyms": ["halley", "1p", "1p/halley"],
        "horizons_rec_id": "90000030",
        "horizons_id": "1P",
        "object_class": COMET,
        "iau_name": "Halley",
        "jpl_designation": "1P/Halley",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 5500.0,
            "rotation_period_in_solar_d": 2.2,
            "axial_tilt_deg": None
        }
    },

    "encke": {
        "synonyms": ["encke", "2p", "2p/encke"],
        "horizons_rec_id": "90000021",
        "horizons_id": "2P",
        "object_class": COMET,
        "iau_name": "Encke",
        "jpl_designation": "2P/Encke",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 2400.0,
            "rotation_period_in_solar_d": 0.4625,
            "axial_tilt_deg": None
        }
    },

    "tempel 1": {
        "synonyms": ["tempel 1", "9p", "9p/tempel"],
        "horizons_rec_id": "90000027",
        "horizons_id": "9P",
        "object_class": COMET,
        "iau_name": "Tempel 1",
        "jpl_designation": "9P/Tempel 1",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": 3000.0,
            "rotation_period_in_solar_d": 1.708,
            "axial_tilt_deg": None
        }
    },

    "churyumov-gerasimenko": {
        "synonyms": ["churyumov-gerasimenko", "67p", "67p/churyumov-gerasimenko"],
        "horizons_rec_id": "90000032",
        "horizons_id": "67P",
        "object_class": COMET,
        "iau_name": "Churyumov-Gerasimenko",
        "jpl_designation": "67P/Churyumov-Gerasimenko",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": 1.0e13,
            "radius_m": 2000.0,
            "rotation_period_in_solar_d": 0.5167,
            "axial_tilt_deg": None
        }
    },


    # -------------------------
    # Spacecraft orbiting Earth
    # -------------------------

    "jwst": {
        "synonyms": ["jwst", "james webb"],
        "horizons_rec_id": "-170",
        "horizons_id": "-170",
        "object_class": SPACECRAFT,
        "iau_name": "James Webb Space Telescope",
        "jpl_designation": "James Webb Space Telescope",
        "center": "500@3",
        "orbiting": "earth",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "gaia": {
        "synonyms": ["gaia"],
        "horizons_rec_id": "gaia",
        "horizons_id": "gaia",
        "object_class": SPACECRAFT,
        "iau_name": "Gaia",
        "jpl_designation": "Gaia",
        "center": "500@3",
        "orbiting": "earth",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "iss": {
        "synonyms": ["iss", "international space station"],
        "horizons_rec_id": "-125544",
        "horizons_id": "-125544",
        "object_class": SPACECRAFT,
        "iau_name": "International Space Station",
        "jpl_designation": "International Space Station",
        "center": "500@3",
        "orbiting": "earth",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "hubble": {
        "synonyms": ["hubble", "hst", "hubble space telescope"],
        "horizons_rec_id": "-48",
        "horizons_id": "-48",
        "object_class": SPACECRAFT,
        "iau_name": "Hubble Space Telescope",
        "jpl_designation": "Hubble Space Telescope",
        "center": "500@3",
        "orbiting": "earth",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "chandra": {
        "synonyms": ["chandra", "chandra x-ray observatory"],
        "horizons_rec_id": "-151",
        "horizons_id": "-151",
        "object_class": SPACECRAFT,
        "iau_name": "Chandra X-ray Observatory",
        "jpl_designation": "Chandra X-ray Observatory",
        "center": "500@3",
        "orbiting": "earth",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "tess": {
        "synonyms": ["tess", "transiting exoplanet survey satellite"],
        "horizons_rec_id": "-95",
        "horizons_id": "-95",
        "object_class": SPACECRAFT,
        "iau_name": "Transiting Exoplanet Survey Satellite",
        "jpl_designation": "Transiting Exoplanet Survey Satellite",
        "center": "500@3",
        "orbiting": "earth",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    # -------------------------
    # Spacecraft orbiting Mars
    # -------------------------

    "mro": {
        "synonyms": ["mro", "mars reconnaissance orbiter"],
        "horizons_rec_id": "-74",
        "horizons_id": "-74",
        "object_class": SPACECRAFT,
        "iau_name": "Mars Reconnaissance Orbiter",
        "jpl_designation": "Mars Reconnaissance Orbiter",
        "center": "500@4",
        "orbiting": "mars",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "odyssey": {
        "synonyms": ["odyssey", "2001 mars odyssey"],
        "horizons_rec_id": "-53",
        "horizons_id": "-53",
        "object_class": SPACECRAFT,
        "iau_name": "2001 Mars Odyssey",
        "jpl_designation": "2001 Mars Odyssey",
        "center": "500@4",
        "orbiting": "mars",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "maven": {
        "synonyms": ["maven"],
        "horizons_rec_id": "-202",
        "horizons_id": "-202",
        "object_class": SPACECRAFT,
        "iau_name": "MAVEN",
        "jpl_designation": "MAVEN",
        "center": "500@4",
        "orbiting": "mars",
        "end_date": "2026-03-01",
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "tgo": {
        "synonyms": ["tgo", "trace gas orbiter"],
        "horizons_rec_id": "-143",
        "horizons_id": "-143",
        "object_class": SPACECRAFT,
        "iau_name": "Trace Gas Orbiter",
        "jpl_designation": "Trace Gas Orbiter",
        "center": "500@4",
        "orbiting": "mars",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    # -------------------------
    # Spacecraft orbiting Jupiter
    # -------------------------

    "juno": {
        "synonyms": ["juno", "juno spacecraft"],
        "horizons_rec_id": "-61",
        "horizons_id": "-61",
        "object_class": SPACECRAFT,
        "iau_name": "Juno",
        "jpl_designation": "Juno",
        "center": "500@5",
        "orbiting": "jupiter",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "galileo": {
        "synonyms": ["galileo"],
        "horizons_rec_id": "-77",
        "horizons_id": "-77",
        "object_class": SPACECRAFT,
        "iau_name": "Galileo",
        "jpl_designation": "Galileo",
        "center": "500@5",
        "orbiting": "jupiter",
        "end_date": "2003-09-29",
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    # -------------------------
    # Spacecraft orbiting Saturn
    # -------------------------

    "cassini": {
        "synonyms": ["cassini", "cassini-huygens"],
        "horizons_rec_id": "-82",
        "horizons_id": "-82",
        "object_class": SPACECRAFT,
        "iau_name": "Cassini–Huygens",
        "jpl_designation": "Cassini–Huygens",
        "center": "500@6",
        "orbiting": "saturn",
        "end_date": "2017-09-14",
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    # -------------------------
    # Spacecraft orbiting Mercury
    # -------------------------

    "messenger": {
        "synonyms": ["messenger"],
        "horizons_rec_id": "-236",
        "horizons_id": "-236",
        "object_class": SPACECRAFT,
        "iau_name": "MESSENGER",
        "jpl_designation": "MESSENGER",
        "center": "500@1",
        "orbiting": "mercury",
        "end_date": "2015-04-29",
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "bepicolombo": {
        "synonyms": ["bepicolombo"],
        "horizons_rec_id": "-121",
        "horizons_id": "-121",
        "object_class": SPACECRAFT,
        "iau_name": "BepiColombo",
        "jpl_designation": "BepiColombo",
        "center": "500@1",
        "orbiting": "mercury",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },


    # -------------------------
    # Spacecraft orbiting the Sun
    # -------------------------

    "voyager 1": {
        "synonyms": ["voyager 1", "vgr1", "voyager-1"],
        "horizons_rec_id": "-31",
        "horizons_id": "-31",
        "object_class": SPACECRAFT,
        "iau_name": "Voyager 1",
        "jpl_designation": "Voyager 1",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "voyager 2": {
        "synonyms": ["voyager 2", "vgr2", "voyager-2"],
        "horizons_rec_id": "-32",
        "horizons_id": "-32",
        "object_class": SPACECRAFT,
        "iau_name": "Voyager 2",
        "jpl_designation": "Voyager 2",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "pioneer 10": {
        "synonyms": ["pioneer 10", "pioneer-10"],
        "horizons_rec_id": "-23",
        "horizons_id": "-23",
        "object_class": SPACECRAFT,
        "iau_name": "Pioneer 10",
        "jpl_designation": "Pioneer 10",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "pioneer 11": {
        "synonyms": ["pioneer 11", "pioneer-11"],
        "horizons_rec_id": "-24",
        "horizons_id": "-24",
        "object_class": SPACECRAFT,
        "iau_name": "Pioneer 11",
        "jpl_designation": "Pioneer 11",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "tesla roadster": {
        "synonyms": ["tesla roadster", "spacex roadster", "elon musk car"],
        "horizons_rec_id": "-143205",
        "horizons_id": "-143205",
        "object_class": SPACECRAFT,
        "iau_name": "Tesla Roadster",
        "jpl_designation": "Tesla Roadster",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "rosetta": {
        "synonyms": ["rosetta"],
        "horizons_rec_id": "-226",
        "horizons_id": "-226",
        "object_class": SPACECRAFT,
        "iau_name": "Rosetta",
        "jpl_designation": "Rosetta",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": "2016-10-04",
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "kepler": {
        "synonyms": ["kepler", "kepler space telescope"],
        "horizons_rec_id": "-227",
        "horizons_id": "-227",
        "object_class": SPACECRAFT,
        "iau_name": "Kepler Space Telescope",
        "jpl_designation": "Kepler Space Telescope",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "dawn": {
        "synonyms": ["dawn"],
        "horizons_rec_id": "-203",
        "horizons_id": "-203",
        "object_class": SPACECRAFT,
        "iau_name": "Dawn",
        "jpl_designation": "Dawn",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "osiris-rex": {
        "synonyms": ["osiris-rex", "osiris rex"],
        "horizons_rec_id": "-64",
        "horizons_id": "-64",
        "object_class": SPACECRAFT,
        "iau_name": "OSIRIS-REx",
        "jpl_designation": "OSIRIS-REx",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "hayabusa": {
        "synonyms": ["hayabusa"],
        "horizons_rec_id": "-130",
        "horizons_id": "-130",
        "object_class": SPACECRAFT,
        "iau_name": "Hayabusa",
        "jpl_designation": "Hayabusa",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": "2010-06-12",
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "hayabusa2": {
        "synonyms": ["hayabusa2", "hayabusa 2"],
        "horizons_rec_id": "-37",
        "horizons_id": "-37",
        "object_class": SPACECRAFT,
        "iau_name": "Hayabusa2",
        "jpl_designation": "Hayabusa2",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    },

    "new horizons": {
        "synonyms": ["new horizons", "nh"],
        "horizons_rec_id": "-98",
        "horizons_id": "-98",
        "object_class": SPACECRAFT,
        "iau_name": "New Horizons",
        "jpl_designation": "New Horizons",
        "center": "500@0",
        "orbiting": "sun",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    }

}
