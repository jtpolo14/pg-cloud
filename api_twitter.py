#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Downloads all tweets from a given user.
Uses twitter.Api.GetUserTimeline to retreive the last 3,200 tweets from a user.
Twitter doesn't allow retreiving more tweets than this through the API, so we get
as many as possible.
config.py should contain the imported variables.

Forked from https://github.com/bear/python-twitter/blob/master/examples/get_all_user_tweets.py

CHANGE LOG

---NAME---  ---Date--- ---------Note---------
 J.Thomas   01-01-2022 Initial Draft

"""

from __future__ import print_function

import json
import sys

import twitter
from config import TWITTER_ACCESS_TOKEN_KEY, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET


class Worker:
    def __init__(self, WORKER_CONSUMER_KEY, WORKER_CONSUMER_SECRET, WORKER_ACCESS_TOKEN_KEY, WORKER_ACCESS_TOKEN_SECRET):
         self.api = twitter.Api(
        WORKER_CONSUMER_KEY, WORKER_CONSUMER_SECRET, WORKER_ACCESS_TOKEN_KEY, WORKER_ACCESS_TOKEN_SECRET
    )
    def get_tweets_for_user(self, screen_name):
        return get_tweets(api=self.api, screen_name=screen_name)

    def get_followers_for_user(self, screen_name):
        return get_followers(api=self.api, screen_name=screen_name)

def get_tweets(api=None, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("getting tweets before:", earliest_tweet)

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline


def get_followers(api=None, screen_name=None):
    followers = api.GetFollowers(screen_name=screen_name)
    print("getting followers...",)

    return followers


if __name__ == "__main__":
    api = twitter.Api(
        TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN_KEY, TWITTER_ACCESS_TOKEN_SECRET
    )
    screen_name = sys.argv[1]
    run_code = sys.argv[2]
    print(screen_name, run_code)

    if run_code == 1:
        followers = get_followers(api=api, screen_name=screen_name)
        with open('followers.json', 'w+') as f:
            for follower in followers:
                f.write(json.dumps(follower._json))
                f.write('\n')

    elif run_code == 2:
        timeline = get_tweets(api=api, screen_name=screen_name)
        with open('timeline.json', 'w+') as f:
            for tweet in timeline:
                f.write(json.dumps(tweet._json))
                f.write('\n')
