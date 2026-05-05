import requests
import logging
from utils.voice import speak

logger = logging.getLogger("FalconAI.WeatherEngine")

API_KEY = "f8a26ced25d514b94ad2d1e61bca80e1"

WEATHER_ICONS = {
    "clear sky":          "☀️",
    "few clouds":         "🌤️",
    "scattered clouds":   "⛅",
    "broken clouds":      "☁️",
    "overcast clouds":    "☁️",
    "light rain":         "🌦️",
    "moderate rain":      "🌧️",
    "heavy rain":         "🌧️",
    "heavy intensity rain": "🌧️",
    "thunderstorm":       "⛈️",
    "snow":               "❄️",
    "light snow":         "🌨️",
    "light intensity drizzle": "🌦️",
    "drizzle":            "🌦️",
    "mist":               "🌫️",
    "fog":                "🌫️",
    "haze":               "🌫️",
}

class WeatherEngine:
    def __init__(self, api_key=API_KEY):
        self.api_key  = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_city_from_ip(self):
        try:
            response = requests.get("https://ipapi.co/json/", timeout=5)
            data = response.json()
            city = data.get("city", "Pristina")
            logger.info(f"[WEATHER] IP detected city: {city}")
            return city
        except Exception:
            logger.warning("[WEATHER] IP lookup failed, using Pristina")
            return "Pristina"

    def detect_city(self, query):
        stopwords = {
            "weather", "in", "what", "is", "the", "today", "tomorrow",
            "forecast", "how", "cold", "hot", "like", "outside", "now",
            "current", "right", "now", "tell", "me", "about", "give",
            "show", "update", "temperature", "will", "be", "it"
        }

        words = query.lower().split()
        city_words = [w for w in words if w not in stopwords and len(w) > 1]

        if city_words:
            return " ".join(city_words).title()

        return self.get_city_from_ip()

    def fetch_weather(self, city):
        response = requests.get(self.base_url, params={
            "q":      city,
            "appid":  self.api_key,
            "units":  "metric",
            "lang":   "en"
        }, timeout=5)

        if response.status_code == 200:
            return response.json()
        
        logger.warning(f"[WEATHER] City '{city}' not found, falling back to IP")
        fallback_city = self.get_city_from_ip()
        
        response2 = requests.get(self.base_url, params={
            "q":      fallback_city,
            "appid":  self.api_key,
            "units":  "metric",
            "lang":   "en"
        }, timeout=5)

        if response2.status_code == 200:
            return response2.json()

        return None

    def build_response(self, data):
        city     = data["name"]
        country  = data["sys"]["country"]
        temp     = round(data["main"]["temp"])
        feels    = round(data["main"]["feels_like"])
        humidity = data["main"]["humidity"]
        wind     = round(data["wind"]["speed"] * 3.6, 1)
        desc     = data["weather"][0]["description"]
        icon     = WEATHER_ICONS.get(desc, "🌡️")

        display = (
            f"\n{'='*38}\n"
            f"  {icon}  WEATHER IN {city.upper()}, {country}\n"
            f"{'='*38}\n"
            f"  🌡️  Temperature : {temp}°C\n"
            f"  🤔  Feels like  : {feels}°C\n"
            f"  💧  Humidity    : {humidity}%\n"
            f"  💨  Wind        : {wind} km/h\n"
            f"  📋  Condition   : {desc.capitalize()}\n"
            f"{'='*38}\n"
        )

        voice_text = (
            f"The weather in {city}, {country} is {desc}. "
            f"Temperature is {temp} degrees Celsius, "
            f"feels like {feels} degrees. "
            f"Humidity is {humidity} percent "
            f"and wind speed is {wind} kilometers per hour."
        )

        return {
            "type": "weather",
            "data": {
                "city":        city,
                "country":     country,
                "temp":        temp,
                "feels_like":  feels,
                "humidity":    humidity,
                "wind":        wind,
                "description": desc,
                "icon":        icon,
                "text":        display,
                "voice_text":  voice_text
            }
        }

    def process(self, query):
        try:
            generic = ["weather today", "what is the weather", "how is the weather",
                      "weather outside", "weather now", "current weather",
                      "weather forecast", "tell me the weather"]

            if any(g in query.lower() for g in generic):
                city = self.get_city_from_ip()
            else:
                city = self.detect_city(query)

            logger.info(f"[WEATHER] Fetching for: {city}")

            raw = self.fetch_weather(city)

            if not raw:
                return self.error_response(query)

            result = self.build_response(raw)

            speak(result["data"]["voice_text"])

            return result

        except Exception as e:
            logger.error(f"[WEATHER ERROR] {e}")
            return self.error_response(query)

    def error_response(self, query):
        return {
            "type": "weather",
            "data": {
                "text": f"Sorry, I couldn't get the weather. Please try again."
            }
        }