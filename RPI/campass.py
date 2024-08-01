import smbus
import math
import time
from gpiozero import LED

# MPU-9250 I2C address
MPU9250_ADDR = 0x68
AK8963_ADDR = 0x0C

# MPU-9250 registers
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43
MAG_XOUT_L = 0x03

# AK8963 registers
AK8963_CNTL = 0x0A
AK8963_ASAX = 0x10

# Initialize I2C bus
bus = smbus.SMBus(1)

# Initialize LED (you can use this to indicate calibration or readings)
led = LED(17)

def init_mpu9250():
    # Wake up MPU-9250
    bus.write_byte_data(MPU9250_ADDR, 0x6B, 0x00)
    time.sleep(0.1)
    # Enable magnetometer
    bus.write_byte_data(MPU9250_ADDR, 0x37, 0x02)
    time.sleep(0.1)
    # Set magnetometer to 16-bit resolution, 100Hz update rate
    bus.write_byte_data(AK8963_ADDR, AK8963_CNTL, 0x16)
    time.sleep(0.1)

def read_mag_data():
    # Set magnetometer to single measurement mode
    bus.write_byte_data(AK8963_ADDR, AK8963_CNTL, 0x01)
    time.sleep(0.01)
    
    # Read magnetometer data
    data = bus.read_i2c_block_data(AK8963_ADDR, MAG_XOUT_L, 7)
    
    # Convert to 16-bit signed integers
    x = (data[1] << 8) | data[0]
    y = (data[3] << 8) | data[2]
    z = (data[5] << 8) | data[4]
    
    # Convert to signed values
    x = x - 65536 if x > 32767 else x
    y = y - 65536 if y > 32767 else y
    z = z - 65536 if z > 32767 else z
    
    return x, y, z

def calculate_heading(x, y):
    heading = math.atan2(y, x)
    
    # Convert to degrees
    heading_deg = math.degrees(heading)
    
    # Normalize to 0-360
    if heading_deg < 0:
        heading_deg += 360
    
    return heading_deg

def get_direction(heading):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(heading / 45) % 8
    return directions[index]

def main():
    init_mpu9250()
    
    print("Calibrating magnetometer. Please rotate the device slowly...")
    led.on()
    time.sleep(5)  # Give time for manual calibration
    led.off()
    
    print("Calibration complete. Starting compass readings.")
    
    while True:
        try:
            mag_x, mag_y, mag_z = read_mag_data()
            heading = calculate_heading(mag_x, mag_y)
            direction = get_direction(heading)
            print(f"Heading: {heading:.2f}° ({direction})")
            led.toggle()
            time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
