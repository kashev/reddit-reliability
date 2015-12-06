#!/usr/bin/env python
## -*- coding: utf-8 -*-
# reddit-reliability

from pymongo import MongoClient
from textstat.textstat import textstat


def main():
    mongo_client = MongoClient('mongodb://cs598tar:cs598tar@'
                               '107.170.215.176:27017')
    reddit_data = mongo_client.reddit_data
    print(reddit_data.collection_names(include_system_collections=False))
    user_data = reddit_data.user_data
    user_comments = reddit_data.user_comments


if __name__ == '__main__':
    main()
