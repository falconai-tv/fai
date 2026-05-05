import yt_dlp
import subprocess
import threading
import logging
import os
import random

logger = logging.getLogger("FalconAI.MusicEngine")

MOOD_QUERIES = {
    "ecstatic":   ["euphoric electronic music", "extreme hype music", "epic pump up songs"],
    "happy":      ["happy pop songs", "feel good music", "cheerful upbeat songs"],
    "romantic":   ["romantic love songs", "soft romantic music", "love ballads"],
    "motivated":  ["motivational workout music", "epic motivation songs", "pump up music"],
    "calm":       ["calm relaxing music", "peaceful ambient music", "soft chill music"],
    "nostalgic":  ["nostalgic 90s music", "throwback classics", "retro oldies music"],
    "focused":    ["lofi hip hop study", "deep focus music", "instrumental study beats"],
    "anxious":    ["calming anxiety music", "peaceful meditation music", "stress relief music"],
    "angry":      ["intense rock music", "aggressive workout music", "heavy metal energy"],
    "heartbreak": ["heartbreak sad songs", "breakup emotional music", "sad love songs"],
    "lonely":     ["lonely sad music", "emotional acoustic songs", "melancholy music"],
    "melancholy": ["melancholy sad music", "emotional piano music", "sad indie songs"],
}

MOOD_KEYWORDS = {
    "ecstatic": [
        "ecstatic", "incredible", "best day", "on top of the world",
        "pumped", "euphoric", "over the moon", "unstoppable", "electric"
    ],
    "happy": [
        "happy", "great", "wonderful", "joyful", "good mood", "cheerful",
        "pleased", "glad", "delighted", "feel good", "feeling good"
    ],
    "romantic": [
        "love", "romantic", "crush", "miss you", "in love", "valentine",
        "sweetheart", "darling", "affectionate", "tender"
    ],
    "motivated": [
        "motivated", "grind", "hustle", "goals", "determined", "unstoppable",
        "driven", "ambitious", "lets go", "let's go", "i can do this"
    ],
    "calm": [
        "calm", "peaceful", "relax", "chill", "serene", "tranquil",
        "at ease", "comfortable", "content", "mellow", "quiet"
    ],
    "nostalgic": [
        "nostalgic", "remember", "old times", "miss those days",
        "childhood", "memories", "back then", "used to", "throwback"
    ],
    "focused": [
        "focus", "study", "work", "concentrate", "coding", "homework",
        "productive", "lofi", "working", "studying", "deep work"
    ],
    "anxious": [
        "anxious", "nervous", "worried", "scared", "stressed", "panic",
        "overthinking", "cant sleep", "can't sleep", "restless", "uneasy"
    ],
    "angry": [
        "angry", "furious", "rage", "mad", "frustrated", "irritated",
        "annoyed", "pissed", "livid", "hate", "infuriated"
    ],
    "heartbreak": [
        "heartbreak", "breakup", "broke up", "left me", "cheated",
        "she left", "he left", "dumped", "rejected", "devastated",
        "cant stop crying", "can't stop crying", "broken heart"
    ],
    "lonely": [
        "lonely", "alone", "no one", "isolated", "empty",
        "nobody cares", "left out", "forgotten", "abandoned"
    ],
    "melancholy": [
        "sad", "depressed", "down", "blue", "unhappy", "miserable",
        "cry", "crying", "upset", "hurt", "pain", "grief", "sorrow",
        "feel bad", "feeling bad", "not okay", "not good"
    ],
}

MOOD_MESSAGES = {
    "ecstatic":   "You're on top of the world! Here's something to match:",
    "happy":      "Love the good vibes! Here's something cheerful:",
    "romantic":   "Feeling the love? Here's something tender:",
    "motivated":  "Let's go! Here's something to fuel that drive:",
    "calm":       "Staying calm. Here's something peaceful:",
    "nostalgic":  "Taking a trip down memory lane:",
    "focused":    "In the zone! Here's something to keep you there:",
    "anxious":    "Take a breath. Here's something to ease your mind:",
    "angry":      "Let it out. Here's something intense:",
    "heartbreak": "Going through it is tough. Here's music that gets it:",
    "lonely":     "You're not alone. Here's something that understands:",
    "melancholy": "I feel you. Here's something that understands:",
}

MOOD_INTENSITY = {
    "ecstatic":   10,
    "angry":      9,
    "motivated":  8,
    "heartbreak": 8,
    "happy":      7,
    "anxious":    7,
    "romantic":   6,
    "lonely":     6,
    "melancholy": 5,
    "nostalgic":  5,
    "focused":    4,
    "calm":       3,
}

