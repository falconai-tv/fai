import requests
import random
import logging

logger = logging.getLogger("FalconAI.SportsEngine")

class SportsEngine:
    def __init__(self):
        # Azhurnuar sipas cURL-it të ri të gjetur në RapidAPI
        self.host = "sofascore6.p.rapidapi.com"
        self.api_key = "53c1d74812msh8abfdd1e3b43de7p1002b4jsn9c3a24d3ec58"
        self.base_url = "https://sofascore6.p.rapidapi.com"
        
        self.headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": self.host,
            "x-rapidapi-key": self.api_key
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
        # Përdorim një match_id testuese (nga cURL-i yt) për të simuluar ose kapur të dhënat e sakta pozicionale
        test_match_id = "14083739"
        url = f"{self.base_url}/api/sofascore/v1/match/player-average-positions"
        params = {"match_id": test_match_id}

        # Koordinatat e topit në fushë (për Canvas-in e Android TV)
        ball_x = round(random.uniform(0.20, 0.80), 2)
        ball_y = round(random.uniform(0.20, 0.80), 2)
        
        players_positions = []
        status_msg = "SIMULATED TACTICS"

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=6)
            if response.status_code == 200:
                api_data = response.json()
                
                # Supozojmë se Sofascore kthen strukturën me lojtarë ('home' ose 'away')
                # Do të nxjerrim pikat X dhe Y për secilin lojtar nëse ekzistojnë në JSON
                points = api_data.get("points", []) or api_data.get("home", [])
                if points and isinstance(points, list):
                    status_msg = "LIVE REAL-TIME TACTICS"
                    for player in points[:11]:  # Marrim deri në 11 lojtarë
                        players_positions.append({
                            "name": player.get("player", {}).get("name", "Player"),
                            "jersey_number": player.get("player", {}).get("jerseyNumber", "0"),
                            "x": player.get("averageX", round(random.uniform(0.15, 0.85), 2)),
                            "y": player.get("averageY", round(random.uniform(0.15, 0.85), 2))
                        })
            else:
                logger.warning(f"Sofascore Positions API returned status: {response.status_code}")
        except Exception as e:
            logger.warning(f"Failed to fetch live player positions ({e}). Injecting safe simulation network.")

        # Nëse API nuk ktheu gjë ose dështoi, krijojmë 5 lojtarë fallbacks me koordinata dinamike që TV të vizatojë skemën pa dështuar
        if not players_positions:
            for i in range(1, 6):
                players_positions.append({
                    "name": f"Player {i}",
                    "jersey_number": str(random.randint(1, 99)),
                    "x": round(random.uniform(0.25, 0.75), 2),
                    "y": round(random.uniform(0.25, 0.75), 2)
                })

        return {
            "type": "sports_live",
            "status": status_msg,
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
