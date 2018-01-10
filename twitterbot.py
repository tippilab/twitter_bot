import csv
import logging
import os
import time

import click
import tweepy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--filename', default='twitter_usernames.csv',
              help='filename with usernames list of users you want to follow')
@click.option('--limit', default=1000,
              help='set limit amount of users you want to follow')
def main(limit, filename):
    with open(filename, 'r') as file:
        list_users = []
        reader = csv.reader(file)
        for row in reader:
            list_users.append(row[0])
    list_users = list(set(list_users))
    logger.info("Successfull reading of usernames file")

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
        retry_errors=None
    )

    current_user = api.me().screen_name
    cached_users = cache_handler(api, current_user)
    counter = 0
    try:
        with open('followers_cache_{}.txt'.format(current_user), 'r') as f:
            cached_local_users = [line.rstrip('\n') for line in f]
        logger.debug("Successfull reading of local cache")
    except:
        cached_local_users = []
        logger.debug("No local cache detected, new cache file will be created")
    cached_users.extend(cached_local_users)
    cached_users = list(set(cached_users))
    try:
        for user in list_users:
            if user and user not in cached_users:
                try:
                    if api.get_user(user).followers_count > 300:
                        logger.info("Follow %s", user)
                        api.create_friendship(user)
                except tweepy.error.TweepError:
                    logger.exception('')
                cached_users.append(user)
                counter += 1
                if counter >= limit:
                    logger.info("The limit of %s followings is reached", limit)
                    return
            else:
                logger.info("Skipped %s", user)
    finally:
        logger.info('Writiind local cache into"followers_cache_%s.txt"',
                    current_user)
        with open('followers_cache_{}.txt'.format(current_user), 'w') as f:
            f.writelines(["%s\n" % item for item in cached_users])


def cache_handler(api, current_user):
    usernames = []
    logger.info(
        "Start fetching %s follwers into local cache", current_user)
    for page in tweepy.Cursor(api.friends_ids,
                              screen_name=current_user).pages():
        wanted_parts = round(len(page) / 100) + 1
        parts = split_list(page, wanted_parts)
        for part in parts:
            users_part = api.lookup_users(user_ids=part)
            for username in users_part:
                usernames.append(username.screen_name)
        logger.debug("Part finished. Waiting 60 seconds to continue")
        time.sleep(60)
    logger.info("Finished fetching followers to local cache")
    return usernames


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]


if __name__ == "__main__":
    main()
