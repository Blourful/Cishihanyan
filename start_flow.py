import time
from adb_tool import tap


def tap_ratio(frame, rx, ry):
    h, w = frame.shape[:2]
    x = int(rx * w)
    y = int(ry * h)
    tap(x, y)


def run_start_flow(frame):
    print("🚀 开始执行开局流程")

    # ① Start
    tap_ratio(frame, 0.2111, 0.8075)
    time.sleep(2)

    # ② 确认
    tap_ratio(frame, 0.4567, 0.4044)
    time.sleep(2)

    # ③ 人物确认
    tap_ratio(frame, 0.2478, 0.5256)
    time.sleep(2)

    print("✅ 开局流程完成")
    

