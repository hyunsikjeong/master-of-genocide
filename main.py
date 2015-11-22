# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from bs4 import element
from urllib.request import urlopen
import statistics
import datetime
import re
import unicodedata
import argparse
import csv
import codecs

mainUrl = "http://www.dream-pro.info/~lavalse/LR2IR/"

argParser = argparse.ArgumentParser(description='Date Arguments')
argParser.add_argument('--date', metavar='date', nargs=2, help = 'vote start date / end date')
args = argParser.parse_args()

#convert string "YYYY/MM/DD" to datetime.date(YYYY, MM, DD).
#avoiding strftime and strptime
def convertToDate(dateString):
    dateList = dateString.split("/")
    return datetime.date(int(dateList[0]), int(dateList[1]), int(dateList[2]))

if args.date is None or len(args.date)!=2:
    try:
        dateFile = open('DATE.txt','r')
        suggStart = convertToDate(dateFile.readline())
        voteEnd = convertToDate(dateFile.readline())
        dateFile.close()
    except:
        print("Failed to load the start/end date(DATE.txt)")
        exit()
else:
    suggStart = convertToDate(args.date[0])
    voteEnd = convertToDate(args.date[1])

blackList=set()

def makeBlackList():
    try:
        file = open('BLACKLIST.txt','r')
        while True:
            line = file.readline()
            if line == '':
                break
            blackList.add( str(int(line)) )
        file.close()
    except:
        print("Failed to read the Black List(BLACKLIST.txt)")




#check whether a comment has correct form
#return value :
#-1: No / 0: Nothing / 1~: Yes, with difficulty
def checkComment(comment):
    checkNo = re.compile("^\(20[0-9]{2}\/([1-9]|0[1-9]|1[12])\/([1-9]|[012][0-9]|3[01])\) *$")
    checkYes = re.compile("^\(20[0-9]{2}\/([1-9]|0[1-9]|1[12])\/([1-9]|[012][0-9]|3[01])\) ?★([1-9]|1[0-9]|2[0-5])(| .*)$")
    try:
        if checkNo.match(comment):
            commentDate = convertToDate(comment[1:comment.find(")")])
            if suggStart <= commentDate and commentDate <= voteEnd:
                return -1
            else:
                return 0
        elif checkYes.match(comment):
            commentDate = convertToDate(comment[1:comment.find(")")])
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
            # kinda dangerous part. check whether it's players' data table or not
            if len(pageTable[0].find_all('th'))!=17:
                break;
            for j in range(1, len(pageTable),2):
                dataRow = pageTable[j]
                commentRow = pageTable[j+1]
                #check black list
                playerID = re.search('[0-9]+',dataRow.a['href']).group(0)
                if playerID in blackList:
                    continue
                #replace fullwidth(Em-size) characters with halfwidth characters
                comment = unicodedata.normalize("NFKC", commentRow.td.string or "")
                checkVal = checkComment(comment)
                if checkVal==-1:
                    no = no+1
                elif checkVal>0:
                    yes = yes+1
                    yesarr.append(checkVal)
            i = i+1
        med = 0
        if len(yesarr):
            med = statistics.median_high(yesarr)
        return (yes, no, med)
    except:
        print("Failed to load the IR page: " + aUrl)
def main():
    makeBlackList()
    try:
        output = open('output.csv','w', encoding='utf-8-sig', newline='')
        #output.write(codecs.BOM_UTF8)
        outputWriter = csv.writer(output)
        outputWriter.writerow(["Name", "Yes", "No", "Median"])
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
                        outputWriter.writerow([lList[2].a.string, res[0], res[1], res[2]])
        except:
            print("Failed to load the ★50 Table")

        output.close()
    except:
        print("Failed to write the file")
        return


main()
