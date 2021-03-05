# Tabish's work
import pymongo
import requests

def storeMetaDatainMongoDB(DOI):
    # retrieve metadata from api
    r = requests.get('https://api.crossref.org/works/'+ DOI)
    # connect to localhost MongoDB
    try:
        client = pymongo.MongoClient('mongodb://localhost:27017/')
    except:
        print("Could not connect to MongoDB")
        return
    # cursor to spcified database; create if it doesn't exist
    dbs=client["MetadataDatabase"]
    # cursor to specified collection; create if it doesn't exist
    coll=dbs["MetaData"]
    data=r.json()
    if data.get("message-type")=="work":
        coll.insert_one(data)
    else:
        print("Invalid data")
    return DOI

if __name__=='__main__':
    # Contains placeholder string
    storeMetaDatainMongoDB("10.1093/jn/128.10.1731")
