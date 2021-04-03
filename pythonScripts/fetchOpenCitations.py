# author: Rihat Rahman
# Lines 1-159
# Script to fetch citation and reference data from OpenCitations and call ingest scripts to ingest data into MySQL
#-------------------------------------------------------------
import os
import json
import time
import requests
import pymongo
import configparser
import mysql.connector
from ingestCitations import ingestCitations
from ingestCitationCounts import ingestCitationCounts
from ingestReferenceCounts import ingestReferenceCounts
from ingestReferences import ingestReferences
import os
import json



def fetchDOICitations (APP_CONFIG):


    mysql_username = APP_CONFIG['DOI-Database']['username']
    mysql_password = APP_CONFIG['DOI-Database']['password']
    doi_database_name = APP_CONFIG['DOI-Database']['name']
    opencitations_name = APP_CONFIG['OpenCitations']['name']
    MongoDBClient = APP_CONFIG['OpenCitations']['address']


    # connect to doi database
    drBowmanDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = doi_database_name)
    drBowmanDatabaseCursor = drBowmanDatabase.cursor()

    # connect to OpenCitations database
    openCitationsDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = opencitations_name)
    openCitationsCursor = openCitationsDatabase.cursor()

    # get list of DOIs from doi database
    drBowmanDatabaseCursor.execute("Select DOI FROM doidata._main_ WHERE DOI IS NOT NULL")
    articles = drBowmanDatabaseCursor.fetchall()
    # articles = drBowmanDatabaseCursor.fetchmany(5)
    
    # connect to MongoDB
    myclient = pymongo.MongoClient(MongoDBClient)

    # MongoDB database to store citation and reference information
    citationsDatabase = myclient[opencitations_name]

    count = 0

    f = open("citation_ingest_runtime_log.txt", "a")

    startTime = time.time()

    for article in articles:

        
        
        count = count + 1
        print(str(count) + "/" + str(len(articles)))



        # fetch citation data into MongoDB (one article at a time)
        fetchCitationData(article[0], openCitationsCursor, citationsDatabase, openCitationsDatabase, APP_CONFIG)

        # fetch reference data into MongoDB (one article at a time)
        # fetchReferenceData(article[0], openCitationsCursor, citationsDatabase, openCitationsDatabase, APP_CONFIG)

        print(article)


        if count == 10:
            executionTime = (time.time() - startTime)
            f.write('Number of DOIs: ' + str(count) + '      Time: ' + str(executionTime) + '\n')

        if count % 100 == 0:
            executionTime = (time.time() - startTime)
            f.write('Number of DOIs: ' + str(count) + '      Time: ' + str(executionTime) + '\n')

    f.close()
    print("Successfully fectched and ingested citation data!")


# function to fetch citation data and call citation ingest scripts
def fetchCitationData (doi, openCitationsCursor, citationsDatabase, openCitationsDatabase, APP_CONFIG):

    citation_collections = APP_CONFIG['MongoDB-OpenCitations-Database']['citation_collection']

    # collection to store citations
    citationCollections = citationsDatabase[citation_collections]


    openCitationsCitationCountAPI = APP_CONFIG['OpenCitations-Citation-Count-API']['url']


    try:
    
        # citation count (total number of publications that cited this DOI)
        citationCountsResponse = requests.get(openCitationsCitationCountAPI + doi)
        citationCountsJSON = citationCountsResponse.json()

    except:
        print('OpenCitations Citation Count API call unsuccessful...')

    # ingest citation count data into MySQL
    need_to_update_citations = ingestCitationCounts(doi, openCitationsCursor, citationCountsJSON, openCitationsDatabase)

    if need_to_update_citations == False:
        return

    # get list of citations that already exist in MySQL
    openCitationsCursor.execute("Select oci FROM opencitations.citations WHERE cited = 'coci => " + doi + "'")
    citationsOCI = openCitationsCursor.fetchall()

    # dictionary
    listOfOCIs = {}

    for oci in citationsOCI:
        listOfOCIs[oci[0]] = None


    openCitationsCitationAPI = APP_CONFIG['OpenCitations-Citation-API']['url']

    try:

        # citations (list of publications that cited this DOI)
        citationResponse = requests.get(openCitationsCitationAPI + doi)
        citationsJSON = citationResponse.json()

        # JSON file 
        cJSON = []


    except:
        print('OpenCitations Citations API call unsuccessful...')


    
    # check if any of the fetched citations already exist in MySQL
    # If not insert into MongoDB
    for citation in citationsJSON:

        if citation['oci'] not in listOfOCIs:
            cJSON.append(citation)


    try:
        # insert citation data into MongoDB
        if cJSON != []:
            citationCollections.delete_many({})
            citationCollections.insert_many(cJSON)

    except:
        print(cJSON)
        print('ERROR: DOI: ' + doi + ' citation data was not inserted')

    # filter citation data and ingest into MySQL
    ingestCitations(doi, openCitationsCursor, citationCollections, openCitationsDatabase)

    # delete MongoDB buffer collection
    citationCollections.delete_many({})



# function to fetch reference data and call citation ingest scripts
def fetchReferenceData (doi, openCitationsCursor, citationsDatabase, openCitationsDatabase, APP_CONFIG):

    reference_collections = APP_CONFIG['MongoDB-OpenCitations-Database']['reference_collection']

    # MongoDB collection to store reference data
    referenceCollections = citationsDatabase[reference_collections]

    openCitationsReferenceCountsAPI = APP_CONFIG['OpenCitations-Reference-Count-API']['url']
    openCitationsReferenceAPI = APP_CONFIG['OpenCitations-Reference-API']['url']

    # reference count (total number of publications referenced by this DOI)
    referenceCountsResponse = requests.get(openCitationsReferenceCountsAPI + doi)
    referenceCountsJson = referenceCountsResponse.json()

    # ingest reference count data into MySQL
    need_to_update_references = ingestReferenceCounts(doi, openCitationsCursor, referenceCountsJson, openCitationsDatabase)

    if need_to_update_references == False:
        return


    # get list of references that already exist in MySQL
    openCitationsCursor.execute("Select oci FROM opencitations.ref WHERE citing = 'coci => " + doi + "'")
    referencesOCI = openCitationsCursor.fetchall()

    # dictionary
    listOfOCIs = {}

    for oci in referencesOCI:
        listOfOCIs[oci[0]] = None

    # citations (list of publications that cited this DOI)
    # doi = '10.1002/adfm.201505328'
    referenceResponse = requests.get(openCitationsReferenceAPI + doi)
    referencesJSON = referenceResponse.json()

    rJSON = []

    # check if any of the fetched citations already exist in MySQL
    # If not insert into MongoDB
    for reference in referencesJSON:

        if reference['oci'] not in listOfOCIs:
            rJSON.append(reference)


    if rJSON != []:
        referenceCollections.insert_many(rJSON)

    # filter citation data and ingest into MySQL
    ingestReferences(doi, openCitationsCursor, referenceCollections, openCitationsDatabase)

    # delete MongoDB buffer collection for references
    referenceCollections.delete_many({})



if __name__ == '__main__':
    
    # current directory 
    path = os.getcwd() 
    
    # parent directory 
    parent = os.path.dirname(path) 
    config_path = os.path.join(parent, "openAlt_W2021\\config", "openAltConfig.json")

    # config file
    f = open(config_path)
    APP_CONFIG = json.load(f)

    fetchDOICitations(APP_CONFIG)
#-------------------------------------------------------------