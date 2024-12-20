import smbus
import math
import time

# MPU6050 레지스터 주소
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

# I2C 버스 초기화
bus = smbus.SMBus(1)
device_address = 0x68

# MPU6050 초기화 함수
def mpu_init():
    bus.write_byte_data(device_address, SMPLRT_DIV, 7)
    bus.write_byte_data(device_address, PWR_MGMT_1, 1)
    bus.write_byte_data(device_address, CONFIG, 0)
    bus.write_byte_data(device_address, GYRO_CONFIG, 24)
    bus.write_byte_data(device_address, ACCEL_CONFIG, 0)
    bus.write_byte_data(device_address, INT_ENABLE, 1)

# MPU6050 데이터 읽기 함수
def read_raw_data(addr):
    high = bus.read_byte_data(device_address, addr)
    low = bus.read_byte_data(device_address, addr + 1)
    value = ((high << 8) | low)
    if value > 32768:
        value = value - 65536
    return value

# 각도 계산 함수
def calculate_angles():
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)
    
    acc_x_angle = math.atan2(acc_y, acc_z) * 180 / math.pi
    acc_y_angle = math.atan2(acc_z, acc_x) * 180 / math.pi
    acc_z_angle = math.atan2(acc_x, acc_y) * 180 / math.pi
    
    return acc_x_angle, acc_y_angle, acc_z_angle, gyro_x, gyro_y, gyro_z

# 컴플리멘터리 필터 함수
def complementary_filter(acc_angle, gyro_rate, prev_angle, dt, alpha=0.98):
    return alpha * (prev_angle + gyro_rate * dt) + (1 - alpha) * acc_angle

# 메인 함수
if __name__ == "__main__":
    mpu_init()
    print("MPU6050 초기화 완료")
    
    prev_x_angle = 0
    prev_y_angle = 0
    prev_z_angle = 0
    prev_time = time.time()
    
    while True:
        acc_x_angle, acc_y_angle, acc_z_angle, gyro_x, gyro_y, gyro_z = calculate_angles()
        
        curr_time = time.time()
        dt = curr_time - prev_time
        prev_time = curr_time
        
        gyro_x_rate = gyro_x / 131.0  # 131 LSB/deg/s
        gyro_y_rate = gyro_y / 131.0  # 131 LSB/deg/s
        gyro_z_rate = gyro_z / 131.0  # 131 LSB/deg/s
        
        filtered_x_angle = complementary_filter(acc_x_angle, gyro_x_rate, prev_x_angle, dt)
        filtered_y_angle = complementary_filter(acc_y_angle, gyro_y_rate, prev_y_angle, dt)
        filtered_z_angle = complementary_filter(acc_z_angle, gyro_z_rate, prev_z_angle, dt)
        
        prev_x_angle = filtered_x_angle
        prev_y_angle = filtered_y_angle
        prev_z_angle = filtered_z_angle
        
        print(f"X 각도: {filtered_x_angle:.2f} | Y 각도: {filtered_y_angle:.2f} | Z 각도: {filtered_z_angle:.2f}")
        
        time.sleep(0.1)

