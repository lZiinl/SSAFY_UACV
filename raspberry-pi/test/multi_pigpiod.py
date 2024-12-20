from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# pigpio 핀 팩토리 설정
factory = PiGPIOFactory()

# 서보 모터 설정 (하드웨어 PWM 핀 사용)
servo1 = AngularServo(12, min_angle=0, max_angle=90, pin_factory=factory)  # GPIO 12 사용
servo2 = AngularServo(13, min_angle=0, max_angle=90, pin_factory=factory)  # GPIO 13 사용

while True:
    servo1.angle = 50
    sleep(2)
    servo2.angle = 50
    sleep(2)
    servo1.angle = 50
    sleep(2)
    servo2.angle = 50
    sleep(2)
    servo2.angle = 50
    sleep(2)

