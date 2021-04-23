# -----------------------------------------------------------------------------------------

# Copyright (c) 2020 tdbowman-CompSci-F2020
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# -----------------------------------------------------------------------------------------

# Author: Salsabil Bakth
# The purpose of this script is to retrieve all of the unique events per each DOI 
# corresponding to the DOIs listed in doidata database.
# The script runs so that it retrieves all of the DOIs from the MySQL database and 
# looks for the corresponding events. Once the events are found, they are inserted 
# into MongoDB. 
# Incorporated a hash map to check for duplication from MySQL. Checks for eventID
# and stores them into a dictionary. The hashmap is then used to compare the eventID
# of the new events. If it does not exist in the MySQL table, then it is inserted into
# MongoDB to be filtered and finally ingested into MySQL.

# -----------------------------------------------------------------------------------------

import mysql.connector
import os
import platform
import csv
import requests
import pymongo
import json
import time
from ingestMongoEvents import ingestMongoEvents

# -----------------------------------------------------------------------------------------

# current directory 
path = os.getcwd() 
  
# parent directory 
parent = os.path.dirname(path) 
config_path = os.path.join(path, "config", "openAltConfig.json")

# config file
f = open(config_path)
APP_CONFIG = json.load(f)

# -----------------------------------------------------------------------------------------

def databaseConnection():
    try:
        # connect to doidata database
        mysql_username = APP_CONFIG['Crossref-Event-Database']['username']
        mysql_password = APP_CONFIG['Crossref-Event-Database']['password']
        crossRefEventDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "crossrefeventdatamain")
        return crossRefEventDatabase

    except:
        print("Error: Cannot connect to MySQL database.")
        return

# -----------------------------------------------------------------------------------------

def mongoDBConnection():
    try:
        # use config file for connection url and database name
        connection = APP_CONFIG['MongoDB-Event-Database']['address']
        databaseName = APP_CONFIG['MongoDB-Event-Database']['name']

        # setup localization
        myclient = pymongo.MongoClient(connection)

        # reference MongoDB database
        eventDatabase = myclient[databaseName]

        return eventDatabase

    except:
        print("Error: Cannot connect to MongoDB.")
        return

# -----------------------------------------------------------------------------------------

def storeHashMap(eventIDs):
    # create dictionary to hold unique eventIDs
    listEventIDs= {}
                
    if (eventIDs != []):
        # store eventID as a key in listEventID dictionary 
        for uniqueEventID in eventIDs:
            listEventIDs[uniqueEventID[0]] = None

    return listEventIDs

# -----------------------------------------------------------------------------------------

