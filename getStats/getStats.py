import sys
import getopt
import praw
import time
# gets statistics for user base and print
def get_stats(users):
	avg_val = dict()
	i = 0
	for user in users:
		i = i+1
		for key in user:
			if i == 1:
				print 'key: ',key,'\n'
			if type(user[key]) is float or type(user[key]) is int:
				try:
					avg_val[key] += (user[key] + 0.0)/len(users)
				except KeyError:
					avg_val[key] = (user[key] + 0.0)/len(users)
			elif type(user[key]) is bool:
				try:
					avg_val[key] += (user[key] + 0.0)/len(users)
				except KeyError:
					avg_val[key] = (user[key] + 0.0)/len(users)
	for value in avg_val:
		print value,': ', avg_val[value]
	return avg_val


def main(argv):
	input_file='input.txt'

	# create files if they don't exist

	# get arguments
	opts,args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	
	# parse arguments
	for opt, arg in opts:
		if(opt == "-i"):
			input_file = arg
	
	# set up files
	try:
		infile = open(input_file,'r+')
	except IOError:
		infile = open(input_file,'a+')
	inset = set(infile.readlines())
	infile.close()

	# Query Reddit for remainder in inset
	r = praw.Reddit(user_agent='Test Script')
	userlist = list() # list of dictionaries
	for user in inset:
		time.sleep(2)
		userlist.append((r.get_redditor(user.strip('\n'))).__dict__)

	get_stats(userlist)

if __name__ == "__main__":
	main(sys.argv[1:])