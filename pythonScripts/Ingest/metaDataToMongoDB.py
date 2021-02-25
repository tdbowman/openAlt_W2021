# Tabish's work
import pymongo
import requests

def storeMetaDatainMongoDB():
    # hard code for testing; change later
    # retrieve metadata from api
    r = requests.get('https://api.crossref.org/works?sample=5&mailto=tabishshaikh97@gmail.com')
    q = requests.get('https://api.crossref.org/works/10.1192/bjp.171.6.519')
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
    data1=r.json()
    md.insert(data1)
    data2=q.json()
    md.insert(data2)

if __name__=='__main__':
    storeMetaDatainMongoDB()
