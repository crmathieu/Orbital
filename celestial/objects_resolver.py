# -*- coding: utf-8 -*-
# objects_resolver.py

from constants import *

OBJECTS = {

    # -------------------------
    # Planets Objects
    # -------------------------

    "sun-barycenter": {
        "synonyms": ["ssb", "solar system barycenter"],
        "spk_id": "0",
        "horizons_id": "0",
        "object_class": BARYCENTER,
        "iau_name": "SSB",
        "jpl_designation": "Solar System Barycenter",
        "center": SUN_BARYCENTER, # Center on itself/Absolute origin
        "orbiting": None,
        "end_date": None,    
    },
        
    "sun": {
        "synonyms": ["sun"],
        "spk_id": "10",
        "horizons_id": "10",
        "object_class": STAR,
        "iau_name": "Sun",
        "jpl_designation": "Sun",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "199",
        "horizons_id": "199",
        "object_class": INNER_PLANET,
        "iau_name": "Mercury",
        "jpl_designation": "Mercury",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "299",
        "horizons_id": "299",
        "object_class": INNER_PLANET,
        "iau_name": "Venus",
        "jpl_designation": "Venus",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "399",
        "horizons_id": "399",
        "object_class": INNER_PLANET,
        "iau_name": "Earth",
        "jpl_designation": "Earth",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "499",
        "horizons_id": "499",
        "object_class": INNER_PLANET,
        "iau_name": "Mars",
        "jpl_designation": "Mars",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "599",
        "horizons_id": "599",
        "object_class": OUTER_PLANET,
        "iau_name": "Jupiter",
        "jpl_designation": "Jupiter",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "699",
        "horizons_id": "699",
        "object_class": OUTER_PLANET,
        "iau_name": "Saturn",
        "jpl_designation": "Saturn",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "799",
        "horizons_id": "799",
        "object_class": OUTER_PLANET,
        "iau_name": "Uranus",
        "jpl_designation": "Uranus",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "899",
        "horizons_id": "899",
        "object_class": OUTER_PLANET,
        "iau_name": "Neptune",
        "jpl_designation": "Neptune",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
        "end_date": None,
        "physical": {
            "texture": "./img/source/2k_neptune-PM-normalized",
            "mass_kg": 1.02413e26,
            "radius_m": 24622000.0,
            "rotation_period_in_solar_d": 0.67125,
            "axial_tilt_deg": 28.32
        }
    },

    "pluto-barycenter2": {
        "synonyms": ["pluto-barycenter2"],
        "spk_id": "9",
        "horizons_id": "9",
        "object_class": BARYCENTER,
        "object_role": DWARF_PLANET,
        "iau_name": "Pluto-Barycenter2",
        "jpl_designation": "Pluto Barycenter2",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
        "end_date": None,
        "physical": {
            "texture": "",
            "mass_kg": 1.303e22,
            "radius_m": 1188300.0,
            "rotation_period_in_solar_d": -6.3872,
            "axial_tilt_deg": 119.61
        }
    },

    "pluto-barycenter": {
        "synonyms": ["pluto-barycenter"],
        "spk_id": "9",
        "horizons_id": "9",
        "object_class": BARYCENTER,
        "iau_name": "Pluto-Barycenter",
        "jpl_designation": "Pluto Barycenter",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
        "end_date": None,
        "physical": {
            "texture": "",
            "mass_kg": 0.0,
            "radius_m": 0.0,
            "rotation_period_in_solar_d": 0.0,
            "axial_tilt_deg": 0.0
        }
    },

    "pluto": {
        "synonyms": ["pluto", "134340 pluto"],
        "spk_id": "999",
        "horizons_id": "999",
        "object_class": DWARF_PLANET,
        "object_role": BARYCENTER_MEMBER,
        "iau_name": "Pluto",
        "jpl_designation": "134340 Pluto",
        "center": PLUTO_BARYCENTER,
        "orbiting": "pluto-barycenter",
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
        "spk_id": "2136199",
        "horizons_id": "2136199",
        "object_class": TNO,
        "iau_name": "Eris",
        "jpl_designation": "136199 Eris",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2136108",
        "horizons_id": "2136108",
        "object_class": TNO,
        "iau_name": "Haumea",
        "jpl_designation": "136108 Haumea",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2136472",
        "horizons_id": "2136472",
        "object_class": TNO,
        "iau_name": "Makemake",
        "jpl_designation": "136472 Makemake",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2225088",
        "horizons_id": "2225088",
        "object_class": TNO,
        "iau_name": "Gonggong",
        "jpl_designation": "225088 Gonggong",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "20050000",
        "horizons_id": "20050000",
        "object_class": TNO,
        "iau_name": "Quaoar",
        "jpl_designation": "50000 Quaoar",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "20090377",
        "horizons_id": "20090377",
        "object_class": TNO,
        "iau_name": "Sedna",
        "jpl_designation": "90377 Sedna",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "20090482",
        "horizons_id": "20090482",
        "object_class": TNO,
        "iau_name": "Orcus",
        "jpl_designation": "90482 Orcus",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2120347",
        "horizons_id": "2120347",
        "object_class": ASTEROID,
        "iau_name": "Salacia",
        "jpl_designation": "120347 Salacia",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "20020000",
        "horizons_id": "20020000",
        "object_class": ASTEROID,
        "iau_name": "Varuna",
        "jpl_designation": "20000 Varuna",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2174567",
        "horizons_id": "2174567",
        "object_class": ASTEROID,
        "iau_name": "Varda",
        "jpl_designation": "174567 Varda",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "20028978",
        "horizons_id": "20028978",
        "object_class": TNO,
        "iau_name": "Ixion",
        "jpl_designation": "28978 Ixion",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2307261",
        "horizons_id": "2307261",
        "object_class": ASTEROID,
        "iau_name": "2002 MS4",
        "jpl_designation": "2002 MS4",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "20055565",
        "horizons_id": "20055565",
        "object_class": ASTEROID,
        "iau_name": "2002 AW197",
        "jpl_designation": "2002 AW197",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000001",
        "horizons_id": "1;",
        "object_class": DWARF_PLANET,
        "iau_name": "Ceres",
        "jpl_designation": "1 Ceres",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
        "end_date": None,
        "physical": {
            "texture": "./img/ceres",
            "mass_kg": 9.393e20,
            "radius_m": 473000.0,
            "rotation_period_in_solar_d": 0.3781,
            "axial_tilt_deg": 4.0
        }
    },

    "pallas": {
        "synonyms": ["pallas", "2 pallas"],
        "spk_id": "2000002",
        "horizons_id": "2;",
        "object_class": DWARF_PLANET,
        "iau_name": "Pallas",
        "jpl_designation": "2 Pallas",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
        "end_date": None,
        "physical": {
            "texture": "./img/pallas",
            "mass_kg": 2.04e20,
            "radius_m": 256000.0,
            "rotation_period_in_solar_d": 0.3255,
            "axial_tilt_deg": 84.0
        }
    },

    "juno astroid": {
        "synonyms": ["juno astroid", "3 juno"],
        "spk_id": "2000003",
        "horizons_id": "3;",
        "object_class": BIG_ASTEROID,
        "iau_name": "Juno",
        "jpl_designation": "3 Juno",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000004",
        "horizons_id": "4;",
        "object_class": DWARF_PLANET,
        "iau_name": "Vesta",
        "jpl_designation": "4 Vesta",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000005",
        "horizons_id": "5",
        "object_class": ASTEROID,
        "iau_name": "Astraea",
        "jpl_designation": "5 Astraea",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000006",
        "horizons_id": "6",
        "object_class": ASTEROID,
        "iau_name": "Hebe",
        "jpl_designation": "6 Hebe",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000007",
        "horizons_id": "7",
        "object_class": ASTEROID,
        "iau_name": "Iris",
        "jpl_designation": "7 Iris",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000008",
        "horizons_id": "8",
        "object_class": ASTEROID,
        "iau_name": "Flora",
        "jpl_designation": "8 Flora",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000009",
        "horizons_id": "9",
        "object_class": ASTEROID,
        "iau_name": "Metis",
        "jpl_designation": "9 Metis",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000010",
        "horizons_id": "10",
        "object_class": ASTEROID,
        "iau_name": "Hygiea",
        "jpl_designation": "10 Hygiea",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000011",
        "horizons_id": "11",
        "object_class": ASTEROID,
        "iau_name": "Parthenope",
        "jpl_designation": "11 Parthenope",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000012",
        "horizons_id": "12",
        "object_class": ASTEROID,
        "iau_name": "Victoria",
        "jpl_designation": "12 Victoria",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000015",
        "horizons_id": "15",
        "object_class": ASTEROID,
        "iau_name": "Eunomia",
        "jpl_designation": "15 Eunomia",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000016",
        "horizons_id": "16",
        "object_class": ASTEROID,
        "iau_name": "Psyche",
        "jpl_designation": "16 Psyche",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000024",
        "horizons_id": "24",
        "object_class": ASTEROID,
        "iau_name": "Themis",
        "jpl_designation": "24 Themis",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000048",
        "horizons_id": "48",
        "object_class": ASTEROID,
        "iau_name": "Doris",
        "jpl_designation": "48 Doris",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000065",
        "horizons_id": "65",
        "object_class": ASTEROID,
        "iau_name": "Cybele",
        "jpl_designation": "65 Cybele",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000079",
        "horizons_id": "79",
        "object_class": ASTEROID,
        "iau_name": "Eurynome",
        "jpl_designation": "79 Eurynome",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000031",
        "horizons_id": "31",
        "object_class": ASTEROID,
        "iau_name": "Euphrosyne",
        "jpl_designation": "31 Euphrosyne",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000704",
        "horizons_id": "704",
        "object_class": ASTEROID,
        "iau_name": "Interamnia",
        "jpl_designation": "704 Interamnia",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000511",
        "horizons_id": "511",
        "object_class": ASTEROID,
        "iau_name": "Davida",
        "jpl_designation": "511 Davida",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000107",
        "horizons_id": "107",
        "object_class": ASTEROID,
        "iau_name": "Camilla",
        "jpl_designation": "107 Camilla",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "2000087",
        "horizons_id": "87",
        "object_class": ASTEROID,
        "iau_name": "Sylvia",
        "jpl_designation": "87 Sylvia",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "1000036",
        "horizons_id": "1P",
        "object_class": COMET,
        "iau_name": "Halley",
        "jpl_designation": "1P/Halley",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "90000002",
        "horizons_id": "2P",
        "object_class": COMET,
        "iau_name": "Encke",
        "jpl_designation": "2P/Encke",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "90000192",
        "horizons_id": "9P",
        "object_class": COMET,
        "iau_name": "Tempel 1",
        "jpl_designation": "9P/Tempel 1",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "1000012",
        "horizons_id": "67P",
        "object_class": COMET,
        "iau_name": "Churyumov-Gerasimenko",
        "jpl_designation": "67P/Churyumov-Gerasimenko",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "-170",
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
        "spk_id": "gaia",
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
        "spk_id": "-125544",
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
        "spk_id": "-48",
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
        "spk_id": "-151",
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
        "spk_id": "-95",
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
        "spk_id": "-74",
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
        "spk_id": "-53",
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
        "spk_id": "-202",
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
        "spk_id": "-143",
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
        "spk_id": "-61",
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
        "spk_id": "-77",
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
        "spk_id": "-82",
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
        "spk_id": "-236",
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
        "spk_id": "-121",
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
        "spk_id": "-31",
        "horizons_id": "-31",
        "object_class": SPACECRAFT,
        "iau_name": "Voyager 1",
        "jpl_designation": "Voyager 1",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "-32",
        "horizons_id": "-32",
        "object_class": SPACECRAFT,
        "iau_name": "Voyager 2",
        "jpl_designation": "Voyager 2",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "-23",
        "horizons_id": "-23",
        "object_class": SPACECRAFT,
        "iau_name": "Pioneer 10",
        "jpl_designation": "Pioneer 10",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "-24",
        "horizons_id": "-24",
        "object_class": SPACECRAFT,
        "iau_name": "Pioneer 11",
        "jpl_designation": "Pioneer 11",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "-143205",
        "horizons_id": "-143205",
        "object_class": SPACECRAFT,
        "iau_name": "Tesla Roadster",
        "jpl_designation": "Tesla Roadster",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None,
            "profile":  {
                "look": "starman",
                "engine": 1,
                "length": 1.0,
                "COPV": 1
            }
        }
    },

    "rosetta": {
        "synonyms": ["rosetta"],
        "spk_id": "-226",
        "horizons_id": "-226",
        "object_class": SPACECRAFT,
        "iau_name": "Rosetta",
        "jpl_designation": "Rosetta",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "-227",
        "horizons_id": "-227",
        "object_class": SPACECRAFT,
        "iau_name": "Kepler Space Telescope",
        "jpl_designation": "Kepler Space Telescope",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "-203",
        "horizons_id": "-203",
        "object_class": SPACECRAFT,
        "iau_name": "Dawn",
        "jpl_designation": "Dawn",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "-64",
        "horizons_id": "-64",
        "object_class": SPACECRAFT,
        "iau_name": "OSIRIS-REx",
        "jpl_designation": "OSIRIS-REx",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "-130",
        "horizons_id": "-130",
        "object_class": SPACECRAFT,
        "iau_name": "Hayabusa",
        "jpl_designation": "Hayabusa",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "-37",
        "horizons_id": "-37",
        "object_class": SPACECRAFT,
        "iau_name": "Hayabusa2",
        "jpl_designation": "Hayabusa2",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
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
        "spk_id": "-98",
        "horizons_id": "-98",
        "object_class": SPACECRAFT,
        "iau_name": "New Horizons",
        "jpl_designation": "New Horizons",
        "center": SUN_BARYCENTER,
        "orbiting": "sun-barycenter",
        "end_date": None,
        "physical": {
            "mass_kg": None,
            "radius_m": None,
            "rotation_period_in_solar_d": None,
            "axial_tilt_deg": None
        }
    }

}

