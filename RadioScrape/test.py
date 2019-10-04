import requests
import pycurl
import urllib
import mysql.connector
import matplotlib.path
import os.path
import re
import numpy as np
class radioPolygon:
    radioCoordinates = []
    fileLocation = ""
    matPath = None

    def __init__(self, filepath):
        if not os.path.isfile(filepath):
            raise (FileNotFoundError)

        self.fileLocation = filepath
        fileData = self.readFile()
        self.parseCoordinatesFromFile(fileData)

    def readFile(self):
        FIN = open(self.fileLocation, "r", re.M)
        data = FIN.read()
        FIN.close()
        return (data)

    def parseCoordinatesFromFile(self, fileData):
        groups = re.findall(r'> (.*?,.*?) \n', fileData)
        pointList = []

        for degree in range(360):
            coord = groups[degree]
            coord = coord.split(",")
            pointList.append((coord[0],coord[1]))
        self.radioCoordinates = pointList

        arr = np.array(pointList, dtype=np.float)
        path = matplotlib.path.Path(arr)
        self.matPath = path

    def testPointInsidePolygon(self, point):
        return (self.matPath.contains_point(point))


poly = radioPolygon("C:\\Users\\cellio02\\Pictures\\Radio FCC Data\\contourplot.txt")