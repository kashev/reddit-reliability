#!/usr/bin/env python3
# reddit-reliability

# TODO: add everyone.
USER_AGENT = "Script by /u/kdalmia for a UIUC CS 598tar Research Project"


def get_user_agent():
    """Get the user agent we're using for this project, for the Reddit API. """
    return USER_AGENT


def get_subreddit_names():
    """ A generator that gives the names of subreddits we care about from
        config/important_subreddits.txt.
    """
    with open('config/important_subreddits.txt', 'r') as f:
        for line in f.readlines():
            yield line.strip()


def get_usernames():
    """ Return a set of usernames, loaded from file. """
    with open('config/usernames.txt', 'r') as f:
        return set(line.strip() for line in f)


def store_usernames(usernames):
    """ Write the set of usernames to file. Ensure that none are lost by merging
        the input set with what's already in the file.
    """
    with open('config/usernames.txt', 'r') as f:
        existing_usernames = set(line.strip() for line in f)

    all_usernames = existing_usernames.union(usernames)

    with open('config/usernames.txt', 'w') as f:
        for username in all_usernames:
            f.write('{}\n'.format(username))


def get_trusted_sources():
    """ Return a set of usernames, loaded from file. """
    with open('config/trusted_sources.txt', 'r') as f:
        return set(line.strip() for line in f)


def store_trusted_sources(usernames):
    """ Write the set of usernames to file. Ensure that none are lost by merging
        the input set with what's already in the file.
    """
    with open('config/trusted_sources.txt', 'r') as f:
        existing_sources = set(line.strip() for line in f)

    all_sources = existing_sources.union(usernames)

    with open('config/trusted_sources.txt', 'w') as f:
        for source in all_sources:
            f.write('{}\n'.format(source))
