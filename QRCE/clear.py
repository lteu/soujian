import csv
import sys
import time



def breakLines(initial_letter, composite_list,all_lines):
	lines = []
	tmp = ""
	found_words = set(all_lines)
	ifPossibleDup = False
	for item in composite_list:
		if '(' in item or ')' in item:
			continue
		if item[0] == initial_letter:
			if  len(lines) > 0  and item in lines[-1]:
				if tmp != "":
					lines.append(tmp)
				tmp = item 
			elif  len(lines) > 0 and lines[-1][0] == initial_letter and item in all_lines:
				ifPossibleDup = True
				tmp += ' '+item
				print('check if it is ok',tmp,composite_list)
			else:
				if tmp != "":
					lines.append(tmp)
				tmp = item
				# print(item,'of',composite_list,lines[-1])
				
		else:
			tmp += ' '+item
	
	# if "mescolare" in composite_list: 
		# print(composite_list,tmp)
	lines.append(tmp)
	rlt = lines
	# if ifPossibleDup:
	# 	print('possible duplication, trace',composite_list)


	return rlt

# def removeParenthesis(aStr):
# 	return aStr.split("(")[0]


def loadIgnore():
	testFile = "nuovo espresso/ignore.txt"
	symb = []
	with open(testFile) as ff:
		for line in ff:
			line = line.strip()
			line = line.lower()
			symb.append(line)

	return set(symb)


def main(args):

	if len(args) < 1:
		sys.exit("launch with file name e.g., python clear.py A1.txt")

	filename = args[0]
	start_time = time.time()


	symbs = loadIgnore()
	testFile = "nuovo espresso/"+filename


	all_lines = []
	with open(testFile) as ff:
		for line in ff:
			for sym in symbs:
				if sym in line:
					continue

			line = line.lower()
			initial_letter = line[0]
			a_vocabolar = ""
			
			pieces = line.strip().split(" ")

			if initial_letter == '(':
				initial_letter = pieces[1][0]
				pieces = pieces[1:]

			if len(pieces) > 1:
				rlt = breakLines(initial_letter, pieces,all_lines)
				all_lines = all_lines+rlt
			else:
				all_lines.append(line)

	


	# replacements
	all_lines = [x.replace('*', '') for x in all_lines]
	all_lines = [x.replace('...', '') for x in all_lines]
	all_lines = [x.replace('!', '') for x in all_lines]
	all_lines = [x.replace('’', '\'') for x in all_lines]

	# trim
	all_lines = [x.strip() for x in all_lines if  x.strip() != ""]
	all_lines = [x for x in all_lines if 'nuovo espresso' not in x]

	# filter out
	all_lines_out = [x for x in all_lines if x[-1] != '?' and '/' not in x and x not in symbs]
	all_lines_out = list(set(all_lines_out))
	all_lines_out.sort()
	out = "\n".join(all_lines_out)
	outfile = "nuovo espresso/out_"+filename
	with open(outfile, 'w+') as outfile:
		outfile.write(out)

	print("--- %s seconds ---" % (time.time() - start_time))





if __name__ == '__main__':
  main(sys.argv[1:])