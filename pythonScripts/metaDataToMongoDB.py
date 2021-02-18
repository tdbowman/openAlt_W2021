import pymongo
import os
import pandas
import json
import requests
import mysql.connector
import urllib
client=pymongo.MongoClient('mongodb://localhost:27017/')

def fetch():
    print("MySQL Credentials")
    mysql_username = "root"
    mysql_password = "pass"
    try:
        drBowmanDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "dr_bowman_doi_data_tables")
    except:
        print("Error: Invalid MySQL credentials")
        return
    print ("Connected to the database...")

def main():
    dbs=client.local
    if dbs==client.local:
        print(dbs)
    opener = urllib.request.build_opener()
    opener.addheaders = [('Accept', 'application/vnd.crossref.unixsd+xml')]
    r = opener.open('http://dx.doi.org/10.5555/515151')
    print (r.info()['Link'])


if __name__=='__main__':
    fetch()
    main()
