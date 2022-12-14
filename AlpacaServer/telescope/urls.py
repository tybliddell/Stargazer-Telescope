from django.urls import path
from telescope.views import (alignmentmode, altitude, aperturearea, aperturediameter, athome, atpark, azimuth, 
                            canfindhome, canpark, canpulseguide, cansetdeclinationrate, cansetguiderates, cansetpark, 
                            cansetpierside, cansetrightascensionrate, cansettracking, canslew, canslewaltaz, canslewaltazasync, 
                            canslewasync, cansync, cansyncaltaz, canunpark, declination, declinationrate, doesrefraction, 
                            equatorialsystem, focallength, guideratedeclination, guideraterightascension, ispulseguiding, 
                            rightascension, rightascensionrate, sideofpier, siderealtime, siteelevation, sitelatitude, 
                            sitelongitude, slewing, slewsettletime, targetdeclination, targetrightascension, tracking, 
                            trackingrate, trackingrates, utcdate, abortslew, axisrates, canmoveaxis, destinationsideofpier, 
                            findhome, moveaxis, park, pulseguide, setpark, slewtoaltaz, slewtoaltazasync, slewtocoordinates, 
                            slewtocoordinatesasync, slewtotarget, slewtotargetasync, synctoaltaz, synctocoordinates, synctotarget, 
                            unpark)
from common.views import action, command_blind, command_bool, command_string, connected, description, driver_info, driver_version, interface_version, name, supported_actions

urlpatterns = [
    path('<int:device_number>/alignmentmode', alignmentmode, name='alignment_mode'),
    path('<int:device_number>/altitude', altitude, name='altitude'),
    path('<int:device_number>/aperturearea', aperturearea, name='aperture_area'),
    path('<int:device_number>/aperturediameter', aperturediameter, name='aperture_diameter'),
    path('<int:device_number>/athome', athome, name='at_home'),
    path('<int:device_number>/atpark', atpark, name='at_park'),
    path('<int:device_number>/azimuth', azimuth, name='azimuth'),
    path('<int:device_number>/canfindhome', canfindhome, name='can_find_home'),
    path('<int:device_number>/canpark', canpark, name='can_park'),
    path('<int:device_number>/canpulseguide', canpulseguide, name='can_pulse_guide'),
    path('<int:device_number>/cansetdeclinationrate', cansetdeclinationrate, name='can_set_declination_rate'),
    path('<int:device_number>/cansetguiderates', cansetguiderates, name='can_set_guide_rates'),
    path('<int:device_number>/cansetpark', cansetpark, name='can_set_park'),
    path('<int:device_number>/cansetpierside', cansetpierside, name='can_set_pier_side'),
    path('<int:device_number>/cansetrightascensionrate', cansetrightascensionrate, name='can_set_right_ascension_rate'),
    path('<int:device_number>/cansettracking', cansettracking, name='can_set_tracking'),
    path('<int:device_number>/canslew', canslew, name='can_slew'),
    path('<int:device_number>/canslewaltaz', canslewaltaz, name='can_slew_alt_az'),
    path('<int:device_number>/canslewaltazasync', canslewaltazasync, name='can_slew_alt_az_async'),
    path('<int:device_number>/canslewasync', canslewasync, name='can_slew_async'),
    path('<int:device_number>/cansync', cansync, name='can_sync'),
    path('<int:device_number>/cansyncaltaz', cansyncaltaz, name='can_sync_alt_az'),
    path('<int:device_number>/canunpark', canunpark, name='can_unpark'),
    path('<int:device_number>/declination', declination, name='declination'),
    path('<int:device_number>/declinationrate', declinationrate, name='declination_rate'),
    path('<int:device_number>/doesrefraction', doesrefraction, name='does_refraction'),
    path('<int:device_number>/equatorialsystem', equatorialsystem, name='equatorial_system'),
    path('<int:device_number>/focallength', focallength, name='focal_length'),
    path('<int:device_number>/guideratedeclination', guideratedeclination, name='guide_rate_declination'),
    path('<int:device_number>/guideraterightascension', guideraterightascension, name='guide_rate_right_ascension'),
    path('<int:device_number>/ispulseguiding', ispulseguiding, name='is_pulse_guiding'),
    path('<int:device_number>/rightascension', rightascension, name='right_ascension'),
    path('<int:device_number>/rightascensionrate', rightascensionrate, name='right_ascension_rate'),
    path('<int:device_number>/sideofpier', sideofpier, name='side_of_pier'),
    path('<int:device_number>/siderealtime', siderealtime, name='side_realtime'),
    path('<int:device_number>/siteelevation', siteelevation, name='site_elevation'),
    path('<int:device_number>/sitelatitude', sitelatitude, name='site_latitude'),
    path('<int:device_number>/sitelongitude', sitelongitude, name='site_longitude'),
    path('<int:device_number>/slewing', slewing, name='slewing'),
    path('<int:device_number>/slewsettletime', slewsettletime, name='slew_settle_time'),
    path('<int:device_number>/targetdeclination', targetdeclination, name='target_declination'),
    path('<int:device_number>/targetrightascension', targetrightascension, name='target_right_ascension'),
    path('<int:device_number>/tracking', tracking, name='tracking'),
    path('<int:device_number>/trackingrate', trackingrate, name='tracking_rate'),
    path('<int:device_number>/trackingrates', trackingrates, name='tracking_rates'),
    path('<int:device_number>/utcdate', utcdate, name='utc_date'),
    path('<int:device_number>/abortslew', abortslew, name='abort_slew'),
    path('<int:device_number>/axisrates', axisrates, name='axis_rates'),
    path('<int:device_number>/canmoveaxis', canmoveaxis, name='can_move_axis'),
    path('<int:device_number>/destinationsideofpier', destinationsideofpier, name='destination_side_of_pier'),
    path('<int:device_number>/findhome', findhome, name='find_home'),
    path('<int:device_number>/moveaxis', moveaxis, name='move_axis'),
    path('<int:device_number>/park', park, name='park'),
    path('<int:device_number>/pulseguide', pulseguide, name='pulse_guide'),
    path('<int:device_number>/setpark', setpark, name='set_park'),
    path('<int:device_number>/slewtoaltaz', slewtoaltaz, name='slew_to_altaz'),
    path('<int:device_number>/slewtoaltazasync', slewtoaltazasync, name='slew_to_alt_az_async'),
    path('<int:device_number>/slewtocoordinates', slewtocoordinates, name='slew_to_coordinates'),
    path('<int:device_number>/slewtocoordinatesasync', slewtocoordinatesasync, name='slew_to_coordinates_async'),
    path('<int:device_number>/slewtotarget', slewtotarget, name='slew_to_target'),
    path('<int:device_number>/slewtotargetasync', slewtotargetasync, name='slew_to_target_async'),
    path('<int:device_number>/synctoaltaz', synctoaltaz, name='sync_to_alt_az'),
    path('<int:device_number>/synctocoordinates', synctocoordinates, name='sync_to_coordinates'),
    path('<int:device_number>/synctotarget', synctotarget, name='sync_to_target'),
    path('<int:device_number>/unpark', unpark, name='unpark'),
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