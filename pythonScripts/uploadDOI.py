import csv
import pandas
import logging

### Start of Darpan's Work ###

#Set the logging parameters
logging.basicConfig(filename='./doi_upload.log', filemode='a', level=logging.INFO,
    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  

try:
    import mysql.connector
except:
    print("MySQL Connector Exception")
    logging.info("Cannot determine how you intend to run the program")

#directory of doi list
#CHANGE DIRECTORY TO YOUR DOI LIST CSV
dir = 'C:\\Users\\darpa\\Desktop\\openAlt_W2021\\pythonScripts\\template_doi.csv'

doi_arr = []

#pandas library reads doi list
doi_list = pandas.read_csv(dir, header=None)


#adds doi values into array and prints the array
for x in range(len(doi_list)):
    doi_arr.append(doi_list.values[x][0])


#print(doi_arr)

## End of Darpan's Work


## Start of Salsabil's Work ##

# Parsing doi input to only include number
doi = "doi:"
url = "http://dx.doi.org/"    

for values in doi_arr:
    values = values.replace(doi,'')
    values = values.replace(url,'')
    #values = "\'" + values + "\'"
    

joinedArr = "\'" + "','".join(doi_arr) + "\'"
print(joinedArr)
print("\n")

#Getting MySQL database credentials
print("\nMySQL Credentials")
mysql_username = input("Username: ")
mysql_password = input("Password: ")

#Connecting to database
connection = mysql.connector.connect(user=str(mysql_username), password=str(
        mysql_password), host='127.0.0.1', database='crossrefeventdatamain')

cursor = connection.cursor()  

## End of Salsabil's Work ##


## Start of Darpan's Work
#Execution of query and output of result + log
query = 'SELECT DOI FROM dr_bowman_doi_ data_tables._main_ WHERE DOI IN (' + joinedArr + ');'

print('\n',query)
logging.info(query)
cursor.execute(query)
logging.info(cursor.fetchall())
cursor.execute(query)
print(cursor.fetchall())

## End of Darpan's Work




