#!/usr/bin/env python
# reddit-reliability

import praw
import pprint

import reddit_util


def main():
    r = praw.Reddit(user_agent=reddit_util.get_user_agent())

    usernames = reddit_util.get_N_random_users(from_file=True)

    for user_name in usernames:
        print(user_name)
        user = r.get_redditor(user_name)

        gen = user.get_submitted(limit=None)

        karma_by_subreddit = {}
        for thing in gen:
            subreddit = thing.subreddit.display_name
            karma_by_subreddit[subreddit] = (
                karma_by_subreddit.get(subreddit, 0) + thing.score)

        pprint.pprint(karma_by_subreddit)


if __name__ == '__main__':
    main()
