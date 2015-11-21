# master-of-genocide
Find yes/no/median values of genocide hakkyou vote.
Made by rbtree( http://github.com/jhs7jhs / https://twitter.com/RBTree_Pg )
* Unicode issue will be resolved in the future

Requirement:
- Beautiful Soup 4(http://www.crummy.com/software/BeautifulSoup/)
- Python 3x

Version 0.6:
- '--date' flag:
	w/ flag: start date and end date would be args
		example(in command line): python main.py --date 2015/11/07 2015/11/27
	w/o flag: automatically load from DATE.txt (check the DATE.txt)
- BAN list:
	put LR2ID in the BLACKLIST.txt to except players from the vote counting

Version 0.5:
- suggStart, voteStart, voteEnd values should be manually changed by users.
- output will be stored in output.csv (csv file format)
- may contain many bugs...