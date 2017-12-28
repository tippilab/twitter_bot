import os

import csv
import tweepy

with open('followers.txt', 'r') as file:
    list_users_url = []
    reader = csv.reader(file)
    for row in reader:
        list_users_url.append(row[0])

list_users = []
for user_url in list_users_url:
    if 'https://twitter.com/' in user_url:
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


with open('followers_cache.txt', 'a') as f:
    for user in list_users:
        print("Follow " + user)
        api.create_friendship(user)
        f.write('https://twitter.com/' + user + '\n')
