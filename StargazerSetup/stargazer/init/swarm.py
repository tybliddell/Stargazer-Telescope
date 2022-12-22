from queue import Queue
import serial
from datetime import datetime
import os

# TODO change this back
SWARM_MESSAGE_RATE = 3

class SwarmSetup():
    def __init__(self) -> None:
        # ttyAMA1 tx is pin 27, rx might be 28
        self.uart = serial.Serial(port="/dev/ttyAMA1", baudrate=115200)
        return

    # Set rates for both date/time and geospatial info
    def set_rates(self):
        while True:
            self.uart.write(bytes(self.nmea(f'DT {SWARM_MESSAGE_RATE}'), 'utf-8'))
            try:
                message = self.uart.readline().decode('utf-8')
                if message == '$DT OK*34\n':
                    break
            except UnicodeDecodeError:
                print('[init-error] receive error, may be dismissed')
        while True:
            self.uart.write(bytes(self.nmea(f'GN {SWARM_MESSAGE_RATE}'), 'utf-8'))
            try:
                message = self.uart.readline().decode('utf-8')
                if message == '$GN OK*2d\n':
                    break
            except UnicodeDecodeError:
                print('[init-error] receive error, may be dismissed')
        while True:
            self.uart.write(bytes(self.nmea(f'RT {SWARM_MESSAGE_RATE}'), 'utf-8'))
            try:
                message = self.uart.readline().decode('utf-8')
                if message == '$RT OK*22\n':
                    break
            except UnicodeDecodeError:
                print('[init-error] receive error, may be dismissed')
            return
    
    # Wait until we have received DT and GN
    def get_dt_gn(self):
        set_time = set_geo = False
        while not set_time or not set_geo:
            try:
                message = self.uart.readline().decode('utf-8')
                print(f'[init-status] swarm message: {message.strip()}')
                if not set_time and message.startswith('$DT'):
                    if 'V' not in message:
                        continue
                    curr_time = message.split(' ')[1].split(',')[0]
                    datetime_obj = datetime.strptime(curr_time, '%Y%m%d%H%M%S')
                    os.system(f"sudo date -us '{str(datetime_obj).split('.')[0]}'")
                    print(f"[init-status] got DT, setting system time: {str(datetime_obj).split('.')[0]}")
                    set_time = True
                if message.startswith('$GN'):
                    message = message.split(' ')[1].split('*')[0]
                    latitude, longitude, altitude, course, speed = message.split(',')
                    data = { 'latitude': latitude, 'longitude': longitude, 'elevation': altitude, 'course': course, 'speed': speed }
                    print(f'[init-status] got GN, latitude: {data["latitude"]}, longitude: {data["longitude"]}, elevation: {data["elevation"]}')
                    set_geo = True
                if set_time and set_geo:
                    return data
            except UnicodeDecodeError:
                print('[init-error] receive error, may be dismissed')
    
    # Create the NMEA message to send
    # Do not include $, *, the checksum, or a \n in the nmea_message
    def nmea(self, nmea_message: str) -> str:
        checksum = 0
        for char in nmea_message:
            checksum ^= ord(char)       
        return f'${nmea_message}*{checksum:02x}\n'