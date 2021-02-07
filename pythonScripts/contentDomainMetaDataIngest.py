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
#Description: Takes "works" object metadata about content domain information and inserts it into content_domain in the databaase

crossmark_restriction = ""
domain = ""

def contentDomainIngest(connection, cursor, doi, contentDomainData):

    logging.basicConfig(filename='contentDomainMetaDataIngest_log.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    #Query to get the foreign key when looking up a DOI
    query = "SELECT fk FROM dr_bowman_doi_data_tables._main_ WHERE DOI = '%s'" % (doi)
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
    query = """SELECT count(*) FROM dr_bowman_doi_data_tables.content_domain WHERE 
            crossmark_restriction = '%s' AND 
            domain = '%s' AND  
            fk = '%s'""" % (crossmark_restriction, domain, fk)
    cursor.execute(query)
    resultSet = cursor.fetchall()
    count = resultSet[0][0]

    if not count > 0:
        #Query the database to insert the values as a row into the table
        query = "INSERT IGNORE INTO dr_bowman_doi_data_tables.content_domain(crossmark_restriction, domain, fk) VALUES (%s, %s, %s)"
        queryValues = (crossmark_restriction, domain, fk)
        cursor.execute(query, queryValues)
        connection.commit()
        logging.info("Author metadata inserted for DOI: " + doi + " fk: " + str(fk))

    '''
    #Delete duplicate values if they exist in the table
    query = """DELETE t1 FROM dr_bowman_doi_data_tables.content_domain t1 INNER JOIN dr_bowman_doi_data_tables.content_domain t2 
                WHERE 
                t1.id < t2.id AND
                t1.crossmark_restriction = t2.crossmark_restriction AND
                t1.domain = t2.domain AND
                t1.fk = t2.fk;"""
    cursor.execute(query)
    connection.commit()
    '''