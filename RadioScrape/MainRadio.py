import re
from bs4 import BeautifulSoup
from selenium import webdriver
from radioStation import *
import copy
import io
def parseFile(filepath):
    FIN = open(filepath, encoding="utf8")
    file = FIN.read()
    FIN.close()

    allLines = file.split("\n")
    listOfStations = []

    #Data: Call   Channel   Class   Frequency   Status    City   State Country  FileNumber      Docket   FacilityID       ERP      HAAT    Licensee/Permittee
    for line in allLines:
        radioData = []

        #We're first going to split the line on state and country. Easy format.
        groups = re.match(r'.*?  ([A-Za-z]{2} [A-Za-z]{2})  .*?', line)
        if groups is None:
            print("Should never see this, regex is broken")
            c = 0/0
        group = groups.group(1)
        splitLine = line.split(group)
        state_and_country = group.strip()
        state_and_country = state_and_country.split(" ")
        state = state_and_country[0]
        country = state_and_country[1]

        #Find info left of state and country
        leftInfo = re.findall(r'(.*?) +(.*?) +(.*?) +(.*?) +(.*?) +(.*?) +(.*?) +(.*)', splitLine[0])
        #Access the tuple
        leftInfo = leftInfo[0]

        #Find info left of state and country
        rightInfo = re.findall(r' *(.*?) +(.*?) +(.*?) +(.*?) +(.*?) +(.*?) +(.*?) +(.*)', splitLine[1])
        #Access the tuple
        rightInfo = rightInfo[0]

        allData = list(leftInfo)
        allData.append(state)
        allData.append(country)
        allData += list(rightInfo)

        for data in allData:
            radioData.append(data.strip())

        listOfStations.append(radioData)

    return (listOfStations)

def printListAsString(list):
    tmp = ""
    for radio in list:
        tmp += radio.getRadioString(" | ")
        tmp += "\n"
    return tmp

def createStations(listOfStations):
    radioList = []
    for radioInfo in listOfStations:
        radioList.append(radioStation(radioInfo))

    radioPurge = []

    #Throw out all stations with ERP of "-". Means it doesn't ouptut anything
    for radio in radioList:
        if '-' not in radio.getERP():
            radioPurge.append(radio)
    radioList = radioPurge

    radioPurge = []
    for radio in radioList:
        if 'FS' not in radio.getService():
            radioPurge.append(radio)

    radioList = radioPurge

    searchList = copy.deepcopy(radioList)
    identicalList = []
    i = 0
    uniqueList = []

    while(len(searchList)>0):
        for radio in searchList:
            unique = 1
            for radio2 in searchList:
                tmp1 = radio.getFacilityID()
                tmp2 = radio.getFacilityID()

                if (radio.getFacilityID() == radio2.getFacilityID() and not radio.allMatch(radio2) and (radio.getFrequency == radio2.getFrequency)):
                    identicalList.append(radio)
                    identicalList.append(radio2)
                    unique = 0

            if (unique == 1):
                uniqueList.append(radio)
            searchList.remove(radio)
            #Rebuild searchList for loop
            print("done " + str(i))
            i+=1
            break

    identStr = printListAsString(identicalList)
    uniqueStr = printListAsString(uniqueList)

    with io.open("C:\\Users\\cellio02\\Pictures\\Radio FCC Data\\identicalRadios.txt", "w", encoding="utf-8") as f:
        f.write(identStr)


    with io.open("C:\\Users\\cellio02\\Pictures\\Radio FCC Data\\uniqueRadios.txt", "w", encoding="utf-8") as f:
        f.write(uniqueStr)
    return uniqueList

def crawlFCCdata(radioList):
    for radio in radioList:
        if radio.getCallSign() is not '-' :
            radio.downloadContourTxt()

def loadStations(path):
    with open(path, "r", encoding="utf=8") as f:
        data = f.read()

    data = data.split("\n")
    radioList = []

    for radio in data:
        radioInfo = radio.split(" | ")
        radioList.append(radioStation(radioInfo))

    return radioList

def main(filepath):
    #listOfStations = parseFile(filepath)
    #listOfRadioStations = createStations(listOfStations)
    listOfRadioStations = loadStations("C:\\Users\\ellio\\Music\\radio\\uniqueRadios.txt")
    crawlFCCdata(listOfRadioStations)





main("C:\\Users\\cellio02\\Pictures\\AllRadiosList.xml")