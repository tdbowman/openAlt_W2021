# Author: Salsabil Bakth
# The purpose of this script is to retrieve all of the unique events per each DOI 
# corresponding to the DOIs listed in doidata database.
# The script runs so that it retrieves all of the DOIs from the MySQL database and 
# looks for the corresponding events. Once the events are found, they are inserted 
# into MongoDB. 

import mysql.connector
import os
import platform
import csv
import requests
import pymongo
import json


def fetch_events():

    drBowmanDatabase = databaseConnection()
    drBowmanDatabaseCursor = drBowmanDatabase.cursor()
    drBowmanDatabaseCursor.execute("Select DOI FROM doidata._main_ WHERE DOI IS NOT NULL")

    # store DOIs 
    articles = drBowmanDatabaseCursor.fetchall()


    # loops for each DOI (for all articles use len(articles))
    # for i in range(5):
        
    #     article = articles[i]

    #     # access the DOI from set
    #     articleDOI = article[0]

    #     print(articleDOI)

    #     print("API Call!")
        
    articleDOI = "10.1016/s0377-2217(02)00134-0"
    # fetching event data for this particular DOI
    response = requests.get("https://api.eventdata.crossref.org/v1/events?mailto=YOUR_EMAIL_HERE&obj-id=" + articleDOI)
    
    # Retrieve the dict with events
    data = response.json()
    
    if (data != []):
        events = data.get("message").get("events")

        transfer_buffer(events, articleDOI)

    

