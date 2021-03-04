# Author: Salsabil Bakth
# The purpose of this script is to ingest the events that are in MongoDB into MySQL tables. 
# Identify each event type by the key (source_id) and ingest them into the proper event tables.

import mysql.connector
import os
import platform
import csv
import requests
import pymongo
import json
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
import logging
import sys
import time

# Logging parameters
logging.basicConfig(filename='./ingest.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  

# Connect to MySQL database
try:
    import mysql.connector
except:
    logging.info("Cannot determine how you intend to run the program")

# MySQL credentials
print("MySQL Credentials")
# mysql_username = input("Username: ")
# mysql_password = input("Password: ")
mysql_username = "root"
mysql_password = "pass1234"


def ingestEvents():

    # Setup MySQL connection
    connection = mysql.connector.connect(user=str(mysql_username), password=str(
        mysql_password), host='127.0.0.1', database='crossrefeventdatamain')
    cursor = connection.cursor() 

    # Connect to MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    # reference MongoDB database
    eventDatabase = myclient["EventDatabase"]

    # reference MongoDB collection
    events = eventDatabase["EventTest"]

    # Iterate through the event list
    for uniqueEvent in events.find({}):
        
        source_id= None
        print (type(uniqueEvent))
        
        # Iterate through each event for the content
        for key, value in uniqueEvent.items():

            # If there is a source_id, iterate and match the event types to get ingested into the proper tables
            if (key == "source_id"):
                source_id = value 
                print(type(source_id))

                if (source_id == "cambia-lens"):
                    cambiaLens.cambiaLensIngest(uniqueEvent, cursor, connection)
                    print("Cambia Lens event!")

                elif (source_id == "crossref"):
                    crossref.crossrefIngest(uniqueEvent, cursor, connection)
                    print("Crossref event!")

                elif (source_id == "datacite"):
                    datacite.dataciteIngest(uniqueEvent, cursor, connection)
                    print("Datacite event!")

                elif (source_id == "f1000"):
                    f1000.F1000Ingest(uniqueEvent, cursor, connection)
                    print("F1000 event!")

                elif (source_id == "hypothesis"):
                    hypothesis.hypothesisIngest(uniqueEvent, cursor, connection)
                    print("Hypothesis event!")
        
                elif (source_id == "newsfeed"):
                    newsfeed.newsfeedIngest(uniqueEvent, cursor, connection)
                    print("Newsfeed event!")
                
                elif (source_id == "reddit"):
                    reddit.redditIngest(uniqueEvent, cursor, connection)
                    print("Reddit event!")

                elif (source_id == "reddit-links"):
                    redditLinks.redditLinksIngest(uniqueEvent, cursor, connection)
                    print("Reddit links event!")

                elif (source_id == "stackexchange"):
                    stackExchange.stackExchangeIngest(uniqueEvent, cursor, connection)
                    print("Stack exchange event!")


                elif (source_id == "twitter"):
                    twitter.twitterIngest(uniqueEvent, cursor, connection)
                    print("Twitter event!")

                elif (source_id == "web"):
                    web.webIngest(uniqueEvent, cursor, connection)
                    print("Web event!")

                elif (source_id == "wikipedia"):
                    wikipedia.wikipediaIngest(uniqueEvent, cursor, connection)
                    print("Wikipedia event!")
                
                elif (source_id == "wordpressdotcom"):
                    wordpress.wordpressIngest(uniqueEvent, cursor, connection)
                    print("Word press event!")

    # End the connection to the MySQL database
    cursor.close()
    connection.close()

    # Print the time it took to run this file
    print("--- %s seconds ---" % (time.time() - start_time))

    
if __name__ == '__main__':
    start_time = time.time()
    ingestEvents()