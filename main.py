import re
import logging
import requests
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from urllib.parse import quote


logger = logging.getLogger("FalconAI.WebEngine")


class WebEngine:

    def __init__(self):

        self.timeout = 6

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

            "sports": [
                "https://feeds.bbci.co.uk/sport/rss.xml"
            ],

            "balkan": [
                "https://feeds.bbci.co.uk/news/world/europe/rss.xml",
                "https://www.trtworld.com/rss",
                "https://exit.al/feed/"
            ],

            "general": [
                "https://feeds.bbci.co.uk/news/rss.xml"
            ]
        }

        self.intent_category = {
            "watch_news": "world",
            "watch_balkan_news": "balkan",
            "tech_news": "technology",
            "sports_news": "sports",
            "business_news": "business",
            "general_search": "general"
        }

        self.movie_platforms = {
            "tubi": "https://tubitv.com/search/",
            "pluto": "https://pluto.tv/en/search/details/movies/",
            "crackle": "https://www.crackle.com/search/",
            "rakuten": "https://www.rakuten.tv/it/search?q="
        }

    def process(self, text: str, intent: str = None, category: str = None):

        try:

            lower = text.lower()

            movie_keywords = [
                "movie",
                "movies",
                "film",
                "films",
                "watch",
                "play",
                "cinema",
                "shiko",
                "luaj",
                "world war",
                "harry potter",
                "batman",
                "spiderman",
                "superman"
            ]

            if (
                intent == "watch_movie"
                or any(k in lower for k in movie_keywords)
            ):
                return self.handle_movie_intent(text)

            return self.run_news_engine(
                query=text,
                intent=intent,
                category=category
            )

        except Exception as e:

            logger.error(f"[WEB ENGINE ERROR] {e}")

            return self.error_response()

    def handle_movie_intent(self, query):

        movie_name = re.sub(
            r"\b(play|watch|movie|movies|film|films|search|find|shiko|luaj|me gjej)\b",
            "",
            query,
            flags=re.I
        ).strip()

        if not movie_name:
            movie_name = query.strip()

        platform = "tubi"

        base_url = self.movie_platforms[platform]

        encoded = quote(movie_name)

        stream_url = f"{base_url}{encoded}"

        logger.info(f"[MOVIE] {movie_name}")
        logger.info(f"[MOVIE URL] {stream_url}")

        return {
            "type": "web_movie",
            "data": {
                "query": movie_name,
                "platform": platform,
                "stream_url": stream_url,
                "auto_play": True,
                "status": "success",
                "text": f"Opening {movie_name} on Tubi.",
                "voice_text": f"I'm opening {movie_name} on Tubi. Enjoy the movie.",
                "falcon_ai": f"Opening {movie_name} on Tubi."
            }
        }

    def run_news_engine(self, query, intent=None, category=None):

        if category is None:
            category = self.intent_category.get(intent, "general")

        logger.info(f"[NEWS] Category: {category}")

        keywords = self.extract_keywords(query)

        articles = self.fetch_articles(category)

        filtered = self.filter_articles(
            articles,
            keywords
        )

        if not filtered:
            return self.fallback_response(query)

        return self.format_response(
            filtered[:3],
            query
        )

    def fetch_articles(self, category):

        articles = []

        feeds = self.feeds.get(
            category,
            self.feeds["general"]
        )

        for url in feeds:

            try:

                response = requests.get(
                    url,
                    timeout=self.timeout,
                    headers={
                        "User-Agent": "Mozilla/5.0"
                    }
                )

                if response.status_code != 200:
                    continue

                root = ET.fromstring(response.content)

                for item in root.findall(".//item"):

                    title = item.findtext("title", "")
                    link = item.findtext("link", "")
                    desc = item.findtext("description", "")

                    if title and link:

                        articles.append({
                            "title": title,
                            "link": link,
                            "description": desc
                        })

            except Exception as e:

                logger.error(f"[RSS ERROR] {url} -> {e}")

        return articles

    def fetch_full_article(self, url):

        try:

            response = requests.get(
                url,
                timeout=8,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            if response.status_code != 200:
                return ""

            soup = BeautifulSoup(
                response.content,
                "html.parser"
            )

            for tag in soup([
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "aside"
            ]):
                tag.decompose()

            article_body = (
                soup.find("article")
                or soup.find(
                    "div",
                    class_=re.compile(r"article|content|body", re.I)
                )
            )

            target = article_body if article_body else soup

            paragraphs = target.find_all("p")

            texts = []

            for p in paragraphs:

                txt = p.get_text().strip()

                if len(txt) > 45:
                    texts.append(txt)

            full_text = " ".join(texts)

            if len(full_text) > 1500:
                return full_text[:1500]

            return full_text

        except Exception as e:

            logger.error(f"[ARTICLE ERROR] {e}")

            return ""

    def extract_keywords(self, text):

        stopwords = {
            "what",
            "happened",
            "latest",
            "news",
            "about",
            "tell",
            "today",
            "world",
            "the",
            "and",
            "for",
            "with",
            "from",
            "this",
            "that"
        }

        words = text.lower().split()

        return [
            w for w in words
            if w not in stopwords and len(w) > 2
        ]

    def filter_articles(self, articles, keywords):

        if not keywords:
            return articles[:3]

        scored = []

        for article in articles:

            combined = (
                article["title"] +
                " " +
                article.get("description", "")
            ).lower()

            score = 0

            for kw in keywords:

                if kw in combined:
                    score += 1

            if score > 0:
                scored.append((score, article))

        scored.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [x[1] for x in scored]

    def format_response(self, articles, query):

        voice_parts = [
            f"Here's the latest on {query}."
        ]

        for index, article in enumerate(articles, start=1):

            full_text = self.fetch_full_article(
                article["link"]
            )

            description = (
                full_text
                if full_text
                else article.get("description", "")
            )

            voice_parts.append(
                f"Article {index}. "
                f"{article['title']}. "
                f"{description[:300]}"
            )

        final_voice = " ".join(voice_parts)

        return {
            "type": "web",
            "data": {
                "query": query,
                "articles": articles,
                "text": final_voice,
                "voice_text": final_voice,
                "status": "success"
            }
        }

    def error_response(self):

        return {
            "type": "error",
            "data": {
                "text": "I encountered an issue accessing the web.",
                "status": "error"
            }
        }

    def fallback_response(self, query):

        return {
            "type": "web",
            "data": {
                "query": query,
                "articles": [],
                "text": f"I couldn't find anything about {query}.",
                "voice_text": f"I couldn't find anything about {query}.",
                "status": "empty"
            }
        }
