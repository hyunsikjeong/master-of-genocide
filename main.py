from bs4 import BeautifulSoup
from bs4 import element
from urllib.request import urlopen
import statistics
import datetime
import re

mainUrl = "http://www.dream-pro.info/~lavalse/LR2IR/"
#I'll gonna make some functions for importing suggestion start date and vote start/end date later.
suggStart = datetime.date(2015, 11, 7)
voteStart = datetime.date(2015, 11, 9)
voteEnd = datetime.date(2015, 11, 27)

#replace fullwidth(Em-size) characters with halfwidth characters
def replaceEm(comment):
    if comment is None:
        return ""
    else:
        replaceList = [('１','1'),('２','2'),('３','3'),('４','4'),('５','5'),('６','6'),('７','7'),('８','8'),('９','9'),('０','0'),('（','('),('）',')'),('　',' ')]
        for replaceSet in replaceList:
            comment = comment.replace(replaceSet[0], replaceSet[1])
        return comment

#convert string "YYYY/MM/DD" to datetime.date(YYYY, MM, DD).
#avoiding strftime and strptime
def convertToDate(dateString):
    dateList = dateString.split("/")
    return datetime.date(int(dateList[0]), int(dateList[1]), int(dateList[2]))

#check whether a comment has correct form
#return value :
#-1: No / 0: Nothing / 1~: Yes, with difficulty
def checkComment(comment):
    checkNo = re.compile("^\(20[0-9]{2}\/([1-9]|0[1-9]|1[12])\/([1-9]|[012][0-9]|3[01])\) *$")
    checkYes = re.compile("^\(20[0-9]{2}\/([1-9]|0[1-9]|1[12])\/([1-9]|[012][0-9]|3[01])\) ?★([1-9]|1[0-9]|2[0-5])(| .*)$")
    try:
        if checkNo.match(comment) is not None:
            temp = comment.find(")")
            commentDate = convertToDate(comment[1:temp])
            if suggStart <= commentDate and commentDate <= voteEnd:
                return -1
            else:
                return 0
        elif checkYes.match(comment) is not None:
            temp = comment.find(")")
            commentDate = convertToDate(comment[1:temp])
            if suggStart <= commentDate and commentDate <= voteEnd:
                difficulty = re.search("★(1[0-9]|2[0-5]|[1-9])", comment)
                return int(difficulty.group(1))
            else:
                return 0
        else:
            return 0
    except:
        print("Failed to check the comment: " + comment)
        return 0
#calculate the yes / no / median of one pattern
def getRate(aUrl):
    irUrl = mainUrl + aUrl
    i = 1
    yes = 0
    no = 0
    yesarr = []
    try:
        while True: #traveling pages
            pageSoup = BeautifulSoup(urlopen(irUrl+"&page="+str(i)), 'html.parser')
            pageTables = pageSoup.body.div.div.find_all('table')
            pageTable = pageTables[len(pageTables)-1].find_all('tr')
            # kinda dangerous part. check whether there's players' data table or not
            if len(pageTable[0].find_all('th'))!=17: 
                break;
            for it in pageTable:
                pageList = it.find_all('td')
                if len(pageList)==1:
                    #for black list feature in future, use previous_sibling here
                    comment = replaceEm(pageList[0].string)
                    checkVal = checkComment(comment)
                    if checkVal==-1:
                        no = no+1
                    elif checkVal>0:
                        yes = yes+1
                        yesarr.append(checkVal)
            i = i+1
        med = 0
        if len(yesarr):
            med = statistics.median(yesarr)
        return (yes, no, med)
    except:
        print("Failed to load the IR page: " + aUrl)
def main():
    try:
        output = open('output.csv','w', encoding='UTF-8')
        output.write("Name,Yes,No,Median\n")
        try:
            lv50Url = mainUrl + 'search.cgi?mode=search&type=insane&exlevel=50&7keys=1'
            lv50Soup = BeautifulSoup(urlopen(lv50Url), 'html.parser')
            lv50Table = lv50Soup.body.div.div.table

            for lChild in lv50Table.children:
            # There could be some white-space NavigateStrings.
                if isinstance(lChild, element.Tag):
                    lList = lChild.find_all('td')
                    if len(lList):
                        res = getRate(lList[2].a['href'])
                        output.write('"' + lList[2].a.string + '",'+str(res[0]) + ',' + str(res[1]) + ',' + str(res[2]) + '\n')
                        #output.write(lList[2].a.string + " Yes: " + str(res[0]) + " No: " + str(res[1]) + " Median : " + str(res[2]) +"\n")
        except:
            print("Failed to load the ★50 Table")
        
        output.close()
    except:
        print("Failed to write the file")
        return
    

main()
