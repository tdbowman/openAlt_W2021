# Tabish's work
"""
MIT License

Copyright (c) 2020 tdbowman-CompSci-F2020

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import pymongo
import os
import sys
import pandas
import json
import requests
import mysql.connector
from ingestCrossrefMetadata import crossrefMetadataIngest

def hashmap(listoffks):
    # Takes every DOI and their associated foreign key
    # from the _main_ table and stores them in a dictionary
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
    # Takes all foreign keys stored in the author table
    # and stores them in a dictionary
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
    # Retrieve metadata from api
    r = requests.get('https://api.crossref.org/works/'+ DOI)
    # Connect to localhost MongoDB
    try:
        client = pymongo.MongoClient('mongodb://localhost:27017/')
    except:
        print("Could not connect to MongoDB.")
        return
    # Cursor to spcified database; create if it doesn't exist
    dbs = client["MetadataDatabase"]
    # Cursor to specified collection; create if it doesn't exist
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
        # For each DOI retrieved from the _main_ table, check to see if its
        # associated foreign key is already stored in the author table
        if value in listofingestedfks:
            print("Metadata already stored.")
        # If the foreign key is not found in the author table,
        # the metadata of the given DOI will be stored in the author table
        else:
            storeMetaDatainMongoDB(key, value)

if __name__ == '__main__':
    main()
