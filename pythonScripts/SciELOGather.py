import os 
import logging
import mysql.connector
import pandas as pd
import sys as sys
from csv import reader
from crossref.restful import Works

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

#Author: Mohammad Tahmid
#Date: 3/2/2021
#Lines: 1-350
#Description: Takes PID's and converts it into a DOI to check with Crossref to get data from. THe date is then taken and inserted into the doidata database.

def PIDSetup():
    #Checking logging file to write to
    dir_file = str(os.path.dirname(os.path.realpath(__file__)))
    filePath = dir_file + '\\Logs\\SciELOIngest.log'

    #Log file size is set in MB
    LogFileSizeLimit = 100

    try:
        #The log file size is checked 
        logFileSize = os.path.getsize(filePath)

        if logFileSize > (LogFileSizeLimit * 1024):

            #File if deleted if it is over the size limit
            os.remove(filePath)
    except FileNotFoundError:
        print("Log not found, will be created")


    # Set the logging parameters
    logging.basicConfig(filename=filePath, filemode='a', level=logging.INFO,
    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    #--------------------------------------------------------------------------------------

    #Opening Configuration file for database connection and API connections
    configFilePath = str(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    configFilePath = os.path.join(configFilePath, "config", "openAltConfig.json")

    configFile = pd.read_json(configFilePath)

    database_user = configFile["DOI-Database"]["username"]
    database_password = configFile["DOI-Database"]["password"]
    database_host = configFile["DOI-Database"]["address"]
    database_name = configFile["DOI-Database"]["name"]


    '''
    print(database_user)
    print(database_host)
    print(database_password)
    print(database_name)
    '''

    connection = mysql.connector.connect(user=str(database_user), password=str(
            database_password), host=database_host, database=database_name)
    cursor = connection.cursor()

    doiURL = str(configFile["SciELO-Data-API"]["url"])
    doiCode = configFile["SciELO-Data-API"]["url-code"]
    doiURL = doiURL + doiCode + os.sep
    
    #--------------------------------------------------------------------------------------

    #Opening directory with files that have CSV number in them

    pidFolder = str(os.path.dirname(os.path.realpath(__file__)))
    pidFolder = os.path.join(pidFolder, "SciELOPID")

    for subdir, dirs, files in os.walk(pidFolder):

        for fileName in files:

            pidFile = os.path.join(subdir, fileName)
            
            if pidFile.endswith(".csv"):

                print(pidFile)
                with open(pidFile, "r") as pointer:

                    csvLine = reader(pointer)
                    #csvHeader = next(csvLine)
                    csvHeader = csvLine

                    if csvHeader is not None:
                        for aRow in csvLine:
                            PIDtoDOI(connection, cursor, aRow[0], doiURL, doiCode)
                        

def PIDtoDOI(connection, cursor, pid, doiURL, doiCode):
    
    queryNum = doiCode + "/" + pid
    
    query = """SELECT count(*) FROM doidata._main_ WHERE DOI = '%s'""" % (queryNum)
    cursor.execute(query)
    resultSet = cursor.fetchall()
    count = resultSet[0][0] 

    foundDOI = ""
    foundURL = ""
    foundAlternateID = ""
    foundContainerTitle = ""

    foundCreatedDatePart = ""
    foundCreatedDateTime = ""
    foundCreatedDateTimestamp = ""

    foundDepositedDatePart = ""
    foundDepositedDateTime = ""
    foundDepositedTimestamp = ""

    foundIndexedDatePart = ""
    foundIndexedDateTime = ""
    foundIndexedTimestamp = ""

    foundIsReferencedByCount = ""
    foundIssue = ""
    foundIssuedDatePart = ""
    foundLanguage = ""
    foundMember = ""
    foundOriginalTitle = ""
    foundPage = ""
    foundPrefix = ""
    foundPublishedPrintDatePart = ""
    foundPublisher = ""
    foundReferenceCount = ""
    foundReferencesCount = ""
    foundScore = ""
    foundShortContainerTitle = ""
    foundShortTitle = ""
    foundSource = ""
    foundSubtitle = ""
    foundTitle = ""
    foundType = ""
    foundVolume = ""
    foundfk = 0

    if not count > 0:
        try:
            works = Works()
            doiInfo = works.doi(queryNum)

            foundDOI = doiInfo['DOI']
            foundURL = doiInfo['URL']
            #foundAlternateID = doiInfo['alternative-id'][0]

            if not doiInfo['alternative-id'][0]:
                foundAlternateID = ""
            else:
                foundAlternateID = doiInfo['alternative-id'][0]

            foundContainerTitle = doiInfo['container-title'][0]


            #foundCreatedDatePart = str(doiInfo['created']['date-parts'][0][0])
            #foundCreatedDatePart = foundCreatedDatePart + "/" + str(doiInfo['created']['date-parts'][0][1])
            #foundCreatedDatePart = foundCreatedDatePart + "/" + str(doiInfo['created']['date-parts'][0][2])

            listLength = len(doiInfo['created']['date-parts'][0])
            for x in (range(listLength)):
                if (x == listLength - 1):
                    foundCreatedDatePart = foundCreatedDatePart + str(doiInfo['created']['date-parts'][0][x])
                else:
                    foundCreatedDatePart = foundCreatedDatePart + str(doiInfo['created']['date-parts'][0][x]) + "/"

            foundCreatedDateTime = doiInfo['created']['date-time']
            foundCreatedDateTime = foundCreatedDateTime.replace("T", " ")
            foundCreatedDateTime = foundCreatedDateTime.replace("Z", "")
            foundCreatedDateTimestamp = doiInfo['created']['timestamp']


            #foundDepositedDatePart = str(doiInfo['deposited']['date-parts'][0][0])
            #foundDepositedDatePart = foundDepositedDatePart + "/" + str(doiInfo['deposited']['date-parts'][0][1])
            #foundDepositedDatePart = foundDepositedDatePart + "/" + str(doiInfo['deposited']['date-parts'][0][2])

            listLength = len(doiInfo['deposited']['date-parts'][0])
            for x in (range(listLength)):
                if (x == listLength - 1):
                    foundDepositedDatePart = foundDepositedDatePart + str(doiInfo['deposited']['date-parts'][0][x])
                else:
                    foundDepositedDatePart = foundDepositedDatePart + str(doiInfo['deposited']['date-parts'][0][x]) + "/"

            foundDepositedDateTime = doiInfo['deposited']['date-time']
            foundDepositedDateTime = foundDepositedDateTime.replace("T", " ")
            foundDepositedDateTime = foundDepositedDateTime.replace("Z", "")
            foundDepositedTimestamp = doiInfo['deposited']['timestamp']


            #foundIndexedDatePart = str(doiInfo['indexed']['date-parts'][0][0])
            #foundIndexedDatePart = foundIndexedDatePart + "/" + str(doiInfo['indexed']['date-parts'][0][1])
            #foundIndexedDatePart = foundIndexedDatePart + "/" + str(doiInfo['indexed']['date-parts'][0][2])

            listLength = len(doiInfo['indexed']['date-parts'][0])
            for x in (range(listLength)):
                if (x == listLength - 1):
                    foundIndexedDatePart = foundIndexedDatePart + str(doiInfo['indexed']['date-parts'][0][x])
                else:
                    foundIndexedDatePart = foundIndexedDatePart + str(doiInfo['indexed']['date-parts'][0][x]) + "/"

            foundIndexedDateTime = doiInfo['indexed']['date-time']
            foundIndexedDateTime = foundIndexedDateTime.replace("T", " ")
            foundIndexedDateTime = foundIndexedDateTime.replace("Z", "")
            foundIndexedTimestamp = doiInfo['indexed']['timestamp']

            foundIsReferencedByCount = doiInfo['is-referenced-by-count']
            foundIssue = doiInfo['issue']

            listLength = len(doiInfo['issued']['date-parts'][0])
            for x in (range(listLength)):
                if (x == listLength - 1):
                    foundIssuedDatePart = foundIssuedDatePart + str(doiInfo['issued']['date-parts'][0][x])
                else:
                    foundIssuedDatePart = foundIssuedDatePart + str(doiInfo['issued']['date-parts'][0][x]) + "/"

            default = ""
            foundLanguage = doiInfo.get("language", default)

            foundMember = doiInfo['member']

            if not doiInfo['original-title']:
                foundOriginalTitle = "None"
            else:
                foundOriginalTitle = doiInfo['original-title']
            
            if not doiInfo['page']:
                foundPage = ""
            else:
                foundPage = doiInfo['page']
            
            foundPrefix = doiInfo['prefix']

            if doiInfo['published-print']['date-parts'][0]:
                foundPublishedPrintDatePart = ""
            else:
                listLength = len(doiInfo['published-print']['date-parts'][0])
                for x in (range(listLength)):
                    if (x == listLength - 1):
                        foundPublishedPrintDatePart = foundPublishedPrintDatePart + str(doiInfo['published-print']['date-parts'][0][x])
                    else:
                        foundPublishedPrintDatePart = foundPublishedPrintDatePart + str(doiInfo['published-print']['date-parts'][0][x]) + "/"

            foundPublisher = doiInfo['publisher']

            foundReferenceCount = doiInfo['reference-count']

            foundReferencesCount = doiInfo['references-count']

            foundScore = doiInfo['score']

            if not doiInfo['short-container-title'][0]:
                foundShortContainerTitle = "None"
            else:
                foundShortContainerTitle = doiInfo['short-container-title'][0]

            if not doiInfo['short-title']:
                foundShortTitle = "None"
            else:
                foundShortTitle = doiInfo['short-title']
            
            foundSource = doiInfo['source']

            if not doiInfo['subtitle']:
                foundSubtitle = "None"
            else:
                foundSubtitle = doiInfo['subtitle']

            if not doiInfo['title'][0]:
                foundTitle = "None"
            else:
                foundTitle = doiInfo['title'][0]

            foundType = doiInfo['type']
        
            if not doiInfo['volume']:
                foundVolume = ""
            else:
                foundVolume = doiInfo['volume']

            query = """SELECT MAX(fk) FROM doidata._main_;"""
            cursor.execute(query)
            resultSet = cursor.fetchall()
            count = int(resultSet[0][0])
            
            foundfk = count + 1

            '''
            print(foundDOI, foundURL, foundAlternateID, foundContainerTitle, foundCreatedDatePart, foundCreatedDateTime, 
                foundCreatedDateTimestamp, foundDepositedDatePart, foundDepositedDateTime, foundDepositedTimestamp, foundIndexedDatePart,
                foundIndexedDateTime, foundIndexedTimestamp, foundIsReferencedByCount, foundIssue, foundIssuedDatePart, foundLanguage,
                foundMember, foundOriginalTitle, foundPage, foundPrefix, foundPublishedPrintDatePart, foundPublisher,foundReferenceCount, 
                foundReferencesCount, foundScore, foundShortContainerTitle, foundShortTitle, foundSource, foundSubtitle, foundTitle, foundType, 
                foundVolume, foundfk)
            '''
            
            query = """INSERT IGNORE INTO doidata._main_(DOI, URL, alternative_id, container_title, created_date_parts, created_date_time, 
                    created_timestamp, deposited_date_parts, deposited_date_time, deposited_timestamp, 
                    indexed_date_parts, indexed_date_time, indexed_timestamp, is_referenced_by_count, issue, 
                    issued_date_parts, language, member, original_title, page, prefix, published_print_date_parts,
                    publisher, reference_count, references_count, score, short_container_title, short_title, source, subtitle, title, 
                    type, volume, fk) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            queryValues = (foundDOI, foundURL, foundAlternateID, foundContainerTitle, foundCreatedDatePart, foundCreatedDateTime, 
                foundCreatedDateTimestamp, foundDepositedDatePart, foundDepositedDateTime, foundDepositedTimestamp, foundIndexedDatePart,
                foundIndexedDateTime, foundIndexedTimestamp, foundIsReferencedByCount, foundIssue, foundIssuedDatePart, foundLanguage,
                foundMember, foundOriginalTitle, foundPage, foundPrefix, foundPublishedPrintDatePart, foundPublisher,foundReferenceCount, 
                foundReferencesCount, foundScore, foundShortContainerTitle, foundShortTitle, foundSource, foundSubtitle, foundTitle, foundType, 
                foundVolume, foundfk)
                
            cursor.execute(query, queryValues)
            connection.commit()

            logging.info("Added DOI: " + foundDOI)
    
        #except Exception as exception:
            #logging.info("Problem retreiving value for DOI: " + queryNum + " Issue: " + str(exception))
        except:
            logging.info("Problem retreiving value for DOI: " + queryNum + " Issue: ")

           
if __name__ == "__main__":
    PIDSetup()