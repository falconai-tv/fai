from dataclasses import dataclass
from typing import List, Optional


# -------------------------
# CHANNEL MODEL
# -------------------------
@dataclass
class Channel:
    name: str
    url: str
    category: str = "general"
    language: str = "multi"
    country: str = "global"
    tags: Optional[List[str]] = None
    is_live: bool = True


# -------------------------
# CHANNEL DATABASE
# -------------------------
CHANNELS = [
    Channel(
        name="DW News",
        url="https://dwamdstream102.akamaized.net/hls/live/2015525/dwstream102/master.m3u8",
        category="news",
        language="en",
        country="germany",
        tags=["world", "politics", "europe", "germany"]
    ),
    Channel(
        name="TRT World",
        url="https://tv-trtworld.medya.trt.com.tr/master.m3u8",
        category="news",
        language="en",
        country="turkey",
        tags=["world", "middle east", "politics"]
    ),
    Channel(
        name="Africa News",
        url="https://euronews-africanews-1-us.samsung.wurl.com/manifest/playlist.m3u8",
        category="news",
        language="en",
        country="france",
        tags=["africa", "world", "news"]
    ),
    Channel(
        name="NASA TV",
        url="https://ntvpublic-v2.akamaized.net/hls/live/2028660/NTV-Public-V2/master.m3u8",
        category="entertainment",
        language="en",
        country="usa",
        tags=["space", "science", "education"]
    )
]


# -------------------------
# GET CHANNEL BY EXACT NAME
# -------------------------
def get_channel(name: str):
    name = name.strip().lower()

    for ch in CHANNELS:
        if ch.name.lower() == name:
            return {
                "name": ch.name,
                "url": ch.url,
                "category": ch.category,
                "language": ch.language,
                "country": ch.country,
                "tags": ch.tags,
                "is_live": ch.is_live
            }

    return None


# -------------------------
# CATEGORY FILTER
# -------------------------
def get_channels_by_category(category: str):
    category = category.lower()
    return [
        {
            "name": ch.name,
            "url": ch.url,
            "category": ch.category,
            "language": ch.language,
            "country": ch.country,
            "tags": ch.tags,
            "is_live": ch.is_live
        }
        for ch in CHANNELS
        if ch.category == category
    ]


# -------------------------
# TAG SEARCH
# -------------------------
def search_channels_by_tag(keyword: str):
    keyword = keyword.lower()

    return [
        {
            "name": ch.name,
            "url": ch.url,
            "category": ch.category,
            "language": ch.language,
            "country": ch.country,
            "tags": ch.tags,
            "is_live": ch.is_live
        }
        for ch in CHANNELS
        if ch.tags and any(keyword in tag for tag in ch.tags)
    ]


# -------------------------
# NEWS CHANNELS
# -------------------------
def get_news_channels():
    return get_channels_by_category("news")


# -------------------------
# FUTURE EXTENSION (BALKAN)
# -------------------------
def get_balkan_channels():
    return [
        {
            "name": ch.name,
            "url": ch.url,
            "category": ch.category,
            "language": ch.language,
            "country": ch.country,
            "tags": ch.tags,
            "is_live": ch.is_live
        }
        for ch in CHANNELS
        if ch.tags and "balkan" in ch.tags
    ]


# -------------------------
# BEST MATCH (SEMANTIC LIGHTWEIGHT)
# -------------------------
def find_best_channel(query: str):
    query = query.lower().strip()

    best = None
    best_score = 0

    for ch in CHANNELS:
        score = 0
        name = ch.name.lower()

        # exact name match
        if query == name:
            score += 10
        elif query in name:
            score += 5

        # category match
        if ch.category in query:
            score += 2

        # tag match
        if ch.tags:
            for tag in ch.tags:
                if tag in query:
                    score += 3

        if score > best_score:
            best_score = score
            best = ch

    if not best:
        return None

    return {
        "name": best.name,
        "url": best.url,
        "category": best.category,
        "language": best.language,
        "country": best.country,
        "tags": best.tags,
        "is_live": best.is_live
    }
