###### Darpan Start ######
import os
import csv
import pandas
import logging
import flask
import platform
import mysql
import shutil
import time
import datetime as dt
import dbQuery
from flask import redirect
import emailResults as er

# importing download function to download zip folder containing results CSV file
from downloadResultsCSV import downloadResultsAsCSV

# Setter for zip directory
def setZipEvents(path):
    global zipEvents
    zipEvents = path
    print("RESULTS DIRECTORY:", zipEvents)

# Getter for zip directory, used to retrieve directory in front end
def getZipEvents():
    return zipEvents

# Setters for stats
def setEventStats(eventCount, total):
    global eventStats
    eventStats = 'EVENTS FOUND: ' + str(eventCount) + '/' + str(total) + ' DOIs'
    print(eventStats)

def setMetadataStats(metadataCount, total):
    global metadataStats
    metadataStats = 'METADATA FOUND: ' + str(metadataCount) + '/' + str(total) + ' DOIs' 
    print(metadataStats)

# Getters for stats
def getEventStats():
    return eventStats

def getMetadataStats():
    return metadataStats


def downloadDOI(mysql, dir_csv, type, email):

    # time execution of script
    start_time = time.time()

    # path of this file
    dir_file = str(os.path.dirname(os.path.realpath(__file__)))

    # path of uploaded file
    dir_template = dir_csv

    # path of config file
    dir_config = dir_file + '\\uploadDOI_config.txt'

    # path of file to print results to
    if not os.path.exists(dir_file + '\\Results'):
        os.mkdir(dir_file + '\\Results')

    dir_results = dir_file  + '\\Results\\doiEvents_' + str(dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

    # Create folder to hold results
    if not os.path.exists(dir_results):
        os.mkdir(dir_results)

    # Set the logging parameters
    if not os.path.exists(dir_file + '\\Logs'):
        os.mkdir(dir_file + '\\Logs')
    logging.basicConfig(filename= dir_file + '\\Logs\\uploadDOI.log', filemode='a', level=logging.INFO,
        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    doi_arr = []

    # pandas library reads doi list
    doi_list = pandas.read_csv(dir_template, header=None)


    # adds doi values into array and prints the array
    for x in range(len(doi_list)):
        if x not in doi_arr:
            doi_arr.append(doi_list.values[x][0])


    # Reading config file to parse doi input to only include number
    config_arr = []
    config_file = open(dir_config,'r')

    # Reading config file line by line
    # Without the r strip, '\n' is added on to the value -> Ex. 'doi:\n'
    for line in config_file:
        config_arr.append(line.rstrip('\n'))

    # Parse out doi formatting
    for config in config_arr:
        doi_arr = [doi.replace(config,'') for doi in doi_arr]

    # Remove duplicates from the doi array
    doi_arr = list(dict.fromkeys(doi_arr))

   
    # Cursor makes connection with the db
    cursor = mysql.connection.cursor()

    # Creating text file with API instructions
    f = open(dir_results + '\\API_Instructions.txt','w+')
    f.write("Thank you for using OpenAlt v2.0!\n" \
            "We do not provide the complete information listed from the APIs. For more complete and raw information, consider using the CrossRef API with the instructions listed below\n\n" \
            "1) Download Postman from https://www.postman.com/downloads/\n" \
            "2) Run a GET Request on Postman, enter a link listed below and hit send\n"
            "3) You will see the output in the body section on the lower third half of the window. Make sure that the *Body* setting is set to *Pretty* and the dropdown to *JSON*\n\n" \
            "You may also use any other API retrieval method, Postman happens to be the method the developers here at OpenAlt use to test APIs\n\n" \
            "For more information about the CrossRef API, checkout the links listed below:\n" \
            "https://www.crossref.org/education/retrieve-metadata/rest-api/\n" \
            "https://github.com/CrossRef/rest-api-doc\n\n\n" \
            "YOUR API QUERIES: \n")


    # Array containing table names found in crossrefeventdatamain (except main)
    event_tables = ['cambiaevent','crossrefevent','dataciteevent', 'f1000event','hypothesisevent','newsfeedevent','redditevent','redditlinksevent','stackexchangeevent','twitterevent','webevent','wikipediaevent','wordpressevent']

    # Count of DOIs found in database
    eventsFound = 0
    metadataFound = 0
    progress = 0

    # Execution of queries and output of result + log
    for doi in doi_arr:
        progress = progress + 1
        print("PROGRESS: " + str(progress) + "/" + str(len(doi_arr)))
        
        # Writing API query to API_Instructions.txt
        f.write("https://api.crossref.org/works/" + doi + "\n")

        # Replace invalid chars for file name
        invalid_chars = ['/','.','(',')',':','<','>','?','|','\"','*']
        file_id = doi.replace(' ', '-')
        for char in invalid_chars:
            file_id = file_id.replace(char,'-')
        
        #print('FILE ID:', file_id)

        
        # Getting event counts
        resultSet = dbQuery.getDOIEventCounts(doi, cursor)
        logging.info(resultSet)

        # If query outputs no results, add to not found csv, else write
        if len(resultSet) == 0:
            # CSV containing list of results not found
            emptyResultPath = dir_results + '\\NotFound_Events.csv'

            with open(emptyResultPath,'a',newline='') as emptyCSV:
                writer = csv.writer(emptyCSV)
                writer.writerow([doi])

            logging.info("DOI EVENT NOT FOUND: " + doi)
        else:
            eventsFound = eventsFound + 1
            # Write result to file.
            df = pandas.DataFrame(resultSet)
            df = df.drop_duplicates()

            # Create folder to hold results
            dir_doi = dir_results + '\\' + str(file_id)
            if not os.path.exists(dir_doi):
                os.mkdir(dir_doi)

            df.columns = [i[0] for i in cursor.description]  ###### CAUSED ISSUE ON SALSBILS MACHINE #######

            if type == 'csv':
                resultPath = dir_doi + '\\eventCounts_' + str(file_id) + '.csv'
                df.to_csv(resultPath,index=False)
            elif type == 'json':
                resultPath = dir_doi + '\\eventCounts_' + str(file_id) + '.json'
                df.to_json(resultPath, orient='index', indent=2)

            # Retreiving Specific DOI Events
            resultSet, headers = dbQuery.getDOIEvents(doi,cursor)
            #logging.info(resultSet)
            
            for table in event_tables:
            # Getting specific event data
                if len(resultSet[table]) > 0:
                    # Write associated DOI info to file.
                    df = pandas.DataFrame(resultSet[table])
                    df.columns = headers[table]

                    # Writing CSV containing DOI metadata
                    if type == 'csv':
                        resultPath = dir_doi + '\\' + table + '_' + str(file_id) + '.csv'
                        df.to_csv(resultPath,index=False)
                    elif type == 'json':
                        resultPath = dir_doi + '\\' + table + '_' + str(file_id) + '.json'
                        df.to_json(resultPath, orient='index', indent=2)

       
        # DOI Info Query
        resultSet = dbQuery.getDOIMetadata(doi, cursor)
        logging.info(resultSet)

        # if results not empty
        if len(resultSet) > 0:
            metadataFound = metadataFound + 1
            # Write associated DOI info to file.
            df = pandas.DataFrame(resultSet)
            #df = df.drop_duplicates()
            df.columns = [i[0] for i in cursor.description]

            # Create folder to hold results
            dir_doi = dir_results + '\\' + str(file_id)
            if not os.path.exists(dir_doi):
                os.mkdir(dir_doi)

            # Writing CSV/JSON containing DOI metadata
            if type == 'csv':
                resultPath = dir_doi + '\\doiInfo_' + str(file_id) + '.csv'
                df.to_csv(resultPath,index=False)
            elif type == 'json':
                resultPath = dir_doi + '\\doiInfo_' + str(file_id) + '.json'
                df.to_json(resultPath, orient='index', indent=2)
        else:
            # CSV containing list of results not found
            emptyResultPath = dir_results + '\\NotFound_doiInfo.csv'
            with open(emptyResultPath,'a',newline='') as emptyCSV:
                writer = csv.writer(emptyCSV)
                writer.writerow([doi])
            
            logging.info("DOI INFO NOT FOUND: " + doi)

            # # Txt showing DOI info was not found in doi folder
            # emptyResult = open(dir_doi + '\\doiInfo_NotFound.txt','w+')
            # emptyResult.write("DOI: " + doi + "\nDOI Information Not Found\n")
            # emptyResult.close()
        

    # Close API_Instructions.txt
    f.close()

    # Stats of query
    print('\n')
    setEventStats(eventsFound, len(doi_arr))
    setMetadataStats(metadataFound, len(doi_arr))

    # Zip folder containing the CSV files=
    shutil.make_archive(str(dir_results),'zip',dir_results)

    # Delete unzipped folder
    if os.path.exists(dir_results):
        shutil.rmtree(dir_results)

    # Path of zip folder
    zipEvents = str(dir_results + '.zip')
    setZipEvents(zipEvents)

    # Send Results via email
    er.emailResults(zipEvents, email, 'doi')

    # Time taken to execute script
    print("--- %s seconds ---" % (time.time() - start_time))

    #return zipEvents

###### Darpan End ######

def searchByDOI(mysql, fileName, type, email):

    # Directory of uploaded file
    dir = '../web/uploadFiles/' + fileName

    downloadDOI(mysql, dir, type, email)

    # Delete uploaded files
    if os.path.exists(dir):
        os.remove(dir)

    #return flask.render_template('searchComplete.html', mysql, dir, type, email, type = 'doi')
    return flask.render_template('downloadDOI.html')
