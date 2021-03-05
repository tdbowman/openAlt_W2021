# Tabish's work
import pymongo
import os
import pandas
import json
import requests
import mysql.connector
from metaDataToMongoDB import storeMetaDatainMongoDB
from ingestCrossrefMetadata import crossrefMetadataIngest

def retrieveFromMongoDB(DOI):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    # cursor to spcified database; create if it doesn't exist
    db=client["MetadataDatabase"]
    # cursor to specified collection; create if it doesn't exist
    coll=db["MetaData"]
    storeinmysql(DOI, coll)
    return

def storeinmysql(DOI, coll):
    mysql_username = "root"
    mysql_password = "pass"
    try:
        drBowmanDatabase = mysql.connector.connect( host = "localhost",
                                                    user = mysql_username,
                                                    passwd = mysql_password,
                                                    database = "doidata")
    except:
        print("Could not connect to MySQL")
        return
    myCursor=drBowmanDatabase.cursor(buffered=True)
    myCursor.execute("SELECT DOI FROM _metadata_")
    for data in coll.find({"DOI":DOI},{"_id":1,"DOI":1, "URL":1, "abstract":1, "created":1, "language":1, "author":1, "subject":1, "publisher":1,
    "reference-count":1, "is-referenced-by-count":1, "references-count":1, "score":1, "source":1, "title":1, "type":1}):
        crossrefMetadataIngest(data, myCursor, drBowmanDatabase)
    # End the connection to the MySQL database
    myCursor.close()
    drBowmanDatabase.close()
    return

if __name__=='__main__':
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db=client["MetadataDatabase"]
    coll=db["MetaData"]
    for i in coll.find({}):
        # DOI value holds placeholder string
        #DOI="10.1093/jn/128.10.1731"
        DOI=i.get("DOI")
        DOI=storeMetaDatainMongoDB(DOI)
        retrieveFromMongoDB(DOI)
