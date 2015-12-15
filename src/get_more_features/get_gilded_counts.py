#!/usr/bin/env python
## -*- coding: utf-8 -*-
# reddit-reliability
from __future__ import division
import pymongo
from pymongo import MongoClient


def main():
    mongo_client = MongoClient('mongodb://cs598tar:cs598tar@'
                               '107.170.215.176:27017')
    reddit_data = mongo_client.reddit_data
    user_data = reddit_data.user_data
    gilded_count = reddit_data.gilded_count
    user_submitted = reddit_data.user_submitted
    user_comments = reddit_data.user_comments

    gilded_count.create_index(
        [("username", pymongo.ASCENDING)],
        background=True,
        unique=True,
        dropDups=True
    )

    for user in user_data.find().sort('data.name', 1):
        name = user['data']['name']
        print name

        post_query = {'data.author': name,
                      'data.gilded': 1,
                      'kind': 't3'}

        comment_query = {'data.author': name,
                         'data.gilded': 1,
                         'kind': 't1'}

        post_count = user_submitted.count(post_query)
        comment_count = user_comments.count(comment_query)
        gilded_doc = {'username': name,
                      'number_posts': post_count,
                      'number_comments': comment_count}

        try:
            gilded_count.insert_one(gilded_doc)
        except pymongo.errors.DuplicateKeyError:
            continue


if __name__ == '__main__':
    main()
