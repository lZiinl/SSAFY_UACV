# -*- coding: utf-8 -*-
from gpiozero import RotaryEncoder, Button
from signal import pause

# ���͸� ���ڴ� �� ��ư �� ����
CLK_PIN = 18  # CLK ��
DT_PIN = 15   # DT ��
SW_PIN = 14   # SW ��

# ���͸� ���ڴ� �ʱ�ȭ
rotor = RotaryEncoder(CLK_PIN, DT_PIN, max_steps=0)
rot_btn = Button(SW_PIN)

# ���͸� ���ڴ� ȸ�� �̺�Ʈ �ڵ鷯
def change_rot():
    rotations = rotor.steps / 20.0  # �� ������ 20 �������� ����, �ʿ信 ���� ����
    print(f"Steps: {rotor.steps} | Rotations: {rotations:.2f}")

# ����ġ ��ư Ŭ�� �̺�Ʈ �ڵ鷯
def click_btn():
    rotor.steps = 0  # ī���� ����
    print("Button pressed! Counter reset to 0.")

# �̺�Ʈ �ڵ鷯 ���
rotor.when_rotated = change_rot
rot_btn.when_pressed = click_btn

print("Rotary Encoder and Button Test")
pause()  # �̺�Ʈ�� ��� �����ϵ��� ���
