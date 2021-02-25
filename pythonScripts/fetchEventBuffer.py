# Author: Salsabil Bakth
# The purpose of this script is to retrieve all of the unique events per each DOI 
# corresponding to the DOIs listed in dr_bowman_doi_data_tables database.
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

    print("MySQL Credentials")
    # mysql_username = input("Username: ")
    # mysql_password = input("Password: ")
    mysql_username = "root"
    mysql_password = "pass1234"


    try:
        # connect to dr_bowman_doi_data_tables database
        drBowmanDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "dr_bowman_doi_data_tables")


    except:
        print("Error: Invalid MySQL credentials")
        return

    print ("Connected to the database...")

    drBowmanDatabaseCursor = drBowmanDatabase.cursor()

    drBowmanDatabaseCursor.execute("Select DOI FROM _main_ WHERE DOI IS NOT NULL")

    # store DOIs 
    articles = drBowmanDatabaseCursor.fetchall()


    # loops for each DOI (for all articles use len(articles))
    for i in range(2):
        article = articles[i]

        # access the DOI from set
        articleDOI = article[0]

        print(articleDOI)
        
        # fetching event data for this particular DOI
        response = requests.get("https://api.eventdata.crossref.org/v1/events?mailto=YOUR_EMAIL_HERE&obj-id=" + articleDOI)
        
        # check to see if the API is responding with a code 200
        print(response.status_code)

        # display info on console
        print(response.json())

        # Retrieve the dict with events
        data = response.json()
        uniqueEvents = data.get("message").get("events")
        print("Print event: ", uniqueEvents)

        transfer_buffer(uniqueEvents)

    

def transfer_buffer(uniqueEvents):
     # check to see if events are empty
    if (uniqueEvents != []):

        # setup localization
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        # reference MongoDB database
        eventDatabase = myclient["EventDatabase"]

        # reference MongoDB collection
        events = eventDatabase["EventTest"]

        # insert data
        events.insert_many(uniqueEvents)    


if __name__ == '__main__':
    fetch_events()