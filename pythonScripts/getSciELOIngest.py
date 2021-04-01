import os 
import logging
import mysql.connector 

#Author: Mohammad Tahmid
#Date: 03/10/2021
#Lines: 1-217
#Description: This python script takes document info from MongoDB and fitlers and places it into the MySQL database.

def PIDtoDOIInsertSQL(connection, cursor, doiInfo, logging):
    
    foundDOI = ""
    foundURL = ""
    foundAlternateID = ""
    foundContainerTitle = ""
    foundCreatedDatePart = ""
    foundCreatedDateTime = ""
    foundCreatedDateTimestamp = ""
    foundDepositedDatePart = ""
    foundDepositedDateTime = ""
    foundDepositedTimestamp = ""
    foundIndexedDatePart = ""
    foundIndexedDateTime = ""
    foundIndexedTimestamp = ""
    foundIsReferencedByCount = ""
    foundIssue = ""
    foundIssuedDatePart = ""
    foundLanguage = ""
    foundMember = ""
    foundOriginalTitle = ""
    foundPage = ""
    foundPrefix = ""
    foundPublishedPrintDatePart = ""
    foundPublisher = ""
    foundReferenceCount = ""
    foundReferencesCount = ""
    foundScore = ""
    foundShortContainerTitle = ""
    foundShortTitle = ""
    foundSource = ""
    foundSubtitle = ""
    foundTitle = ""
    foundType = ""
    foundVolume = ""
    foundfk = ""

    foundDOI = doiInfo['DOI']
    foundURL = doiInfo['URL']
    #foundAlternateID = doiInfo['alternative-id'][0]

    if not doiInfo['alternative-id'][0]:
        foundAlternateID = ""
    else:
        foundAlternateID = doiInfo['alternative-id'][0]

    foundContainerTitle = doiInfo['container-title'][0]


    #foundCreatedDatePart = str(doiInfo['created']['date-parts'][0][0])
    #foundCreatedDatePart = foundCreatedDatePart + "/" + str(doiInfo['created']['date-parts'][0][1])
    #foundCreatedDatePart = foundCreatedDatePart + "/" + str(doiInfo['created']['date-parts'][0][2])

    listLength = len(doiInfo['created']['date-parts'][0])
    for x in (range(listLength)):
        if (x == listLength - 1):
            foundCreatedDatePart = foundCreatedDatePart + str(doiInfo['created']['date-parts'][0][x])
        else:
            foundCreatedDatePart = foundCreatedDatePart + str(doiInfo['created']['date-parts'][0][x]) + "/"

    foundCreatedDateTime = doiInfo['created']['date-time']
    foundCreatedDateTime = foundCreatedDateTime.replace("T", " ")
    foundCreatedDateTime = foundCreatedDateTime.replace("Z", "")
    foundCreatedDateTimestamp = doiInfo['created']['timestamp']


    #foundDepositedDatePart = str(doiInfo['deposited']['date-parts'][0][0])
    #foundDepositedDatePart = foundDepositedDatePart + "/" + str(doiInfo['deposited']['date-parts'][0][1])
    #foundDepositedDatePart = foundDepositedDatePart + "/" + str(doiInfo['deposited']['date-parts'][0][2])

    listLength = len(doiInfo['deposited']['date-parts'][0])
    for x in (range(listLength)):
        if (x == listLength - 1):
            foundDepositedDatePart = foundDepositedDatePart + str(doiInfo['deposited']['date-parts'][0][x])
        else:
            foundDepositedDatePart = foundDepositedDatePart + str(doiInfo['deposited']['date-parts'][0][x]) + "/"

    foundDepositedDateTime = doiInfo['deposited']['date-time']
    foundDepositedDateTime = foundDepositedDateTime.replace("T", " ")
    foundDepositedDateTime = foundDepositedDateTime.replace("Z", "")
    foundDepositedTimestamp = doiInfo['deposited']['timestamp']


    #foundIndexedDatePart = str(doiInfo['indexed']['date-parts'][0][0])
    #foundIndexedDatePart = foundIndexedDatePart + "/" + str(doiInfo['indexed']['date-parts'][0][1])
    #foundIndexedDatePart = foundIndexedDatePart + "/" + str(doiInfo['indexed']['date-parts'][0][2])

    listLength = len(doiInfo['indexed']['date-parts'][0])
    for x in (range(listLength)):
        if (x == listLength - 1):
            foundIndexedDatePart = foundIndexedDatePart + str(doiInfo['indexed']['date-parts'][0][x])
        else:
            foundIndexedDatePart = foundIndexedDatePart + str(doiInfo['indexed']['date-parts'][0][x]) + "/"

    foundIndexedDateTime = doiInfo['indexed']['date-time']
    foundIndexedDateTime = foundIndexedDateTime.replace("T", " ")
    foundIndexedDateTime = foundIndexedDateTime.replace("Z", "")
    foundIndexedTimestamp = doiInfo['indexed']['timestamp']

    foundIsReferencedByCount = doiInfo['is-referenced-by-count']
    foundIssue = doiInfo['issue']

    listLength = len(doiInfo['issued']['date-parts'][0])
    for x in (range(listLength)):
        if (x == listLength - 1):
            foundIssuedDatePart = foundIssuedDatePart + str(doiInfo['issued']['date-parts'][0][x])
        else:
            foundIssuedDatePart = foundIssuedDatePart + str(doiInfo['issued']['date-parts'][0][x]) + "/"

    default = ""
    foundLanguage = doiInfo.get("language", default)

    foundMember = doiInfo['member']

    if not doiInfo['original-title']:
        foundOriginalTitle = "None"
    else:
        foundOriginalTitle = doiInfo['original-title']
    
    if not doiInfo['page']:
        foundPage = ""
    else:
        foundPage = doiInfo['page']
    
    foundPrefix = doiInfo['prefix']

    if doiInfo['published-print']['date-parts'][0]:
        foundPublishedPrintDatePart = ""
    else:
        listLength = len(doiInfo['published-print']['date-parts'][0])
        for x in (range(listLength)):
            if (x == listLength - 1):
                foundPublishedPrintDatePart = foundPublishedPrintDatePart + str(doiInfo['published-print']['date-parts'][0][x])
            else:
                foundPublishedPrintDatePart = foundPublishedPrintDatePart + str(doiInfo['published-print']['date-parts'][0][x]) + "/"

    foundPublisher = doiInfo['publisher']

    foundReferenceCount = doiInfo['reference-count']

    foundReferencesCount = doiInfo['references-count']

    foundScore = doiInfo['score']

    if not doiInfo['short-container-title'][0]:
        foundShortContainerTitle = "None"
    else:
        foundShortContainerTitle = doiInfo['short-container-title'][0]

    if not doiInfo['short-title']:
        foundShortTitle = "None"
    else:
        foundShortTitle = doiInfo['short-title']
    
    foundSource = doiInfo['source']

    if not doiInfo['subtitle']:
        foundSubtitle = "None"
    else:
        foundSubtitle = doiInfo['subtitle']

    if not doiInfo['title'][0]:
        foundTitle = "None"
    else:
        foundTitle = doiInfo['title'][0]

    foundType = doiInfo['type']

    if not doiInfo['volume']:
        foundVolume = ""
    else:
        foundVolume = doiInfo['volume']

    query = """SELECT MAX(fk) FROM doidata._main_;"""
    cursor.execute(query)
    resultSet = cursor.fetchall()
    count = int(resultSet[0][0])
    
    foundfk = count + 1

    '''
    print(foundDOI, foundURL, foundAlternateID, foundContainerTitle, foundCreatedDatePart, foundCreatedDateTime, 
        foundCreatedDateTimestamp, foundDepositedDatePart, foundDepositedDateTime, foundDepositedTimestamp, foundIndexedDatePart,
        foundIndexedDateTime, foundIndexedTimestamp, foundIsReferencedByCount, foundIssue, foundIssuedDatePart, foundLanguage,
        foundMember, foundOriginalTitle, foundPage, foundPrefix, foundPublishedPrintDatePart, foundPublisher,foundReferenceCount, 
        foundReferencesCount, foundScore, foundShortContainerTitle, foundShortTitle, foundSource, foundSubtitle, foundTitle, foundType, 
        foundVolume, foundfk)
    '''
    
    query = """INSERT IGNORE INTO doidata._main_(DOI, URL, alternative_id, container_title, created_date_parts, created_date_time, 
            created_timestamp, deposited_date_parts, deposited_date_time, deposited_timestamp, 
            indexed_date_parts, indexed_date_time, indexed_timestamp, is_referenced_by_count, issue, 
            issued_date_parts, language, member, original_title, page, prefix, published_print_date_parts,
            publisher, reference_count, references_count, score, short_container_title, short_title, source, subtitle, title, 
            type, volume, fk) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    queryValues = (foundDOI, foundURL, foundAlternateID, foundContainerTitle, foundCreatedDatePart, foundCreatedDateTime, 
        foundCreatedDateTimestamp, foundDepositedDatePart, foundDepositedDateTime, foundDepositedTimestamp, foundIndexedDatePart,
        foundIndexedDateTime, foundIndexedTimestamp, foundIsReferencedByCount, foundIssue, foundIssuedDatePart, foundLanguage,
        foundMember, foundOriginalTitle, foundPage, foundPrefix, foundPublishedPrintDatePart, foundPublisher,foundReferenceCount, 
        foundReferencesCount, foundScore, foundShortContainerTitle, foundShortTitle, foundSource, foundSubtitle, foundTitle, foundType, 
        foundVolume, foundfk)

    #print(foundDOI)
        
    #cursor.execute(query, queryValues)
    #connection.commit()

    logging.info("Added DOI: " + foundDOI)  


    return queryValues