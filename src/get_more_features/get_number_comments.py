#!/usr/bin/env python
## -*- coding: utf-8 -*-
# reddit-reliability

import pymongo
from pymongo import MongoClient


def main():
    mongo_client = MongoClient('mongodb://cs598tar:cs598tar@'
                               '107.170.215.176:27017')
    reddit_data = mongo_client.reddit_data
    user_data = reddit_data.user_data
    number_of_comments = reddit_data.number_of_comments
    user_comments = reddit_data.user_comments

    number_of_comments.create_index(
        [("username", pymongo.ASCENDING)],
        background=True,
        unique=True,
        dropDups=True
    )

    for user in user_data.find():
        name = user['data']['name']
        print name
        comment_count = 0
        for comment in user_comments.find({'data.author': name}):
            if comment['kind'] == 't1':  # Actually a comment
                comment_count += 1

        number_of_comments_doc = {'username': name,
                                  'number_comments': comment_count}

        try:
            number_of_comments.insert_one(number_of_comments_doc)
        except pymongo.errors.DuplicateKeyError:
            continue

if __name__ == '__main__':
    main()
