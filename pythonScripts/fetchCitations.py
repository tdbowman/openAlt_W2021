"""
MIT License

Copyright (c) 2020 tdbowman-CompSci-F2020

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
# This script will fetch citation data from OpenCitations API and call ingest scripts to ingest data into MySQL
# author: Rihat Rahman
# Lines 1-105
#-------------------------------------------------------------

import mysql.connector
import requests
import json
from OpenCitationsCitationIngest import OCCitationIngest
from OpenCitationsReferenceIngest import OCReferenceIngest
import os
import json


# current directory 
path = os.getcwd() 
  
# parent directory 
parent = os.path.dirname(path) 
config_path = os.path.join(parent, "config", "openAltConfig.json")

# config file
f = open(config_path)
APP_CONFIG = json.load(f)


def getCitationData(mysql_username, mysql_password):

    try:
        # connect to doidata database
        drBowmanDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "doidata")

        # connect to citatons database
        citationDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "opencitations")

    except:
        print("Error: Invalid MySQL credentials")

    drBowmanDatabaseCursor = drBowmanDatabase.cursor()
    openCitationsCursor = citationDatabase.cursor()

    drBowmanDatabaseCursor.execute("Select DOI FROM _main_")
    articles = drBowmanDatabaseCursor.fetchall()

    emptyDOI = (None, )

    # To fetch citation data for all articles, set numberOfArticlesToFetch = articles.length
    numberOfArticlesToFetch = 500 

    for i in range(numberOfArticlesToFetch):

        if (articles[i] != emptyDOI):

            article = articles[i]
            articleDOI = article[0]

            citationResponse = requests.get('https://opencitations.net/index/croci/api/v1/citations/' + articleDOI)
            citationCountsResponse = requests.get('https://opencitations.net/index/croci/api/v1/citation-count/' + articleDOI)

            referenceResponse = requests.get('https://opencitations.net/index/croci/api/v1/references/' + articleDOI)
            referenceCountsResponse = requests.get('https://opencitations.net/index/croci/api/v1/reference-count/' + articleDOI)

            citationsJSON = citationResponse.json()
            countJSON = citationCountsResponse.json()
            referenceJSON = referenceResponse.json()
            referenceCountsJson = referenceCountsResponse.json()

            if response.json() != []:

                # Passing data to citation ingest script
                OCCitationIngest(citationDatabase, openCitationsCursor, articleDOI, citationsJSON, countJSON)

                # passing data to reference ingest script
                OCReferenceIngest(citationDatabase, openCitationsCursor, articleDOI, referenceJSON, referenceCountsJson)
                

if __name__ == '__main__':

    print("MySQL Credentials")
    mysql_username = input("Username: ")
    mysql_password = input("Password: ")
    getCitationData(mysql_username, mysql_password)
#-------------------------------------------------------------