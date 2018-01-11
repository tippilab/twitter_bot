import logging
import os

import tweepy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

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

    current_user = api.me().screen_name
    friends_id = api.friends_ids(current_user)

    with open('friends_{}.txt'.format(current_user), 'w') as f:
        for f_id in friends_id:
            name = api.get_user(f_id).screen_name
            logger.info("Write %s", name)
            f.write(name + ' \n')


if __name__ == "__main__":
    main()
