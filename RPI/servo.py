from gpiozero import AngularServo
from time import sleep

servo = AngularServo(14, min_angle=0, max_angle=90)

while True:
        servo.angle = 90
        sleep(0.5)
        servo.angle = 10
        sleep(0.5)
