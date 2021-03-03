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
dir_template = 'C:\\Users\\darpa\\Desktop\\universityTest.csv'

# path of results folder with current time
dir_results = dir_file  + '\\Results\\universityEvents_' + str(dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))



# Create folder to hold results
if not os.path.exists(dir_results):
    os.mkdir(dir_results)

#Delete temp CSV file if exists
# if os.path.exists(dir_results):
#     os.remove(dir_results)

# Set the logging parameters
logging.basicConfig(filename= dir_file + '\\Logs\\uploadUniversity.log', filemode='a', level=logging.INFO,
format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

uni_arr = []

# Pandas library reads doi list
uni_list = pandas.read_csv(dir_template, header=None)


# Adds doi values into array and prints the array
for x in range(len(uni_list)):
    uni_arr.append(uni_list.values[x][0].lower())

# Remove duplicates from author array
uni_arr = list(dict.fromkeys(uni_arr))


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

print(uni_arr)

#Count of authors found
count = 0

for uni in uni_arr:
    # Author Info Query
    query = "SELECT affiliation, authenticated_orcid, family, given, name, orcid, sequence, suffix " \
                "FROM doidata.author where affiliation LIKE " \
                "\'%" + uni + "%\'" + ';'
    cursor.execute(query)
    resultSet = cursor.fetchall()

    print('\n',query)
    logging.info(query)
    print('RESULT SET:',resultSet)
    logging.info(resultSet)

    # Writing API query to API_Instructions.txt
    uni_api = uni.replace(' ','+')
    f.write("https://api.crossref.org/works?query.affiliation=" + uni_api + "\n")

    # Write result to file.
    df = pandas.DataFrame(resultSet)

    # If query outputs no results, then author not in database
    if df.empty:
        # CSV containing list of results not found
        emptyResultPath = dir_results + '\\NotFound.csv'

        with open(emptyResultPath,'a',newline='') as emptyCSV:
            writer = csv.writer(emptyCSV)
            writer.writerow([uni])

        print("UNIVERSITY NOT FOUND:", uni)
        logging.info("UNIVERSITY NOT FOUND: " + uni)

    else:
        count = count + 1
        # Replace invalid chars for file name
        file_id = uni.replace(' ','-')
        file_id = file_id.replace('.','')
        print('FILE ID:', file_id)

        resultPath = dir_results + '\\' + str(file_id) + '_authorInfo.csv'
        df.columns = [i[0] for i in cursor.description]  ###### CAUSED ISSUE ON SALSBILS MACHINE #######
        df.to_csv(resultPath,index=False)



        # Author Associated DOIs Query
        query = "SELECT DOI, URL, title, container_title, name as author, page, publisher, language, alternative_id, created_date_time, " \
                        "deposited_date_time, is_referenced_by_count, issue, issued_date_parts, prefix, published_online_date_parts, published_print_date_parts " \
                    "FROM doidata._main_ JOIN doidata.author ON doidata._main_.id = doidata.author.fk WHERE doidata.author.affiliation  LIKE " \
                        "\'%" + uni + "%\'" + ';'
        cursor.execute(query)
        resultSet = cursor.fetchall()


        print('\n',query)
        logging.info(query)
        print('RESULT SET:',resultSet)
        logging.info(resultSet)

        resultPath = dir_results + '\\' + str(file_id) + '_DOIs.csv'

        # Write associated DOI info to file.
        df = pandas.DataFrame(resultSet)

        if not df.empty:
            df.columns = [i[0] for i in cursor.description]
            df.to_csv(resultPath,index=False)


# Close API_Instructions.txt
f.close()

# Stats of query
print('\n')
print(count, 'results found out of', len(uni_arr))

shutil.make_archive(str(dir_results),'zip',dir_results)

# Delete unzipped folder
if os.path.exists(dir_results):
    shutil.rmtree(dir_results)

zipResults = dir_results + '.zip'
print("RESULTS ZIP",zipResults)



###### Darpan End ######
