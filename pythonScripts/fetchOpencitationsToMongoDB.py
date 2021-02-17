# author: rihat rahman
# inserts a sample from OpenCitations into MongoDB
# Lines 1-24
#-------------------------------------------------------------
import requests
import pymongo

# connect to MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# create database
citationsDatabase = myclient["cDatabase"]

# create collections
citations = citationsDatabase["citations"]

# get sample data from OpenCitations
response = requests.get('https://w3id.org/oc/index/api/v1/citations/10.1002/adfm.201505328')

# insert data
insertion = citations.insert_many(response.json())

# print id's of documents that were inserted
print(insertion.inserted_ids)
#-------------------------------------------------------------