from skyfield.toposlib import wgs84
from skyfield.api import load


temp = wgs84.latlon(40.760780, -111.891045)
ts = load.timescale()
t = ts.now()
print(temp.lst_hours_at(t))