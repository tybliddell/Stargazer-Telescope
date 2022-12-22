# External Imports
import os
from queue import Queue
import signal
import time
from optparse import OptionParser
from threading import Thread, Lock

# Internal Imports
from stargazer_server import Server
from image_processor import ImageProcessor
from alpaca_client import AlpacaClient
from swarm_reader import SwarmReader
from config import DEFAULT_GPS

SKIP_GPS_DATA_REQ = os.environ.get('SKIP_GPS_DATA_REQ') is not None


def ctrl_c_pressed(_, __):
    """Signal handler for ctrl-c
    """
    os._exit(0)

# Register signal handler
signal.signal(signal.SIGINT, ctrl_c_pressed)

# Parse command line arguments
parser = OptionParser()
parser.add_option('-p', type='int', dest='serverPort')
parser.add_option('-a', type='string', dest='serverAddress')
(options, args) = parser.parse_args()

# Queues used for communication between threads
sg_to_alp = Queue()
alp_to_proc = Queue()
proc_to_sg = Queue()

if not SKIP_GPS_DATA_REQ:
    swarm_reader = SwarmReader()
    gps = swarm_reader.read_loop()
    print('[client-server-entrypoint] received gps data')
else:
    print('[client-server-entrypoint] skipping waiting for gps data. Errors may occur when sending requests to AlpacaServer')
    gps = DEFAULT_GPS

# SERVER
exposure_time_left = {'seconds': 0}
exposure_time_lock = Lock()
server = Server(in_queue=proc_to_sg, out_queue=sg_to_alp, exposure_time_left=exposure_time_left,
                exposure_time_lock=exposure_time_lock, address=options.serverAddress, port=options.serverPort, gps=gps)
server_thread = Thread(target=server.listen)
server_thread.start()

# ALPACA CLIENT
alpaca_client = AlpacaClient(in_queue=sg_to_alp, out_queue=alp_to_proc, exposure_time_left=exposure_time_left,
                             exposure_time_lock=exposure_time_lock, gps=gps)
alpaca_client_thread = Thread(target=alpaca_client.controller)
alpaca_client_thread.start()

# IMAGE PROCESSOR
image_processor = ImageProcessor(alp_to_proc, proc_to_sg)
image_processor_thread = Thread(target=image_processor.process_image)
image_processor_thread.start()

while True:
    time.sleep(1)