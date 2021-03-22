# author: Rihat Rahman
# Lines: 1-54
# script to ingest citations from MongoDB to MySQL
#-------------------------------------------------------------
import pymongo
import mysql.connector

def ingestCitations(doi, openCitationsCursor, citationCollections, openCitationsDatabase):


    # retrieve list of citations from MongoDB buffer database
    listOfCitations = citationCollections.find()

    for citation in listOfCitations:

        creation = None
        oci = None
        author_sc = None
        citing = None
        timespan = None
        cited = None
        journal_sc = None

        for key, value in citation.items():

            if key == 'oci':
                oci = value[8:]

            elif key == 'citing':
                citing = value[8:]

            elif key == 'cited':
                cited = value[8:]

            elif key == 'creation':
                creation = value [8:]

            # TODO: change time format
            elif timespan == 'timespan':
                timespan = value[8:]

            elif journal_sc == 'journal_sc':
                journal_sc = value[8:]

            elif key == 'author_sc':
                author_sc = value[8:]

        # query to insert citation data into MySQL
        query = ("Insert IGNORE INTO opencitations.citations " " (oci, citing, cited, creation, timespan, journal_sc, author_sc) " " VALUES (%s,%s,%s,%s,%s,%s,%s)")
        data = (oci, citing, cited, creation, timespan, journal_sc, author_sc)

        openCitationsCursor.execute(query, data)
        openCitationsDatabase.commit()
#-------------------------------------------------------------