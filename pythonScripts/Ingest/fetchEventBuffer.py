# Author: Salsabil Bakth
# The purpose of this script is to retrieve all of the unique events per each DOI 
# corresponding to the DOIs listed in doidata database.
# The script runs so that it retrieves all of the DOIs from the MySQL database and 
# looks for the corresponding events. Once the events are found, they are inserted 
# into MongoDB. 
# Incorporated a hash map to check for duplication from MySQL. Checks for eventID
# and stores them into a dictionary. The hashmap is then used to compare the eventID
# of the new events. If it does not exist in the MySQL table, then it is inserted into
# MongoDB.

import mysql.connector
import os
import platform
import csv
import requests
import pymongo
import json
from ingestMongoEvents import ingestMongoEvents


def fetch_events():

    crossRefEventDatabaseConnection = databaseConnection()
    crossRefEventDatabaseCursor = crossRefEventDatabaseConnection.cursor()
    crossRefEventDatabaseCursor.execute("Select DOI FROM doidata._main_ WHERE DOI IS NOT NULL")

    # store DOIs 
    articles = crossRefEventDatabaseCursor.fetchall()


    # loops for each DOI (for all articles use len(articles))
    for i in range(5):
        
        article = articles[i]

        # access the DOI from set
        articleDOI = article[0]

        print(articleDOI)

        print("API Call!")

        # fetching event data for this particular DOI
        response = requests.get("https://api.eventdata.crossref.org/v1/events?mailto=YOUR_EMAIL_HERE&obj-id=" + articleDOI)
        
        # Retrieve the dict with events
        data = response.json()
        
        if (data != []):
            events = data.get("message").get("events")
            # print("Events:", events)
            transfer_buffer(events, articleDOI, crossRefEventDatabaseCursor, crossRefEventDatabaseConnection)
    
    print("\nIngest to MySQL:")
    ingestMongoEvents()

    

