from gpiozero import OutputDevice
from time import sleep

# GPIO 핀 번호 설정
relay = OutputDevice(25, active_high=True, initial_value=False)  # 릴레이가 HIGH로 활성화됨

# 릴레이 제어 함수
def relay_on():
    relay.on()  # 릴레이 켜기
    print("Relay is ON")

def relay_off():
    relay.off()  # 릴레이 끄기
    print("Relay is OFF")

try:
    while True:
        relay_on()  # 릴레이 켜기
        sleep(2)  # 5초 대기
        relay_off()  # 릴레이 끄기
        sleep(2)  # 5초 대기

except KeyboardInterrupt:
    print("Program terminated")