class MusicEngine:
    def __init__(self):
        self.is_playing  = False
        self.current_url = None
        self.played = set()

        self.ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
        }

        logger.info("[MUSIC] MusicEngine initialized with yt-dlp!")

    def analyze_mood(self, text):
        text = text.lower().strip()

        scores = {}
        for mood, keywords in MOOD_KEYWORDS.items():
            score = 0
            for kw in keywords:
                if kw in text:
                    score += len(kw.split())
            if score > 0:
                scores[mood] = score

        if scores:
            best_mood = max(scores, key=scores.get)
            intensity = MOOD_INTENSITY.get(best_mood, 5)

            boosters = ["very", "so", "really", "extremely", "completely", "totally", "absolutely"]
            if any(b in text for b in boosters):
                intensity = min(intensity + 2, 10)

            return best_mood, intensity

        return "calm", 5

    def search_youtube(self, mood, intensity):
        queries = MOOD_QUERIES.get(mood, ["chill music"])

        query = random.choice(queries)

        offset = random.randint(1, 8)
        search_query = f"ytsearch{offset}:{query}"

        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info    = ydl.extract_info(search_query, download=False)
                entries = info.get("entries", [])

                if not entries:
                    return None

                fresh = [e for e in entries if e.get("id") not in self.played]

                if not fresh:
                    self.played.clear()
                    fresh = entries

                entry = random.choice(fresh)

                self.played.add(entry.get("id"))

                return {
                    "title":    entry.get("title", "Unknown"),
                    "uploader": entry.get("uploader", "Unknown"),
                    "url":      entry.get("url") or entry.get("webpage_url"),
                    "duration": entry.get("duration", 0),
                    "id":       entry.get("id")
                }

        except Exception as e:
            logger.error(f"[MUSIC] YouTube search failed: {e}")
            return None

    def play_audio(self, url):
        try:
            self.is_playing  = True
            self.current_url = url

            if os.name == "nt":
                os.startfile(url)
            else:
                subprocess.Popen(["xdg-open", url])

            self.is_playing = False

        except Exception as e:
            logger.error(f"[MUSIC] Playback failed: {e}")
            self.is_playing = False

    def play_async(self, url):
        thread = threading.Thread(target=self.play_audio, args=(url,))
        thread.daemon = True
        thread.start()

    def process(self, text):
        mood, intensity = self.analyze_mood(text)

        print(f"\n   [Mood Detected] {mood.upper()} — intensity {intensity}/10\n")
        print(f"   [Searching YouTube...]\n")

        message = MOOD_MESSAGES.get(mood, "Here's some music for you:")

        track = self.search_youtube(mood, intensity)

        if not track:
            return self.fallback_response(mood, message)

        if track.get("url"):
            self.play_async(track["url"])

        title = track.get("title",    "Unknown")
        uploader = track.get("uploader", "Unknown")
        duration = track.get("duration", 0)
        mins = duration // 60
        secs = duration  % 60

        response_text = (
            f"{message}\n\n"
            f"  🎵 {title}\n"
            f"  👤 {uploader}\n"
            f"  🎭 Mood      : {mood.capitalize()}\n"
            f"  ⚡ Intensity : {intensity}/10\n"
            f"  ⏱️  Duration  : {mins}:{secs:02d}\n"
        )

        return {
            "type": "music",
            "data": {
                "mood":      mood,
                "intensity": intensity,
                "track":     track,
                "text":      response_text
            }
        }

    def fallback_response(self, mood, message):
        fallback = {
            "ecstatic":   "Can't Stop the Feeling - Justin Timberlake",
            "happy":      "Happy - Pharrell Williams",
            "romantic":   "Perfect - Ed Sheeran",
            "motivated":  "Eye of the Tiger - Survivor",
            "calm":       "Weightless - Marconi Union",
            "nostalgic":  "Yesterday - The Beatles",
            "focused":    "Lo-Fi Hip Hop - ChillHop",
            "anxious":    "Breathe - Pink Floyd",
            "angry":      "Killing in the Name - RATM",
            "heartbreak": "Someone Like You - Adele",
            "lonely":     "Sound of Silence - Simon & Garfunkel",
            "melancholy": "The Night - Zack Hemsey",
        }

        track_name = fallback.get(mood, "Chill Music")

        return {
            "type": "music",
            "data": {
                "text": (
                    f"{message}\n\n"
                    f"  🎵 {track_name}\n"
                    f"  🎭 Mood: {mood.capitalize()}\n"
                )
            }
        }