# How to run a script

## Create your *Keys and Access Tokens*

Go to [Twitter Application Management](https://apps.twitter.com/) and click **"Create New App"**.  
Fill in the required fields on the website [https://apps.twitter.com/app/new](https://apps.twitter.com/app/new)  and click **"Yes, I have read and agree to the Twitter Developer Agreement."** then **"Create your Twitter application"**.  
Click **"Keys and Access Tokens"** and you look your *Consumer Key (API Key)* and *Consumer Secret (API Secret)*.  
Click **"create my access token"** and you give your *Access Token* and *Access Token Secret*.

## Install Environment variables 
```
$ export CONSUMER_KEY='your consumer key'
$ export CONSUMER_SECRET='your consumer secret'
$ export ACCESS_TOKEN='your access token'
$ export ACCESS_TOKEN_SECRET='your access token secret'
```

## Creation of virtual environment

Creation of virtual environment is done by executing the command venv:

`python3 -m venv /path/to/new/virtual/environment`

### Activate virtual environment

If you use Posix Platform:

`$ source <venv>/bin/activate`

### Install the required packages

`$ pip install -r requirements.txt`

## Run script using docker

```
docker build -t test/test .
docker run -it -e CONSUMER_KEY='your_consumer_key' -e CONSUMER_SECRET='your_consumer_secret' -e ACCESS_TOKEN='your_access_token' -e ACCESS_TOKEN_SECRET='your_access_token_secret' test/test
```
