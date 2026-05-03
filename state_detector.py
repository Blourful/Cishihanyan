import cv2

from recognize_menu import detect_menu
from recognize_start import detect_start
from recognize_restart import detect_restart


class StateDetector:
    def __init__(self):
        pass

    def detect(self, frame):
        """
        返回：
        state, score
        """

        # =========================
        # 1. RESTART（最高优先级）
        # =========================
        ok_r, score_r = detect_restart(frame)
        if ok_r:
            return "RESTART", score_r

        # =========================
        # 2. START
        # =========================
        ok_s, score_s = detect_start(frame)
        if ok_s:
            return "START", score_s

        # =========================
        # 3. MENU（模板）
        # =========================
        ok_m, score_m = detect_menu(frame)
        if ok_m:
            return "MENU", score_m

        # =========================
        # 4. 默认 PLAYING
        # =========================
        return "PLAYING", 0.0
