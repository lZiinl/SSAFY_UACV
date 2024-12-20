import json
import paho.mqtt.client as mqtt
import board
import busio
from adafruit_motor import motor
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
import threading
import time

# MQTT 설정
HOST = "i11c102.p.ssafy.io"
PORT = 1883
control_topic = "orin/#"

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

kit.servo[0].angle = 90
kit.servo[1].angle = 140
kit.servo[2].angle = 90

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
    global servo_steer
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
        steer = payload.get("steer")
        cannon_x = payload.get("cannon_x")
        cannon_y = payload.get("cannon_y")
        command = payload.get("move")

        print(f"Publish: {payload}")

        if command == 'forward':
            print("전진")
            motor_hat.set_throttle(1)
        
        elif command == 'backward':
            print("후진")
            motor_hat.set_throttle(-1)
        
        elif command == 'stop':
            print("정지")
            motor_hat.set_throttle(0)
        
        if steer != servo_steer:

            if steer < 45:
                steer = 45

            elif steer > 135:
                steer = 135

            kit.servo[0].angle = steer
            if steer < 90 :
                print("좌측")

            elif steer > 90 :
                print("우측")

            elif steer == 90 :
                print("가운데")

            steer_servo = steer

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
    except json.JSONDecodeError:
        print("Failed to decode JSON message")

# MQTT 클라이언트 설정
client = mqtt.Client()

client.username_pw_set(username="orin", password="ssafyi11C102!!")

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

