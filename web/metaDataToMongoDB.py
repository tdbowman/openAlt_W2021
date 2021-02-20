# Tabish's work
import pymongo
import os
import pandas
import json
import requests
import mysql.connector
from getPassword import getPassword

def main():
    r = requests.get('https://api.crossref.org/works?sample=10')

    try:
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        print("Connected successfully to MongoDB")
    except:
        print("Could not connect to MongoDB")
        return

    dbs=client.retrievedFromAPI

    coll=dbs.my_coll

    id1 = coll.insert_one(r.json())

if __name__=='__main__':
    main()
