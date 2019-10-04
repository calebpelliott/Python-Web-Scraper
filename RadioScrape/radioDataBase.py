import mysql.connector

class radioDataBase:
    radioDict = {}

    def __init__(self, dict):
        self.radioDict = dict

    def write(self):
        connection = mysql.connector.connect(user="root", password="root", host="127.0.0.1", database="radiodata")
        cursor = connection.cursor()
        add_station = ("INSERT INTO radio_node "
                       "(callSign, callSignURL, hasInfo, infoURL, hasBitcast, bitcastURL, frequency, am_fm, city, cityURL, school, format, state) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        for i in self.radioDict:
            for j in self.radioDict[i]:
                data = j.returnAllDataDbFormat()
                cursor.execute(add_station, data)
        connection.commit()
        cursor.close()
        connection.close()
