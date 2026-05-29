import re
import requests
import xml.etree.ElementTree as ET
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("FalconAI.WebEngine")

class WebEngine:
    def __init__(self):
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
                "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
                "https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines"
                "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml"
            ],
            "technology": [
                "https://feeds.bbci.co.uk/news/technology/rss.xml",
                "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
                "https://feeds.feedburner.com/TechCrunch",
                "https://www.theverge.com/rss/index.xml"
            ],
            "war": [
                "https://feeds.bbci.co.uk/news/world/rss.xml",
                "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
            ],
            "balkan": [
                "https://feeds.bbci.co.uk/news/world/europe/rss.xml",
                "https://www.trtworld.com/rss",
                "https://exit.al/feed/"
            ],
            "sports": [
                "https://feeds.bbci.co.uk/sport/rss.xml"
            ],
            "health": [
                "https://feeds.bbci.co.uk/news/health/rss.xml"
            ],
            "general": [
                "https://feeds.bbci.co.uk/news/rss.xml"
            ]
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
            "watch_news":        "world",
            "watch_war":         "war",
            "watch_news": "world",
            "watch_balkan_news": "balkan",
            "tech_news":         "technology",
            "sports_news":       "sports",
            "business_news":     "business",
            "person_search":     "world",
            "weather_query":     "general",
            "general_search":    "general"
            "tech_news": "technology",
            "sports_news": "sports",
            "business_news": "business",
            "general_search": "general"
        }

    def run(self, query, intent=None, category=None):
    def process(self, text: str, intent: str = None, category: str = None):
        try:
            if category is None:
                category = self.intent_category.get(intent, "general")

            logger.info(f"[WEB] Query: {query} | Intent: {intent} | Category: {category}")
            if intent == "watch_movie" or any(word in text.lower() for word in ["play movie", "shiko filmin", "search movie"]):
                return self.handle_movie_intent(text)

            keywords = self.extract_keywords(query)
            articles = self.fetch_articles(category)
            filtered = self.filter_articles(articles, keywords)

            if not filtered:
                return self.fallback_response(query)

            return self.format_response(filtered[:3], query)
            return self.run_news_engine(text, intent, category)

        except Exception as e:
            logger.error(f"[WEB ERROR] {str(e)}")
            return self.error_response()

    def handle_movie_intent(self, query):
        movie_name = re.sub(r'\b(play|watch|shiko|movie|film|search|find|me gjej)\b', '', query, flags=re.I).strip()

        platform = "tubi"
        base_url = self.movie_platforms[platform]

        search_url = f"{base_url}{movie_name.replace(' ', '%20')}"

        logger.info(f"[VOD] Routing '{movie_name}' to {platform.upper()}")

        return {
            "type": "web_movie",
            "data": {
                "query": movie_name,
                "platform": platform,
                "stream_url": search_url,
                "auto_play": True,
                "falcon_ai": f"I'm opening {movie_name} on {platform.capitalize()}. Sit back and enjoy!"
            }
        }

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
                if response.status_code != 200:
                    continue

                if response.status_code != 200: continue
                root = ET.fromstring(response.content)

                for item in root.findall(".//item"):
                    title = item.findtext("title", "")
                    link  = item.findtext("link", "")
                    desc  = item.findtext("description", "")

                    if title and link:
                        articles.append({
                            "title":       title,
                            "link":        link,
                            "description": desc
                        })

            except Exception as e:
                logger.warning(f"[RSS FAIL] {url} -> {str(e)}")
                continue

                        articles.append({"title": title, "link": link, "description": desc})
            except: continue
        return articles

    def fetch_full_article(self, url):
        try:
            response = requests.get(url, timeout=8, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
            })

            if response.status_code != 200:
                return ""

            response = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code != 200: return ""
            
            soup = BeautifulSoup(response.content, "html.parser")

            for tag in soup(["script", "style", "nav", "footer", "header", "aside", "figure", "figcaption", "iframe", "form"]):
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()

            article_body = (
                soup.find("article") or
                soup.find("div", class_=re.compile(r"article|content|story|body|post", re.I)) or
                soup.find("main")
            )

            article_body = soup.find("article") or soup.find("div", class_=re.compile(r"article|content|body", re.I))
            target = article_body if article_body else soup

            paragraphs = target.find_all("p")
            texts = [
                p.get_text().strip()
                for p in paragraphs
                if len(p.get_text().strip()) > 40
            ]

            texts = [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 45]
            
            full_text = " ".join(texts)

            if len(full_text) > 1500:
                full_text = full_text[:1500].rsplit(' ', 1)[0] + '...'

            return full_text.strip()

        except Exception as e:
            logger.warning(f"[ARTICLE FAIL] {url} -> {str(e)}")
            return ""
            return full_text[:1500].strip() if len(full_text) > 1500 else full_text.strip()
        except: return ""

    def extract_keywords(self, text):
        stopwords = {
            "what", "happened", "in", "the", "is", "right", "now",
            "tell", "me", "about", "latest", "news", "from", "can",
            "you", "show", "give", "get", "find", "please", "today",
            "happening", "going", "on", "any", "update", "updates"
        }
        words = text.lower().split()
        return [w for w in words if w not in stopwords and len(w) > 2]
        stopwords = {"what", "happened", "in", "the", "is", "now", "tell", "about", "latest", "news"}
        return [w for w in text.lower().split() if w not in stopwords and len(w) > 2]

    def filter_articles(self, articles, keywords):
        if not keywords:
            return articles[:3]

        if not keywords: return articles[:3]
        scored = []
        for article in articles:
            text  = (article["title"] + " " + article["description"]).lower()
        for art in articles:
            text = (art["title"] + " " + art.get("description", "")).lower()
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scored.append((score, article))

            if score > 0: scored.append((score, art))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [a[1] for a in scored]

    def clean_description(self, desc):
        if not desc:
            return ""

        desc = re.sub(r'<[^>]+>', '', desc)
        desc = re.sub(r'&[a-zA-Z]+;', ' ', desc)
        desc = re.sub(r'\s+', ' ', desc)
        desc = desc.strip()

        if len(desc) > 300:
            desc = desc[:300].rsplit(' ', 1)[0] + '...'

        return desc

    def format_response(self, articles, query):
        response_text = f"Here's what's happening related to '{query}':\n\n"
        voice_parts   = [f"Here's what's happening related to {query}."]

        voice_parts = [f"Here's the latest on {query}."]
        for i, art in enumerate(articles, 1):
            title = art['title'].strip()

            print(f"   [Fetching article {i}...]")
            full_text = self.fetch_full_article(art['link'])
            desc = full_text if full_text else art.get('description', '')
            voice_parts.append(f"Article {i}. {art['title']}. {desc[:300]}")

            if full_text:
                desc = full_text
            else:
                desc = self.clean_description(art.get('description', ''))

            response_text += f"{i}. {title}\n"
            if desc:
                response_text += f"   {desc}\n"
            response_text += "\n"

            voice_parts.append(f"Article {i}. {title}. {desc}")

        voice_text = " ".join(voice_parts)

        return {
            "type": "web",
            "data": {
                "query":      query,
                "articles":   articles,
                "text":       response_text,
                "voice_text": voice_text
            }
        }

    def fallback_response(self, query):
        return {
            "type": "web",
            "data": {
                "query":    query,
                "articles": [],
                "text":     f"I couldn't find exact matches for '{query}', but try a broader topic."
                "query": query,
                "articles": articles,
                "voice_text": " ".join(voice_parts)
            }
        }

    def error_response(self):
        return {
            "type": "web",
            "data": {
                "text": "Something went wrong while fetching news."
            }
        }
        return {"type": "error", "data": {"text": "I encountered an issue accessing the web."}}

    def process(self, text: str, intent: str = None, category: str = None):
        return self.run(text, intent=intent, category=category)
    def fallback_response(self, query):
        return {"type": "web", "data": {"query": query, "articles": [], "text": "No specific news found."}}
