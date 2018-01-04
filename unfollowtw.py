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
@click.option('--limit', default=1000,
              help='set limit amount of users you want to follow')
def main(consumer_key, consumer_secret, access_token,
         access_token_secret, limit):
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

    f = open('friends_cache_{}.txt'.format(currrent_user), 'a')

    for fr in range(limit):
        if len(api.followers_ids(list_friends[fr])) < 200:
            api.destroy_friendship(list_friends[fr])
            print("Unfollow " + list_friends[fr])
            f.write(list_friends[fr] + ' \n')
        else:
            print("Add " + list_friends[fr] + " to file")
            f.write(list_friends[fr] + ' \n')

    f.close()


if __name__ == "__main__":
    main()
