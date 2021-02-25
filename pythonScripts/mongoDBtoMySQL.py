# Tabish's work
import pymongo
import os
import pandas
import json
import requests
import mysql.connector
from metaDataToMongoDB import storeMetaDatainMongoDB

def retrieveFromMongoDB():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    # cursor to spcified database; create if it doesn't exist
    db=client["MetadataDatabase"]
    # cursor to specified collection; create if it doesn't exist
    coll=db["MetaData"]
    data=coll.find({},{"_id":1,"message-type":1,"message":1})
    for i in data:
        print(i.get("_id"))
        if i.get("message-type")=="work-list":
            checkmysqlforlist(i.get("message").get("items"))
        elif i.get("message-type")=="work":
            checkmysqlfordict(i.get("message"))
        else:
            print("Invalid data")

def checkmysqlforlist(li):
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
    myCursor.execute("SELECT DOI FROM _metadata_")
    dupe=[False]*len(li)
    for i in myCursor.fetchall():
        for j in li:
            if i[0]==j.get("DOI"):
                print("found dupe")
                dupe[j]=True
    for j in dupe:
        if dupe[j]==False:
            print("no dice")
            storeinmysql(li[j])

def checkmysqlfordict(di):
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
    myCursor.execute("SELECT DOI FROM _metadata_")
    dupe=False
    for i in myCursor.fetchall():
        if i[0] == di.get("DOI"):
            print("found dupe")
            dupe=True
    if dupe==False:
        print("no dice")
        storeinmysql(di)

def storeinmysql(data):
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
    df=pandas.DataFrame(data)
    print(type(df))
    #myCursor.execute("INSERT INTO _test_ VALUES %s", json_object)






    return

if __name__=='__main__':
    #storeMetaDatainMongoDB()
    retrieveFromMongoDB()
