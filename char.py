import csv
import sys
import time


# def whatisthis(s):
isascii = lambda s: len(s) == len(s.encode())
    # return isascii


start_time = time.time()


# import codecs

a = 'hi'
b = '你行不行'

# print (a,b)
print('is ascii ? ',a,isascii(a))
print('is ascii ? ',b,isascii(b))
print("--- %s seconds ---" % (time.time() - start_time))

# print len(users.keys())
		# print ', '.join(row)