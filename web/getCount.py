# Author: Salsabil Bakth
# The purpose of this file is to retrieve the total records found 
# from the user's uploaded file in the doidata table. This result
# will be displayed on the email page.

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
from flask import redirect

# Setter for stats
def setStats(x,y):
    global stats
    stats = 'Records Found: ' + str(x) + '/' + str(y)
    print(stats)

# Getter for stats
def getStats():
    return stats

def uploadDOIList(mysql, fileName):

    # Directory of uploaded file
    dir = '../web/uploadFiles/' + fileName

    # downloadDOI(mysql, dir, type, email)
    getDOICount(mysql, dir)

    # Delete uploaded files
    if os.path.exists(dir):
        os.remove(dir)

    #return flask.render_template('searchComplete.html', mysql, dir, type, email, type = 'doi')
    return flask.render_template('downloadDOI.html', results = getStats())

def getDOICount(mysql, dir_csv):

     # directories
    dir_file = str(os.path.dirname(os.path.realpath(__file__)))

    # path of uploaded file
    dir_template = dir_csv

    # path of config file
    dir_config = dir_file + '\\uploadDOI_config.txt'

    # # path of file to print results to
    # dir_results = dir_file  + '\\Results\\doiEvents_' + str(dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

    # # Create folder to hold results
    # if not os.path.exists(dir_results):
    #     os.mkdir(dir_results)

    # Set the logging parameters
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

    # # Join array for sql query
    # joinedArr = "\'" + "','".join(doi_arr) + "\'"

    #Cursor makes connection with the db
    cursor = mysql.connection.cursor() 

    # Count of DOIs found in database
    count = 0

    # Execution of query and output of result + log
    for doi in doi_arr:
        query = "SELECT * FROM doidata._main_ WHERE DOI LIKE '%" + doi + "%'"
        cursor.execute(query)
        resultSet = cursor.fetchall()

        # Print queries and results in console and log
        # print('\n',query)
        # logging.info(query)
        # print('RESULT SET:', resultSet)
        # logging.info(resultSet)   

       
        # Write result to file.
        df = pandas.DataFrame(resultSet)

        
        # If query outputs no results, add to not found csv, else write
        if df.empty:
            print("DOI NOT FOUND:", doi)
            # logging.info("DOI NOT FOUND: " + doi)

        else:
            # Replace invalid chars for file name
            # file_id = doi.replace('/','-')
            # file_id = file_id.replace('.','-')
            # print('FILE ID:', file_id)

            # resultPath = dir_results + '\\doiEvent_' + str(file_id) + '.csv'
            # df.columns = [i[0] for i in cursor.description]  ###### CAUSED ISSUE ON SALSBILS MACHINE #######
            # df.to_csv(resultPath,index=False)
            count = count + 1
            
    # Stats of query
    print('\n')
    setStats(count, len(doi_arr))
