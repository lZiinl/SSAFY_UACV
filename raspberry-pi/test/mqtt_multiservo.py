import paho.mqtt.client as mqtt
from gpiozero import AngularServo
from gpiozero import Servo
from time import sleep
from threading import Thread
import logging

# 로그 설정
logging.basicConfig(level=logging.INFO)

# 서보 모터 설정
servo1 = AngularServo(14, min_angle=0, max_angle=90)  # 각도 제어 서보 모터
servo2 = Servo(23)  # 연속 회전 서보 모터
servo3 = Servo(24)  # 연속 회전 서보 모터

# MQTT 브로커 주소와 포트 번호
broker_address = "192.168.100.104"
port = 1883
topic_servo1 = "act/servo1"
topic_servo2 = "act/servo2"
topic_servo3 = "act/servo3"

# 수신된 데이터를 저장할 변수 초기화
data1 = None
data2 = None
data3 = None

# MQTT 클라이언트 콜백 함수 설정
def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected with result code {rc}")
    client.subscribe([(topic_servo1, 0), (topic_servo2, 0), (topic_servo3, 0)])

def on_message(client, userdata, msg):
    global data1, data2, data3
    
    try:
        if msg.topic == topic_servo1:
            data1 = float(msg.payload.decode())
            logging.info(f"Servo 1 received data: {data1}")
        elif msg.topic == topic_servo2:
            data2 = float(msg.payload.decode())
            logging.info(f"Servo 2 received data: {data2}")
        elif msg.topic == topic_servo3:
            data3 = float(msg.payload.decode())
            logging.info(f"Servo 3 received data: {data3}")
    except ValueError:
        logging.error("Received non-numeric data")

# MQTT 클라이언트 설정
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# MQTT 브로커에 연결
client.connect(broker_address, port, 60)

# 서보 모터 제어를 위한 루프
def control_loop():
    global data1, data2, data3
    while True:
        # Servo 1 control (각도 제어 서보 모터)
        if data1 is not None:
            servo1.angle = data1
            logging.info(f"Servo 1 angle set to {data1}")
            data1 = None  # 데이터 처리 후 초기화
        
        # Servo 2 control (연속 회전 서보 모터)
        if data2 is not None:
            if data2 == 0:
                servo2.value = None  # 중지
                logging.info("Servo 2 stopped")
            else:
                servo2.value = data2
                logging.info(f"Servo 2 set to speed {data2}")
            data2 = None  # 데이터 처리 후 초기화
        
        # Servo 3 control (연속 회전 서보 모터)
        if data3 is not None:
            if data3 == 0:
                servo3.value = None  # 중지
                logging.info("Servo 3 stopped")
            else:
                servo3.value = data3
                logging.info(f"Servo 3 set to speed {data3}")
            data3 = None  # 데이터 처리 후 초기화
        
        sleep(0.1)

# 제어 루프를 비차단식으로 실행
control_thread = Thread(target=control_loop)
control_thread.daemon = True
control_thread.start()

# 네트워크 루프 시작
client.loop_forever()
