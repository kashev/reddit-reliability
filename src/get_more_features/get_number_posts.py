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
    number_of_posts = reddit_data.number_of_posts
    user_submitted = reddit_data.user_submitted

    number_of_posts.create_index(
        [("username", pymongo.ASCENDING)],
        background=True,
        unique=True,
        dropDups=True
    )

    for user in user_data.find():
        name = user['data']['name']
        print name
        post_count = user_submitted.count({'data.author': name})
        number_of_posts_doc = {'username': name,
                               'number_posts': post_count}

        try:
            number_of_posts.insert_one(number_of_posts_doc)
        except pymongo.errors.DuplicateKeyError:
            continue

if __name__ == '__main__':
    main()
