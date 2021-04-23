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

import os
import platform
import json
import argparse
import csv 
import pandas as pd
import crossref
import mysql.connector
import logging

#Author: Mohammad Tahmid
#Date: 01/31/2021
#Lines: 1-86
#Description: Takes "works" object metadata about author information and inserts it into the author table in the database. 
#UPDATE: This is during the beginning of version 2.0 of the author metadata insertion that was replaced later on in the development of this project. This took the metadata and later placed in directly into the MySQL database instead of filtering into MongoDB first

given_name = ""
family_name = ""
sequence = ""
affiliation = ""

def authorIngest(connection, cursor, doi, authorData):

    logging.basicConfig(filename='authorMetaDataIngest_log.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    #Query to get the foreign key when looking up a DOI
    query = "SELECT fk FROM doidata._main_ WHERE DOI = '%s'" % (doi)
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
        # TODO: 
        # 1. Split affilication infomration and adjust author table to account for the split in university, state, etc.
        ##################

        #Query to check if the record exists in the database
        query = """SELECT count(*) FROM doidata.author WHERE 
            given = '%s' AND 
            family = '%s' AND
            name = '%s' AND
            sequence = '%s' AND 
            affiliation = '%s' AND 
            fk = '%s'""" % (given_name, family_name, full_name, sequence, affiliationToInsert, fk)
        cursor.execute(query)
        resultSet = cursor.fetchall()
        count = resultSet[0][0]
        
        if not count > 0:

            #Query the database to insert the values as a row into the table
            query = "INSERT IGNORE INTO doidata.author(given, family, name, sequence, affiliation, fk) VALUES (%s, %s, %s, %s, %s, %s)"
            queryValues = (given_name, family_name, full_name, sequence, affiliationToInsert, fk)
            cursor.execute(query, queryValues)
            connection.commit()
            logging.info("Author metadata inserted for DOI: " + doi + " Name: " + full_name + " fk: " + str(fk))
        '''
        #Does a MySQL concatenation query to fill in the "name" column in the table
        query = "UPDATE doidata.author SET name = concat(given,' ',family)"
        cursor.execute(query)
        connection.commit()

		#Delete duplicate values if they exist in the table 
        query = """DELETE t1 FROM doidata.author t1 INNER JOIN doidata.author t2 WHERE 
        t1.id < t2.id AND 
        t1.family = t2.family AND 
        t1.given = t2.given AND 
        t1.name = t2.name AND 
        t1.sequence = t2.sequence AND 
        t1.fk = t2.fk"""
        cursor.execute(query)
        connection.commit()
        '''