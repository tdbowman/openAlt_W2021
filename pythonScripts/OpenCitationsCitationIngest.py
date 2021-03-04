import os
import platform
import pandas as pd
import logging
import mysql.connector
import getpass

#Author: 
    #Name: Mohammad Tahmid 
    #Lines 1-113
    #---------------------
#Date: 01/31/2021
#Description: Takes in citation JSON from the OPenCitations API to be filtered and then later inserted into the citations database.

def OCCitationIngest(connection, cursor, doi, citationData, citationCount):

    #Log file name can be set here
    logFile = 'OpenCitationsCitationIngest_log.log'

    #Log file size is set in MB
    LogFileSizeLimit = 100

    try:
        #The log file size is checked 
        logFileSize = os.path.getsize(logFile)

        if logFileSize > (LogFileSizeLimit * 1024):

            #File if deleted if it is over the size limit
            os.remove(logFile)
    except FileNotFoundError:
        print("Log not found, will be created")
        
    #Creation of log file for the citations code to allow for troubleshooting later on
    logging.basicConfig(filename=logFile, filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

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
    
    OCCitationCountIngest(connection, cursor, doi, citationCount)

def OCCitationCountIngest(connection, cursor, doi, citationCount):

    #Check database to see if the citation count exists already and if it does, what is the value and does it need to be updated
    query = """SELECT count(*), count FROM opencitations.citation_count WHERE doi = '%s'""" % (doi)
    cursor.execute(query)
    resultSet = cursor.fetchall()

    #Result is the count of rows 
    count = resultSet[0][0]

    #Result is the actual count value from the count column if it already exists
    DBCitationCount = resultSet[0][1]

    #If a entry for the doi does not exist then one is made and the citation count is added to the database
    if not count > 0:

        query = "INSERT IGNORE INTO opencitations.citation_count(doi, count) VALUES (%s, %s)"
        queryValues = (doi, citationCount)
        cursor.execute(query, queryValues)
        connection.commit()
        logging.info("DOI: " + doi + " Citation Count Added: " + str(citationCount))

    #If the entry already exists then it is checked to see if it is the same, if it is not then the citation count value is updated
    elif DBCitationCount != citationCount:

        query = """UPDATE opencitations.citation_count SET count = '%s'  WHERE doi = '%s'""" % (citationCount, doi)
        cursor.execute(query)
        connection.commit()  
        logging.info("DOI: " + doi + " Citation Count Modified: " + str(citationCount))