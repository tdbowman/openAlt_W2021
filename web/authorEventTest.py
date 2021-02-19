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

#Count of authors found
count = 0

for author in author_arr:
    # Author Info Query
    query = "SELECT affiliation, authenticated_orcid, family, given, name, orcid, sequence, suffix " \
                "FROM doidata.author where name LIKE " \
                "\'%" + author + "%\'" + ';'
    cursor.execute(query)
    resultSet = cursor.fetchall()

    print('\n',query)
    logging.info(query)
    print('RESULT SET:',resultSet)
    logging.info(resultSet)

    # Write result to file.
    df = pandas.DataFrame(resultSet)

    # If query outputs no results, then author not in database
    if df.empty:
        # CSV containing list of results not found
        emptyResultPath = dir_results + '\\NotFound.csv'
        
        with open(emptyResultPath,'a',newline='') as emptyCSV:
            writer = csv.writer(emptyCSV)
            writer.writerow([author])
        
        print("AUTHOR NOT FOUND:", author)
        logging.info("AUTHOR NOT FOUND: " + author)

    else:
        count = count + 1
        # Replace invalid chars for file name
        file_id = author.replace(' ','-')
        file_id = file_id.replace('.','')
        print('FILE ID:', file_id)

        resultPath = dir_results + '\\' + str(file_id) + '_authorInfo.csv'
        df.columns = [i[0] for i in cursor.description]  ###### CAUSED ISSUE ON SALSBILS MACHINE #######
        df.to_csv(resultPath,index=False)
        
    

        # Author Associated DOIs Query
        query = "SELECT * FROM doidata._main_ JOIN doidata.author ON doidata._main_.id = doidata.author.fk WHERE doidata.author.name  LIKE " \
                    "\'%" + author + "%\'" + ';'
        cursor.execute(query)
        resultSet = cursor.fetchall()

  
        print('\n',query)
        logging.info(query)
        print('RESULT SET:',resultSet)
        logging.info(resultSet)

        resultPath = dir_results + '\\' + str(file_id) + '_authorDOIs.csv'

        # Write associated DOI info to file.
        df = pandas.DataFrame(resultSet)
        
        if not df.empty:
            df.columns = [i[0] for i in cursor.description]
            df.to_csv(resultPath,index=False)



# Stats of query
print('\n')
print(count, 'results found out of', len(author_arr))   

shutil.make_archive(str(dir_results),'zip',dir_results)

# Delete unzipped folder
if os.path.exists(dir_results):
    shutil.rmtree(dir_results)

zipResults = dir_results + '.zip'
print("RESULTS ZIP",zipResults)



###### Darpan End ######

