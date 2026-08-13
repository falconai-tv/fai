import os
import sys
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.logger_config import setup_logger
from core.agent import Agent
from core.executor import Executor
from core.brain import FalconBrain
from core.router import Router
from engines.web_engine import WebEngine
from engines.music_engine import MusicEngine
from engines.weather_engine import WeatherEngine
from engines.sports_engine import SportsEngine

try:
    from core.channel_player import ChannelPlayer
except ImportError:
    ChannelPlayer = None

try:
    from core.channel_ai import ChannelAI
except ImportError:
    ChannelAI = None

logger = setup_logger("FalconAI.Main")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

logger.info("--- FalconAI Booting ---")

web_engine = None
music_engine = None
weather_engine = None
sports_engine = None
router = None
brain = None
agent = None
executor = None

try:
    web_engine = WebEngine()
    music_engine = MusicEngine()
    weather_engine = WeatherEngine()
    sports_engine = SportsEngine()

    router = Router(
        music_engine=music_engine,
        web_engine=web_engine,
        weather_engine=weather_engine,
        sports_engine=sports_engine
    )

    brain = FalconBrain()

    agent = Agent(
        music_engine=music_engine,
        web_engine=web_engine,
        weather_engine=weather_engine,
        sports_engine=sports_engine
    )
    
    channel_ai = ChannelAI() if ChannelAI else None
    channel_player = ChannelPlayer(channels=sports_engine, channel_ai=channel_ai, web_engine=web_engine) if ChannelPlayer else None
    
    executor = Executor(
        channel_player=channel_player,
        channel_ai=channel_ai
    )

    logger.info("--- All Systems Ready (Agent, Executor, and ML Model Loaded) ---")
except Exception as e:
    logger.error(f"FATAL ERROR DURING BOOT: {str(e)}")

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "system": "FalconAI V3",
        "version": "3.0.0"
    }), 200

@app.route('/debug/live', methods=['GET'])
def debug_live():
    try:
        matches = sports_engine.fetch_live_matches()
        return jsonify({
            "total": len(matches),
            "matches": [
                {
                    "home": m.get("teams", {}).get("home", {}).get("name"),
                    "away": m.get("teams", {}).get("away", {}).get("name"),
                    "league": m.get("league", {}).get("name"),
                    "country": m.get("league", {}).get("country"),
                    "minute": m.get("fixture", {}).get("status", {}).get("elapsed"),
                    "score_h": m.get("goals", {}).get("home"),
                    "score_a": m.get("goals", {}).get("away"),
                }
                for m in matches
            ]
        }), 200
    except Exception as e:
        logger.error(f"Debug live error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/process', methods=['POST', 'OPTIONS'])
def process_request():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        if agent is None or executor is None or router is None:
            return jsonify({
                "status": "error",
                "message": "FalconAI core components are not initialized properly. Check boot logs."
            }), 500

        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({"status": "error", "message": "No text provided"}), 400

        user_text = data['text']
        user_id = data.get('user_id', "default_user")
        clean_input = user_text.lower().strip()

        logger.info(f"User Input [{user_id}]: {user_text}")

        if "weather" in clean_input or "moti" in clean_input:
            city_query = clean_input
            for prefix in ["weather in", "weather", "moti ne", "moti në", "moti", "forecast for", "forecast"]:
                city_query = city_query.replace(prefix, "")
            
            city = city_query.strip()
            if not city:
                city = "San Francisco"
            
            if weather_engine:
                try:
                    weather_res = weather_engine.get_weather(city) if hasattr(weather_engine, 'get_weather') else weather_engine.process(city)
                    return jsonify(weather_res), 200
                except Exception as w_err:
                    logger.error(f"[Weather Direct Fallback Error]: {w_err}")

        response_data = agent.handle_request(user_text)
        route_name = response_data.get("type", "unknown")
        execution_result = executor.execute_action(route_name, response_data)

        final_response = execution_result.get('response', response_data)

        if isinstance(final_response, dict) and 'status' not in final_response:
            final_response['status'] = 'success'

        return jsonify(final_response), 200

    except Exception as e:
        logger.error(f"Processing Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal processing error",
            "details": str(e)
        }), 500

def run_cli():
    print("\n" + "="*50)
    print(" FALCONAI V3 - TERMINAL TEST MODE")
    print(" Shkruaj komandën tënde ose shkruaj 'exit' për të dalë.")
    print("="*50 + "\n")

    while True:
        try:
            user_input = input("FalconAI > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "dalje"):
                print("Duke u mbyllur... Mirupafshim!")
                os._exit(0)

            clean_input = user_input.lower()

            if "weather" in clean_input or "moti" in clean_input:
                city_query = clean_input
                for prefix in ["weather in", "weather", "moti ne", "moti në", "moti", "forecast for", "forecast"]:
                    city_query = city_query.replace(prefix, "")
                city = city_query.strip()
                if not city:
                    city = "Prishtina"
                
                if weather_engine:
                    try:
                        weather_res = weather_engine.get_weather(city) if hasattr(weather_engine, 'get_weather') else weather_engine.process(city)
                        print(f"[Përgjigjja]:\n{weather_res.get('data', {}).get('text', weather_res)}\n")
                        continue
                    except Exception as w_err:
                        print(f"[Gabim moti]: {w_err}")

            if agent and executor:
                response_data = agent.handle_request(user_input)
                route_name = response_data.get("type", "unknown")
                execution_result = executor.execute_action(route_name, response_data)
                
                final_msg = execution_result.get('response', {}).get('message', response_data)
                print(f"[Përgjigjja]: {final_msg}\n")
            else:
                print("[Gabim]: Sistemet nuk janë ngarkuar plotësisht.")
        except KeyboardInterrupt:
            print("\nU ndërpre nga përdoruesi.")
            break
        except Exception as e:
            print(f"[Gabim gjatë procesimit]: {e}\n")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))

    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()

    run_cli()
