from pico import PicoSetup
from swarm import SwarmSetup
import os

SKIP_SWARM_PICO_SETUP = os.environ.get('SKIP_SWARM_PICO_SETUP') is not None

if SKIP_SWARM_PICO_SETUP:
    print("[init-status] skipping swarm and pico setup due to environment flag")
    exit()

print("[init-status] setting Swarm rates")
swarm = SwarmSetup()
swarm.set_rates()
print('[init-status] sucessfully set Swarm DT, GN and RT rates')

# Now wait for a DT and GN message
print('[init-status] waiting for DT and GN messages')
data = swarm.get_dt_gn()
print('[init-status] received DT and GN messages')
del swarm

print('[init-status] initializing pico')
pico = PicoSetup()
pico.send_data(data['latitude'])
del pico

# TODO: do we want to pass this data at startup?
#print('[init-status] writing data to ../AlpacaServer/telescope/startup_data.py')

print('[init-status] swarm_pico_init complete')