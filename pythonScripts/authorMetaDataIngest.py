import os
import platform
import json
import argparse
import csv 
import pandas as pd
import crossref
import mysql.connector

#Author: Mohammad Tahmid
#Date: 01/31/2021
#Description: Takes "works" object metadata about author information and inserts it into the author table in the databaase

given_name = ""
family_name = ""
sequence = ""
affiliation = ""

def authorIngest(connection, cursor, doi, authorData):

    #Query to get the foreign key when looking up a DOI
    query = "SELECT fk FROM dr_bowman_doi_data_tables._main_ WHERE DOI = '%s'" % (doi)
    cursor.execute(query)
    resultSet = cursor.fetchall()
    fk = resultSet[0][0]

    #From the "works" object for DOI, the data is split and saved to be used to query the databse to insert the information
    for index, authorValue in enumerate(authorData):

        given_name = authorValue['given']
        family_name = authorValue['family']
        sequence = authorValue['sequence']
        affiliation = authorValue['affiliation']
        affiliationToInsert = ""

        for index, affiliationData in enumerate(affiliation):
            affiliationToInsert= affiliationData['name']

        ##################
        # TODO: 
        # 1. Split affilication infomration and adjust author table to account for the split in university, state, etc.
        ##################

        #Query the database to insert the values as a row into the table
        query = "INSERT INTO dr_bowman_doi_data_tables.author(given, family, sequence, affiliation, fk) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE id=id"
        queryValues = (given_name, family_name, sequence, affiliationToInsert, fk)
        cursor.execute(query, queryValues)
        connection.commit()

        #Does a MySQL concatenation query to fill in the "name" column in the table
        query = "UPDATE dr_bowman_doi_data_tables.author SET name = concat(given,' ',family)"
        cursor.execute(query)
        connection.commit()
    