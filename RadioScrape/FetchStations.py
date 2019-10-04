from RadioData import *
from radioDataBase import *
import urllib
import re
stateabbv = "state_abbrevs"


class FetchStations:
    def __init__(self, filename):
        self.filename = filename

    def createStateURL(self, state):
        baseBeginURL = 'https://radio-locator.com/cgi-bin/finder?state='
        baseEndURL = '&country=u&count=100&s=T&sr=1&is_ful=Y&is_lp=Y&prev=0'
        fullURL = baseBeginURL + state + baseEndURL

        return (fullURL)

    def fixHTML(self, html):
        capture = html[17] + "n"
        html = html.replace(capture, '\n')
        html = html[2:]
        return (html)

    def parseHTML(self, html, state):
        isMore = False

        #meaning radio-locator shuts of access
        if(html.find("You have exceeded")is not -1):
            return ([isMore, ["Access Shutdown"]])
        match = re.search(r'.*?Freq\.(.*?)page ', html, re.S)
        table = match.group(1)

        match = re.findall(r'<tr>(.*?)</tr>', table, re.S)
        radioList = []

        if(html.find('next">next')):
            isMore = True
        for radioSet in match:
            radioLines = re.findall(r'<td(.*?)</td>', radioSet, re.S)
            radioStation = RadioData(state)

            bitCastLine = radioLines[0]
            infoLine = radioLines[1]
            callSignLine = radioLines[2]
            frequencyLine = radioLines[3]
            cityLine = radioLines[4]
            schoolLine = radioLines[5]
            formatLine = radioLines[6]

            bitCast = 0
            bitCastURL = None

            info = 0
            infoURL = None

            radioCallSign = None
            radioURL = None

            frequency = None
            am_fm = None

            city = None
            cityURL = None

            school = None

            format = None

            search = re.search(r'href="(.*?)"', bitCastLine, re.S)
            if search:
                bitCast = 1
                bitCastURL = search.groups(1)
                bitCastURL = bitCastURL[0]

            search = re.search(r'href="(.*?)"', infoLine, re.S)
            if search:
                info = 1
                infoURL = search.groups(1)
                infoURL = infoURL[0]

            search = re.search('<b>(.*?)</b>', callSignLine, re.S)
            if search:
                radioCallSign = search.groups(1)
                radioCallSign = radioCallSign[0]
            search = re.search(r'href="(.*?)"', callSignLine, re.S)
            if search:
                radioURL = search.groups(1)
                radioURL = radioURL[0]

            search = re.findall(r'>(.*?)<', frequencyLine, re.S)
            if search:
                frequency = search[0]
                am_fm = search[1]

            search = re.search('href.*?>(.*?)</a>', cityLine, re.S)
            if search:
                city = search.groups(1)
                city = city[0]
            search = re.search(r'href="(.*?)"', cityLine, re.S)
            if search:
                cityURL = search.groups(1)
                cityURL = cityURL[0]

            search = re.search('>(.*?)<', schoolLine, re.S)
            if search:
                school = search.groups(1)
                school = school[0]

            search = re.findall('"max1">(.*?)<', formatLine, re.S)
            if search:
                format = search[0]

            radioStation.setData(hasInfo=info, infoURL=infoURL, hasBitcast=bitCast, bitcastURL=bitCastURL,
                                 callSign=radioCallSign, callSignURL=radioURL, freqNum=frequency, am_fm=am_fm,
                                 city=city,cityURL=cityURL, school=school, format=format)
            radioList.append(radioStation)
        return [isMore, radioList]

    def pullPageInfo(self, url, state):
        ##### ADD A TIMER
        html = urllib.request.urlopen(url)
        html = html.read()
        html = str(html)

        html = self.fixHTML(html)

        [isMore, radioList] = self.parseHTML(html, state)

        return [isMore, radioList]

    def nextPageURL(self, state, current_page):
        beginning = 'https://radio-locator.com/cgi-bin/finder?state='
        mid = '&country=u&count='
        mid2 = '&s=T&sr=1&is_ful=Y&is_lp=Y&prev='
        return (beginning+state+mid+str(current_page+100)+mid2+str(current_page))

    #create a dictionary {state:list[RadioData]}
    def getStationsByState(self, states_list):
        stateRadioDict = {}

        for state in states_list:
            current_page = 0
            more = True
            url = self.createStateURL(state)
            radioList = []
            while(more):
                [more, tempRadioList] = self.pullPageInfo(url, state)
                for i in tempRadioList:
                    if type(i) != RadioData:
                        return (stateRadioDict)
                    radioList.append(i)
                if more:
                    url = self.nextPageURL(state, current_page)
                    current_page += 100
            stateRadioDict[state] = radioList
        return stateRadioDict

    #return a list all state abbreviations
    def parseStateFile(self):
        FILEIN = open(self.filename, "r")
        states_in = FILEIN.read()
        FILEIN.close()

        stateList = states_in.split("\n")

        stationsByState = self.getStationsByState(stateList)

        return (stationsByState)




if __name__ == "__main__":
    stations = FetchStations(stateabbv)
    stationList = stations.parseStateFile()

    db = radioDataBase(stationList)
    db.write()

    #call = 'ABC'
    #for i in range(3):
    #    radioObj = RadioData("OH")
    #    radioObj.setData(hasInfo=1, infoURL='x.com', hasBitcast=1, bitcastURL='y.com', callSign=call,
    #                     callSignURL='z.com', freqNum='97.9', am_fm='FM', city='Dublin, OH', cityURL='h.com', school='Purdue', format='Rock')
    #    list.append(radioObj)
    #    call += 'C'
    #dict["OH"] = list