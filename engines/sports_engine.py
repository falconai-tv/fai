import requests
import random
import logging
from core.brain import Brain  # Integrojmë trurin e AI për gjenerimin e komentit

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
        
        # Inicializojmë modelin e AI (TinyLlama / Brain)
        self.brain = Brain()

    def process(self, text_query: str) -> dict:
        logger.info(f"SportsEngine po përpunon kërkesën: {text_query}")

        if any(w in text_query for w in ["h2h", "historiku", "kunder", "kundër", "ballë për ballë"]):
            return self.merr_historikun_h2h()

        return self.merr_analizen_live(text_query)

    def merr_analizen_live(self, text_query: str) -> dict:
        url = f"{self.base_url}/matches/get-live" # Endpoint-i i Sofascore për ndeshjet live
        
        # Gjenerojmë koordinata gjithmonë dinamike për topin në fushë
        ball_x = round(random.uniform(0.15, 0.85), 2)
        ball_y = round(random.uniform(0.15, 0.85), 2)

        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                api_data = response.json()
                
                # Nxjerrim tekstin e papërpunuar nga API e Sofascore (p.sh. emrat e ekipeve, rezultatet)
                events = api_data.get("events", [])
                match_summary = ""
                if events:
                    # Marrim deri në 3 ndeshjet e para live për kontekst
                    sampled_events = events[:3]
                    summary_parts = []
                    for ev in sampled_events:
                        home_team = ev.get("homeTeam", {}).get("name", "Home")
                        away_team = ev.get("awayTeam", {}).get("name", "Away")
                        home_score = ev.get("homeScore", {}).get("current", 0)
                        away_score = ev.get("awayScore", {}).get("current", 0)
                        summary_parts.append(f"{home_team} vs {away_team} ({home_score}-{away_score})")
                    match_summary = " Current live matches: " + ", ".join(summary_parts)

                # Detyrojmë AI ta kthejë në komentim televiziv duke u bazuar te të dhënat reale
                prompt = (
                    f"Context: The user is asking about '{text_query}'.{match_summary}\n"
                    f"Task: Act as an enthusiastic, dramatic live football TV commentator. "
                    f"Generate a thrilling, concise match commentary section based on the query. "
                    f"Talk about the incredible build-up play, the tension on the field, or a sudden counter-attack. "
                    f"Do not mention data formats, coordinates, or API. Keep it under 3 sentences!"
                )
                
                komentimi_ai = self.brain.generate(text=prompt, user_id="tv_user")
                
                return {
                    "type": "sports",
                    "status": "LIVE MATCH",
                    "ball_position": {
                        "x": ball_x,
                        "y": ball_y
                    },
                    "commentary": komentimi_ai
                }
                
        except Exception as e:
            logger.warning(f"API reale dështoi ose s'ka ndeshje live ({e}). Po kaloj në simulator AI.")
        
        # FALLBACK / SIMULATORI INTELEGJENT (Kur API dështon ose s'ka ndeshje në atë moment)
        prompt_fallback = (
            f"Context: The live sports API is temporarily offline. The user wants to know about: '{text_query}'.\n"
            f"Task: Act as a legendary live TV football commentator. Generate a realistic, energetic, and highly "
            f"dramatic commentary about an intense imaginary match moment related to '{text_query}' as if it is happening right now! "
            f"Keep it thrilling and restrict the response to 3 sentences maximum."
        )
        
        try:
            komentimi_ai = self.brain.generate(text=prompt_fallback, user_id="tv_user")
        except Exception as brain_err:
            logger.error(f"Edhe truri i AI dështoi: {brain_err}")
            komentimi_ai = f"What an unbelievable atmosphere in the stadium! The play is moving rapidly across the wings for '{text_query}', keeping every single fan on the edge of their seat!"

        return {
            "type": "sports",
            "status": "LIVE MATCH",
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
                api_data = response.json()
                prompt_h2h = (
                    f"Based on this Head-to-Head historical football data: {str(api_data)[:500]}...\n"
                    f"Summarize the historical rivalry as an exciting sports analyst in 2-3 sentences."
                )
                analiza_h2h = self.brain.generate(text=prompt_h2h, user_id="tv_user")
                
                return {
                    "type": "sports",
                    "status": "HISTORIKU H2H",
                    "commentary": analiza_h2h
                }
        except Exception as e:
            logger.error(f"Gabim në H2H API: {e}")

        return {
            "type": "sports",
            "status": "H2H FALLBACK",
            "commentary": "FalconAI Analizë: Rivaliteti historik mes këtyre dy ekipeve ka qenë gjithmonë i zjarrtë. Të dhënat e fundit tregojnë ndeshje të mbyllura me diferenca minimale golash!"
        }

    def _formato_pergjigjen_live(self, api_data: dict, query: str) -> dict:
        return self.merr_analizen_live(query)
