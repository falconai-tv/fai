import requests
import random
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    API_FOOTBALL_KEY,
    API_FOOTBALL_URL,
    SPORTS_API_TIMEOUT,
    FORMATIONS,
    DEFAULT_FORMATION,
    SUPPORTED_LEAGUES
)

logger = logging.getLogger("FalconAI.SportsEngine")


class SportsEngine:
    def __init__(self):
        self.headers = {
            "x-apisports-key": API_FOOTBALL_KEY
        }
        self.base_url = API_FOOTBALL_URL

        self.team_aliases = {
            "real":        "real madrid",
            "barca":       "barcelona",
            "city":        "manchester city",
            "united":      "manchester united",
            "arsenal":     "arsenal",
            "chelsea":     "chelsea",
            "liverpool":   "liverpool",
            "juventus":    "juventus",
            "milan":       "ac milan",
            "inter":       "inter",
            "napoli":      "napoli",
            "psg":         "paris saint-germain",
            "paris":       "paris saint-germain",
            "bayern":      "bayern munich",
            "dortmund":    "borussia dortmund",
            "atletico":    "atletico madrid",
            "sevilla":     "sevilla",
            "portugal":    "portugal",
            "albania":     "albania",
            "kosovo":      "kosovo",
            "serbia":      "serbia",
            "brazil":      "brazil",
            "argentina":   "argentina",
            "france":      "france",
            "england":     "england",
            "germany":     "germany",
            "spain":       "spain",
            "italy":       "italy",
        }

    def process(self, text_query: str) -> dict:
        logger.info(f"[SPORTS] Processing: {text_query}")
        query = text_query.lower().strip()

        if any(w in query for w in ["h2h", "history", "versus", "vs", "head to head",
                                     "past matches", "previous matches", "record"]):
            return self.get_h2h(query)

        return self.get_live_analysis(query)

    def get_live_analysis(self, query: str) -> dict:
        live_matches = self.fetch_live_matches()

        home_team = "Home"
        away_team = "Away"
        match_id  = None
        fixture   = None
        stats     = {}

        team_name = self.extract_team_name(query)

        if live_matches:
            fixture, match_id = self.find_match(team_name, live_matches)

        if fixture:
            home_team = fixture.get("teams", {}).get("home", {}).get("name", "Home")
            away_team = fixture.get("teams", {}).get("away", {}).get("name", "Away")
            score_h   = fixture.get("goals", {}).get("home", 0) or 0
            score_a   = fixture.get("goals", {}).get("away", 0) or 0
            minute    = fixture.get("fixture", {}).get("status", {}).get("elapsed", 0) or 0

            if match_id:
                stats = self.fetch_match_stats(match_id)

            lineups = self.fetch_lineups(match_id) if match_id else {}

            players, ball = self.generate_intelligent_positions(stats, lineups, home_team, away_team)

            commentary = self.generate_smart_commentary(
                players, ball, home_team, away_team, stats, minute, score_h, score_a
            )

            return {
                "type":               "sports_live",
                "status":             "LIVE REAL-TIME",
                "match":              f"{home_team} vs {away_team}",
                "score":              f"{score_h} - {score_a}",
                "minute":             minute,
                "match_id_processed": match_id,
                "ball_position":      ball,
                "players":            players,
                "stats":              stats,
                "commentary":         commentary
            }

        if not live_matches:
            return self.no_live_response()

        first     = live_matches[0]
        match_id  = str(first.get("fixture", {}).get("id", ""))
        home_team = first.get("teams", {}).get("home", {}).get("name", "Home")
        away_team = first.get("teams", {}).get("away", {}).get("name", "Away")
        score_h   = first.get("goals", {}).get("home", 0) or 0
        score_a   = first.get("goals", {}).get("away", 0) or 0
        minute    = first.get("fixture", {}).get("status", {}).get("elapsed", 0) or 0

        stats   = self.fetch_match_stats(match_id)
        lineups = self.fetch_lineups(match_id)
        players, ball = self.generate_intelligent_positions(stats, lineups, home_team, away_team)
        commentary = self.generate_smart_commentary(
            players, ball, home_team, away_team, stats, minute, score_h, score_a
        )

        logger.info(f"[SPORTS] No team match found. Showing first live: {home_team} vs {away_team}")

        return {
            "type":               "sports_live",
            "status":             "LIVE — FIRST AVAILABLE",
            "match":              f"{home_team} vs {away_team}",
            "score":              f"{score_h} - {score_a}",
            "minute":             minute,
            "match_id_processed": match_id,
            "ball_position":      ball,
            "players":            players,
            "stats":              stats,
            "commentary":         commentary
        }

    def fetch_live_matches(self) -> list:
        try:
            url      = f"{self.base_url}/fixtures"
            response = requests.get(
                url,
                headers=self.headers,
                params={"live": "all"},
                timeout=SPORTS_API_TIMEOUT
            )

            if response.status_code == 200:
                data    = response.json()
                matches = data.get("response", [])
                logger.info(f"[SPORTS] Live matches found: {len(matches)}")
                return matches

            logger.warning(f"[SPORTS] API returned status: {response.status_code}")

        except Exception as e:
            logger.warning(f"[SPORTS] fetch_live_matches failed: {e}")

        return []

    def fetch_match_stats(self, fixture_id: str) -> dict:
        try:
            url      = f"{self.base_url}/fixtures/statistics"
            response = requests.get(
                url,
                headers=self.headers,
                params={"fixture": fixture_id},
                timeout=SPORTS_API_TIMEOUT
            )

            if response.status_code == 200:
                data  = response.json()
                items = data.get("response", [])

                if len(items) >= 2:
                    home_stats = {s["type"]: s["value"] for s in items[0].get("statistics", [])}
                    away_stats = {s["type"]: s["value"] for s in items[1].get("statistics", [])}

                    def safe_int(val):
                        if val is None:
                            return 0
                        if isinstance(val, str) and "%" in val:
                            return int(val.replace("%", "").strip())
                        try:
                            return int(val)
                        except (ValueError, TypeError):
                            return 0

                    return {
                        "possession_home":  safe_int(home_stats.get("Ball Possession", "50%")),
                        "possession_away":  safe_int(away_stats.get("Ball Possession", "50%")),
                        "shots_home":       safe_int(home_stats.get("Total Shots", 0)),
                        "shots_away":       safe_int(away_stats.get("Total Shots", 0)),
                        "shots_on_home":    safe_int(home_stats.get("Shots on Goal", 0)),
                        "shots_on_away":    safe_int(away_stats.get("Shots on Goal", 0)),
                        "corners_home":     safe_int(home_stats.get("Corner Kicks", 0)),
                        "corners_away":     safe_int(away_stats.get("Corner Kicks", 0)),
                        "attacks_home":     safe_int(home_stats.get("Total Attacks", 0)),
                        "attacks_away":     safe_int(away_stats.get("Total Attacks", 0)),
                        "dangerous_home":   safe_int(home_stats.get("Dangerous Attacks", 0)),
                        "dangerous_away":   safe_int(away_stats.get("Dangerous Attacks", 0)),
                        "fouls_home":       safe_int(home_stats.get("Fouls", 0)),
                        "fouls_away":       safe_int(away_stats.get("Fouls", 0)),
                        "yellow_home":      safe_int(home_stats.get("Yellow Cards", 0)),
                        "yellow_away":      safe_int(away_stats.get("Yellow Cards", 0)),
                    }

        except Exception as e:
            logger.warning(f"[SPORTS] fetch_match_stats failed: {e}")

        return {}

    def fetch_lineups(self, fixture_id: str) -> dict:
        try:
            url      = f"{self.base_url}/fixtures/lineups"
            response = requests.get(
                url,
                headers=self.headers,
                params={"fixture": fixture_id},
                timeout=SPORTS_API_TIMEOUT
            )

            if response.status_code == 200:
                data  = response.json()
                items = data.get("response", [])

                if len(items) >= 2:
                    return {
                        "home": {
                            "formation": items[0].get("formation", DEFAULT_FORMATION),
                            "players": [
                                {
                                    "name":   p.get("player", {}).get("name", f"Player {i+1}"),
                                    "number": str(p.get("player", {}).get("number", i+1)),
                                    "pos":    p.get("player", {}).get("pos", "")
                                }
                                for i, p in enumerate(items[0].get("startXI", []))
                            ]
                        },
                        "away": {
                            "formation": items[1].get("formation", DEFAULT_FORMATION),
                            "players": [
                                {
                                    "name":   p.get("player", {}).get("name", f"Player {i+1}"),
                                    "number": str(p.get("player", {}).get("number", i+1)),
                                    "pos":    p.get("player", {}).get("pos", "")
                                }
                                for i, p in enumerate(items[1].get("startXI", []))
                            ]
                        }
                    }

        except Exception as e:
            logger.warning(f"[SPORTS] fetch_lineups failed: {e}")

        return {}

    def generate_intelligent_positions(self, stats: dict, lineups: dict, home_name: str, away_name: str):
        possession_home = stats.get("possession_home", 50)
        possession_away = stats.get("possession_away", 50)
        dangerous_home  = stats.get("dangerous_home", 0)
        dangerous_away  = stats.get("dangerous_away", 0)
        corners_home    = stats.get("corners_home", 0)
        corners_away    = stats.get("corners_away", 0)

        home_formation = lineups.get("home", {}).get("formation", DEFAULT_FORMATION)
        away_formation = lineups.get("away", {}).get("formation", DEFAULT_FORMATION)

        if home_formation not in FORMATIONS:
            home_formation = DEFAULT_FORMATION
        if away_formation not in FORMATIONS:
            away_formation = DEFAULT_FORMATION

        home_base = FORMATIONS[home_formation]["home"]
        away_base = FORMATIONS[away_formation]["away"]

        home_players = lineups.get("home", {}).get("players", [])
        away_players = lineups.get("away", {}).get("players", [])

        home_pressure = (possession_home - 50) / 100   # -0.5 to +0.5
        away_pressure = (possession_away - 50) / 100

        if dangerous_home > dangerous_away * 1.5:
            ball_x = round(random.uniform(0.65, 0.90), 2)
            ball_y = round(random.uniform(0.25, 0.75), 2)
        elif dangerous_away > dangerous_home * 1.5:
            ball_x = round(random.uniform(0.10, 0.35), 2)
            ball_y = round(random.uniform(0.25, 0.75), 2)
        elif corners_home > corners_away:
            ball_x = round(random.uniform(0.85, 0.98), 2)
            ball_y = round(random.choice([
                random.uniform(0.02, 0.15),
                random.uniform(0.85, 0.98)
            ]), 2)
        elif corners_away > corners_home:
            ball_x = round(random.uniform(0.02, 0.15), 2)
            ball_y = round(random.choice([
                random.uniform(0.02, 0.15),
                random.uniform(0.85, 0.98)
            ]), 2)
        else:
            ball_x = round(random.uniform(0.35, 0.65), 2)
            ball_y = round(random.uniform(0.20, 0.80), 2)

        ball = {"x": ball_x, "y": ball_y}

        players = []

        for i, base in enumerate(home_base):
            name   = home_players[i]["name"]   if i < len(home_players) else f"Home {i+1}"
            number = home_players[i]["number"] if i < len(home_players) else str(i+1)

            x_shift = home_pressure * 0.12
            x_noise = random.uniform(-0.03, 0.03)
            y_noise = random.uniform(-0.04, 0.04)

            x = round(min(max(base["x"] + x_shift + x_noise, 0.02), 0.97), 2)
            y = round(min(max(base["y"] + y_noise, 0.02), 0.97), 2)

            players.append({
                "name":          name,
                "jersey_number": number,
                "team":          "home",
                "role":          base["role"],
                "x":             x,
                "y":             y
            })

        for i, base in enumerate(away_base):
            name   = away_players[i]["name"]   if i < len(away_players) else f"Away {i+1}"
            number = away_players[i]["number"] if i < len(away_players) else str(i+1)

            x_shift = away_pressure * 0.12
            x_noise = random.uniform(-0.03, 0.03)
            y_noise = random.uniform(-0.04, 0.04)

            x = round(min(max(base["x"] - x_shift + x_noise, 0.02), 0.97), 2)
            y = round(min(max(base["y"] + y_noise, 0.02), 0.97), 2)

            players.append({
                "name":          name,
                "jersey_number": number,
                "team":          "away",
                "role":          base["role"],
                "x":             x,
                "y":             y
            })

        return players, ball

    def generate_smart_commentary(self, players, ball, home, away,stats, minute, score_h, score_a) -> str:
        closest  = None
        min_dist = float("inf")
        for p in players:
            dist = ((p["x"] - ball["x"]) ** 2 + (p["y"] - ball["y"]) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                closest  = p

        bx = ball["x"]
        if bx > 0.80:
            zone   = f"the danger zone — {away}'s penalty area"
            action = "Huge chance! Shot incoming!"
        elif bx > 0.65:
            zone   = f"{home}'s attacking third"
            action = "High pressure from the home side!"
        elif bx < 0.20:
            zone   = f"the danger zone — {home}'s penalty area"
            action = "Counter-attack! Defensive alert!"
        elif bx < 0.35:
            zone   = f"{away}'s attacking third"
            action = "Away side building up the attack!"
        else:
            zone   = "the midfield"
            action = "Controlled possession play."

        poss_h  = stats.get("possession_home", 50)
        poss_a  = stats.get("possession_away", 50)
        shots_h = stats.get("shots_home", 0)
        shots_a = stats.get("shots_away", 0)
        on_h    = stats.get("shots_on_home", 0)
        on_a    = stats.get("shots_on_away", 0)
        dan_h   = stats.get("dangerous_home", 0)
        dan_a   = stats.get("dangerous_away", 0)

        player_name = closest["name"] if closest else "Unknown player"
        team_label  = home if closest and closest["team"] == "home" else away

        lines = [
            f"⏱️  Minute {minute}' — {home} {score_h}:{score_a} {away}",
            f"",
            f"🟡 {player_name} ({team_label}) on the ball in {zone}. {action}",
            f"",
            f"📊 Possession   : {home} {poss_h}% — {away} {poss_a}%",
            f"🎯 Total Shots  : {home} {shots_h} — {away} {shots_a}",
            f"🔵 Shots on Goal: {home} {on_h} — {away} {on_a}",
            f"⚡ Danger Attacks: {home} {dan_h} — {away} {dan_a}",
        ]

        if dan_h > dan_a * 1.5:
            lines.append(f"\n🔮 Prediction: {home} are highly likely to score — dominant pressure!")
        elif dan_a > dan_h * 1.5:
            lines.append(f"\n🔮 Prediction: {away} are threatening seriously — danger on the counter!")
        elif shots_h > shots_a + 4:
            lines.append(f"\n🔮 Prediction: {home} are creating more chances — goal could come soon!")
        elif shots_a > shots_h + 4:
            lines.append(f"\n🔮 Prediction: {away} are pushing hard — equalizer or lead incoming!")
        else:
            lines.append(f"\n🔮 Prediction: Tight match — any moment could be decisive!")

        return "\n".join(lines)

    def get_h2h(self, query: str) -> dict:
        live = self.fetch_live_matches()

        team_name = self.extract_team_name(query)
        fixture, match_id = self.find_match(team_name, live) if live else (None, None)

        if not fixture:
            return {
                "type":       "sports_live",
                "status":     "H2H HISTORY",
                "commentary": "No active match found for H2H lookup. Try searching by team name!"
            }

        home_id = fixture.get("teams", {}).get("home", {}).get("id", "")
        away_id = fixture.get("teams", {}).get("away", {}).get("id", "")
        home_nm = fixture.get("teams", {}).get("home", {}).get("name", "Home")
        away_nm = fixture.get("teams", {}).get("away", {}).get("name", "Away")

        try:
            url      = f"{self.base_url}/fixtures/headtohead"
            response = requests.get(
                url,
                headers=self.headers,
                params={"h2h": f"{home_id}-{away_id}", "last": 5},
                timeout=SPORTS_API_TIMEOUT
            )

            if response.status_code == 200:
                data      = response.json()
                matches   = data.get("response", [])
                home_wins = 0
                away_wins = 0
                draws     = 0

                lines = [f"📋 H2H — {home_nm} vs {away_nm} (Last 5 matches):\n"]

                for m in matches[:5]:
                    h    = m.get("teams", {}).get("home", {}).get("name", "?")
                    a    = m.get("teams", {}).get("away", {}).get("name", "?")
                    gh   = m.get("goals", {}).get("home", 0)
                    ga   = m.get("goals", {}).get("away", 0)
                    date = m.get("fixture", {}).get("date", "")[:10]
                    lines.append(f"  {date}:  {h} {gh} – {ga} {a}")

                    winner = m.get("teams", {}).get("home", {}).get("winner")
                    if winner is True:
                        if h == home_nm: home_wins += 1
                        else:            away_wins += 1
                    elif winner is False:
                        if a == home_nm: home_wins += 1
                        else:            away_wins += 1
                    else:
                        draws += 1

                lines.append(
                    f"\n🏆 {home_nm}: {home_wins} wins  |  "
                    f"Draws: {draws}  |  "
                    f"{away_nm}: {away_wins} wins"
                )

                return {
                    "type":       "sports_live",
                    "status":     "H2H HISTORY",
                    "commentary": "\n".join(lines)
                }

        except Exception as e:
            logger.warning(f"[SPORTS] H2H fetch failed: {e}")

        return {
            "type":       "sports_live",
            "status":     "H2H HISTORY",
            "commentary": f"FalconAI Analysis: The H2H record between {home_nm} and {away_nm} is historically very tight!"
        }

    def extract_team_name(self, query: str) -> str:
        for alias, real_name in self.team_aliases.items():
            if alias in query:
                return real_name

        words = [w for w in query.split() if len(w) > 3]
        return words[-1] if words else ""

    def find_match(self, team_name: str, live_matches: list):
        if not team_name:
            return None, None

        for match in live_matches:
            home = match.get("teams", {}).get("home", {}).get("name", "").lower()
            away = match.get("teams", {}).get("away", {}).get("name", "").lower()

            if team_name.lower() in home or team_name.lower() in away:
                match_id = str(match.get("fixture", {}).get("id", ""))
                logger.info(f"[SPORTS] Match found: {home} vs {away} (ID: {match_id})")
                return match, match_id

        return None, None

    def no_live_response(self) -> dict:
        return {
            "type":          "sports_live",
            "status":        "NO_LIVE_MATCHES",
            "players":       [],
            "ball_position": {"x": 0.5, "y": 0.5},
            "commentary": (
                "⚽ No live matches at the moment.\n"
                "Try again later or ask for H2H history between two teams!"
            )
        }
