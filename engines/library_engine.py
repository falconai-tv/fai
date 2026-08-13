import os
import re
import pickle
import logging

from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger("FalconAI.LibraryEngine")

def is_low_quality_chunk(text: str) -> bool:
    if not text:
        return True

    length = len(text)
    if length < 50:
        return True

    digit_ratio = sum(ch.isdigit() for ch in text) / length
    comma_count = text.count(",")
    words = text.split()
    word_count = max(len(words), 1)
    comma_ratio = comma_count / word_count

    if digit_ratio > 0.08:
        return True

    if comma_ratio > 0.12:
        return True

    sentence_endings = len(re.findall(r"[.!?]\s+[A-Z]", text))
    if sentence_endings < 2 and word_count > 60:
        return True

    chapter_mentions = len(re.findall(r"\bChapter\s+\d+\b", text, flags=re.I))
    if chapter_mentions >= 2:
        return True

    capitalized = sum(1 for w in words if w[:1].isupper())
    cap_ratio = capitalized / word_count
    if cap_ratio > 0.4 and sentence_endings < 3 and word_count > 40:
        return True

    lower_text = text.lower()
    if "about the author" in lower_text:
        return True

    if re.search(r"\b(?:[A-Z]\s){3,}[A-Z]\b", text):
        return True

    all_caps_words = sum(1 for w in words if len(w) > 1 and w.isupper())
    all_caps_ratio = all_caps_words / word_count
    if all_caps_ratio > 0.25:
        return True

    return False

class LibraryEngine:
    def __init__(self, books_dir="books"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.books_dir = os.path.join(base_dir, books_dir)
        self.index_path = os.path.join(base_dir, "core", "library_index.pkl")

        self.vectorizer = None
        self.vectors = None
        self.chunks = []

        self._load_index()

    def _load_index(self):
        if not os.path.exists(self.index_path):
            logger.warning(
                f"Indeksi i librarise mungon te {self.index_path}. "
                f"Xhiro 'python build_library_index.py' per ta krijuar."
            )
            return

        try:
            with open(self.index_path, "rb") as f:
                data = pickle.load(f)

            self.vectorizer = data["vectorizer"]
            self.vectors = data["vectors"]
            self.chunks = data["chunks"]

            book_count = len({c["book"] for c in self.chunks})
            logger.info(
                f"LibraryEngine u ngarkua: {len(self.chunks)} copeza teksti "
                f"nga {book_count} libra."
            )
        except Exception as e:
            logger.error(f"Deshtoi ngarkimi i indeksit te librarise: {e}")

    def is_ready(self) -> bool:
        return self.vectorizer is not None and self.vectors is not None

    def search(self, query: str, top_k: int = 3, candidate_pool: int = 20):
        if not self.is_ready() or not query:
            return []

        query_vec = self.vectorizer.transform([query.lower()])
        scores = cosine_similarity(query_vec, self.vectors).flatten()

        top_indices = scores.argsort()[::-1][:candidate_pool]

        results = []
        for idx in top_indices:
            score = float(scores[idx])
            if score <= 0.05:
                continue

            chunk = self.chunks[idx]

            if is_low_quality_chunk(chunk["text"]):
                continue

            results.append({
                "book": chunk["book"],
                "text": chunk["text"],
                "score": round(score, 3)
            })

            if len(results) >= top_k:
                break

        return results

    def learn_and_extract(self, query: str) -> str:
        if not query:
            return "Ju lutem jepni nje pyetje te vlefshme."

        if not self.is_ready():
            return (
                "Libraria ende nuk eshte indeksuar. Xhiro "
                "'python build_library_index.py' per te aktivizuar "
                "kerkimin ne librat e tu."
            )

        results = self.search(query, top_k=3)

        if not results:
            return (
                f"Nuk gjeta permbajtje te qarte te lidhur me '{query}' ne "
                f"librat e disponueshem, por mund te pergjigjem me njohuri "
                f"te pergjithshme nese deshiron."
            )

        response_parts = []
        for r in results:
            snippet = r["text"][:600].rsplit(" ", 1)[0] + "..."
            response_parts.append(f"[Nga: {r['book']}]\n{snippet}")

        return "\n\n".join(response_parts)

    def list_books(self):
        if not self.chunks:
            return []
        return sorted({c["book"] for c in self.chunks})
