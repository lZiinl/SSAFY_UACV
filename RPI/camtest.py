from picamera2 import Picamera2
import time

# 첫 번째 카메라 설정
picam2_1 = Picamera2(camera_num=0)
picam2_1.start()
time.sleep(2)
picam2_1.capture_file("image1.jpg")
picam2_1.stop()

# 두 번째 카메라 설정
picam2_2 = Picamera2(camera_num=1)
picam2_2.start()
time.sleep(2)
picam2_2.capture_file("image2.jpg")
picam2_2.stop()

