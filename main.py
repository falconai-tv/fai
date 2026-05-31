import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# Sigurohemi që Python të gjejë folderat 'core' dhe 'engines' në nivelin rrënjë (root)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)  # Lejon kërkesat nga Web (Fetch) dhe Android pa bllokime CORS

ai_router = None

def initialize_falcon_system():
    """
    Inicializon të gjithë motorët e FalconAI dhe i injekton ato te Router-i kryesor.
    Përdor try-except për të kapur çdo gabim specifik gjatë ndezjes (boot).
    """
    global ai_router
    try:
        print("⏳ Duke inicializuar motorët e FalconAI...")
        
        # 1. Importet e moduleve tuaja
        from engines.music import MusicEngine
        from engines.web import WebEngine
        from engines.weather import WeatherEngine
        from core.router import Router  # Sipas skedarit tuaj core/router.py
        
        # 2. Instancimi i motorëve individualë
        music_geo = MusicEngine()
        web_geo = WebEngine()
        weather_geo = WeatherEngine()
        
        # 3. Krijimi i Router-it duke i kaluar të 3 argumentet e domosdoshme
        ai_router = Router(
            music_engine=music_geo, 
            web_engine=web_geo, 
            weather_engine=weather_geo
        )
        
        print("✅ FalconAI: Të gjitha sistemet u ndezën dhe u lidhën me sukses!")
        
    except ImportError as ie:
        print(f"❌ GABIM IMPORTI: Mungon ndonjë skedar ose librari në requirements.txt: {str(ie)}")
        ai_router = None
    except Exception as e:
        print(f"❌ GABIM KRITIK GJATË BOOT: Klasa Router dështoi të krijohet: {str(e)}")
        ai_router = None

# Thirrja e funksionit të inicializimit kur ndizet serveri në Railway
initialize_falcon_system()

@app.route('/')
def health_check():
    """Endpoint për të parë statusin e serverit përpara se të dërgosh kërkesa."""
    return jsonify({
        "status": "online",
        "router_initialized": ai_router is not None,
        "message": "FalconAI Server is up and running."
    }), 200

@app.route('/process', methods=['POST'])
def process():
    global ai_router
    
    # Sigurohemi që Router-i është gati përpara se të pranojmë kërkesën
    if ai_router is None:
        return jsonify({
            "status": "error",
            "message": "Router not initialized. Check server logs for boot errors."
        }), 500

    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON payload received"}), 400

        # Sinkronizimi: Pranon 'query' nga Android dhe 'text' nga testi në Web
        user_query = data.get('query') or data.get('text')
        
        if not user_query:
            return jsonify({"status": "error", "message": "Missing 'query' or 'text' field"}), 400

        # Thirrja e metodës të saktë .route() që ke definuar te core/router.py
        # Kjo metodë kthen automatikisht 'result' (dict) që pret aplikacioni
        response_data = ai_router.route(user_query)
        
        # Sigurohemi që nëse kthehet dict i thjeshtë, Flask e kthen në JSON valid me kodin 200
        return jsonify(response_data), 200

    except Exception as e:
        print(f"❌ GABIM GJATË PROCESIMIT: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"An error occurred inside the router: {str(e)}"
        }), 500

# --- KOORDINIMI I PORTËS PËR RAILWAY ---
if __name__ == '__main__':
    # Railway përdor portën dinamike përmes variablës së mjedisit PORT
    port = int(os.environ.get("PORT", 5000))
    # '0.0.0.0' lejon aplikacionin Android jashtë rrjetit lokal të lidhet me serverin
    app.run(host='0.0.0.0', port=port, debug=False)
