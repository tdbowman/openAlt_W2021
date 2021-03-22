# Author: Salsabil Bakth
# The purpose of this script is to ingest the events that are in MongoDB into MySQL tables. 
# Sort through all of the collections by name and ingest the documents within the collection
# into the proper sql tables.

import mysql.connector
import os
import pymongo
import cambiaLens
import wordpress
import wikipedia
import web
import f1000
import twitter
import stackExchange
import redditLinks
import reddit
import newsfeed
import hypothesis
import datacite
import crossref

def ingestMongoEvents():
    # MySQL credentials
    print("MySQL Credentials")
    mysql_username = input("Username: ")
    mysql_password = input("Password: ")

    # Setup MySQL connection
    connection = mysql.connector.connect(user=str(mysql_username), password=str(
        mysql_password), host='127.0.0.1', database='crossrefeventdatamain')
    cursor = connection.cursor() 

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    database = myclient['EventDatabase']

    # collNames = {"Cambia-Lens", "Crossref", "Datacite", "F1000", "Hypothesis", "Newsfeed", "Reddit", "Reddit-Links", "StackExchange",
    # "Twitter", "Web", "Wikipedia", "WordPressDotCom"}

    # for names in collNames:
    for coll in database.list_collection_names():
        # if (names == coll):
        #     print (coll)
        if (coll == "Cambia-Lens"):
            print("Cambia-Lens Ingest!")
            events = database[coll]
            for uniqueEvent in events.find({}):
                cambiaLens.cambiaLensIngest(uniqueEvent, cursor, connection)

        elif (coll == "Crossref"):
            print("Crossref Ingest!")
            events = database[coll]
            for uniqueEvent in events.find({}):
                crossref.crossrefIngest(uniqueEvent, cursor, connection)

        elif (coll == "Datacite"):
            print("Datacite Ingest!")
            events = database[coll]
            for uniqueEvent in events.find({}):
                datacite.dataciteIngest(uniqueEvent, cursor, connection)

        elif (coll == "F1000"):
            print("F1000 Ingest!")
            events = database[coll]
            for uniqueEvent in events.find({}):
                f1000.F1000Ingest(uniqueEvent, cursor, connection)

        elif (coll == "Hypothesis"):
            print("Hypothesis Ingest!")
            events = database[coll]
            for uniqueEvent in events.find({}):
                hypothesis.hypothesisIngest(uniqueEvent, cursor, connection)

        elif (coll == "Newsfeed"):
            print("Newsfeed Ingest!")
            events = database[coll]
            for uniqueEvent in events.find({}):
                newsfeed.newsfeedIngest(uniqueEvent, cursor, connection)

        elif (coll == "Reddit"):
            print("Reddit Ingest!")
            events = database[coll]
            for uniqueEvent in events.find({}):
                reddit.redditIngest(uniqueEvent, cursor, connection)

        elif (coll == "Reddit-Links"):
            print("Reddit-Links Ingest!")
            events = database[coll]
            for uniqueEvent in events.find({}):
                redditLinks.redditLinksIngest(uniqueEvent, cursor, connection)

        elif (coll == "StackExchange"):
            print("StackExchange Ingest!")
            events = database[coll]
            for uniqueEvent in events.find({}):
                stackExchange.stackExchangeIngest(uniqueEvent, cursor, connection)

        elif (coll == "Twitter"):
            print("Twitter Ingest!")
            events = database[coll]
            for uniqueEvent in events.find({}):
                twitter.twitterIngest(uniqueEvent, cursor, connection)

        elif (coll == "Web"):
            print("Web Ingest!")
            events = database[coll]
            for uniqueEvent in events.find({}):
                web.webIngest(uniqueEvent, cursor, connection)

        elif (coll == "Wikipedia"):
            print("Wikipedia Ingest!")
            events = database[coll]
            for uniqueEvent in events.find({}):
                wikipedia.wikipediaIngest(uniqueEvent, cursor, connection)
                
        elif (coll == "WordPressDotCom"):
            print("WordPressDotCom Ingest!")
            events = database[coll]
            for uniqueEvent in events.find({}):
                wordpress.wordpressIngest(uniqueEvent, cursor, connection)

        else:
            print("Nothing!")