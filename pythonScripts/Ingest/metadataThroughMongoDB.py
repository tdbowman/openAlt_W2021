# Tabish's work
import pymongo
import os
import pandas
import json
import requests
import mysql.connector
from ingestCrossrefMetadata import crossrefMetadataIngest

def checkmysql(DOI):
    # Check MySQL database for the specified DOI
    mysql_username = "root"
    mysql_password = "pass"
    try:
        db = mysql.connector.connect( host = "localhost",
                                        user = mysql_username,
                                        passwd = mysql_password,
                                        database = "doidata")
    except:
        print("Could not connect to MySQL")
        return
    myCursor=db.cursor(buffered=True)
    myCursor.execute("SELECT * FROM _metadata_ WHERE DOI LIKE '%" + (str(DOI)) + "%'")
    if myCursor.fetchone() == None:
        # If the DOI is not in the database, retrieve from API and store in MongoDB
        storeMetaDatainMongoDB(DOI)
    else:
        # Retrieve from MySQL
        print("Data is already in MySQL database")
        return
    return

def storeMetaDatainMongoDB(DOI):
    # retrieve metadata from api
    r = requests.get('https://api.crossref.org/works/'+ DOI)
    # connect to localhost MongoDB
    try:
        client = pymongo.MongoClient('mongodb://localhost:27017/')
    except:
        print("Could not connect to MongoDB")
        return
    # cursor to spcified database; create if it doesn't exist
    dbs=client["MetadataDatabase"]
    # cursor to specified collection; create if it doesn't exist
    coll=dbs["MetaData"]
    data=r.json()
    if data.get("message-type")=="work":
        coll.insert_one(data.get("message"))
    else:
        print("Invalid data")
    storeinmysql(DOI, coll)
    return

def storeinmysql(DOI, coll):
    # Calls function from ingestCrossrefMetadata.py
    # and stores metadata in MySQL
    mysql_username = "root"
    mysql_password = "pass"
    try:
        db = mysql.connector.connect( host = "localhost",
                                        user = mysql_username,
                                        passwd = mysql_password,
                                        database = "doidata")
    except:
        print("Could not connect to MySQL")
        return
    myCursor=db.cursor(buffered=True)
    myCursor.execute("SELECT DOI FROM _metadata_")
    for data in coll.find({},{"_id":1,"DOI":1, "URL":1, "abstract":1, "created":1, "language":1, "author":1, "subject":1, "publisher":1,
    "reference-count":1, "is-referenced-by-count":1, "references-count":1, "score":1, "source":1, "title":1, "type":1}):
        crossrefMetadataIngest(data, myCursor, db)
    # End the connection to the MySQL database
    myCursor.close()
    db.close()
    print("Data stored")
    # Delete all contents of collection; delete_many used just to be safe
    coll.delete_many({})
    return

if __name__=='__main__':
    # This is only for testing
    # Call checkmysql() function with the DOI as the argument to ingest metadata
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    dbs=client["MetadataDatabase"]
    coll=dbs["MetaData"]
    r = requests.get('https://api.crossref.org/works?sample=100')
    data=r.json()
    for i in data.get("message").get("items"):
        DOI=i.get("DOI")
        checkmysql(DOI)
