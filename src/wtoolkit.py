import csv
import sys
import time
from datetime import datetime

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
		searchid = row[0].replace('"','')
		userid = row[1].replace('"','')
		word = row[2].replace('"','').strip()
		thedate = row[4].replace('"','')
		thedate = int(thedate)
		ifexist = row[6]
		anItem = [word,thedate,ifexist,searchid]

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


def loadSQL_ipbased(filetoread):
	users = {}

	if '\0' in open(filetoread).read():
	    print ("you have null bytes in your input file")

	data_initial = open(filetoread, "r")
	# thereader = csv.reader((line.replace('\0','') for line in data_initial), delimiter=",", quotechar='\"')

	thereader = csv.reader((line for line in data_initial), delimiter=",", quotechar='\"')

	
	for row in thereader:
		if len(row) < 5:
			continue
		searchid = row[0].replace('"','')
		# userid = row[1].replace('"','')
		word = row[1].replace('"','').strip()
		timestamp = int(row[2].replace('"',''))
		# thedate = int(thedate)
		a = datetime.fromtimestamp(timestamp)
		thedate = a.strftime("%Y%m%d")
		ip = row[3]
		ifexist = row[4]
		anItem = [word,thedate,ifexist,searchid,ip]
		# print(anItem)
		# sys.exit()
		# account only ita words
		if not isascii(word):
			continue

		if ip == 'NULL':
			continue

		# skip in case word not found
		if int(ifexist) != 1:
			continue

		if ip not in users:
			users[ip] = [anItem]
		else:
			users[ip].append(anItem)

		# print(users)
	
	# print(len(users.keys()))
	# sys.exit()
	return users



def loadSQL2(filetoread):
	"""
	reads a cleaner file treated by loadSQL()
	"""
	users = {}
	data_initial = open(filetoread, "r")
	# thereader = csv.reader((line.replace('\0','') for line in data_initial), delimiter=",", quotechar='\"')

	thereader = csv.reader((line for line in data_initial), delimiter=";", quotechar='\"')

	for row in thereader:
		if len(row) < 3:
			continue

		userid = row[0]
		# if userid == 1463:
		# 	print('hello')
		word = row[1].strip()
		thedate = row[2]
		thedate = int(thedate)
		ifexist = row[3]
		searchid = row[4]
		anItem = [word,thedate,ifexist,searchid]
		# account only ita words
		if not isascii(word):
			continue
		if userid == 'NULL':
			continue
		if userid not in users:
			users[userid] = [anItem]
		else:
			users[userid].append(anItem)

	# print (users[1463])
	# sys.exit('deg2')
	return users
