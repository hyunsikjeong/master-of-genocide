# master-of-genocide
Find/Calculate statistics of GENOCIDE hakkyou vote.

Made by rbtree( http://github.com/jhs7jhs / https://twitter.com/RBTree_Pg )

F you, CP932 and Shift-JIS.

* What is GENOCIDE hakkyou vote?: http://nekokan.dyndns.info/~lobsak/genocide/about.html

#### In the Future:
- GENOCIDE新規提案投票状況 automatical recording https://goo.gl/JZyPdC
- Sort flags

#### Requirement:
- Beautiful Soup 4(http://www.crummy.com/software/BeautifulSoup/)
- Python 3x

## History

#### Version 0.8:
* History log feature added.
    * Voting status is printed in status.csv / History in history.csv
	* teian flag '-teian' for printing suggestion date data
        * example(in command line): python main.py -teian

#### Version 0.7:
* Using CP932 now, and it works nicely. (Do not confuse Shift-JIS with CP932, seriously.)

#### Version 0.6.6:
* sort by median(level) value

#### Version 0.6.5:
* csv issues fixed
    * using csv lib now!
	* encoding changed from utf-8 to utf-8-sig (utf-8 w/ BOM)
* By the rule of hakkyou vote, program calculates the high median.

#### Version 0.6:
* '--date' flag:
    * w/ flag: start date and end date would be args
        * example(in command line): python main.py --date 2015/11/07 2015/11/27
    * w/o flag: automatically load from DATE.txt (check the DATE.txt)
* BAN list:
    * put LR2ID in the BLACKLIST.txt to except players from the vote counting

#### Version 0.5:
* suggStart, voteStart, voteEnd values should be manually changed by users.
* output will be stored in output.csv (csv file format)
* may contain many bugs...