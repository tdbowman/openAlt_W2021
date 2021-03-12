# Author: Darpan
######## Darpan Start ########

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
            "FROM doidata._main_ JOIN doidata.author ON doidata._main_.id = doidata.author.fk " \
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
            "FROM doidata._main_ JOIN doidata.author ON doidata._main_.id = doidata.author.fk WHERE doidata.author.name  LIKE " \
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
            "FROM doidata._main_ JOIN doidata.author ON doidata._main_.id = doidata.author.fk WHERE doidata.author.affiliation  LIKE " \
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
















######## Darpan End ########
