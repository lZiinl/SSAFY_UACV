from gpiozero import OutputDevice, AngularServo
from time import sleep
import time
import math
import numpy as np
import json
from smbus2 import SMBus
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

# 릴레이 설정
relay = OutputDevice(25, active_high=True, initial_value=False)

def relay_on():
    relay.on()
    print("Relay is ON")

def relay_off():
    relay.off()
    print("Relay is OFF")

# 서보 모터 설정
servo1 = AngularServo(23, min_angle=0, max_angle=90)
servo2 = AngularServo(24, min_angle=0, max_angle=90)

servo1.angle = 50

# I2C 버스 및 센서 설정
bus = SMBus(1)
mpu = MPU9250(
    address_ak=AK8963_ADDRESS,
    address_mpu_master=MPU9050_ADDRESS_68,
    bus=1,
    gfs=GFS_250,
    afs=AFS_2G,
    mfs=AK8963_BIT_16,
    mode=AK8963_MODE_C100HZ
)

mpu.configure()

CALIBRATION_FILE = 'mag_calibration.json'

def calibrate_magnetometer():
    print("Calibrating magnetometer... Move the sensor in a figure-eight pattern")
    mag_data = []
    start_time = time.time()
    while time.time() - start_time < 60:
        mag = mpu.readMagnetometerMaster()
        mag_data.append(mag)
        time.sleep(0.1)
    mag_data = np.array(mag_data)
    mag_min = mag_data.min(axis=0)
    mag_max = mag_data.max(axis=0)
    mag_offset = (mag_max + mag_min) / 2
    with open(CALIBRATION_FILE, 'w') as f:
        json.dump(mag_offset.tolist(), f)
    return mag_offset

def load_calibration():
    try:
        with open(CALIBRATION_FILE, 'r') as f:
            mag_offset = np.array(json.load(f))
        return mag_offset
    except FileNotFoundError:
        return calibrate_magnetometer()

mag_offset = load_calibration()

def get_heading(mag_offset):
    mag_data = mpu.readMagnetometerMaster()
    mx, my, mz = mag_data - mag_offset
    heading = math.atan2(my, mx) * (180 / math.pi)
    if heading < 0:
        heading += 360
    return heading

def get_direction(heading):
    directions = [
        "N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"
    ]
    idx = round(heading / 45) % 8
    return directions[idx]

try:
    while True:
        # 릴레이 제어
        relay_on()
        sleep(2)
        relay_off()
        sleep(2)
        
        # 서보 모터 제어
        servo1.angle = 80
        sleep(2)
        servo2.angle = 90
        sleep(2)
        servo1.angle = 50
        sleep(2)
        servo2.angle = 0
        sleep(2)
        servo2.angle = 45
        sleep(2)
        
        # 자력계 데이터 읽기 및 출력
        heading = get_heading(mag_offset)
        direction = get_direction(heading)
        print("Heading: {:.2f} degrees, Direction: {}".format(heading, direction))
        sleep(1)

except KeyboardInterrupt:
    print("사용자에 의해 프로그램이 중단되었습니다.")
finally:
    bus.close()

