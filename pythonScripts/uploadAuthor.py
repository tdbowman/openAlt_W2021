import csv
import pandas
import logging

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


#Set the logging parameters
logging.basicConfig(filename='./author_upload.log', filemode='a', level=logging.INFO,
    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  

try:
    import mysql.connector
except:
    print("MySQL Connector Exception")
    logging.info("Cannot determine how you intend to run the program")

#directory of doi list
#CHANGE DIRECTORY TO YOUR DOI LIST CSV
dir = 'C:\\Users\\darpa\\Desktop\\openAlt_W2021\\pythonScripts\\template_author.csv'
author_arr = []

#pandas library reads doi list
doi_list = pandas.read_csv(dir, header=None)



#adds doi values into array and prints the array
for x in range(len(doi_list)):
    author_arr.append(doi_list.values[x][0])


#print(author_arr)


# joinedArr = "\'" + "','".join(author_arr) + "\'"
# print(joinedArr)
# print("\n")

#Getting MySQL database credentials
print("\nMySQL Credentials")
mysql_username = input("Username: ")
mysql_password = input("Password: ")

#Connecting to database
connection = mysql.connector.connect(user=str(mysql_username), password=str(
        mysql_password), host='127.0.0.1', database='crossrefeventdatamain')

cursor = connection.cursor()  


#Execution of query and output of result + log

for values in author_arr:

    query = 'SELECT * FROM dr_bowman_doi_data_tables.author WHERE family LIKE ' + "\'%" + values + "%\'" + ';' #### will need to change query based on how author information is retrieved ####

    print('\n',query)
    logging.info(query)
    cursor.execute(query)
    logging.info(cursor.fetchall())
    cursor.execute(query)
    print(cursor.fetchall())






