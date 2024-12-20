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
import paho.mqtt.client as mqtt

# MQTT 설정
HOST = "i11c102.p.ssafy.io"
PORT = 1883
mqtt_topic = "rpi/sensor"
relay_topic = "rpi/fire"

# MQTT 클라이언트 초기화
client = mqtt.Client()

client.username_pw_set(username="rpi5", password="ssafyi11C102!!")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(relay_topic)  # relay_topic 구독
    else:
        print(f"Failed to connect, return code {rc}\n")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT Broker")

def on_message(client, userdata, msg):
    if msg.topic == relay_topic:
        payload = json.loads(msg.payload.decode('utf-8'))

        print(f"Publish: {payload}")

        command = payload.get("relay")
        if command == "on":
            relay_on()
            sleep(2)
            relay_off()
            sleep(2)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# 브로커에 연결 시도
try:
    client.connect(HOST, PORT, 60)
    client.loop_start()
except Exception as e:
    print(f"Could not connect to MQTT Broker: {e}")
    exit()

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
        sleep(0.1)
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

def magnetometer_reading():
    try:
        while True:
            heading = get_heading(mag_offset)
            direction = get_direction(heading)
            #print("Heading: {:.2f} degrees, Direction: {}".format(heading, direction))
            payload = {
                    "Heading" : round(heading,2),
                    "Direction" : direction
            }
            #client.publish(mqtt_topic, json.dumps(payload))
            sleep(1)
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        bus.close()
        client.disconnect()

# 자력계 데이터 읽기 스레드 생성
mag_thread = threading.Thread(target=magnetometer_reading)

mag_thread.start()

mag_thread.join()

