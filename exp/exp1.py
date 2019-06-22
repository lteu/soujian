'''
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
root = '/'.join(root_arr) 
# src_path = root + '/learn/'
sys.path.append(root)

from wtoolkit import *
# from mid import *
# from wtoolkit import isascii,loadSQL

def dateToDays(aDate):
	days = (int(str(aDate)[4:6])-1)*30 + int(str(aDate)[-2:])
	return days

def checkTimeRange(userid,item,month_threshold):
	item.sort(key=lambda x:x[1])
	initial_date = dateToDays(item[0][1])
	end_date = dateToDays(item[-1][1])

	# if str(userid) == '2356':
	# 	print(initial_date,end_date)
	# 	print((end_date-initial_date)/30)
	# 	sys.exit()
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
	# print (eff_user_words,eff_tmp_words)
	# sys.exit('deg3')
	occurrence = [x for x in eff_user_words if x in eff_tmp_words]
	# print(userid)
	# if int(userid) == 3320:
	# 	print (tmp_words)
	# 	print (occurrence)
	# 	sys.exit('deg')
	# if len(occurrence) > 0:
	# 	print(occurrence,userid)
	return len(occurrence) / len(user_words)

def findNeighbourhood(current_userid,list_words,context_users,k=10):
	rank = []
	# print (context_users[3320])
	for userid,info in context_users.items():
		tmpScore = getSimilarityScore(list_words,info,userid)
		if tmpScore > 0:
			rank.append([userid,tmpScore])

	rank.sort(key=lambda x:x[1],reverse=True)
	rank = rank[:k]
	# print (list_words, "---------\n",rank,"---\n",current_userid)
	# sys.exit()
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
	# print(statsInList[:50],eff_user_words)
	# sys.exit()

def predictionMatchingScore(userid,recommended,user_ground):
	words_rec = [x[0] for x in recommended]
	words_grd = [x[0] for x in user_ground]
	words_guessed = [x for x in words_rec if x in words_grd]
	if len(words_rec) == 0:
		sys.exit('0 recommendation occured for user with ID '+ str(userid))
	precision = len(words_guessed)/len(words_rec)
	return precision
	# print (precision)

def predictWords(test_instances,test_ground,context_users,num_reccom):
	stack = []
	for userid,info in test_instances.items():
		neigh = findNeighbourhood(userid,info,context_users)
		recommended = findRecommendationFromNeigh(num_reccom,info,neigh,context_users)
		# todo then check precision!
		# print(recommended)
		precision = predictionMatchingScore(userid,recommended,test_ground[userid])
		print(precision)
		stack.append(precision)

	print('stack',stack)
	return stack
		# sys.exit()

def oneFoldExp(test_ids,full_users,month_threshold,month_train,num_reccom):
	context_users = {**full_users}
	target_users = {}

	# firstly, create test profiles
	for target_id in test_ids:
		target_users[target_id] = full_users[target_id]
		del context_users[target_id]

	# secondly, extract test user info
	test_instances,test_ground = extTestUsersInfo(target_users,month_train)

	# get predictions
	# print(test_ids)
	stack = predictWords(test_instances,test_ground,context_users,num_reccom)
	return statistics.mean(stack)

def main(args):
	if len(args) <= 0:
		sys.exit("please launch with fold number, for example 0-4")

	# parameters
	random.seed(100)
	month_threshold = 2
	month_train = month_threshold/2
	number_of_folds = 5
	num_reccom = 50
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

	

	i = int(args[0])
	test_ids = partitioned[i]
	avg = oneFoldExp(test_ids,users,month_threshold,month_train,num_reccom)
	avgs.append(avg)
	# for i in range(0,5):
	# 	test_ids = partitioned[i]
	# 	avg = oneFoldExp(test_ids,users,month_threshold,month_train,num_reccom)
	# 	avgs.append(avg)

	print ('avgs',avgs)

	print("--- number of remained users %s ---" % (len(partitioned)))
	print('number of users in consideration ',len(partitioned[0]),' with month set as ',month_threshold)
	# print(test_users.keys()[10])

	# usersInList = list(users.items())
	# usersInList.sort(key=lambda x:len(x[1]))


	# print("--- sorted in %s seconds ---" % (time.time() - start_time))


	# number_of_words = 0
	# for userprofile in usersInList:
	# 	number_of_words += len(userprofile[1])


	# print('=== report stats ====')
	# num_of_users = len(users.keys())
	# print('num of users:',num_of_users)
	# print('num of words:',number_of_words)
	# print('avg word per user:',number_of_words/num_of_users)
	# median_user_index = int(num_of_users/2)
	# print('median word per user:',len(usersInList[median_user_index][1]))
	# print('==============')

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