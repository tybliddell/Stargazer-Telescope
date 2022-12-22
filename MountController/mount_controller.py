from math import sin, cos, tan, asin, atan, degrees, radians
import utime
from machine import UART, Pin, I2C, PWM
from ucollections import namedtuple
from config import PINS, DEBUG
from hwlib import tmc2209_uart, tmc2209_reg
from hwlib.BNO055 import BNO055

DEGREES_PER_SIDEREAL_HOUR = 15.04
PULSES_PER_DEGREE = 152


def setup_motors():
    if DEBUG:
        print('Setting up motors')
    Motors = namedtuple('Motors', ['ra', 'ra_disable', 'dec', 'dec_disable', 'ra_step', 'ra_step_dir'])
    motor_uart = UART(1, 115200, rx=Pin(PINS['motor_uart_rx'], Pin.IN), tx=Pin(PINS['motor_uart_tx'], Pin.OUT),
                      parity=0, timeout=2000)
    if DEBUG:
        print('Successfully set up uart')
    dec_motor = tmc2209_uart.TMC_UART(motor_uart, 0)
    dec_motor_disable = Pin(PINS["dec_motor_enable"], mode=Pin.OUT, pull=Pin.PULL_DOWN)
    ra_motor = tmc2209_uart.TMC_UART(motor_uart, 1)
    ra_motor_disable = Pin(PINS["ra_motor_enable"], mode=Pin.OUT, pull=Pin.PULL_DOWN)
    ra_step = Pin(PINS["ra_motor_step"], mode=Pin.OUT, pull=Pin.PULL_DOWN) #PWM(Pin(PINS["ra_motor_step"]), freq=1000, duty=0)
    ra_step_dir = Pin(PINS["ra_motor_step_dir"], mode=Pin.OUT)
    ra_step.off()
    ra_step_dir.off()
    dec_motor_disable.off()
    ra_motor_disable.on()
    return Motors(ra_motor, ra_motor_disable, dec_motor, dec_motor_disable, ra_step, ra_step_dir)


def setup_sensor():
    sensor_i2c = I2C(0, scl=Pin(PINS["sensor_i2c_scl"], mode=Pin.OUT, pull=Pin.PULL_UP),
                     sda=Pin(PINS["sensor_i2c_sda"], mode=Pin.OUT, pull=Pin.PULL_UP), freq=400000)
    return BNO055(sensor_i2c)


