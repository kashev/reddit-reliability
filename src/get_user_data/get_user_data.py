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
        [("data.name",pymongo.ASCENDING)],
        unique=True,
        dropDups=True
    )

    usernames = util.get_usernames()

    for user in usernames:
        print user
        r = reddit.api_get('user/' + user.strip() + '/about', {})
        if r != None:
            try:
                u = user_data.insert_one(r)
            except pymongo.errors.DuplicateKeyError:
                continue

# GET REDDIT USER CONTENT
def get_reddit_user_content():
    mongo_client = MongoClient('localhost', 27017)
    reddit_data = mongo_client.reddit_data
    user_posts = reddit_data.user_posts

    params = {
        'sort': 'new',
        't': 'all',
        'limit': 100,
        'sr_detail': True
    }


if __name__ == '__main__':
    util.setup()
    get_reddit_user_bios()
