from urllib.parse import parse_qs
from django.http import JsonResponse
from skyfield.toposlib import wgs84
from skyfield.api import load
from common.config import DEBUG

SERVER_TRANSACTION_ID = -1


def get_next_trans_id():
    global SERVER_TRANSACTION_ID
    SERVER_TRANSACTION_ID += 1
    return SERVER_TRANSACTION_ID


def extract_client_id(request):
    client_transaction_id = parse_qs(request.body.decode()).get('ClientTransactionID')
    if client_transaction_id:
        return client_transaction_id[0]


# init response with next server transaction id,
# client transaction id if it was included,
# error number of 0 and blank error message
def init_response(request):
    response = {'ServerTransactionID': get_next_trans_id(), 'ErrorNumber': 0, 'ErrorMessage': ''}
    if (client_id := extract_client_id(request)) is not None:
        response['ClientTransactionID'] = client_id
    return response


def return_error(response, error_num, error_message):
    response.update({'ErrorNumber': error_num, 'ErrorMessage': error_message})
    return JsonResponse(response, status=200)


def get_sidereal_time(site_lat, site_lon, site_elev):
    temp = wgs84.latlon(latitude_degrees=site_lat, longitude_degrees=site_lon, elevation_m=site_elev)
    ts = load.timescale()
    t = ts.now()
    lst = temp.lst_hours_at(t)
    if DEBUG:
        print(f'local sidereal time: {lst}')
    return lst
