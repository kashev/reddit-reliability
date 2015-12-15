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
    print(reddit_data.collection_names(include_system_collections=False))
    comment_karma_by_subreddit = reddit_data.comment_karma_by_subreddit
    important_karma_mongo = reddit_data.important_comment_karma

    important_karma_mongo.create_index(
        [("username", pymongo.ASCENDING)],
        background=True,
        unique=True,
        dropDups=True
    )

    # Read in trusted_subreddits and important_subreddits
    trusted_subreddits = set([line.rstrip('\n') for line in
                              open('../config/trusted_subreddits.txt')])
    top_100 = set([line.rstrip('\n') for line in
                   open('../config/top_100.txt')])
    top_50 = set([line.rstrip('\n') for line in
                  open('../config/top_50.txt')])
    top_25 = set([line.rstrip('\n') for line in
                  open('../config/top_25.txt')])
    top_10 = set([line.rstrip('\n') for line in
                  open('../config/top_10.txt')])

    for user_mongo in (comment_karma_by_subreddit.find(no_cursor_timeout=True)
                                                 .sort('data.name', 1)):
        user_name = user_mongo['username']
        print(user_name)

        karma_by_subreddit = user_mongo['karma_by_subreddit']
        trusted_karma = 0
        top_100_karma = 0
        top_50_karma = 0
        top_25_karma = 0
        top_10_karma = 0

        for subreddit, karma in karma_by_subreddit.iteritems():
            if subreddit in trusted_subreddits:
                trusted_karma += karma
            if subreddit in top_100:
                top_100_karma += karma
            if subreddit in top_50:
                top_50_karma += karma
            if subreddit in top_25:
                top_25_karma += karma
            if subreddit in top_10:
                top_10_karma += karma
        try:
            important_karma_mongo.insert_one({
                "username": user_name,
                "trusted_karma": trusted_karma,
                "top_100_karma": top_100_karma,
                "top_50_karma": top_50_karma,
                "top_25_karma": top_25_karma,
                "top_10_karma": top_10_karma
            })
        except pymongo.errors.DuplicateKeyError:
            continue


if __name__ == '__main__':
    main()
