import cv2
import numpy as np

RESTART_ROI = {"start": (0.2056, 0.1456), "end": (0.3233, 0.3475)}


def crop_roi(frame, roi):
    h, w = frame.shape[:2]

    x1 = int(roi["start"][0] * w)
    y1 = int(roi["start"][1] * h)
    x2 = int(roi["end"][0] * w)
    y2 = int(roi["end"][1] * h)

    return frame[y1:y2, x1:x2], (x1, y1, x2, y2)


def detect_restart(frame, debug=False):

    roi, box = crop_roi(frame, RESTART_ROI)

    if roi is None or roi.size == 0:
        return False, 0.0

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    contrast = gray.std()

    edges = cv2.Canny(gray, 60, 150)
    edge_ratio = np.mean(edges > 0)

    score = contrast + edge_ratio * 100
    is_restart = 30 < score < 45

    # is_restart = contrast > params["contrast_thr"] and edge_ratio > params["edge_thr"]
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

        # cv2.imshow("debug_restart", show)
        cv2.imshow("debug_roi", roi)

        cv2.waitKey(1)

    return is_restart, score


if __name__ == "__main__":
    import time
    from adb_tool import screenshot

    params = {"contrast_thr": 21.35, "edge_thr": 0.0731}

    while True:
        frame = screenshot()

        ok, score = detect_restart(frame, debug=True)

        if ok:
            print("👉 检测到 再来一次界面")

        # ===== 关闭窗口检测 =====
        if cv2.getWindowProperty("debug_roi", cv2.WND_PROP_VISIBLE) < 1:
            break

        time.sleep(0.1)

    cv2.destroyAllWindows()
