import re
import unicodedata
from typing import List

class TextCleaner:
    def __init__(self):
        self.url_pattern = re.compile(r"http\S+|www\S+|https\S+")
        self.mention_pattern = re.compile(r"@\w+")
        self.hashtag_pattern = re.compile(r"#\w+")
        self.multi_space_pattern = re.compile(r"\s+")

    def clean(self, text: str) -> str:
        if not text:
            return ""

        text = self._normalize(text)
        text = self._remove_urls(text)
        text = self._remove_mentions(text)
        text = self._remove_hashtags(text)
        text = self._remove_non_ascii_noise(text)
        text = self._normalize_spaces(text)

        return text.strip().lower()

    def _normalize(self, text: str) -> str:
        return unicodedata.normalize("NFKD", text)

    def _remove_urls(self, text: str) -> str:
        return self.url_pattern.sub("", text)

    def _remove_mentions(self, text: str) -> str:
        return self.mention_pattern.sub("", text)

    def _remove_hashtags(self, text: str) -> str:
        return self.hashtag_pattern.sub("", text)

    def _remove_non_ascii_noise(self, text: str) -> str:
        return re.sub(r"[^\w\s\.\,\?\!\-]", "", text)

    def _normalize_spaces(self, text: str) -> str:
        return self.multi_space_pattern.sub(" ", text)

    def tokenize(self, text: str) -> List[str]:
        cleaned = self.clean(text)
        return cleaned.split()

    def extract_keywords(self, text: str) -> List[str]:
        tokens = self.tokenize(text)

        stopwords = {
            "the", "is", "a", "an", "and", "or", "to", "in", "on",
            "i", "you", "we", "they", "he", "she", "it", "of", "for",
            "me", "my", "your", "our"
        }

        return [t for t in tokens if t not in stopwords and len(t) > 2]

    def debug(self, text: str) -> dict:
        return {
            "original": text,
            "cleaned": self.clean(text),
            "tokens": self.tokenize(text),
            "keywords": self.extract_keywords(text)
        }