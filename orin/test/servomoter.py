import time
from adafruit_servokit import ServoKit

import smbus2
import busio
import board

i2c_bus = busio.I2C(board.SCL, board.SDA)

def i2c_scan(i2c):
    while not i2c.try_lock():
        pass

    try:
        devices = i2c.scan()
        return devices
    finally:
        i2c.unlock()

try:
    print("Scanning I2C bus ...")

    devices = i2c_scan(i2c_bus)
     

    if not devices:
        raise ValueError("No I2C devices found on the bus.")

    try:
        kit = ServoKit(channels=16, i2c=i2c_bus, address=0x60)
        print("PCA9685 initialized at address 0x60")

    except Exception as e:
        print(f"ERROR initializing PCA9685: {e}")
        raise

    pan = 0
    kit.servo[0].angle = pan

    print("Servo moters initialized")
    print("Starting servo control test...")

    for i in range(0,180):
        kit.servo[0].angle = i
        print(f"Servo 0 angle: {i}")
        time.sleep(0.05)
    for i in range(180, 0 , -1):
        kit.servo[0].angle = i
        print(f"Servo 0 angle: {i}")
        time.sleep(0.05)

    print("Servo control test complete")

except Exception as a:
    print("error")

kit.servo[0].angle = 90
