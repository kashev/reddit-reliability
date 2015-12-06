#!/usr/bin/env python
## -*- coding: utf-8 -*-
# reddit-reliability

from collections import defaultdict
import pymongo
import pprint
from pymongo import MongoClient


def main():
    mongo_client = MongoClient('mongodb://cs598tar:cs598tar@'
                               '107.170.215.176:27017')
    reddit_data = mongo_client.reddit_data
    print(reddit_data.collection_names(include_system_collections=False))
    post_karma_by_subreddit = reddit_data.post_karma_by_subreddit
    important_karma_mongo = reddit_data.important_karma

    important_karma_mongo.create_index(
        [("username", pymongo.ASCENDING)],
        background=True,
        unique=True,
        dropDups=True
    )

    # Read in trusted_subreddits and important_subreddits
    impotant_subreddits = set()
    lines = [line.rstrip('\n') for line in
             open('../config/important_subreddits.txt')]
    for line in lines:
        impotant_subreddits.add(line)
    trusted_subreddits = set()
    lines = [line.rstrip('\n') for line in
             open('../config/trusted_subreddits.txt')]
    for line in lines:
        trusted_subreddits.add(line)

    for user_mongo in post_karma_by_subreddit.find():
        user_name = user_mongo['username']
        print(user_name)

        karma_by_subreddit = user_mongo['karma_by_subreddit']
        important_karma = 0
        trusted_karma = 0
        for subreddit, karma in karma_by_subreddit.iteritems():
            if subreddit in impotant_subreddits:
                important_karma += karma
            if subreddit in trusted_subreddits:
                trusted_karma += karma
        try:
            important_karma_mongo.insert_one({
                "username": user_name,
                "important_karma": important_karma,
                "trusted_karma": trusted_karma
            })
        except pymongo.errors.DuplicateKeyError:
            continue


if __name__ == '__main__':
    main()
