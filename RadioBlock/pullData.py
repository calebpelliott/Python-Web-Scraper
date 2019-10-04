from urllib import request
#from urllib import request

class dataRetriever:
    def __init__(self):
        self.SongName = "N\A"
        self.adStatus = "N\A"

    def fix_newline(self, html):
        place = len(html)
        i = 0
        while(place > 0):
            final = html[i]
            place = 0
            if html[i] is 'n' and html[i-1] is '\\' :
                part1 = html[0:i-1]
                part2 = html[i+1:]
                html = part1 + "\n" + part2
                print("i:"+str(i))
                print(len(html))
        return (html)

    def pullURL(self, url):
        with request.urlopen('http://python.org/') as response:
            html = response.read()
            this = response.info()
        self.fix_newline(str(html))

tester = dataRetriever()

with request.urlopen('http://python.org/') as response:
   html = response.read()
   this = response.info()

tester.fix_newline(str(html))

#x = 3
with open("datatest.html", "w") as FILEOUT:
    FILEOUT.write(html)

#with open("data2.html", "w") as FILEOUT:
#    FILEOUT.write(str(this))