"""
This file refines the generated out.csv
it leaves only the user records who have searched more than 10 words during a year,
and only the found words are left
"""

import csv
import sys
import time
import yaml
import os
from wtoolkit import *


def main(args):

	start_time = time.time()

	root_arr = os.path.realpath(__file__).split('/')[:-2]
	datadir = '/'.join(root_arr+['data']) 

	filetoread= datadir+'/out.csv'
	loaded_users = loadSQL2(filetoread)

	print("--- loaded in %s seconds ---" % (time.time() - start_time))

	iterate_dir = loaded_users
	users = {}
	for key,item in iterate_dir.items():
		
		# filter out not found
		items_new = [x for x in item if int(x[2]) == 1]
		
		# filter out users belown x items
		if len(items_new) <= 10:
			continue

		users[key] = items_new


	usersInList = list(users.items())
	usersInList.sort(key=lambda x:len(x[1]))


	print("--- sorted in %s seconds ---" % (time.time() - start_time))

	number_of_words = 0
	for userprofile in usersInList:
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
	# 	print (counter,len(words))
	# 	counter += 1
	# print(list_count) # for plot


	# PRINT csv file
	out_file = datadir+'/out2.csv'
	print('Printing CSV file ...',out_file)
	writer = csv.writer(open(out_file, 'w'), delimiter = ';')
	for userinfo in usersInList:
		row = ''
		userid = userinfo[0]
		# if userid == '825':
		# 	sys.exit('found')
		words = userinfo[1]
		for w in words:
			writer.writerow([str(userid),str(w[0]),str(w[1]),str(w[2]),str(w[3])])
	print("--- %s seconds ---" % (time.time() - start_time))




if __name__ == '__main__':
  main(sys.argv[1:])