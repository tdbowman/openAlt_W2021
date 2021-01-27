import csv
import argparse
import crossref
import mysql.connector
import getpass
import os


print("MySQL Credentials")
mysql_username = input("Username: ")
mysql_password = getpass.getpass("Password: ")

dir_path = os.path.dirname(os.path.realpath(__file__))
#print(dir_path)
filepath = str(dir_path) + str("\\DOIValues.csv")

connection = mysql.connector.connect(user=str(mysql_username), password=str(
        mysql_password), host='127.0.0.1', database='crossrefeventdatamain')
cursor = connection.cursor()  

cursor.execute("SELECT COUNT(id) FROM dr_bowman_doi_data_tables._main_")
myresult = cursor.fetchall()

for count in myresult:
    totalRows = count[0]
    #print(totalRows)

#totalRows = totalRows - 1
currentRows = 0
#counter = 0

while currentRows < totalRows:
    '''
    #cursor.execute("SELECT DOI FROM dr_bowman_doi_data_tables._main_ LIMIT 1000 OFFSET \?", (currentRows))
    query = "SELECT DOI FROM dr_bowman_doi_data_tables._main_ LIMIT 1000 OFFSET " + str(currentRows)
    cursor.execute (query)
    myresult = cursor.fetchall()
    '''

    #query = "SELECT DOI FROM dr_bowman_doi_data_tables._main_ ORDER BY id LIMIT 1000 OFFSET 1000"
    query = "SELECT DOI FROM dr_bowman_doi_data_tables._main_ WHERE DOI IS NOT NULL ORDER BY id LIMIT 1000 OFFSET " + str(currentRows)
    cursor.execute(query)
    myresult = cursor.fetchall()
    #print(myresult[0])
    with open(filepath,'a', newline="") as csv_file:
        for i in myresult:
            writer = csv.writer(csv_file)
        
            #emptyStringCheck = i[0]
            #print(emptyStringCheck)
            writer.writerow([i[0]])
            #counter = counter + 1
            #print(counter)
            #writer.writerow([emptyStringCheck]) 

    currentRows = currentRows + 1000

    if currentRows > totalRows:
        currentRows = totalRows
    #print(currentRows)


'''
#query = "SELECT DOI FROM dr_bowman_doi_data_tables._main_ ORDER BY id LIMIT 1000 OFFSET 1000"
query = "SELECT DOI FROM dr_bowman_doi_data_tables._main_ WHERE DOI IS NOT NULL ORDER BY id LIMIT 1000 OFFSET 0"
cursor.execute(query)
myresult = cursor.fetchall()
#print(myresult[0])

with open(filepath,'a', newline="") as csv_file:
    for i in myresult:
        writer = csv.writer(csv_file)
        
        #emptyStringCheck = i[0]
        #print(emptyStringCheck)
        writer.writerow([i[0]])
        #writer.writerow([emptyStringCheck])   
'''