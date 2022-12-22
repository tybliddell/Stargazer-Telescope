from machine import Pin, I2C  # , SPI SPI not needed so far
from hwlib.BNO055 import BNO055
from utime import sleep

# finding the address for the devices currently connected to the bus. Find a better way to do this


def find_devices(i2c_connection, screen=None, gyro=None):
    devices = i2c_connection.scan()
    # save addresses that are known only for the ones we are interested in
    if devices:
        for d in devices:
            print("Device add:", hex(d))
    else:
        print("No devices seen!")
        print("Check connections and try again")


Pins = {"switch": 18, "switch2": 19, "led": 25, "enable": 2, "spi": 0, "miso": 4,
        "mosi": 7, "sck": 6, "csn": 5, "ce": 12, "sda": 0, "scl": 1, "uart_tx": 16, "uart_rx": 17,
        "calib_mag": 16, "calib_accel": 17, "calib_gyro": 18, "calib_sys": 19 }
i2c_addresses = {"nina": 0x50, "screen": 0x3C}
i2c = I2C(0, scl=Pin(Pins["scl"], mode=Pin.OUT, pull=Pin.PULL_UP), sda=Pin(
    Pins["sda"], mode=Pin.OUT, pull=Pin.PULL_UP), freq=400000)

led_accel = Pin(Pins['calib_accel'], mode=Pin.OUT)
led_gyro = Pin(Pins['calib_gyro'], mode=Pin.OUT)
led_mag = Pin(Pins['calib_mag'], mode=Pin.OUT)
led_sys = Pin(Pins['calib_sys'], mode=Pin.OUT)

led_accel.off()
led_gyro.off()
led_mag.off()
led_sys.off()

driver = BNO055(i2c_conn=i2c)

while True:
    print(f'roll: {driver.get_roll()}')
    print(f'pitch: {driver.get_pitch()}')
    print(f'yaw: {driver.get_yaw()}')
    
    calib = driver.get_calib_status()
    print(f'calib_status: {calib:08b}')
    print()
    if calib & 0b11 == 0b11:
        led_mag.on()
    else:
        led_mag.off()
    if calib & (0b11 << 2) == (0b11 << 2):
        led_accel.on()
    else:
        led_accel.off()
    if calib & (0b11 << 4) == (0b11 << 4):
        led_gyro.on()
    else:
        led_gyro.off()
    if calib & (0b11 << 6) == (0b11 << 6):
        led_sys.on()
    else:
        led_sys.off()
    if (calib & 0b11111111 == 0b11111111):
        driver.set_config_mode()
        print('---OFFSETS---')
        print(f'x_acc: {driver.get_acc_offset_x()}')
        print(f'y_acc: {driver.get_acc_offset_y()}')
        print(f'z_acc: {driver.get_acc_offset_z()}')
        print(f'x_mag: {driver.get_mag_offset_x()}')
        print(f'y_mag: {driver.get_mag_offset_y()}')
        print(f'z_mag: {driver.get_mag_offset_z()}')
        print(f'x_gyro: {driver.get_gyro_offset_x()}')
        print(f'y_gyro: {driver.get_gyro_offset_y()}')
        print(f'z_gyro: {driver.get_gyro_offset_z()}')

        print('---RADIUS---')
        print(f'acc_radius: {driver.get_acc_radius()}')
        print(f'mag_radius: {driver.get_mag_radius()}')
        break

    sleep(.2)