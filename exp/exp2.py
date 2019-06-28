import csv
import sys
import time
import yaml
import os
import random

import statistics
from exp1 import *




def recommendTempWords(u_past,words_feat,num_words_predict,neigh,context_users):
	# print(words_feat)
	num_reccom = num_words_predict
	stats = {}
	user_words = u_past
	eff_user_words = [x[0] for x in user_words]
	for usr in neigh:
		uid = usr[0]
		searched = usr[3]
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


def findTempSimilarities(words_feat,context_users_day,neigh_size):
	rank = []
	for userid,search in context_users_day.items():
		tmp_best_score = 0 
		tmp_best_day = 0
		tmp_best_search = []
		for aDay,aDaySearch in search:
			tmp_words = aDaySearch
			user_words = words_feat
			ts = getSimilarityScore(user_words,tmp_words,userid)
			if ts > tmp_best_score:
				tmp_best_score = ts
				tmp_best_day = aDay
				tmp_best_search = aDaySearch

		rank.append([userid,tmp_best_score,tmp_best_day,tmp_best_search])

	rank.sort(key=lambda x:x[1],reverse=True)
	rank = rank[:neigh_size]
	return rank



def getUserSearchedWords(aUser,aDay):
	words = []
	for item in aUser:
		if item[1] < aDay:
			words.append(item)
	return words

def oneFoldShortTermExp(fold_id,folds,num_words_feat,num_words_predict,neigh_size,users,users_day):
	result_stack = []
	context_users = {**users}
	context_users_day = {**users_day}

	uids_in_exam = [x[0] for x in folds[fold_id]]

	# firstly, create test profiles
	for target_id in uids_in_exam:
		del context_users_day[target_id]
	
	# make word feature and ground words
	for user_log in folds[fold_id]:
		uid = user_log[0]
		day = user_log[1]
		uwords = user_log[2]

		words_feat = uwords[:num_words_feat]
		words_ground_predict = uwords[num_words_feat:]

		u_past = getUserSearchedWords(users[uid],day)

		tmp_neigh_search = findTempSimilarities(words_feat,context_users_day,neigh_size)
		predicted_words = recommendTempWords(u_past,words_feat,num_words_predict,tmp_neigh_search,context_users)

		# score prediction
		if len(predicted_words)==0: # if cannot be predicted 
			continue

		precision = predictionMatchingScore(uid,predicted_words,words_ground_predict)
		print(precision)
		# precision = (precision*len(predicted_words)/len(words_ground_predict)) # less strict metric

		# print(precision,len(predicted_words),len(words_ground_predict))
		result_stack.append(precision)

	return statistics.mean(result_stack)

def findInRangeDaySearch(threshold_up,threshold_down,aList):
	for item in aList:
		list_len = len(item[1])
		if list_len >= threshold_down and list_len <= threshold_up:
			return item
	return False

def main(args):
	if len(args) <= 0:
		sys.exit("please launch with fold number, for example 11")

	# parameters
	random.seed(100)

	# ----
	num_sample = 800 # for CV
	number_of_folds = 5
	num_words_predict = 10
	num_words_feat = 10
	neigh_size = 10
	# - - -

	start_time = time.time()

	root_arr = os.path.realpath(__file__).split('/')[:-2]
	datadir = '/'.join(root_arr+['data']) 
	filetoread= datadir+'/out2.csv'
	# filetoread= datadir+'/out_ipbased.csv'
	
	users = loadSQL2(filetoread)
	print("--- loaded in %s seconds ---" % (time.time() - start_time))
	
	user_dialy = []
	dataset = []


	# re-structure user info by day
	# ---
	users_day = {}
	for userid,search in users.items():
		user_seach_day = {}
		for anItem in search:
			w = anItem[0]
			day = anItem[1]
			existance = anItem[2]
			dbid = anItem[3]
			word_info = [w,dbid]
			user_seach_day[day] =  [word_info] if day not in user_seach_day else user_seach_day[day] + [word_info]
		usersdayInList = list(user_seach_day.items()) # a stack mode
		usersdayInList.sort(key=lambda x:len(x[1]),reverse=True)
		users_day[userid] = usersdayInList

	# Prepare test set
	# ---
	for userid,usersdayInList in users_day.items():
		foundDay = findInRangeDaySearch(25,20,usersdayInList)
		if not foundDay:
			continue
		else:
			wordset = [[x[0],int(x[1])] for x in foundDay[1]]
			wordset.sort(key=lambda x:x[1])
			dataset.append([userid,foundDay[0],wordset])

	print("The dataset has been prepared ...")

	total_inst = random.sample(dataset, num_sample)
	folds = partition_shuffle(total_inst,5)	

	avgs = []
	i = int(args[0])
	test_ids = folds[i]

	avg = oneFoldShortTermExp(i,folds,num_words_feat,num_words_predict,neigh_size,users,users_day)
	print(avg)

	# avgs.append(avg)

	print("--- Completed in %s seconds ---" % (time.time() - start_time))




if __name__ == '__main__':
  main(sys.argv[1:])