def fetch_events():

    # Database connection to retrieve all of the DOIs
    crossRefEventDatabaseConnection = databaseConnection()
    crossRefEventDatabaseCursor = crossRefEventDatabaseConnection.cursor()
    crossRefEventDatabaseCursor.execute("Select DOI FROM doidata._main_ WHERE DOI IS NOT NULL")

    # store DOIs 
    articles = crossRefEventDatabaseCursor.fetchall()

    # Open the log file
    f = open("eventLogFile.txt", "a")
    count = 0
    startTime = time.time()

    # -----------------------------------------------------------------------------------------
    
    # loops for each DOI (for all articles use len(articles))
    for i in range(len(articles)):

        # -----------------------------------------------------------------------------------------

        # counter of DOI from the total
        count = count + 1
        print("\nCount DOIs: " + str(count) + "/" + str(len(articles)))
        
        # For the first 10 DOIs, record the time it took
        if count == 10:
            executionTime = (time.time() - startTime)
            f.write('Number of DOIs: ' + str(count) + '      Time: ' + str(executionTime) + '\n')

        # For the every 100 DOIs, record the time it took
        if count % 100 == 0:
            executionTime = (time.time() - startTime)
            f.write('Number of DOIs: ' + str(count) + '      Time: ' + str(executionTime) + '\n')

        # -----------------------------------------------------------------------------------------
        
        # Connect to MongoDB and drop all existing collections 
        eventDatabaseMongoDB = mongoDBConnection()
        
        for coll in eventDatabaseMongoDB.list_collection_names():
            print("\nExisting Collection: ", coll)
            eventDatabaseMongoDB.drop_collection(coll)

        # -----------------------------------------------------------------------------------------
            
        # access the DOI from the list
        article = articles[i]
        articleDOI = article[0]
        print(articleDOI)

        # Crossref Event API connection
        crossrefURL = APP_CONFIG['Crossref-Event-API']['url']

        # -----------------------------------------------------------------------------------------

        try:
            # fetching event data for this particular DOI
            response = requests.get(crossrefURL + articleDOI)
            
            # Retrieve the dict with events
            data = response.json()

            # Check to see if the data is null
            if (data != []):

                # Retrieve the events on the current page and retrieve the cursor for the next page of events
                cursor = data.get("message").get("next-cursor")
                events = data.get("message").get("events")

                # Transfer the events to be sorted through
                transfer_buffer(events, articleDOI, crossRefEventDatabaseCursor, crossRefEventDatabaseConnection)

                # Iterate through the cursor until none
                while (cursor != None):

                    # use the cursor to make a new API call for more data 
                    extendResponse = requests.get(crossrefURL + articleDOI + "&cursor=" + cursor)

                    # Retrieve the dict with events
                    extendData = extendResponse.json()

                    # Retrieve the events
                    extendEvents = extendData.get("message").get("events")
                    
                    # check to see if events are not null, then sort through the events
                    if (extendEvents != []):
                        transfer_buffer(extendEvents, articleDOI, crossRefEventDatabaseCursor, crossRefEventDatabaseConnection)

                    # get the next cursor
                    cursor = extendData.get("message").get("next-cursor")

                    # if curose is none, end iteration
                    if cursor == None:
                        break

            # Ingest from MongoDB to MySQL
            print("\nIngest to MySQL:")
            ingestMongoEvents()

        # -----------------------------------------------------------------------------------------

        except:
            print("Event information is not available.")
            pass

        # -----------------------------------------------------------------------------------------

    # Close the log file
    f.close()
    
# -----------------------------------------------------------------------------------------

