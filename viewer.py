import cv2
import numpy as np
import time
from adb_tool import screenshot, tap

# ===== 缩放比例 =====
SCALE = 1

click_points = []

# ===== ROI框选变量 =====
start_x, start_y = -1, -1
end_x, end_y = -1, -1
selecting = False

# ===== 当前分辨率 =====
frame_w, frame_h = 1, 1


# ===== 点击 + ROI框选 =====
def mouse_event(event, x, y, flags, param):
    global start_x, start_y, end_x, end_y, selecting, frame_w, frame_h

    real_x = int(x / SCALE)
    real_y = int(y / SCALE)

    # ===== 左键按下 → 开始框选 =====
    if event == cv2.EVENT_LBUTTONDOWN:
        start_x, start_y = real_x, real_y
        selecting = True

        print(f"[START] ({start_x},{start_y})")

    # ===== 鼠标移动 → 更新框 =====
    elif event == cv2.EVENT_MOUSEMOVE and selecting:
        end_x, end_y = real_x, real_y

    # ===== 左键松开 → 结束框选 =====
    elif event == cv2.EVENT_LBUTTONUP:
        end_x, end_y = real_x, real_y
        selecting = False

        # ===== 比例输出 =====
        sx_r = start_x / frame_w
        sy_r = start_y / frame_h
        ex_r = end_x / frame_w
        ey_r = end_y / frame_h

        print(f"""
[ROI]
pixel:
  start: ({start_x}, {start_y})
  end:   ({end_x}, {end_y})

ratio:
  start: ({sx_r:.4f}, {sy_r:.4f})
  end:   ({ex_r:.4f}, {ey_r:.4f})
""")

    # ===== 右键：全屏截图（新增）=====
    elif event == cv2.EVENT_RBUTTONDOWN:
        frame = screenshot()
        cv2.imwrite("full.png", frame)
        print("[SAVE] 已保存 full.png")


# ===== 画点击点 =====
def draw_points(frame):
    for x, y in click_points:
        sx, sy = int(x * SCALE), int(y * SCALE)
        cv2.circle(frame, (sx, sy), 6, (0, 0, 255), -1)
    return frame


# ===== 主循环 =====
def run_viewer():
    global start_x, start_y, end_x, end_y, frame_w, frame_h

    cv2.namedWindow("debug", cv2.WINDOW_NORMAL)

    frame = screenshot()
    frame = cv2.resize(frame, (0, 0), fx=SCALE, fy=SCALE)
    cv2.imshow("debug", frame)
    cv2.waitKey(1)

    cv2.setMouseCallback("debug", mouse_event)

    print("调试启动：左键框选 / 右键全屏保存 / Space保存ROI / ESC退出")

    while True:
        frame = screenshot()
        if frame is None:
            continue

        raw = frame.copy()

        # ===== 更新分辨率 =====
        frame_h, frame_w = frame.shape[:2]

        # ===== 画ROI框 =====
        if start_x != -1 and end_x != -1:
            x1, y1 = int(start_x * SCALE), int(start_y * SCALE)
            x2, y2 = int(end_x * SCALE), int(end_y * SCALE)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # ===== 画点击点 =====
        frame = draw_points(frame)

        # ===== 显示 =====
        frame = cv2.resize(frame, (0, 0), fx=SCALE, fy=SCALE)
        cv2.imshow("debug", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 27:
            break

        if key == 32:
            if start_x != -1 and end_x != -1:
                x1, x2 = sorted([start_x, end_x])
                y1, y2 = sorted([start_y, end_y])

                roi = raw[y1:y2, x1:x2]
                cv2.imwrite("template.png", roi)
                print(f"[SAVE] template.png {roi.shape}")
            else:
                print("[WARN] 没有选中区域")

        if cv2.getWindowProperty("debug", cv2.WND_PROP_VISIBLE) < 1:
            break

        # time.sleep(0.03)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_viewer()
