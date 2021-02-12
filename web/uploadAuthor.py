###### Darpan Start ######
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
    dir_results = dir_file + '\\Results\\uploadAuthor_Results.csv'


    # Set the logging parameters
    logging.basicConfig(filename=dir_file + '\\Logs\\uploadAuthor.log', filemode='a', level=logging.INFO,
        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  

    # try:
    #     import mysql.connector
    # except:
    #     print("MySQL Connector Exception")
    #     logging.info("Cannot determine how you intend to run the program")

    author_arr = []

    # Pandas library reads doi list
    doi_list = pandas.read_csv(dir_template, header=None)


    # Adds doi values into array and prints the array
    for x in range(len(doi_list)):
        author_arr.append(doi_list.values[x][0].lower())

    # Remove duplicates from author array
    author_arr = list(dict.fromkeys(author_arr))

    # Set up cursor to run SQL query
    cursor = mysql.connection.cursor()  


    # Delete temp CSV file if exists 
    if os.path.exists(dir_results):
        os.remove(dir_results)

    # Execution of query and output of result + log
    resultSet = []
    index = 0

    for values in author_arr:

        query = "SELECT affiliation, authenticated_orcid, family, given, name, orcid, sequence, suffix " \
                "FROM dr_bowman_doi_data_tables.author where name LIKE " \
                "\'%" + values + "%\'" + ';'
        cursor.execute(query)
        result = cursor.fetchall()
        resultSet.append(result)

        print('\n',query)
        logging.info(query)
        print(result)
        logging.info(result)

        print(index)
    
        
        # Write result to file. If first record, include header, else append without header
        if index == 0:
            df = pandas.DataFrame(result)
            df.to_csv(dir_results,mode='a',index=False)    
        else:
            df = pandas.DataFrame(result)
            df.to_csv(dir_results,header=False,mode='a',index=False)
            
        index += 1
    
    
    # send results to zip (directory, zip file name, csv name)
    downloadResultsAsCSV(dir_results,'uploadAuthor_Results.zip','uploadAuthor_Results.csv')

###### Darpan End ######

def searchByAuthor(mysql, fileName):

    # Directory of doi list
    dir = '../web/uploadFiles/' + fileName

    downloadAuthor(mysql, dir)

    return flask.render_template('downloadAuthors.html')








