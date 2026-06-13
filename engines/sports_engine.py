import requests
import random
import logging

logger = logging.getLogger("FalconAI.SportsEngine")

class SportsEngine:
    def __init__(self):
        self.host = "sofascore6.p.rapidapi.com"
        self.api_key = "53c1d74812msh8abfdd1e3b43de7p1002b4jsn9c3a24d3ec58"
        self.base_url = "https://sofascore6.p.rapidapi.com"
        
        self.headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": self.host,
            "x-rapidapi-key": self.api_key
        }

        # Match Locator Matrix: Mapon skuadrat e mëdha me ID-të e tyre aktuale në Sofascore për testim të saktë live
        self.live_match_registry = {
            "qatar": "14083739",
            "switzerland": "14083739",
            "madrid": "14083740",
            "barcelona": "14083740",
            "arsenal": "14083741",
            "chelsea": "14083742",
            "liverpool": "14083743",
            "city": "14083743"
        }

    def process(self, text_query: str) -> dict:
        logger.info(f"SportsEngine processing request: {text_query}")
        text_query = text_query.lower()

        if any(w in text_query for w in ["h2h", "history", "versus", "vs", "head to head", "kunder", "kundër"]):
            return self.get_h2h_history()

        return self.get_live_analysis(text_query)

    def generate_commentary(self, query: str) -> str:
        commentary_templates = [
            f"Unbelievable vision out there on the pitch! The tactical build-up for '{query}' is absolute poetry in motion right now!",
            f"High tactical pressure high up the pitch! The team is trying hard to break down the opponent's defensive line!",
            f"What a stunning counter-attack! Massive space opening up on the wings as they push forward on this critical play!"
        ]
        return random.choice(commentary_templates)

    def get_live_analysis(self, text_query: str) -> dict:
        # Përcaktimi i ID-së dinamike: nëse nuk përputhet asnjë skuadër, përdoret ID-ja jote '14083739' si Default
        match_id = "14083739"
        for team, m_id in self.live_match_registry.items():
            if team in text_query:
                match_id = m_id
                break

        url = f"{self.base_url}/api/sofascore/v1/match/player-average-positions"
        params = {"match_id": match_id}

        # Koordinatat dinamike të topit për Canvas-in në Android TV
        ball_x = round(random.uniform(0.20, 0.80), 2)
        ball_y = round(random.uniform(0.20, 0.80), 2)
        
        players_positions = []
        status_msg = "SIMULATED TACTICS"

        try:
            logger.info(f"Executing Sofascore API hit for match_id: {match_id}")
            response = requests.get(url, headers=self.headers, params=params, timeout=6)
            
            if response.status_code == 200:
                api_data = response.json()
                
                # Leximi i saktë i pikëve nga struktura e Sofascore
                points = api_data.get("points", []) or api_data.get("home", [])
                if points and isinstance(points, list):
                    status_msg = "LIVE REAL-TIME TACTICS"
                    for player in points[:11]:  # Kapim formacionin bazë (11 lojtarë)
                        players_positions.append({
                            "name": player.get("player", {}).get("name", "Player"),
                            "jersey_number": str(player.get("player", {}).get("jerseyNumber", random.randint(1, 99))),
                            "x": player.get("averageX", round(random.uniform(0.15, 0.85), 2)),
                            "y": player.get("averageY", round(random.uniform(0.15, 0.85), 2))
                        })
            else:
                logger.warning(f"Sofascore API returned response code: {response.status_code}")
                
        except Exception as e:
            logger.warning(f"Sofascore live API connection failed ({e}). Running adaptive simulation mode.")

        # FALLBACK: Nëse nuk ka lojtarë live ose API është e mbingarkuar, gjenerohen koordinata automatike elastike
        if not players_positions:
            for i in range(1, 12):
                players_positions.append({
                    "name": f"Lineup Node {i}",
                    "jersey_number": str(random.randint(1, 99)),
                    "x": round(random.uniform(0.20, 0.80), 2),
                    "y": round(random.uniform(0.15, 0.85), 2)
                })

        return {
            "type": "sports_live",
            "status": status_msg,
            "match_id_processed": match_id,
            "ball_position": {
                "x": ball_x,
                "y": ball_y
            },
            "players": players_positions,
            "commentary": self.generate_commentary(text_query)
        }

    def get_h2h_history(self) -> dict:
        return {
            "type": "sports_live",
            "status": "H2H HISTORY",
            "commentary": "FalconAI Analysis: Historically, this matchup delivers sheer tactical warfare. Both squads show a razor-thin goal variance over their last structural head-to-head encounters!"
        }
