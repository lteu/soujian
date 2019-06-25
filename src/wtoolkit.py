import csv
import sys
import time

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

		userid = int(row[0])
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
