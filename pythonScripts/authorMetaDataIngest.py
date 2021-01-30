import json
import argparse
import pandas as pd
import csv 
import os
import crossref
import platform
import mysql.connector

given_name = ""
family_name = ""
full_name = ""
sequence = ""
affiliation = ""

'''
mysql_username = "root"
mysql_password = "Hamtramck#1999"
connection = mysql.connector.connect(user=str(mysql_username), password=str(
        mysql_password), host='127.0.0.1', database='crossrefeventdatamain')
cursor = connection.cursor()
cursor2 = connection.cursor()
'''
'''
#query = "SELECT fk FROM dr_bowman_doi_data_tables._main_ WHERE DOI=?"

doi = "10.1177/070674379704200909"
query = "SELECT fk FROM dr_bowman_doi_data_tables._main_ WHERE DOI = '%s'" % (doi)
cursor.execute(query)
fk = cursor.fetchall()


print(fk)
numba = fk[0][0]
#numba = 0 + numba

print(numba)
#nameA = ("tim turner", 2)


#query2 = "insert into dr_bowman_doi_data_tables.author(name, fk) values('%s')" % (nameA)


sql = "INSERT INTO dr_bowman_doi_data_tables.author(name, fk) VALUES (%s, %s) ON DUPLICATE KEY UPDATE id=id"
nameA = ("tim turner", )
cursor.execute(sql, nameA)
connection.commit()
'''

def authorIngest(connection, cursor, doi, authorData):

    query = "SELECT fk FROM dr_bowman_doi_data_tables._main_ WHERE DOI = '%s'" % (doi)
    cursor.execute(query)
    resultSet = cursor.fetchall()
    fk = resultSet[0][0]

    #print(authorData)

    
    for index, authorValue in enumerate(authorData):
        given_name = authorValue['given']
        family_name = authorValue['family']
        full_name = given_name + " " + family_name
        sequence = authorValue['sequence']
        affiliation = authorValue['affiliation']
        affiliationToInsert = ""

        for index, affiliationData in enumerate(affiliation):
            affiliationToInsert= affiliationData['name']

        #print(given_name)
        #print(family_name)
        #print(full_name)
        #print(sequence)

        queryValues = (given_name, family_name, full_name, sequence, affiliationToInsert, fk)
        query = "INSERT INTO dr_bowman_doi_data_tables.author(given, family, name, sequence, affiliation, fk) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE id=id"

        # TODO: 
        # 1. Split affilication infomration and adjust author table to account for the split in university, state, etc.

        cursor.execute(query, queryValues)
        connection.commit()
    