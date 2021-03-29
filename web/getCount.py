# Author: Salsabil Bakth
# The purpose of this file is to retrieve the total records found 
# from the user's uploaded file in the doidata table. This result
# will be displayed on the email page.

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

# Setter for stats
def setStats(x):
    global stats
    stats = str(x) + ' records found!'
    print(stats)

# Getter for stats
def getStats():
    return stats

def setCount(x):
    global count
    count = str(x)
    print(count)
    setStats(x)

# Getter for stats
def getCount():
    return count

def uploadDOIList(mysql, fileName):

    # Directory of uploaded file
    dir = '../web/uploadFiles/' + fileName

    # downloadDOI(mysql, dir, type, email)
    getDOICount(mysql, dir)

    # Delete uploaded files
    if os.path.exists(dir):
        os.remove(dir)

    count = getCount()

    if count == "0":
        return flask.render_template('noResultsPage.html')
    else:
        return flask.render_template('downloadDOI.html', results = getStats())

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

    # # Join array for sql query
    joinedArr = "\'" + "','".join(doi_arr) + "\'"

    #Cursor makes connection with the db
    cursor = mysql.connection.cursor() 

    query = "SELECT count(*) FROM doidata._main_ WHERE DOI in (" + joinedArr + ")"
    cursor.execute(query)
    resultSet = cursor.fetchone()
    
    setCount(resultSet["count(*)"])

def uploadAuthorList (mysql, fileName):

    # Directory of doi list
    dir = '../web/uploadFiles/' + fileName

    getAuthorCount(mysql, dir)

    # Delete uploaded file
    if os.path.exists(dir):
        os.remove(dir)

    return flask.render_template('downloadAuthors.html', results = getStats())

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
    
    query = "SELECT count(*) FROM doidata.author where name like \'%" + author_arr[0] + "%\'"

    for author in author_arr[1:]:
        query = query + " OR name like \'%" + author + "%\'"  

    # Set up cursor to run SQL query
    cursor = mysql.connection.cursor()  

    cursor.execute(query)
    resultSet = cursor.fetchone()
    
    setCount(resultSet["count(*)"])

def uploadUniList(mysql, fileName):

    # Directory of doi list
    dir = '../web/uploadFiles/' + fileName

    getUniCount(mysql, dir)

    # Delete uploaded file
    if os.path.exists(dir):
        os.remove(dir)

    return flask.render_template('downloadUni.html', results=getStats())

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

    query = "SELECT count(distinct university) FROM doidata.author where affiliation like \'%" + uni_arr[0] + "%\'"

    for university in uni_arr[1:]:
        query = query + " OR affiliation like \'%" + university + "%\'"

    #Cursor makes connection with the db
    cursor = mysql.connection.cursor() 

    cursor.execute(query)
    resultSet = cursor.fetchone()

    setCount(resultSet["count(distinct university)"])