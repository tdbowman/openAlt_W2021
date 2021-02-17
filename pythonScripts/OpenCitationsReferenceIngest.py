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
#Date: 02/16/2021
#Description: Takes in reference JSON from the OpenCitations API to be filtered and then later inserted into the citations database.

def OCReferenceIngest(connection, cursor, doi, referenceData, referenceCount):\

    #Creation of log file for the citations code to allow for troubleshooting later on
    logging.basicConfig(filename='OpenCitationsReferenceIngest_log.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    #Creation of variables to stop any errors where a variable is not declared if empty
    OCINumber = ""
    creation = ""
    cited = ""
    author_sc = ""
    journal_sc = ""
    timespan = ""
    citing = ""

    #Getting count from the pandas table that has the JSON information in a pandas object
    rowCount = len(referenceData.index)

    #For each citation the data is extracted and will be placed into the database
    for index in range(rowCount):

        OCINumber = referenceData['oci'][index]
        creation = referenceData['creation'][index]
        cited = referenceData['cited'][index]
        author_sc = referenceData['author_sc'][index]
        journal_sc = referenceData['journal_sc'][index]
        timespan = referenceData['timespan'][index]
        citing = referenceData['citing'][index]

        #TODO: Is count in the main table or in a seperate table?, If it is in the main table there will be a lot of duplicate values in the column.

        #Query to database to see if the infomraiton already exists before inserting
        query = """SELECT count(*) FROM opencitations.reference WHERE 
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
            query = "INSERT IGNORE INTO opencitations.reference(oci, citing, cited, creation, timespan, journal_sc, author_sc) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            queryValues = (OCINumber, citing, cited, creation, timespan, journal_sc, author_sc)
            cursor.execute(query, queryValues)
            connection.commit()
            logging.info("DOI: " + cited + " Cited By: " + citing)