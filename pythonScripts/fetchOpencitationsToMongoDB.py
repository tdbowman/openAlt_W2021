import json
import requests
import pymongo
import mysql.connector


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

    for article in articles:
        fetchCitationData(article[0], openCitationsCursor)



def fetchCitationData (doi, openCitationsCursor):

    # connect to MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    # database
    citationsDatabase = myclient["cDatabase"]

    # collections
    citationCollections = citationsDatabase["citations"]
    citationCountCollections = citationsDatabase["citation_counts"]
    referenceCollections = citationsDatabase["references"]
    referenceCountsCollections = citationsDatabase["reference_counts"]





    # get list of citations that already exist in MySQL
    openCitationsCursor.execute("Select oci FROM citations WHERE cited = '" + doi + "'")
    citationsOCI = openCitationsCursor.fetchall()


    listOfOCIs = []

    for oci in citationsOCI:
        listOfOCIs.append(oci[0])

    # citations (list of publications that cited this DOI)
    doi = '10.1002/adfm.201505328'
    citationResponse = requests.get('https://w3id.org/oc/index/api/v1/citations/' + doi)
    citationsJSON = citationResponse.json()
    print(citationsJSON)

    # check if any of the fetched citations already exist in MySQL
    # If not insert into MongoDB
    for citation in citationsJSON:
        if citation['oci'] in listOfOCIs:
            citationsJSON.remove(citation)

    citationCollections.insert_many(citationsJSON)



    # citation count (total number of publications that cited this DOI)
    citationCountsResponse = requests.get('https://opencitations.net/index/croci/api/v1/citation-count/' + doi)
    citationCountsJSON = citationCountsResponse.json()



    openCitationsCursor.execute("Select oci FROM ref WHERE citing = '" + doi + "'")
    referencesOCI = openCitationsCursor.fetchall()

    # references (list of publications referenced by this DOI)
    referenceResponse = requests.get('https://w3id.org/oc/index/api/v1/references/' + doi)
    referencesJSON = referenceResponse.json()

    for reference in referencesJSON:
        if reference['oci'] in referencesOCI:
            referencesJSON.remove(reference)

    referenceCollections.insert_many(referencesJSON)
    


    # reference count (total number of publications referenced by this DOI)
    referenceCountsResponse = requests.get('https://opencitations.net/index/croci/api/v1/reference-count/' + doi)
    referenceCountsJson = referenceCountsResponse.json()
            


if __name__ == '__main__':
    
    # mysql credentials
    mysql_username ='root'
    mysql_password = 'Dsus1209.'


    openCitationsDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "opencitations")

    openCitationsCursor = openCitationsDatabase.cursor()

    fetchCitationData('10.1002/adfm.201505328', openCitationsCursor)
