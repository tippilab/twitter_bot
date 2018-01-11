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
    friends = []
    with open('friends_{}.txt'.format(current_user), 'r') as f:
        for line in f:
            friends.append(line.strip())

    friends_cache = []
    with open('friends_un_cache_{}.txt'.format(current_user), 'r') as f:
        for line in f:
            friends_cache.append(line.strip())

    list_friends = [x for x in friends if x not in friends_cache]

    with open('friends_un_cache_{}.txt'.format(current_user), 'a') as f:
        try:
            for fr in list_friends:
                try:
                    if api.get_user(fr).followers_count < 300:
                        api.destroy_friendship(fr)
                        logger.info("Unfollow %s", fr)
                        f.write(fr + ' \n')
                    else:
                        logger.info("Add %s to file", fr)
                        f.write(fr + ' \n')
                except Exception:
                    logging.exception("Pass first try!")
                    try:
                        if len(api.followers_ids(fr)) < 300:
                            api.destroy_friendship(fr)
                            logger.info("Unfollow %s", fr)
                            f.write(fr + ' \n')
                        else:
                            logger.info("Add %s to file", fr)
                            f.write(fr + ' \n')
                    except Exception:
                        logging.exception("Pass second try!")
                        pass
        except Exception:
            logging.exception("Pass iterate through the list!")
            pass

if __name__ == "__main__":
    main()
