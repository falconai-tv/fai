import logging
import random
import threading
from ytmusicapi import YTMusic

logger = logging.getLogger("FalconAI.MusicEngine")

MOOD_QUERIES = {
    "ecstatic": ["The Weeknd upbeat", "Travis Scott hype", "Dua Lipa dance hits"],
    "happy": ["Bad Bunny summer hits", "Bruno Mars happy", "Pop radio hits 2026"],
    "romantic": ["Ed Sheeran romantic", "Drake R&B love", "Taylor Swift love songs"],
    "motivated": ["Eminem workout", "Gym motivational hits", "Kanye West hype"],
    "calm": ["Lofi Girl study beats", "Coldplay acoustic", "Chill ambient piano"],
    "nostalgic": ["90s hip hop classics", "2000s pop hits", "Retro throwback classics"],
    "focused": ["Deep focus lofi", "Coding instrumental beats", "Hans Zimmer score"],
    "anxious": ["Calming piano instrumental", "Meditation ambient soundscapes"],
    "angry": ["Rage Against the Machine", "Linkin Park heavy", "Aggressive workout rap"],
    "heartbreak": ["Olivia Rodrigo sad", "Adele emotional", "Sad breakup songs"],
    "lonely": ["Billie Eilish sad", "Passenger acoustic", "Melancholy indie acoustic"],
    "melancholy": ["Zack Hemsey melancholic", "Interstellar theme ambient"],
}

MOOD_KEYWORDS = {
    "ecstatic": ["ecstatic", "incredible", "best day", "pumped", "euphoric", "unstoppable", "electric"],
    "happy": ["happy", "great", "wonderful", "joyful", "good mood", "cheerful", "feel good"],
    "romantic": ["love", "romantic", "crush", "in love", "valentine", "sweetheart"],
    "motivated": ["motivated", "grind", "hustle", "determined", "driven", "ambitious", "lets go"],
    "calm": ["calm", "peaceful", "relax", "chill", "serene", "tranquil", "quiet"],
    "nostalgic": ["nostalgic", "remember", "old times", "childhood", "memories", "throwback"],
    "focused": ["focus", "study", "work", "concentrate", "coding", "homework", "lofi"],
    "anxious": ["anxious", "nervous", "worried", "scared", "stressed", "panic"],
    "angry": ["angry", "furious", "rage", "mad", "frustrated", "irritated", "pissed"],
    "heartbreak": ["heartbreak", "breakup", "broke up", "left me", "dumped", "broken heart"],
    "lonely": ["lonely", "alone", "isolated", "empty", "abandoned"],
    "melancholy": ["sad", "depressed", "down", "unhappy", "cry", "upset", "pain"],
}

MOOD_MESSAGES = {
    "ecstatic": "You're on top of the world! Here's something to match:",
    "happy": "Love the good vibes! Here's something cheerful:",
    "romantic": "Feeling the love? Here's something tender:",
    "motivated": "Let's go! Here's something to fuel that drive:",
    "calm": "Staying calm. Here's something peaceful:",
    "nostalgic": "Taking a trip down memory lane:",
    "focused": "In the zone! Here's something to keep you there:",
    "anxious": "Take a breath. Here's something to ease your mind:",
    "angry": "Let it out. Here's something intense:",
    "heartbreak": "Going through it is tough. Here's music that gets it:",
    "lonely": "You're not alone. Here's something that understands:",
    "melancholy": "I feel you. Here's something that understands:",
}

MOOD_INTENSITY = {
    "ecstatic": 10, "angry": 9, "motivated": 8, "heartbreak": 8,
    "happy": 7, "anxious": 7, "romantic": 6, "lonely": 6,
    "melancholy": 5, "nostalgic": 5, "focused": 4, "calm": 3
}

class MusicEngine:
    def __init__(self):
        self.is_playing = False
        self.played = set()
        self.ytm = YTMusic()
        logger.info("[MUSIC] MusicEngine initialized with YouTube Music!")

    def analyze_mood(self, text):
        text = text.lower().strip()
        scores = {}
        for mood, keywords in MOOD_KEYWORDS.items():
            score = sum(len(kw.split()) for kw in keywords if kw in text)
            if score > 0:
                scores[mood] = score

        if scores:
            best_mood = max(scores, key=scores.get)
            intensity = MOOD_INTENSITY.get(best_mood, 5)
            if any(b in text for b in ["very", "so", "really", "extremely", "totally"]):
                intensity = min(intensity + 2, 10)
            return best_mood, intensity

        return "calm", 5

    def search_ytmusic(self, mood, intensity):
        queries = MOOD_QUERIES.get(mood, ["chill music"])
        query = random.choice(queries)

        try:
            results = self.ytm.search(query, filter="songs", limit=10)
            if not results:
                return None

            fresh = [r for r in results if r.get("videoId") not in self.played]
            if not fresh:
                self.played.clear()
                fresh = results

            track = random.choice(fresh)
            video_id = track.get("videoId")
            self.played.add(video_id)

            thumbnails = track.get("thumbnails", [])
            cover_url = thumbnails[-1]["url"] if thumbnails else ""

            artists = track.get("artists", [])
            artist_name = artists[0]["name"] if artists else "Unknown Artist"

            return {
                "id": video_id,
                "title": track.get("title", "Unknown Track"),
                "uploader": artist_name,
                "album": track.get("album", {}).get("name", "Single"),
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "stream_url": f"https://music.youtube.com/watch?v={video_id}",
                "cover": cover_url,
                "duration": track.get("duration_seconds", 0)
            }

        except Exception as e:
            logger.error(f"[MUSIC] YouTube Music search failed: {e}")
            return None

    def process(self, text):
        mood, intensity = self.analyze_mood(text)
        message = MOOD_MESSAGES.get(mood, "Here's some music for you:")

        track = self.search_ytmusic(mood, intensity)
        if not track:
            return {
                "type": "music",
                "data": {
                    "text": f"{message}\n\n 🎵 Chill Music\n 🎭 Mood: {mood.capitalize()}"
                }
            }

        title = track.get("title", "Unknown")
        uploader = track.get("uploader", "Unknown")
        duration = track.get("duration", 0)
        mins = duration // 60
        secs = duration % 60

        response_text = (
            f"{message}\n\n"
            f" 🎵 {title}\n"
            f" 👤 {uploader}\n"
            f" 🎭 Mood     : {mood.capitalize()}\n"
            f" ⚡ Intensity : {intensity}/10\n"
            f" ⏱️  Duration  : {mins}:{secs:02d}\n"
        )

        return {
            "type": "music",
            "data": {
                "mood": mood,
                "intensity": intensity,
                "track": track,
                "text": response_text
            }
        }
