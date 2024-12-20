## UACV 라즈베리파이 기반 모니터링 및 제어

### 개요
라즈베리파이 5를 통해 2개의 pi camera를 통해 포신 및 주행 보조 카메라 구동<br>
MPU9250 기반의 방향, 가속도, 각속도 측정<br>
릴레이 기반의 솔레노이드 제어<br>
모니터링 및 제어 신호를 MQTT를 통해 서버와 통신<br>
가속도 및 각속도는 시리얼 통신을 통해 젯슨 오린으로 전송<br>

## Raspberry Pi 5 HW결선
![라즈베리파이_HW결선.png](./assets/라즈베리파이_HW결선.png)

## 사용 라이브러리
from gpiozero import OutputDevice <br>
from time import sleep <br>
import time <br>
import math <br>
import numpy as np <br>
import json <br>
from smbus2 import SMBus <br>
from mpu9250_jmdev.registers import * <br>
from mpu9250_jmdev.mpu_9250 import MPU9250 <br>
import threading <br>
import paho.mqtt.client as mqtt <br>
from picamera2 import Picamera2 <br>
import io <br>
import base64 <br>
import serial <br>
