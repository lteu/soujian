import csv
import sys
import time
import yaml
import os
import random

import statistics
from exp1 import *

def main(args):
	if len(args) <= 0:
		sys.exit("please launch with recc number, for example 10")

	# parameters
	random.seed(100)
	month_threshold = 2
	month_train = month_threshold/2
	number_of_folds = 5
	num_reccom = 20
	# ----
	start_time = time.time()

	filetoread= 'out2.csv'
	
	users = loadSQL2(filetoread)
	print("--- loaded in %s seconds ---" % (time.time() - start_time))
	
	iterate_dir = users

	test_users = {}

	# eliminate duplicates
	for key,item in iterate_dir.items():
		if checkTimeRange(key,item,month_threshold):
			test_users[key] = item

	
	user_ids = list(test_users.keys())
	partitioned = partition_shuffle(user_ids,number_of_folds)
	


	avgs = []

	

	num_reccom = int(args[0])

	for i in range(5):
		
		test_ids = partitioned[i]
		avg = oneFoldExp(test_ids,users,month_threshold,month_train,num_reccom)
		
		avgs.append(avg)
		# for i in range(0,5):
		# 	test_ids = partitioned[i]
		# 	avg = oneFoldExp(test_ids,users,month_threshold,month_train,num_reccom)
		# 	avgs.append(avg)
		print ('avg fold',1,'is',avg)
		print('number of users in consideration ',len(partitioned[0]),' with month set as ',month_threshold)
	

	print("--- Completed in %s seconds ---" % (time.time() - start_time))
	print('final for num recc',num_reccom,'is',statistics.mean(avgs))


if __name__ == '__main__':
  main(sys.argv[1:])