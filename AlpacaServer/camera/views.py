from decimal import Decimal
import json
from django.http import JsonResponse, QueryDict
from common.config import ALPACA_ERROR_CODES
from common.helpers import init_response, return_error
from redis import Redis
from decorators import retry_redis_request
import base64

RED = Redis(host='redis')
SUB = RED.pubsub()


def _redis_request(json_data,timeout=2):
    @retry_redis_request
    def find_my_response(expected_id):

        _response = json.loads(SUB.get_message(timeout=timeout).get('data').decode())
        return _response if _response.get('id') == expected_id else None
    SUB.subscribe('CAMERA_DATA')
    RED.publish('ALPACA', json.dumps(json_data))
    response = find_my_response(json_data['id'])
    SUB.unsubscribe('CAMERA_DATA')
    return response


def bayeroffsetx(request, device_number: int):
    response = init_response(request)
    response.update({'Value': 0})
    return JsonResponse(response, status=200)

def bayeroffsety(request, device_number: int):
    response = init_response(request)
    response.update({'Value': 0})
    return JsonResponse(response, status=200)

def binx(request, device_number: int):
    response = init_response(request)
    response.update({'Value': 0})
    return JsonResponse(response, status=200)


def biny(request, device_number: int):
    response = init_response(request)
    response.update({'Value': 0})
    return JsonResponse(response, status=200)

