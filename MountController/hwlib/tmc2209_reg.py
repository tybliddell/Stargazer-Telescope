#-----------------------------------------------------------------------
# this file contains:
# 1. hexadecimal address of the different registers
# 2. bitposition and bitmasks of the different values of each register
#
# Example:
# the register IOIN has the address 0x06 and the first bit shows
# whether the ENABLE (EN/ENN) Pin is currently HIGH or LOW
#-----------------------------------------------------------------------

# Addresses for registers within the TMC2209 driver. These registers are provided
# in the 2209 driver documentation (datasheet)
GCONF           =   0x00
GSTAT           =   0x01

# 8 bits (1 byte)
# Interface transmission counter. This register becomes incremented with each successful UART interface write
# access. Read out to check the serial transmission for lost data. Read accesses do not change the content.
# The counter wraps around from 255 to 0.
IFCNT           =   0x02

# 4 bits (1 nibble)
# SENDDELAY for read access (time until reply is sent):
#   0, 1:            8 bit times
#   2, 3:        3 * 8 bit times
#   4, 5:        5 * 8 bit times
#   6, 7:        7 * 8 bit times
#   8, 9:        9 * 8 bit times
#   10, 11:     11 * 8 bit times
#   12, 13:     13 * 8 bit times
#   14, 15:     15 * 8 bit times
SLAVECONF       =   0x03

IOIN            =   0x06
IHOLD_IRUN      =   0x10
TSTEP           =   0x12
# VACTUAL allows moving the motor by UART control.
#   It gives the motor velocity in +-(2^23)-1 [μsteps / t]
#      0: Normal operation. Driver reacts to STEP input.
#   /= 0: Motor moves with the velocity given by VACTUAL. Step pulses can be
#         monitored via INDEX output. The motor direction is controlled by the
#         sign of VACTUAL.
VACTUAL         =   0x22


TCOOLTHRS       =   0x14
SGTHRS          =   0x40
SG_RESULT       =   0x41
MSCNT           =   0x6A
CHOPCONF        =   0x6C
DRVSTATUS       =   0x6F

##################################
# GCONF bit locations
##################################

gconf_i_scale_analog      = 1<<0
# (Default reset val: OTP)
# set low for external sense resistor, set high for internal
gconf_internal_rsense     = 1<<1

# 0:    StealthChop PWM mode enabled (depending on
#       velocity thresholds). Initially switch from off to
#       on state while in stand still, only.
#
# 1: SpreadCycle mode enabled
#
# * set SPREAD Pin high to invert flag and switch between modes
gconf_en_spreadcycle      = 1<<2

# set high to invert motor direction
gconf_shaft               = 1<<3

# set high to use INDEX for overtemp prewarning
# set low to show first microstep position of sequencer
gconf_index_otpw          = 1<<4

# 0: output as selected by gconf_index_otpw
# 1: output shows step pulses from pulse generator one per step
gconf_index_step          = 1<<5

# 0: controls standstill current reduction
# 1: input function disabled
# bit pdn_disable(6) should be set high when using uart interface *(per tmc2209 datasheet)
gconf_pdn_disable         = 1<<6

# 0: Microstep resolution selected by pins MS1 & MS2
# 1: Microstep resolution selected by MSTEP reg
gconf_mstep_reg_select    = 1<<7

# 0: No filtering of STEP pulses
# 1: Software pulse generator optimization enabled
#    when fullstep frequency > 750Hz (roughly). TSTEP shows filtered step time values when active.
gconf_multistep_filter    = 1<<8

# 0: Normal operation
# 1: Enable analog test output on pin ENN (pull down
#    resistor off), ENN treated as enabled. IHOLD[1..0] selects the function of DCO: 0...2: T120, DAC, VDDH
#    Attention: Not for user, set to 0 for normal operation!
gconf_test_mode           = 1<<9

# GSTAT bit locations (ReWrite with 1 to clear respective flags)
# 1: Indicates that the IC has been reset since the last
#    read access to GSTAT
gstat_reset               = 1<<0


# 1: Indicates, that the driver has been shut down due to overtemperature or short circuit detection since
#    the last read access. Read DRV_STATUS for details. The flag can only be cleared when all error conditions
#    are cleared.
gstat_drv_err             = 1<<1

# 1: Indicates an undervoltage on the charge pump. The driver is disabled in this case. This flag is not
#    latched and thus does not need to be cleared.
gstat_uv_cp               = 1<<2

#CHOPCONF bit locations
chopconf_vsense              = 1<<17
chopconf_msres0              = 1<<24
chopconf_msres1              = 1<<25
chopconf_msres2              = 1<<26
chopconf_msres3              = 1<<27
chopconf_intpol              = 1<<28

#IOIN bit locations
ioin_io_enn           = 1<<0
ioin_ms1              = 1<<2
ioin_ms2              = 1<<3
ioin_diag             = 1<<4
ioin_pdn_uart         = 1<<6
ioin_step             = 1<<7
ioin_spread           = 1<<8
ioin_dir              = 1<<9
# bits 31..24
ioin_version          = 0xFF << 24

#DRVSTATUS bit locations
drvstat_stst                = 1<<31
drvstat_stealth             = 1<<30
drvstat_cs_actual           = 31<<16
drvstat_t157                = 1<<11
drvstat_t150                = 1<<10
drvstat_t143                = 1<<9
drvstat_t120                = 1<<8
drvstat_olb                 = 1<<7
drvstat_ola                 = 1<<6
drvstat_s2vsb               = 1<<5
drvstat_s2vsa               = 1<<4
drvstat_s2gb                = 1<<3
drvstat_s2ga                = 1<<2
drvstat_ot                  = 1<<1
drvstat_otpw                = 1<<0

#IHOLD_IRUN bit locations
ihir_ihold               = 31<<0
ihir_irun                = 31<<8
ihir_iholddelay          = 15<<16

#SGTHRS
sgthrs              = 255<<0

#others
mres_256 = 0
mres_128 = 1
mres_64 = 2
mres_32 = 3
mres_16 = 4
mres_8 = 5
mres_4 = 6
mres_2 = 7
mres_1 = 8