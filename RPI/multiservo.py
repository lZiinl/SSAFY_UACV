from gpiozero import AngularServo
from time import sleep

servo1 = AngularServo(14, min_angle=0, max_angle=90)
servo2 = AngularServo(23, min_angle=0, max_angle=90)
servo3 = AngularServo(24, min_angle=0, max_angle=90)

while True:
    for i in range(0,180,90):
        servo1.angle = i
        servo2.angle = i
        servo3.angle = i
        sleep(1)

