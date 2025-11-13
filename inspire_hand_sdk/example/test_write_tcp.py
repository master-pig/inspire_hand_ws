"""
通过 Modbus TCP 控制灵巧手动作示例
需要安装 pymodbus: pip install pymodbus
"""

from pymodbus.client import ModbusTcpClient
import time

# ====== 配置 ======
HAND_IP = "192.168.123.210"   # 灵巧手 IP
HAND_PORT = 6000               # Modbus TCP 默认端口（说明书里可能是6000）
FINGER_COUNT = 12               # 六个自由度（通常五指+掌）
MOVE_DELAY = 1.0               # 每次动作等待时间（秒）

# 寄存器地址（根据说明书）
RESET_PARA = 1006              # 恢复出厂参数
DEFAULT_SPEED_SET = 1032       # 上电速度设置，6 short (12 byte)
ANGLE_SET = 1486               # 角度目标寄存器，6 short (12 byte)

# ====== 连接灵巧手 ======
client = ModbusTcpClient(HAND_IP, port=HAND_PORT)
if not client.connect():
    print("连接失败，请检查 IP 和端口")
    exit(1)

print("连接成功")

# ====== 可选：复位参数 ======
print("复位参数")
client.write_register(RESET_PARA - 1000, 1)  # 写1表示复位
time.sleep(0.5)

# ====== 设置速度 ======
print("设置默认速度")
speed_values = [50, 50, 50, 50, 50, 50]  # 每个自由度的速度，可调整
for i, val in enumerate(speed_values):
    client.write_register(DEFAULT_SPEED_SET - 1000 + i, val)
time.sleep(0.5)

# ====== 控制手指动作 ======
# 定义几个动作，每个动作对应六个自由度角度
actions = [
    [30, 30, 30, 30, 30, 0,0, 0, 0, 0, 0, 0],  # 半握
    [0, 0, 0, 60, 60, 0,0, 0, 0, 0, 0, 0],  # 握拳
    [255, 255, 0, 0, 0, 0,0, 0, 0, 0, 0, 0],       # 张开手

]

for action in actions:
    print(f"执行动作: {action}")
    for i, angle in enumerate(action):
        client.write_register(ANGLE_SET - 1000 + i, angle)
    time.sleep(MOVE_DELAY)

print("完成动作，关闭连接")
client.close()
