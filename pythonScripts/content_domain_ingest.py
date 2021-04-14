import os
import json
import time
import crossref
import requests
import pymongo
import configparser
import mysql.connector
import os
import json

def fetch_conten_domain (APP_CONFIG):

    mysql_username = APP_CONFIG['DOI-Database']['username']
    mysql_password = APP_CONFIG['DOI-Database']['password']
    doi_database_name = APP_CONFIG['DOI-Database']['name']


    # connect to doi database
    drBowmanDatabase = mysql.connector.connect(host = "localhost", user = 'root', passwd = 'Dsus1209.', database = doi_database_name)
    drBowmanDatabaseCursor = drBowmanDatabase.cursor()



    # get list of DOIs from doi database
    drBowmanDatabaseCursor.execute("Select DOI, fk FROM doidata._main_ WHERE DOI IS NOT NULL")
    articles = drBowmanDatabaseCursor.fetchall()
    # articles = drBowmanDatabaseCursor.fetchmany(5)
    

    count = 0


    for article in articles:

        doi = article[0]
        fk = article[1]
        count = count + 1
        print(str(count) + "/" + str(len(articles)))


        # print(article)

        from crossref.restful import Works
        works = Works()
        data = works.doi(doi)
        domainData = data['content-domain']
        domain = domainData['domain']
        # print(domain)
        ingest_content_domain(APP_CONFIG, drBowmanDatabase, drBowmanDatabaseCursor, domainData, doi, fk)
        
        


def ingest_content_domain(APP_CONFIG, drBowmanDatabase, drBowmanDatabaseCursor, data, doi, fk):


    crossmark_restriction = data['crossmark-restriction']
    domain = data['domain']

    
    if domain != []:
        print(domain[0])
        query = "INSERT IGNORE INTO doidata.content_domain(crossmark_restriction, domain, fk) VALUES ( " +  str(crossmark_restriction) + ",'" +  domain[0] + "',"  + str(fk) + ")"
        print(query)
        
        drBowmanDatabaseCursor.execute(query)
        drBowmanDatabase.commit()





if __name__ == '__main__':

    # current directory 
    path = os.getcwd() 

    # parent directory 
    parent = os.path.dirname(path) 
    config_path = os.path.join(parent, "config", "openAltConfig.json")

    # config file
    f = open(config_path)
    APP_CONFIG = json.load(f)



    fetch_conten_domain(APP_CONFIG)