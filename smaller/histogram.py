import csv
import sys
import time
import yaml
import os

root_arr = os.path.realpath(__file__).split('/')[:-2]
root = '/'.join(root_arr) 
sys.path.append(root)

from wtoolkit import *

def main(args):

	start_time = time.time()

	arr_steps = [0]+list(range(1,5000,5))
	print(arr_steps)

	filetoread= 'out.csv'
	users = loadSQL2(filetoread)

	print("--- loaded in %s seconds ---" % (time.time() - start_time))

	register = [0 for i in range(1,len(arr_steps))]

	for i in range(1,len(arr_steps)):
		end  = arr_steps[i]
		start = arr_steps[i-1]
		count = 0
		for key,items in users.items(): 
			if len(items) > start and len(items) <= end:
				register[i-1] += 1

	print (register)

if __name__ == '__main__':
  main(sys.argv[1:])