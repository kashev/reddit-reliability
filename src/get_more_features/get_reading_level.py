#!/usr/bin/env python
## -*- coding: utf-8 -*-
# reddit-reliability

import pymongo
from textstat.textstat import textstat
from pymongo import MongoClient


def main():
    mongo_client = MongoClient('mongodb://cs598tar:cs598tar@'
                               '107.170.215.176:27017')
    reddit_data = mongo_client.reddit_data
    user_data = reddit_data.user_data
    user_reading_level = reddit_data.user_reading_level
    user_comments = reddit_data.user_comments

    user_reading_level.create_index(
        [("username", pymongo.ASCENDING)],
        background=True,
        unique=True,
        dropDups=True
    )

    for user in user_data.find():
        name = user['data']['name']
        print name
        comment_list = []
        for comment in user_comments.find({'data.author': name}):
            if comment['kind'] == 't1':  # Actually a comment
                comment_text = comment['data']['body']
                comment_list.append(comment_text)

        comment_book = ' '.join(comment_list).strip()
        try:
            if len(comment_book) > 0:
                reading_ease = textstat.flesch_reading_ease(comment_book)
            else:
                reading_ease = 0
        except TypeError:  # I hate textstat
            reading_ease = 0

        reading_level_data = {'username': name,
                              'reading_level': reading_ease}

        try:
            user_reading_level.insert_one(reading_level_data)
        except pymongo.errors.DuplicateKeyError:
            continue

if __name__ == '__main__':
    main()
