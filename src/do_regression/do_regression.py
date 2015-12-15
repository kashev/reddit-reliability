#!/usr/bin/env python
# -*- coding: utf-8 -*-
# reddit-reliability

import argparse

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor


def train_model(num_trees):
    np.set_printoptions(threshold=np.nan, suppress=True)

    training_usernames = np.load("data/training_usernames.npy")
    training_input_matrix = np.load("data/training_input_matrix.npy")
    training_output_vector = np.load("data/training_output_vector.npy")
    test_usernames = np.load("data/test_usernames.npy")
    test_input_matrix = np.load("data/test_input_matrix.npy")
    feature_names = np.load("data/feature_docs.npy")
    for feature, idx in zip(feature_names, range(len(feature_names))):
        print idx, feature

    # Gives the ability to turn features off.
    features_to_use = np.arange(len(feature_names))

    assert(len(feature_names) == len(features_to_use))

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

    zipped = zip(used_feature_names, importance * 100)
    zipped.sort(key=lambda t: t[1], reverse=True)

    with open('results/result.txt', 'w') as f:
        for feature, weight in zipped:
            f.write("{} & {:.2f}\\\\\n".format(feature, weight))

    plt.figure()
    plt.hexbin(predictions, test_input_matrix[:, 3], bins='log')
    plt.xlabel('Reddit Reliability Score')
    plt.ylabel('Average Readability')
    plt.title('Reliability vs Readability')
    plt.savefig('figs/reliability_readability.png')

    plt.figure()
    plt.scatter(predictions, test_input_matrix[:, 4])
    plt.ylim(0, 20000)
    plt.grid(True)
    plt.xlabel('Reddit Reliability Score')
    plt.ylabel('Post Karma')
    plt.title('Reliability vs Post Karma')
    plt.savefig('figs/reliability_post_karma.png')

    plt.figure()
    plt.scatter(predictions, test_input_matrix[:, 5])
    plt.ylim(0, 200000)
    plt.grid(True)
    plt.xlabel('Reddit Reliability Score')
    plt.ylabel('Comment Karma')
    plt.title('Reliability vs Comment Karma')
    plt.savefig('figs/reliability_comment_karma.png')

    plt.figure()
    plt.scatter(predictions, test_input_matrix[:, 10])
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

    plt.figure()
    plt.scatter(predictions, test_input_matrix[:, 7])
    plt.grid(True)
    plt.xlabel('Reddit Reliability Score')
    plt.ylabel('Comment Count')
    plt.title('Reliability vs Comment Count')
    plt.savefig('figs/reliability_comment_count.png')

    plt.figure()
    plt.scatter(predictions, test_input_matrix[:, 10])
    plt.grid(True)
    plt.ylim(0, 5000)
    plt.xlabel('Reddit Reliability Score')
    plt.ylabel('Average Karma per Post')
    plt.title('Reliability vs Average Karma per Post')
    plt.savefig('figs/reliability_avg_post_karma.png')

    plt.figure()
    plt.scatter(predictions, test_input_matrix[:, 12])
    plt.grid(True)
    plt.ylim(0, 5000)
    plt.xlabel('Reddit Reliability Score')
    plt.ylabel('Average Karma per Comment')
    plt.title('Reliability vs Average Karma per Comment')
    plt.savefig('figs/reliability_avg_comment_karma.png')

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

    parser.add_argument("-n", "--num_trees", type=int, default=5000,
                        help="Specify number of decision trees in forest")
    args = parser.parse_args()

    train_model(args.num_trees)


if __name__ == '__main__':
    main()
