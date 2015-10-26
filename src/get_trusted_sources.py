#!/usr/bin/env python3
# reddit-reliability

import praw
import reddit_util


def main():
    r = praw.Reddit(user_agent=reddit_util.get_user_agent())

    sources = reddit_util.get_trusted_sources()

    submissions = r.get_subreddit('news').get_hot()
    for sub in submissions:
        # Save the username of the author.
        sources.add(sub.domain)

    reddit_util.store_trusted_sources(sources)


if __name__ == '__main__':
    main()
