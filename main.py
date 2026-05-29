from flask import Flask, request, jsonify
import logging

from core.channel_registry import ChannelRegistry
from engines.web_engine import WebEngine
from engines.weather_engine import WeatherEngine
from engines.music_engine import MusicEngine

# -------------------------
# INIT APP
# -------------------------
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FalconAI")

# -------------------------
# INIT MODULES
# -------------------------
channel_registry = ChannelRegistry()
web_engine = WebEngine()
weather_engine = WeatherEngine()
music_engine = MusicEngine()


# -------------------------
# CHANNEL HANDLER
# -------------------------
def handle_channel(text: str):
    """
    Channels are STRICT MATCH ONLY by name.
    """
    return channel_registry.get_channel(text)


# -------------------------
# ROUTER LOGIC
# -------------------------
def route(text: str):
    if not text:
        return {
            "type": "error",
            "data": {"text": "Empty input"}
        }

    t = text.lower().strip()

    # ---------------- CHANNELS (highest priority)
    channel = handle_channel(text)
    if channel:
        return {
            "type": "channel",
            "data": channel
        }

    # ---------------- WEATHER
    if "weather" in t:
        return weather_engine.process(text)

    # ---------------- MUSIC
    if any(k in t for k in ["music", "song", "spotify", "audio", "play song"]):
        return music_engine.process(text)

    # ---------------- MOVIE / VIDEO / STREAM
    if any(k in t for k in [
        "movie", "film", "watch", "netflix",
        "tubi", "action", "series", "episode"
    ]):
        return web_engine.process(text, intent="watch_movie")

    # ---------------- NEWS / SEARCH DEFAULT
    return web_engine.process(text, intent="general_search")


# -------------------------
# MAIN API ENDPOINT
# -------------------------
@app.route("/process", methods=["POST"])
def process():
    try:
        data = request.get_json(force=True)
        text = data.get("text", "").strip()

        logger.info(f"[INPUT] {text}")

        result = route(text)
        return jsonify(result)

    except Exception as e:
        logger.error(f"[ERROR] {str(e)}")

        return jsonify({
            "type": "error",
            "data": {
                "text": "Internal server error"
            }
        })


# -------------------------
# HEALTH CHECK
# -------------------------
@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "FalconAI Backend",
        "version": "1.0.0"
    })


# -------------------------
# START SERVER
# -------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )
