from bs4 import BeautifulSoup
from selenium import webdriver
import re
import shutil
import time
import os
import random
from selenium.webdriver.chrome.options import Options

class radioStation:
    CallSign = ""
    Channel = ""
    Class = ""
    Frequency = ""
    Service = ""
    Status = ""
    City = ""
    State = ""
    Country = ""
    FileNumber = ""
    Docket = ""
    FacilityID = ""
    ERP = ""
    HAAT = ""
    LinceseePermittee = ""

    contourKML_File = ""
    baseRadioURL = "https://transition.fcc.gov/fcc-bin/fmq?list=0&facid="
    fullRadioURL = ""
    kmlURL = ""

    def __init__(self, dataList):
        # Data: Call   Channel   Class  Service  Frequency   Status    City   State Country  FileNumber      Docket   FacilityID       ERP      HAAT    Licensee/Permittee
        if len(dataList) == 16 :
            self.CallSign = dataList[0]
            self.Channel = dataList[1]
            self.Class = dataList[2]
            self.Service = dataList[3]
            self.Frequency = dataList[4]
            self.Status = dataList[5]
            self.City = dataList[6]
            self.State = dataList[7]
            self.Country = dataList[8]
            self.FileNumber = dataList[9]
            self.Docket = dataList[10]
            self.FacilityID = dataList[11]
            self.ERP = dataList[12]
            self.HAAT = dataList[13]
            self.LinceseePermittee = dataList[14]
            self.fullRadioURL = self.baseRadioURL + self.FacilityID
            self.fileCount = 0
            return

        self.CallSign = dataList[0]
        self.Channel = dataList[1]
        self.Class = dataList[2]
        self.Service = dataList[3]
        self.Frequency = dataList[4] + " " + dataList[5]
        self.Status = dataList[6]
        self.City = dataList[7]
        self.State = dataList[8]
        self.Country = dataList[9]
        self.FileNumber = dataList[10]
        self.Docket = dataList[11]
        self.FacilityID = dataList[12]
        self.ERP = dataList[13] + " " + dataList[14]
        self.HAAT = dataList[15] + dataList [16]
        self.LinceseePermittee = dataList[17]
        self.fullRadioURL = self.baseRadioURL + self.FacilityID
        #self.getKMLURL()

        self.kmlURL = ""
        self.fileCount = 0

    def downloadContourTxt(self):
        print("Downloading file for " + self.CallSign)
        fileList = self.getKMLURL()

        #Move it from downloads to project directory.
        projectDir = "C:\\Users\\ellio\\Music\\radio\\contourplots"
        destLocation = projectDir + os.sep + self.CallSign


        try:
            os.mkdir(destLocation)
        except:
            print(self.CallSign + " already made")
            numOfFiles = len([name for name in os.listdir(destLocation) if os.path.isfile(name)])
            self.fileCount = numOfFiles
        for file in fileList:
            fileName = self.CallSign + self.Frequency + " " + str(self.fileCount)
            self.fileCount += 1
            finalLocation = destLocation + os.sep + fileName
            try:
                with open(finalLocation, "w", encoding="utf-8") as f:
                    f.write(file)
                print(fileName + " printed")
            except:
                print("Couldn't write: " + fileName)
        time.sleep(random.randint(10,12))

    def getKMLURL(self):
        WINDOW_SIZE = "1920,1080"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        #chrome_options.binary_location = CHROME_PATH

        driver = webdriver.Chrome(executable_path="C:\\Users\\ellio\\Music\\radio\\chromedriver.exe", chrome_options=chrome_options)
        driver.get(self.fullRadioURL)
        html = driver.page_source
        soup = BeautifulSoup(html)

        group = re.findall(r'.*?Service contour plotted on a regional KML file in a new browser window.*?"(https.*?)"', html, re.M|re.S)

        #Removes unwanted .kml files
        txtList = []
        for i in group:
            if ".txt" in i:
                txtList.append(i)

        htmlList = []
        for file in txtList:
            driver.get(file)
            html = driver.page_source
            htmlList.append(html)
        driver.close()
        newList = self.removeOtherFreq(htmlList)
        return newList

    def removeOtherFreq(self, htmlList):
        new = []
        for file in htmlList:
            if self.Frequency in file:
                new.append(file)
        return new

    def getFacilityID(self):
        return (self.FacilityID)

    def getERP(self):
        return (self.ERP)

    def getService(self):
        return (self.Service)
    def getMembersAsList(self):
        return ([self.CallSign,
        self.Channel,
        self.Class,
        self.Service,
        self.Frequency,
        self.Status,
        self.City,
        self.State,
        self.Country,
        self.FileNumber,
        self.Docket,
        self.FacilityID,
        self.ERP,
        self.HAAT,
        self.LinceseePermittee])

    def allMatch(self, radio):
        if self.getMembersAsList() == radio.getMembersAsList():
            return True
        return False
    def getRadioString(self, delimeter):
        tmp = ""
        for member in self.getMembersAsList():
            tmp += member
            tmp += delimeter
        return tmp

    def getFrequency(self):
        return self.Frequency

    def getCallSign(self):
        return self.CallSign