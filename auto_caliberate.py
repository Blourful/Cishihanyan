import cv2
import numpy as np
from adb_tool import screenshot, tap

def analyze_roi(roi):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    contrast = gray.std()
    brightness = gray.mean()

    edges = cv2.Canny(gray, 60, 150)
    edge_ratio = np.mean(edges > 0)

    return {"contrast": contrast, "brightness": brightness, "edge_ratio": edge_ratio}


def auto_threshold(sample_images):
    """
    sample_images: 一组“start界面截图”
    """

    contrasts = []
    edges = []

    for img in sample_images:
        roi_stats = analyze_roi(img)
        contrasts.append(roi_stats["contrast"])
        edges.append(roi_stats["edge_ratio"])

    # ===== 自动生成阈值 =====
    contrast_thr = np.mean(contrasts) * 0.8
    edge_thr = np.mean(edges) * 0.8

    return {"contrast_thr": contrast_thr, "edge_thr": edge_thr}

img = cv2.imread("restart_button.png")
params = auto_threshold([img])
print(params)