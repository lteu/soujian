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
		# print(key,item)
		user_seach_day = {}
		for anItem in search:
			# anItem=search[0]
			w = anItem[0]
			day = anItem[1]
			existance = anItem[2]
			dbid = anItem[3]
			user_seach_day[day] =  1 if day not in user_seach_day else user_seach_day[day] + 1
			# if day not in user_seach_day:
			# 	user_seach_day[day] = 1
			# else:
			# 	user_seach_day[day] = 1
		# user_seach_day.items()
		usersdayInList = list(user_seach_day.items())
		usersdayInList.sort(key=lambda x:x[1],reverse=True)
		user_dialy.append([usersdayInList[0][1],userid,usersdayInList[0][0]])
		# print(usersdayInList[0][1])
		# sys.exit()


	user_dialy.sort(key=lambda x:x[0])
	print(user_dialy)

	search_rank = [x[0] for x in user_dialy]
	print(search_rank)
	print(statistics.mean(search_rank))
	sys.exit()

	iterate_dir = users
	usersInList = list(users.items())
	usersInList.sort(key=lambda x:len(x[1]))


	print("--- sorted in %s seconds ---" % (time.time() - start_time))


	number_of_words = 0
	for userprofile in usersInList:
		print (userprofile[1])
		sys.exit()
		number_of_words += len(userprofile[1])


	print('=== report stats ====')
	num_of_users = len(users.keys())
	print('num of users:',num_of_users)
	print('num of words:',number_of_words)
	print('avg word per user:',number_of_words/num_of_users)
	median_user_index = int(num_of_users/2)
	print('median word per user:',len(usersInList[median_user_index][1]))
	print('==============')

	# print ('normed user id and search frequency')
	# counter = 1
	# list_count=[]
	# for userinfo in usersInList:
	# 	userid = userinfo[0]
	# 	words = userinfo[1]
	# 	list_count.append(len(words))
	# 	# print (counter,len(words))
	# 	counter += 1
	# print(list_count)



if __name__ == '__main__':
  main(sys.argv[1:])