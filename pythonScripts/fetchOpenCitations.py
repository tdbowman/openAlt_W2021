# author: Rihat Rahman
# Lines 1-159
# Script to fetch citation and reference data from OpenCitations and call ingest scripts to ingest data into MySQL
#-------------------------------------------------------------
import json
import requests
import pymongo
import mysql.connector
from ingestCitations import ingestCitations
from ingestCitationCounts import ingestCitationCounts
from ingestReferenceCounts import ingestReferenceCounts
from ingestReferences import ingestReferences


def fetchDOICitations ():
    # mysql credentials
    mysql_username ='root'
    mysql_password = 'Dsus1209.'

    # connect to doi database
    drBowmanDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "dr_bowman_doi_data_tables")
    drBowmanDatabaseCursor = drBowmanDatabase.cursor()

    # connect to OpenCitations database
    openCitationsDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "opencitations")
    openCitationsCursor = openCitationsDatabase.cursor()

    # get list of DOIs from doi database
    drBowmanDatabaseCursor.execute("Select DOI FROM _main_ WHERE DOI IS NOT NULL")
    articles = drBowmanDatabaseCursor.fetchall()
    
    # connect to MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    # MongoDB database to store citation and reference information
    citationsDatabase = myclient["OpenCitations"]

    for article in articles:

        # fetch citation data into MongoDB (one article at a time)
        fetchCitationData(article[0], openCitationsCursor, citationsDatabase, openCitationsDatabase)

        # fetch reference data into MongoDB (one article at a time)
        fetchReferenceData(article[0], openCitationsCursor, citationsDatabase, openCitationsDatabase)
        


# function to fetch citation data and call citation ingest scripts
def fetchCitationData (doi, openCitationsCursor, citationsDatabase, openCitationsDatabase):

    # collection to store citations
    citationCollections = citationsDatabase["citations"]
    
    # citation count (total number of publications that cited this DOI)
    citationCountsResponse = requests.get('https://w3id.org/oc/index/api/v1/citation-count/' + doi)
    citationCountsJSON = citationCountsResponse.json()

    # ingest citation count data into MySQL
    need_to_update_citations = ingestCitationCounts(doi, openCitationsCursor, citationCountsJSON, openCitationsDatabase)

    if need_to_update_citations == False:
        return

    # get list of citations that already exist in MySQL
    openCitationsCursor.execute("Select oci FROM citations WHERE cited = 'coci => " + doi + "'")
    citationsOCI = openCitationsCursor.fetchall()

    # dictionary
    listOfOCIs = {}

    for oci in citationsOCI:
        listOfOCIs[oci[0]] = None

    # citations (list of publications that cited this DOI)
    citationResponse = requests.get('https://w3id.org/oc/index/api/v1/citations/' + doi)
    citationsJSON = citationResponse.json()

    # JSON file 
    cJSON = []
    
    # check if any of the fetched citations already exist in MySQL
    # If not insert into MongoDB
    for citation in citationsJSON:

        if citation['oci'] not in listOfOCIs:
            cJSON.append(citation)


    try:
        # insert citation data into MongoDB
        if cJSON != []:
            citationCollections.insert_many(cJSON)

    except:
        print('ERROR: DOI: ' + doi + ' citation data was not inserted')

    # filter citation data and ingest into MySQL
    ingestCitations(doi, openCitationsCursor, citationCollections, openCitationsDatabase)

    # delete MongoDB buffer collection
    citationCollections.delete_many({})



# function to fetch reference data and call citation ingest scripts
def fetchReferenceData (doi, openCitationsCursor, citationsDatabase, openCitationsDatabase):

    # MongoDB collection to store reference data
    referenceCollections = citationsDatabase["references"]

    # reference count (total number of publications referenced by this DOI)
    referenceCountsResponse = requests.get('https://w3id.org/oc/index/api/v1/reference-count/' + doi)
    referenceCountsJson = referenceCountsResponse.json()

    # ingest reference count data into MySQL
    need_to_update_references = ingestReferenceCounts(doi, openCitationsCursor, referenceCountsJson, openCitationsDatabase)

    if need_to_update_references == False:
        return


    # get list of references that already exist in MySQL
    openCitationsCursor.execute("Select oci FROM ref WHERE citing = 'coci => " + doi + "'")
    referencesOCI = openCitationsCursor.fetchall()

    # dictionary
    listOfOCIs = {}

    for oci in referencesOCI:
        listOfOCIs[oci[0]] = None

    # citations (list of publications that cited this DOI)
    # doi = '10.1002/adfm.201505328'
    referenceResponse = requests.get('https://w3id.org/oc/index/api/v1/references/' + doi)
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
    
    fetchDOICitations()
#-------------------------------------------------------------