import re
from RadioData import *

FILEIN = open("goog2.html", "r")
html = FILEIN.read()
FILEIN.close()

match = re.search(r'.*?Freq\.(.*?)page ', html, re.S)
table = match.group(1)

match = re.findall(r'<tr>(.*?)</tr>', table, re.S)
radioList = []
for radioSet in match:
    radioLines = re.findall(r'<td(.*?)</td>', radioSet, re.S)
    radioStation = RadioData("OH")

    bitCastLine = radioLines[0]
    infoLine = radioLines[1]
    callSignLine = radioLines[2]
    frequencyLine = radioLines[3]
    cityLine = radioLines[4]
    schoolLine = radioLines[5]
    formatLine = radioLines[6]

    bitCast = False
    bitCastURL = None

    info = False
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
        bitCast = True
        bitCastURL = search.groups(1)
        bitCastURL = bitCastURL[0]

    search = re.search(r'href="(.*?)"', infoLine, re.S)
    if search:
        info = True
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

    radioStation.setData(info, infoURL, bitCast, bitCastURL, radioCallSign, radioURL, frequency, am_fm, city, cityURL, school, format)
    radioList.append(radioStation)

x=3



