# Name: GetTweetsFrom Accounts
# Purpose: To pull in tweets from files in json format with \n into dataframe
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

#Getting files in folder
#http://stackoverflow.com/questions/11968976/list-files-in-only-the-current-directory 
import pandas
import jsonpickle
import os

# or consider saving the data directly to a dataframe and pickling the dataframe to disk



def main():
#     filecontents =open("skysportsrugby.txt",'r')
#     tweets = []
#     for line in filecontents:
#         line = line[:-1]  # Drop '\n' char
#         decoded = jsonpickle.decode(line)
#         tweets.append(decoded)
#     print tweets 
#     frame =pandas.DataFrame(tweets)
#     print frame 
      
    tester = pandas.DataFrame    
    #decoded =jsonpickle.decode(filecontents.read())
    #print decoded
    #tester = pandas.read_json(decoded)
    # Get all the files in the current directory that end in .txt
    for fileToProcess in os.listdir(os.curdir):
        if fileToProcess.endswith(".json"):
            print(fileToProcess)
            tester= pandas.read_json(fileToProcess)
    print(tester.head(10))

if __name__ == '__main__':
    main()
    

