# Author: Rihat Rahman
# Lines: 1 - 110
# This scripts fetches events for papers from doidata database and stores event information 
# in JSON files. It also creates a CSV filecontaining information about which JSON file belongs to what DOI.
# After running this script, change dataDirectory of IngestJSONMain.py to eventData folder and run that script 
# to ingest data into crossrefevent database

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

import mysql.connector
import os
import platform
import csv


def fetch_events():

    print("MySQL Credentials")
    mysql_username = input("Username: ")
    mysql_password = input("Password: ")


    try:
        # connect to doidata database
        drBowmanDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "doidata")


    except:
        print("Error: Invalid MySQL credentials")
        return

    print ("Connected to the database...")

    drBowmanDatabaseCursor = drBowmanDatabase.cursor()

    drBowmanDatabaseCursor.execute("Select DOI FROM _main_")
    articles = drBowmanDatabaseCursor.fetchall()

    # To fetch event data for all articles, set numberOfArticlesToFetch = articles.length
    numberOfArticlesToFetch = 500 

    # create directory to store temporary JSON files
    eventDataDirectory = 'eventData'

    emptyDOI = (None, )


    # path for different operating systems
    if platform.system() == "Windows":
        directory = "eventData\\events_"

    elif platform.system() == "Darwin" | "Linux":
        "eventData/events_"

    if not os.path.exists("eventData"):
        os.makedirs(eventDataDirectory)


    with open("json_info.csv", "w", newline="") as jsonInfoFile:
        writer = csv.writer(jsonInfoFile)
        writer.writerow(["File Name", "DOI"])

        fileCounter = 1


        for i in range(numberOfArticlesToFetch):

            if (articles[i] != emptyDOI):

                article = articles[i]
                articleDOI = article[0]

                print(articleDOI)

                fileName = directory + str(fileCounter) + ".json"
                fileCounter += 1
                print(fileName)

                # fetching event data for this particular DOI
                query = "curl " + "\"" + "https://api.eventdata.crossref.org/v1/events?mailto=YOUR_EMAIL_HERE&obj-id=" + articleDOI + "\"" + " > " + fileName
                os.system(query)

                writer.writerow([fileName[10:], articleDOI])



if __name__ == '__main__':
    fetch_events()