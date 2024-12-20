import serial
import time

ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)

while True:
    ser.write(b'Hello from Raspberry Pi\n')
    time.sleep(1)

