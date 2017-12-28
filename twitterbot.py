import os

import tweepy

list_users_url = []
f = open('followers.txt')
for line in f:
    list_users_url.append(line)
f.close()

list_users = []

for user_url in list_users_url:
    list_users.append(user_url.split('https://twitter.com/')[-1])

consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(
    auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True,
    retry_count=10, retry_delay=5,
    retry_errors=5
)

for user in list_users:
    print("Follow " + user)
    api.create_friendship(user)
