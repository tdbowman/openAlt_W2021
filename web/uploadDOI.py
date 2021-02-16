###### Darpan Start ######
import os
import csv
import pandas
import logging
import flask
from flask import redirect

# importing download function to download zip folder containing results CSV file
from downloadResultsCSV import downloadResultsAsCSV


def downloadDOI(mysql, dir_csv):

    # directories
    dir_file = str(os.path.dirname(os.path.realpath(__file__)))

    # path of uploaded file
    dir_template = dir_csv

    # path of config file
    dir_config = dir_file + '\\uploadDOI_config.txt'

    # path of file to print results to
    dir_results = dir_file  + '\\Results\\uploadDOI_results.csv'

    #Delete temp CSV file if exists 
    if os.path.exists(dir_results):
        os.remove(dir_results)

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

    # Join array for sql query
    joinedArr = "\'" + "','".join(doi_arr) + "\'"

    #Cursor makes connection with the db
    cursor = mysql.connection.cursor() 

    # Execution of query and output of result + log
    query = "SELECT DOI, url, container_title, created_date_parts, issued_date_parts, language, publisher, title " \
            "FROM dr_bowman_doi_data_tables._main_ WHERE DOI IN " \
            "(" + joinedArr + ");"
    cursor.execute(query)
    resultSet = cursor.fetchall()

    print('\n',query)
    logging.info(query)
    print('RESULT SET',resultSet)
    logging.info(resultSet)


    # Write result to file.
    df = pandas.DataFrame(resultSet)
    df.to_csv(dir_results,index=False)

    
    # send results to zip (directory, zip file name, csv name)
    downloadResultsAsCSV(dir_results,'uploadDOI_Results.zip','uploadDOI_Results.csv')

###### Darpan End ######

def searchByDOI(mysql, fileName):
    
    #directories
    dir = '../web/uploadFiles/' + fileName
    dir_file = str(os.path.dirname(os.path.realpath(__file__)))
    dir_results = dir_file + '\\Results\\uploadDOI_Results.zip'

    downloadDOI(mysql, dir)
   
    return flask.render_template('download.html', dir_zip = dir_results)