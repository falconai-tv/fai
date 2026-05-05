import cv2
import numpy as np
import time
import logging
import threading
import requests
import tempfile

from dataclasses import dataclass

logger = logging.getLogger("FalconAI.ChannelPlayer")


@dataclass
class Channel:
    name: str
    url: str

class ChannelPlayer:
    def __init__(self, channels, channel_ai, web_engine):
        self.channels = channels
        self.channel_ai = channel_ai
        self.web_engine = web_engine

        self.scan_interval = 6
        self.frame_sample_rate = 1

        self.stop_flag = False

    def find_and_play(self, query: str):
        logger.info(f"[CHANNEL_PLAYER] Query received: {query}")

        best_match = None
        best_score = 0

        for channel in self.channels:
            score = self.scan_channel(channel, query)

            logger.info(f"[CHANNEL_SCAN] {channel.name} score={score}")

            if score > best_score:
                best_score = score
                best_match = channel

        if best_match and best_score > 0.4:
            logger.info(f"[CHANNEL_PLAYER] MATCH FOUND: {best_match.name}")
            return self.play_channel(best_match)

        logger.info("[CHANNEL_PLAYER] No match found → fallback web engine")
        return self.web_engine.process(query, intent="watch_news")

    def scan_channel(self, channel: Channel, query: str) -> float:
        try:
            cap = cv2.VideoCapture(channel.url)

            if not cap.isOpened():
                return 0.0

            frame_count = 0
            scores = []

            start_time = time.time()

            while time.time() - start_time < self.scan_interval:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1

                if frame_count % self.frame_sample_rate != 0:
                    continue

                score = self.channel_ai.analyze_frame(frame, query)
                scores.append(score)

            cap.release()

            if not scores:
                return 0.0

            return float(np.mean(scores))

        except Exception as e:
            logger.error(f"[CHANNEL_SCAN_ERROR] {channel.name}: {e}")
            return 0.0

    def play_channel(self, channel: Channel):
        return {
            "type": "video_stream",
            "data": {
                "name": channel.name,
                "url": channel.url,
                "autoplay": True
            }
        }

    def continuous_monitor(self, query: str):
        def loop():
            while not self.stop_flag:
                self.find_and_play(query)
                time.sleep(30)

        thread = threading.Thread(target=loop)
        thread.daemon = True
        thread.start()