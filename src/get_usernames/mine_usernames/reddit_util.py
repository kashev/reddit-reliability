#!/usr/bin/env python
# reddit-reliability

import random

# TODO: add everyone.
USER_AGENT = "Script by /u/kdalmia for a UIUC CS 598tar Research Project"


def get_user_agent():
    """Get the user agent we're using for this project, for the Reddit API. """
    return USER_AGENT


def load_file_as_set(file_name):
    """ Given a file name, load that file as a set, and return it. """
    with open(file_name, 'r') as f:
        return set(line.strip() for line in f)


def write_set_as_file(s, file_name):
    """ Given a set s and a file name, write that set to file. """
    with open(file_name, 'w') as f:
        for item in sorted(s):
            f.write('{}\n'.format(item))


def get_subreddit_names():
    """ A generator that gives the names of subreddits we care about from
        config/important_subreddits.txt.
    """
    with open('config/important_subreddits.txt', 'r') as f:
        for line in f.readlines():
            yield line.strip()


def get_usernames():
    """ Return a set of usernames, loaded from file. """
    return load_file_as_set('config/usernames.txt')


def store_usernames(usernames):
    """ Write the set of usernames to file. Ensure that none are lost by merging
        the input set with what's already in the file.
    """
    existing_usernames = get_usernames()
    all_usernames = existing_usernames.union(usernames)
    write_set_as_file(all_usernames, 'config/usernames.txt')


def get_N_random_users(N=1000, from_file=False):
    """ Return N random users. """
    if from_file:
        return load_file_as_set('config/random_N_users.txt')
    else:
        all_users = get_usernames()
        return random.sampe(all_users, N)


def store_random_users(usernames):
    """ Store a set of users to the list of random_N_users, for repeatability
        of experiements.
    """
    write_set_as_file(usernames, 'config/random_N_users.txt')


def get_trusted_sources():
    """ Return a set of trusted sources, loaded from file. """
    return load_file_as_set('config/trusted_sources.txt')


def store_trusted_sources(usernames):
    """ Write the set of trusted sources to file. Ensure that none are lost by
        merging the input set with what's already in the file.
    """
    existing_sources = load_file_as_set('config/trusted_sources.txt')
    all_sources = existing_sources.union(usernames)
    write_set_as_file(all_sources, 'config/trusted_sources.txt')


def get_trusted_subreddits():
    """ Return a set of the names of 'trusted' subreddits. """
    return load_file_as_set('config/trusted_subreddits.txt')
