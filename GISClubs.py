'''
Created on 7 Dec 2015

@author: michael.obrien
'''
#Pull the details for senior clubs & junior rugby clubs in Munsters
#http://www.munsterrugby.ie/domestic/clubs/juniorcontacts.php
#http://www.munsterrugby.ie/domestic/clubs/seniorcontacts.php 
#table class="clubindex" gets the table of urls for the senior clubs and <div class="clubinfo clubinfo_ea"> gets the general section
#<div class="row address"> gets the address area with class=field getting the address value 
#<div class="field"> inside div class="row displayname gets the club name

# Import the beautiful soup library
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
# import requests library to actually go get the webpage for Beautiful Soup (previously used urllib2 but requests seems better able to handle urls with spaces
import requests
import sys
import unicodecsv as csv

#Use Google to get long lats 
from geopy.geocoders import GoogleV3

def getClubDetails(ClubName,ClubURL):
    #Define the Dictionary
    Club={}
    
    #define the geolocator tool with Irish maps
    GeoTool = GoogleV3(domain='maps.google.ie')
    #Define the soup strainer to get just the club details
    ClubContentStrainer= SoupStrainer("div",class_="clubinfo clubinfo_ea")
    AddressStrainer = SoupStrainer("div",class_="row address")
    
    #Load the Dictionary with what we know already
    Club['Name'] = ClubName
    Club['Link'] = ClubURL
    if 'senior' in ClubURL:
        Club['ClubType'] ="Senior"
    else:
        Club['ClubType'] ="Junior"
    
    with requests.Session() as clubsession:
        ClubDetails = clubsession.get(ClubURL,timeout=10)
        ClubContent = BeautifulSoup(ClubDetails.text, "html.parser",parse_only=ClubContentStrainer)
        #print ClubContent.prettify(formatter="html")
        #Use the strainer to get to the containing dive with class row address then find a div tag with a css class of field before stripping the html and separating the lines with a comma
        Club['Address'] = ClubContent.find(AddressStrainer).find("div", class_="field").get_text(",")
        FindClub = str(ClubName +","+Club['Address'])
        Location = GeoTool.geocode(FindClub,exactly_one=True, timeout=5)
        if Location is not None:
            Club['GeoAddress'] = Location.address
            Club['longitude'] = Location.longitude
            Club['latitude'] = Location.latitude
        else:
            Club['GeoAddress'] = "None Found"
            Club['longitude'] = "None Found"
            Club['latitude'] = "None Found"
        #print("----",Club)
        
    return Club

def main(OutputFileName ='GISClubs.csv', FileDelimiter=";"):
    
    #Define the soup strainers to reduce the soup processing required to find content
    TableListStrainer = SoupStrainer("table",class_="clubindex")
    #Declare the variables
    Weblinks =['http://www.munsterrugby.ie/domestic/clubs/seniorcontacts.php','http://www.munsterrugby.ie/domestic/clubs/juniorcontacts.php']   
    BaseURL = 'http://www.munsterrugby.ie' 
    
    ReturnedClubDictionary ={}
    MyCSVFile = open(OutputFileName, "wb") 
    #ClubList = csv.writer(MyCSVFile, delimiter=FileDelimiter)
    #Write the header row
    
    fieldnames = ['Name','Link','ClubType','Address','GeoAddress','longitude','latitude']
    writer = csv.DictWriter(MyCSVFile, fieldnames=fieldnames,delimiter=FileDelimiter)
    writer.writeheader()
   
    for Weblink in Weblinks:
        with requests.Session() as s:
                PageContent = s.get(Weblink,timeout=10)
                TableContent = BeautifulSoup(PageContent.text, "html.parser",parse_only=TableListStrainer)
                #print TableContent.prettify(formatter="html")
                Cells = TableContent.find_all("td")
                for cell in Cells:
                    if cell.get_text() != "":
                        ClubLink = BaseURL + str(cell.find('a').get('href'))
                        ClubName = cell.get_text()
                        print(ClubName,"--" ,ClubLink)
                        ReturnedClubDictionary = getClubDetails(str(ClubName), str(ClubLink))
                        #Write the row and flush the change to disk
                        #ClubList.writerow([Club['Name'],Club['Link'],Club['ClubType'],Club['Address'],Club['GeoAddress'],Club['longitude'],Club['latitude']])
                        writer.writerow(ReturnedClubDictionary)
                        MyCSVFile.flush()
                                  
    # Exit successfully
    MyCSVFile.close()
    sys.exit(0)

if __name__ == '__main__':
    main()