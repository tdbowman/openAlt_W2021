import os
import argparse
import csv
import crossref
import mysql.connector
import getpass

"""
MIT License

Copyright (c) 2020 tdbowman-CompSci-F2020

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#Author: Mohammad Tahmid
#Date: 01/28/2021
#Lines: 1-92
#Description: Gathers a list of all DOI's in the database and saves it to a .csv in the same directory as this script
#UPDATE: This is during the beginning of version 2.0 of the project that was replaced later on in the development of this project. This placed data in directly into the MySQL database instead of filtering into MongoDB first

#Establlish a connection to the MySQL server to the correct database
print("MySQL Credentials")

#Gets username information from user
mysql_username = input("Username: ")

#Gets password information from user (WHEN TYPING THE PASSWORD IN, IT WILL BE HIDDEN BUT LETTERS ARE BEING ENTERED IN)
mysql_password = getpass.getpass("Password: ")

#Set directory path
directoryName = os.path.dirname(os.path.realpath(__file__))
savingFilePath = str(directoryName) + str("\\gatherDOI_csv.csv")

#Establish a connection to the databse
connection = mysql.connector.connect(user=str(mysql_username), password=str(
        mysql_password), host='127.0.0.1', database='crossrefeventdatamain')

cursor = connection.cursor()

#Find the total number of DOI's from the database
cursor.execute("SELECT COUNT(id) FROM doidata._main_")
myresult = cursor.fetchall()

#Store the DOI count into a variable
for count in myresult:
    totalRows = count[0]

def main():

    #Tracks the row that is entered in from the DOI list.
    currentRows = 0
    
    #Getting DOI continues till the whole list of is saved in the .csv
    while currentRows < totalRows:
  
        #Query to get DOI's from the database with 1000 rows at a time
        query = "SELECT DOI FROM doidata._main_ WHERE DOI IS NOT NULL ORDER BY id LIMIT 1000 OFFSET " + str(currentRows)
        cursor.execute(query)
        resultSet = cursor.fetchall()

        #Open's the .csv file to write to it
        with open(savingFilePath,'a', newline="") as csvFile:
            for i in resultSet:

                #Write DOI to the csv file in the "filepath variable"
                writer = csv.writer(csvFile)
                writer.writerow([i[0]]) 

        #Increases counter to keep track of whether at the end the 1000 row result
        currentRows = currentRows + 1000
        if currentRows > totalRows:
            currentRows = totalRows

if __name__ == '__main__':
    main()