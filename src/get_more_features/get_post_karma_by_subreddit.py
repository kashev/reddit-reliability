#!/usr/bin/env python
## -*- coding: utf-8 -*-
# reddit-reliability
from __future__ import division

from collections import defaultdict
import pymongo
from pymongo import MongoClient


def main():
    mongo_client = MongoClient('mongodb://cs598tar:cs598tar@'
                               '107.170.215.176:27017')
    reddit_data = mongo_client.reddit_data
    print(reddit_data.collection_names(include_system_collections=False))
    user_data = reddit_data.user_data
    user_submitted = reddit_data.user_submitted
    post_karma_by_subreddit = reddit_data.post_karma_by_subreddit

    post_karma_by_subreddit.create_index(
        [("username", pymongo.ASCENDING)],
        background=True,
        unique=True,
        dropDups=True
    )

    for user_mongo in user_data.find().sort('data.name', 1):
        user_name = user_mongo['data']['name']
        print(user_name)

        karma_by_subreddit = defaultdict(int)
        for submission in user_submitted.find({"data.author": user_name}):
            subreddit = submission['data']['subreddit'].replace('.', '')
            score = submission['data']['score']
            karma_by_subreddit[subreddit] += score
        try:
            post_karma_by_subreddit.insert_one({
                "username": user_name,
                "karma_by_subreddit": dict(karma_by_subreddit)
            })
        except pymongo.errors.DuplicateKeyError:
            continue


if __name__ == '__main__':
    main()
