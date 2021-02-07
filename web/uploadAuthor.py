import os
import csv
import pandas
import logging
import flask

# importing download function to download zip folder containing results CSV file
from downloadResultsCSV import downloadResultsAsCSV

### SAMPLE AUTHOR API INFO ###
### https://api.crossref.org/works?query=renear+ontologies ###
# "author": [
#                     {
#                         "given": "Allen H.",
#                         "family": "Renear",
#                         "sequence": "first",
#                         "affiliation": [
#                             {
#                                 "name": "Graduate School of Library and Information Science, University of Illinois at Urbana-Champaign"
#                             }
#                         ]
#                     },
#                     {
#                         "given": "Karen M.",
#                         "family": "Wickett",
#                         "sequence": "additional",
#                         "affiliation": [
#                             {
#                                 "name": "Graduate School of Library and Information Science, University of Illinois at Urbana-Champaign"
#                             }
#                         ]
#                     }
#                 ]

def downloadAuthor(mysql,dir_csv):

    # Directories 
    dir_file = str(os.path.dirname(os.path.realpath(__file__)))
    dir_template = dir_csv
    dir_results = dir_file + '\\Results\\uploadAuthor_results.csv'


    # Set the logging parameters
    logging.basicConfig(filename=dir_file + '\\Logs\\uploadAuthor.log', filemode='a', level=logging.INFO,
        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  

    # try:
    #     import mysql.connector
    # except:
    #     print("MySQL Connector Exception")
    #     logging.info("Cannot determine how you intend to run the program")

    author_arr = []

    #pandas library reads doi list
    doi_list = pandas.read_csv(dir_template, header=None)


    #adds doi values into array and prints the array
    for x in range(len(doi_list)):
        author_arr.append(doi_list.values[x][0])


    #print(author_arr)


    # joinedArr = "\'" + "','".join(author_arr) + "\'"
    # print(joinedArr)
    # print("\n")

    # #Getting MySQL database credentials
    # print("\nMySQL Credentials")
    # mysql_username = input("Username: ")
    # mysql_password = input("Password: ")

    # #Connecting to database
    # connection = mysql.connector.connect(user=str(mysql_username), password=str(
    #         mysql_password), host='127.0.0.1', database='crossrefeventdatamain')

    cursor = mysql.connection.cursor()  


    #Execution of query and output of result + log
    resultSet = []
    for values in author_arr:

        query = 'SELECT * FROM dr_bowman_doi_data_tables.author WHERE name LIKE ' + "\'%" + values + "%\'" + ';' #### will need to change query based on how author information is retrieved ####
        cursor.execute(query)
        result = cursor.fetchall()
        resultSet.append(result)

        print('\n',query)
        logging.info(query)
        print(result)
        logging.info(result)

    # Write result to file.
    df = pandas.DataFrame(resultSet)
    df.to_csv(dir_results)
        
    # send results to zip (directory, zip file name, csv name)
    downloadResultsAsCSV(dir_results,'uploadAuthor_Results.zip','uploadDOI_Author.csv')

    
def searchByAuthor(mysql, fileName):

    #directory of doi list
    dir = '../web/uploadFiles/' + fileName

    downloadAuthor(mysql, dir)

    return flask.render_template('download.html')








