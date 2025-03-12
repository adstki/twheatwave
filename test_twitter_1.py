#Adrian Strasser-King INST326, August 18, 2023

from unittest.mock import patch, Mock
import unittest
from collections import defaultdict

"""Since there is no guarantee for the input to be constant, this module implements 
    mock versions of the classes and its functions used."""

class MockTwitterAPIForAPIAdmin:
    
    def get_tweets(self, hashtag, count):
        return [("tweet_1", "New York"), ("tweet_2", "California")]
    
class MockAPIAdmin:
    def __init__(self):
        self.api = MockTwitterAPIForAPIAdmin()
    
    def get_sorted_tweets(self):
        return self.api.get_tweets("#test", 2)

class MockTwitterAPI:
    def get_tweets(self, hashtag, count):
        return [("tweet_1", "New York"), ("tweet_2", "California")]
    
    def group_tweets_by_state(self, tweets_with_locations):
        state_counts = defaultdict(int)
        for tweet, location in tweets_with_locations:
            states = {"New York" : "NY", "California" : "CA"}
            state = states.get(location)
            if state : 
                state_counts[state] += 1
        return state_counts
    
class TestAPIAdminMethods(unittest.TestCase):
    def setUp(self):
        self.app = MockAPIAdmin()
    
    def test_get_sorted_tweets(self):
        result  = self.app.get_sorted_tweets()
        self.assertEqual(result, [("tweet_1", "New York"), ("tweet_2", "California")])
    
class TestTwitterAPIMethods(unittest.TestCase):
    def setUp(self):
        self.api = MockTwitterAPI()
    
    def test_get_tweets(self):
        result  = self.api.get_tweets("#test", 2)
        self.assertEqual(result, [("tweet_1", "New York"), ("tweet_2", "California")])

    def test_group_tweets_by_state(self):
        tweets_with_locations = [("tweet_1", "New York"), ("tweet_2", "California")]
        result = self.api.group_tweets_by_state(tweets_with_locations)
        self.assertEqual(result, {"NY" : 1, "CA" : 1})

if __name__ == "__main__":
    unittest.main()