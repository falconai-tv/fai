import pytesseract
import cv2
import numpy as np


class ChannelAI:
    def __init__(self):
        pass

    def analyze_frame(self, frame, query: str) -> float:
        text_score = self.ocr_score(frame, query)
        vision_score = self.visual_score(frame, query)

        return (text_score * 0.7) + (vision_score * 0.3)

    def ocr_score(self, frame, query: str) -> float:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(gray)

        text = text.lower()
        query = query.lower()

        keywords = query.split()

        matches = sum(1 for k in keywords if k in text)

        return min(matches / max(len(keywords), 1), 1.0)

    def visual_score(self, frame, query: str) -> float:
        h, w, _ = frame.shape

        bottom = frame[int(h*0.7):h, :]

        brightness = np.mean(bottom)

        score = 0.5 if brightness > 120 else 0.2

        geopolitical = ["iran", "war", "russia", "israel", "china"]

        if any(g in query.lower() for g in geopolitical):
            score += 0.3

        return min(score, 1.0)