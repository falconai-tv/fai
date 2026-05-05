import os
import hashlib
import threading

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    from gtts import gTTS
except ImportError:
    gTTS = None

VOICE_CACHE_DIR = "data/voice_cache"
DEFAULT_LANG = "en"
DEFAULT_SPEED = 180

def init_cache():
    if not os.path.exists(VOICE_CACHE_DIR):
        os.makedirs(VOICE_CACHE_DIR)

def text_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def get_cache_path(text):
    h = text_hash(text)
    return os.path.join(VOICE_CACHE_DIR, f"{h}.mp3")

def detect_tone(text):
    text = text.lower()

    if any(w in text for w in ["sad", "trisht", "keq", "depressed"]):
        return "calm"

    if any(w in text for w in ["lajm", "news", "breaking"]):
        return "serious"

    if any(w in text for w in ["music", "këng", "song"]):
        return "energetic"

    return "neutral"

def generate_offline(text, speed=DEFAULT_SPEED):
    if not pyttsx3:
        return None

    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', speed)

        path = get_cache_path(text)
        engine.save_to_file(text, path)
        engine.runAndWait()

        return path
    except Exception:
        return None

def generate_online(text, lang=DEFAULT_LANG):
    if not gTTS:
        return None

    try:
        path = get_cache_path(text)
        tts = gTTS(text=text, lang=lang)
        tts.save(path)
        return path
    except Exception:
        return None

def generate_voice(text, lang=DEFAULT_LANG):
    init_cache()

    path = get_cache_path(text)

    if os.path.exists(path):
        return path

    tone = detect_tone(text)

    speed_map = {
        "calm": 150,
        "serious": 170,
        "energetic": 200,
        "neutral": DEFAULT_SPEED
    }

    speed = speed_map.get(tone, DEFAULT_SPEED)

    audio_path = generate_offline(text, speed=speed)

    if audio_path:
        return audio_path

    audio_path = generate_online(text, lang=lang)

    return audio_path

def generate_voice_async(text, callback=None):
    def run():
        path = generate_voice(text)
        if callback:
            callback(path)

    thread = threading.Thread(target=run)
    thread.start()

def play_audio(path):
    try:
        if os.name == "nt":
            os.startfile(path)
        else:
            os.system(f"mpg123 {path}")
    except Exception:
        pass

def speak(text, async_mode=True):
    if async_mode:
        generate_voice_async(text, callback=play_audio)
    else:
        path = generate_voice(text)
        if path:
            play_audio(path)

    return True