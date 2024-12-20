from adafruit_motor import motor
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
import board
import busio
import paho.mqtt.client as mqtt
import threading
import time
import json

# MQTT 설정
HOST = "192.168.100.104"
PORT = 1883
control_topic = "orin/control"

# PWMThrottleHat 클래스 정의
class PWMThrottleHat:
    def __init__(self, pwm, channel):
        self.pwm = pwm
        self.channel = channel
        self.pwm.frequency = 60

    def set_throttle(self, throttle):
        pulse = int(0xFFFF * abs(throttle))
        if throttle > 0:  # 전진
            self.pwm.channels[self.channel + 5].duty_cycle = pulse
            self.pwm.channels[self.channel + 4].duty_cycle = 0xFFFF
            self.pwm.channels[self.channel + 3].duty_cycle = 0

        elif throttle < 0:  # 후진
            self.pwm.channels[self.channel + 5].duty_cycle = pulse
            self.pwm.channels[self.channel + 4].duty_cycle = 0
            self.pwm.channels[self.channel + 3].duty_cycle = 0xFFFF

        else:  # 정지
            self.pwm.channels[self.channel + 5].duty_cycle = 0
            self.pwm.channels[self.channel + 4].duty_cycle = 0
            self.pwm.channels[self.channel + 3].duty_cycle = 0

# I2C 설정
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 60

motor_hat = PWMThrottleHat(pca, channel=0)

kit = ServoKit(channels=16, i2c=i2c, address=0x60)
pan = 90
kit.servo[0].angle = pan

# MQTT 콜백 함수 정의
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(control_topic)  # control_topic 구독
    else:
        print(f"Failed to connect, return code {rc}\n")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT Broker")

def on_message(client, userdata, msg):
    global pan
    command = msg.payload.decode('utf-8')
    
    if command == 'go':
        print("전진")
        motor_hat.set_throttle(1)
    
    elif command == 'back':
        print("후진")
        motor_hat.set_throttle(-1)
    
    elif command == 'stop':
        print("정지")
        motor_hat.set_throttle(0)
    
    elif command == 'left':
        print("좌측")
        pan = 20
        kit.servo[0].angle = pan

    elif command == 'right':
        print("우측")
        pan = 160
        kit.servo[0].angle = pan
    
    elif command == 'mid':
        print("가운데")
        pan = 90
        kit.servo[0].angle = pan

    elif command == 'gun_up':
        print('포신 상승')
        pan = 70
        kit.servo[1].angle = pan

    elif command == 'gun_down':
        print('포신 하강')
        pan = 140
        kit.servo[1].angle = pan

    elif command == 'gun_mid':
        print('포신 가운데')
        pan = 140
        kit.servo[1].angle = pan
        pan = 90
        kit.servo[2].angle = pan

    elif command == 'gun_left':
        print('포신 좌측')
        pan = 170
        kit.servo[2].angle = pan

    elif command == 'gun_right':
        print('포신 우측')
        pan = 10
        kit.servo[2].angle = pan

    else:
        print("잘못된 명령어입니다.")

# MQTT 클라이언트 설정
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# 브로커에 연결 시도
try:
    client.connect(HOST, PORT, 60)
    client.loop_start()
except Exception as e:
    print(f"Could not connect to MQTT Broker: {e}")
    exit()

# 자원 정리
def cleanup():
    motor_hat.set_throttle(0)
    kit.servo[0].angle = 90
    kit.servo[1].angle = 140
    kit.servo[2].angle = 90
    pca.deinit()
    print("핀 정리 완료")

# 메인 프로그램
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.loop_stop()
    cleanup()
    client.disconnect()

