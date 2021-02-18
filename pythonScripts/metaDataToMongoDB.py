# Tabish's work
import pymongo
import os
import pandas
import json
import requests
import mysql.connector

def connecttomysql():

    mysql_username = "root"

    mysql_password = "pass"

    try:
        drBowmanDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "dr_bowman_doi_data_tables")

        print ("Connected successfully to MySQL")
    except:
        print("Could not connect to MySQL")

        return

def main():
    try:
        client = pymongo.MongoClient('mongodb://localhost:27017/')

        print("Connected successfully to MongoDB")
    except:
        print("Could not connect to MongoDB")

        return

    dbs=client.local

    coll=dbs.my_coll

    r = requests.get('https://api.crossref.org/v1/works/10.1088/0004-637X/722/2/971')

    id1 = coll.insert_one(r.json())

    print(id1)
    print(coll)

if __name__=='__main__':
    connecttomysql()
    main()
