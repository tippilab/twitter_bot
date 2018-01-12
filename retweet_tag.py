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

    query = 'python programming'
    max_tweets = 10000
    searched_tweets = [status for status in tweepy.Cursor(
        api.search, q=query, lang='en').items(max_tweets)]

    for tweet in searched_tweets:
        if tweet.user.followers_count > 300 \
                and tweet.retweet_count > 50 and tweet.favorite_count > 50:
            api.retweet(tweet.id)
            logger.info('Retweet %s', tweet.id)


if __name__ == "__main__":
    main()
