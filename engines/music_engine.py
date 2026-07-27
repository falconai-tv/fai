import logging
import random
from ytmusicapi import YTMusic

logger = logging.getLogger("FalconAI.MusicEngine")

class MusicEngine:
    def __init__(self):
        try:
            self.ytm = YTMusic()
            self.played = set()
            logger.info("--- YouTube Music Engine Initialized ---")
        except Exception as e:
            logger.error(f"Failed to initialize YTMusic: {e}")
            self.ytm = None

    def analyze_mood(self, text):
        text = text.lower()
        if any(w in text for w in ["sad", "cry", "depressed", "lonely", "heartbreak"]):
            return "sad", 3
        elif any(w in text for w in ["happy", "party", "dance", "celebrate", "excited"]):
            return "happy", 8
        elif any(w in text for w in ["focus", "study", "coding", "concentrate", "work"]):
            return "focus", 5
        return "neutral", 6

    def search_ytmusic(self, query_text):
        if not self.ytm:
            return None
            
        try:
            results = self.ytm.search(query_text, filter="songs", limit=10)
            if not results:
                results = self.ytm.search("pop hits", filter="songs", limit=10)
            
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
        
        track = self.search_ytmusic(text)
        
        message = f"Found this for '{text}':"
        if not track:
            return {
                "type": "music",
                "data": {
                    "text": f"{message}\n\n 🎵 Chill Music\n 🎭 Query: {text}"
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
