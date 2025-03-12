
#Adrian Strasser-King INST326, August 18, 2023

#Imports dotenvironment for bearer token and authentication for Twitter
import os 
import requests
from dotenv import load_dotenv
from collections import defaultdict
from datetime import datetime
load_dotenv()


class TwitterApi:
    """This class is used to retrieve tweets from Twitter users related to the keyword."""

    
    def __init__(self):
        self.bearer_token = os.getenv("bearer_token")
        self.endpoint = "https://api.twitter.com/2/tweets/search/recent"
        self.location_dict = {}

    def get_tweets(self, hashtag, count):

        """Method that uses Twitter Response keywords and json requests to pull 
        in tweets"""

        headers = {
            "Authorization": f"Bearer {self.bearer_token}", 
        }
        params = {
            "query": hashtag, 
            "max_results": count,
            "tweet.fields": "text",
            "tweet.fields":  "created_at",
            "user.fields":  "location",
            "expansions": "author_id",
        }
        response = requests.get(self.endpoint, headers=headers, params=params)
        #Checking for error while pulling 
        if response.status_code != 200: 
            raise Exception(f"Api request failed with the status {response.status_code}: {response.text}")

        data = response.json()
        if 'data' not in data or 'includes' not in data:
            raise Exception("Unexpected response structure from Twitter API")

        tweets = data['data']
        
        users = {user['id']:user for user in data['includes']['users']}
        tweets_locations = [(tweet['text'], users[tweet['author_id']]['location'] 
        if 'location' in users[tweet['author_id']] else 'Unknown', tweet['created_at']) for tweet in tweets]
    
        sorted_tweets = sorted(tweets_locations, key=lambda x: x[1])
        return sorted_tweets
