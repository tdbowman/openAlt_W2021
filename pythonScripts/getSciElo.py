import os
import json
import requests
import pymongo
import mysql.connector 
import logging
import pandas as pd

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

        if csvHeader is not None:
            for aRow in csvLine:

                DOINum = str(doiCode) + "/" + str(aRow[0])
                print(DOINum)

                query = "Select DOI FROM doidata._main_ WHERE DOI=" + "'" + str(DOINum) + "'"
                cursor.execute(query)
                resultSet = cursor.fetchall()

                if not resultSet:
                    PIDtoDOIInsertMongoDB(connection, cursor, sciEloDatabase, DOINum)

def PIDtoDOIInsertMongoDB(connection, cursor, sciEloDatabase, DOINum):

    try:
        works = Works()
        doiInfo = works.doi(DOINum)
        logging.info("Crossref Metadata API for DOI: " + DOINum + " found")
    except:
        logging.info("Error occured retreiving information from Crossref Metadata API for DOI: " + DOINum)
        #print("Error occured retreiving information from Crossref Metadata API for PID")        

    try:
        mongoDBInsertResult = sciEloDatabase.insert_one(doiInfo)
        logging.info("DOI: " + DOINum + " inserted into MongoDB")
        dataFiltered = sciEloDatabase.find_one(mongoDBInsertResult.inserted_id)
        print(dataFiltered)
        PIDtoDOIInsertSQL(connection, cursor, dataFiltered, logging)
    except:
        logging.info("Error occured inserting info for DOI: " + DOINum + " into MongoDB collection")
        #print("Error occured inserting Crossref Metadata for ")  
 
if __name__ == "__main__":
    getSciELOPID()