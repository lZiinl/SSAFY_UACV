import paho.mqtt.client as mqtt
from gpiozero import AngularServo
from time import sleep

servo1 = AngularServo(14, min_angle=0, max_angle=90)
servo2 = AngularServo(23, min_angle=0, max_angle=360)
servo3 = AngularServo(24, min_angle=0, max_angle=360)

# 서보 모터 초기화
current_angle = 0
servo.angle = current_angle

# MQTT 브로커 주소와 포트 번호
broker_address = "192.168.100.104"
port = 1883
topic_servo1 = "act/servo1"
topic_servo2 = "act/servo2"
topic_servo3 = "act/servo3"

# 수신된 데이터를 저장할 변수 초기화
data1 = 0.0
data2 = 0.0
data3 = 0.0

# MQTT 클라이언트 콜백 함수 설정
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    global data1
    global data2
    global data3
    
    try:
        # 수신된 메시지(payload)를 숫자로 변환
        data1 = float(msg.payload.decode())
        data2 = float(msg.payload.decode())
        data3 = float(msg.payload.decode())
        print(f"Received data: {data}")
    except ValueError:
        print("Received non-numeric data")

# MQTT 클라이언트 설정
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# MQTT 브로커에 연결
client.connect(broker_address, port, 60)

# 서보 모터 제어를 위한 루프
def servo_control_loop():
    global data
    global current_angle
    while True:
        if current_angle != data:
            current_angle = data
            if current_angle > 90:
                current_angle = 90
            elif current_angle < 0:
                current_angle = 0
            servo.angle = current_angle
            print(f"angle = {current_angle}", end='\r\n')
        sleep(0.1)

# 서보 모터 제어 루프를 비차단식으로 실행
from threading import Thread
control_thread = Thread(target=servo_control_loop)
control_thread.start()

# 네트워크 루프 시작
client.loop_forever()

