# Name: GetTweetsFrom Accounts
# Purpose: To pull in tweets from accounts up to a max number and only as far back as the set date
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


import tweepy
import json 
import codecs
import unicodecsv as csv
import os
import sys
import datetime as dt


def main():
    
    #Twitter API Values
    MyConsumerKey = ''
    MyConsumerSecret = ''
    #MyAccessToken = ''
    #MyAccessTokenSecret = ''
    
    Accounts=['MRSC16','ChampionsCup','leicestertigers','munsterrugby','skysportsrugby','btsportrugby','rugbytonight','rugby_ie','threeredkings']
    EarliestTweet = dt.datetime(2015,11,1,0,0)
    currenttime = dt.datetime.now()
    csvfilename = "CombinedAccountsResults-"+currenttime.strftime("%H_%M_%S_%b_%d_%Y")+".csv"    
    MyCSVFile = open(csvfilename, "wb")    
    csvTweets = csv.writer(MyCSVFile, delimiter='|')
    csvTweets.writerow(['MinedAccount', 'CreatedDate', 'Coordinates','userLocation','id', 'retweetCount','text'])

    
    #Authenticate to the Twitter API using application authentication for higher usage rates
    auth = tweepy.AppAuthHandler(MyConsumerKey,MyConsumerSecret)
    # Enable waiting on rate limit and notification to auto wait if it exceeds the twitter api usage rate
    print("Attempting to authenticate")
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    if (not api):
        print ("Can't Authenticate")
        sys.exit(-1)

    print("Attempting to get tweets from",Accounts)
    for account in Accounts:
        filename = account +".json"
       
        #If the file doesn't already exist 
        if (not os.path.isfile(filename)):
            #Get me at most 1000 tweets from each account
            jsonfile = codecs.open(filename,'w','utf8')          
            print("Getting tweets for ",account," now")
            for tweets in tweepy.Cursor(api.user_timeline, id=account).items(1000):
                # build up the datasets for each account enhancing the missing locations
                # depending on where the supports club are home or away
                if tweets.created_at >= EarliestTweet:
                    print("Coordinates ", tweets.coordinates,"Tweeted: ",tweets.created_at.strftime("%H:%M:%S %B %d, %Y"), " Text: ", tweets.text)
                    csvTweets.writerow([account,tweets.created_at.strftime("%H:%M:%S %B %d, %Y"),tweets.coordinates,tweets.user.location,tweets.id,tweets.retweet_count,tweets.text])
                    MyCSVFile.flush()
                    print(EarliestTweet)
                    #Write it in a human readable way
                    json.dump(tweets._json,jsonfile, sort_keys = True, skipkeys = True, indent = 2,ensure_ascii=False)
                else:
                    jsonfile.close
                    
                    #kick off the next iteration of the loop
                    continue
        else:
            print("JSON File already exists for account",account)
    MyCSVFile.close()
    print("Finished getting the tweets for the listed accounts ")

if __name__ == '__main__':
    main()
    
