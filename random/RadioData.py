class RadioData:
    bitCastURLBase = "https://radio-locator.com"
    def __init__(self, state):
        self.state = state
        self.hasInfo = None
        self.infoURL = None
        self.hasBitcast = None
        self.bitcastURL = None
        self.callSign = None
        self.callSignURL = None
        self.freqNum = None
        self.am_fm = None
        self.city = None
        self.cityURL = None
        self.school = None
        self.format = None

    def returnAllData(self):
        return ([self.state, self.hasInfo, self.infoURL, self.hasBitcast, self.bitcastURL, self.callSign, self.callSignURL, self.freqNum, self.am_fm, self.city, self.cityURL, self.school, self.format])
    def setData(self, hasInfo=None, infoURL=None, hasBitcast=None, bitcastURL=None, callSign=None, callSignURL=None, freqNum=None, am_fm=None, city=None, cityURL=None, school=None, format=None):
        self.hasInfo = hasInfo
        self.infoURL = infoURL
        self.hasBitcast = hasBitcast
        self.bitcastURL = bitcastURL
        self.callSign = callSign
        self.callSignURL = callSignURL
        self.freqNum = freqNum
        self.am_fm = am_fm
        self.city = city
        self.cityURL = cityURL
        self.school = school
        self.format = format