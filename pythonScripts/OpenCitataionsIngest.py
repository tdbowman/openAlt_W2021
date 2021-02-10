import os
import platform
import pandas as pd
import logging
import mysql.connector
import getpass

def OCIngest(connection, cursor, doi, jsonData):

    logging.basicConfig(filename='OpenCitationsIngest_log.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    #Query to get the foreign key when looking up a DOI
    query = ""
    cursor.execute(query)
    resultSet = cursor.fetchall()
    fk = resultSet[0][0]

    filePath = os.path.realpath(__file__)
    directoryName = os.path.dirname(filePath)
    fullPath = os.path.join(directoryName, "OCSample.JSON")

    dataSet = pd.read_json(fullPath)
    rowCount = len(dataSet.index)

    for index in range(rowCount):
        print(dataSet['citing'][index])
        print(dataSet['creation'][index])
        print(dataSet['timespan'][index])
        print("\n")

    query = """""" % ()
    cursor.execute(query)
    resultSet = cursor.fetchall()
    count = resultSet[0][0]

    if not count > 0:

        #Query the database to insert the values as a row into the table
        query = ""
        queryValues = "" 
        cursor.execute(query, queryValues)
        connection.commit()
        logging.info(" ")

