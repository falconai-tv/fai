import re
import unicodedata
from typing import List


class TextCleaner:
    def __init__(self):
        self.contractions = {
            "im": "i am",
            "i'm": "i am",
            "dont": "do not",
            "can't": "cannot",
            "cant": "cannot",
            "won't": "will not",
            "wont": "will not",
            "it's": "it is",
            "thats": "that is",
            "what's": "what is",
            "whats": "what is",
            "ive": "i have",
            "i've": "i have",
            "you're": "you are",
            "youre": "you are"
        }

        self.common_fixes = {
            "happend": "happened",
            "hapened": "happened",
            "recieve": "receive",
            "teh": "the",
            "im": "i am"
        }

    def clean(self, text: str) -> str:
        if not text:
            return ""

        text = self._normalize_unicode(text)
        text = text.lower()
        text = self._remove_urls(text)
        text = self._remove_special_chars(text)
        text = self._expand_contractions(text)
        text = self._fix_spelling(text)
        text = self._remove_extra_spaces(text)

        return text.strip()

    def _normalize_unicode(self, text: str) -> str:
        return unicodedata.normalize("NFKD", text)

    def _remove_urls(self, text: str) -> str:
        return re.sub(r"http\S+|www\S+", "", text)

    def _remove_special_chars(self, text: str) -> str:
        return re.sub(r"[^a-z0-9\s]", " ", text)

    def _expand_contractions(self, text: str) -> str:
        words = text.split()
        expanded = [self.contractions.get(w, w) for w in words]
        return " ".join(expanded)

    def _fix_spelling(self, text: str) -> str:
        words = text.split()
        fixed = [self.common_fixes.get(w, w) for w in words]
        return " ".join(fixed)

    def _remove_extra_spaces(self, text: str) -> str:
        return re.sub(r"\s+", " ", text)

    def tokenize(self, text: str) -> List[str]:
        return self.clean(text).split()

    def remove_stopwords(self, text: str) -> str:
        stopwords = {
            "the", "is", "at", "which", "on", "and", "a", "an", "i",
            "am", "are", "was", "were", "to", "for", "of"
        }

        words = self.clean(text).split()
        filtered = [w for w in words if w not in stopwords]

        return " ".join(filtered)

    def extract_keywords(self, text: str) -> List[str]:
        words = self.clean(text).split()

        keywords = [w for w in words if len(w) > 3]

        return keywords

    def normalize_for_ml(self, text: str) -> str:
        text = self.clean(text)
        text = self.remove_stopwords(text)
        return text

_cleaner_instance = TextCleaner()

def clean_text(text: str) -> str:
    return _cleaner_instance.clean(text)