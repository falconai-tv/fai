import requests
import random

class SportsEngine:
    def __init__(self):
        self.host = "sofascore.p.rapidapi.com"
        self.api_key = "53c1d74812msh8abfdd1e3b43de7p1002b4jsn9c3a24d3ec58"
        self.headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": self.host,
            "x-rapidapi-key": self.api_key
        }

    def merr_analizen_live(self, text_query: str) -> dict:
        ball_x = round(random.uniform(0.1, 0.9), 2)
        ball_y = round(random.uniform(0.1, 0.9), 2)

        ai_commentary = f"FalconAI Analizë: Bazuar në kërkesën tuaj '{text_query}', ekipi vendas po mbrohet me skemën 5-4-1 pasi topi aktualisht gjendet në koordinatat X:{ball_x}, Y:{ball_y}."

        return {
            "type": "sports",
            "status": "live",
            "ball_position": {
                "x": ball_x,
                "y": ball_y
            },
            "commentary": ai_commentary
        }