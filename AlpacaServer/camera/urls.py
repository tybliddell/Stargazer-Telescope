from django.urls import path
from camera.views import (bayeroffsetx, bayeroffsety, binx, biny, camerastate, cameraxsize, cameraysize, 
                          canabortexposure, canasymmetricbin, canfastreadout, cangetcoolerpower, 
                          canpulseguide, cansetccdtemperature, canstopexposure, ccdtemperature, cooleron, 
                          coolerpower, electronsperadu, exposuremax, exposuremin, exposureresolution, 
                          fastreadout, fullwellcapacity, gain, gainmax, gainmin, gains, hasshutter, 
                          heatsinktemperature, imagearray, imagearrayvariant, imageready, ispulseguiding, 
                          lastexposureduration, lastexposurestarttime, maxadu, maxbinx, maxbiny, numx, numy, 
                          offset, offsetmax, offsetmin, offsets, percentcompleted, pixelsizex, pixelsizey, 
                          readoutmode, readoutmodes, sensorname, sensortype, setccdtemperature, startx, starty, 
                          subexposureduration, abortexposure, pulseguide, startexposure, stopexposure)
from common.views import action, command_blind, command_bool, command_string, connected, description, driver_info, driver_version, interface_version, name, supported_actions

urlpatterns = [
    path('<int:device_number>/bayeroffsetx', bayeroffsetx, name='bayer_offset_x'),
    path('<int:device_number>/bayeroffsety', bayeroffsety, name='bayer_offset_y'),
    path('<int:device_number>/binx', binx, name='bin_x'),
    path('<int:device_number>/biny', biny, name='bin_y'),
    path('<int:device_number>/camerastate', camerastate, name='camera_state'),
    path('<int:device_number>/cameraxsize', cameraxsize, name='camera_x_size'),
    path('<int:device_number>/cameraysize', cameraysize, name='camera_y_size'),
    path('<int:device_number>/canabortexposure', canabortexposure, name='can_abort_exposure'),
    path('<int:device_number>/canasymmetricbin', canasymmetricbin, name='can_asymmetric_bin'),
    path('<int:device_number>/canfastreadout', canfastreadout, name='can_fast_readout'),
    path('<int:device_number>/cangetcoolerpower', cangetcoolerpower, name='can_get_cooler_power'),
    path('<int:device_number>/canpulseguide', canpulseguide, name='can_pulse_guide'),
    path('<int:device_number>/cansetccdtemperature', cansetccdtemperature, name='can_set_ccd_temperature'),
    path('<int:device_number>/canstopexposure', canstopexposure, name='can_stop_exposure'),
    path('<int:device_number>/ccdtemperature', ccdtemperature, name='ccd_temperature'),
    path('<int:device_number>/cooleron', cooleron, name='cooleron'),
    path('<int:device_number>/coolerpower', coolerpower, name='cooler_power'),
    path('<int:device_number>/electronsperadu', electronsperadu, name='electrons_per_adu'),
    path('<int:device_number>/exposuremax', exposuremax, name='exposure_max'),
    path('<int:device_number>/exposuremin', exposuremin, name='exposure_min'),
    path('<int:device_number>/exposureresolution', exposureresolution, name='exposure_resolution'),
    path('<int:device_number>/fastreadout', fastreadout, name='fast_readout'),
    path('<int:device_number>/fullwellcapacity', fullwellcapacity, name='full_well_capacity'),
    path('<int:device_number>/gain', gain, name='gain'),
    path('<int:device_number>/gainmax', gainmax, name='gain_max'),
    path('<int:device_number>/gainmin', gainmin, name='gain_min'),
    path('<int:device_number>/gains', gains, name='gains'),
    path('<int:device_number>/hasshutter', hasshutter, name='has_shutter'),
    path('<int:device_number>/heatsinktemperature', heatsinktemperature, name='heat_sink_temperature'),
    path('<int:device_number>/imagearray', imagearray, name='image_array'),
    path('<int:device_number>/imagearrayvariant', imagearrayvariant, name='image_array_variant'),
    path('<int:device_number>/imageready', imageready, name='image_ready'),
    path('<int:device_number>/ispulseguiding', ispulseguiding, name='is_pulse_guiding'),                      
    path('<int:device_number>/lastexposureduration', lastexposureduration, name='last_exposure_duration'),
    path('<int:device_number>/lastexposurestarttime', lastexposurestarttime, name='last_exposure_start_time'),
    path('<int:device_number>/maxadu', maxadu, name='max_adu'),
    path('<int:device_number>/maxbinx', maxbinx, name='max_bin_x'),
    path('<int:device_number>/maxbiny', maxbiny, name='max_bin_y'),
    path('<int:device_number>/numx', numx, name='num_x'),
    path('<int:device_number>/numy', numy, name='num_y'),
    path('<int:device_number>/offset', offset, name='offset'),
    path('<int:device_number>/offsetmax', offsetmax, name='offset_max'),
    path('<int:device_number>/offsetmin', offsetmin, name='offset_min'),
    path('<int:device_number>/offsets', offsets, name='offsets'),
    path('<int:device_number>/percentcompleted', percentcompleted, name='percent_completed'),
    path('<int:device_number>/pixelsizex', pixelsizex, name='pixel_size_x'),
    path('<int:device_number>/pixelsizey', pixelsizey, name='pixel_size_y'),
    path('<int:device_number>/readoutmode', readoutmode, name='readout_mode'),
    path('<int:device_number>/readoutmodes', readoutmodes, name='readout_modes'),
    path('<int:device_number>/sensorname', sensorname, name='sensor_name'),
    path('<int:device_number>/sensortype', sensortype, name='sensor_type'),
    path('<int:device_number>/setccdtemperature', setccdtemperature, name='set_ccd_temperature'),
    path('<int:device_number>/startx', startx, name='start_x'),
    path('<int:device_number>/starty', starty, name='start_y'),
    path('<int:device_number>/subexposureduration', subexposureduration, name='sub_exposure_duration'),
    path('<int:device_number>/abortexposure', abortexposure, name='abort_exposure'),
    path('<int:device_number>/pulseguide', pulseguide, name='pulse_guide'),
    path('<int:device_number>/startexposure', startexposure, name='start_exposure'),
    path('<int:device_number>/stopexposure', stopexposure, name='stop_exposure'),
    # Common urls
    path('<int:device_number>/action', action, name='action'),
    path('<int:device_number>/commandblind', command_blind, name='command_blind'),
    path('<int:device_number>/commandbool', command_bool, name='command_bool'),
    path('<int:device_number>/commandstring', command_string, name='command_string'),
    path('<int:device_number>/connected', connected, name='connected'),
    path('<int:device_number>/description', description, name='description'),
    path('<int:device_number>/driverinfo', driver_info, name='driver_info'),
    path('<int:device_number>/driverversion', driver_version, name='driver_version'),
    path('<int:device_number>/interfaceversion', interface_version, name='interface_version'),
    path('<int:device_number>/name', name, name='name'),
    path('<int:device_number>/supportedactions', supported_actions, name='supported_actions'),
]

