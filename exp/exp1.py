'''
This exp aims to understand long-term prediction.
Let's say, 2 months for user profile features and 4 month for prediction

data structure:

userid - 	[
				[word1,thedate,ifexist],
				[word2,thedate,ifexist],
	  			...
  			]

'''

import csv
import sys
import time
import yaml
import os
import random

import statistics

root_arr = os.path.realpath(__file__).split('/')[:-2]
root = '/'.join(root_arr+['src']) 
sys.path.append(root)

from wtoolkit import *


def dateToDays(aDate):
	days = (int(str(aDate)[4:6])-1)*30 + int(str(aDate)[-2:])
	return days

def checkTimeRange(userid,item,month_threshold):
	item.sort(key=lambda x:x[1])
	initial_date = dateToDays(item[0][1])
	end_date = dateToDays(item[-1][1])

	if (end_date-initial_date)/30 >= month_threshold:
		return True
	else:
		return False

	# print (dateToDays(initial_date),dateToDays(end_date))
	# sys.exit()

def partition_shuffle(lst, number_of_folds):
	'''
	Random partition
	'''
	n = number_of_folds
	random.shuffle(lst)
	division = len(lst) / float(n)
	return [ lst[int(round(division * i)): int(round(division * (i + 1)))] for i in range(n) ]

# def divideSearchByDate(info):

def separateSearchesByTime(info,month_train):
	initial_date = dateToDays(info[0][1])
	initial_train_date = initial_date + month_train*30
	# print(initial_date,initial_train_date)
	first_part = []
	second_part = []
	for item in info:
		if dateToDays(item[1]) >= initial_date and dateToDays(item[1]) <= initial_train_date:
			first_part.append(item)
		else:
			second_part.append(item)
	return first_part,second_part

def extTestUsersInfo(target_users,month_train):
	test_instances ={}
	test_ground={}
	for userid,info in target_users.items():
		first_part,second_part = separateSearchesByTime(info,month_train)
		test_instances[userid] = first_part
		test_ground[userid] = second_part

	return test_instances,test_ground

def getSimilarityScore(user_words,tmp_words,userid):
	eff_user_words = [x[0] for x in user_words]
	eff_tmp_words = [x[0] for x in tmp_words]
	occurrence = [x for x in eff_user_words if x in eff_tmp_words]
	return len(occurrence) / len(user_words)

def findNeighbourhood(current_userid,list_words,context_users,neigh_size=30):
	rank = []
	# print (context_users[3320])
	for userid,info in context_users.items():
		tmpScore = getSimilarityScore(list_words,info,userid)
		if tmpScore > 0:
			rank.append([userid,tmpScore])

	rank.sort(key=lambda x:x[1],reverse=True)
	rank = rank[:neigh_size]
	return rank

def findRecommendationFromNeigh(num_reccom,user_words,neigh,context_users):
	stats = {}
	eff_user_words = [x[0] for x in user_words]
	for usr in neigh:
		uid = usr[0]
		searched = context_users[uid]
		for wordentry in searched:
			wd = wordentry[0]
			if wd in eff_user_words:
				continue
			if wd not in stats:
				stats[wd] = 1
			else:
				stats[wd] += 1

	statsInList = list(stats.items())
	statsInList.sort(key=lambda x:x[1],reverse=True)
	recommended = statsInList[:num_reccom]

	#debug
	if len(recommended) == 0:
		print('debug msg: recommended words - nought, neigh found',len(neigh))
	return recommended


def predictionMatchingScore(userid,recommended,user_ground):
	words_rec = [x[0][:-1] for x in recommended]
	words_grd = set([x[0][:-1] for x in user_ground])
	words_guessed = []
	words_guessed = [x for x in words_rec if x in words_grd]
	if len(words_rec) == 0:
		sys.exit('0 recommendation occured for user with ID '+ str(userid))
	# precision = len(words_guessed)/len(words_rec)
	
	# comparison with QCER
	com_divisor = min(len(words_grd),len(recommended))
	precision = len(words_guessed)/com_divisor

	return precision
	# print (precision)

def predictWords(test_instances,test_ground,context_users,num_reccom, ifPrint):
	stack = []
	for userid,info in test_instances.items():

		if len(info) < num_reccom or len(test_ground[userid]) < num_reccom:
			continue
		
		neigh = findNeighbourhood(userid,info,context_users)
		
		recommended = findRecommendationFromNeigh(num_reccom,info,neigh,context_users)
		
		if ifPrint:
			print(recommended)

		if len(recommended)==0: # if cannot be predicted 
			continue
			
		# print(recommended)
		precision = predictionMatchingScore(userid,recommended,test_ground[userid])
		

		# print(precision)
		stack.append(precision)

	# print('stack',stack)
	return stack


def oneFoldExp(test_ids,full_users,month_threshold,month_train,num_reccom,inspect=''):
	context_users = {**full_users}
	target_users = {}

	# firstly, create test profiles
	for target_id in test_ids:
		target_users[target_id] = full_users[target_id]
		del context_users[target_id]

	# secondly, extract test user info

	test_instances,test_ground = extTestUsersInfo(target_users,month_train)

	# inspection
	ifPrint=False
	if inspect != '':
		content = test_instances[inspect]
		test_instances =  {inspect:content}
		content = test_ground[inspect]
		test_ground = {inspect:content}
		ifPrint=True
	stack = predictWords(test_instances,test_ground,context_users,num_reccom,ifPrint=ifPrint)
	# print(stack)
	return statistics.mean(stack)

def main(args):
	if len(args) <= 0:
		sys.exit("please launch with fold number, for example 0-4")

	# parameters
	random.seed(100)
	month_threshold = 2
	month_train = month_threshold/2
	number_of_folds = 5
	num_reccom = 20
	# ----
	start_time = time.time()

	root_arr = os.path.realpath(__file__).split('/')[:-2]
	datadir = '/'.join(root_arr+['data']) 

	filetoread= datadir+'/out2.csv'
	
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


	i = int(args[0])
	test_ids = partitioned[i]

	avg = oneFoldExp(test_ids,users,month_threshold,month_train,num_reccom,inspect='825')
	# avg = oneFoldExp(test_ids,users,month_threshold,month_train,num_reccom)
	
	avgs.append(avg)

	print ('avgs',avgs)
	print('number of users in consideration ',len(partitioned[0]),' with month set as ',month_threshold)

	print("--- Completed in %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
  main(sys.argv[1:])