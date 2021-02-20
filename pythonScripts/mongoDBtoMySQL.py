# Tabish's work
import pymongo
import os
import pandas
import json
import requests
import mysql.connector
from getPassword import getPassword

def connecttomysql():
    # get the users password from openAlt_W2021/web/passwd.txt
    mysql_username = "root"
    mysql_password = "pass"

    try:
        drBowmanDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "dr_bowman_doi_data_tables")
        print("Connected successfully to MySQL")
    except:
        print("Could not connect to MySQL")
        return

def retrieveFromMongoDB():
    try:
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        print("Connected successfully to MongoDB")
    except:
        print("Could not connect to MongoDB")
        return

    dbs=client.retrievedFromAPI
    coll=dbs.my_coll
    x=coll.find({},{'_id':0,'status':0,'message-type':0,'message-version':0,'message':1})
    #y=x.find({},{'facets':0,'total-results':0,'items':1,'items-per-page':0,'query':0})
    print(x)


    return

def storeInMySQL():

    return

if __name__=='__main__':
    connecttomysql()
    retrieveFromMongoDB()
    storeInMySQL()
