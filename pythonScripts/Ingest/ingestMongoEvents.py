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
# The purpose of this script is to ingest the events that are in MongoDB into MySQL tables. 
# Sort through all of the collections by event name and ingest the documents within the collection
# into the proper sql tables.

# -----------------------------------------------------------------------------------------

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
import json

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
        print("Error: Cannot connect to database.")
        return

    print ("Connected to the database...")

# -----------------------------------------------------------------------------------------

def ingestMongoEvents():

    # -----------------------------------------------------------------------------------------

    # Retrieve MongoDB info from config file
    mongoConnection = APP_CONFIG['MongoDB-Event-Database']['address']
    databaseName = APP_CONFIG['MongoDB-Event-Database']['name']

    # Retrieve the MySQL database curose 
    connection = databaseConnection()
    cursor = connection.cursor()

    # setup localization
    myclient = pymongo.MongoClient(mongoConnection)

    # reference MongoDB database
    database = myclient[databaseName]

    # -----------------------------------------------------------------------------------------

    try:
        # for names in collNames:
        for coll in database.list_collection_names():

            # -----------------------------------------------------------------------------------------

            if (coll == "Cambia-Lens"):
                print("Cambia-Lens Ingest!")

                # Match the event with the collection name
                events = database[coll]

                # For all events in the collection, iterate through them and ingest them
                for uniqueEvent in events.find({}):
                    cambiaLens.cambiaLensIngest(uniqueEvent, cursor, connection)

            # -----------------------------------------------------------------------------------------

            elif (coll == "Crossref"):
                print("Crossref Ingest!")

                # Match the event with the collection name
                events = database[coll]

                # For all events in the collection, iterate through them and ingest them
                for uniqueEvent in events.find({}):
                    crossref.crossrefIngest(uniqueEvent, cursor, connection)

            # -----------------------------------------------------------------------------------------

            elif (coll == "Datacite"):
                print("Datacite Ingest!")

                # Match the event with the collection name
                events = database[coll]

                # For all events in the collection, iterate through them and ingest them
                for uniqueEvent in events.find({}):
                    datacite.dataciteIngest(uniqueEvent, cursor, connection)

            # -----------------------------------------------------------------------------------------

            elif (coll == "F1000"):
                print("F1000 Ingest!")

                # Match the event with the collection name
                events = database[coll]

                # For all events in the collection, iterate through them and ingest them
                for uniqueEvent in events.find({}):
                    f1000.F1000Ingest(uniqueEvent, cursor, connection)

            # -----------------------------------------------------------------------------------------

            elif (coll == "Hypothesis"):
                print("Hypothesis Ingest!")

                # Match the event with the collection name
                events = database[coll]

                # For all events in the collection, iterate through them and ingest them
                for uniqueEvent in events.find({}):
                    hypothesis.hypothesisIngest(uniqueEvent, cursor, connection)

            # -----------------------------------------------------------------------------------------

            elif (coll == "Newsfeed"):
                print("Newsfeed Ingest!")

                # Match the event with the collection name
                events = database[coll]

                # For all events in the collection, iterate through them and ingest them
                for uniqueEvent in events.find({}):
                    newsfeed.newsfeedIngest(uniqueEvent, cursor, connection)

            # -----------------------------------------------------------------------------------------

            elif (coll == "Reddit"):
                print("Reddit Ingest!")

                # Match the event with the collection name
                events = database[coll]

                # For all events in the collection, iterate through them and ingest them
                for uniqueEvent in events.find({}):
                    reddit.redditIngest(uniqueEvent, cursor, connection)

            # -----------------------------------------------------------------------------------------

            elif (coll == "Reddit-Links"):
                print("Reddit-Links Ingest!")

                # Match the event with the collection name
                events = database[coll]

                # For all events in the collection, iterate through them and ingest them
                for uniqueEvent in events.find({}):
                    redditLinks.redditLinksIngest(uniqueEvent, cursor, connection)

            # -----------------------------------------------------------------------------------------

            elif (coll == "StackExchange"):
                print("StackExchange Ingest!")

                # Match the event with the collection name
                events = database[coll]

                # For all events in the collection, iterate through them and ingest them
                for uniqueEvent in events.find({}):
                    stackExchange.stackExchangeIngest(uniqueEvent, cursor, connection)

            # -----------------------------------------------------------------------------------------

            elif (coll == "Twitter"):
                print("Twitter Ingest!")

                # Match the event with the collection name
                events = database[coll]

                # For all events in the collection, iterate through them and ingest them
                for uniqueEvent in events.find({}):
                    twitter.twitterIngest(uniqueEvent, cursor, connection)

            # -----------------------------------------------------------------------------------------

            elif (coll == "Web"):
                print("Web Ingest!")

                # Match the event with the collection name
                events = database[coll]

                # For all events in the collection, iterate through them and ingest them
                for uniqueEvent in events.find({}):
                    web.webIngest(uniqueEvent, cursor, connection)

            # -----------------------------------------------------------------------------------------

            elif (coll == "Wikipedia"):
                print("Wikipedia Ingest!")

                # Match the event with the collection name
                events = database[coll]

                # For all events in the collection, iterate through them and ingest them
                for uniqueEvent in events.find({}):
                    wikipedia.wikipediaIngest(uniqueEvent, cursor, connection)

            # -----------------------------------------------------------------------------------------
                    
            elif (coll == "WordPressDotCom"):
                print("WordPressDotCom Ingest!")

                # Match the event with the collection name
                events = database[coll]

                # For all events in the collection, iterate through them and ingest them
                for uniqueEvent in events.find({}):
                    wordpress.wordpressIngest(uniqueEvent, cursor, connection)

    # -----------------------------------------------------------------------------------------

    except:
        print("Ingest failed!")
        cursor.close()
        connection.close()

    # -----------------------------------------------------------------------------------------