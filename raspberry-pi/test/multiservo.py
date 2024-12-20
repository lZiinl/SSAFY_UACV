from gpiozero import AngularServo
from time import sleep

servo1 = AngularServo(12, min_angle=0, max_angle=90)
servo2 = AngularServo(13, min_angle=0, max_angle=90)

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


