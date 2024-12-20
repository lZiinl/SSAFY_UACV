from gpiozero import OutputDevice
from gpiozero import AngularServo
from time import sleep

# GPIO 핀 번호 설정
relay = OutputDevice(25, active_high=True, initial_value=False)  # 릴레이가 HIGH로 활성화됨
servo2 = AngularServo(24, min_angle=0, max_angle=90)
servo1 = AngularServo(23, min_angle=0, max_angle=90)# 릴레이 제어 함수

def relay_on():
    relay.on()  # 릴레이 켜기
    print("Relay is ON")

def relay_off():
    relay.off()  # 릴레이 끄기
    print("Relay is OFF")

try:
    while True:
        relay_on()  # 릴레이 켜기
        servo1.angle=90
        servo2.angle=90
        sleep(1)  # 5초 대기
        relay_off()  # 릴레이 끄기
        servo1.angle=10
        servo2.angle=10
        sleep(1)  # 5초 대기

except KeyboardInterrupt:
    print("Program terminated")


