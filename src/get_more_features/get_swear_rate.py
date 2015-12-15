#!/usr/bin/env python
## -*- coding: utf-8 -*-
# reddit-reliability

from __future__ import division

import pymongo
import re
from pymongo import MongoClient
from collections import Counter


def main():
    mongo_client = MongoClient('mongodb://cs598tar:cs598tar@'
                               '107.170.215.176:27017')
    reddit_data = mongo_client.reddit_data
    user_data = reddit_data.user_data
    user_word_stats = reddit_data.user_word_stats
    user_comments = reddit_data.user_comments

    user_word_stats.create_index(
        [("username", pymongo.ASCENDING)],
        background=True,
        unique=True,
        dropDups=True
    )

    # Load in Googles List of Swear Words
    bad_words = set()
    lines = [line.rstrip('\n').lower() for line in
             open('../config/googles_bad_words.txt')]
    for line in lines:
        bad_words.add(line)

    for user in user_data.find(no_cursor_timeout=True).sort('data.name', 1):
        name = user['data']['name']
        print name
        comment_list = []
        for comment in user_comments.find({'data.author': name}):
            if comment['kind'] == 't1':  # Actually a comment
                comment_text = comment['data']['body']
                comment_list.append(comment_text)

        comment_book = ' '.join(comment_list).strip()
        word_list = re.sub("[^\w]", " ",  comment_book).split()
        word_list = [w.lower() for w in word_list]
        word_list_len = len(word_list)
        print word_list_len

        wordcounter = Counter(word_list)
        unique_words = len(wordcounter)

        # Count the bad words
        swear_count = 0
        for swear in bad_words:
            swear_count += wordcounter[swear]

        if word_list_len > 0:
            swear_rate = swear_count / word_list_len
        else:
            swear_rate = 0

        word_stat_data = {
            'username': name,
            'word_count': word_list_len,
            'swear_count': swear_count,
            'swear_rate': swear_rate,
            'unique_words': unique_words
        }

        try:
            user_word_stats.insert_one(word_stat_data)
        except pymongo.errors.DuplicateKeyError:
            continue

if __name__ == '__main__':
    main()
