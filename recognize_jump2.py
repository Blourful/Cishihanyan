import cv2
import numpy as np

# =========================================================
# ROI（开始按钮区域）
# =========================================================
START_ROI = {"start": (0.2689, 0.7013), "end": (0.3778, 0.8394)}


def crop_roi(frame, roi):
    h, w = frame.shape[:2]

    x1 = int(roi["start"][0] * w)
    y1 = int(roi["start"][1] * h)
    x2 = int(roi["end"][0] * w)
    y2 = int(roi["end"][1] * h)

    return frame[y1:y2, x1:x2], (x1, y1, x2, y2)


def detect_jump(frame, debug=False):

    roi, box = crop_roi(frame, START_ROI)

    if roi is None or roi.size == 0:
        return False, 0.0

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    contrast = gray.std()

    edges = cv2.Canny(gray, 60, 150)
    edge_ratio = np.mean(edges > 0)

    score = contrast + edge_ratio * 100
    is_jump = 84 < score < 85

    #is_jump = contrast > params["contrast_thr"] and edge_ratio > params["edge_thr"]
    # ===== 可视化 =====
    if debug:
        show = frame.copy()

        x1, y1, x2, y2 = box
        cv2.rectangle(show, (x1, y1), (x2, y2), (0, 255, 0), 2)

        text = f"C:{contrast:.1f} E:{edge_ratio:.3f} S:{score:.1f}"
        cv2.putText(
            show,
            text,
            (x1, max(20, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2,
        )

        # cv2.imshow("debug_start", show)
        cv2.imshow("debug_roi", roi)

        cv2.waitKey(1)

    return is_jump, score


if __name__ == "__main__":
    import time
    from adb_tool import screenshot, tap

    params = {"contrast_thr": 21.35, "edge_thr": 0.0731}

    while True:
        frame = screenshot()

        ok, score = detect_jump(frame, debug=True)

        print(score)
        if score<75 and score>60: 
            print("click")
            print("👉 检测到 跳跃")
            # print("score:", score)
            tap(540, 540)
        # ===== 关闭窗口检测 =====
        if cv2.getWindowProperty("debug_roi", cv2.WND_PROP_VISIBLE) < 1:
            break

        # time.sleep(0.01)

    cv2.destroyAllWindows()
