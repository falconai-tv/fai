import os
import sys
import threading
import time
from flask import Flask, request, jsonify, send_from_directory
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


@app.route('/downloads/<path:filename>')
def serve_downloaded_file(filename):
    downloads_dir = os.path.join(BASE_DIR, "downloads")
    return send_from_directory(downloads_dir, filename)


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


@app.route('/debug/music', methods=['GET'])
def debug_music():
    """
    Quick isolated test for MusicEngine, bypassing agent/router/executor entirely.
    Usage: GET /debug/music?q=don%20xhoni%20100%25
    """
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"status": "error", "message": "Provide ?q=<song name>"}), 400

    if music_engine is None:
        return jsonify({"status": "error", "message": "music_engine is not initialized"}), 500

    try:
        logger.info(f"[/debug/music] Testing query: '{query}'")
        result = music_engine.play(query)
        logger.info(f"[/debug/music] Result: {result}")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"[/debug/music] Exception: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/process', methods=['POST', 'OPTIONS'])
def process_request():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        if agent is None or executor is None or router is None:
            logger.error("Core components not initialized (agent/executor/router is None)")
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

        # --- Agent: figure out intent/type for this input ---
        response_data = agent.handle_request(user_text)
        route_name = response_data.get("type", "unknown")
        logger.info(f"[Agent] route_name='{route_name}' intent='{response_data.get('intent')}' raw={response_data}")

        # --- Executor: actually perform the action for that route ---
        execution_result = executor.execute_action(route_name, response_data)
        logger.info(f"[Executor] execution_result={execution_result}")

        final_response = execution_result.get('response', response_data)

        if route_name == "music" or response_data.get("intent") == "play_music":
            logger.info(f"[Music Branch] response_data={response_data} | final_response(before)={final_response}")

            if not isinstance(final_response, dict):
                final_response = {"text": str(final_response)}

            if "data" not in final_response:
                final_response["data"] = {}

            if "audio_url" in response_data:
                final_response["data"]["stream_url"] = response_data["audio_url"]
            elif "audio_url" in final_response:
                final_response["data"]["stream_url"] = final_response["audio_url"]
            else:
                logger.info("[Music Branch] No audio_url found in response_data or final_response — "
                            "this is likely why the 'could not generate link' message appears.")

        if isinstance(final_response, dict) and 'status' not in final_response:
            final_response['status'] = 'success'

        logger.info(f"[Final Response] {final_response}")
        return jsonify(final_response), 200

    except Exception as e:
        logger.error(f"Processing Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal processing error",
            "details": str(e)
        }), 500


def run_cli():
    print("\n" + "=" * 50)
    print(" FALCONAI V3 - TERMINAL TEST MODE")
    print(" Type your command or type 'exit' to quit.")
    print("=" * 50 + "\n")

    while True:
        try:
            user_input = input("FalconAI > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "dalje"):
                print("Shutting down... Goodbye!")
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
                        print(f"[Response]:\n{weather_res.get('data', {}).get('text', weather_res)}\n")
                        continue
                    except Exception as w_err:
                        print(f"[Weather Error]: {w_err}")

            if agent and executor:
                response_data = agent.handle_request(user_input)
                route_name = response_data.get("type", "unknown")

                execution_result = executor.execute_action(route_name, response_data)

                final_res = execution_result.get('response', response_data)
                if isinstance(final_res, dict):
                    output_msg = final_res.get('message', final_res.get('text', str(final_res)))
                    if "audio_url" in final_res:
                        print(f"[Stream Link]: {final_res['audio_url']}")
                else:
                    output_msg = str(final_res)

                print(f"[Response]: {output_msg}\n")
            else:
                print("[Error]: Systems are not fully loaded.")
        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            break
        except Exception as e:
            print(f"[Processing Error]: {e}\n")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))

    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()

    run_cli()
