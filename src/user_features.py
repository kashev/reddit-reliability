#!/usr/bin/env python3
# reddit-reliability

import reddit_util

TRUSTED_SOURCES = reddit_util.get_trusted_sources()
TRUSTED_SUBREDDITS = reddit_util.get_trusted_subreddits()


def has_verified_email(user):
    """ Given a user, return if the user has a verified email or not. """
    return user.has_verified_email


def is_mod(user):
    """ Given a user, return if the user is a moderator anywhere. """
    return user.is_mod


def account_creation_time(user):
    """ Given a user, give the UTC timestamp at which the user was created. """
    return user.created_utc


def percentage_trusted_sources(user):
    """ Given a user, give the percentage of their posts which come from
        'reputable' sources.
    """
    number_submissions = 0
    number_trusted_sources = 0
    for sub in user.get_submitted():
        number_submissions += 1
        if sub.domain in TRUSTED_SOURCES:
            number_trusted_sources += 1
    return number_trusted_sources / number_submissions


def karma_from_trusted_subreddits(user):
    """ Given a user, give the amount of karma they have from subreddits which
        are marked as trusted.
    """
    trusted_karma = 0
    for submission in user.get_submitted():
        if submission.subreddit.display_name in TRUSTED_SUBREDDITS:
            trusted_karma += submission.score
    for comment in user.get_comments():
        if comment.subreddit.display_name in TRUSTED_SUBREDDITS:
            trusted_karma += comment.score
    return trusted_karma
