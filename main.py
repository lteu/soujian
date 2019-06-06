import csv
import sys
import time

import yaml


isascii = lambda s: len(s) == len(s.encode())

def loadSQL(filetoread):
	users = {}

	if '\0' in open(filetoread).read():
	    print ("you have null bytes in your input file")

	data_initial = open(filetoread, "r")
	# thereader = csv.reader((line.replace('\0','') for line in data_initial), delimiter=",", quotechar='\"')

	thereader = csv.reader((line for line in data_initial), delimiter=",", quotechar='\"')

	
	for row in thereader:
		if len(row) < 5:
			continue
		userid = row[1].replace('"','')
		word = row[2].replace('"','')
		thedate = row[4].replace('"','')
		thedate = int(thedate)
		anItem = [word,thedate]

		# account only ita words
		if not isascii(word):
			continue

		if userid == 'NULL':
			continue
		

		if userid not in users:
			users[userid] = [anItem]
		else:
			users[userid].append(anItem)
	return users




def main(args):

	start_time = time.time()

	filetoread= 'wlog.csv'
	users = loadSQL(filetoread)

	print("--- loaded in %s seconds ---" % (time.time() - start_time))

	iterate_dir = users
	# eliminate duplicates
	for key,item in iterate_dir.items():
		users[key] = set(map(tuple, item))

	print("--- duplicates eliminated in %s seconds ---" % (time.time() - start_time))


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
	# 	# print (counter,len(words))
	# 	counter += 1
	# print(list_count)


	# PRINT csv file
	out_file = 'out.csv'
	print('Printing CSV file ...',out_file)
	writer = csv.writer(open(out_file, 'w'), delimiter = ',')
	for userinfo in usersInList:
		row = ''
		userid = userinfo[0]
		words = userinfo[1]
		for w in words:
			row = str(userid) + ','+str(w[0])+','+str(w[1])
			writer.writerow(row.split(','))
	print("--- %s seconds ---" % (time.time() - start_time))

	# generate yaml file
	# with open('data.yml', 'w') as outfile:
	# 	yaml.dump(usersInList, outfile)
	    # yaml.dump(usersInList, outfile, default_flow_style=False)


	# print len(users.keys())
			# print ', '.join(row)


if __name__ == '__main__':
  main(sys.argv[1:])