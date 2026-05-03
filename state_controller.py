import time


class RestartController:
    def __init__(self):
        self.last_trigger_time = 0
        self.cooldown = 2.0  # 2秒内不重复触发
        self.hit_count = 0
        self.hit_threshold = 3  # 连续3帧才算成功

    def update(self, detected):
        now = time.time()

        if detected:
            self.hit_count += 1
        else:
            self.hit_count = 0

        # 连续命中判断
        if self.hit_count >= self.hit_threshold:

            # 冷却判断
            if now - self.last_trigger_time > self.cooldown:
                self.last_trigger_time = now
                self.hit_count = 0
                return True

        return False
