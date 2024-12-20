import time
import math
import numpy as np
import json
from smbus2 import SMBus
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import serial

# I2C 버스 번호
bus = SMBus(1)
mpu = MPU9250(
    address_ak=AK8963_ADDRESS,  # 자력계 주소
    address_mpu_master=MPU9050_ADDRESS_68,  # 자이로스코프 및 가속도계 주소
    bus=1,
    gfs=GFS_250,  # 자이로스코프 전체 범위 250dps
    afs=AFS_2G,  # 가속도계 전체 범위 2G
    mfs=AK8963_BIT_16,  # 자력계 전체 범위 16비트
    mode=AK8963_MODE_C100HZ  # 자력계 100Hz 연속 모드
)

mpu.configure()  # 설정을 레지스터에 적용합니다.

# UART 설정
ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)

CALIBRATION_FILE = 'mag_calibration.json'

def calibrate_magnetometer():
    print("Calibrating magnetometer... Move the sensor in a figure-eight pattern")
    mag_data = []
    start_time = time.time()
    while time.time() - start_time < 60:  # 60초 동안 데이터를 수집합니다.
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

def read_accel_gyro():
    accel = mpu.readAccelerometerMaster()
    gyro = mpu.readGyroscopeMaster()
    return accel, gyro

try:
    while True:
        heading = get_heading(mag_offset)
        direction = get_direction(heading)
        accel, gyro = read_accel_gyro()

        payload = "Heading: {:.2f} degrees, Direction: {}\n".format(heading, direction)
        payload += "Accelerometer: X={:.2f}, Y={:.2f}, Z={:.2f}\n".format(accel[0], accel[1], accel[2])
        payload += "Gyroscope: X={:.2f}, Y={:.2f}, Z={:.2f}\n".format(gyro[0], gyro[1], gyro[2])

        print(payload)
        ser.write(payload.encode('utf-8'))

        time.sleep(1)
except KeyboardInterrupt:
    print("사용자에 의해 프로그램이 중단되었습니다.")
finally:
    ser.close()
    bus.close()

