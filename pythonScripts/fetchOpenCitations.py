# author: Rihat Rahman
# Lines 1-111
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


    drBowmanDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "dr_bowman_doi_data_tables")
    openCitationsDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "opencitations")

    drBowmanDatabaseCursor = drBowmanDatabase.cursor()
    openCitationsCursor = openCitationsDatabase.cursor()

    drBowmanDatabaseCursor.execute("Select DOI FROM _main_ WHERE DOI IS NOT NULL")
    articles = drBowmanDatabaseCursor.fetchall()

    
    # connect to MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    # database
    citationsDatabase = myclient["cDatabase"]


    i = 0
    for article in articles:

        # fetch data into MongoDB
        fetchCitationData(article[0], openCitationsCursor, citationsDatabase, openCitationsDatabase)
        fetchReferenceData(article[0], openCitationsCursor, citationsDatabase, openCitationsDatabase)
        print(i)
        i = i + 1
        

    



def fetchCitationData (doi, openCitationsCursor, citationsDatabase, openCitationsDatabase):

    # collections
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


    listOfOCIs = []

    for oci in citationsOCI:
        listOfOCIs.append(oci[0])

    # citations (list of publications that cited this DOI)
    # doi = '10.1002/adfm.201505328'
    citationResponse = requests.get('https://w3id.org/oc/index/api/v1/citations/' + doi)
    citationsJSON = citationResponse.json()

    cJSON = []
    

    # check if any of the fetched citations already exist in MySQL
    # If not insert into MongoDB
    for citation in citationsJSON:

        if citation['oci'] in listOfOCIs:
            citationsJSON.remove(citation)
            
        else:
            cJSON.append(citation)



    if cJSON != []:
        citationCollections.insert_many(cJSON)

    # filter citation data and ingest into MySQL
    ingestCitations(doi, openCitationsCursor, citationCollections, openCitationsDatabase)


    citationCollections.delete_many({})



def fetchReferenceData (doi, openCitationsCursor, citationsDatabase, openCitationsDatabase):

    referenceCollections = citationsDatabase["references"]


    # reference count (total number of publications referenced by this DOI)
    referenceCountsResponse = requests.get('https://w3id.org/oc/index/api/v1/reference-count/' + doi)
    referenceCountsJson = referenceCountsResponse.json()

    # ingest reference count data into MySQL
    need_to_update_references = ingestReferenceCounts(doi, openCitationsCursor, referenceCountsJson, openCitationsDatabase)

    

    if need_to_update_references == False:
        print('here')
        return



    # get list of references that already exist in MySQL
    openCitationsCursor.execute("Select oci FROM ref WHERE citing = 'coci => " + doi + "'")
    referencesOCI = openCitationsCursor.fetchall()

    

    listOfOCIs = []

    for oci in referencesOCI:
        listOfOCIs.append(oci[0])

    # citations (list of publications that cited this DOI)
    # doi = '10.1002/adfm.201505328'
    referenceResponse = requests.get('https://w3id.org/oc/index/api/v1/references/' + doi)
    referencesJSON = referenceResponse.json()

    rJSON = []
    

    # check if any of the fetched citations already exist in MySQL
    # If not insert into MongoDB
    for reference in referencesJSON:

        if reference['oci'] in listOfOCIs:
            referencesJSON.remove(reference)
            
        else:
            rJSON.append(reference)



    if rJSON != []:
        referenceCollections.insert_many(rJSON)

    # filter citation data and ingest into MySQL
    ingestReferences(doi, openCitationsCursor, referenceCollections, openCitationsDatabase)


    referenceCollections.delete_many({})




            


if __name__ == '__main__':

    # mysql credentials
    mysql_username ='root'
    mysql_password = 'Dsus1209.'

    openCitationsDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "opencitations")

    openCitationsCursor = openCitationsDatabase.cursor()

    # connect to MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    # database
    citationsDatabase = myclient["cDatabase"]

    fetchReferenceData('10.1186/1756-8722-6-59', openCitationsCursor, citationsDatabase, openCitationsDatabase)

    # fetchDOICitations()
#-------------------------------------------------------------