import pymongo
import os
import pandas
import json
import requests
import mysql.connector

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
    drBowmanDatabaseCursor = drBowmanDatabase.cursor()

    drBowmanDatabaseCursor.execute("Select DOI FROM _main_ WHERE DOI IS NOT NULL")

    articles = drBowmanDatabaseCursor.fetchall()
    print(articles)

def main():
    dbs=client.list_database_names()
    if client==pymongo.MongoClient('mongodb://localhost:27017/'):
        print(dbs)



if __name__=='__main__':
    fetch()
    main()
