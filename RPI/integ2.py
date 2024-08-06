from gpiozero import OutputDevice
from time import sleep
import time
import math
import numpy as np
import json
from smbus2 import SMBus
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import threading

# 릴레이 설정
relay = OutputDevice(25, active_high=True, initial_value=False)

def relay_on():
    relay.on()
    print("Relay is ON")

def relay_off():
    relay.off()
    print("Relay is OFF")

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

def relay_control():
    while True:
        command = input("Enter 'on' to activate the relay: \n")
        if command.lower() == "on":
            relay_on()
            sleep(2)
            relay_off()
            sleep(2)

def magnetometer_reading():
    try:
        while True:
            heading = get_heading(mag_offset)
            direction = get_direction(heading)
            print("Heading: {:.2f} degrees, Direction: {}".format(heading, direction))
            sleep(1)
    except KeyboardInterrupt:
        print("사용자에 의해 프로그램이 중단되었습니다.")
    finally:
        bus.close()

# 두 개의 스레드를 생성하여 각각 키보드 입력과 자력계 데이터 읽기를 처리
relay_thread = threading.Thread(target=relay_control)
mag_thread = threading.Thread(target=magnetometer_reading)

relay_thread.start()
mag_thread.start()

relay_thread.join()
mag_thread.join()

