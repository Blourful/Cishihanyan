import subprocess
import numpy as np
import cv2

ADB_PATH = r"D:\Program Files\YXArkNights-12.0\shell\adb.exe"
DEVICE_ID = "127.0.0.1:16384"


def adb(*args):
    return subprocess.run(
        [ADB_PATH, "-s", DEVICE_ID, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )


def screenshot():
    result = adb("exec-out", "screencap", "-p")

    img = np.frombuffer(result.stdout, np.uint8)
    frame = cv2.imdecode(img, cv2.IMREAD_COLOR)

    if frame is None:
        raise RuntimeError("截图失败")

    return frame


def tap(x, y):
    adb("shell", "input", "tap", str(x), str(y))
