#Load the cleaned tweets from the bar delimited csv file then
#Get the long, lat from google and get the sentiment from the other api
import sys
import unicodecsv as csv
import StringIO
import codecs
#Use Google to get long lats 
from geopy.geocoders import GoogleV3
#Use unirest for integrating with mashape.com where the sentiment API is hosted and managed 
import unirest


#Code from https://dzone.com/articles/python-27-csv-files-unicode
#To decode the column from the csv 1 by 1 
# class UnicodeDictReader( object ):
#     def __init__( self, *args, **kw ):
#         self.encoding= kw.pop('encoding', 'mac_roman')
#         self.reader= csv.DictReader( *args, **kw )
#     def __iter__( self ):
#         decode= codecs.getdecoder( self.encoding )
#         for row in self.reader:
#             t= dict( (k,decode(row[k])[0]) for k in row )
#             yield t

def getSentiment(TextToSentiment,Delay=5):
# These code snippets use an open-source library. http://unirest.io/python and was produced by Mashape.com
    response = unirest.post("https://community-sentiment.p.mashape.com/text/",
        headers={
                 "X-Mashape-Key": "",
                 "Content-Type": "application/x-www-form-urlencoded",
                 "Accept": "application/json"
    },
        params={
                "txt": TextToSentiment
                }
    )
    return response 

def main(inputFileName='TweetTextUTF8.csv',OutputFileName ='TweetSentiment.csv', FileDelimiter=",", APIDelay=5):
 
    CSVInput = codecs.open(inputFileName,"rb",errors='ignore',encoding='utf-8')#,encoding='cp1252', 
    MyCSVOutputFile = open(OutputFileName, "wb") 
    #Define the header row
    inputfieldnames = ["id","CleanedTex"]
    fieldnames = ["id","CleanedText","Sentiment","SentimentNumeric"]
    #Open the csv source file using the code referenced from internet to handle unicode characters in csv
    tempdata = CSVInput.read()
    CSVInput.close()
    FileString = StringIO.StringIO(tempdata)
    reader = csv.DictReader(FileString,fieldnames=inputfieldnames,delimiter=FileDelimiter)
    writer = csv.DictWriter(MyCSVOutputFile, fieldnames=fieldnames,delimiter=FileDelimiter)
    #rowdictionary.f
    writer.writeheader()
    #Loop through the csv 
    for row in reader:
        #MyText = row["CleanedText"].encode('ascii', 'xmlcharrefreplace')
        print row
        #print (row["SearchString"],row["CreatedDate"],row["Coordinates"],row["Coord 1"],row["Coord 2"],row["CleanedLocation"],row["id"],row["retweetCount"],MyText)
    
    
    
    
    # Exit successfully
    MyCSVOutputFile.close()
    CSVInput.close()
    sys.exit(0)
  
#         if (filerow['SearchString'].contains('SearchString')):
#             #Indicates header row so skip
#             filerow.next()
#         else:
#             #Get the sentiment of the text
#             print(filerow)
#             myText = (filerow["text"])
#             SentimentResponse = getSentiment(myText,APIDelay)
#             print("The sentiment of ",myText," is ", SentimentResponse.sentiment," with a confidence of ",SentimentResponse.confidence)
#             print("----------------")
            
#         with requests.Session() as s:
#                 PageContent = s.get(Weblink,timeout=10)
#                 TableContent = BeautifulSoup(PageContent.text, "html.parser",parse_only=TableListStrainer)
#                 #print TableContent.prettify(formatter="html")
#                 Cells = TableContent.find_all("td")
#                 for cell in Cells:
#                     if cell.get_text() != "":
#                         ClubLink = BaseURL + str(cell.find('a').get('href'))
#                         ClubName = cell.get_text()
#                         print(ClubName,"--" ,ClubLink)
#                         ReturnedClubDictionary = getClubDetails(str(ClubName), str(ClubLink))
#                         #Write the row and flush the change to disk
#                         #ClubList.writerow([Club['Name'],Club['Link'],Club['ClubType'],Club['Address'],Club['GeoAddress'],Club['longitude'],Club['latitude']])
#                         writer.writerow(ReturnedClubDictionary)
#                         MyCSVFile.flush()
                                  


if __name__ == '__main__':
    main()