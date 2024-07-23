import time
import io
import base64
from picamera2 import Picamera2
from PIL import Image
import paho.mqtt.client as mqtt

# MQTT 설정
mqtt_broker = "192.168.100.104"
mqtt_port = 1883
mqtt_topic = "raspberrypi/camera"

# MQTT 클라이언트 초기화
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}\n")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT Broker")

client.on_connect = on_connect
client.on_disconnect = on_disconnect

# 브로커에 연결 시도
try:
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_start()
except Exception as e:
    print(f"Could not connect to MQTT Broker: {e}")
    exit()

# 카메라 설정
picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()

def capture_and_publish():
    buffer = io.BytesIO()
    image_array = picam2.capture_array()
    image = Image.fromarray(image_array)
    image.save(buffer, format='JPEG')
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    result = client.publish(mqtt_topic, encoded_image)
    status = result[0]
    if status == 0:
        print("Image published")
    else:
        print(f"Failed to send message to topic {mqtt_topic}")

# 주기적으로 이미지 캡처 및 전송
try:
    while True:
        capture_and_publish()
        #time.sleep(0.1)  # 2초마다 이미지 캡처 및 전송
except KeyboardInterrupt:
    picam2.stop()
    client.disconnect()
    print("Stopped")

