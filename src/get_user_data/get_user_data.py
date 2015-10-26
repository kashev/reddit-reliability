import praw
import requests
import sys

def setup():
    sys.path.insert(0, "../config")
    print sys.path

def getPraw():
    user_agent = "Python:edu.illinois.cs.redditReliability:v1.0 (by /u/goodusername)"
    r = praw.Reddit(user_agent=user_agent)
    return r

def get_file_contents(filename):
    return open(filename)

def get_usernames():
    return get_file_contents('../config/usernames.txt')

# TODO fixme
def getAuthedPraw():
    r = getPraw()
    r.set_oauth_app_info(
      client_id='i5B-zIPFJVwZVw',
      client_secret='RzJoUuDew5N7eHNxt8vKrYwN3As'
    )
    return r

# TODO build in request queueing so we don't bust through rate limiting
# (aka we try to be nice people)
def get_results(endpoint):
    headers = {
        'user-agent': 'Python:edu.illinois.cs.redditReliability:v1.0 (by /u/goodusername)'
    }

    r = requests.get('https://api.reddit.com/' + endpoint, headers=headers)

    if (r.status_code == requests.codes.ok) :
        return r.json()
    else:
        r.raise_for_status()

def get_reddit_user_bios():
    #usernames = reddit_util.get_usernames()
    usernames = get_usernames()

    for user in usernames:
        r = get_results('user/' + user + '/about')

        print r

if __name__ == '__main__':
    setup()
    get_reddit_user_bios()
