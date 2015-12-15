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

    for user in user_data.find(no_cursor_timeout=True).sort('data.name', 1):
        name = user['data']['name']
        print name
        comment_count = user_comments.count({'data.author': name,
                                             'kind': 't1'})

        number_of_comments_doc = {'username': name,
                                  'number_comments': comment_count}

        try:
            number_of_comments.insert_one(number_of_comments_doc)
        except pymongo.errors.DuplicateKeyError:
            continue

if __name__ == '__main__':
    main()
