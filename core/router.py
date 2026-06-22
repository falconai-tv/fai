import os

API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY", "VENDOS_KEY_TEND_KETU")

OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY", "f8a26ced25d514b94ad2d1e61bca80e1")

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "53c1d74812msh8abfdd1e3b43de7p1002b4jsn9c3a24d3ec58")

PORT  = int(os.getenv("PORT", 8080))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
HOST  = "0.0.0.0"

API_FOOTBALL_URL = "https://v3.football.api-sports.io"

SPORTS_API_TIMEOUT = 6

SUPPORTED_LEAGUES = {
    "premier_league":   39,
    "la_liga":          140,
    "serie_a":          135,
    "bundesliga":       78,
    "ligue_1":          61,
    "champions_league": 2,
    "europa_league":    3,
    "world_cup":        1,
}

DEFAULT_FORMATION = "4-3-3"

FORMATIONS = {
    "4-3-3": {
        "home": [
            {"role": "GK",  "x": 0.05, "y": 0.50},
            {"role": "RB",  "x": 0.20, "y": 0.15},
            {"role": "CB",  "x": 0.20, "y": 0.35},
            {"role": "CB",  "x": 0.20, "y": 0.65},
            {"role": "LB",  "x": 0.20, "y": 0.85},
            {"role": "CM",  "x": 0.45, "y": 0.25},
            {"role": "CDM", "x": 0.40, "y": 0.50},
            {"role": "CM",  "x": 0.45, "y": 0.75},
            {"role": "RW",  "x": 0.70, "y": 0.15},
            {"role": "ST",  "x": 0.78, "y": 0.50},
            {"role": "LW",  "x": 0.70, "y": 0.85},
        ],
        "away": [
            {"role": "GK",  "x": 0.95, "y": 0.50},
            {"role": "RB",  "x": 0.80, "y": 0.85},
            {"role": "CB",  "x": 0.80, "y": 0.65},
            {"role": "CB",  "x": 0.80, "y": 0.35},
            {"role": "LB",  "x": 0.80, "y": 0.15},
            {"role": "CM",  "x": 0.55, "y": 0.75},
            {"role": "CDM", "x": 0.60, "y": 0.50},
            {"role": "CM",  "x": 0.55, "y": 0.25},
            {"role": "RW",  "x": 0.30, "y": 0.85},
            {"role": "ST",  "x": 0.22, "y": 0.50},
            {"role": "LW",  "x": 0.30, "y": 0.15},
        ]
    },
    "4-4-2": {
        "home": [
            {"role": "GK",  "x": 0.05, "y": 0.50},
            {"role": "RB",  "x": 0.20, "y": 0.15},
            {"role": "CB",  "x": 0.20, "y": 0.35},
            {"role": "CB",  "x": 0.20, "y": 0.65},
            {"role": "LB",  "x": 0.20, "y": 0.85},
            {"role": "RM",  "x": 0.50, "y": 0.15},
            {"role": "CM",  "x": 0.45, "y": 0.38},
            {"role": "CM",  "x": 0.45, "y": 0.62},
            {"role": "LM",  "x": 0.50, "y": 0.85},
            {"role": "ST",  "x": 0.75, "y": 0.38},
            {"role": "ST",  "x": 0.75, "y": 0.62},
        ],
        "away": [
            {"role": "GK",  "x": 0.95, "y": 0.50},
            {"role": "RB",  "x": 0.80, "y": 0.85},
            {"role": "CB",  "x": 0.80, "y": 0.65},
            {"role": "CB",  "x": 0.80, "y": 0.35},
            {"role": "LB",  "x": 0.80, "y": 0.15},
            {"role": "RM",  "x": 0.50, "y": 0.85},
            {"role": "CM",  "x": 0.55, "y": 0.62},
            {"role": "CM",  "x": 0.55, "y": 0.38},
            {"role": "LM",  "x": 0.50, "y": 0.15},
            {"role": "ST",  "x": 0.25, "y": 0.62},
            {"role": "ST",  "x": 0.25, "y": 0.38},
        ]
    },
    "3-5-2": {
        "home": [
            {"role": "GK",  "x": 0.05, "y": 0.50},
            {"role": "CB",  "x": 0.20, "y": 0.25},
            {"role": "CB",  "x": 0.20, "y": 0.50},
            {"role": "CB",  "x": 0.20, "y": 0.75},
            {"role": "RWB", "x": 0.45, "y": 0.10},
            {"role": "CM",  "x": 0.45, "y": 0.32},
            {"role": "CDM", "x": 0.40, "y": 0.50},
            {"role": "CM",  "x": 0.45, "y": 0.68},
            {"role": "LWB", "x": 0.45, "y": 0.90},
            {"role": "ST",  "x": 0.75, "y": 0.38},
            {"role": "ST",  "x": 0.75, "y": 0.62},
        ],
        "away": [
            {"role": "GK",  "x": 0.95, "y": 0.50},
            {"role": "CB",  "x": 0.80, "y": 0.75},
            {"role": "CB",  "x": 0.80, "y": 0.50},
            {"role": "CB",  "x": 0.80, "y": 0.25},
            {"role": "RWB", "x": 0.55, "y": 0.90},
            {"role": "CM",  "x": 0.55, "y": 0.68},
            {"role": "CDM", "x": 0.60, "y": 0.50},
            {"role": "CM",  "x": 0.55, "y": 0.32},
            {"role": "LWB", "x": 0.55, "y": 0.10},
            {"role": "ST",  "x": 0.25, "y": 0.62},
            {"role": "ST",  "x": 0.25, "y": 0.38},
        ]
    }
}

WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
WEATHER_TIMEOUT  = 5
WEATHER_UNITS    = "metric"
WEATHER_LANG     = "en"
WEATHER_FALLBACK_CITY = "New York"

MUSIC_MAX_HISTORY = 50
MUSIC_SEARCH_OFFSET_MAX = 8

WEB_TIMEOUT         = 5
ARTICLE_MAX_LENGTH  = 1500
NEWS_ARTICLES_COUNT = 3

ML_CONFIDENCE_THRESHOLD = 0.7
DEFAULT_USER_ID         = "default_user"

BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
DATA_DIR        = os.path.join(BASE_DIR, "data")
VOICE_CACHE_DIR = os.path.join(DATA_DIR, "voice_cache")
LOGS_FILE       = os.path.join(DATA_DIR, "logs.jsonl")
USER_MEMORY     = os.path.join(DATA_DIR, "user_memory.json")
CHANNELS_FILE   = os.path.join(DATA_DIR, "channels.json")

VOICE_CACHE_ENABLED = True
VOICE_LANG          = "en"
