import time
from adb_tool import screenshot, tap

from state_detector import StateDetector
from start_flow import run_start_flow , tap_ratio
from recognize_jump import detect_jump
from recognize_jump2 import detect_jump as detect_jump2


def wait_menu(detector):
    print("📍 等待 MENU...")

    while True:
        frame = screenshot()

        if frame is None:
            continue

        state, score = detector.detect(frame)

        if state == "MENU":
            print(f"👉 MENU detected score={score:.1f}")

            run_start_flow(frame)

            time.sleep(0.5)
            return


def wait_start(detector):
    print("⏳ 等待 START...")

    while True:
        frame = screenshot()
        if frame is None:
            continue

        state, score = detector.detect(frame)

        if state == "START":
            print("👉 START detected score={score:.1f}")

            time.sleep(0.1)
            return


def play_loop(detector):
    print("🎮 进入 PLAY")
    count = 0

    while True:
        frame = screenshot()
        if frame is None:
            continue
        
        state, score = detector.detect(frame)
        
        ok, score1 = detect_jump(frame, debug=False)
        if score1<66 and score1>52 and count == 0:
            print("👉 检测到 跳跃")
            print("score1:", score1)
            tap(540, 540)
            count+=1
        ok2, score2 = detect_jump2(frame, debug=False)
        if score2<75 and score2>60 and count==1:
            print("👉 检测到 跳跃2")
            print("score2:", score2)
            tap(540, 540)
            count-=1

        if state == "RESTART":
            break
        
def restart(detector):
    print("🔄 重新开始")
    time.sleep(1)
    frame = screenshot()
    tap_ratio(frame, 0.2644, 0.2419)
   


if __name__ == "__main__":
    detector = StateDetector()

    wait_menu(detector)
    # wait_start(detector)
    play_loop(detector)
    while True:
        restart(detector)
        play_loop(detector)
