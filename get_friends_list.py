import os

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
def main(consumer_key, consumer_secret, access_token,
         access_token_secret):

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(
        auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True,
        retry_count=10, retry_delay=5,
        retry_errors=5
    )

    currrent_user = api.me().screen_name
    friends_id = api.friends_ids(currrent_user)

    with open('friends_{}.txt'.format(currrent_user), 'w') as f:
        for f_id in friends_id:
            name = api.get_user(f_id).screen_name
            print("Write " + name)
            f.write(name + ' \n')


if __name__ == "__main__":
    main()
