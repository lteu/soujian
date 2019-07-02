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
from exp1 import extTestUsersInfo


def readWordFile(filename):
	words = []
	with open(filename) as ff:
		for line in ff:
			if line.strip() != "":
				words.append(line.strip())
	return words


def loadQCER():
	root_arr = os.path.realpath(__file__).split('/')[:-2]
	datadir = '/'.join(root_arr+['QRCE']) 

	filetoread1= datadir+'/out_A1.txt'
	a1 = readWordFile(filetoread1)
	filetoread1= datadir+'/out_A2.txt'
	a2 = readWordFile(filetoread1)
	filetoread1= datadir+'/out_B1.txt'
	b1 = readWordFile(filetoread1)
	filetoread1= datadir+'/out_B2.txt'
	b2 = readWordFile(filetoread1)
	filetoread1= datadir+'/out_C1.txt'
	c1 = readWordFile(filetoread1)
	return {'a1':a1,'b1':b1,'b2':b2,'a2':a2,'c1':c1}

def findLevelByComparingWords(info,livelli):
	words_past = [x[0] for x in info]
	words_past = set(words_past)
	max_num,sel_range,sel_lvl = 0,[],'b1' # b1 as default
	for lvl,wordsrange in livelli.items(): 
		selected = [x for x in wordsrange if x in words_past]
		if len(selected) > max_num:
			max_num = len(selected)
			sel_range = selected
			sel_lvl = lvl
	return sel_lvl
	# print(sel_range,sel_lvl)
	# sys.exit()

def calCoverage(listSuggested,user_ground):
	u_g_list = set([x[0] for x in user_ground])
	sel = [x for x in listSuggested if x in u_g_list]
	percentage = len(sel)/len(u_g_list)
	return percentage
	# print(percentage)

def predictWordsWithQCER(test_instances,test_ground,context_users,num_reccom,livelli):
	# configure user profile level
	stack = []
	for userid,info in test_instances.items():

		if len(info) < num_reccom or len(test_ground[userid]) < num_reccom:
			continue
		
		level = findLevelByComparingWords(info,livelli)
		percentage = calCoverage(livelli[level],test_ground[userid])
		stack.append(percentage)
		# sys.exit()
		# neigh = findNeighbourhood(userid,info,context_users)
		
		# recommended = findRecommendationFromNeigh(num_reccom,info,neigh,context_users)
		
		# if len(recommended)==0: # if cannot be predicted 
		# 	continue
			
		# # print(recommended)
		# precision = predictionMatchingScore(userid,recommended,test_ground[userid])
		

		# # print(precision)
		# stack.append(precision)

	# print('stack',stack)
	return stack




def theExp(users,month_threshold,month_train,num_reccom,livelli):
	# target_users = users.keys()
	test_instances,test_ground = extTestUsersInfo(users,month_train)

	stack = predictWordsWithQCER(test_instances,test_ground,users,num_reccom,livelli)

	return statistics.mean(stack)
def main(args):
	# if len(args) <= 0:
	# 	sys.exit("please launch with fold number, for example 0-4")

	livelli = loadQCER()
	# print(livelli)
	# sys.exit()
	# parameters
	random.seed(100)
	month_threshold = 2
	month_train = month_threshold/2
	num_reccom = 20
	# ----
	start_time = time.time()

	root_arr = os.path.realpath(__file__).split('/')[:-2]
	datadir = '/'.join(root_arr+['data']) 

	filetoread= datadir+'/out2.csv'
	
	users = loadSQL2(filetoread)
	print("--- loaded in %s seconds ---" % (time.time() - start_time))
	
	score = theExp(users,month_threshold,month_train,num_reccom,livelli)
	print(score)
	
	print("--- Completed in %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
  main(sys.argv[1:])