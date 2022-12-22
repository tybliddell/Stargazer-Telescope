from hwlib import tmc2209_reg
import utime
from machine import UART
from config import DEBUG


# ENABLE PIN IS ACTIVE LOW!!!


def compute_crc8(datagram, initial_value=0):
    """Calculate crc8 parity bit for comms"""
    crc = initial_value
    # Iterate bytes in data
    for byte in datagram:
        # Iterate bits in byte
        for _ in range(0, 8):
            if (crc >> 7) ^ (byte & 0x01):
                crc = ((crc << 1) ^ 0x07) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
            # Shift to next bit
            byte = byte >> 1
    return crc


class TMC_UART:
    def __init__(self, uart: UART, mtr_id=0):
        uart.read(uart.any()) # Flush the buffer at the very beginning
        self.serial = uart
        self.mtr_id = mtr_id
        self.set_gconf(33)
        if DEBUG:
            print(f'Created motor: {mtr_id}')

    def set_gconf(self, data):
        self.read_reg(tmc2209_reg.GCONF)
        self.write_reg(tmc2209_reg.GCONF, data)
        self.read_reg(tmc2209_reg.GCONF)

    def wait(self, char_num):
        counter = 0
        while self.serial.any() < char_num and counter < 100:
            if DEBUG:
                print(f'Waiting: {counter}. So far: {self.serial.any()}')
            utime.sleep(0.01)
            counter += 1
        return counter < 100 

    def get_read_frame(self, register):
        read_frame = [0x55,
                      self.mtr_id,
                      register]
        read_frame.append(compute_crc8(read_frame))
        return bytes(read_frame)

    def read_reg(self, register):
        '''
        read specified register (check tmc2209_reg.py)
        retries until successfull
        '''
        if DEBUG:
            print(f'Reading: {register}')
        self.serial.read(self.serial.any()) # clear buffer
        while True:
            self.serial.write(self.get_read_frame(register))
            if self.wait(12):
                break
            utime.sleep(0.1)
            if DEBUG:
                print(f'Retrying reading: {register}')
            self.serial.read(self.serial.any())
        return self.serial.read(12)

    def get_write_frame(self, register, data):
        write_frame = [0x55,
                       self.mtr_id,
                       (register | 0x80),
                       (data >> 24) & 0xFF,
                       (data >> 16) & 0xFF,
                       (data >> 8) & 0xFF,
                       data & 0xFF]
        write_frame.append(compute_crc8(write_frame))
        return bytes(write_frame)

    def write_reg(self, register, data):
        """Sends a data packet of size 32(bits)(signed) to the motor driver"""
        if DEBUG:
            print(f'Writing {data} to {register}')
        self.serial.read(self.serial.any()) # clear buffer
        while True:
            self.serial.write(self.get_write_frame(register, data))
            if self.wait(8):
                break
            utime.sleep(0.1)
            if DEBUG:
                print(f'Retrying writing {data} to {register}')
            self.serial.read(self.serial.any())
        self.serial.read(8)
