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
import logging
import mysql.connector 

#Author: Mohammad Tahmid
#Date: 03/10/2021
#Lines: 1-316
#Description: This python script takes document info from MongoDB and fitlers it into a list of values to be returned and later inserted into the MySQL database

def PIDtoDOIInsertSQL(connection, cursor, doiInfo, logging):
    
	#Variables to hold the data for the MySQL query that is inserted later on
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

	#The value for "DOI is saved
    foundDOI = doiInfo['DOI']
	
	#----------------------------------------------------------------------
	
	#The value for "URL" is saved
    foundURL = doiInfo['URL']
	
	#----------------------------------------------------------------------
	
	#The value for "alternative-id" is saved if it is not a NULL value
    if not doiInfo['alternative-id'][0]:
        foundAlternateID = ""
    else:
        foundAlternateID = doiInfo['alternative-id'][0]
	
	#----------------------------------------------------------------------
	
	#The value for "container-title" is saved if it is not a NULL value
    foundContainerTitle = doiInfo['container-title'][0]
	
	#----------------------------------------------------------------------

	#The range for "created_date_parts" is found to see if the month, day, and year is found 
    listLength = len(doiInfo['created']['date-parts'][0])
    
	#Creates a string with the whole date
    for x in (range(listLength)):
        if (x == listLength - 1):
            foundCreatedDatePart = foundCreatedDatePart + str(doiInfo['created']['date-parts'][0][x])
        else:
            foundCreatedDatePart = foundCreatedDatePart + str(doiInfo['created']['date-parts'][0][x]) + "/"
	
	#----------------------------------------------------------------------

	#Take the 'date-time" value and replaces some of the letters in the string from Crossref with spaces so it can be inserted into the MySQL database
    foundCreatedDateTime = doiInfo['created']['date-time']
    foundCreatedDateTime = foundCreatedDateTime.replace("T", " ")
    foundCreatedDateTime = foundCreatedDateTime.replace("Z", "")
	
	#----------------------------------------------------------------------
	
	#The value for "timestamp" is saved
    foundCreatedDateTimestamp = doiInfo['created']['timestamp']
	
	#----------------------------------------------------------------------

	#The range for "deposited_date_parts" is found to see if the month, day, and year is found
    listLength = len(doiInfo['deposited']['date-parts'][0])
	
	#Creates a string with the whole date
    for x in (range(listLength)):
        if (x == listLength - 1):
            foundDepositedDatePart = foundDepositedDatePart + str(doiInfo['deposited']['date-parts'][0][x])
        else:
            foundDepositedDatePart = foundDepositedDatePart + str(doiInfo['deposited']['date-parts'][0][x]) + "/"
			
	#----------------------------------------------------------------------

	#Take the 'deposited_date-time" value and replaces some of the letters in the string from Crossref with spaces so it can be inserted into the MySQL database
    foundDepositedDateTime = doiInfo['deposited']['date-time']
    foundDepositedDateTime = foundDepositedDateTime.replace("T", " ")
    foundDepositedDateTime = foundDepositedDateTime.replace("Z", "")
	
	#----------------------------------------------------------------------
	
	#The value for "timestamp" is saved
    foundDepositedTimestamp = doiInfo['deposited']['timestamp']

	#----------------------------------------------------------------------

	#The range for "indexed_date_parts" is found to see if the month, day, and year is found
    listLength = len(doiInfo['indexed']['date-parts'][0])
	
	#Creates a string with the whole date
    for x in (range(listLength)):
        if (x == listLength - 1):
            foundIndexedDatePart = foundIndexedDatePart + str(doiInfo['indexed']['date-parts'][0][x])
        else:
            foundIndexedDatePart = foundIndexedDatePart + str(doiInfo['indexed']['date-parts'][0][x]) + "/"
	
	#----------------------------------------------------------------------

	#Take the 'deposited_date-time" value and replaces some of the letters in the string from Crossref with spaces so it can be inserted into the MySQL database
    foundIndexedDateTime = doiInfo['indexed']['date-time']
    foundIndexedDateTime = foundIndexedDateTime.replace("T", " ")
    foundIndexedDateTime = foundIndexedDateTime.replace("Z", "")
	
	#----------------------------------------------------------------------
	
	#The value for "timestamp" is saved
    foundIndexedTimestamp = doiInfo['indexed']['timestamp']
	
	#----------------------------------------------------------------------

	#The value for "is_referenced_count" is saved
    foundIsReferencedByCount = doiInfo['is-referenced-by-count']
	
	#----------------------------------------------------------------------
	
	#The value for "issue" is saved
    foundIssue = doiInfo['issue']
	
	#----------------------------------------------------------------------

	#The range for "indexed_date_parts" is found to see if the month, day, and year is found
    listLength = len(doiInfo['issued']['date-parts'][0])
	
	#Creates a string with the whole date
    for x in (range(listLength)):
        if (x == listLength - 1):
            foundIssuedDatePart = foundIssuedDatePart + str(doiInfo['issued']['date-parts'][0][x])
        else:
            foundIssuedDatePart = foundIssuedDatePart + str(doiInfo['issued']['date-parts'][0][x]) + "/"

    #----------------------------------------------------------------------
	
    default = ""
    foundLanguage = doiInfo.get("language", default)

	#----------------------------------------------------------------------
	
	#The value for "member" is saved
    foundMember = doiInfo['member']

	#----------------------------------------------------------------------
	
	#The value for "issue" is saved
    if not doiInfo['original-title']:
        foundOriginalTitle = "None"
    else:
        foundOriginalTitle = doiInfo['original-title']
		
	#----------------------------------------------------------------------
    
	#The value for "ipage" is saved if not empty
    if not doiInfo['page']:
        foundPage = ""
    else:
        foundPage = doiInfo['page']
		
	#----------------------------------------------------------------------
    
	#The value for "prefix" is saved
    foundPrefix = doiInfo['prefix']
	
	#----------------------------------------------------------------------

	#The value for "published_date_parts" is saved
    if doiInfo['published-print']['date-parts'][0]:
        foundPublishedPrintDatePart = ""
    else:
		
		#The range is found to see if month, day, and year exist and make the string accordingly
        listLength = len(doiInfo['published-print']['date-parts'][0])
        for x in (range(listLength)):
            if (x == listLength - 1):
                foundPublishedPrintDatePart = foundPublishedPrintDatePart + str(doiInfo['published-print']['date-parts'][0][x])
            else:
                foundPublishedPrintDatePart = foundPublishedPrintDatePart + str(doiInfo['published-print']['date-parts'][0][x]) + "/"
	
	#----------------------------------------------------------------------

	#The value for "publisher" is saved
    foundPublisher = doiInfo['publisher']
	
	#----------------------------------------------------------------------
	
	#The value for "reference_count" is saved
    foundReferenceCount = doiInfo['reference-count']
	
	#----------------------------------------------------------------------

	#The value for "references_count" is saved
	#"Reference" and "References" two different values
    foundReferencesCount = doiInfo['references-count']
	
	#----------------------------------------------------------------------

	#The value for "score" is saved
    foundScore = doiInfo['score']
	
	#----------------------------------------------------------------------

	#The value for "short_container_title" is saved if not empty
    if not doiInfo['short-container-title'][0]:
        foundShortContainerTitle = "None"
    else:
        foundShortContainerTitle = doiInfo['short-container-title'][0]
		
	#----------------------------------------------------------------------
	
	#The value for "short_title" is saved if not empty
    if not doiInfo['short-title']:
        foundShortTitle = "None"
    else:
        foundShortTitle = doiInfo['short-title']
		
	#----------------------------------------------------------------------

	#The value for "source" is saved if not empty
    foundSource = doiInfo['source']
	
	#----------------------------------------------------------------------

	#The value for "subtitle" is saved if not empty
    if not doiInfo['subtitle']:
        foundSubtitle = "None"
    else:
        foundSubtitle = doiInfo['subtitle']
		
	#----------------------------------------------------------------------

	#The value for "title" is saved if not empty
    if not doiInfo['title'][0]:
        foundTitle = "None"
    else:
        foundTitle = doiInfo['title'][0]
		
	#----------------------------------------------------------------------

	#The value for type" is saved
    foundType = doiInfo['type']
	
	#----------------------------------------------------------------------

	#The value for "svolume" is saved if not empty
    if not doiInfo['volume']:
        foundVolume = ""
    else:
        foundVolume = doiInfo['volume']
		
	#----------------------------------------------------------------------

	#A list of all the value is prepared and returned
    queryValues = (foundDOI, foundURL, foundAlternateID, foundContainerTitle, foundCreatedDatePart, foundCreatedDateTime, 
        foundCreatedDateTimestamp, foundDepositedDatePart, foundDepositedDateTime, foundDepositedTimestamp, foundIndexedDatePart,
        foundIndexedDateTime, foundIndexedTimestamp, foundIsReferencedByCount, foundIssue, foundIssuedDatePart, foundLanguage,
        foundMember, foundOriginalTitle, foundPage, foundPrefix, foundPublishedPrintDatePart, foundPublisher,foundReferenceCount, 
        foundReferencesCount, foundScore, foundShortContainerTitle, foundShortTitle, foundSource, foundSubtitle, foundTitle, foundType, 
        foundVolume, foundfk)

    logging.info("Added DOI: " + foundDOI)  

    return queryValues