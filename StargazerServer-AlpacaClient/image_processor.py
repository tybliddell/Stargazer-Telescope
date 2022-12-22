from queue import Queue
from time import sleep
from datetime import datetime
from redis import Redis
import json
from decorators import retry_redis_request
import os

class ImageProcessor:

    def __init__(self, in_queue: Queue, out_queue: Queue) -> None:
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.red = Redis(host='redis')
        self.sub = self.red.pubsub()
        if not os.path.exists("images"):
            os.makedirs("images")
        return


    def _redis_request(self, json_data,timeout=120):
        @retry_redis_request
        def find_my_response(expected_id):
            _response = json.loads(self.sub.get_message(timeout=timeout).get('data').decode())
            return _response if _response.get('id') == expected_id else None
        self.sub.subscribe('IMAGE_PROCESSOR_FINISHED')
        self.red.publish('IMAGE_PROCESSOR_COMMAND', json.dumps(json_data))
        response = find_my_response(json_data['id'])
        if response is not None:
            response['data'] = response.get('data', '')
        self.sub.unsubscribe('IMAGE_PROCESSOR_FINISHED')
        return response
    
    def process_image(self) -> None:
        #self.sub.subscribe('IMAGE_PROCESSOR_FINISHED')
        while True:
            while self.in_queue.empty():
                sleep(5)
            queue_item = self.in_queue.get()
            print(f"[proc-status] processing images for {queue_item['object_name']} ({queue_item['star_id']})")
            # Tell Redis to go look for images to process under specific ID
            query = {}
            query['command'] = 'PROCESS_IMAGE'
            query['id'] = queue_item['star_id']
            query['args'] = {'db_keys': queue_item['db_keys']}
            message = self._redis_request(query)
            if message is None:
                print(f'[proc-status] did not get response from image processor, continuing')
                continue
            print(f'[proc-status] received processed image with status: {message["status"]} and ID: {message["data"]}')
            if message['status'] != 'ok':
                print(f"[proc-status] error from img proc: {message['data']}")
                continue
            database_key = message['data']

            with open(f'images/{database_key}', 'w') as f:
                f.write(str(self.red.get(database_key)))
            queue_item['finished_processing'] = str(datetime.now())
            queue_item['image_id'] = database_key
            print(f"[proc-status] finsished processing {queue_item['object_name']} ({queue_item['star_id']})")
            self.out_queue.put(queue_item)

# imginfo = self.camera.ImageArrayInfo
# if imginfo.ImageElementType == ImageArrayElementTypes.Int32:
#     if self.camera.MaxADU <= 65535:
#         imgDataType = np.uint16 # Required for BZERO & BSCALE to be written
#     else:
#         imgDataType = np.int32
# elif imginfo.ImageElementType == ImageArrayElementTypes.Double:
#     imgDataType = np.float64
# if imginfo.Rank == 2:
#     nda = np.array(image, dtype=imgDataType).transpose()
# else:
#     nda = np.array(image, dtype=imgDataType).transpose(2,1,0)
# hdr = fits.Header()
# hdr['COMMENT'] = 'FITS (Flexible Image Transport System) format defined in Astronomy and ' \
#                 'Astrophysics Supplement Series v44/p363, v44/p371, v73/p359, v73/p365. ' \
#                 'Contact the NASA Science Office of Standards and Technology for the ' \
#                 'FITS Definition document #100 and other FITS information.'
# if imgDataType ==  np.uint16:
#     hdr['BZERO'] = 32768.0
#     hdr['BSCALE'] = 1.0
# hdr['EXPOSURE'] = self.camera.LastExposureDuration
# hdr['EXPTIME'] = self.camera.LastExposureDuration
# hdr['DATE-OBS'] = self.camera.LastExposureStartTime
# hdr['TIMESYS'] = 'UTC'
# hdr['XBINNING'] = self.camera.BinX
# hdr['YBINNING'] = self.camera.BinY
# hdr['INSTRUME'] = self.camera.SensorName
# try:
#     hdr['GAIN'] = self.camera.Gain
# except:
#     pass
# try:
#     hdr['OFFSET'] = self.camera.Offset
#     if type(self.camera.Offset == int):
#         hdr['PEDESTAL'] = self.camera.Offset
# except:
#     pass
# hdr['HISTORY'] = 'Created using Stargazer 9001 :)'

# hdu = fits.PrimaryHDU(nda, header=hdr)

# img_file = f"./raw_images/{queue_item['object_name']}-{queue_item['star_id']}.fts"
# hdu.writeto(img_file, overwrite=True)

# queue_item['image_path'] = img_file