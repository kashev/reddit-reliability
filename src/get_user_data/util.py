import sys

def setup():
    sys.path.insert(0, "../config")

def get_file_contents(filename):
    return open(filename)

def get_usernames():
    return get_file_contents('../config/subsample-72Rel-91Unrel.txt')
