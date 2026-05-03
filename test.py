import subprocess

ADB_PATH = r"D:\Program Files\YXArkNights-12.0\shell\adb.exe"
DEVICE_ID = "127.0.0.1:16384"


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


# 1. 测试 adb 是否可用
result = run([ADB_PATH, "version"])
print("ADB版本检查：")
print(result.stdout)
print(result.stderr)

# 2. 查看设备列表
result = run([ADB_PATH, "devices"])
print("\n设备列表：")
print(result.stdout)

# 3. 单独检查目标设备
if DEVICE_ID in result.stdout:
    print("\n✔ 设备已连接")
else:
    print("\n✘ 设备未连接")
