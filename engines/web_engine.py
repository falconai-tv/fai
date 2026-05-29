import re
import requests
import xml.etree.ElementTree as ET
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("FalconAI.WebEngine")

class WebEngine:
    def __init__(self):
        self.timeout = 5

        self.feeds = {
            "world": [
                "https://feeds.bbci.co.uk/news/world/rss.xml",
                "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
            ],
            "politics": [
                "https://feeds.bbci.co.uk/news/politics/rss.xml",
                "https://rss.politico.com/politics-news.xml"
            ],
            "business": [
                "https://feeds.bbci.co.uk/news/business/rss.xml",
                "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml"
            ],
            "technology": [
                "https://feeds.bbci.co.uk/news/technology/rss.xml",
                "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
                "https://feeds.feedburner.com/TechCrunch",
                "https://www.theverge.com/rss/index.xml"
            ],
            "balkan": [
                "https://feeds.bbci.co.uk/news/world/europe/rss.xml",
                "https://www.trtworld.com/rss",
                "https://exit.al/feed/"
            ],
            "sports": ["https://feeds.bbci.co.uk/sport/rss.xml"],
            "general": ["https://feeds.bbci.co.uk/news/rss.xml"]
        }

        self.movie_platforms = {
            "tubi": "https://tubitv.com/search/",
            "pluto": "https://pluto.tv/en/search/details/movies/",
            "crackle": "https://www.crackle.com/search/",
            "rakuten": "https://www.rakuten.tv/it/search?q="
        }

        self.intent_category = {
            "watch_news": "world",
            "watch_balkan_news": "balkan",
            "tech_news": "technology",
            "sports_news": "sports",
            "business_news": "business",
            "general_search": "general"
        }

    def process(self, text: str, intent: str = None, category: str = None):
        try:
            if intent == "watch_movie" or any(word in text.lower() for word in ["play movie", "shiko filmin", "search movie"]):
                return self.handle_movie_intent(text)

            return self.run_news_engine(text, intent, category)

        except Exception as e:
            logger.error(f"[WEB ERROR] {str(e)}")
            return self.error_response()

    def handle_movie_intent(self, query):
        movie_name = re.sub(
            r'\b(play|watch|shiko|movie|film|search|find|me gjej)\b',
            '',
            query,
            flags=re.I
        ).strip()

        platform = "tubi"

        search_url = (
            f"https://tubitv.com/search/"
            f"{movie_name.replace(' ', '%20')}"
        )

        logger.info(
            f"[MOVIE SEARCH] Searching movie: {movie_name}"
        )

        try:

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(
                search_url,
                headers=headers,
                timeout=8
            )

            html = response.text

            movie_match = re.search(
                r'"/movies/(\d+)/([^"]+)"',
                html
            )

            if movie_match:

                movie_id = movie_match.group(1)
                movie_slug = movie_match.group(2)

                direct_url = (
                    f"https://tubitv.com/movies/"
                    f"{movie_id}/{movie_slug}"
                )

                logger.info(
                    f"[MOVIE FOUND] {direct_url}"
                )

                return {
                    "type": "web_movie",
                    "data": {
                        "query": movie_name,
                        "platform": platform,
                        "stream_url": direct_url,
                        "auto_play": True,
                        "fullscreen": True,
                        "falcon_ai":
                            f"Playing {movie_name} now."
                    }
                }

            logger.warning(
                f"[MOVIE NOT FOUND] {movie_name}"
            )

            return {
                "type": "web",
                "data": {
                    "text":
                        f"I couldn't find {movie_name}."
                }
            }

        except Exception as e:

            logger.error(
                f"[MOVIE ERROR] {str(e)}"
            )

            return self.error_response()
    
    def run_news_engine(self, query, intent=None, category=None):
        if category is None:
            category = self.intent_category.get(intent, "general")

        logger.info(f"[WEB NEWS] Category: {category}")

        keywords = self.extract_keywords(query)
        articles = self.fetch_articles(category)
        filtered = self.filter_articles(articles, keywords)

        if not filtered:
            return self.fallback_response(query)

        return self.format_response(filtered[:3], query)

    def fetch_articles(self, category):
        articles = []
        feeds = self.feeds.get(category, self.feeds["general"])

        for url in feeds:
            try:
                response = requests.get(url, timeout=self.timeout)
                if response.status_code != 200: continue
                root = ET.fromstring(response.content)

                for item in root.findall(".//item"):
                    title = item.findtext("title", "")
                    link  = item.findtext("link", "")
                    desc  = item.findtext("description", "")
                    if title and link:
                        articles.append({"title": title, "link": link, "description": desc})
            except: continue
        return articles

    def fetch_full_article(self, url):
        try:
            response = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code != 200: return ""
            
            soup = BeautifulSoup(response.content, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()

            article_body = soup.find("article") or soup.find("div", class_=re.compile(r"article|content|body", re.I))
            target = article_body if article_body else soup
            paragraphs = target.find_all("p")
            texts = [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 45]
            
            full_text = " ".join(texts)
            return full_text[:1500].strip() if len(full_text) > 1500 else full_text.strip()
        except: return ""

    def extract_keywords(self, text):
        stopwords = {"what", "happened", "in", "the", "is", "now", "tell", "about", "latest", "news"}
        return [w for w in text.lower().split() if w not in stopwords and len(w) > 2]

    def filter_articles(self, articles, keywords):
        if not keywords: return articles[:3]
        scored = []
        for art in articles:
            text = (art["title"] + " " + art.get("description", "")).lower()
            score = sum(1 for kw in keywords if kw in text)
            if score > 0: scored.append((score, art))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [a[1] for a in scored]

    def format_response(self, articles, query):
        voice_parts = [f"Here's the latest on {query}."]
        for i, art in enumerate(articles, 1):
            full_text = self.fetch_full_article(art['link'])
            desc = full_text if full_text else art.get('description', '')
            voice_parts.append(f"Article {i}. {art['title']}. {desc[:300]}")

        return {
            "type": "web",
            "data": {
                "query": query,
                "articles": articles,
                "voice_text": " ".join(voice_parts)
            }
        }

    def error_response(self):
        return {"type": "error", "data": {"text": "I encountered an issue accessing the web."}}

    def fallback_response(self, query):
        return {"type": "web", "data": {"query": query, "articles": [], "text": "No specific news found."}}
