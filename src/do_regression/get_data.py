#!/usr/bin/env python
# -*- coding: utf-8 -*-
# reddit-reliability

# http://scikit-learn.org/stable/modules/tree.html#classification

from pymongo import MongoClient
import numpy as np


def main():
    mongo_client = MongoClient('mongodb://cs598tar:cs598tar@'
                               '107.170.215.176:27017')
    reddit_data = mongo_client.reddit_data
    print(reddit_data.collection_names(include_system_collections=False))
    user_data = reddit_data.user_data
    important_karma = reddit_data.important_karma
    user_reading_level = reddit_data.user_reading_level
    number_of_comments = reddit_data.number_of_comments
    number_of_posts = reddit_data.number_of_posts
    gilded_count = reddit_data.gilded_count

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

    for user_mongo in user_data.find():
        user_name = user_mongo['data']['name']
        print(user_name)

        feature_vector = []

        feature_vector.append(user_mongo['data']['link_karma'])
        feature_vector.append(user_mongo['data']['comment_karma'])
        try:
            feature_vector.append(int(user_mongo['data']['is_gold']))
        except TypeError:
            feature_vector.append(False)
        try:
            feature_vector.append(int(user_mongo['data']['is_mod']))
        except TypeError:
            feature_vector.append(False)
        try:
            feature_vector.append(int(user_mongo['data']['has_verified_email']))
        except TypeError:
            feature_vector.append(False)
        feature_vector.append(user_mongo['data']['created'])

        # Get this users important karma
        res = important_karma.find({'username': user_name})[0]

        feature_vector.append(res['important_karma'])
        feature_vector.append(res['trusted_karma'])

        # Get users reading level
        res = user_reading_level.find({'username': user_name})[0]
        feature_vector.append(res['reading_level'])

        # Get absolute number of posts
        res = number_of_comments.find({'username': user_name})[0]
        feature_vector.append(res['number_comments'])
        res = number_of_posts.find({'username': user_name})[0]
        feature_vector.append(res['number_posts'])

        # Get absolute number of gilded posts and comments
        res = gilded_count.find({'username': user_name})[0]
        feature_vector.append(res['number_posts'])
        feature_vector.append(res['number_comments'])

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