def transfer_buffer(events, articleDOI):

    objectID = "https://doi.org/" + articleDOI

    # setup localization
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    # reference MongoDB database
    eventDatabase = myclient["EventDatabase"]
        
    for info in events: 

        for key, value in list(info.items()):

            if (key=="id"):
                mongoEventID = value
                print("MongoEventID:", mongoEventID)

            if (key == "source_id" and value == "cambia-lens"):
                print("Cambia-Lens")

                drBowmanDatabase = databaseConnection()
                drBowmanDatabaseCursor = drBowmanDatabase.cursor()
                drBowmanDatabaseCursor.execute("Select eventID FROM cambiaevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = drBowmanDatabaseCursor.fetchall()

                print(eventIDs)

                listEventIDs= {}

                if (listEventIDs != []):
                    # store eventID as a key in listEventID dictionary 
                    for uniqueEventID in eventIDs:
                        listEventIDs[uniqueEventID[0]] = None

                    # for each key in the dictionary, check for duplication or else insert into MongoDB
                    for eventID in listEventIDs:
                        print(eventID)

                        # checks to see if an eventID in the database matches with an API eventID 
                        if (eventID == mongoEventID):
                            print("Duplicate!")

                        else: 
                            # reference MongoDB collection
                            cambiaLens = eventDatabase["Cambia-Lens"]

                            # insert data
                            insertCollection(cambiaLens, info)
                else:
                    print("Ingest Cambia!")
                    # reference MongoDB collection
                    cambiaLens = eventDatabase["Cambia-Lens"]

                    # insert data
                    insertCollection(cambiaLens, info)
                break
            
            elif (key == "source_id" and value == "crossref"):
                print("Crossref")

                drBowmanDatabase = databaseConnection()
                drBowmanDatabaseCursor = drBowmanDatabase.cursor()
                drBowmanDatabaseCursor.execute("Select eventID FROM crossrefevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = drBowmanDatabaseCursor.fetchall()

                print(eventIDs)

                listEventIDs= {}

                if (eventIDs != []):
                    # store eventID as a key in listEventID dictionary 
                    for uniqueEventID in eventIDs:
                        listEventIDs[uniqueEventID[0]] = None

                    # for each key in the dictionary, check for duplication or else insert into MongoDB
                    for eventID in listEventIDs:
                        print(eventID)

                        # checks to see if an eventID in the database matches with an API eventID 
                        if (eventID == mongoEventID):
                            print("Duplicate!")

                        else: 
                            print("Ingest!")
                            # reference MongoDB collection
                            crossref = eventDatabase["Crossref"]

                            # insert data
                            insertCollection(crossref, info)
                else:
                    print("Crossref Ingest!")
                    # reference MongoDB collection
                    crossref = eventDatabase["Crossref"]

                    # insert data
                    insertCollection(crossref, info)
                break

            elif (key == "source_id" and value == "datacite"):
                print("Datacite")

                drBowmanDatabase = databaseConnection()
                drBowmanDatabaseCursor = drBowmanDatabase.cursor()
                drBowmanDatabaseCursor.execute("Select eventID FROM dataciteevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = drBowmanDatabaseCursor.fetchall()

                print(eventIDs)

                listEventIDs= {}

                # store eventID as a key in listEventID dictionary 
                for uniqueEventID in eventIDs:
                    listEventIDs[uniqueEventID[0]] = None

                # for each key in the dictionary, check for duplication or else insert into MongoDB
                for eventID in listEventIDs:
                    print(eventID)

                    # checks to see if an eventID in the database matches with an API eventID 
                    if (eventID == mongoEventID):
                        print("Duplicate!")

                    else: 
                        # reference MongoDB collection
                        datacite = eventDatabase["Datacite"]

                        # insert data
                        insertCollection(datacite, info)
                break

            elif (key == "source_id" and value == "f1000"):
                print("F1000")

                # reference MongoDB collection
                f1000 = eventDatabase["F1000"]

                # insert data
                insertCollection(f1000, info)
                break

            elif (key == "source_id" and value == "hypothesis"):
                print("Hypothesis")

                # reference MongoDB collection
                hypothesis = eventDatabase["Hypothesis"]

                # insert data
                insertCollection(hypothesis, info)
                break

            elif (key == "source_id" and value == "newsfeed"):
                print("Newsfeed")

                # reference MongoDB collection
                newsfeed = eventDatabase["Newsfeed"]

                # insert data
                insertCollection(newsfeed, info)
                break

            elif (key == "source_id" and value == "reddit"):
                print("Reddit")

                # reference MongoDB collection
                reddit = eventDatabase["Reddit"]

                # insert data
                insertCollection(reddit, info)
                break

            elif (key == "source_id" and value == "reddit-links"):
                print("Reddit-links")

                # reference MongoDB collection
                redditLinks = eventDatabase["Reddit-Links"]

                # insert data
                insertCollection(redditLinks, info)
                break

            elif (key == "source_id" and value == "stackexchange"):
                print("Stack Exchange")

                # reference MongoDB collection
                stackexchange = eventDatabase["Stackexchange"]

                # insert data
                insertCollection(stackexchange, info)
                break

            elif (key == "source_id" and value == "twitter"):

                print("Twitter")

                drBowmanDatabase = databaseConnection()
                drBowmanDatabaseCursor = drBowmanDatabase.cursor()
                drBowmanDatabaseCursor.execute("Select eventID FROM twitterevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = drBowmanDatabaseCursor.fetchall()

                print(eventIDs)

                listEventIDs= {}

                # store eventID as a key in listEventID dictionary 
                for uniqueEventID in eventIDs:
                    listEventIDs[uniqueEventID[0]] = None

                # for each key in the dictionary, check for duplication or else insert into MongoDB
                for eventID in listEventIDs:
                    print(eventID)

                    # checks to see if an eventID in the database matches with an API eventID 
                    if (eventID == mongoEventID):
                        print("Duplicate!")

                    else: 
                        # reference MongoDB collection
                        twitter = eventDatabase["Twitter"]

                        # insert data
                        insertCollection(twitter, info)
                break

            elif (key == "source_id" and value == "web"):
                print("Web")

                # reference MongoDB collection
                web = eventDatabase["Web"]

                # insert data
                insertCollection(web, info)
                break

            elif (key == "source_id" and value == "wikipedia"):
                print("Wikipedia")
                
                drBowmanDatabase = databaseConnection()
                drBowmanDatabaseCursor = drBowmanDatabase.cursor()
                drBowmanDatabaseCursor.execute("Select eventID FROM wikipediaevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = drBowmanDatabaseCursor.fetchall()

                print(eventIDs)

                listEventIDs= {}

                # store eventID as a key in listEventID dictionary 
                for uniqueEventID in eventIDs:
                    listEventIDs[uniqueEventID[0]] = None

                # for each key in the dictionary, check for duplication or else insert into MongoDB
                for eventID in listEventIDs:
                    print(eventID)

                    # checks to see if an eventID in the database matches with an API eventID 
                    if (eventID == mongoEventID):
                        print("Duplicate!")

                    else: 
                        # reference MongoDB collection
                        wikipedia = eventDatabase["Wikipedia"]

                        # insert data
                        insertCollection(wikipedia, info)
                break

            elif (key == "source_id" and value == "wordpressdotcom"):
                print("Wordpress.com")

                # reference MongoDB collection
                wordpressdotcom = eventDatabase["WordPressDotCom"]

                # insert data
                insertCollection(wordpressdotcom, info)
                break


def insertCollection(collection, info):
    for documents in collection.find({}):
        for events in documents:
            if (info == events):
                break
            else:
                collection.insert_one(info) 

# def hashMap():

def databaseConnection():
    try:
        # connect to doidata database
        mysql_username = "root"
        mysql_password = "pass1234"

        drBowmanDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "crossrefeventdatamain")

        return drBowmanDatabase


    except:
        print("Error: Invalid MySQL credentials")
        return

    print ("Connected to the database...")


if __name__ == '__main__':
    fetch_events()