def transfer_buffer(events, articleDOI, crossRefEventDatabaseCursor, crossRefEventDatabaseConnection):

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
                crossRefEventDatabaseCursor.execute("Select eventID FROM cambiaevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()
                listEventIDs= {}
                
                if (eventIDs != []):
                    # store eventID as a key in listEventID dictionary 
                    for uniqueEventID in eventIDs:
                        listEventIDs[uniqueEventID[0]] = None

                    for eventID in listEventIDs:
                        # checks to see if an eventID in the database matches with an API eventID 
                        if (eventID == mongoEventID):
                            print("Duplicate Cambia-Lens Event!")
                            break

                        else: 
                            print("Cambia-Lens Ingest!")
                            # reference MongoDB collection
                            cambia = eventDatabase["Cambia-Lens"]

                            cambia.insert_one(info)
                            print("Success!")
                            break
                else:
                    print("Cambia-Lens Ingest!")
                    # reference MongoDB collection
                    cambia = eventDatabase["Cambia-Lens"]

                    cambia.insert_one(info)
                    print("Success!")
                    break
                break

            elif (key == "source_id" and value == "crossref"):
                print("Crossref")
                crossRefEventDatabaseCursor.execute("Select eventID FROM crossrefevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()
                listEventIDs= {}
                
                if (eventIDs != []):
                    # store eventID as a key in listEventID dictionary 
                    for uniqueEventID in eventIDs:
                        listEventIDs[uniqueEventID[0]] = None

                    for eventID in listEventIDs:
                        # checks to see if an eventID in the database matches with an API eventID 
                        if (eventID == mongoEventID):
                            print("Duplicate Crossref Event!")
                            break

                        else: 
                            print("Crossref Ingest!")
                            # reference MongoDB collection
                            crossref = eventDatabase["Crossref"]

                            crossref.insert_one(info)
                            print("Success!")
                            break
                else:
                    print("Crossref Ingest!")
                    # reference MongoDB collection
                    crossref = eventDatabase["Crossref"]

                    crossref.insert_one(info)
                    print("Success!")
                    break
                break

            elif (key == "source_id" and value == "datacite"):
                print("Datacite")
                crossRefEventDatabaseCursor.execute("Select eventID FROM dataciteevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()
                listEventIDs= {}
                
                if (eventIDs != []):
                    # store eventID as a key in listEventID dictionary 
                    for uniqueEventID in eventIDs:
                        listEventIDs[uniqueEventID[0]] = None

                    for eventID in listEventIDs:
                        # checks to see if an eventID in the database matches with an API eventID 
                        if (eventID == mongoEventID):
                            print("Duplicate Datacite Event!")
                            break

                        else: 
                            print("Datacite Ingest!")
                            # reference MongoDB collection
                            datacite = eventDatabase["Datacite"]

                            datacite.insert_one(info)
                            print("Success!")
                            break

                else:
                    print("Datacite Ingest!")
                    # reference MongoDB collection
                    datacite = eventDatabase["Datacite"]

                    # insert data
                    datacite.insert_one(info)
                    print("Success!")
                    break
                break

            elif (key == "source_id" and value == "f1000"):
                print("F1000")
                crossRefEventDatabaseCursor.execute("Select eventID FROM f1000event WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()
                listEventIDs= {}
                
                if (eventIDs != []):
                    # store eventID as a key in listEventID dictionary 
                    for uniqueEventID in eventIDs:
                        listEventIDs[uniqueEventID[0]] = None

                    for eventID in listEventIDs:
                        # checks to see if an eventID in the database matches with an API eventID 
                        if (eventID == mongoEventID):
                            print("Duplicate F1000 Event!")
                            break

                        else: 
                            print("F1000 Ingest!")
                            # reference MongoDB collection
                            f1000 = eventDatabase["F1000"]

                            f1000.insert_one(info)
                            print("Success!")
                            break

                else:
                    print("F1000 Ingest!")
                    # reference MongoDB collection
                    f1000 = eventDatabase["F1000"]

                    f1000.insert_one(info)
                    print("Success!")
                    break
                break

            elif (key == "source_id" and value == "hypothesis"):
                print("Hypothesis")
                crossRefEventDatabaseCursor.execute("Select eventID FROM hypothesisevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()
                listEventIDs= {}
                
                if (eventIDs != []):
                    # store eventID as a key in listEventID dictionary 
                    for uniqueEventID in eventIDs:
                        listEventIDs[uniqueEventID[0]] = None

                    for eventID in listEventIDs:
                        # checks to see if an eventID in the database matches with an API eventID 
                        if (eventID == mongoEventID):
                            print("Duplicate Hypothesis Event!")
                            break

                        else: 
                            print("Hypothesis Ingest!")
                            # reference MongoDB collection
                            hypothesis = eventDatabase["Hypothesis"]

                            hypothesis.insert_one(info)
                            print("Success!")
                            break

                else:
                    print("Hypothesis Ingest!")
                    # reference MongoDB collection
                    hypothesis = eventDatabase["Hypothesis"]

                    hypothesis.insert_one(info)
                    print("Success!")
                    break
                break

            elif (key == "source_id" and value == "newsfeed"):
                print("Newsfeed")
                crossRefEventDatabaseCursor.execute("Select eventID FROM newsfeedevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()
                listEventIDs= {}
                
                if (eventIDs != []):
                    # store eventID as a key in listEventID dictionary 
                    for uniqueEventID in eventIDs:
                        listEventIDs[uniqueEventID[0]] = None

                    for eventID in listEventIDs:
                        # checks to see if an eventID in the database matches with an API eventID 
                        if (eventID == mongoEventID):
                            print("Duplicate Newsfeed Event!")
                            break

                        else: 
                            print("Newsfeed Ingest!")
                            # reference MongoDB collection
                            newsfeed = eventDatabase["Newsfeed"]

                            newsfeed.insert_one(info)
                            print("Success!")
                            break

                else:
                    print("Newsfeed Ingest!")
                    # reference MongoDB collection
                    newsfeed = eventDatabase["Newsfeed"]

                    newsfeed.insert_one(info)
                    print("Success!")
                    break
                break

            elif (key == "source_id" and value == "reddit"):
                print("Reddit")
                crossRefEventDatabaseCursor.execute("Select eventID FROM redditevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()
                listEventIDs= {}
                
                if (eventIDs != []):
                    # store eventID as a key in listEventID dictionary 
                    for uniqueEventID in eventIDs:
                        listEventIDs[uniqueEventID[0]] = None

                    for eventID in listEventIDs:
                        # checks to see if an eventID in the database matches with an API eventID 
                        if (eventID == mongoEventID):
                            print("Duplicate Reddit Event!")
                            break

                        else: 
                            print("Reddit Ingest!")
                            # reference MongoDB collection
                            reddit = eventDatabase["Reddit"]

                            reddit.insert_one(info)
                            print("Success!")
                            break

                else:
                    print("Reddit Ingest!")
                    # reference MongoDB collection
                    reddit = eventDatabase["Reddit"]

                    reddit.insert_one(info)
                    print("Success!")
                    break
                break

            elif (key == "source_id" and value == "reddit-links"):
                print("Reddit-Links")
                crossRefEventDatabaseCursor.execute("Select eventID FROM redditlinksevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()
                listEventIDs= {}
                
                if (eventIDs != []):
                    # store eventID as a key in listEventID dictionary 
                    for uniqueEventID in eventIDs:
                        listEventIDs[uniqueEventID[0]] = None

                    for eventID in listEventIDs:
                        # checks to see if an eventID in the database matches with an API eventID 
                        if (eventID == mongoEventID):
                            print("Duplicate Reddit-Links Event!")
                            break

                        else: 
                            print("Reddit-Links Ingest!")
                            # reference MongoDB collection
                            redditlinks = eventDatabase["Reddit-Links"]

                            redditlinks.insert_one(info)
                            print("Success!")
                            break

                else:
                    print("Reddit-Links Ingest!")
                    # reference MongoDB collection
                    redditlinks = eventDatabase["Reddit-Links"]

                    redditlinks.insert_one(info)
                    print("Success!")
                    break
                break

            elif (key == "source_id" and value == "stackexchange"):
                print("Stack Exchange")
                crossRefEventDatabaseCursor.execute("Select eventID FROM stackexchangeevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()
                listEventIDs= {}
                
                if (eventIDs != []):
                    # store eventID as a key in listEventID dictionary 
                    for uniqueEventID in eventIDs:
                        listEventIDs[uniqueEventID[0]] = None

                    for eventID in listEventIDs:
                        # checks to see if an eventID in the database matches with an API eventID 
                        if (eventID == mongoEventID):
                            print("Duplicate Stack Exchange Event!")
                            break

                        else: 
                            print("Stack Exchange Ingest!")
                            # reference MongoDB collection
                            stackexchange = eventDatabase["StackExchange"]

                            stackexchange.insert_one(info)
                            print("Success!")
                            break
                else:
                    print("Stack Exchange Ingest!")
                    # reference MongoDB collection
                    stackexchange = eventDatabase["StackExchange"]

                    stackexchange.insert_one(info)
                    print("Success!")
                    break
                break

            elif (key == "source_id" and value == "twitter"):
                print("Twitter")
                crossRefEventDatabaseCursor.execute("Select eventID FROM twitterevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()
                listEventIDs= {}
                
                if (eventIDs != []):
                    # store eventID as a key in listEventID dictionary 
                    for uniqueEventID in eventIDs:
                        listEventIDs[uniqueEventID[0]] = None

                    for eventID in listEventIDs:
                        # checks to see if an eventID in the database matches with an API eventID 
                        if (eventID == mongoEventID):
                            print("Duplicate Twitter Event!")
                            break

                        else: 
                            print("Twitter Ingest!")
                            # reference MongoDB collection
                            twitter = eventDatabase["Twitter"]

                            twitter.insert_one(info)
                            print("Success!")
                            break
                else:
                    print("Twitter Ingest!")
                    # reference MongoDB collection
                    twitter = eventDatabase["Twitter"]

                    twitter.insert_one(info)
                    print("Success!")
                    break
                break

            elif (key == "source_id" and value == "web"):
                print("Web")
                crossRefEventDatabaseCursor.execute("Select eventID FROM webevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()
                listEventIDs= {}
                
                if (eventIDs != []):
                    # store eventID as a key in listEventID dictionary 
                    for uniqueEventID in eventIDs:
                        listEventIDs[uniqueEventID[0]] = None

                    for eventID in listEventIDs:
                        # checks to see if an eventID in the database matches with an API eventID 
                        if (eventID == mongoEventID):
                            print("Duplicate Web Event!")
                            break

                        else: 
                            print("Web Ingest!")
                            # reference MongoDB collection
                            web = eventDatabase["Web"]

                            web.insert_one(info)
                            print("Success!")
                            break
                else:
                    print("Web Ingest!")
                    # reference MongoDB collection
                    web = eventDatabase["Web"]

                    web.insert_one(info)
                    print("Success!")
                    break
                break

            elif (key == "source_id" and value == "wikipedia"):
                print("Wikipedia")
                crossRefEventDatabaseCursor.execute("Select eventID FROM wikipediaevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()
                listEventIDs= {}
                
                if (eventIDs != []):
                    # store eventID as a key in listEventID dictionary 
                    for uniqueEventID in eventIDs:
                        listEventIDs[uniqueEventID[0]] = None

                    for eventID in listEventIDs:
                        # checks to see if an eventID in the database matches with an API eventID 
                        if (eventID == mongoEventID):
                            print("Duplicate Wikipedia Event!")
                            break

                        else: 
                            print("Wikipedia Ingest!")
                            # reference MongoDB collection
                            wikipedia = eventDatabase["Wikipedia"]

                            wikipedia.insert_one(info)
                            print("Success!")
                            break
                else:
                    print("Wikipedia Ingest!")
                    # reference MongoDB collection
                    wikipedia = eventDatabase["Wikipedia"]

                    wikipedia.insert_one(info)
                    print("Success!")
                    break
                break

            elif (key == "source_id" and value == "wordpressdotcom"):
                print("Wordpress.com")
                crossRefEventDatabaseCursor.execute("Select eventID FROM wordpressevent WHERE objectID='" + objectID + "'")

                # store DOIs 
                eventIDs = crossRefEventDatabaseCursor.fetchall()
                listEventIDs= {}
                
                if (eventIDs != []):
                    # store eventID as a key in listEventID dictionary 
                    for uniqueEventID in eventIDs:
                        listEventIDs[uniqueEventID[0]] = None

                    for eventID in listEventIDs:
                        # checks to see if an eventID in the database matches with an API eventID 
                        if (eventID == mongoEventID):
                            print("Duplicate Wordpress.com Event!")
                            break

                        else: 
                            print("Wordpress.com Ingest!")
                            # reference MongoDB collection
                            wordpress = eventDatabase["WordPressDotCom"]

                            wordpress.insert_one(info)
                            print("Success!")
                            break
                else:
                    print("Wordpress.com Ingest!")
                    # reference MongoDB collection
                    wordpress = eventDatabase["WordPressDotCom"]

                    wordpress.insert_one(info)
                    print("Success!")
                    break
                break


# def insertCollection(collection, info):
#     # print(info)
#     # collection.insert_one(info) 
#     result = collection.find()
#     for documents in result:
#         print("List:" , list(result))
#         if (documents != info):
#             try:
#                 print("Data: ", info)
#                 collection.insert_one(info)
#             except pymongo.errors.DuplicateKeyError:
#                 continue
            
#         else:
#             print("Pass!")
#         # except pymongo.errors.DuplicateKeyError:
#         # # skip document because it already exists in new collection
#         #     continue
            

def databaseConnection():
    try:
        # connect to doidata database
        print("MySQL Credentials")
        mysql_username = input("Username: ")
        mysql_password = input("Password: ")

        crossRefEventDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "crossrefeventdatamain")

        return crossRefEventDatabase


    except:
        print("Error: Invalid MySQL credentials")
        return

    print ("Connected to the database...")


if __name__ == '__main__':
    fetch_events()