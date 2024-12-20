from adafruit_motor import motor
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
import board
import busio
import time
from pynput import keyboard

class PWMThrottleHat:
    def __init__(self, pwm, channel):
        self.pwm = pwm
        self.channel = channel
        self.pwm.frequency = 60

    def set_throttle(self, throttle):
        pulse = int(0xFFFF * abs(throttle))
        if throttle > 0: #전진 throttle > 0, 0보다 클 때
            self.pwm.channels[self.channel + 5].duty_cycle = pulse
            self.pwm.channels[self.channel + 4].duty_cycle = 0xFFFF
            self.pwm.channels[self.channel + 3].duty_cycle = 0

        elif throttle < 0: # 후진 throttle < 0, 0보다 작을 때
            self.pwm.channels[self.channel + 5].duty_cycle = pulse
            self.pwm.channels[self.channel + 4].duty_cycle = 0
            self.pwm.channels[self.channel + 3].duty_cycle = 0xFFFF
        
        else: #정지 상태 throttle == 0
            self.pwm.channels[self.channel + 5].duty_cycle = 0
            self.pwm.channels[self.channel + 4].duty_cycle = 0
            self.pwm.channels[self.channel + 3].duty_cycle = 0

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 60

motor_hat = PWMThrottleHat(pca, channel=0)

kit = ServoKit(channels=16, i2c=i2c, address=0x60)
pan = 90
kit.servo[0].angle = pan

def i2c_scan(i2c):
    while not i2c.try_lock():
        pass

    try:
        devices = i2c.scan()
        return devices

    finally:
        i2c.unlock()


# 작동부 

def move():
    global pan
    while True:
        move_command = input("명령어를 입력하세요 : ")

        if move_command == 'go':
            print("전진")
            motor_hat.set_throttle(1)
        
        elif move_command == 'back':
            print("후진")
            motor_hat.set_throttle(-1)
        
        elif move_command == 'stop':
            print("정지")
            motor_hat.set_throttle(0)
        
        elif move_command == 'left':
            print("좌측")
            pan = 45
            kit.servo[0].angle = pan

        elif move_command == 'right':
            print("우측")
            pan = 135
            kit.servo[0].angle = pan
        
        elif move_command == 'mid':
            print("가운데")
            pan = 90
            kit.servo[0].angle = pan

        elif move_command == 'gun_up':
            print('포신 상승')
            pan = 70
            kit.servo[1].angle=pan

        elif move_command == 'gun_down':
            print('포신 하강')
            pan = 140
            kit.servo[1].angle=pan

        elif move_command == 'gun_mid':
            print('포신 가운데')
            pan = 140
            kit.servo[1].angle=pan
            pan = 90
            kit.servo[2].angle=pan

        elif move_command == 'gun_left':
            print('포신 좌측')
            pan = 170
            kit.servo[2].angle=pan

        elif move_command == 'gun_right':
            print('포신 우측')
            pan = 10
            kit.servo[2].angle=pan

        else:
            print("wrong command")
        
try:
    move()
except KeyboardInterrupt:
    print("Exiting...")
finally:
    motor_hat.set_throttle(0)
    kit.servo[0].angle = 90
    kit.servo[1].angle = 140
    kit.servo[2].angle = 90
    pca.deinit()
    print("Cleaning up pins")
