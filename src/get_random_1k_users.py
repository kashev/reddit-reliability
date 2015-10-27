#!/usr/bin/env python3
# reddit-reliability

import reddit_util
import random


def main():
    usernames = reddit_util.get_usernames()
    random_1k = random.sample(usernames, 1000)

    with open('config/random_1k_users.txt', 'w') as f:
        for username in sorted(random_1k):
            f.write('{}\n'.format(username))

if __name__ == '__main__':
    main()
