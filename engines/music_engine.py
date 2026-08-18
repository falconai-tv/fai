import os
import sys
import subprocess
import threading
import urllib.request
from ytmusicapi import YTMusic

try:
    from lyricsgenius import Genius
    GENIUS_AVAILABLE = True
except ImportError:
    GENIUS_AVAILABLE = False

try:
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3, TIT2, TPE1, APIC, USLT
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False

class MusicEngine:
    def __init__(self):
        try:
            self.ytmusic = YTMusic()
        except Exception:
            self.ytmusic = None
            
        self.genius_token = None 
        if GENIUS_AVAILABLE:
            try:
                self.genius = Genius(self.genius_token, verbose=False, remove_section_headers=True)
            except Exception:
                self.genius = None
        else:
            self.genius = None

        self.download_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "downloads")
        os.makedirs(self.download_dir, exist_ok=True)

        self.ffmpeg_path = "C:\\ffmpeg\\bin" if os.name == 'nt' else ""

    def embed_metadata(self, mp3_path: str, title: str, artist: str, image_path: str, lyrics: str = None):
        if not MUTAGEN_AVAILABLE:
            return
        try:
            audio = MP3(mp3_path, ID3=ID3)
            try:
                audio.add_tags()
            except Exception:
                pass

            if title:
                audio.tags.add(TIT2(encoding=3, text=title))
            if artist:
                audio.tags.add(TPE1(encoding=3, text=artist))

            if image_path and os.path.exists(image_path):
                with open(image_path, 'rb') as img:
                    audio.tags.add(
                        APIC(
                            encoding=3,
                            mime='image/jpeg',
                            type=3,
                            desc='Cover',
                            data=img.read()
                        )
                    )
            
            if lyrics:
                audio.tags.add(USLT(encoding=3, lang='eng', desc='Lyrics', text=lyrics))

            audio.save()
        except Exception as e:
            print(f"[Metadata Error]: {e}")

    def search_and_download(self, query: str):
        try:
            search_query = query.lower()
            for trig in ["play", "këngë", "song", "music", "lësho"]:
                search_query = search_query.replace(trig, "")
            search_query = search_query.strip()

            if not search_query:
                search_query = query

            song_title = search_query
            song_artist = ""
            lyrics_text = None

            if self.genius:
                try:
                    print(f"\n[FalconAI Genius Engine]: Duke kërkuar tekstin/frazën te Genius...")
                    songs_search = self.genius.search_songs(search_query, per_page=1)
                    if songs_search and 'songs' in songs_search and len(songs_search['songs']) > 0:
                        top_hit = songs_search['songs'][0]
                        song_title = top_hit.get('title', search_query)
                        song_artist = top_hit.get('primary_artist', {}).get('name', '')
                        print(f"[FalconAI Genius Engine]: U gjet -> {song_artist} - {song_title}")

                        lyrics_text = self.genius.search_lyrics(search_query)
                except Exception as g_err:
                    print(f"[Genius Search Warning]: {g_err}")

            yt_search_query = f"{song_artist} - {song_title}" if song_artist else search_query

            video_url = None
            thumbnail_url = None
            
            if self.ytmusic:
                try:
                    results = self.ytmusic.search(yt_search_query, filter="songs")
                    if not results:
                        results = self.ytmusic.search(yt_search_query)

                    if results and len(results) > 0:
                        top_result = results[0]
                        video_id = top_result.get('videoId')
                        if video_id:
                            video_url = f"https://www.youtube.com/watch?v={video_id}"

                        song_title = top_result.get('title', song_title)
                        artists = top_result.get('artists', [])
                        if artists and not song_artist:
                            song_artist = artists[0].get('name', '')

                        thumbnails = top_result.get('thumbnails', [])
                        if thumbnails:
                            thumbnail_url = thumbnails[-1].get('url')
                            if thumbnail_url and "=" in thumbnail_url:
                                thumbnail_url = thumbnail_url.split("=")[0] + "=w1000-h1000-l90-rj"
                except Exception as e:
                    print(f"[YTMusic Search Warning]: {e}")

            if not video_url:
                video_url = f"ytsearch1:{yt_search_query}"

            existing_files = os.listdir(self.download_dir)
            clean_song_title = "".join(c for c in song_title.lower() if c.isalnum() or c.isspace()).strip()
            clean_artist = "".join(c for c in song_artist.lower() if c.isalnum() or c.isspace()).strip()

            for file in existing_files:
                if file.endswith(".mp3"):
                    file_lower = file.lower()
                    clean_file_name = "".join(c for c in file_lower if c.isalnum() or c.isspace()).strip()
                    
                    title_match = clean_song_title in clean_file_name and len(clean_song_title) > 2
                    artist_match = clean_artist in clean_file_name if clean_artist else True

                    if title_match and artist_match:
                        local_file_path = os.path.join(self.download_dir, file)
                        print(f"\n[FalconAI Offline Engine]: Kënga u gjet në cache-in lokal!")
                        filename = os.path.basename(local_file_path)
                        print(f"[Stream Link]: http://127.0.0.1:8080/downloads/{filename}\n")
                        self.play_audio(local_file_path)
                        return

            output_template = os.path.join(self.download_dir, "%(title)s.%(ext)s")

            ydl_opts = [
                "yt-dlp",
                "--extractor-args", "youtube:player_client=android",
                "-x", "--audio-format", "mp3",
                "-o", output_template,
                "--print", "after_move:filepath",
                "--no-update",
                video_url
            ]
            
            if self.ffmpeg_path and os.path.exists(self.ffmpeg_path):
                ydl_opts[1:1] = ["--ffmpeg-location", self.ffmpeg_path]

            process = subprocess.Popen(ydl_opts, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                lines = stdout.strip().split("\n")
                file_path = lines[-1].strip() if lines else None

                if file_path and os.path.exists(file_path):
                    base_name = os.path.splitext(file_path)[0]
                    
                    image_path = None
                    if thumbnail_url:
                        try:
                            image_path = f"{base_name}.jpg"
                            req = urllib.request.Request(thumbnail_url, headers={'User-Agent': 'Mozilla/5.0'})
                            with urllib.request.urlopen(req) as response:
                                with open(image_path, 'wb') as img_file:
                                    img_file.write(response.read())
                        except Exception:
                            pass

                    if lyrics_text:
                        try:
                            txt_path = f"{base_name}_lyrics.txt"
                            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                                txt_file.write(lyrics_text)
                        except Exception:
                            pass

                    self.embed_metadata(file_path, song_title, song_artist if song_artist else "FalconAI", image_path, lyrics_text)

                    print(f"\n[FalconAI Music Engine]: Kënga u shkarkua dhe u optimizua plotësisht.")
                    if video_url and "youtube.com/watch" in video_url:
                        print(f"[YouTube Link]: {video_url}")

                    filename = os.path.basename(file_path)
                    print(f"[Stream Link]: http://127.0.0.1:8080/downloads/{filename}\n")
                    
                    self.play_audio(file_path)
                else:
                    print(f"\n[MusicEngine]: Skedari u shkarkua por path-i nuk u gjet saktë.")
            else:
                print(f"\n[MusicEngine Error]: {stderr}")

        except Exception as e:
            print(f"\n[MusicEngine Exception]: {e}")

    def play_audio(self, file_path: str):
        try:
            print(f"\n[Duke u luajtur]: {file_path}")
            if os.name == 'nt':
                os.startfile(file_path)
            elif sys.platform == 'darwin':
                subprocess.Popen(['afplay', file_path])
            else:
                subprocess.Popen(['xdg-open', file_path])
        except Exception as e:
            print(f"[Audio Player Error]: {e}")

    def play(self, query: str) -> dict:
        thread = threading.Thread(target=self.search_and_download, args=(query,))
        thread.daemon = True
        thread.start()

        return {
            "text": f"Duke analizuar tekstin/frazën për: {query}...",
            "voice": "Analyzing lyrics and searching music.",
            "meta": {"type": "music", "intent": "play_music"}
        }
