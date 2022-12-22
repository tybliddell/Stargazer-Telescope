DEBUG = True

SUPPORTED_ACTIONS = {}

ALPACA_ERROR_CODES = { 
    'PropertyNotImplementedException': 0x400,
    'MethodNotImplemented': 0x400, 
    'InvalidValue': 0x401, 
    'ValueNotSet': 0x402, 
    'NotConnected': 0x407, 
    'InvalidWhileParked': 0x408, 
    'InvalidWhileSlaved': 0x409, 
    'InvalidOperationException': 0x40B, 
    'ActionNotImplementedException': 0x40C,
    'DriverException': 0x500,
}