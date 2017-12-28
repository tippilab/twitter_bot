import csv
import os

import tweepy
import click


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
    with open('followers.txt', 'r') as file:
        list_users_url = []
        reader = csv.reader(file)
        for row in reader:
            list_users_url.append(row[0])

    list_users = []
    for user_url in list_users_url:
        if 'https://twitter.com/' in user_url:
            list_users.append(user_url.split('https://twitter.com/')[-1])
        elif 'http://twitter.com/' in user_url:
            list_users.append(user_url.split('http://twitter.com/')[-1])

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(
        auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True,
        retry_count=10, retry_delay=5,
        retry_errors=5
    )
    print(api)
    counter = 0
    with open('followers_cache.txt', 'ar+') as f:
        cached_users = []
        tmp_cache = []
        reader = csv.reader(f)
        for row in reader:
            cached_users.append(row[0])
        for user in list_users:
            if ('https://twitter.com/' + user) not in cached_users and (
                    'https://twitter.com/' + user + '\n') not in tmp_cache:
                print("Follow " + user)
                api.create_friendship(user)
                f.write('https://twitter.com/' + user + '\n')
                tmp_cache.append('https://twitter.com/' + user + '\n')
                counter += 1
                if counter >= limit:
                    return
            else:
                print("Skipped " + user + '\n')


if __name__ == "__main__":
    main()
