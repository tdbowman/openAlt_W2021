import json
import argparse
import pandas as pd
import csv 
import os
import crossref
import platform
import mysql.connector
import getpass
import authorMetaDataIngest


tempDir = "AuthorMetaData"
#csvLineCount = 0

print("MySQL Credentials")
mysql_username = input("Username: ")
mysql_password = getpass.getpass("Password: ")

connection = mysql.connector.connect(user=str(mysql_username), password=str(
        mysql_password), host='127.0.0.1', database='crossrefeventdatamain')

cursor = connection.cursor()

try: 

    filePath = os.path.abspath(__file__)
    directoryName = os.path.dirname(filePath)
    os.chdir(directoryName)

    if not os.path.isdir(tempDir):

        os.makedirs(tempDir)

    if (platform.system() == 'Linux'):

        directoryName = directoryName + "/" + tempDir 

    elif(platform.system() == 'Windows'):

        directoryName = directoryName + "\\" + tempDir 
    
    csvData = pd.read_csv("DOIValues.csv", header = None)
    csvLineCount = len(list(csvData.index))
except OSError:

    print("Cannot change directory to the location of this file")
except:

    print("Unspecified Error, Exiting")



def main():

    currentRows = 0
    #csvLineCount = 100

    with open('DOIValues.csv', newline='') as csvFile:
            lineIn = csv.reader(csvFile)

            while currentRows < csvLineCount:
            
                csvRow = next(lineIn) 
                StringConvert = ""
                csvLineString = StringConvert.join(csvRow)

                print(csvLineString)

                try:
                    from crossref.restful import Works
                    works = Works()
                    doiMetaData = works.doi(csvLineString)

                    if (doiMetaData['author']):
                        
                        #print(doiMetaData)

                        authorInfo = doiMetaData['author']
                        print("Author information for DOI found")
                        authorMetaDataIngest.authorIngest(connection, cursor, csvLineString, authorInfo)

                except ImportError:
                    print("Installation of the Crossref API is needed")
                except:
                    print("Unknown Error")

                currentRows += 1
                if currentRows > csvLineCount:
                    currentRows = csvLineCount

if __name__ == '__main__':
    main()