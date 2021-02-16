import os
import platform
import json
import argparse
import csv 
import pandas as pd
import crossref
import mysql.connector
import logging
from getCountry import extract_country
from getUniversity import extract_university



#Author: Mohammad Tahmid
#Date: 01/31/2021
#Description: Takes "works" object metadata about author information and inserts it into the author table in the databaase

given_name = ""
family_name = ""
sequence = ""
affiliation = ""

def authorIngest(connection, cursor, doi, authorData):

    logging.basicConfig(filename='authorMetaDataIngest_log.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    #Query to get the foreign key when looking up a DOI
    query = "SELECT fk FROM dr_bowman_doi_data_tables._main_ WHERE DOI = '%s'" % (doi)
    cursor.execute(query)
    resultSet = cursor.fetchall()
    fk = resultSet[0][0]

    #From the "works" object for DOI, the data is split and saved to be used to query the databse to insert the information
    for index, authorValue in enumerate(authorData):

        given_name = authorValue['given']
        family_name = authorValue['family']
        full_name = given_name + " " + family_name
        sequence = authorValue['sequence']
        affiliation = authorValue['affiliation']
        affiliationToInsert = ""

        for index, affiliationData in enumerate(affiliation):
            affiliationToInsert= affiliationData['name']

        ##################
        # Split affiliation information into country and university

        country = extract_country(affiliation)
        university = extract_university(affiliation)
        
        ##################

        #Query to check if the record exists in the database
        query = """SELECT count(*) FROM dr_bowman_doi_data_tables.author WHERE 
            given = '%s' AND 
            family = '%s' AND
            name = '%s' AND
            sequence = '%s' AND 
            affiliation = '%s' AND 
            country = '%s' AND
            university = '%s' AND
            fk = '%s'""" % (given_name, family_name, full_name, sequence, affiliationToInsert, country, university, fk)
        cursor.execute(query)
        resultSet = cursor.fetchall()
        count = resultSet[0][0]
        
        if not count > 0:

            #Query the database to insert the values as a row into the table
            query = "INSERT IGNORE INTO dr_bowman_doi_data_tables.author(given, family, name, sequence, affiliation, country, university, fk) VALUES (%s, %s, %s, %s, %s, %s)"
            queryValues = (given_name, family_name, full_name, sequence, affiliationToInsert, country, university, fk)
            cursor.execute(query, queryValues)
            connection.commit()
            logging.info("Author metadata inserted for DOI: " + doi + " Name: " + full_name + " fk: " + str(fk))
        '''
        #Does a MySQL concatenation query to fill in the "name" column in the table
        query = "UPDATE dr_bowman_doi_data_tables.author SET name = concat(given,' ',family)"
        cursor.execute(query)
        connection.commit()

		#Delete duplicate values if they exist in the table 
        query = """DELETE t1 FROM dr_bowman_doi_data_tables.author t1 INNER JOIN dr_bowman_doi_data_tables.author t2 WHERE 
        t1.id < t2.id AND 
        t1.family = t2.family AND 
        t1.given = t2.given AND 
        t1.name = t2.name AND 
        t1.sequence = t2.sequence AND 
        t1.fk = t2.fk"""
        cursor.execute(query)
        connection.commit()
        '''