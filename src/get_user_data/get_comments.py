import reddit
import requests
import util
import pymongo
from pymongo import MongoClient

# GET REDDIT USER BIOS
def get_reddit_user_bios():
    mongo_client = MongoClient('localhost', 27017)
    reddit_data = mongo_client.reddit_data
    user_data = reddit_data.user_data

    user_data.create_index(
        [("name",pymongo.ASCENDING)],
        background=True
    )

    usernames = util.get_usernames()

    for user in usernames:
        r = reddit.api_get('user/' + user.strip() + '/about', {})
        if r != None:
            user_data.insert_one(r)

# GET REDDIT USER CONTENT
def get_reddit_user_content():
    mongo_client = MongoClient('localhost', 27017)
    reddit_data = mongo_client.reddit_data
    user_commentss = reddit_data.user_comments

    user_comments.create_index(
        [("data.id",pymongo.ASCENDING)],
        background=True,
        unique=True,
        dropDups=True
    )

    params = {
        'sort': 'new',
        't': 'all',
        'limit': 100,
        'sr_detail': True
    }

    usernames = util.get_usernames()

    for user in usernames:
        print user
        continueWithUser = True

        while continueWithUser:
            r = reddit.api_get('user/' + user.strip() + '/submitted', params)
            if r != None:
                for thing in r['data']['children']:
                    try:
                        user_comments.insert_one(thing)
                    except pymongo.errors.DuplicateKeyError:
                        continue
                if r['data']['after'] is None:
                    continueWithUser = False
                    break
                else:
                    params['after'] = r['data']['after']
            else:
                continueWithUser = False


if __name__ == '__main__':
    util.setup()
    get_reddit_user_content()
