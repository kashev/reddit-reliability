#!/usr/bin/env python
# -*- coding: utf-8 -*-
# reddit-reliability

import argparse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from sklearn.ensemble import RandomForestRegressor


def train_model(num_trees):
    np.set_printoptions(threshold=np.nan, suppress=True)

    training_usernames = np.load("data/training_usernames.npy")
    training_input_matrix = np.load("data/training_input_matrix.npy")
    training_output_vector = np.load("data/training_output_vector.npy")
    test_usernames = np.load("data/test_usernames.npy")
    test_input_matrix = np.load("data/test_input_matrix.npy")

    model = RandomForestRegressor(n_estimators=num_trees, n_jobs=-1, verbose=1)
    model.fit(training_input_matrix, training_output_vector)
    # score = model.score(test_input, test_output)

    predictions = model.predict(test_input_matrix)
    min_prediction = np.min(predictions)
    max_prediction = np.max(predictions)

    n, bins, patches = plt.hist(predictions, 100, normed=1,
                                facecolor='green', alpha=0.75)

    plt.xlabel('Reddit Reliability Score')
    plt.ylabel('Probability')
    plt.title('Reddit Reliability Score for {} Test Users'
              .format(test_input_matrix.shape[0]))
    plt.grid(True)

    plt.savefig('data.png')


def main():
    """ Train and evaluate a Hidden Forest """
    parser = argparse.ArgumentParser(
        description=("Feature Correspondence Compute for Reddit"))

    parser.add_argument("-n", "--num_trees", required=True, type=int,
                        help="Specify number of decision trees in forest")
    args = parser.parse_args()

    train_model(args.num_trees)


if __name__ == '__main__':
    main()
