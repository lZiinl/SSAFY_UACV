from gpiozero import AngularServo
from time import sleep

servo = AngularServo(24, min_angle=0, max_angle=90)

while True:
        servo.angle = 90
        sleep(1)
        servo.angle = 0
        sleep(1)
