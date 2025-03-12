#Adrian Strasser-King INST326, August 18, 2023

from TwitterAPI import TwitterApi
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob


class APIAdmin:

    "Interacts with the user input to output specific graphics and stats. "
    def __init__(self):
        self.api = TwitterApi()
       
       
    def run(self, confirm_exit = True):
    
        if confirm_exit == True:

            menu = """Welcome to Twitter API
            1 Display Tweets with Location and Date
            2 Plot Tweets by Location 
            3 Display Overall Sentiment
            4 Exit
            Choose an option to proceed:"""

            choice = None
             
            while choice != 4:
                choice = int(input(menu))
                if choice == 1:
                    self.display_tweet_information()
                elif choice == 2:
                    self.plot_tweets_by_location()
                elif choice == 3:
                    self.plot_sentiment()

                else:
                    print("\n""Please enter a valid option or a valid count.")

    def get_sorted_tweets(self, hashtag, count):
        sorted_tweets = self.api.get_tweets(hashtag = hashtag, count = count)
        return sorted_tweets


    def display_tweet_information(self):
        
        query = input('Ask for a specific hashtag: ')
        number = int(input('How many tweets do you want to get? '))
        sorted_tweets = self.get_sorted_tweets(query, number)
        
        i = 0
        for tweet, location, time in sorted_tweets: 
            print("\n" f"--Tweet {i + 1}: " + tweet)
            print("\n" f"Location {i + 1}: " + location)
            print(f"Time of Post: " + time + "\n")
            i += 1
            
        if i < number/2:
            print("SUMMARY:""\n" f"Out of the {number} tweets requested, less than half ({i} tweets) were able to match the query and be pulled. Maybe try a different keyword?")
        else:
            print("SUMMARY:" "\n" f"Out of the {number} tweets requested, {i} tweets were able to match the query and be pulled.")
        
        back = input('Enter \"yes\" to go back to menu.')       
        if back != 'yes':
            raise ValueError(f'Invalid input. Entered {back} not \"yes\" ')
        else:
            self.run(confirm_exit = False)
            
    def plot_tweets_by_location(self):
        location_counts = defaultdict(int)
        query = input('Ask for a specific hashtag: ')
        number = int(input('How many tweets do you want to get? '))
        sorted_tweets = self.get_sorted_tweets(query, number)
          
        for _, location, _ in sorted_tweets: 
            if location != 'Unknown':
                location_counts[location] += 1
        
        locations = list(location_counts.keys())
        counts = list(location_counts.values())
        plt.figure(figsize=(8,6))
        plt.rc('axes', unicode_minus=False)
        plt.barh(locations, counts, color = 'skyblue')
        plt.xlabel('Number of Tweets')
        plt.ylabel('Location')
        plt.title('Tweets by Location')
        plt.gca().invert_yaxis()
        plt.show()

        back = input('Enter \"yes\" to go back to menu.')       
        if back != 'yes':
            raise ValueError(f'Invalid input. Entered {back} not \"yes\" ')
        else:
            self.run(confirm_exit = False)
            

    def plot_sentiment(self):
        query = input('Ask for a specific hashtag: ')
        number = int(input('How many tweets do you want to get? '))
        sorted_tweets = self.get_sorted_tweets(query, number)
        sentiment_objects = [TextBlob(tweet) for tweet, _, _ in sorted_tweets]
        sentiment_objects[0].polarity, sentiment_objects[0]

        sentiment_values = [[tweet.sentiment.polarity, str(tweet)] for tweet in sentiment_objects]
        sentiment_values[0]

        sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "tweet"])
        sentiment_df.head()
        
        sentiment_df = sentiment_df[sentiment_df.polarity != 0]
        fig, ax = plt.subplots(figsize=(8, 6))
        sentiment_df.hist(bins=[-1, -0.75, -0.5, -0.25, 0.25, 0.5, 0.75, 1],
        ax=ax,
        color="skyblue")

        plt.title(f"Sentiments for Tweets on {query}")
        plt.rc('axes', unicode_minus=False)
        plt.xlabel('Polarity Value')
        plt.ylabel('Amount of Tweets')
        plt.show()

        back = input('Enter \"yes\" to go back to menu.')       
        if back != 'yes':
            raise ValueError(f'Invalid input. Entered {back} not \"yes\" ')
        else:
            self.run(confirm_exit = False)
            
           

        
       
