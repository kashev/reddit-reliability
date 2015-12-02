#!/usr/bin/env python
# reddit-reliability

import praw
import inspect
import reddit_util
import user_features

r = praw.Reddit(user_agent='Test Script by /u/kdalmia'
                           ' for a UIUC CS 598tar Research Project')

# subreddit = r.get_subreddit('news')
# for c in inspect.getmembers(subreddit):
#     print(c)

# submissions = r.get_subreddit('news').get_hot(limit=5)
# for x in submissions:
#     # for y in x.comments:
#     #     for z in y.replies:
#     for c in inspect.getmembers(x):
#         print(c)
#     break

user = r.get_redditor('magenta_placenta')
# for y in user.get_submitted():
#     print(y.domain)
# for y in inspect.getmembers(user):
#     print(y)

print(user_features.has_verified_email(user))
print(user_features.is_mod(user))
print(user_features.account_creation_time(user))
print(user_features.percentage_trusted_sources(user))
print(user_features.karma_from_trusted_subreddits(user))

# print(user.link_karma, user.comment_karma)

# for x in user.get_comments():
#     for y in inspect.getmembers(x):
#         print(y)
#     break
