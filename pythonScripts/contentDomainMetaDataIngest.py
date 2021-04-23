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
#Date: 02/03/2021
#Lines: 1-99
#Description: Takes "works" object metadata about content domain information and inserts it into content_domain in the databaase
#UPDATE: This is during the beginning of version 2.0 of the content domain information insertion that was replaced later on in the development of this project. This placed data into MySQL directly instead of using MongoDB.

crossmark_restriction = ""
domain = ""

def contentDomainIngest(connection, cursor, doi, contentDomainData):

    logging.basicConfig(filename='contentDomainMetaDataIngest_log.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    #Query to get the foreign key when looking up a DOI
    query = "SELECT fk FROM doidata._main_ WHERE DOI = '%s'" % (doi)
    cursor.execute(query)
    resultSet = cursor.fetchall()
    fk = resultSet[0][0]
    
    #From the "works" object for DOI, the data is split and saved to be used to query the database to insert the information
    try:
        crossmark_restriction = str(contentDomainData['crossmark-restriction'])
        
        if not ((crossmark_restriction == "True") or (crossmark_restriction == "False")):
            print("No \"crossmark-restriction\" for DOI: " + doi)
            crossmark_restriction = "" 

        domain = contentDomainData['domain']

        if not domain:
            print("No \"domain\" for DOI: " + doi)
            domain = ""
        else: 
            domain = domain[0]
    except:
        print("Unknown error in \"contentDomainMetaDataIngest.py\" for DOI: " + doi)

    #Query to check if the record exists in the database
    query = """SELECT count(*) FROM doidata.content_domain WHERE 
            crossmark_restriction = '%s' AND 
            domain = '%s' AND  
            fk = '%s'""" % (crossmark_restriction, domain, fk)
    cursor.execute(query)
    resultSet = cursor.fetchall()
    count = resultSet[0][0]

    if not count > 0:
        #Query the database to insert the values as a row into the table
        query = "INSERT IGNORE INTO doidata.content_domain(crossmark_restriction, domain, fk) VALUES (%s, %s, %s)"
        queryValues = (crossmark_restriction, domain, fk)
        cursor.execute(query, queryValues)
        connection.commit()
        logging.info("Author metadata inserted for DOI: " + doi + " fk: " + str(fk))

    '''
    #Delete duplicate values if they exist in the table
    query = """DELETE t1 FROM doidata.content_domain t1 INNER JOIN doidata.content_domain t2 
                WHERE 
                t1.id < t2.id AND
                t1.crossmark_restriction = t2.crossmark_restriction AND
                t1.domain = t2.domain AND
                t1.fk = t2.fk;"""
    cursor.execute(query)
    connection.commit()
    '''