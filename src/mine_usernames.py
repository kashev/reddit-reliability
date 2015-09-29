#!/usr/bin/env python3
# reddit-reliability

import praw
import reddit_util


def main():
    r = praw.Reddit(user_agent=reddit_util.get_user_agent())

    usernames = reddit_util.get_usernames()

    for subreddit_name in reddit_util.get_subreddit_names():
        submissions = r.get_subreddit(subreddit_name).get_hot()
        for sub in submissions:
            # Save the username of the author.
            usernames.add(sub.author.name)

            # Get the authors of comments.
            for comment in sub.comments:
                # Put in try block to get around deleted or removed comments:
                try:
                    usernames.add(comment.author.name)
                except AttributeError:
                    pass

    reddit_util.store_usernames(usernames)


if __name__ == '__main__':
    main()
