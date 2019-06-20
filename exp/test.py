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


def main(args):

	# x = 20181204
	# print(str(x)[4:6]+','+str(x)[-2:])
	# print(dateToDays(x))

	# full_users = {"a":[1,3],"b":[3,1],"c":[3,2]}
	# context_users = {**full_users}
	# del context_users['a']
	# print(full_users,context_users)

	a = [1,3,5,1]
	print(statistics.mean(a))


if __name__ == '__main__':
  main(sys.argv[1:])