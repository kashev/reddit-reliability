import sys
import getopt
import praw
import time
# gets statistics for user base and print
def get_stats(users,filename):
	avg_val = dict()
	i = 0
	j = 0
	# I know... it's horrendous. I could make a list of keys but... this is easier.
	avg_val['link_karma'] = 0.0
	avg_val['comment_karma'] = 0.0
	avg_val['is_gold'] = 0.0
	avg_val['is_mod'] = 0.0
	avg_val['has_verified_email'] = 0.0
	avg_val['created'] = 0.0
	nonexistantusers = list()
	for user in users:
		j = j+1
		try:
			i = i+1
			avg_val['link_karma'] = user.link_karma + avg_val['link_karma']
			avg_val['comment_karma'] = user.comment_karma + avg_val['comment_karma']
			avg_val['is_gold'] = user.is_gold + avg_val['is_gold']
			avg_val['is_mod'] = user.is_mod + avg_val['is_mod']
			try:
				avg_val['has_verified_email'] = user.has_verified_email + avg_val['has_verified_email']
			except TypeError:
				avg_val['has_verified_email'] = 0 + avg_val['has_verified_email']
			avg_val['created'] = user.created + avg_val['created']
		except praw.errors.NotFound:
			print user.name
			nonexistantusers.append(user.name)
	remove_user(nonexistantusers,filename)
	for key in avg_val:
		avg_val[key] = avg_val[key]/i
		print key,': ', avg_val[key]
	return avg_val

def remove_user(usernames,filename):
	f = open(filename,"r")
	lines = f.readlines()
	f.close()
	f = open(filename,"w")
	b = False
	for user in lines:
		for username in usernames:
			if user == username+"\n":
				b = True
		if not b:
			f.write(user)
		else:
			print "deleting user : ",user,"..."
		b = False
	f.close()
	print "bad users deleted."
			


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
		userlist.append((r.get_redditor(user.strip('\n'))))

	get_stats(userlist,input_file)

if __name__ == "__main__":
	main(sys.argv[1:])