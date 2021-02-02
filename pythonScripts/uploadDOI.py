import csv
import pandas
import logging


# Set the logging parameters
logging.basicConfig(filename='./doi_upload.log', filemode='a', level=logging.INFO,
    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  

try:
    import mysql.connector
except:
    print("MySQL Connector Exception")
    logging.info("Cannot determine how you intend to run the program")

# directories
# CHANGE DIRECTORY TO YOUR DOI LIST CSV AND CONFIG FILE
dir_template = 'C:\\Users\\darpa\\Desktop\\openAlt_W2021\\pythonScripts\\template_doi.csv'
dir_config = 'C:\\Users\\darpa\\Desktop\\openAlt_W2021\\pythonScripts\\config_doi.txt'


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
print("\nMySQL Credentials")
mysql_username = input("Username: ")
mysql_password = input("Password: ")

# Connecting to database
connection = mysql.connector.connect(user=str(mysql_username), password=str(
        mysql_password), host='127.0.0.1', database='crossrefeventdatamain')

cursor = connection.cursor()  


# Execution of query and output of result + log
query = 'SELECT DOI FROM dr_bowman_doi_data_tables._main_ WHERE DOI IN (' + joinedArr + ');'

print('\n',query)
logging.info(query)
cursor.execute(query)
logging.info(cursor.fetchall())
cursor.execute(query)
print(cursor.fetchall())

