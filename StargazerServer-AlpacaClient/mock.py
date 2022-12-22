class MockTelescope:
    def __init__(self):
        print('[alpclient-status] creating MOCK telescope')
    
    @property
    def Connected(self):
        return True

    @Connected.setter
    def Connected(self, x):
        pass

    @property
    def SiteElevation(self):
        return True
    
    @SiteElevation.setter
    def SiteElevation(self, x):
        pass

    @property
    def SiteLatitude(self):
        return True
    
    @SiteLatitude.setter
    def SiteLatitude(self, x):
        pass
    
    @property
    def SiteLongitude(self):
        return True
        
    @SiteLongitude.setter
    def SiteLongitude(self, x):
        pass

    @property
    def Tracking(self):
        return True
        
    @Tracking.setter
    def Tracking(self, x):
        pass

    @property
    def Slewing(self):
        return False

    @Slewing.setter
    def Slewing(self, x):
        pass     

    def SlewToCoordinatesAsync(self, ra, dec):
        return True

class MockCamera:
    def __init__(self):
        print('[alpclient-status] creating MOCK camera')
    
    @property
    def Connected(self):
        return True

    @Connected.setter
    def Connected(self, x):
        pass

    @property
    def ImageReady(self):
        return True

    @ImageReady.setter
    def ImageReady(self, x):
        pass

    @property
    def ImageArray(self):
        return 'mock'

    @ImageArray.setter
    def ImageArray(self, x):
        pass

    def StartExposure(self, duration, light):
        return True