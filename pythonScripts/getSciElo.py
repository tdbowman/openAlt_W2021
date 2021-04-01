import os
import json
import requests
import pymongo
import mysql.connector 
import logging
import pandas as pd
import numpy as np

#Author: Mohammad Tahmid
#Date: 03/10/2021
#Lines: 1-164
#Description: This python script takes in PIDs and converts them into DOIs. Then the DOI is put through the Crossref Data API and placed into MongoDB for filtering.

from crossref.restful import Works
from csv import reader
from getSciELOIngest import PIDtoDOIInsertSQL

def getSciELOPID():

    #Configuration file is accessed to get values set by administrator to run script
    try:
        configFilePath = str(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        configFilePath = os.path.join(configFilePath, "config", "openAltConfig.json")
        configFile = pd.read_json(configFilePath)
    except:
        logging.info("Configuration file \"openAltConfig.json\" not found")
        #print("Configuration file \"openAltConfig.json\" not found")
    
    #--------------------------------------------------------------------------------------

    #Logs file is created if it does not exists or if it is over the limit set in the configuration file
    try:
        dir_file = str(os.path.dirname(os.path.realpath(__file__)))
        filePath = os.path.join(dir_file, "Logs")
        if not os.path.isdir(filePath):
            os.mkdir(filePath)
    except:
        logging.info("Log file not found. Log file will be created")
        #print("Log file not found. Log file will be created")

    try:

        filePath = os.path.join(filePath, "SciELOIngest.log")
        logging.basicConfig(filename=filePath, filemode='a', level=logging.INFO,
        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

        #The log file size is checked 
        logFileSize = os.path.getsize(filePath)

        fileSizeLimit = int(configFile["SciELO-Brazil-Log"]["file_limit"]) * 10000

        if logFileSize > fileSizeLimit:

            #File if deleted if it is over the size limit
            os.remove(filePath)
            logging.basicConfig(filename=filePath, filemode='a', level=logging.INFO,
            format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    except FileNotFoundError:
        logging.info("Log not found, will be created")
        #print("Log not found, will be created")
    
    #--------------------------------------------------------------------------------------

    #Database connections are setup to use for the script
    #MySQL Connection is made
    database_user = configFile["DOI-Database"]["username"]
    database_password = configFile["DOI-Database"]["password"]
    database_host = configFile["DOI-Database"]["address"]
    database_name = configFile["DOI-Database"]["name"]

    connection = mysql.connector.connect(user=str(database_user), password=str(
            database_password), host=database_host, database=database_name)
    cursor = connection.cursor()

    #--------------------------------------------------------------------------------------

    #MongoDB connection is made
    mongoDB_user = configFile["MongoDB-SciELO-Database"]["username"]
    mongoDB_password = configFile["MongoDB-SciELO-Database"]["password"]
    mongoDB_host = configFile["MongoDB-SciELO-Database"]["address"]
    mongoDB_name = configFile["MongoDB-SciELO-Database"]["name"]
    mongoDB_collection = configFile["MongoDB-SciELO-Database"]["collection"]

    myClient = pymongo.MongoClient(mongoDB_host)
    sciELODatabase = myClient[mongoDB_name]
    sciELODatabase = sciELODatabase[mongoDB_collection]

    #--------------------------------------------------------------------------------------

    #Setup DOI code for Crossref Metadata API
    doiURL = str(configFile["SciELO-Brazil-Data-API"]["url"])
    doiCode = configFile["SciELO-Brazil-Data-API"]["url-code"]
    doiURL = doiURL + doiCode + os.sep

    #--------------------------------------------------------------------------------------

    #Open directory that contains csv files that contain PIDs from SciELO
    try:
        pidFolder = str(os.path.dirname(os.path.realpath(__file__)))
        pidFolder = os.path.join(pidFolder, "SciELOPID")
        if not os.path.isdir(pidFolder):
            os.mkdir(pidFolder)
    except:
        logging.info("SciELO folder not found. Directory will be created")
        #print("SciELO folder not found. Directory will be created")

    print(pidFolder)

    
    for subdir, dirs, files in os.walk(pidFolder):

        for fileName in files:

            pidFile = os.path.join(subdir, fileName)
                
            if pidFile.endswith(".csv"):

                PIDtoDOICheck(connection, cursor, sciELODatabase, pidFile, doiURL, doiCode,)

def PIDtoDOICheck(connection, cursor, sciEloDatabase, pidFile, doiURL, doiCode):

    DOIFullLink = str(doiURL) + str(doiCode) + "/"

    with open(pidFile, "r") as pointer:

        csvLine = reader(pointer)
        #csvHeader = next(csvLine)
        csvHeader = csvLine

        limitFileCount = 10
        maxfileCount = sum(1 for row in pointer)
        currentFileCount = 0
        currentLimitFileCount = 0

        pointer.seek(0)

        rowArray = {}
        rowArray2 = {}
        
        listToSearch = ""

        if csvHeader is not None:
            for aRow in csvLine:

                rowArray[aRow[0]] = ""
                #DOINum = str(doiCode) + "/" + str(aRow[0])
                DOINum = str(aRow[0])
                #print(rowArray)

                if (currentLimitFileCount == 0):
                    listToSearch = "\"" + DOINum + "\"" 
                else:
                    listToSearch = listToSearch + ", " + "\"" + DOINum + "\""

                currentFileCount += 1
                currentLimitFileCount += 1

                #query = "Select DOI FROM doidata._main_ WHERE DOI=" + "'" + str(DOINum) + "'"
                if (currentLimitFileCount == limitFileCount) or (currentFileCount == maxfileCount):
                    query = "Select alternative_id FROM doidata._main_ WHERE alternative_id IN (" + listToSearch + ")"
                    #query = "Select alternative_id FROM doidata._main_ WHERE alternative_id = \"S0100-879X1998000800006\""
                    cursor.execute(query)
                    resultSet = cursor.fetchall()
                    #print(resultSet)
                    

                    for rowValue in resultSet:
                        #rowArray2[rowValue[0]] = ""
                        #print(rowArray)
                        #print(rowArray2)

                        for key, value in rowArray2.items():
                            if key in rowArray:
                                del rowArray[key]

                    PIDtoDOIInsertMongoDB(connection, cursor, sciEloDatabase, rowArray, doiCode)
                    
                    #currentFileCount = 0
                    currentLimitFileCount = 0
                    rowArray.clear()
                    rowArray2.clear()
    
    sciEloDatabase.drop()

                #if not resultSet:
                    #PIDtoDOIInsertMongoDB(connection, cursor, sciEloDatabase, "10.1590/S0100-879X1998000800006")
                    #print("")

def PIDtoDOIInsertMongoDB(connection, cursor, sciEloDatabase, rowArray, doiCode):
                                                     
    mongoInfo = []
    doiInfo = ""
    mongoID = []
    mongoID2 = []
    sqlInfo = []

    for key, value in rowArray.items():

        DOINum = str(doiCode) + "/" + str(key)
        #print(DOINum)
        #mongoInfo = []
        #doiInfo = ""

        try:
            works = Works()
            doiInfo = works.doi(DOINum)
            #print(doiInfo)
            mongoInfo.append(doiInfo)
            #print(doiInfo)
            logging.info("Crossref Metadata API for DOI: " + DOINum + " found")
        except:
            logging.info("Error occured retreiving information from Crossref Metadata API for DOI: " + DOINum)
            #print("Error occured retreiving information from Crossref Metadata API for PID")        

        try:
            #mongoDBInsertResult = sciEloDatabase.insert_one(doiInfo)
            #mongoDBInsertResult = sciEloDatabase.insert_many(mongoInfo)
            logging.info("DOI: " + DOINum + " inserted into MongoDB")
            #dataFiltered = sciEloDatabase.find_one(mongoDBInsertResult.inserted_id)
            #print(dataFiltered)
            #PIDtoDOIInsertSQL(connection, cursor, dataFiltered, logging)
        except:
            logging.info("Error occured inserting info for DOI: " + DOINum + " into MongoDB collection")
            #print("Error occured inserting Crossref Metadata for ") 

    try:
        #print(mongoInfo)
        mongoID = (sciEloDatabase.insert_many(mongoInfo))
        #print(mongoID.inserted_ids)
        logging.info("Crossref Metadata API for DOI: " + DOINum + " found")
        #for x in mongoID.inserted_ids:
    except:
        logging.info("Error occured inserting info into MongoDB collection")

    try:  
        #mongoID2 = []
        mongoID2 = sciEloDatabase.find({"_id": {"$in": mongoID.inserted_ids}})
        #mongoID2 = sciEloDatabase.find({"_id": {mongoID}})
        #print(mongoID2)
        #print(mongoID2)
        for mongoDocs in mongoID2:
            sqlInfo.append(PIDtoDOIInsertSQL(connection, cursor, mongoDocs, logging))
        
        #mongoID2 = sciEloDatabase.find({"_id": {mongoID}})
        #print(mongoID.inserted_id)\
    
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
    
    mongoInfo.clear()
    doiInfo.clear()
    del mongoID
    del mongoID2
    del sqlInfo
    print("finished")
 
if __name__ == "__main__":
    getSciELOPID()