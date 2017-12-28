# How to run a script

## Create your *Keys and Access Tokens*

Go to [Twitter Application Management](https://apps.twitter.com/) and click **"Create New App"**.  
Fill in the required fields on the website [https://apps.twitter.com/app/new](https://apps.twitter.com/app/new)  and click **"Yes, I have read and agree to the Twitter Developer Agreement."** then **"Create your Twitter application"**.  
Click **"Keys and Access Tokens"** and you look your *Consumer Key (API Key)* and *Consumer Secret (API Secret)*.  
Click **"create my access token"** and you give your *Access Token* and *Access Token Secret*.

## Run script using docker

```
docker build -t test/test .
docker run -e CONSUMER_KEY='your_consumer_key' -e CONSUMER_SECRET='your_consumer_secret' -e ACCESS_TOKEN='your_access_token' -e ACCESS_TOKEN_SECRET='your_access_token_secret' test/test
```
