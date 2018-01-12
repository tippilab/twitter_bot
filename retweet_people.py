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
        retry_errors=None
    )

    with open('need_retweet_list_people.txt', 'r') as f:
        retweet_people = [line.rstrip('\n') for line in f]

    with open('the_key_words.txt', 'r') as f:
        key_words = [line.rstrip('\n') for line in f]


    for name in retweet_people:
        all_post = api.user_timeline(
            screen_name=name)  # Returns the 20 most recent tw.
        for post in all_post:
            for the_key in key_words:
                if the_key in post.text.lower():
                    try:
                        api.retweet(post.id)
                        logger.info('Retweet %s', post.id)
                    except tweepy.TweepError:
                        logging.exception('Pass %s', post.id)


if __name__ == "__main__":
    main()
