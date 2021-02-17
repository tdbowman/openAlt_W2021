import os
import platform
import pandas as pd
import logging
import mysql.connector
import getpass

#Author: 
    #Name: Mohammad Tahmid 
    #Lines 1-64
    #---------------------
#Date: 01/31/2021
#Description: Takes in citation JSON from the OPenCitations API to be filtered and then later inserted into the citations database.

def OCCitationIngest(connection, cursor, doi, citationData, citationCount):

    #Creation of log file for the citations code to allow for troubleshooting later on
    logging.basicConfig(filename='OpenCitationsCitationIngest_log.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    #Creation of variables to stop any errors where a variable is not declared if empty
    OCINumber = ""
    creation = ""
    cited = ""
    author_sc = ""
    journal_sc = ""
    timespan = ""
    citing = ""

    #Getting count from the pandas table that has the JSON information in a pandas object
    rowCount = len(citationData.index)

    #For each citation the data is extracted and will be placed into the database
    for index in range(rowCount):

        OCINumber = citationData['oci'][index]
        creation = citationData['creation'][index]
        cited = citationData['cited'][index]
        author_sc = citationData['author_sc'][index]
        journal_sc = citationData['journal_sc'][index]
        timespan = citationData['timespan'][index]
        citing = citationData['citing'][index]

        #TODO: Is count in the main table or in a seperate table?, If it is in the main table there will be a lot of duplicate values in the column.

        #Query to database to see if the infomraiton already exists before inserting
        query = """SELECT count(*) FROM opencitations.citation WHERE 
            oci = '%s' AND 
            citing = '%s' AND
            cited = '%s' AND
            creation = '%s' AND
            timespan = '%s' AND 
            journal_sc = '%s' AND 
            author_sc = '%s'""" % (OCINumber, citing, cited, creation, timespan, journal_sc, author_sc)
        cursor.execute(query)
        resultSet = cursor.fetchall()
        count = resultSet[0][0]

        if not count > 0:
            #Query the database to insert the values as a row into the table
            query = "INSERT IGNORE INTO opencitations.citation(oci, citing, cited, creation, timespan, journal_sc, author_sc) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            queryValues = (OCINumber, citing, cited, creation, timespan, journal_sc, author_sc)
            cursor.execute(query, queryValues)
            connection.commit()
            logging.info("DOI: " + cited + " Cited By: " + citing)