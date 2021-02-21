# Tabish's work
import pymongo
import os
import pandas
import json
import requests
import mysql.connector

def retrieveFromMongoDB():
    try:
        client = pymongo.MongoClient('mongodb://localhost:27017/')
    except:
        print("Could not connect to MongoDB")
        return
    # cursor to spcified database; create if it doesn't exist
    dbs=client["MetadataDatabase"]
    # cursor to specified collection; create if it doesn't exist
    md=dbs["MetaData"]
    storeInMySQL(md)

def storeInMySQL(md):
    mysql_username = "root"
    mysql_password = "pass"

    try:
        drBowmanDatabase = mysql.connector.connect( host = "localhost",
                                                    user = mysql_username,
                                                    passwd = mysql_password,
                                                    database = "dr_bowman_doi_data_tables")
    except:
        print("Could not connect to MySQL")
        return
    myCursor=drBowmanDatabase.cursor()
    sql = "INSERT INTO _main_ VALUES " + md

    #drBowmanDatabase.commit()

if __name__=='__main__':
    retrieveFromMongoDB()
