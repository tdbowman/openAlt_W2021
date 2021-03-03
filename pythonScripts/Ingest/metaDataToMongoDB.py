# Tabish's work
import pymongo
import requests

def storeMetaDatainMongoDB():
    # retrieve metadata from api
    r = requests.get('https://api.crossref.org/works?sample=100&mailto=tabishshaikh97@gmail.com')
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
    print(type(data))
    print(data.get("message-type"))
    if data.get("message-type")=="work-list":
        check(coll, data.get("message").get("items"))
    else:
        print("Invalid data")

def check(coll, li):
    for i in li:
        dupe=False
        x=coll.find({})
        for y in x:
            if i.get("DOI")==y.get("DOI"):
                print("Duplicate")
                dupe=True
        if dupe==False:
            coll.insert_one(i)
    return

if __name__=='__main__':
    storeMetaDatainMongoDB()
