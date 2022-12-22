from datetime import datetime
from django.http import JsonResponse, QueryDict
from common.helpers import init_response, return_error, get_sidereal_time
from common.config import ALPACA_ERROR_CODES
from decimal import Decimal
from telescope.config import POLAR_ALIGNMENT, TOPOCENTRIC, SIDEREAL_RATE, SKIP_GEOINFO
from uart.uart_queue import UARTQueue
import json

SITE_LATITUDE = 40.76 if SKIP_GEOINFO else None
SITE_LONGITUDE = -111.83 if SKIP_GEOINFO else None
SITE_ELEVATION = 1464 if SKIP_GEOINFO else None

def alignmentmode(request, device_number: int):
    response = init_response(request)
    response.update({'Value': POLAR_ALIGNMENT})
    return JsonResponse(response, status=200)


def altitude(request, device_number: int):
    response = init_response(request)
    uart = UARTQueue()
    uart_string, uart_response_code = uart.safe_send_request('altitude()')
    if uart_response_code in ALPACA_ERROR_CODES.values():
        return return_error(response, uart_response_code, uart_string)
    response.update({'Value': Decimal(uart_string)})
    return JsonResponse(response, status=200)


def aperturearea(request, device_number: int):
    response = init_response(request)
    # TODO
    # Ask Rich about aperture area on his camera lens
    # Probably end up being constant in config file
    response.update({'Value': Decimal('1337')})
    return JsonResponse(response, status=200)


def aperturediameter(request, device_number: int):
    response = init_response(request)
    # TODO
    # Same as above, ask Rich and put in config file
    response.update({'Value': Decimal('1337')})
    return JsonResponse(response, status=200)


