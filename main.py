import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# Sigurohemi që Python mund të gjejë folderin 'engines'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)  # Lejon kërkesat nga aplikacioni dhe web-i pa bllokime CORS

# --- INICIALIZIMI I ROUTER-IT ---
ai_router = None

def initialize_router():
    """
    Funksion për të instancuar IntentRouter me error handling të plotë.
    Ndihmon në identifikimin e saktë të problemeve gjatë boot-it në Railway.
    """
    global ai_router
    try:
        # Importimi bëhet brenda try që të kapim çdo dështim të librarive (si openai, requests etj.)
        from engines.router import IntentRouter
        ai_router = IntentRouter()
        print("✅ FalconAI: Router u inicializua me sukses.")
    except ImportError as e:
        print(f"❌ GABIM IMPORTI: Mungon një librari në requirements.txt: {e}")
    except Exception as e:
        print(f"❌ GABIM BOOT: Klasa IntentRouter dështoi: {e}")

# Thirrja e inicializimit në momentin që nis scripti
initialize_router()

@app.route('/')
def health_check():
    """Endpoint për të parë nëse serveri është gjallë dhe nëse Router është gati."""
    return jsonify({
        "status": "online",
        "router_ready": ai_router is not None,
        "environment": "production"
    }), 200

@app.route('/process', methods=['POST'])
def process():
    global ai_router
    
    # Kontrolli i parë: Nëse router nuk është inicializuar, mos provo më tej
    if ai_router is None:
        return jsonify({
            "status": "error",
            "message": "Router not initialized. Check server logs for boot errors."
        }), 500

    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON data provided"}), 400

        # Kapim tekstin pavarësisht nëse vjen si 'query' apo 'text'
        user_input = data.get('query') or data.get('text')
        
        if not user_input:
            return jsonify({"status": "error", "message": "Missing 'query' or 'text' field"}), 400

        print(f"🚀 Processing: {user_input}")

        # Thirrja e motorit të AI (handle duhet të kthejë një fjalor/dict)
        # Supozojmë se handle kthen të dhënat që pret Android (WeatherActivity, News, etj.)
        response_data = ai_router.handle(user_input)
        
        return jsonify(response_data), 200

    except Exception as e:
        print(f"❌ GABIM GJATË PROCESIMIT: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Server encountered an error: {str(e)}"
        }), 500

# --- KONFIGURIMI I PORTËS PËR RAILWAY ---
if __name__ == '__main__':
    # Railway injekton portën automatikisht përmes variablës PORT
    port = int(os.environ.get("PORT", 5000))
    # '0.0.0.0' është e domosdoshme që serveri të jetë i aksesueshëm nga jashtë
    app.run(host='0.0.0.0', port=port, debug=False)
