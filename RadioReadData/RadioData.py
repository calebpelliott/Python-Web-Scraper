import os

class RadioData:
    def __init__(self, filepath):
        dataList = self.readAllFiles(filepath)

    def readAllFiles(self, filepath):
        for dirName, subdirList, fileList in os.walk(filepath):
            for file in fileList:
               with open(dirName + os.sep + file) as data:
                   self.parseData(data.read(), dirName)

    def parseData(self, data, dirName):

        MHz = ""

