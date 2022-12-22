from rhodesmill_skyfield.named_stars import NAMED_STARS
from skyfield.api import Star, load, Angle, Loader
from skyfield.data import hipparcos
from typing import Tuple


def get_ra_and_dec(star_name) -> Tuple[Angle, Angle]:
    hip = int(NAMED_STARS[star_name]['HIP'])
    with load.open('repos/StargazerServer-AlpacaClient/hip_main.dat') as f:
        df = hipparcos.load_dataframe(f)
    desired_star = Star.from_dataframe(df.loc[hip])
    load_bsp = Loader('repos/StargazerServer-AlpacaClient')
    planets = load_bsp('de421.bsp')
    earth = planets['earth']
    ts = load.timescale()
    t = ts.now()
    ra, dec, _ = earth.at(t).observe(desired_star).radec()
    return ra, dec


def get_star(star_name) -> dict:
    ra, dec = get_ra_and_dec(star_name)
    star = {'coordinates': {'ascension': ra.hours, 'declination': dec.degrees}}
    designation = NAMED_STARS[star_name]['Designation']
    constellation = NAMED_STARS[star_name]['Constellation']
    star['object_info'] = f"{star_name}'s IAU designation is {designation} and is part of the {constellation} constellation"
    return star
