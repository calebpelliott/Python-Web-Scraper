import requests
import pycurl
import urllib
import mysql.connector



connection = mysql.connector.connect(user="root", password = "root", host="127.0.0.1",database="radiodata")
cursor = connection.cursor()

add_station = ("INSERT INTO radio_node "
               "(callSign, callSignURL, hasInfo, infoURL, hasBitcast, bitcastURL, frequency, am_fm, city, cityURL, school, format) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
data = ('ABC', 'x.com', 1, 'y.com', 1, 'z.com', '97.9', 'FM', 'Dublin, OH', 'h.com', 'Purdue', 'Rock')
cursor.execute(add_station, data)
connection.commit()
cursor.close()
connection.close()
x = urllib.request.urlopen("https://radio-locator.com/cgi-bin/finder?state=OH&country=u&count=1000&s=T&sr=1&is_ful=Y&is_lp=Y&prev=0")
q = x.read()
t = str(q)
print(q)
print(t)

cap = t[1]
cap2 = t[17]+"n"
done = True
asd = t.replace(cap2,"\n")
asd = asd[2:]

FILE = open("goog.html","w")
FILE2 = open("goog2.html","w")
FILE2.write(asd)
#FILE.write(q)
r = requests.get("https://radio-locator.com/cgi-bin/finder?state=OH&country=u&count=1000&s=T&sr=1&is_ful=Y&is_lp=Y&prev=0")
x = r.status_code
print(x)