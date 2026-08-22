import os
import subprocess
from ytmusicapi import YTMusic

try:
    from core.logger_config import setup_logger
    logger = setup_logger("FalconAI.MusicEngine")
except Exception:
    import logging
    logger = logging.getLogger("FalconAI.MusicEngine")
    logging.basicConfig(level=logging.INFO)


class MusicEngine:
    def __init__(self):
        try:
            self.ytmusic = YTMusic()
            logger.info("[MusicEngine] YTMusic initialized successfully")
        except Exception as e:
            logger.error(f"[MusicEngine] YTMusic init failed: {e}")
            self.ytmusic = None

    def get_stream_url(self, query: str):
        try:
            if self.ytmusic is None:
                logger.error("[MusicEngine] get_stream_url aborted: ytmusic is None (init failed earlier)")
                return None, None

            search_query = query.lower()
            for trig in ["play", "këngë", "song", "music", "lësho"]:
                search_query = search_query.replace(trig, "")
            search_query = search_query.strip()

            logger.info(f"[MusicEngine] Original query: '{query}' -> Cleaned: '{search_query}'")

            if not search_query:
                logger.error("[MusicEngine] Cleaned search query is empty after removing trigger words")
                return None, None

            # --- Search attempt 1: songs filter ---
            try:
                results = self.ytmusic.search(search_query, filter="songs")
            except Exception as search_err:
                logger.error(f"[MusicEngine] ytmusic.search (songs filter) raised: {search_err}")
                results = None

            if not results:
                logger.info("[MusicEngine] No results with filter='songs', retrying without filter")
                try:
                    results = self.ytmusic.search(search_query)
                except Exception as search_err:
                    logger.error(f"[MusicEngine] ytmusic.search (no filter) raised: {search_err}")
                    results = None

            if not results:
                logger.error(f"[MusicEngine] No search results at all for query: '{search_query}'")
                return None, None

            top_result = results[0]
            video_id = top_result.get('videoId')
            video_title = top_result.get('title', 'Unknown Title')

            if not video_id:
                logger.error(f"[MusicEngine] Top result has no videoId: {top_result}")
                return None, None

            logger.info(f"[MusicEngine] Top result: '{video_title}' (videoId={video_id})")

            video_url = f"https://www.youtube.com/watch?v={video_id}"
            cmd = ["yt-dlp", "-g", "-f", "bestaudio", video_url]

            logger.info(f"[MusicEngine] Running: {' '.join(cmd)}")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=30)

            if process.returncode == 0 and stdout.strip():
                stream_url = stdout.strip()
                logger.info(f"[MusicEngine] yt-dlp succeeded, stream URL obtained (len={len(stream_url)})")
                return stream_url, video_title
            else:
                logger.error(
                    f"[MusicEngine] yt-dlp failed (returncode={process.returncode}). "
                    f"stderr: {stderr.strip()[:500]}"
                )
                return None, None

        except subprocess.TimeoutExpired:
            logger.error("[MusicEngine] yt-dlp timed out after 30s")
            try:
                process.kill()
            except Exception:
                pass
            return None, None
        except Exception as e:
            logger.error(f"[MusicEngine] Unexpected exception in get_stream_url: {e}")
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
