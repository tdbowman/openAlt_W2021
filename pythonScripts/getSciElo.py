"""
MIT License

Copyright (c) 2020 tdbowman-CompSci-F2020

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import json
import requests
import pymongo
import mysql.connector
import logging
import pandas as pd
import numpy as np

from crossref.restful import Works
from csv import reader
from getSciELOIngest import PIDtoDOIInsertSQL


# Author: Mohammad Tahmid
# Date: 03/10/2021
# Lines: 1-321
# Description: This python script takes in PIDs and converts them into DOIs. Then the DOI is put through the Crossref Data API and placed into MongoDB for filtering.


def getSciELOPID():

    # Configuration file is accessed to get values set by administrator to run script
    try:
        configFilePath = str(os.path.dirname(
            os.path.dirname(os.path.realpath(__file__))))
        configFilePath = os.path.join(
            configFilePath, "config", "openAltConfig.json")
        configFile = pd.read_json(configFilePath)
    except:
        logging.info("Configuration file \"openAltConfig.json\" not found")
        # print("Configuration file \"openAltConfig.json\" not found")

    # --------------------------------------------------------------------------------------

    # Logs file is created if it does not exists or if it is over the limit set in the configuration file
    try:
        dir_file = str(os.path.dirname(os.path.realpath(__file__)))
        filePath = os.path.join(dir_file, "Logs")
        if not os.path.isdir(filePath):
            os.mkdir(filePath)
    except:
        logging.info("Log file not found. Log file will be created")
        # print("Log file not found. Log file will be created")

    try:

        filePath = os.path.join(filePath, "SciELOIngest.log")
        logging.basicConfig(filename=filePath, filemode='a', level=logging.INFO,
        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

        # The log file size is checked
        logFileSize = os.path.getsize(filePath)

        fileSizeLimit = int(
            configFile["SciELO-Brazil-Log"]["file_limit"]) * 10000

        if logFileSize > fileSizeLimit:

            # File if deleted if it is over the size limit
            os.remove(filePath)
            logging.basicConfig(filename=filePath, filemode='a', level=logging.INFO,
            format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    except FileNotFoundError:
        logging.info("Log not found, will be created")
        # print("Log not found, will be created")

    # --------------------------------------------------------------------------------------

    # Database connections are setup to use for the script
    # MySQL Connection is made

	# Username from the configuration for the MySQL database is retreived
    database_user = configFile["DOI-Database"]["username"]

	# Password from the configuration for the MySQL database is retreived
    database_password = configFile["DOI-Database"]["password"]

	# IP Address from the configuration for the MySQL database is retreived
    database_host = configFile["DOI-Database"]["address"]

	# Name from the configuration for the MySQL database is retreived
    database_name = configFile["DOI-Database"]["name"]

	# Connection is established and used by the script for insertion
    connection = mysql.connector.connect(user=str(database_user), password=str(
            database_password), host=database_host, database=database_name)

	# Cursor for the connection to the MySQL database
    cursor = connection.cursor()

    # --------------------------------------------------------------------------------------

    # MongoDB connection is made

	# Username from the configuration for the MongoDB database is retreived
    mongoDB_user = configFile["MongoDB-SciELO-Database"]["username"]

	# Password from the configuration for the MongoDB database is retreived
    mongoDB_password = configFile["MongoDB-SciELO-Database"]["password"]

	# IP Address from the configuration for the MongoDB database is retreived
    mongoDB_host = configFile["MongoDB-SciELO-Database"]["address"]

	# UName from the configuration for the MongoDB database is retreived
    mongoDB_name = configFile["MongoDB-SciELO-Database"]["name"]

	# Collection name from the configuration for the MongoDB database is retreived
    mongoDB_collection = configFile["MongoDB-SciELO-Database"]["collection"]

	# Connection to the MongoDB database is established
    myClient = pymongo.MongoClient(mongoDB_host)
    sciELODatabase = myClient[mongoDB_name]

	# Collection cursor for the connection made in the previous line
    sciELODatabase = sciELODatabase[mongoDB_collection]

    # --------------------------------------------------------------------------------------

    # Setup DOI code for Crossref Metadata API

	# This is the Crossred API URL
    doiURL = str(configFile["SciELO-Brazil-Data-API"]["url"])

	# This is the country code for the documents from Brazil from Crossref API
    doiCode = configFile["SciELO-Brazil-Data-API"]["url-code"]

	# Full URL and country code to check info for DOI
    doiURL = doiURL + doiCode + os.sep

    # --------------------------------------------------------------------------------------

    # Open directory that contains csv files that contain PIDs from SciELO
    try:
        pidFolder = str(os.path.dirname(os.path.realpath(__file__)))
        pidFolder = os.path.join(pidFolder, "SciELOPID")
        if not os.path.isdir(pidFolder):
            os.mkdir(pidFolder)
    except:
        logging.info("SciELO folder not found. Directory will be created")
        # print("SciELO folder not found. Directory will be created")

	# Every "CSV" file in the "../pythonScripts/SciELOPID" folder is checked for articles PIDs
    for subdir, dirs, files in os.walk(pidFolder):
        for fileName in files:

            pidFile = os.path.join(subdir, fileName)

            if pidFile.endswith(".csv"):

				# Every CSV file will run the following function to check the value and see if it exists in Crossref
                PIDtoDOICheck(connection, cursor, sciELODatabase,
                              pidFile, doiURL, doiCode,)


def PIDtoDOICheck(connection, cursor, sciEloDatabase, pidFile, doiURL, doiCode):

    DOIFullLink = str(doiURL) + str(doiCode) + "/"

	# Opens the CSV file and begins to read the cells in the CSV file
    with open(pidFile, "r") as pointer:

		# Create a reader pointer to later use to get the row count instead of reading the whole file into memory
        csvLine = reader(pointer)
        csvHeader = csvLine

		# LIMITS THE AMOUNT OF PIDS THAT ARE CHECKED AT A TIME AND ARE INSERTED INTO THE MYSQL DATABASE
        limitFileCount = 10

		# Finds the amount of of rows in the CSV file and saves the number
        maxfileCount = sum(1 for row in pointer)

		# Counters to make insertions into the database that are incrememted when running the function
        currentFileCount = 0
        currentLimitFileCount = 0

		# Resets the pointer for the CSV file back to the top of the file after finding out how many rows the file contains
        pointer.seek(0)

		# Python dictionaries use a hash table which are used to make sure there are no duplicates values being inserted into the database
        rowArray = {}
        rowArray2 = {}

		# Creates a long query to search through the MySQL database to see if the value exists
        listToSearch = ""

        if csvHeader is not None:
            for aRow in csvLine:
                aPID = ""
                
				# If a row in the CSV file is empty, this will continue the function and not cause the program to fail
                try:
                    aPID = aRow[0]
                except Exception:
                    pass

				# Takes the value in the cell and converts all letters to uppercase letters
                rowArray[aPID.upper()] = ""
                DOINum = str(aPID.upper())
         
				# Creates the query string based on if it is addition to a string or the begining of the whole string
                if (currentLimitFileCount == 0):
                    listToSearch = "\"" + DOINum + "\"" 
                else:
                    listToSearch = listToSearch + ", " + "\"" + DOINum + "\""

                currentFileCount += 1
                currentLimitFileCount += 1

				# If the amount of PIDs from the CSV file reaches the end or it hits the limit on how many PIDs can be checked at once, then the SQL query is ran to check for duplicates
                if (currentLimitFileCount == limitFileCount) or (currentFileCount == maxfileCount):
                    query = "Select alternative_id FROM doidata._main_ WHERE alternative_id IN (" + listToSearch + ")" 
                    cursor.execute(query)
                    resultSet = cursor.fetchall()
                    
					# There are 2 dictionaries, the first contains the values from the CSV file and the second one contains all of the ones that exist in the MySQL database
					# If the value in the first dictionary exists in the second dictonary, then it is removed because the data for that PID does not need to be inserted again
                    for rowValue in resultSet:
                        for key, value in rowArray2.items():
                            if key in rowArray:
                                del rowArray[key]

					# Values in the dictionary are passed to this function to be retreived and placed into the MongoDB database
                    PIDtoDOIInsertMongoDB(connection, cursor, sciEloDatabase, rowArray, doiCode)
                    
                    currentLimitFileCount = 0
                    rowArray.clear()
                    rowArray2.clear()
    
    sciEloDatabase.drop()
    
def PIDtoDOIInsertMongoDB(connection, cursor, sciEloDatabase, rowArray, doiCode):
                                                     
    mongoInfo = []
    doiInfo = ""
    mongoID = []
    mongoID2 = []
    sqlInfo = []

    for key, value in rowArray.items():

		# The value from the CSV is concatenated with the country code from Crossref so the PID is transformed into a Crossref DOI
        DOINum = str(doiCode) + "/" + str(key)

        try:
			# This is an object from the Crossref.restful API that is used to contact Crossref and see if the article exists in their database
            works = Works()
			
			# The DOI is searched in the Crossref API and if data exists then it is retreived and saved
            doiInfo = works.doi(DOINum)
			
			# If the data retrieved is not empty then it is added to the list that will be inserted into the MongoDB collection
            if doiInfo is not None:
                mongoInfo.append(doiInfo)
				
            logging.info("Crossref Metadata API for DOI: " + DOINum + " found")
        except:
            logging.info("Error occured retreiving information from Crossref Metadata API for DOI: " + DOINum)        

    try:
		# The list that has all the data for the DOIs is inserted in the MongoDB collection
        mongoID = (sciEloDatabase.insert_many(mongoInfo))
		
        logging.info("Crossref Metadata API for DOI: " + DOINum + " found")
        logging.info("DOI: " + DOINum + " inserted into MongoDB")
    except:
        logging.info("Error occured inserting info for DOI: " + DOINum + " into MongoDB collection")

    try:
		# When the list of data was inserted into the MongoDB collection, another list was returned with all the ID values given automatically by MongoDB.
		# The data is filtered by MongoDB into a JSON format and it retreived back using the IDs and then sent to another Python script to filter for insertion into the MySQL database
        mongoID2 = sciEloDatabase.find({"_id": {"$in": mongoID.inserted_ids}})
		
        for mongoDocs in mongoID2:
            sqlInfo.append(PIDtoDOIInsertSQL(connection, cursor, mongoDocs, logging))
    
		# Query to insert the information into the MySQL database
        query = """INSERT IGNORE INTO doidata._main_(DOI, URL, alternative_id, container_title, created_date_parts, created_date_time, 
                created_timestamp, deposited_date_parts, deposited_date_time, deposited_timestamp, 
                indexed_date_parts, indexed_date_time, indexed_timestamp, is_referenced_by_count, issue, 
                issued_date_parts, language, member, original_title, page, prefix, published_print_date_parts,
                publisher, reference_count, references_count, score, short_container_title, short_title, source, subtitle, title, 
                type, volume, fk) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        cursor.executemany(query, sqlInfo)
        connection.commit() 
    except:
       logging.info("Error occured inserting info into SQL table")
    
    del mongoID
    del mongoID2
    del sqlInfo
 
if __name__ == "__main__":
    getSciELOPID()
