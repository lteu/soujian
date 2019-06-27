"""
A prototype 
"""

import csv
import sys
import time
import yaml
import os

root_arr = os.path.realpath(__file__).split('/')[:-2]
root = '/'.join(root_arr+['src']) 
sys.path.append(root)

import statistics
from wtoolkit import *


def main(args):

	start_time = time.time()

	root_arr = os.path.realpath(__file__).split('/')[:-2]
	datadir = '/'.join(root_arr+['data']) 
	filetoread= datadir+'/out2.csv'

	users = loadSQL2(filetoread)

	print("--- loaded in %s seconds ---" % (time.time() - start_time))


	user_dialy = []
	for userid,search in users.items():
		# loop users record to find max daily search
		user_seach_day = {}
		for anItem in search:
			w = anItem[0]
			day = anItem[1]
			existance = anItem[2]
			dbid = anItem[3]
			user_seach_day[day] =  1 if day not in user_seach_day else user_seach_day[day] + 1

		usersdayInList = list(user_seach_day.items())
		usersdayInList.sort(key=lambda x:x[1],reverse=True)
		user_dialy.append([usersdayInList[0][1],userid,usersdayInList[0][0]])


	user_dialy.sort(key=lambda x:x[0])
	print(user_dialy)

	search_rank = [x[0] for x in user_dialy]
	print(search_rank)
	print(statistics.mean(search_rank))


if __name__ == '__main__':
  main(sys.argv[1:])