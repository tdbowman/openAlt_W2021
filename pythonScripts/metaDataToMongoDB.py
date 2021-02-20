# Tabish's work
import pymongo
import os
import requests

def storeMetaDatainMongoDB():
    r = requests.get('https://api.crossref.org/works?sample=10')

    try:
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        print("Connected successfully to MongoDB")
    except:
        print("Could not connect to MongoDB")
        return

    dbs=client.retrievedFromAPI

    coll=dbs.my_coll

    coll.insert_one(r.json())

if __name__=='__main__':
    storeMetaDatainMongoDB()
