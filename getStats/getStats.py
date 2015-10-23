import sys
import getopt
import praw
import time

# How this file works:
# Writes user information to output.txt and reads reliable users from file specified at run time
# how to run:
# (assuming you have praw) python getStats.py -i <input file name>

# What it does:
# > Reads users in that we have queried before
# > Reads users from file specified in input
# > Removes duplicate users from query list
# > Queries reddit for missing info
# > Calculates statistical information based on all users stored
 


# Files used:
# > Reads from file specified with -i flag
# > Writes files output_users.txt, users.p (pickle file)


# removes all items in fileusers from users
# if not in fileusers add to fileusers
def remove_duplicates(inset,fileusers):
	for u in inset:
		if u not in fileusers:
			fileusers.add(u)
		else:
			inset.remove(u)

# gets statistics for user base and store in stats.txt file
def get_stats(users):
	return



def main(argv):
	input_file='input.txt'
	info_file='info.txt'
	user_file = 'output_users.txt'

	# create files if they don't exist

	# get arguments
	opts,args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	
	# parse arguments
	for opt, arg in opts:
		if(opt == "-i"):
			input_file = arg
	
	# set up files
	try:
		infile = open(input_file,'r+').readlines()
	except IOError:
		infile = open(input_file,'a+').readlines()

	inset = set(infile)
	try:
		usernameset = set(open(user_file,'r+').readlines())
	except IOError:
		usernameset = set(open(user_file,'a+').readlines())

	# remove duplicates
	remove_duplicates(inset,usernameset)
	
	# Query Reddit for remainder in inset
	r = praw.Reddit(user_agent='Test Script by Ryan')
	users = list()
	for user in inset:
		time.sleep(2)
		users.append(r.get_redditor(user.strip('\n')))

	# get a full list of users
	try:
		su = open(info_file,"r+")
	except IOError:
		su = open(info_file,"a+")

	stored_users = list(set(su))
	for u in users:
		stored_users.append(str(u.__dict__))
	su.close()

	# get statistics for the users we've gathered
	get_stats(stored_users)

	# write user objects to file
	pd = open(info_file,"a+")
	for u in users:
		pd.write(str(u.__dict__))	
	# write stored usernames to file
	usernames = open(user_file,'a+')
	for i in inset:
		usernames.write(inset)

if __name__ == "__main__":
	main(sys.argv[1:])