# author: Rihat Rahman
# This script will fetch citation data from OpenCitations API
import mysql.connector
import requests
import json
from OpenCitataionsIngest import OCIngest

def getCitationData(mysql_username, mysql_password):

    try:
        # connect to dr_bowman_doi_data_tables database
        drBowmanDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "dr_bowman_doi_data_tables")

        # connect to citatons database
        citationDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "opencitations")

    except:
        print("Error: Invalid MySQL credentials")

    drBowmanDatabaseCursor = drBowmanDatabase.cursor()
    openCitationsCursor = citationDatabase.cursor()

    drBowmanDatabaseCursor.execute("Select DOI FROM _main_")
    articles = drBowmanDatabaseCursor.fetchall()

    emptyDOI = (None, )

    # To fetch citation data for all articles, set numberOfArticlesToFetch = articles.length
    numberOfArticlesToFetch = 500 

    for i in range(numberOfArticlesToFetch):

        if (articles[i] != emptyDOI):

            article = articles[i]
            articleDOI = article[0]

            citationResponse = requests.get('https://opencitations.net/index/croci/api/v1/citations/' + articleDOI)
            citationCountsResponse = requests.get('https://opencitations.net/index/croci/api/v1/citation-count/' + articleDOI)

            citationsJSON = citationResponse.json()
            countJSON = citationCountsResponse.json()

            if response.json() != []:

                # Passing data to ingest script
                OCIngest(citationDatabase, openCitationsCursor, articleDOI, citationsJSON, countJSON)
                

if __name__ == '__main__':

    print("MySQL Credentials")
    mysql_username = input("Username: ")
    mysql_password = input("Password: ")
    getCitationData(mysql_username, mysql_password)