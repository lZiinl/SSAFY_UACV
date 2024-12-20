import time
from gpiozero import DistanceSensor
import math
import paho.mqtt.client as mqtt
import json

# MQTT 설정
HOST = "i11c102.p.ssafy.io"  # 예: "localhost" 또는 브로커의 올바른 호스트 이름/주소
PORT = 1883
mqtt_topic = "raspberry/sensors/data"

client = mqtt.Client()

cnt = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client.on_connect = on_connect
client.username_pw_set(username="client2", password="ssafyi11C102!!")
client.connect(HOST, PORT)

try:
    while True:
        # 센서 데이터 MQTT로 전송

        cnt = cnt + 1
        payload = "HI"
        client.publish(mqtt_topic, json.dumps(payload))
        print(f"Published: {payload}")

        time.sleep(1)

except KeyboardInterrupt:
    print("종료")

finally:
    client.disconnect()
