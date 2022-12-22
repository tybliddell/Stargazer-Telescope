import serial
from datetime import datetime
import os
from config import GPS
from decimal import Decimal

SWARM_MESSAGE_RATE = 30


def nmea(nmea_message: str) -> str:
    """Create the NMEA message to send

    Do not include $, *, the checksum, or a \n in the nmea_message
    """
    checksum = 0
    for char in nmea_message:
        checksum ^= ord(char)
    return f'${nmea_message}*{checksum:02x}\n'


class SwarmReader:
    def __init__(self) -> None:
        # ttyAMA1 tx is pin 27, rx might be 28
        self.uart = serial.Serial(port="/dev/ttyAMA1", baudrate=115200)
        return

    # Set rates for both date/time and geospatial info
    def set_rates(self):
        print('[swarm-status] setting rates for swarm')
        while True:
            self.uart.write(bytes(nmea(f'DT {SWARM_MESSAGE_RATE}'), 'utf-8'))
            message = self.uart.readline().decode('utf-8')
            if message == '$DT OK*34\n':
                break
        while True:
            self.uart.write(bytes(nmea(f'GN {SWARM_MESSAGE_RATE}'), 'utf-8'))
            message = self.uart.readline().decode('utf-8')
            if message == '$GN OK*2d\n':
                break
        while True:
            self.uart.write(bytes(nmea(f'RT {SWARM_MESSAGE_RATE}'), 'utf-8'))
            message = self.uart.readline().decode('utf-8')
            if message == '$RT OK*22\n':
                break
        print('[swarm-status] sucessfully set DT, GN and RT rates')
        self.read_loop()

    def read_loop(self) -> GPS:
        set_time = False
        gps = None
        print('[swarm-status] beginning read loop')
        while gps is None or not set_time:
            message = self.uart.readline().decode('utf-8')
            if message.startswith('$DT'):
                if 'V' not in message:
                    continue
                curr_time = message.split(' ')[1].split(',')[0]
                datetime_obj = datetime.strptime(curr_time, '%Y%m%d%H%M%S')
                if not set_time:
                    os.system(f"sudo date -us '{str(datetime_obj).split('.')[0]}'")
                    print(f"[swarm-status] setting system time: {str(datetime_obj).split('.')[0]}")
                    set_time = True
                print(f"[swarm-status] swarm time: {str(datetime_obj).split('.')[0]}, system time: {datetime.now()}")
            elif message.startswith('$GN'):
                message = message.split(' ')[1].split('*')[0]
                latitude, longitude, altitude = message.split(',')[0:3]
                print(f"[swarm-status] Obtained GN. Lat: {latitude}. Lon: {longitude}. Elev: {altitude}")
                gps = GPS(Decimal(latitude), Decimal(longitude), Decimal(altitude))
            elif message.startswith('$RT'):
                message = message.split(' ')[1].split('*')[0]
                if message == 'OK':
                    continue
                rssi = {keyval.split('=')[0]: keyval.split('=')[1] for keyval in message.split(',')}['RSSI']
                print(f'[swarm-status] current signal strength: {rssi}')
            elif '$M138 BOOT,RUNNING*2a' in message:
                print('[swarm-status] Swarm restart detected, setting rates again')
                self.set_rates()
            else:
                print(f'[swarm-status] received message from Swarm: {message}')
        return gps
