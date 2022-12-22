import time
from queue import Queue
from alpaca.camera import *
from alpaca.telescope import *
from requests import RequestException
from datetime import datetime
from config import EXPOSURES, GPS
from threading import Lock
from mock import MockCamera, MockTelescope
import os
from rhodesmill_skyfield.skyfield_api import get_star

SKIP_TELESCOPE = os.environ.get('SKIP_TELESCOPE') is not None
SKIP_CAMERA = os.environ.get('SKIP_CAMERA') is not None


class AlpacaClient:
    def __init__(self, in_queue: Queue, out_queue: Queue, exposure_time_left: dict, exposure_time_lock: Lock,  gps: GPS) -> None:
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.exposure_time_left = exposure_time_left
        self.exposure_time_lock = exposure_time_lock
        self.telescope = Telescope('stargazer:8000', 0) if not SKIP_TELESCOPE else MockTelescope()
        self.telescope.SiteElevation = gps.elevation
        self.telescope.SiteLatitude = gps.latitude
        self.telescope.SiteLongitude = gps.longitude
        self.camera = Camera('stargazer:8000', 0) if not SKIP_CAMERA else MockCamera()
        self.should_disconnect = True
        self.loading_queue = []
        return

    def controller(self):
        try:
            print('[alpclient-status] ready for commands')
            while True:
                self.telescope.Connected = True
                self.camera.Connected = True
                while self.in_queue.empty():
                    time.sleep(5)
                # Prioritize gps data
                queue_item = self.in_queue.get()
                star = get_star(queue_item['object_name'])
                ra, dec = star['coordinates']['ascension'], star['coordinates']['declination']
                queue_item['coordinates'] = {'ascension': ra, 'declination': dec}
                self.telescope.Tracking = True
                self.telescope.SlewToCoordinatesAsync(ra, dec)
                while self.telescope.Slewing:
                    time.sleep(5)
                all_images = []
                print(f"[alpclient-status] imaging {queue_item['object_name']} ({queue_item['star_id']}) at dec: {dec} and ra: {ra}")
                for i in range(len(EXPOSURES[queue_item['image_quality']])):
                    seconds = EXPOSURES[queue_item['image_quality']][i]
                    print(f"[alpclient-status] image {i+1}/{len(EXPOSURES[queue_item['image_quality']])} ({seconds} seconds)")
                    self.camera.StartExposure(seconds, False)
                    while not self.camera.ImageReady:
                        time.sleep(10)
                    all_images.append(self.camera.ImageArray)
                    with self.exposure_time_lock:
                        seconds_left = self.exposure_time_left['seconds']
                        self.exposure_time_left['seconds'] = max(seconds_left - seconds, 0)
                self.telescope.Tracking = False
                # give id to other thread
                queue_item['finished_imaging'] = str(datetime.now())
                queue_item['db_keys'] = all_images
                self.out_queue.put(queue_item)
                print(f"[alpclient-status] done imaging {queue_item['object_name']} ({queue_item['star_id']}), written to db")

        except ActionNotImplementedException as e:
            print(f'[alpclient-error] {e}')
            pass
        except InvalidValueException as e:
            print(e)
            pass
        except NotConnectedException as e:
            print('[alpclient-error] not connected')
        except NotImplementedException as e:
            print(e)
            pass
        except ParkedException as e:
            print(e)
            pass
        except SlavedException as e:
            print(e)
            pass
        except ValueNotSetException as e:
            print(e)
            pass
        except RequestException as e:
            print('[alpclient-error] could not connect camera or telescope to server')
            self.should_disconnect = False
        except DriverException as e:
            print(f'Driver exception: {e}')
        except Exception as e:
            print(e)
            pass
        finally:
            if self.should_disconnect:
                self.disconnect()
        return
    
    def disconnect(self):
        try:
            print('[alpclient-status] disconnecting from camera and telescope')
            self.telescope.Connected = False
            self.camera.Connected = False
        except Exception as e:
            print(f'[alpclient-error] in disconnect: {e}')
