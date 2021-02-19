###### Darpan Start ######
import os
import csv
import pandas
import logging
import flask
import platform
import mysql
import shutil
import datetime as dt
from flask import redirect

# importing download function to download zip folder containing results CSV file
from downloadResultsCSV import downloadResultsAsCSV

# directories
dir_file = str(os.path.dirname(os.path.realpath(__file__)))

# path of uploaded file
dir_template = 'C:\\Users\\darpa\\Desktop\\authorTest.csv'

# path of config file
dir_config = dir_file + '\\uploadAuthor_config.txt'

# path of results folder with current time
dir_results = dir_file  + '\\Results\\authorEvents_' + str(dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))



# Create folder to hold results
if not os.path.exists(dir_results):
    os.mkdir(dir_results)

#Delete temp CSV file if exists 
# if os.path.exists(dir_results):
#     os.remove(dir_results)

# Set the logging parameters
logging.basicConfig(filename= dir_file + '\\Logs\\uploadAuthor.log', filemode='a', level=logging.INFO,
format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  

author_arr = []

# Pandas library reads doi list
author_list = pandas.read_csv(dir_template, header=None)


# Adds doi values into array and prints the array
for x in range(len(author_list)):
    author_arr.append(author_list.values[x][0].lower())

# Remove duplicates from author array
author_arr = list(dict.fromkeys(author_arr))


try:
    import mysql.connector
except:
    print("MySQL Connector Exception")
    logging.info("Cannot determine how you intend to run the program")


# Connecting to database
connection = mysql.connector.connect(user=str('root'), password=str(
        'pass'), host='127.0.0.1', database='crossrefeventdatamain')

#Cursor makes connection with the db
cursor = connection.cursor() 

print(author_arr)

count = 1
for author in author_arr:
    # Execution of query and output of result + log
    query = "SELECT affiliation, authenticated_orcid, family, given, name, orcid, sequence, suffix " \
                "FROM dr_bowman_doi_data_tables.author where name LIKE " \
                "\'%" + author + "%\'" + ';'
    cursor.execute(query)
    resultSet = cursor.fetchall()

    print('\n',query)
    logging.info(query)
    print('RESULT SET:',resultSet)
    logging.info(resultSet)

   
    file_id = author.replace(' ','-')
    file_id = file_id.replace('.','')
    print('FILE ID:', file_id)

    resultPath = dir_results + '\\authorEvent_' + str(file_id) + '.csv'

    # Write result to file.
    df = pandas.DataFrame(resultSet)
    df.columns = [i[0] for i in cursor.description]
    df.to_csv(resultPath,index=False)

    count = count + 1

    # send results to zip (directory, zip file name, csv name)
    # downloadResultsAsCSV(dir_results,'uploadDOI_Results.zip','uploadDOI_Results.csv')

shutil.make_archive(str(dir_results),'zip',dir_results)

# Delete unzipped folder
if os.path.exists(dir_results):
    shutil.rmtree(dir_results)

zipResults = dir_results + '.zip'
print("RESULTS ZIP",zipResults)



###### Darpan End ######

