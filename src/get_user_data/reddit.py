import requests
import time

APP_CLIENT = ''
APP_SECRET = ''

# TODO build in request queueing so we don't bust through rate limiting
# (aka we try to be nice people)
#
# 30 requests/minute if NO AUTH
# 60 requests/minute if AUTHED
def api_get(endpoint):
    headers = {
        'user-agent': 'Python:edu.illinois.cs.redditReliability:v1.0 (by /u/goodusername)'
    }

    try:
        r = requests.get('https://api.reddit.com/' + endpoint, headers=headers)

        if (r.status_code == requests.codes.ok) :
            time.sleep(2)
            return r.json()
        else:
            r.raise_for_status()
    except:
        print r.reason


def oauth_dance():
    postdata = {
        'grant_type': 'client_credentials'

    }

    r = requests.post('https://www.reddit.com/api/v1/access_token')


def get_usernames():
    return get_file_contents('../config/usernames.txt')

def get_reddit_user_bios(user):

    r = api_get('user/' + user + '/about')
