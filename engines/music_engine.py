import os
import subprocess
from ytmusicapi import YTMusic

class MusicEngine:
    def __init__(self):
        try:
            self.ytmusic = YTMusic()
        except Exception:
            self.ytmusic = None

    def get_stream_url(self, query: str):
        try:
            search_query = query.lower()
            for trig in ["play", "këngë", "song", "music", "lësho"]:
                search_query = search_query.replace(trig, "")
            search_query = search_query.strip()

            results = self.ytmusic.search(search_query, filter="songs")
            if not results:
                results = self.ytmusic.search(search_query)
            
            if not results:
                return None, None
                
            top_result = results[0]
            video_id = top_result.get('videoId')
            video_title = top_result.get('title', 'Unknown Title')
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            cmd = ["yt-dlp", "-g", "-f", "bestaudio", video_url]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                stream_url = stdout.strip()
                return stream_url, video_title
            else:
                return None, None

        except Exception as e:
            return None, None

    def play(self, query: str) -> dict:
        stream_url, title = self.get_stream_url(query)
        
        if stream_url:
            return {
                "text": f"Now playing: {title}",
                "audio_url": stream_url,
                "meta": {
                    "type": "music", 
                    "intent": "play_music",
                    "title": title
                }
            }
        else:
            return {
                "text": "Sorry, I could not generate the link for this track.",
                "meta": {"type": "error"}
            }
