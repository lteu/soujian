import matplotlib.pyplot as plt
import sys

def main(args):

	y=[164, 983, 376, 262, 230, 181, 150, 133, 97, 79, 87, 84, 75, 58, 59, 48, 50, 43, 49, 39, 40, 30, 36, 35, 37, 39, 17, 30, 24, 27, 31, 14, 22, 20, 20, 18, 17, 10, 19, 13, 16, 14, 12, 13, 7, 9, 12, 10, 14, 8, 14, 7, 11, 9, 5, 8, 11, 5, 5, 6, 3, 6, 3, 3, 3, 5, 1, 2, 2, 4, 4, 2, 1, 0, 1, 0, 1, 1, 1, 1, 3, 1, 0, 0, 3, 0, 0, 1, 3, 1, 2, 1, 0, 1, 0, 0, 3, 0, 3, 1]

	x = list(range(1,5000,50))
	plt.plot(x,y)
	# plt.axis(x)

	plt.ylabel('number of people')
	plt.xlabel('search range')
	plt.grid(True)
	plt.show()

if __name__ == '__main__':
  main(sys.argv[1:])