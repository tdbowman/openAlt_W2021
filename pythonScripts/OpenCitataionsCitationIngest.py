import os
import platform
import pandas as pd
import logging
import mysql.connector
import getpass

#Author: Mohammad Tahmid
#Date: 01/31/2021
#Lines: 1-65
#Description: Takes in JSON from the OPenCitations API to be filtered and then later inserted into the citations database.
#UPDATE: This is during the beginning of version 2.0 of the project that was replaced later on in the development of this project. This placed data in directly into the MySQL database instead of filtering into MongoDB first

def OCIngest(connection, cursor, doi, jsonData):

    #Creation of log file for the citations code to allow for troubleshooting later on
    logging.basicConfig(filename='OpenCitationsIngest_log.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    #Query to get the foreign key when looking up a DOI
    query = ""
    
    cursor.execute(query)
    resultSet = cursor.fetchall()
    fk = resultSet[0][0]

    #Creation of file path to look at list of OpenCitations info to filter through
    filePath = os.path.realpath(__file__)
    directoryName = os.path.dirname(filePath)

    #Command used to create full file path, moduele will handle the correct seperator for the OS
    fullPath = os.path.join(directoryName, "OCSample.JSON")

    #Using panda's modile to load JSON information to work on being able to parse through it
    dataSet = pd.read_json(fullPath)
    rowCount = len(dataSet.index)

    for index in range(rowCount):
        #print(dataSet['citing'][index])
        #print(dataSet['creation'][index])
        #print(dataSet['timespan'][index])
        #print("\n")

    #Query to database to see if the infomraiton already exists before inserting
    query = """""" % ()

    cursor.execute(query)
    resultSet = cursor.fetchall()

    count = resultSet[0][0]

    #Insert query to database to insert the information to the appropriate table
    if not count > 0:

        # TODO: Query to insert to databse will need to added in after the schema is created
        #Query the database to insert the values as a row into the table
        query = ""
        queryValues = "" 

        cursor.execute(query, queryValues)
        connection.commit()

        # TODO: Logging comment will need to added here but at a later date when doing bug testing
        logging.info(" ")

