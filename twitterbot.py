import csv
import os
import sys
import time
import traceback

import click
import tweepy


@click.command()
@click.option('--consumer_key', default=os.environ.get('CONSUMER_KEY'),
              help='CONSUMER_KEY')
@click.option('--consumer_secret', default=os.environ.get('CONSUMER_SECRET'),
              help='CONSUMER_KEY')
@click.option('--access_token', default=os.environ.get('ACCESS_TOKEN'),
              help='ACCESS_TOKEN')
@click.option('--access_token_secret',
              default=os.environ.get('ACCESS_TOKEN_SECRET'),
              help='ACCESS_TOKEN_SECRET')
@click.option('--limit', default=1000,
              help='set limit amount of users you want to follow')
def main(consumer_key, consumer_secret, access_token,
         access_token_secret, limit):
    with open('twitter_usernames.csv', 'r') as file:
        list_users = []
        reader = csv.reader(file)
        for row in reader:
            list_users.append(row[0])
    list_users = list(set(list_users))
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(
        auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True,
        retry_count=10, retry_delay=5,
        retry_errors=None
    )
    currrent_user = api.me().screen_name
    cached_users = cache_handler(api, currrent_user)
    counter = 0
    try:
        with open('followers_cache_{}.txt'.format(currrent_user), 'r') as f:
            cached_local_users = [line.rstrip('\n') for line in f]
    except:
        cached_local_users = []
    cached_users.extend(cached_local_users)
    cached_users = list(set(cached_users))
    try:
        for user in list_users:
            if user and user not in cached_users:
                try:
                    if api.get_user(user).followers_count > 200:
                        counter = create_fr(api, user, cached_users,
                                                   counter, limit)
                    else:
                        print("Skipped " + user + '\n')
                except:
                        pass

    finally:
        with open('followers_cache_{}.txt'.format(currrent_user), 'w') as f:
            f.writelines(["%s\n" % item for item in cached_users])


def cache_handler(api, currrent_user):
    usernames = []
    for page in tweepy.Cursor(api.friends_ids,
                              screen_name=currrent_user).pages():
        wanted_parts = round(len(page) / 100) + 1
        parts = split_list(page, wanted_parts)
        for part in parts:
            users_part = api.lookup_users(user_ids=part)
            for username in users_part:
                usernames.append(username.screen_name)
        time.sleep(60)
    return usernames


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]


def create_fr(api, user, cached_users, counter, limit):
    print("Follow " + user)
    try:
        api.create_friendship(user)
    except tweepy.error.TweepError:
        traceback.print_exc(file=sys.stdout)
    cached_users.append(user)
    counter += 1
    if counter >= limit:
        return
    return counter, limit


if __name__ == "__main__":
    main()
