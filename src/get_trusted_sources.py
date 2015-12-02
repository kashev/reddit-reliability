#!/usr/bin/env python
# reddit-reliability

import praw
import reddit_util


def main():
    r = praw.Reddit(user_agent=reddit_util.get_user_agent())

    sources = reddit_util.get_trusted_sources()

    for sub in r.get_subreddit('news').get_hot():
        sources.add(sub.domain)
    for sub in r.get_subreddit('news').get_top():
        sources.add(sub.domain)
    for sub in r.get_subreddit('news').get_top_from_all():
        sources.add(sub.domain)
    for sub in r.get_subreddit('news').get_top_from_year():
        sources.add(sub.domain)
    for sub in r.get_subreddit('news').get_rising():
        sources.add(sub.domain)
    for sub in r.get_subreddit('news').get_controversial():
        sources.add(sub.domain)
    for sub in r.get_subreddit('news').get_controversial_from_all():
        sources.add(sub.domain)

    reddit_util.store_trusted_sources(sources)


if __name__ == '__main__':
    main()
