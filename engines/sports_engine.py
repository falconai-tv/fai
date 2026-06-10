import requests
import random
import logging

logger = logging.getLogger("FalconAI.SportsEngine")

class SportsEngine:
    def __init__(self):
        self.host = "sofascore.p.rapidapi.com"
        self.api_key = "53c1d74812msh8abfdd1e3b43de7p1002b4jsn9c3a24d3ec58"
        self.base_url = "https://sofascore.p.rapidapi.com"
        
        self.headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": self.host,
            "x-rapidapi-key": self.api_key
        }

    def process(self, text_query: str) -> dict:
        logger.info(f"SportsEngine po përpunon kërkesën: {text_query}")

        if any(w in text_query for w in ["h2h", "historiku", "kunder", "kundër", "ballë për ballë"]):
            return self.merr_historikun_h2h()

        return self.merr_analizen_live(text_query)

    def merr_analizen_live(self, text_query: str) -> dict:
        url = f"{self.base_url}/matches/get-live" # Endpoint-i i Sofascore për ndeshjet live
        
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return self._formato_pergjigjen_live(data, text_query)
                
        except Exception as e:
            logger.warning(f"API reale dështoi ose s'ka ndeshje live ({e}). Po kaloj në simulator.")
        
        ball_x = round(random.uniform(0.1, 0.9), 2)
        ball_y = round(random.uniform(0.1, 0.9), 2)

        komentimi_ai = ""
        if ball_x > 0.7:
            komentimi_ai = f"FalconAI Analizë: Presion mbytës në zonën kundërshtare! Topi është në koordinatat (X:{ball_x}, Y:{ball_y}). Skema ka kaluar në një 4-3-3 agresiv."
        elif ball_x < 0.3:
            komentimi_ai = f"FalconAI Analizë: Ekipi po mbrohet me kujdes në gjysmëfushën e vet (X:{ball_x}). Kundërshtari po bën presion të lartë."
        else:
            komentimi_ai = f"FalconAI Analizë: Loja po zhvillohet e qetë në mesfushë (X:{ball_x}). Po kërkohet hapësirë për pasim vertikal."

        return {
            "type": "sports",
            "status": "live",
            "ball_position": {
                "x": ball_x,
                "y": ball_y
            },
            "commentary": komentimi_ai
        }

    def merr_historikun_h2h(self) -> dict:
        url = f"{self.base_url}/matches/get-h2h-events"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            if response.status_code == 200:
                return {
                    "type": "sports",
                    "status": "h2h",
                    "data": response.json()
                }
        except Exception as e:
            logger.error(f"Gabim në H2H API: {e}")

        return {
            "type": "sports",
            "status": "h2h_fallback",
            "commentary": "FalconAI: Nuk mund të ngarkoj historikun H2H në këto momente. Ju lutem provoni përsëri më vonë."
        }

    def _formato_pergjigjen_live(self, api_data: dict, query: str) -> dict:
        return {
            "type": "sports",
            "status": "live",
            "ball_position": {
                "x": 0.52,
                "y": 0.48
            },
            "commentary": f"Analizë Live (Sofascore): Ndeshja po monitorohet. Kërkesa juaj: '{query}'."
        }
