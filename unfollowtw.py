import logging
import os

import click
import tweepy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option('--limit', default=1000,
              help='set limit amount of users you want to follow')

def main(limit):

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

    currrent_user = api.me().screen_name
    friends = []
    with open('friends_{}.txt'.format(currrent_user), 'r') as f:
        for line in f:
            friends.append(line.strip())

    friends_cache = []
    with open('friends_cache_{}.txt'.format(currrent_user), 'r') as f:
        for line in f:
            friends_cache.append(line.strip())

    list_friends = [x for x in friends if x not in friends_cache]

    with open('friends_cache_{}.txt'.format(currrent_user), 'a') as f:
        for fr in range(limit):
            try:
                if api.get_user(list_friends[fr]).friends_count < 200:
                    api.destroy_friendship(list_friends[fr])
                    logger.info("Unfollow %s", list_friends[fr])
                    f.write(list_friends[fr] + ' \n')
                else:
                    logger.info("Add %s to file", list_friends[fr])
                    f.write(list_friends[fr] + ' \n')
            except:
                try:
                    if len(api.followers_ids(list_friends[fr])) < 200:
                        api.destroy_friendship(list_friends[fr])
                        logger.info("Unfollow %s", list_friends[fr])
                        f.write(list_friends[fr] + ' \n')
                    else:
                        logger.info("Add %s to file", list_friends[fr])
                        f.write(list_friends[fr] + ' \n')
                except:
                    pass

if __name__ == "__main__":
    main()
