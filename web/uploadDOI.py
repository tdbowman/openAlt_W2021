import os
import csv
import pandas
import logging
import flask

# importing download function to download zip folder containing results CSV file
from downloadResultsCSV import downloadResultsAsCSV


def downloadDOI(mysql, dir_csv):

    # try:
    #     import mysql.connector
    # except:
    #     print("MySQL Connector Exception")
    #     logging.info("Cannot determine how you intend to run the program")


    # directories
    dir_file = str(os.path.dirname(os.path.realpath(__file__)))
    dir_template = dir_csv
    dir_config = dir_file + '\\uploadDOI_config.txt'
    dir_results = dir_file  + '\\Results\\uploadDOI_results.csv'

    # Set the logging parameters
    logging.basicConfig(filename= dir_file + '\\Logs\\uploadDOI.log', filemode='a', level=logging.INFO,
        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  


    doi_arr = []

    # pandas library reads doi list
    doi_list = pandas.read_csv(dir_template, header=None)


    # adds doi values into array and prints the array
    for x in range(len(doi_list)):
        doi_arr.append(doi_list.values[x][0])


    # print(doi_arr)


    # Reading config file to parse doi input to only include number
    config_arr = []
    config_file = open(dir_config,'r')

    # Reading config file line by line
    # Without the r strip, '\n' is added on to the value -> Ex. 'doi:\n'
    for line in config_file:
        config_arr.append(line.rstrip('\n'))  

    # print('\nCONFIG ARR:',config_arr)
    # print('\nDOI ARR:', doi_arr)


    # Parse out doi formatting
    for config in config_arr:
        doi_arr = [doi.replace(config,'') for doi in doi_arr]


    #print("\nPARSED DOI ARR:", doi_arr)
        

    joinedArr = "\'" + "','".join(doi_arr) + "\'"
    #print("\nJOINED ARRAY:",joinedArr)
    print("\n")

    # Getting MySQL database credentials
    # print("\nMySQL Credentials")
    # mysql_username = input("Username: ")
    # mysql_password = input("Password: ")

    # Connecting to database
    # connection = mysql.connector.connect(user=str(mysql_username), password=str(
    #         mysql_password), host='127.0.0.1', database='crossrefeventdatamain')

    cursor = mysql.connection.cursor() 


    # Execution of query and output of result + log
    query = 'SELECT * FROM dr_bowman_doi_data_tables._main_ WHERE DOI IN (' + joinedArr + ');'
    cursor.execute(query)
    resultSet = cursor.fetchall()

    print('\n',query)
    logging.info(query)
    print(resultSet)
    logging.info(resultSet)


    # Write result to file.
    with open(dir_results, 'a', newline='') as resultCSV:
        resultCSV = csv.writer(resultCSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in resultSet:
            resultCSV.writerow(row)


    # send results to zip (directory, zip file name, csv name)
    downloadResultsAsCSV(dir_results,'uploadDOI_Results.zip','uploadDOI_Results.csv')


def searchByDOI(mysql, fileName):
    
    #directory of doi list
    dir = '../web/uploadFiles/' + fileName

    downloadDOI(mysql, dir)
   
    return flask.render_template('download.html')