def transfer_buffer(events, articleDOI, crossRefEventDatabaseCursor, crossRefEventDatabaseConnection):

    # -----------------------------------------------------------------------------------------
    
    # create the objectID using the articleDOI
    objectID = "https://doi.org/" + articleDOI

    # Connect to the MongoDB database
    connection = APP_CONFIG['MongoDB-Event-Database']['address']
    databaseName = APP_CONFIG['MongoDB-Event-Database']['name']

    # setup localization
    myclient = pymongo.MongoClient(connection)

    # reference MongoDB database
    eventDatabase = myclient[databaseName]

    # -----------------------------------------------------------------------------------------

    # Iterate through the events    
    for info in events: 

        # Iterate through the values of each event
        for key, value in list(info.items()):
            
            # -----------------------------------------------------------------------------------------

            # Store the unique event ID as a value
            if (key=="id"):
                mongoEventID = value
                print("\nMongoEventID:", mongoEventID)

            # -----------------------------------------------------------------------------------------

            if (key == "source_id" and value == "cambia-lens"):
                print("Cambia-Lens")
                # Find all of the eventIDs for the DOI
                crossRefEventDatabaseCursor.execute("Select eventID FROM cambiaevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()

                # retrieve the hashmap
                listEventIDs = storeHashMap(eventIDs)

                try:
                    # check if the event does not exist in the hashmap, then insert into the collection
                    if mongoEventID not in listEventIDs:
                        print("Cambia-Lens Ingest!")
                        cambia = eventDatabase["Cambia-Lens"]
                        cambia.insert_one(info)
                    else:
                        print("Duplicate event!")

                except:
                    print("Event ID (" + mongoEventID + ") fetch failed.")

            # -----------------------------------------------------------------------------------------

            elif (key == "source_id" and value == "crossref"):
                print("Crossref")
                # Find all of the eventIDs for the DOI
                crossRefEventDatabaseCursor.execute("Select eventID FROM crossrefevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()

                 # retrieve the hashmap
                listEventIDs = storeHashMap(eventIDs)

                try:
                    # check if the event does not exist in the hashmap, then insert into the collection
                    if mongoEventID not in listEventIDs:
                        print("Crossref Ingest!")
                        crossref = eventDatabase["Crossref"]
                        crossref.insert_one(info)
                    else:
                        print("Duplicate event!")

                except:
                    print("Event ID (" + mongoEventID + ") fetch failed.")

            # -----------------------------------------------------------------------------------------

            elif (key == "source_id" and value == "datacite"):
                print("Datacite")
                # Find all of the eventIDs for the DOI
                crossRefEventDatabaseCursor.execute("Select eventID FROM dataciteevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()

                # retrieve the hashmap
                listEventIDs = storeHashMap(eventIDs)

                try:
                    # check if the event does not exist in the hashmap, then insert into the collection
                    if mongoEventID not in listEventIDs:
                        print("Datacite Ingest!")
                        datacite = eventDatabase["Datacite"]
                        datacite.insert_one(info)
                    else:
                        print("Duplicate event!")

                except:
                    print("Event ID (" + mongoEventID + ") fetch failed.")

            # -----------------------------------------------------------------------------------------

            elif (key == "source_id" and value == "f1000"):
                print("F1000")
                # Find all of the eventIDs for the DOI
                crossRefEventDatabaseCursor.execute("Select eventID FROM f1000event WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()

                # retrieve the hashmap
                listEventIDs = storeHashMap(eventIDs)

                try:
                    # check if the event does not exist in the hashmap, then insert into the collection
                    if mongoEventID not in listEventIDs:
                        print("F1000 Ingest!")
                        f1000 = eventDatabase["F1000"]
                        f1000.insert_one(info)
                    else:
                        print("Duplicate event!")

                except:
                    print("Event ID (" + mongoEventID + ") fetch failed.")

            # -----------------------------------------------------------------------------------------
            
            elif (key == "source_id" and value == "hypothesis"):
                print("Hypothesis")
                # Find all of the eventIDs for the DOI
                crossRefEventDatabaseCursor.execute("Select eventID FROM hypothesisevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()

                # retrieve the hashmap
                listEventIDs = storeHashMap(eventIDs)

                try:
                    # check if the event does not exist in the hashmap, then insert into the collection
                    if mongoEventID not in listEventIDs:
                        print("Hypothesis Ingest!")
                        hypothesis = eventDatabase["Hypothesis"]
                        hypothesis.insert_one(info)
                    else:
                        print("Duplicate event!")

                except:
                    print("Event ID (" + mongoEventID + ") fetch failed.")

            # -----------------------------------------------------------------------------------------

            elif (key == "source_id" and value == "newsfeed"):
                print("Newsfeed")
                # Find all of the eventIDs for the DOI
                crossRefEventDatabaseCursor.execute("Select eventID FROM newsfeedevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()

                # retrieve the hashmap
                listEventIDs = storeHashMap(eventIDs)

                try:
                    # check if the event does not exist in the hashmap, then insert into the collection
                    if mongoEventID not in listEventIDs:
                        print("Newsfeed Ingest!")
                        newsfeed = eventDatabase["Newsfeed"]
                        newsfeed.insert_one(info)
                    else:
                        print("Duplicate event!")

                except:
                    print("Event ID (" + mongoEventID + ") fetch failed.")

            # -----------------------------------------------------------------------------------------

            elif (key == "source_id" and value == "reddit"):
                print("Reddit")
                # Find all of the eventIDs for the DOI
                crossRefEventDatabaseCursor.execute("Select eventID FROM redditevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()

                # retrieve the hashmap
                listEventIDs = storeHashMap(eventIDs)

                try:
                    # check if the event does not exist in the hashmap, then insert into the collection
                    if mongoEventID not in listEventIDs:
                        print("Reddit Ingest!")
                        reddit = eventDatabase["Reddit"]
                        reddit.insert_one(info)
                    else:
                        print("Duplicate event!")

                except:
                    print("Event ID (" + mongoEventID + ") fetch failed.")

            # -----------------------------------------------------------------------------------------

            elif (key == "source_id" and value == "reddit-links"):
                print("Reddit-Links")
                # Find all of the eventIDs for the DOI
                crossRefEventDatabaseCursor.execute("Select eventID FROM redditlinksevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()

                # retrieve the hashmap
                listEventIDs = storeHashMap(eventIDs)

                try:
                    # check if the event does not exist in the hashmap, then insert into the collection
                    if mongoEventID not in listEventIDs:
                        print("Reddit-Links Ingest!")
                        redditlinks = eventDatabase["Reddit-Links"]
                        redditlinks.insert_one(info)
                    else:
                        print("Duplicate event!")

                except:
                    print("Event ID (" + mongoEventID + ") fetch failed.")

            # -----------------------------------------------------------------------------------------

            elif (key == "source_id" and value == "stackexchange"):
                print("Stack Exchange")
                # Find all of the eventIDs for the DOI
                crossRefEventDatabaseCursor.execute("Select eventID FROM stackexchangeevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()

                # retrieve the hashmap
                listEventIDs = storeHashMap(eventIDs)

                try:
                    # check if the event does not exist in the hashmap, then insert into the collection
                    if mongoEventID not in listEventIDs:
                        print("Stack Exchange Ingest!")
                        stackexchange = eventDatabase["StackExchange"]
                        stackexchange.insert_one(info)
                    else:
                        print("Duplicate event!")

                except:
                    print("Event ID (" + mongoEventID + ") fetch failed.")

            # -----------------------------------------------------------------------------------------

            elif (key == "source_id" and value == "twitter"):
                print("Twitter")
                # Find all of the eventIDs for the DOI
                crossRefEventDatabaseCursor.execute("Select eventID FROM twitterevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()

                # retrieve the hashmap
                listEventIDs = storeHashMap(eventIDs)

                try:
                    # check if the event does not exist in the hashmap, then insert into the collection
                    if mongoEventID not in listEventIDs:
                        print("Twitter Ingest!")
                        twitter = eventDatabase["Twitter"]
                        twitter.insert_one(info)
                    else:
                        print("Duplicate event!")

                except:
                    print("Event ID (" + mongoEventID + ") fetch failed.")

            # -----------------------------------------------------------------------------------------

            elif (key == "source_id" and value == "web"):
                print("Web")
                # Find all of the eventIDs for the DOI
                crossRefEventDatabaseCursor.execute("Select eventID FROM webevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()

                # retrieve the hashmap
                listEventIDs = storeHashMap(eventIDs)

                try:
                    # check if the event does not exist in the hashmap, then insert into the collection
                    if mongoEventID not in listEventIDs:
                        print("Web Ingest!")
                        web = eventDatabase["Web"]
                        web.insert_one(info)
                    else:
                        print("Duplicate event!")

                except:
                    print("Event ID (" + mongoEventID + ") fetch failed.")

            # -----------------------------------------------------------------------------------------

            elif (key == "source_id" and value == "wikipedia"):
                print("Wikipedia")
                # Find all of the eventIDs for the DOI
                crossRefEventDatabaseCursor.execute("Select eventID FROM wikipediaevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()

                # retrieve the hashmap
                listEventIDs = storeHashMap(eventIDs)

                try:
                    # check if the event does not exist in the hashmap, then insert into the collection
                    if mongoEventID not in listEventIDs:
                        print("Wikipedia Ingest!")
                        wikipedia = eventDatabase["Wikipedia"]
                        wikipedia.insert_one(info)
                    else:
                        print("Duplicate event!")

                except:
                    print("Event ID (" + mongoEventID + ") fetch failed.")

            # -----------------------------------------------------------------------------------------

            elif (key == "source_id" and value == "wordpressdotcom"):
                print("Wordpress.com")
                # Find all of the eventIDs for the DOI
                crossRefEventDatabaseCursor.execute("Select eventID FROM wordpressevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()

                # retrieve the hashmap
                listEventIDs = storeHashMap(eventIDs)

                try:
                    # check if the event does not exist in the hashmap, then insert into the collection
                    if mongoEventID not in listEventIDs:
                        print("Wordpress.com Ingest!")
                        wordpress = eventDatabase["WordPressDotCom"]
                        wordpress.insert_one(info)
                    else:
                        print("Duplicate event!")

                except:
                    print("Event ID (" + mongoEventID + ") fetch failed.")

# -----------------------------------------------------------------------------------------

if __name__ == '__main__':
    fetch_events()

# -----------------------------------------------------------------------------------------