class MountController:
    def __init__(self, oled):
        if DEBUG:
            print('creating mount controller')
        oled.set_text_and_show('Setting up motors', 1)
        self.motors = setup_motors()
        self.slew_speed_dec = 100
        self.slew_speed_ra = 5000 # hz of pulses of pain
        self.current_slew_dir = 1
        self.tracking_speed = 1  # Needs to be 15 degrees per hour
        self.ra_half_period = 100
        self.accuracy = 0.05
        self.switch = Pin(PINS['switch'], mode=Pin.IN, pull=Pin.PULL_DOWN)
        self.holo = Pin(PINS['holo'], mode=Pin.IN, pull=Pin.PULL_UP)
        oled.set_text_and_show('Setting up sensor', 1)
        self.sensor = setup_sensor()
        self.latitude = None
        self.is_tracking = False
        self.is_slewing = False
        self.oled = oled
        oled.set_text_and_show('MountController created', 1)

    def _set_latitude(self, latitude):
        self.latitude = radians(float(latitude))

    def calc_dec(self, altitude, azimuth):
        calc_value = 90 - degrees(self.latitude) + altitude
        # alt = radians(altitude)
        # az = radians((azimuth + 180) % 360)
        # calc_value = degrees(asin(sin(self.latitude) * sin(alt) - cos(self.latitude) * cos(alt) * -1))
        # if DEBUG:
        #     print(f'alt-deg: {altitude}, az: {azimuth}')
        #     print(f'alt-rad: {alt}, az: {az}, calc: {calc_value}')
        return calc_value

    def calc_ra(self, sidereal_time, altitude, azimuth):
        alt = radians((90+altitude-degrees(self.latitude)) % 90) # test
        az = radians((azimuth + 180) % 360)
        local_hour_angle = degrees(atan(sin(az) / (cos(az) * sin(self.latitude) + tan(alt) * cos(self.latitude))))
        if DEBUG:
            # print(f'alt-deg: {degrees(alt)}, az-deg: {degrees(az)}')
            # print(f'Sidereal Time: {sidereal_time * 15}. Local Hour Angle: {local_hour_angle}')
            print(f'{sidereal_time*15-local_hour_angle},{local_hour_angle},{alt},{az},{self.latitude}')
            # TODO REMOVE!!!!!
            utime.sleep(.01)
        return (sidereal_time * 15) - local_hour_angle

    def get_current_dec(self):
        euler_angles = self.sensor.get_angles()
        return self.calc_dec(euler_angles.pitch, euler_angles.yaw)

    def get_current_ra(self, sidereal_time):
        euler_angles = self.sensor.get_angles()
        return self.calc_ra(sidereal_time, euler_angles.pitch, euler_angles.yaw)

    def _accurate(self, current, goal):
        return goal - self.accuracy < current < goal + self.accuracy

    def _calculate_direction_dec(self, current, target):
        return -1 if current < target else 1

    def _calculate_direction_ra(self, current, target):
        # TODO: We don't know how to do this yet figure it out
        if abs(current - target) > 180:
            return -1
        return 1

    def _set_ra_speed(self, direction, speed):
        self.motors.ra_disable.off()
        self.motors.ra.write_reg(tmc2209_reg.VACTUAL, speed * direction)
        if not speed:
            self.motors.ra_disable.on()

    def _send_ra_pulses(self, direction, num_pulses):
        self.oled.set_text_and_show(f'pulsing ra: dir {direction} num {num_pulses}', 1)
        if DEBUG:
            print(f'pulsing ra: dir {direction} num {num_pulses} wait_us {self.ra_half_period}')
        self.motors.ra_disable.off()
        if direction:
            print('setting high')
            self.motors.ra_step_dir.on()
        else:
            print('setting low')
            self.motors.ra_step_dir.off()

        #utime.sleep(1)
        for i in range(num_pulses):
            self.motors.ra_step.on()
            utime.sleep_us(self.ra_half_period)
            self.motors.ra_step.off()
            utime.sleep_us(self.ra_half_period)
        
        self.motors.ra_step_dir.off()
        self.motors.ra_disable.on()

    def _slew_to_target_dec(self, target):
        prev_drive_direction = 0
        while not self._accurate((current := self.get_current_dec()), target):
            if DEBUG:
                print(f'DEC - goal: {target}, current: {current}')
            self.oled.set_text_and_show(f'curr: {current}, t: {target}', 1)
            direction = self._calculate_direction_dec(current, target)
            if direction != prev_drive_direction:
                self.motors.dec.write_reg(tmc2209_reg.VACTUAL, self.slew_speed_dec * direction)
                prev_drive_direction = direction
        self.motors.dec.write_reg(tmc2209_reg.VACTUAL, 0)

    def _slew_to_target_ra(self, target, sidereal_time):
        st_deg = (sidereal_time * DEGREES_PER_SIDEREAL_HOUR + 180) % 360
        offset_deg = (target * DEGREES_PER_SIDEREAL_HOUR) - st_deg
        num_pulses = PULSES_PER_DEGREE * offset_deg
        print(f'offset: {offset_deg}, num_pulses: {num_pulses}')
        self._send_ra_pulses(1 if offset_deg < 0 else 0, abs(num_pulses))

    def _slew_to_altitude(self, target):
        prev_drive_direction = 0
        print('slewing to altitude')
        while not self._accurate((current := self.sensor.get_angles().pitch), target):
            if DEBUG:
                print(f'ALT - goal: {target}, current: {current}')
            self.oled.set_text_and_show(f'curr: {current}, t: {target}', 1)
            direction = -1 if current < target else 1
            if direction != prev_drive_direction:
                self.motors.dec.write_reg(tmc2209_reg.VACTUAL, self.slew_speed_dec * direction)
                prev_drive_direction = direction
        self.motors.dec.write_reg(tmc2209_reg.VACTUAL, 0)        

    def slew(self, target_dec, target_ra, sidereal_time):
        self.is_slewing = True
        was_tracking = self.is_tracking
        self.tracking(False)
        self.return_to_home()
        self._slew_to_target_dec(target_dec)
        self._slew_to_target_ra(target_ra, sidereal_time)
        self.is_slewing = False
        if was_tracking:
            self.tracking(True)

    def tracking(self, track):
        self.is_tracking = track
        self._set_ra_speed(-1, track * self.tracking_speed)

    def home(self):
        # drive ra motor for one sec
        self.motors.ra_disable.off()
        self.motors.ra.write_reg(tmc2209_reg.VACTUAL, -self.slew_speed_ra)
        utime.sleep(1)
        self.motors.ra.write_reg(tmc2209_reg.VACTUAL, 0)
        self.motors.ra_disable.on()

        self.return_to_home()
        # Slew until latitude
        self.oled.set_text_and_show(f'slewing to 90-lat: {90-degrees(self.latitude)}', 1)
        if DEBUG:
            print('homing')
        self._slew_to_altitude(90-degrees(self.latitude))
        while True:
            euler_angles = self.sensor.get_angles()
            self.oled.set_text_and_show(f'desired: 0 current: {euler_angles.pitch}', 1)
            if self.switch.value() == 1 and self._accurate(euler_angles.pitch, 0):
                break
            elif self.switch.value() == 1:
                self.oled.set_text_and_show('try again :(', 1)
                utime.sleep(.1)
        # Slew to look at north star
        self._slew_to_altitude(degrees(self.latitude) - 1)
        self.sensor.set_yaw_offset()
        if DEBUG:
            print(f'offset: {self.sensor.yaw_offset}, curr: {self.sensor.get_yaw()}')
        self.oled.set_text_and_show('homed', 1)
        return

    def return_to_home(self):
        # spin ra motor until we reach holo
        self.oled.set_text_and_show('returning to home', 1)
        if DEBUG:
            print('returning to home')
        if self.holo.value() != 0:
            self.motors.ra_disable.off()
            self.motors.ra.write_reg(tmc2209_reg.VACTUAL, self.slew_speed_ra * self.current_slew_dir)
            self.current_slew_dir *= -1
            while self.holo.value() != 0:
                utime.sleep(0.01)
        self.motors.ra.write_reg(tmc2209_reg.VACTUAL, 0)
        self.motors.ra_disable.on()