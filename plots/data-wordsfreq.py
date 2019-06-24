"""
Number of seaches per word
It only considers the user records who searched more than 10 words during a year.
"""

import csv
import sys
import time
import yaml
import os

root_arr = os.path.realpath(__file__).split('/')[:-2]
root = '/'.join(root_arr+['src']) 
sys.path.append(root)


from wtoolkit import *


def main(args):

	start_time = time.time()

	root_arr = os.path.realpath(__file__).split('/')[:-2]
	datadir = '/'.join(root_arr+['data']) 
	filetoread= datadir+'/out2.csv'

	loaded_users = loadSQL2(filetoread)

	print("--- loaded in %s seconds ---" % (time.time() - start_time))


	word_dic = {}
	usersInList = list(loaded_users.items())
	usersInList.sort(key=lambda x:len(x[1]))
	for userinfo in usersInList:
		row = ''
		userid = userinfo[0]
		words = userinfo[1]
		for w in words:
			wordstr = w[0]
			worddate = w[1]
			if wordstr not in word_dic.keys():
				word_dic[wordstr] = 1
			else:
				word_dic[wordstr] += 1

	wordsInList = list(word_dic.items())
	wordsInList.sort(key=lambda x:x[1])
	# print(wordsInList)
	freqc = [x[1] for x in wordsInList]
	print(freqc)
	# print(len(word_dic.keys()))



if __name__ == '__main__':
  main(sys.argv[1:])