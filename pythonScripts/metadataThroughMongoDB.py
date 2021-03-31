# Tabish's work
import pymongo
import os
import sys
import pandas
import json
import requests
import mysql.connector
from ingestCrossrefMetadata import crossrefMetadataIngest

def hashmap(listoffks):
    mysql_username = "root"
    mysql_password = "pass"
    try:
        db = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "doidata")
    except:
        print("Could not connect to MySQL.")
        return
    myCursor = db.cursor(buffered=True)
    myCursor.execute("SELECT DOI,fk FROM _main_ WHERE DOI IS NOT NULL")
    fks = myCursor.fetchall()
    for i,j in fks:
        listoffks[i] = j
    return listoffks

def checkhash(listofingestedfks):
    mysql_username = "root"
    mysql_password = "pass"
    try:
        db = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "doidata")
    except:
        print("Could not connect to MySQL.")
        return
    myCursor = db.cursor(buffered=True)
    myCursor.execute("SELECT fk FROM author")
    fks = myCursor.fetchall()
    for i in fks:
        listofingestedfks[i[0]] = None
    return listofingestedfks


def storeMetaDatainMongoDB(DOI, fk):
    # retrieve metadata from api
    r = requests.get('https://api.crossref.org/works/'+ DOI)
    # connect to localhost MongoDB
    try:
        client = pymongo.MongoClient('mongodb://localhost:27017/')
    except:
        print("Could not connect to MongoDB.")
        return
    # cursor to spcified database; create if it doesn't exist
    dbs = client["MetadataDatabase"]
    # cursor to specified collection; create if it doesn't exist
    coll = dbs["MetaData"]
    # Make sure collection is empty
    coll.delete_many({})
    # Try to convert httpresponse to JSON
    try:
         data = r.json()
    except:
        print("Invalid data. Data could not be converted to JSON.")
        return
    # Insert JSON data in MongoDB
    if data.get("message-type") == "work":
        coll.insert_one(data.get("message"))
    else:
        print("Invalid data. Use message-type = work.")
        return
    storeinmysql(coll, DOI, fk)
    return

def storeinmysql(coll, DOI, fk):
    # Calls function from ingestCrossrefMetadata.py
    # and stores metadata in MySQL
    mysql_username = "root"
    mysql_password = "pass"
    try:
        db = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "doidata")
    except:
        print("Could not connect to MySQL.")
        return
    myCursor = db.cursor(buffered=True)
    for data in coll.find({},{"author":1}):
        if "author" in data.keys():
            for i in data["author"]:
                crossrefMetadataIngest(i, myCursor, db, fk)
        else:
            print("Invalid data. Author metadata not found.")
            return
    # End the connection to the MySQL database
    myCursor.close()
    db.close()
    print("Metadata stored.")
    # Delete all contents of collection
    coll.delete_many({})
    return

def main():
    listoffks = hashmap({})
    listofingestedfks = checkhash({})
    for key,value in listoffks.items():
        print(value)
        if value in listofingestedfks:
            print("Metadata already stored.")
        else:
            storeMetaDatainMongoDB(key, value)

if __name__ == '__main__':
    # This main block is only for testing
    main()
