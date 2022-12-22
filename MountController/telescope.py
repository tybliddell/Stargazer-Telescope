from collections import deque
from mount_controller import MountController

ALP_STAT = {
    'Success': 0x0,
    'PropertyNotImplementedException': 0x400,
    'InvalidValue': 0x401,
    'ValueNotSet': 0x402,
    'NotConnected': 0x407,
    'InvalidWhileParked': 0x408,
    'InvalidWhileSlaved': 0x409,
    'InvalidOperationException': 0x40B,
    'ActionNotImplementedException': 0x40C
}


class Telescope:
    def __init__(self, mount_controller):
        self.current_seq = -1
        self.last_response = ''
        self.last_status = ALP_STAT['Success']
        # Contains { 'req': 'ex_req', 'params': {} }
        self.queue = deque((), 16)
        self.target_declination = None
        self.target_rightascension = None
        self.mount_controller: MountController = mount_controller
        return

    def set_latitude(self, latitude):
        self.mount_controller._set_latitude(latitude)
        self.queue.append((self.mount_controller.home, []))
        return

    def altitude(self):
        self.last_response = str(self.mount_controller.sensor.get_angles().pitch)
        self.last_status = ALP_STAT['Success']
        return

    def azimuth(self):
        self.last_response = str(self.mount_controller.sensor.get_angles().yaw)
        self.last_status = ALP_STAT['Success']
        return

    def declination(self):
        # TODO check units
        self.last_response = self.mount_controller.get_current_dec()
        self.last_status = ALP_STAT['Success']
        return

    def rightascension(self, sidereal_time):
        # TODO check units
        self.last_response = self.mount_controller.get_current_ra(sidereal_time)
        self.last_status = ALP_STAT['Success']
        return

    def targetdeclination(self, declination=None):
        # GET request
        if declination is None:
            if self.target_declination is None:
                self.last_response = "TargetDeclination has not been set yet"
                self.last_status = ALP_STAT['InvalidOperationException']
            else:
                self.last_response = self.target_declination
                self.last_status = ALP_STAT['Success']
        # SET request
        else:
            self.target_declination = float(declination)
            self.last_response = ""
            self.last_status = ALP_STAT['Success']
        return

    def targetra(self, ra=None):
        # GET request
        if ra is None:
            if self.target_rightascension is None:
                self.last_response = "Target Right Ascension has not been set yet"
                self.last_status = ALP_STAT['InvalidOperationException']
            else:
                self.last_response = self.target_rightascension
                self.last_status = ALP_STAT['Success']
        # SET request
        else:
            self.target_rightascension = float(ra)
            self.last_response = ""
            self.last_status = ALP_STAT['Success']
        return

    def tracking(self, set_tracking=None):
        # GET request
        if set_tracking is None:
            self.last_response = self.mount_controller.is_tracking
            self.last_status = ALP_STAT['Success']
        # SET request
        else:
            self.last_response = ""
            self.last_status = ALP_STAT['Success']
            self.queue.append((self.mount_controller.tracking, [set_tracking]))
        return

    def slewing(self):
        self.last_response = self.mount_controller.is_slewing
        self.last_status = ALP_STAT['Success']
        return

    def abort_slew(self):
        # TODO: Implement if we have time after everything else
        if self.mount_controller.is_slewing:
            self.queue.appendleft(())
        self.last_response = ""
        self.last_status = ALP_STAT['Success']
        return

    def slewtoaltazasync(self, altitude, azimuth, sidereal_time):
        ra = self.mount_controller.calc_ra(sidereal_time, altitude, azimuth)
        dec = self.mount_controller.calc_dec(altitude, azimuth)
        self.queue.append((self.mount_controller.slew, [dec, ra, sidereal_time]))

    def slewtotargetasync(self, sidereal_time):
        if self.target_declination is None:
            self.last_response = "Target declination has not been set"
            self.last_status = ALP_STAT['ValueNotSet']
            return
        if self.target_rightascension is None:
            self.last_response = "Target right ascension has not been set"
            self.last_status = ALP_STAT['ValueNotSet']
        self.queue.append((self.mount_controller.slew, [self.target_declination, self.target_rightascension, sidereal_time]))

    def slewtocoordinatesasync(self, ra, dec, sidereal_time):
        self.target_rightascension = float(ra)
        self.target_declination = float(dec)
        self.queue.append((self.mount_controller.slew, [self.target_declination, self.target_rightascension, sidereal_time]))
