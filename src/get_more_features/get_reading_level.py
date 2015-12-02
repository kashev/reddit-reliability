import pymongo
import textstat
from pymongo import MongoClient


def main():
    mongo_client = MongoClient('mongodb://cs598tar:cs598tar@'
                               '107.170.215.176:27017')
    reddit_data = mongo_client.reddit_data
    user_data = reddit_data.user_data
    user_reading_level = reddit_data.user_reading_level

    user_data.create_index(
        [("name", pymongo.ASCENDING)],
        background=True
    )

    user_reading_level.create_index(
        [("data.id", pymongo.ASCENDING)],
        background=True,
        unique=True,
        dropDups=True
    )

    for user in user_data.find():
        name = user['data']['name']

        reading_level_data = {'name': name,
                              'reading_level': 0}
        user_reading_level.insert_one(reading_level_data)

    # params = {
    #     'sort': 'new',
    #     't': 'all',
    #     'limit': 100,
    #     'sr_detail': True
    # }

    # usernames = util.get_usernames()

    # for user in usernames:
    #     print user
    #     continueWithUser = True

    #     while continueWithUser:
    #         r = reddit.api_get('user/' + user.strip() + '/submitted', params)
    #         if r != None:
    #             for thing in r['data']['children']:
    #                 try:
    #                     user_comments.insert_one(thing)
    #                 except pymongo.errors.DuplicateKeyError:
    #                     continue
    #             if r['data']['after'] is None:
    #                 continueWithUser = False
    #                 break
    #             else:
    #                 params['after'] = r['data']['after']
    #         else:
    #             continueWithUser = False


if __name__ == '__main__':
    main()