def camerastate(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': 1337})
    return JsonResponse(response, status=200)

def cameraxsize(request, device_number: int):
    response = init_response(request)
    response.update({'Value': 6000})
    return JsonResponse(response, status=200)

def cameraysize(request, device_number: int):
    response = init_response(request)
    response.update({'Value': 4000})
    return JsonResponse(response, status=200)

def canabortexposure(request, device_number: int):
    response = init_response(request)
    response.update({'Value': True})
    return JsonResponse(response, status=200)

def canasymmetricbin(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)

def canfastreadout(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)

def cangetcoolerpower(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)

def canpulseguide(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)

def cansetccdtemperature(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)

def canstopexposure(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)

def ccdtemperature(request, device_number: int):
    response = init_response(request)
    return return_error(response, ALPACA_ERROR_CODES['PropertyNotImplementedException'], "Not supported")

def cooleron(request, device_number: int):
    response = init_response(request)
    if request.method == "GET":
        response.update({'Value': False})
        return JsonResponse(response, status=200)
    else:
        return return_error(response, ALPACA_ERROR_CODES['PropertyNotImplementedException'], "Cooler not implemented")

def coolerpower(request, device_number: int):
    response = init_response(request)
    return return_error(response, ALPACA_ERROR_CODES['PropertyNotImplementedException'], "Cooler not implemented")

def electronsperadu(request, device_number: int):
    response = init_response(request)
    response.update({'Value': Decimal('86000')})
    return JsonResponse(response, status=200)

def exposuremax(request, device_number: int):
    response = init_response(request)
    response.update({'Value': Decimal('120')})
    return JsonResponse(response, status=200)

def exposuremin(request, device_number: int):
    response = init_response(request)
    response.update({'Value': '0.000125'})
    return JsonResponse(response, status=200)

def exposureresolution(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': '0.000125'})
    return JsonResponse(response, status=200)

def fastreadout(request, device_number: int):
    response = init_response(request)
    return return_error(response, ALPACA_ERROR_CODES['PropertyNotImplementedException'], "Fast readout is not supported")

def fullwellcapacity(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': Decimal('1337')})
    return JsonResponse(response, status=200)

def gain(request, device_number: int):
    response = init_response(request)
    if request.method == "GET":
        # TODO rich_wish_list
        response.update({'Value': 1337})
        return JsonResponse(response, status=200)
    else:
        # TODO rich_wish_list
        return JsonResponse(response, status=200)

def gainmax(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': 1337})
    return JsonResponse(response, status=200)

def gainmin(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': 1337})
    return JsonResponse(response, status=200)

def gains(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': ['gain', 'gain', 'gain']})
    return JsonResponse(response, status=200)

def hasshutter(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': False})
    return JsonResponse(response, status=200)

def heatsinktemperature(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': Decimal('1337')})
    return JsonResponse(response, status=200)

def imagearray(request, device_number: int):
    response = init_response(request)
    qd = QueryDict(request.body)
    query = {}
    query['command'] = 'LAST_IMAGE'
    query['id'] = response['ServerTransactionID']
    query['args'] = {}

    if (redis_response := _redis_request(query, 5)) is None:
        return return_error(response, 0x500, "Something goofy went wrong with the camera :(")
    response['Value'] = redis_response['data']
    return JsonResponse(response, status=200)

def imagearrayvariant(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    # TODO We will want to change data type of value based on type and rank values, unless we get those from Rich in correct format
    response.update({'Type': 0, 'Rank': 2, 'Value': [1337]})
    return JsonResponse(response, status=200)

def imageready(request, device_number: int):
    response = init_response(request)
    qd = QueryDict(request.body)
    query = {}
    query['command'] = 'STATUS'
    query['id'] = response['ServerTransactionID']
    query['args'] = {}

    if (redis_response := _redis_request(query)) is None:
        return return_error(response, 0x500, "Something goofy went wrong with the camera :(")
    response['Value'] = redis_response.get('data') == 'IMAGE_READY'
    return JsonResponse(response, status=200)

def ispulseguiding(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': False})
    return JsonResponse(response, status=200)

def lastexposureduration(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': Decimal('1337')})
    return JsonResponse(response, status=200)

def lastexposurestarttime(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': 'Bond, James Bond'})
    return JsonResponse(response, status=200)

def maxadu(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': 1337})
    return JsonResponse(response, status=200)

def maxbinx(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': 1337})
    return JsonResponse(response, status=200)

def maxbiny(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': 1337})
    return JsonResponse(response, status=200)

def numx(request, device_number: int):
    response = init_response(request)
    if request.method == "GET":
        # TODO rich_wish_list
        response.update({'Value': 1337})
        return JsonResponse(response, status=200)
    else:
        # TODO rich_wish_list
        return JsonResponse(response, status=200)

def numy(request, device_number: int):
    response = init_response(request)
    if request.method == "GET":
        # TODO rich_wish_list
        response.update({'Value': 1337})
        return JsonResponse(response, status=200)
    else:
        # TODO rich_wish_list
        return JsonResponse(response, status=200)

def offset(request, device_number: int):
    response = init_response(request)
    if request.method == "GET":
        # TODO rich_wish_list
        response.update({'Value': 1337})
        return JsonResponse(response, status=200)
    else:
        # TODO rich_wish_list
        return JsonResponse(response, status=200)

def offsetmax(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': 1337})
    return JsonResponse(response, status=200)

def offsetmin(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': 1337})
    return JsonResponse(response, status=200)

def offsets(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': ['Hello', 'World']})
    return JsonResponse(response, status=200)

def percentcompleted(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': 1337})
    return JsonResponse(response, status=200)

def pixelsizex(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': Decimal('1337')})
    return JsonResponse(response, status=200)

def pixelsizey(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': Decimal('1337')})
    return JsonResponse(response, status=200)

def readoutmode(request, device_number: int):
    response = init_response(request)
    if request.method == "GET":
        # TODO rich_wish_list
        response.update({'Value': 1337})
        return JsonResponse(response, status=200)
    else:
        # TODO rich_wish_list
        return JsonResponse(response, status=200)

def readoutmodes(request, device_number: int):
    response = init_response(request)
    if request.method == "GET":
        # TODO rich_wish_list
        response.update({'Value': ['stun', 'kill']})
        return JsonResponse(response, status=200)
    else:
        # TODO rich_wish_list
        return JsonResponse(response, status=200)

def sensorname(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': 'response'})
    return JsonResponse(response, status=200)

def sensortype(request, device_number: int):
    response = init_response(request)
    # TODO rich_wish_list
    response.update({'Value': 1337})
    return JsonResponse(response, status=200)

def setccdtemperature(request, device_number: int):
    response = init_response(request)
    if request.method == "GET":
        # TODO rich_wish_list
        response.update({'Value': Decimal('1337')})
        return JsonResponse(response, status=200)
    else:
        # TODO rich_wish_list
        return JsonResponse(response, status=200)

def startx(request, device_number: int):
    response = init_response(request)
    if request.method == "GET":
        # TODO rich_wish_list
        response.update({'Value': 1337})
        return JsonResponse(response, status=200)
    else:
        # TODO rich_wish_list
        return JsonResponse(response, status=200)

def starty(request, device_number: int):
    response = init_response(request)
    if request.method == "GET":
        # TODO rich_wish_list
        response.update({'Value': 1337})
        return JsonResponse(response, status=200)
    else:
        # TODO rich_wish_list
        return JsonResponse(response, status=200)

def subexposureduration(request, device_number: int):
    response = init_response(request)
    if request.method == "GET":
        # TODO rich_wish_list
        response.update({'Value': Decimal('1337')})
        return JsonResponse(response, status=200)
    else:
        # TODO rich_wish_list
        return JsonResponse(response, status=200)

def abortexposure(request, device_number: int):
    response = init_response(request)
    qd = QueryDict(request.body)
    query = {}
    query['command'] = 'ABORT'
    query['id'] = response['ServerTransactionID']
    query['args'] = {}

    if (redis_response := _redis_request(query)) is None:
        return return_error(response, 0x500, "Something goofy went wrong with the camera :(")
    return JsonResponse(response, status=200)
    
def pulseguide(request, device_number: int):
    response = init_response(request)
    # TODO Tyler and Hyrum wish list
    return JsonResponse(response, status=200)

def startexposure(request, device_number: int):
    response = init_response(request)
    qd = QueryDict(request.body)
    query = {}
    query['command'] = 'CAPTURE'
    query['id'] = response['ServerTransactionID']
    query['args'] = { 'light' : bool(qd['Light']), 'time' : float(qd['Duration']) }

    if (redis_response := _redis_request(query)) is None:
        return return_error(response, 0x500, "Something goofy went wrong with the camera :(")
    return JsonResponse(response, status=200)

def stopexposure(request, device_number: int):
    # TODO return not implemented??
    response = init_response(request)
    # TODO rich_wish_list
    return JsonResponse(response, status=200)
