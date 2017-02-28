# GIS
Contains Python Code used in GIS Project which
- [Scraps the websites to get lists of rugby clubs in Munster] (https://github.com/mobcdi/gis/blob/master/GISClubs.py) using BeautifulSoup and exports the contents to csv (;) delimited. It also attempts to get the __long__, __lat__ coordinates for the address from Google using `geopy.geocoders`
- [Creates a json file of tweets from a number of accounts](https://github.com/mobcdi/gis/blob/master/GetTweetsFromAccounts.py) using tweepy. Also creates a csv file with just `['MinedAccount', 'CreatedDate', 'Coordinates','userLocation','id', 'retweetCount','text']`
- [Creates a json and csv file of tweets using twitter search](https://github.com/mobcdi/gis/blob/master/TweetsFromSearch.py) also using tweepy. Search strings are hard coded

> Also used [MMQGIS plugin for QGIS ](http://blog.mangomap.com/post/74368997570/how-to-make-a-web-map-from-a-list-of-addresses-in) to convert addresses to __long__, __lat__ using csv data compiled above
