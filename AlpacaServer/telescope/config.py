# Imports

# Everything below this point is TELESCOPE CONTSANTS

# Alignment Modes
ALT_AZ_ALIGNMENT = 0
POLAR_ALIGNMENT = 1
GERMAN_POLAR_ALIGNMENT = 2

# Drive Rates
SIDEREAL_RATE = 0  # 15.041 arcseconds per second
LUNAR_RATE = 1  # 14.685 arcseconds per second
SOLAR_RATE = 2  # 15 arcseconds per second
KING_RATE = 3  # 15.0369 arcseconds per second

# Equatorial Coordinate Types
OTHER = 0  # Custom or unknown equinox and/or reference frame
TOPOCENTRIC = 1  # Coordinates of the object at the current date having allowed for annual aberration, precession and nutation.
J2000 = 2  # Coordinates of the object at mid-day on 1st January 2000, ICRS reference frame.
J2050 = 3  # Same as above except for 1st January 2050
B1950 = 4  # B1950 equinox, FK4 reference frame

# Guide Directions
NORTH = 0  # North (+ declination/altitude)
SOUTH = 1  # South (- declination/altitude)
EAST = 2  # East (+ right ascension/azimuth)
WEST = 3  # West (- right ascension/azimuth)

# Pier Side
EAST = 0  # Normal pointing state - mount on east side of pier (looking west)
WEST = 1  # Through the pole pointing state - mount on the west side of pier (looking east)
UNKNOWN = -1  # Unknown or indeterminate

# Axes
PRIMARY = 0  # Primary axis (Righ Ascension or Azimuth)
SECONDARY = 1  # Secondary axis (Declination or Altitude)
TERTIARY = 2  # Tertiary axis (imager rotator/de-rotator)

SKIP_GEOINFO = True