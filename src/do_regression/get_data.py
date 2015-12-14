#!/usr/bin/env python
# -*- coding: utf-8 -*-
# reddit-reliability

# http://scikit-learn.org/stable/modules/tree.html#classification

from __future__ import division
from pymongo import MongoClient
import numpy as np


def main():
    mongo_client = MongoClient('mongodb://cs598tar:cs598tar@'
                               '107.170.215.176:27017')
    reddit_data = mongo_client.reddit_data
    print(reddit_data.collection_names(include_system_collections=False))

    # Read in Training User Names and 'Labels'
    reliable_users = set()
    lines = [line.rstrip('\n') for line in
             open('../config/reliable_users.txt')]
    for line in lines:
        reliable_users.add(line)

    bad_users = set()
    lines = [line.rstrip('\n') for line in
             open('../../getStats/badset.txt')]
    for line in lines:
        bad_users.add(line)

    training_usernames = []
    training_input_matrix = []
    training_output_vector = []

    test_usernames = []
    test_input_matrix = []

    for user_mongo in reddit_data.user_data.find().sort('data.name', 1):
        user_name = user_mongo['data']['name']
        print(user_name)

        feature_vector = []

        link_karma = user_mongo['data']['link_karma']
        comment_karma = user_mongo['data']['comment_karma']

        try:
            is_gold = int(user_mongo['data']['is_gold'])
        except TypeError:
            is_gold = False
        try:
            is_mod = int(user_mongo['data']['is_mod'])
        except TypeError:
            is_mod = False
        try:
            has_verified_email = int(user_mongo['data']['has_verified_email'])
        except TypeError:
            has_verified_email = False

        time_created = user_mongo['data']['created']

        user_query = {'username': user_name}

        # Get users reading level
        res = reddit_data.user_reading_level.find(user_query)[0]
        reading_level = res['reading_level']

        # Get absolute number of posts
        res = reddit_data.number_of_comments.find(user_query)[0]
        number_comments = res['number_comments']
        res = reddit_data.number_of_posts.find(user_query)[0]
        number_posts = res['number_posts']

        # Get absolute number of gilded posts and comments
        res = reddit_data.gilded_count.find(user_query)[0]
        number_posts_gilded = res['number_posts']
        number_comments_gilded = res['number_comments']

        # Get Word Stats
        res = reddit_data.user_word_stats.find(user_query)[0]
        word_count = res['word_count']
        swear_count = res['swear_count']
        unique_words = res['unique_words']

        # Get Karma From Important Places
        res = reddit_data.important_post_karma.find(user_query)[0]
        trusted_post_karma = res['trusted_karma']
        top_100_post_karma = res['top_100_karma']
        top_50_post_karma = res['top_50_karma']
        top_25_post_karma = res['top_25_karma']
        top_10_post_karma = res['top_10_karma']

        res = reddit_data.important_comment_karma.find(user_query)[0]
        trusted_comment_karma = res['trusted_karma']
        top_100_comment_karma = res['top_100_karma']
        top_50_comment_karma = res['top_50_karma']
        top_25_comment_karma = res['top_25_karma']
        top_10_comment_karma = res['top_10_karma']

        # Append features
        feature_vector.append(is_gold)
        feature_vector.append(has_verified_email)
        feature_vector.append(time_created)
        feature_vector.append(reading_level)

        feature_vector.append(link_karma)
        feature_vector.append(number_posts_gilded)
        feature_vector.append(number_posts)
        feature_vector.append(number_comments)

        try:
            feature_vector.append(link_karma / number_posts)
            feature_vector.append(number_posts_gilded / number_posts)
        except ZeroDivisionError:
            feature_vector.extend([0] * 2)

        feature_vector.append(comment_karma)
        feature_vector.append(number_comments_gilded)

        try:
            feature_vector.append(comment_karma / number_comments)
            feature_vector.append(number_comments_gilded / number_comments)
        except ZeroDivisionError:
            feature_vector.extend([0] * 2)
        try:
            feature_vector.append(trusted_post_karma / link_karma)
            feature_vector.append(top_100_post_karma / link_karma)
            feature_vector.append(top_50_post_karma / link_karma)
            feature_vector.append(top_25_post_karma / link_karma)
            feature_vector.append(top_10_post_karma / link_karma)
        except ZeroDivisionError:
            feature_vector.extend([0] * 5)

        try:
            feature_vector.append(trusted_comment_karma / comment_karma)
            feature_vector.append(top_100_comment_karma / comment_karma)
            feature_vector.append(top_50_comment_karma / comment_karma)
            feature_vector.append(top_25_comment_karma / comment_karma)
            feature_vector.append(top_10_comment_karma / comment_karma)
        except ZeroDivisionError:
            feature_vector.extend([0] * 5)

        try:
            feature_vector.append(swear_count / word_count)
            feature_vector.append(unique_words / word_count)
        except ZeroDivisionError:
            feature_vector.extend([0] * 2)

        # Categorize the users
        if user_name in reliable_users:
            training_input_matrix.append(feature_vector)
            training_output_vector.append(1.0)
            training_usernames.append(user_name)
        elif user_name in bad_users:
            training_input_matrix.append(feature_vector)
            training_output_vector.append(-1.0)
            training_usernames.append(user_name)
        else:
            test_input_matrix.append(feature_vector)
            test_usernames.append(user_name)

    np.save("data/training_usernames.npy",
            training_usernames)
    np.save("data/training_input_matrix.npy",
            training_input_matrix)
    np.save("data/training_output_vector.npy",
            training_output_vector)
    np.save("data/test_usernames.npy",
            test_usernames)
    np.save("data/test_input_matrix.npy",
            test_input_matrix)


if __name__ == '__main__':
    main()
