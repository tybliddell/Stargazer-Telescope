from collections import namedtuple

EXPOSURES = [
    [0.1] * 2,  # Potato
    [0.1] * 2,  # Okay
    [0.1] * 2,  # Good
    [0.1] * 2  # Great
]

GPS = namedtuple('GPS', ['latitude', 'longitude', 'elevation'])
DEFAULT_GPS = GPS(40.8921, -111.0155, 1449)
