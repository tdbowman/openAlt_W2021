# -----------------------------------------------------------------------------------------

# Copyright (c) 2020 tdbowman-CompSci-F2020
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# -----------------------------------------------------------------------------------------

# Author: Salsabil Bakth
# The purpose of this file is to retrieve the total records found 
# from the user's uploaded file in the bulk search. This result
# will be previewed on the email/download page.

# -----------------------------------------------------------------------------------------

import os
import csv
import pandas
import logging
import flask
import platform
import mysql
import shutil
import time
import datetime as dt

# -----------------------------------------------------------------------------------------

# Setter for stats
def setStats(x):
    global stats
    stats = str(x) + ' records found!'
    print(stats)

# -----------------------------------------------------------------------------------------

# Getter for stats
def getStats():
    return stats

# -----------------------------------------------------------------------------------------

# Setter for count 
def setCount(x):
    global count
    count = str(x)
    print(count)
    setStats(x)

# -----------------------------------------------------------------------------------------

# Getter for count
def getCount():
    return count

# -----------------------------------------------------------------------------------------

# Bulk Search by DOI
def uploadDOIList(mysql, fileName):

    # Directory of uploaded file
    dir = '../web/uploadFiles/' + fileName

    # Go through the content of the file and count
    getDOICount(mysql, dir)

# -----------------------------------------------------------------------------------------

def getDOICount(mysql, dir_csv):

    # directories
    dir_file = str(os.path.dirname(os.path.realpath(__file__)))

    # path of uploaded file
    dir_template = dir_csv

    # path of config file
    dir_config = dir_file + '\\uploadDOI_config.txt'

    # Set the logging parameters
    if not os.path.exists(dir_file + '\\Logs'):
        os.mkdir(dir_file + '\\Logs')
    logging.basicConfig(filename= dir_file + '\\Logs\\uploadDOI.log', filemode='a', level=logging.INFO,
        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  

    doi_arr = []

    # pandas library reads doi list
    doi_list = pandas.read_csv(dir_template, header=None)


    # adds doi values into array and prints the array
    for x in range(len(doi_list)):
        if x not in doi_arr:
            doi_arr.append(doi_list.values[x][0])


    # Reading config file to parse doi input to only include number
    config_arr = []
    config_file = open(dir_config,'r')

    # Reading config file line by line
    # Without the r strip, '\n' is added on to the value -> Ex. 'doi:\n'
    for line in config_file:
        config_arr.append(line.rstrip('\n'))  

    # Parse out doi formatting
    for config in config_arr:
        doi_arr = [doi.replace(config,'') for doi in doi_arr]

    # Remove duplicates from the doi array
    doi_arr = list(dict.fromkeys(doi_arr))

    # Join array for sql query
    joinedArr = "\'" + "','".join(doi_arr) + "\'"

    # Cursor makes connection with the db
    cursor = mysql.connection.cursor() 

    # Execute query to retrieve count from the list of DOIs in the array
    query = "SELECT count(*) FROM doidata._main_ WHERE DOI in (" + joinedArr + ")"
    cursor.execute(query)

    # Store count result in var
    resultSet = cursor.fetchone()
    
    # Pass query result to set the count function
    setCount(resultSet["count(*)"])

# -----------------------------------------------------------------------------------------

# Bulk Search by Author
def uploadAuthorList (mysql, fileName):

    # Directory of doi list
    dir = '../web/uploadFiles/' + fileName

    # Go through the content of the file and count
    getAuthorCount(mysql, dir)

# -----------------------------------------------------------------------------------------

def getAuthorCount(mysql, dir_csv):
    # Directories 
    dir_file = str(os.path.dirname(os.path.realpath(__file__)))

    # Path of uploaded file
    dir_template = dir_csv

    # Path of results folde with current time
    if not os.path.exists(dir_file + '\\Results'):
        os.mkdir(dir_file + '\\Results')

    dir_results = dir_file + '\\Results\\authorEvents_' + str(dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

    # Create folder to hold results
    if not os.path.exists(dir_results):
        os.mkdir(dir_results)

    # Set the logging parameters
    if not os.path.exists(dir_file + '\\Logs'):
        os.mkdir(dir_file + '\\Logs')

    logging.basicConfig(filename=dir_file + '\\Logs\\uploadAuthor.log', filemode='a', level=logging.INFO,
        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  

    # Array containing authors listed in uploaded file
    author_arr = []

    # Pandas library reads doi list
    author_list = pandas.read_csv(dir_template, header=None)

    # Adds doi values into array and prints the array
    for x in range(len(author_list)):
        author_arr.append(author_list.values[x][0].lower())

    # Remove duplicates from author array
    author_arr = list(dict.fromkeys(author_arr))
    
    # Initialize the query statement
    query = "SELECT count(*) FROM doidata.author where name like \'%" + author_arr[0] + "%\'"

    # Build the query statement by iterating through the array 
    for author in author_arr[1:]:
        query = query + " OR name like \'%" + author + "%\'"  

    # Set up cursor to run SQL query
    cursor = mysql.connection.cursor()  

    # Executre the query and store the result in a var
    cursor.execute(query)
    resultSet = cursor.fetchone()
    
    # Pass query result to set the count function
    setCount(resultSet["count(*)"])

# -----------------------------------------------------------------------------------------

# Bulk Search by University
def uploadUniList(mysql, fileName):

    # Directory of doi list
    dir = '../web/uploadFiles/' + fileName

    # Go through the content of the file and count
    getUniCount(mysql, dir)

# -----------------------------------------------------------------------------------------

def getUniCount(mysql, dir_csv):

    # Directories
    dir_file = str(os.path.dirname(os.path.realpath(__file__)))

    # Path of uploaded file
    dir_template = dir_csv

    # Path of results folde with current time
    if not os.path.exists(dir_file + '\\Results'):
        os.mkdir(dir_file + '\\Results')

    dir_results = dir_file + '\\Results\\universityEvents_' + \
        str(dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

    # Create folder to hold results
    if not os.path.exists(dir_results):
        os.mkdir(dir_results)

    # Set the logging parameters
    if not os.path.exists(dir_file + '\\Logs'):
        os.mkdir(dir_file + '\\Logs')
    logging.basicConfig(filename=dir_file + '\\Logs\\uploadUniversity.log', filemode='a', level=logging.INFO,
                        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    # Array containing universities listed in uploaded file
    uni_arr = []

    # Pandas library reads doi list
    uni_list = pandas.read_csv(dir_template, header=None)

    # Adds doi values into array and prints the array
    for x in range(len(uni_list)):
        uni_arr.append(uni_list.values[x][0].lower())

    # Remove duplicates from author array
    uni_arr = list(dict.fromkeys(uni_arr))

    # Initialize the query statement
    query = "SELECT count(distinct university) FROM doidata.author where affiliation like \'%" + uni_arr[0] + "%\'"

    # Build the query statement by iterating through the array 
    for university in uni_arr[1:]:
        query = query + " OR affiliation like \'%" + university + "%\'"

    # Cursor makes connection with the db
    cursor = mysql.connection.cursor() 

    # Executre the query and store the result in a var
    cursor.execute(query)
    resultSet = cursor.fetchone()

    # Pass query result to set the count function
    setCount(resultSet["count(distinct university)"])

# -----------------------------------------------------------------------------------------