from django.http import JsonResponse
from common.config import SUPPORTED_ACTIONS
from urllib.parse import parse_qs
from common.helpers import init_response, return_error

def action(request, device_number: int):
    response = init_response(request)
    arguments = parse_qs(request.body.decode())
    actions = arguments.get('Action')
    if actions and actions[0] not in SUPPORTED_ACTIONS:
        return return_error(response, 0x400, 'Not Supported')
    response.update({'Value': 'This is your response dood'})
    return JsonResponse(response, status=200)

def command_blind(request, device_number: int):
    response = init_response(request)
    return return_error(response, 0x400, 'This device does not support command_blind')

def command_bool(request, device_number: int):
    response = init_response(request)
    return return_error(response, 0x400, 'This device does not support command_bool')

def command_string(request, device_number: int):
    response = init_response(request)
    return return_error(response, 0x400, 'This device does not support command_string')

def connected(request, device_number: int):
    response = init_response(request)
    # TODO FINISH THIS- Branch on get/put and actually get values
    response.update({'Value': True})
    # TODO: Once we have all the devices set up we should actually check device statuses here instead of just responding 200
    return JsonResponse(response, status=200)

def description(request, device_number: int):
    response = init_response(request)
    if 'camera' in request.path:
        # TODO rich_wish_list
        return JsonResponse(response, status=200)
    if 'telescope' in request.path:
        response.update({'Value': 'Manufacturer: Miguel Gomez, Model Number: v420.69'})
        return JsonResponse(response, status=200)
    return return_error(response, 0x400, 'Device not found')

def driver_info(request, device_number: int):
    response = init_response(request)
    response.update({'Value': ["Granny's homebaked pie", 'Version=1.0', "Authors: Hyrum Saunders and Tyler Liddell"]})
    return JsonResponse(response, status=200)

def driver_version(request, device_number: int):
    response = init_response(request)
    response.update({'Value': '1.0'})
    return JsonResponse(response, status=200)

def interface_version(request, device_number: int):
    response = init_response(request)
    response.update({'Value': 3})
    return JsonResponse(response, status=200)

def name(request, device_number: int):
    response = init_response(request)
    if 'telescope' in request.path:
        response.update({'Value': 'Telescope, duh'})
    if 'camera' in request.path:
        response.update({'Value': 'Camera, duh'})
    return response

def supported_actions(request, device_number: int):
    response = init_response(request)
    response.update({'Value': []})
    return JsonResponse(response, status=200)
