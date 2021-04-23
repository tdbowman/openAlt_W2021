# Author: Darpan (whole file)
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
import json

# current directory 
path = os.getcwd() 
  
# parent directory 
parent = os.path.dirname(path) 
#config_path = os.path.join(path, "config", "openAltConfig.json")
config_path = "C:\\Users\\salsa\\Documents\\GitHub\\openAlt_W2021\\config\\openAltConfig.json"

# config file
f = open(config_path)
APP_CONFIG = json.load(f)


# Gets DOI event counts
def getDOIEventCounts(doi, cursor):
    query = "SELECT objectID, totalEvents, totalCrossrefEvents, totalDataciteEvents, totalF1000Events, totalHypothesisEvents, totalNewsfeedEvents, totalRedditEvents, totalRedditLinksEvents, totalStackExchangeEvents, totalTwitterEvents, totalWebEvents, totalWikipediaEvents, totalWordpressEvents FROM crossrefeventdatamain.main WHERE objectID LIKE '%" + doi + "%'"
    
    print('\n',"Retrieving Event Counts: " + doi)
    #print('\n',query)

    cursor.execute(query)
    resultSet = cursor.fetchall()
    
    if len(resultSet) == 0:
        print("DOI Event Counts Not Found\n")
    else:
        print("Event Counts Recieved!\n")
    
    return resultSet


# Gets DOI metadata
def getDOIMetadata(doi, cursor):

    # DOI Info Query
    query = "SELECT DOI, URL, title, container_title, name as authors, page, publisher, language, alternative_id, created_date_time, " \
                "deposited_date_time, is_referenced_by_count, issue, issued_date_parts, prefix, published_online_date_parts, published_print_date_parts " \
            "FROM doidata._main_ JOIN doidata.author ON doidata._main_.fk = doidata.author.fk " \
            "WHERE DOI = '" + doi + "'"
    
    print("Retrieving Metadata: " + doi)
    #print('\n',query)

    cursor.execute(query)
    resultSet = cursor.fetchall()

    #print('\nRESULT SET:',resultSet)
    if len(resultSet) == 0:
        print("DOI Metadata Not Found\n")
    else:
        print("DOI Metadata Recieved!\n")
    
    return resultSet


# Gets all event data for a DOI. Ex: wikipediaevent, twitterevent, redditevent, etc.
# Returns TWO dictionaries
def getDOIEvents(doi, cursor):
    # Array containing table names found in crossrefeventdatamain (except main)
    event_tables = ['cambiaevent','crossrefevent','dataciteevent', 'f1000event','hypothesisevent','newsfeedevent','redditevent','redditlinksevent','stackexchangeevent','twitterevent','webevent','wikipediaevent','wordpressevent']
    result = {}
    header = {}
    for table in event_tables:
        query = "SELECT * FROM crossrefeventdatamain." + table + " WHERE objectID LIKE '%" + doi + "%'"
        
        print("Retrieving " + table + " Event Data: " + doi)
        #print(query)

        cursor.execute(query)
        resultSet = cursor.fetchall()

        if len(resultSet) == 0:
            print(table + " Event Data Not Found\n")
        else:
            print(table + " Event Data recieved!\n")


        headers = [i[0] for i in cursor.description]
        header[table] = headers
        result[table] = resultSet

              
        
        
    
    #print('\nRESULT SET:',result)
    
    return(result,header)

# Gets citation data for DOI
def getDOICitations(doi, cursor):

    # DOI Info Query
    query = "SELECT citing as citations from opencitations.citations where citing = '" + doi + "' or cited = '" + doi + "'"
    
    print("Retrieving Citations: " + doi)
    #print('\n',query)

    cursor.execute(query)
    resultSet = cursor.fetchall()

    #print('\nRESULT SET:',resultSet)
    if len(resultSet) == 0:
        print("Citations Not Found\n")
    else:
        print("Citations Recieved!\n")
    
    return resultSet



# Gets author information
def getAuthorMetadata(author,cursor):
    # Author Info Query
    query = "SELECT affiliation, authenticated_orcid, family, given, name, orcid, sequence, suffix " \
                "FROM doidata.author where name LIKE " \
                "\'%" + author + "%\'" + ';'
    
    print("Retrieving Metadata: " + author)
    #print('\n',query)
    
    cursor.execute(query)    
    resultSet = cursor.fetchall()

    if len(resultSet) == 0:
        print("Author Not Found\n")
    else:
        print("Author Metadata Recieved!\n")

    return resultSet


