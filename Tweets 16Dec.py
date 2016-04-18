# Name: Tweets
# Purpose: To pull in tweets from tags and accounts and get sentiment 
# 
# Author: Michael O'Brien
# Created: Dec 2015
#===============================================================================

#Package for getting tweets https://github.com/tweepy/tweepy

#Using the Application Authentication method for more throughput from the twitter api
#http://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./ 

#Using the cursor method to iterate and using dataframes for data analysis
#http://blog.impiyush.me/2015/03/data-analysis-using-twitter-api-and.html 
#The values returned in an status object
#http://tkang.blogspot.ie/2011/01/tweepy-twitter-api-status-object.html

#Sentiment analysis via API
#https://market.mashape.com/mobcdi/applications/gis-sentiment 
#https://github.com/Mashape/unirest-python 

#Working with dates in python
#https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior

#ElasticSearch
#http://blog.tryolabs.com/2015/02/17/python-elasticsearch-first-steps/ 
#https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html


import pandas as pd
import tweepy
import jsonpickle
import os
import datetime as dt


def main():
    
    #Twitter API Values
    MyConsumerKey = 'hw9b06uUbg0TjA82YArJ3jxUb'
    MyConsumerSecret = 'lX682RJfSjRAGnYSGdeMeSqKVZkbsCwbuIhhO6mYbA09qbbw8T'
    #MyAccessToken = '710587225-TCychzmlMfCnHNjDivmgZQ63N5ygnh0Ibp9tI2eI'
    #MyAccessTokenSecret = 'TJudL6LaswNhwB2a5UZjFGCSdhYLQ4vG1L377bBV3S1Dg'
    
    SentimentText ={}
    Accounts=['MRSC16','ChampionsCup','leicestertigers','munsterrugby','skysportsrugby','btsportrugby','rugbytonight']
    EarliestTweet = dt.datetime(2015,10,1,0,0)
    
    #Authenticate to the Twitter API using application authentication for higher usage rates
    auth = tweepy.AppAuthHandler(MyConsumerKey,MyConsumerSecret)
    # Enable waiting on rate limit and notification to auto wait if it exceeds the twitter api usage rate
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    for account in Accounts:
        filename = account +".txt"
        file = open(filename,'w')
        if not os.path.isfile(filename):
            for tweets in tweepy.Cursor(api.user_timeline, id=account).items():
                # process status here
                # Maybe forget about elastic and use the dataframe and over the notebook build up the dataset enhancing the missing locations
                # depending on where the supports club are home or away
                if tweets.created_at >= EarliestTweet:
                    print("Coordinates ", tweets.coordinates,"Tweeted: ",tweets.created_at.strftime("%H:%M:%S %B %d, %Y"), " Text: ", tweets.text)
                    print(EarliestTweet)
                    file.write(jsonpickle.encode(tweets._json,unpicklable=False)+'\n')
                file.close

        


    #Get all my tweets from my timeline and print them
    #public_tweets = api.home_timeline()
    #for tweet in public_tweets:
        #print tweet.text
    
    #Search Twitter
    #q = '#RWC2015 AND #IREvFRA'
    # en and fr in an array
    #lanq =['en','fr'] 

if __name__ == '__main__':
    main()
    
