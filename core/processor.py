import random

AI_INTROS = ["Here's what I found for you.:", "This is what I could find.:", "I think this might interest you.:", "This seems relevant to your request.:"]

LOW_CONF_WARNINGS = ["I'm not 100% sure, but here's the closest result:", "It may not be perfect, but this is the best I found:","This is a lower-reliability answer.:"]

NOT_FOUND_MESSAGES = ["I didn't find anything specific about this request.", "I couldn't find an accurate result.", "Try rewording the request."]

def format_channel(data):
    if not data:
        return "No channels found."

    if not data.get("found"):
        suggestions = data.get("suggestions", [])

        text = "I couldn't find the correct channel.\n"

        if suggestions:
            text += "\n Suggestions:\n"
            for s in suggestions[:3]:
                text += f"- {s['name']}\n"

        return text

    name = data.get("channel")
    confidence = data.get("confidence", 0)

    text = f"I am showing you: {name}"

    if confidence < 0.6:
        text = random.choice(LOW_CONF_WARNINGS) + "\n" + text

    return text

def format_web(data):
    if not data or data.get("status") != "ok":
        return random.choice(NOT_FOUND_MESSAGES)

    title = data.get("title", "")
    summary = data.get("summary", "")
    confidence = data.get("confidence", 0)

    intro = random.choice(AI_INTROS)

    text = f"{intro}\n\n"
    text += f"{title}\n\n"
    text += f"{summary}"

    if confidence < 0.5:
        text = random.choice(LOW_CONF_WARNINGS) + "\n\n" + text

    return text

def format_music(data):
    if not data:
        return "I couldn't find music for this request."

    text = "I'm suggesting something for you.:\n"

    if isinstance(data, list):
        for track in data[:3]:
            text += f"- {track}\n"
    else:
        text += str(data)

    return text

def clean_for_voice(text):
    replacements = {
        "📺": "",
        "📰": "",
        "🎵": "",
        "👉": "",
        "❌": ""
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text.strip()

def process_response(result: dict):
    if not isinstance(result, dict):
        return {
            "text": str(result),
            "voice": str(result),
            "meta": {}
        }

    r_type = result.get("type")
    
    if r_type == "channel":
        text = format_channel(result.get("data"))

    elif r_type == "web":
        text = format_web(result.get("data"))

    elif r_type == "music":
        text = format_music(result.get("data"))

    else:
        text = result.get("message", random.choice(NOT_FOUND_MESSAGES))

    voice_text = clean_for_voice(text)

    return {
        "text": text,
        "voice": voice_text,
        "meta": {
            "type": r_type
        }
    }