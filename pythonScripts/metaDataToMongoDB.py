# Tabish's work
import pymongo
import os
import requests

def storeMetaDatainMongoDB():
    # hard code for testing; change later
    # retrieve metadata from api
    r = requests.get('https://api.crossref.org/works?sample=10')
    # connect to localhost MongoDB
    try:
        client = pymongo.MongoClient('mongodb://localhost:27017/')
    except:
        print("Could not connect to MongoDB")
        return
    # cursor to spcified database; create if it doesn't exist
    dbs=client["MetadataDatabase"]
    # cursor to specified collection; create if it doesn't exist
    md=dbs["MetaData"]
    # store metadate from api as json
    data=r.json()
    # find relevant data in nested dictionary
    data=data.get("message").get("items")
    # store data in collection
    md.insert_many(data)

if __name__=='__main__':
    storeMetaDatainMongoDB()