# Gets DOIs associated with an author
def getAuthorArticles(author, cursor):

    # Author Associated DOIs Query
    query = "SELECT DOI, URL, title, container_title, name as author, page, publisher, language, alternative_id, created_date_time, " \
                "deposited_date_time, is_referenced_by_count, issue, issued_date_parts, prefix, published_online_date_parts, published_print_date_parts " \
            "FROM doidata._main_ JOIN doidata.author ON doidata._main_.fk = doidata.author.fk WHERE doidata.author.name  LIKE " \
                "\'%" + author + "%\'" + ';'

    print("Retrieving Articles: " + author)
    #print('\n',query)
    

    cursor.execute(query)
    resultSet = cursor.fetchall()

    if len(resultSet) == 0:
        print("Author Articles Not Found\n")
    else:
        print("Author Articles Recieved!\n")
    
    return resultSet


# Gets Authors associated with a university
def getUniAuthors(uni, cursor):
    # Author Info Query
    query = "SELECT affiliation, authenticated_orcid, family, given, name, orcid, sequence, suffix " \
                "FROM doidata.author where affiliation LIKE " \
                "\'%" + uni + "%\'" + ';'

    print("Retrieving University Authors: " + uni)
    #print('\n',query)

    cursor.execute(query)
    resultSet = cursor.fetchall()

    if len(resultSet) == 0:
        print("University Authors Not Found\n")
    else:
        print("University Authors Recieved!\n")

    return resultSet


# Gets DOIs associated with university
def getUniArticles(uni, cursor):
    query = "SELECT DOI, URL, title, container_title, name as authors, affiliation, page, publisher, language, alternative_id, created_date_time, " \
                "deposited_date_time, is_referenced_by_count, issue, issued_date_parts, prefix, published_online_date_parts, published_print_date_parts " \
            "FROM doidata._main_ JOIN doidata.author ON doidata._main_.fk = doidata.author.fk WHERE doidata.author.affiliation  LIKE " \
                "\'%" + uni + "%\'" + ';'
    
    print("Retrieving University DOIs: " + uni)
    #print('\n',query)

    cursor.execute(query)
    resultSet = cursor.fetchall()

    if len(resultSet) == 0:
        print("University DOIs Not Found\n")
    else:
        print("University DOIs Recieved!\n")
    
    return resultSet

# insert user stats into bulksearchstats table
def bulkSearchUserInsert(email, type, cursor, db):
    query = "INSERT INTO bulksearchStats.bulksearch (email, type) VALUES ('" + email + "', '" + type + "');" 
    cursor.execute(query)
    db.commit()

    
    print("User Stat Inserted")


# User Limit Check
def checkUser(email, type, cursor):

    limit = int(APP_CONFIG['User-Result-Limit']['limit'])
    interval = APP_CONFIG['User-Result-Limit']['dayInterval']

    query = "SELECT count(*) as count FROM bulksearchstats.bulksearch where time >=  NOW() - INTERVAL " + str(interval) + " DAY and email = '" + email + "' and type = '" + type + "'"
    cursor.execute(query)
    resultSet = cursor.fetchone()

    print(resultSet['count'])

    if int(resultSet['count']) >= limit:
        print("false:", resultSet['count'])
        return False
    else:
        return True
    

### Check IP Address (Not in use currently) ###
def checkIP(ip, type, cursor):
    limit = int(APP_CONFIG['User-Result-Limit']['limit'])
    interval = APP_CONFIG['User-Result-Limit']['dayInterval']

    ### IP address not included in table
    query = "SELECT count(*) as count FROM bulksearchstats.bulksearch where time >=  NOW() - INTERVAL " + str(interval) + " DAY and ip_addr = '" + ip + "' and type = '" + type + "'"
    cursor.execute(query)
    resultSet = cursor.fetchone()

    print(resultSet['count'])

    if resultSet['count'] >= limit:
        print("false:", resultSet['count'])
        return False
    else:
        return True



