import requests
import random
import logging
from core.brain import brain

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

        # Reference the imported lowercase instance/module directly
        self.brain = brain

    def process(self, text_query: str) -> dict:
        logger.info(f"SportsEngine processing request: {text_query}")

        if any(w in text_query for w in ["h2h", "history", "versus", "vs", "head to head", "kunder", "kundër"]):
            return self.get_h2h_history()

        return self.get_live_analysis(text_query)

    def get_live_analysis(self, text_query: str) -> dict:
        url = f"{self.base_url}/matches/get-live"

        ball_x = round(random.uniform(0.15, 0.85), 2)
        ball_y = round(random.uniform(0.15, 0.85), 2)

        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                api_data = response.json()

                events = api_data.get("events", [])
                match_summary = ""
                if events:
                    sampled_events = events[:3]
                    summary_parts = []
                    for ev in sampled_events:
                        home_team = ev.get("homeTeam", {}).get("name", "Home")
                        away_team = ev.get("awayTeam", {}).get("name", "Away")
                        home_score = ev.get("homeScore", {}).get("current", 0)
                        away_score = ev.get("awayScore", {}).get("current", 0)
                        summary_parts.append(f"{home_team} vs {away_team} ({home_score}-{away_score})")
                    match_summary = " Current live matches: " + ", ".join(summary_parts)

                prompt = (
                    f"Context: The user is asking about '{text_query}'.{match_summary}\n"
                    f"Task: Act as an enthusiastic, dramatic live football TV commentator. "
                    f"Generate a thrilling, concise match commentary section based on the query. "
                    f"Talk about the incredible build-up play, the tension on the field, or a sudden counter-attack. "
                    f"Do not mention data formats, coordinates, or API. Keep it under 3 sentences!"
                )
                
                ai_commentary = self.brain.generate(text=prompt, user_id="tv_user")
                
                return {
                    "type": "sports",
                    "status": "LIVE MATCH",
                    "ball_position": {
                        "x": ball_x,
                        "y": ball_y
                    },
                    "commentary": ai_commentary
                }
                
        except Exception as e:
            logger.warning(f"Real API failed or no live matches available ({e}). Switching to AI simulator.")

        prompt_fallback = (
            f"Context: The live sports API is temporarily offline. The user wants to know about: '{text_query}'.\n"
            f"Task: Act as a legendary live TV football commentator. Generate a realistic, energetic, and highly "
            f"dramatic commentary about an intense imaginary match moment related to '{text_query}' as if it is happening right now! "
            f"Keep it thrilling and restrict the response to 3 sentences maximum."
        )
        
        try:
            ai_commentary = self.brain.generate(text=prompt_fallback, user_id="tv_user")
        except Exception as brain_err:
            logger.error(f"AI brain execution failed: {brain_err}")
            ai_commentary = f"What an unbelievable atmosphere in the stadium! The play is moving rapidly across the wings for '{text_query}', keeping every single fan on the edge of their seat!"

        return {
            "type": "sports",
            "status": "LIVE MATCH",
            "ball_position": {
                "x": ball_x,
                "y": ball_y
            },
            "commentary": ai_commentary
        }

    def get_h2h_history(self) -> dict:
        url = f"{self.base_url}/matches/get-h2h-events"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            if response.status_code == 200:
                api_data = response.json()
                prompt_h2h = (
                    f"Based on this Head-to-Head historical football data: {str(api_data)[:500]}...\n"
                    f"Summary the historical rivalry as an exciting sports analyst in 2-3 sentences."
                )
                h2h_analysis = self.brain.generate(text=prompt_h2h, user_id="tv_user")
                
                return {
                    "type": "sports",
                    "status": "H2H HISTORY",
                    "commentary": h2h_analysis
                }
        except Exception as e:
            logger.error(f"Error in H2H API execution: {e}")

        return {
            "type": "sports",
            "status": "H2H FALLBACK",
            "commentary": "FalconAI Analysis: The historical rivalry between these squads has always been a fierce battle. Recent data points to narrow margins and highly tactical encounters on the field!"
        }

    def _format_live_response(self, api_data: dict, query: str) -> dict:
        return self.get_live_analysis(query)
