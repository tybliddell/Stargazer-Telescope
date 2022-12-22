from utime import sleep
from machine import I2C
from ucollections import namedtuple
from config import DEBUG

ACC_OFFSET_X = 0
ACC_OFFSET_Y = 3
ACC_OFFSET_Z = 5

MAG_OFFSET_X = 800
MAG_OFFSET_Y = 100
MAG_OFFSET_Z = 64000

GYRO_OFFSET_X = 0
GYRO_OFFSET_Y = 0
GYRO_OFFSET_Z = 0

ACC_RADIUS = 0
MAG_RADIUS = 700

class BNO055:
    def __init__(self, i2c_conn=None, add=0x28):
        self.euler_angles = None
        self.yaw_offset = 0
        try:
            if i2c_conn is None:
                print("No I2C connection provided, Must have a connection for the device to work")
            else:
                self.i2c = i2c_conn
                self.add = add
                # initialize the sensor with bytes 107, 0
                while self.Check_status() != 0x0F:
                    print("Error during self test")
                    sleep(5)
            # start in NDOF, then switch to config to write offset/radius
            self.set_ndof_mode()
            self.set_config_mode()
            self.set_acc_offset_x()
            self.set_acc_offset_y()
            self.set_acc_offset_z()
            self.set_gyro_offset_x()
            self.set_gyro_offset_y()
            self.set_gyro_offset_z()
            self.set_mag_offset_x()
            self.set_mag_offset_y()
            self.set_mag_offset_z()
            self.set_acc_radius()
            self.set_mag_radius()
            self.set_ndof_mode()
        except Exception as e:
            print(f"error in init: {e}")
            return None

    def _read_from_mem(self, addr, size):
        return self.i2c.readfrom_mem(self.add, addr, size)
    
    def _write_to_mem(self, addr, data):
        return self.i2c.writeto_mem(self.add, addr, data.to_bytes(1, 'little'))

    def Check_status(self):
        """
        Check the status  of the self test.
        Should be called after power on, or after built in self test.
        """
        return self._read_from_mem(0x36, 1)[0]

    def get_angles(self):
        EulerAngles = namedtuple('EulerAngles', ['roll', 'pitch', 'yaw'])
        try:
            self.euler_angles = EulerAngles(self.get_roll(), self.get_pitch(), self.get_yaw())
        except:
            pass
        return self.euler_angles

    def get_roll(self):
        roll = self._read_from_mem(0x1E, 2)
        return self.convert_to_degrees(int.from_bytes(roll, "little"))

    def get_pitch(self):
        pitch = self._read_from_mem(0x1C, 2)
        return -self.convert_to_degrees(int.from_bytes(pitch, "little"))

    def get_yaw(self):
        yaw = self._read_from_mem(0x1A, 2)
        temp = self.convert_to_degrees(int.from_bytes(yaw, "little"))
        return (360 - self.yaw_offset + temp) % 360

    def fucking_garbage_hack(self) -> bool:
        garb = self.get_yaw()
        return garb < 90 or garb > 270

    def set_yaw_offset(self):
        self.yaw_offset = self.get_yaw()

    def get_calib_status(self):
        calib = self._read_from_mem(0x35, 1)
        return int.from_bytes(calib, "little")

    def convert_to_degrees(self, val: int) -> float:
        if val > 2**15:
            val -= 2**16
        return float(val / 16)
    #########################
    # getters for offset and radius 
    def get_acc_offset_x(self):
        offset_x = self._read_from_mem(0x55, 2)
        return int.from_bytes(offset_x, "little")
    
    def get_acc_offset_y(self):
        offset_y = self._read_from_mem(0x57, 2)
        return int.from_bytes(offset_y, "little")

    def get_acc_offset_z(self):
        offset_z = self._read_from_mem(0x59, 2)
        return int.from_bytes(offset_z, "little")

    def get_mag_offset_x(self):
        offset_x = self._read_from_mem(0x5B, 2)
        return int.from_bytes(offset_x, "little")

    def get_mag_offset_y(self):
        offset_y = self._read_from_mem(0x5D, 2)
        return int.from_bytes(offset_y, "little")
    
    def get_mag_offset_z(self):
        offset_z = self._read_from_mem(0x5F, 2)
        return int.from_bytes(offset_z, "little")

    def get_gyro_offset_x(self):
        offset_x = self._read_from_mem(0x61, 2)
        return int.from_bytes(offset_x, "little")

    def get_gyro_offset_y(self):
        offset_y = self._read_from_mem(0x63, 2)
        return int.from_bytes(offset_y, "little")

    def get_gyro_offset_z(self):
        offset_z = self._read_from_mem(0x65, 2)
        return int.from_bytes(offset_z, "little")

    def get_acc_radius(self):
        radius = self._read_from_mem(0x67, 2)
        return int.from_bytes(radius, "little")

    def get_mag_radius(self):
        radius = self._read_from_mem(0x69, 2)
        return int.from_bytes(radius, "little")        
    # getters for offset and radius 
    #########################

    #########################
    # setters for offset and radius
    def set_acc_offset_x(self):
        self._write_to_mem(0x55, ACC_OFFSET_X)
    
    def set_acc_offset_y(self):
        self._write_to_mem(0x57, ACC_OFFSET_Y)

    def set_acc_offset_z(self):
        self._write_to_mem(0x59, ACC_OFFSET_Z)

    def set_mag_offset_x(self):
        self._write_to_mem(0x5B, MAG_OFFSET_X)

    def set_mag_offset_y(self):
        self._write_to_mem(0x5D, MAG_OFFSET_Y)

    def set_mag_offset_z(self):
        self._write_to_mem(0x5F, MAG_OFFSET_Z)

    def set_gyro_offset_x(self):
        self._write_to_mem(0x61, GYRO_OFFSET_X)

    def set_gyro_offset_y(self):
        self._write_to_mem(0x63, GYRO_OFFSET_Y)

    def set_gyro_offset_z(self):
        self._write_to_mem(0x65, GYRO_OFFSET_Z)

    def set_acc_radius(self):
        self._write_to_mem(0x67, ACC_RADIUS)

    def set_mag_radius(self):
        self._write_to_mem(0x69, MAG_RADIUS) 
    # setters for offset and radius
    #########################

    def set_config_mode(self):
        mode = self.i2c.readfrom_mem(self.add, 0x3D, 1)
        temp = int.from_bytes(mode, "little")
        temp &= (0b1111 << 4)
        self._write_to_mem(0x3D, temp)

    def set_ndof_mode(self):
        mode = self.i2c.readfrom_mem(self.add, 0x3D, 1)
        temp = int.from_bytes(mode, "little")
        temp |= 12
        self._write_to_mem(0x3D, temp)