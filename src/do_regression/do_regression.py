#!/usr/bin/env python
# -*- coding: utf-8 -*-
# reddit-reliability

import argparse

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from sklearn.ensemble import RandomForestRegressor
from matplotlib.ticker import FuncFormatter


def train_model(num_trees):
    np.set_printoptions(threshold=np.nan, suppress=True)

    training_usernames = np.load("data/training_usernames.npy")
    training_input_matrix = np.load("data/training_input_matrix.npy")
    training_output_vector = np.load("data/training_output_vector.npy")
    test_usernames = np.load("data/test_usernames.npy")
    test_input_matrix = np.load("data/test_input_matrix.npy")

    features_to_use = np.array([
        0,   # is_gold
        1,   # has_verified_email
        2,   # time_created
        3,   # reading_level
        # 4,   # link_karma
        5,   # number_posts_gilded
        # 6,   # number_posts
        # 7,   # link_karma / number_posts
        8,   # number_posts_gilded / number_posts
        # 9,   # comment_karma
        10,   # number_comments_gilded
        # 11,  # comment_karma / number_comments
        12,  # number_comments_gilded / number_comments
        13,  # trusted_post_karma / link_karma
        14,  # top_100_post_karma / link_karma
        15,  # top_50_post_karma / link_karma
        16,  # top_25_post_karma / link_karma
        17,  # top_10_post_karma / link_karma
        18,  # trusted_comment_karma / comment_karma
        # 19,  # top_100_comment_karma / comment_karma
        20,  # top_50_comment_karma / comment_karma
        21,  # top_25_comment_karma / comment_karma
        22,  # top_10_comment_karma / comment_karma
        23,  # swear_count / word_count
        24,  # unique_words / word_count
    ])

    feature_names = np.array([
        "is_gold",
        "has_verified_email",
        "time_created",
        "reading_level",
        "link_karma",
        "number_posts_gilded",
        "number_posts",
        "link_karma / number_posts",
        "number_posts_gilded / number_posts",
        "comment_karma",
        "number_comments_gilded",
        "comment_karma / number_comments",
        "number_comments_gilded / number_comments",
        "trusted_post_karma / link_karma",
        "top_100_post_karma / link_karma",
        "top_50_post_karma / link_karma",
        "top_25_post_karma / link_karma",
        "top_10_post_karma / link_karma",
        "trusted_comment_karma / comment_karma",
        "top_100_comment_karma / comment_karma",
        "top_50_comment_karma / comment_karma",
        "top_25_comment_karma / comment_karma",
        "top_10_comment_karma / comment_karma",
        "swear_count / word_count",
        "unique_words / word_count",
    ])
    used_feature_names = feature_names[features_to_use]

    model = RandomForestRegressor(n_estimators=num_trees, n_jobs=-1, verbose=1)
    model.fit(training_input_matrix[:, features_to_use], training_output_vector)
    # score = model.score(test_input, test_output)

    predictions = model.predict(test_input_matrix[:, features_to_use])

    weights = np.ones_like(predictions)/float(len(predictions))

    for bins in [2, 20, 200]:
        plt.figure()
        plt.hist(predictions, bins, weights=weights)
        plt.xlabel('Reddit Reliability Score')
        plt.ylabel('Probability ({} bins)'.format(bins))
        plt.title('Reddit Reliability Score for {} Test Users'
                  .format(test_input_matrix.shape[0]))
        plt.grid(True)
        plt.savefig('figs/data_{}.png'.format(bins))

    zipped = zip(test_usernames, predictions)
    zipped.sort(key=lambda t: t[1])

    with open('results/scores.txt', 'w') as f:
        for name, score in zipped:
            f.write("{} \t {}\n".format(score, name))

    importance = model.feature_importances_
    print model.feature_importances_

    zipped = zip(used_feature_names, importance)
    zipped.sort(key=lambda t: t[1])

    with open('results/result.txt', 'w') as f:
        for feature, weight in zipped:
            f.write("{} : {}\n".format(weight, feature))

    plt.figure()
    plt.hexbin(predictions, test_input_matrix[:, 3], bins='log')
    plt.xlabel('Reddit Reliability Score')
    plt.ylabel('Average Readability')
    plt.title('Reliability vs Readability')
    plt.savefig('figs/reliability_readability.png')

    plt.figure()
    normed_karma = test_input_matrix[:, 4]
    for i in range(len(normed_karma)):
        if normed_karma[i] > 10000:
            normed_karma[i] = 10000
    plt.scatter(predictions, normed_karma)
    plt.ylim(0, 10000)
    plt.grid(True)
    plt.xlabel('Reddit Reliability Score')
    plt.ylabel('Post Karma')
    plt.title('Reliability vs Karma')
    plt.savefig('figs/reliability_post_karma.png')

    plt.figure()
    plt.scatter(predictions, test_input_matrix[:, 8])
    plt.grid(True)
    plt.xlabel('Reddit Reliability Score')
    plt.ylabel('Gilded Percentage')
    plt.title('Reliability vs Gilded Post Percentage')
    plt.savefig('figs/reliability_gilded.png')

    plt.figure()
    plt.scatter(predictions, test_input_matrix[:, 6])
    plt.grid(True)
    plt.xlabel('Reddit Reliability Score')
    plt.ylabel('Post Count')
    plt.title('Reliability vs Post Count')
    plt.savefig('figs/reliability_post_count.png')

    scores_yes_email = predictions[test_input_matrix[:, 1].astype(bool)]
    scores_no_email = predictions[np.logical_not(
        test_input_matrix[:, 1].astype(bool))]
    plt.figure()
    weights_yes = np.ones_like(scores_yes_email)/float(len(scores_yes_email))
    weights_no = np.ones_like(scores_no_email)/float(len(scores_no_email))

    plt.hist(scores_yes_email, 20, weights=weights_yes,
             alpha=0.5, label='Email')
    plt.hist(scores_no_email, 20, weights=weights_no,
             alpha=0.5, label='No')
    plt.xlabel('Reddit Reliability Score')
    plt.ylabel('Probability ({} bins)'.format(20))
    plt.title('Reddit Reliability Score for Users by Email')
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.savefig('figs/data_{}_email.png'.format(20))


def main():
    """ Train and evaluate a Hidden Forest """
    parser = argparse.ArgumentParser(
        description=("Feature Correspondence Compute for Reddit"))

    parser.add_argument("-n", "--num_trees", type=int, default=1000,
                        help="Specify number of decision trees in forest")
    args = parser.parse_args()

    train_model(args.num_trees)


if __name__ == '__main__':
    main()