def athome(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def atpark(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def azimuth(request, device_number: int):
    response = init_response(request)
    uart = UARTQueue()
    uart_string, uart_response_code = uart.safe_send_request('azimuth()')
    if uart_response_code in ALPACA_ERROR_CODES.values():
        return return_error(response, uart_response_code, uart_string)
    response.update({'Value': Decimal(uart_string)})
    return JsonResponse(response, status=200)


def canfindhome(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def canpark(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def canpulseguide(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def cansetdeclinationrate(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def cansetguiderates(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def cansetpark(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def cansetpierside(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def cansetrightascensionrate(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def cansettracking(request, device_number: int):
    response = init_response(request)
    response.update({'Value': True})
    return JsonResponse(response, status=200)


def canslew(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def canslewaltaz(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def canslewaltazasync(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def canslewasync(request, device_number: int):
    response = init_response(request)
    response.update({'Value': True})
    return JsonResponse(response, status=200)


def cansync(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def cansyncaltaz(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def canunpark(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def declination(request, device_number: int):
    response = init_response(request)
    uart = UARTQueue()
    if SITE_LATITUDE is None:
        return return_error(response, ALPACA_ERROR_CODES['InvalidOperationException'], "You must set the site latitude before you can get the declination.")
    uart_string, uart_response_code = uart.safe_send_request(f'declination()')
    if uart_response_code in ALPACA_ERROR_CODES.values():
        return return_error(response, uart_response_code, uart_string)
    response.update({'Value': Decimal(uart_string)})
    return JsonResponse(response, status=200)


def declinationrate(request, device_number: int):
    response = init_response(request)
    response.update({'Value': Decimal('0')})
    return JsonResponse(response, status=200)


def doesrefraction(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def equatorialsystem(request, device_number: int):
    response = init_response(request)
    response.update({'Value': TOPOCENTRIC})
    return JsonResponse(response, status=200)


def focallength(request, device_number: int):
    response = init_response(request)
    response.update({'Value': Decimal('0.3')})
    return JsonResponse(response, status=200)


def guideratedeclination(request, device_number: int):
    response = init_response(request)
    response.update({'Value': Decimal('0')})
    return JsonResponse(response, status=200)


def guideraterightascension(request, device_number: int):
    response = init_response(request)
    response.update({'Value': Decimal('0')})
    return JsonResponse(response, status=200)


def ispulseguiding(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def rightascension(request, device_number: int):
    response = init_response(request)
    uart = UARTQueue()
    if not (SITE_ELEVATION and SITE_LONGITUDE and SITE_LATITUDE):
        return return_error(response, ALPACA_ERROR_CODES['InvalidOperationException'], "You must set site elevation, latitude, and longitude before getting the right ascension.")
    sidereal_time = get_sidereal_time(SITE_LATITUDE, SITE_LONGITUDE, SITE_ELEVATION)
    uart_string, uart_response_code = uart.safe_send_request(f'rightascension({sidereal_time})')
    if uart_response_code in ALPACA_ERROR_CODES.values():
        return return_error(response, uart_response_code, uart_string)
    response.update({'Value': Decimal(uart_string)})
    return JsonResponse(response, status=200)


def rightascensionrate(request, device_number: int):
    response = init_response(request)
    response.update({'Value': Decimal('0')})
    return JsonResponse(response, status=200)


def sideofpier(request, device_number: int):
    response = init_response(request)
    return return_error(response, ALPACA_ERROR_CODES['PropertyNotImplementedException'], 'Not Supported')


def siderealtime(request, device_number: int):
    response = init_response(request)
    if not (SITE_ELEVATION and SITE_LONGITUDE and SITE_LATITUDE):
        return return_error(response, 0x40B, "You must set site elevation, latitude, and longitude before getting the sidereal time.")
    response.update({'Value': Decimal(get_sidereal_time(SITE_LATITUDE, SITE_LONGITUDE, SITE_ELEVATION))})
    return JsonResponse(response, status=200)


def siteelevation(request, device_number: int):
    response = init_response(request)
    global SITE_ELEVATION
    if request.method == "GET":
        if SITE_ELEVATION is None:
            return return_error(response, ALPACA_ERROR_CODES['InvalidOperationException'], "You must set the site elevation before getting it.")
        response.update({'Value': Decimal(str(SITE_ELEVATION))})
        return JsonResponse(response, status=200)
    else:
        put = QueryDict(request.body)
        site_elevation_temp = Decimal(put['SiteElevation'])
        if -300 > site_elevation_temp > 10000:
            return return_error(response, ALPACA_ERROR_CODES['InvalidValue'], "You may not take pictures of stars from the bottom of the ocean or the top of Mount Everest")
        SITE_ELEVATION = site_elevation_temp
        return JsonResponse(response, status=200)


def sitelatitude(request, device_number: int):
    response = init_response(request)
    global SITE_LATITUDE
    if request.method == "GET":
        if SITE_LATITUDE is None:
            return return_error(response, ALPACA_ERROR_CODES['InvalidOperationException'], "You must set the site latitude before getting it.")
        response.update({'Value': Decimal(str(SITE_LATITUDE))})
        return JsonResponse(response, status=200)
    else:
        put = QueryDict(request.body)
        site_latitude_temp = Decimal(put['SiteLatitude'])
        if -90 > site_latitude_temp > 90:
            return return_error(response, ALPACA_ERROR_CODES['InvalidValue'], "Please take pictures in the third dimension")
        SITE_LATITUDE = site_latitude_temp
        return JsonResponse(response, status=200)


def sitelongitude(request, device_number: int):
    response = init_response(request)
    global SITE_LONGITUDE
    if request.method == "GET":
        if SITE_LONGITUDE is None:
            return return_error(response, ALPACA_ERROR_CODES['InvalidOperationException'], "You must set the site longitude before getting it.")
        response.update({'Value': Decimal(str(SITE_LONGITUDE))})
        return JsonResponse(response, status=200)
    else:
        put = QueryDict(request.body)
        site_longitude_temp = Decimal(put['SiteLongitude'])
        if -180 > site_longitude_temp > 180:
            return return_error(response, ALPACA_ERROR_CODES['InvalidValue'], "Please take pictures in the third dimension")
        SITE_LONGITUDE = site_longitude_temp
        return JsonResponse(response, status=200)


def slewing(request, device_number: int):
    response = init_response(request)
    uart = UARTQueue()
    uart_string, uart_response_code = uart.safe_send_request('slewing()')
    if uart_response_code in ALPACA_ERROR_CODES.values():
        return return_error(response, uart_response_code, uart_string)
    response.update({'Value': uart_string == "True"})
    return JsonResponse(response, status=200)


def slewsettletime(request, device_number: int):
    response = init_response(request)
    # TODO Ask pico, or tell pico slew settle time
    if request.method == "GET":
        response.update({'Value': 1337})
        return JsonResponse(response, status=200)
    else:
        return JsonResponse(response, status=200)


def targetdeclination(request, device_number: int):
    response = init_response(request)
    uart = UARTQueue()
    if request.method == "GET":
        uart_string, uart_response_code = uart.safe_send_request(f'targetdeclination()')
    else:
        put = QueryDict(request.body)
        target_declination_temp = Decimal(put['TargetDeclination'])
        if -90 > target_declination_temp > 90:
            return return_error(response, ALPACA_ERROR_CODES['InvalidValue'], "Must be between -90 and 90")
        uart_string, uart_response_code = uart.safe_send_request(f'targetdeclination({target_declination_temp})')

    if uart_response_code in ALPACA_ERROR_CODES.values():
        return return_error(response, uart_response_code, uart_string)
    response.update({'Value': Decimal(uart_string)})
    return JsonResponse(response, status=200)


def targetrightascension(request, device_number: int):
    response = init_response(request)
    uart = UARTQueue()
    if request.method == "GET":
        uart_string, uart_response_code = uart.safe_send_request(f'targetra()')
    else:
        put = QueryDict(request.body)
        target_ra_temp = Decimal(put['TargetRightAscension'])
        if 0 > target_ra_temp > 24:
            return return_error(response, ALPACA_ERROR_CODES['InvalidValue'], "Must be between 0 and 24")
        uart_string, uart_response_code = uart.safe_send_request(f'targetra({target_ra_temp})')

    if uart_response_code in ALPACA_ERROR_CODES.values():
        return return_error(response, uart_response_code, uart_string)
    response.update({'Value': Decimal(uart_string)})
    return JsonResponse(response, status=200)


def tracking(request, device_number: int):
    response = init_response(request)
    uart = UARTQueue()
    if request.method == "GET":
        uart_string, uart_response_code = uart.safe_send_request('tracking()')
    else:
        put = QueryDict(request.body)
        uart_string, uart_response_code = uart.safe_send_request(f"tracking({json.loads(put['Tracking'].lower())})")

    if uart_response_code in ALPACA_ERROR_CODES.values():
        return return_error(response, uart_response_code, uart_string)
    response.update({'Value': uart_string == "True"})
    return JsonResponse(response, status=200)


def trackingrate(request, device_number: int):
    response = init_response(request)
    if request.method == "GET":
        response.update({'Value': SIDEREAL_RATE})
        return JsonResponse(response, status=200)
    else:
        return return_error(response, ALPACA_ERROR_CODES['PropertyNotImplementedException'], 'Cannot change the tracking rate')


def trackingrates(request, device_number: int):
    response = init_response(request)
    response.update({'Value': [SIDEREAL_RATE]})
    return JsonResponse(response, status=200)


def utcdate(request, device_number: int):
    response = init_response(request)
    if request.method == "GET":
        response.update({'Value': str(datetime.utcnow())})
        return JsonResponse(response, status=200)
    else:
        return return_error(response, ALPACA_ERROR_CODES['PropertyNotImplementedException'], "It's time for you to get a watch. Cause that ain't the correct time.")


def abortslew(request, device_number: int):
    response = init_response(request)
    uart = UARTQueue()
    uart_string, uart_response_code = uart.safe_send_request('abortslew()')
    if uart_response_code in ALPACA_ERROR_CODES.values():
        return return_error(response, uart_response_code, uart_string)
    response.update({'Value': Decimal(uart_string)})
    return JsonResponse(response, status=200)


def axisrates(request, device_number: int):
    response = init_response(request)
    response.update({'Value': []})
    return JsonResponse(response, status=200)


def canmoveaxis(request, device_number: int):
    response = init_response(request)
    response.update({'Value': False})
    return JsonResponse(response, status=200)


def destinationsideofpier(request, device_number: int):
    response = init_response(request)
    return return_error(response, "MethodNotImplemented", "No Germans here. :( or else this would have been engineered a lot better")


def findhome(request, device_number: int):
    response = init_response(request)
    return return_error(response, "MethodNotImplemented", "Sorry, you are homeless")


def moveaxis(request, device_number: int):
    response = init_response(request)
    return return_error(response, "MethodNotImplemented", "I don't want to do math")


def park(request, device_number: int):
    response = init_response(request)
    return return_error(response, "MethodNotImplemented", "We might park someday")


def pulseguide(request, device_number: int):
    response = init_response(request)
    return return_error(response, "MethodNotImplemented", "There's a flatline, no pulse, we lost her.")


def setpark(request, device_number: int):
    response = init_response(request)
    return return_error(response, "MethodNotImplemented", "Parallel parking is really hard")


def slewtoaltaz(request, device_number: int):
    response = init_response(request)
    return return_error(response, "MethodNotImplemented", "Just use async methods")


def slewtoaltazasync(request, device_number: int):
    response = init_response(request)
    put = QueryDict(request.body)
    az = put['Azimuth']
    alt = put['Altitude']
    if 0 > Decimal(alt) > 90:
        return return_error(response, "InvalidValue", "Altitude must be between 0 and 90")
    # Normalize altitude to 0-360
    if Decimal(az) > 0:
        alt = alt % 360
    else:
        alt = 360 - (abs(alt) % 360)

    sidereal_time = get_sidereal_time(SITE_LATITUDE, SITE_LONGITUDE, SITE_ELEVATION)
    uart = UARTQueue()
    uart_string, uart_response_code = uart.safe_send_request(f'slewtoaltazasync({alt}, {az}, {sidereal_time})')
    if uart_response_code in ALPACA_ERROR_CODES.values():
        return return_error(response, uart_response_code, uart_string)
    return JsonResponse(response, status=200)


def slewtocoordinates(request, device_number: int):
    response = init_response(request)
    return return_error(response, "MethodNotImplemented", "Just use async methods")


def slewtocoordinatesasync(request, device_number: int):
    response = init_response(request)
    put = QueryDict(request.body)
    ra = put['RightAscension']
    dec = put['Declination']
    sidereal_time = get_sidereal_time(SITE_LATITUDE, SITE_LONGITUDE, SITE_ELEVATION)
    uart = UARTQueue()
    uart_string, uart_response_code = uart.safe_send_request(f'slewtocoordinatesasync({ra}, {dec}, {sidereal_time})')
    if uart_response_code in ALPACA_ERROR_CODES.values():
        return return_error(response, uart_response_code, uart_string)
    return JsonResponse(response, status=200)


def slewtotarget(request, device_number: int):
    response = init_response(request)
    return return_error(response, "MethodNotImplemented", "Just use async methods")


def slewtotargetasync(request, device_number: int):
    response = init_response(request)
    if not (SITE_ELEVATION and SITE_LONGITUDE and SITE_LATITUDE):
        return return_error(response, ALPACA_ERROR_CODES['DriverException'], "You must set site elevation, latitude, and longitude before slewing to target.")
    sidereal_time = get_sidereal_time(SITE_LATITUDE, SITE_LONGITUDE, SITE_ELEVATION)
    uart = UARTQueue()
    uart_string, uart_response_code = uart.safe_send_request(f'slewtotargetasync({sidereal_time})')
    if uart_response_code in ALPACA_ERROR_CODES.values():
        return return_error(response, uart_response_code, uart_string)
    return JsonResponse(response, status=200)


def synctoaltaz(request, device_number: int):
    response = init_response(request)
    return return_error(response, "MethodNotImplemented", "slewing > syncing")


def synctocoordinates(request, device_number: int):
    response = init_response(request)
    return return_error(response, "MethodNotImplemented", "slewing > syncing")


def synctotarget(request, device_number: int):
    response = init_response(request)
    return return_error(response, "MethodNotImplemented", "slewing > syncing")


def unpark(request, device_number: int):
    response = init_response(request)
    return return_error(response, "MethodNotImplemented", "Parking lot is full, no parking")
    # TODO Implement once we have finished motor drivers
    # return JsonResponse(response, status=200)