# -*- coding: utf-8 -*-
from gpiozero import RotaryEncoder, Button
from signal import pause

# 로터리 인코더 및 버튼 핀 정의
CLK_PIN = 18  # CLK 핀
DT_PIN = 15   # DT 핀
SW_PIN = 14   # SW 핀

# 로터리 인코더 초기화
rotor = RotaryEncoder(CLK_PIN, DT_PIN, max_steps=0)
rot_btn = Button(SW_PIN)

# 로터리 인코더 회전 이벤트 핸들러
def change_rot():
    rotations = rotor.steps / 20.0  # 한 바퀴에 20 스텝으로 가정, 필요에 따라 조정
    print(f"Steps: {rotor.steps} | Rotations: {rotations:.2f}")

# 스위치 버튼 클릭 이벤트 핸들러
def click_btn():
    rotor.steps = 0  # 카운터 리셋
    print("Button pressed! Counter reset to 0.")

# 이벤트 핸들러 등록
rotor.when_rotated = change_rot
rot_btn.when_pressed = click_btn

print("Rotary Encoder and Button Test")
pause()  # 이벤트를 계속 감지하도록 대기
