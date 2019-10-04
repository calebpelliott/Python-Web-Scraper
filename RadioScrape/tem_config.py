import re
docpath = "C:\\Users\\cellio02\\ABI\\applications\\TEM_VAST\\sn03\\TEM\\VAST_Tem_Config.cfgt"
tagtochange = "resourceName"
iterable = True

infile = open(docpath, "r")
data = infile.read()
infile.close()

tag = "<" + tagtochange + ">"
tagList = data.split(tag)
count = 0
new = []
new.append(tagList[0])
for i in tagList[1:]:
    ending = i[i.find("/"+tagtochange):]
    ending = "<" + ending
    if count < 2 :
        temp =tag + "VAST PICOAMM " + str(count+1) + ending
        new.append(temp)
    else:
        temp =tag + "VAST PS " + str(count-1) + ending
        new.append(temp)
    count+=1
new_string = ""
for i in new:
    new_string += i
print(new_string)
outfile = open("C:\\Users\\cellio02\\ABI\\applications\\TEM_VAST\\sn03\\TEM\\VAST_Tem_Config.cfgt2", "w")
outfile.write(new_string)
outfile.close()