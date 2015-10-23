import sys
import getopt
import praw
import time
import csv
import cPickle as pkl


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
	for u in inset.copy():
		if u not in fileusers:
			fileusers.add(u)
		else:
			inset.remove(u)

# gets statistics for user base and store in stats.txt file
def get_stats(users):
	return

def string_to_user(users):
	
	return

def main(argv):
	input_file='input.txt'
	user_file='user_list.txt'
	info_file = 'dictionaries.p'

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

	# store new reddit information in pickle
	f1 = open(info_file,'wb')
	for user in inset:
		time.sleep(2)
		temp = r.get_redditor(user.strip('\n'))
		pkl.dump(temp.__dict__,f1)
	f1.close()

	# load dictionaries from pickle
	userdicts = list()
	f2 = open(info_file,'r+b')
	while 1:
		try:
			userdicts.append(pkl.load(f2))
		except EOFError:
			break

	# write user objects to file

	# write stored usernames to file
	usernames = open(user_file,'a+')
	for i in inset:
		usernames.write(i)

if __name__ == "__main__":
	main(sys.argv[1:])