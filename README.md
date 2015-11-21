# master-of-genocide
Find yes/no/median values of genocide hakkyou vote.
Made by rbtree( http://github.com/jhs7jhs / https://twitter.com/RBTree_Pg )
* Unicode issue will be resolved in the future

Requirement:
- Beautiful Soup 4(http://www.crummy.com/software/BeautifulSoup/)
- Python 3x

Version 0.6:
1. '--date' flag:
	1. w/ flag: start date and end date would be args
		* example(in command line): python main.py --date 2015/11/07 2015/11/27
	2. w/o flag: automatically load from DATE.txt (check the DATE.txt)
2. BAN list:
	* put LR2ID in the BLACKLIST.txt to except players from the vote counting

Version 0.5:
1. suggStart, voteStart, voteEnd values should be manually changed by users.
2. output will be stored in output.csv (csv file format)
3. may contain many bugs...