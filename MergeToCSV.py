# Name: Mergecsv
# Purpose: To pull in csv files with the same structure into 1 file
# 
# Author: Michael O'Brien
# Created: Dec 2015
#===============================================================================

import pandas as pd
import os

def main(CombinedFileName ="Combined.csv"):
    
    #Create an list to store the list of objects/csv files
    Combinedlist =[]
    Colnames = ['Method', 'CreatedDate', 'Coordinates','userLocation','id', 'retweetCount','text']
    print(Colnames)
    # Get all the csv files in the current directory
    for fileToProcess in os.listdir(os.curdir):
        if fileToProcess.endswith(".csv"):
            print(fileToProcess)
            df=pd.read_csv(fileToProcess,sep='|')
            #df = pd.read_csv(file_,index_col=None, header=0)
            Combinedlist.append(df)
    #Concat the files vertically
    concatDf =pd.concat(Combinedlist)
    #concatDf.columns=Colnames
    concatDf.to_csv(CombinedFileName)
    print(concatDf.head(10))
   # frame = pd.concat(Combinedlist)
   
if __name__ == '__main__':
    main()
    