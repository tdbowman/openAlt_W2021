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

# author: Rihat Rahman
# Lines: 1-78
# script to ingest citations from MongoDB to MySQL
#-------------------------------------------------------------
import pymongo
import mysql.connector

def ingestCitations(doi, openCitationsCursor, citationCollections, openCitationsDatabase):


    # retrieve list of citations from MongoDB buffer database
    listOfCitations = citationCollections.find()

    for citation in listOfCitations:

        creation = None
        oci = None
        author_sc = None
        citing = None
        timespan = None
        cited = None
        journal_sc = None

        for key, value in citation.items():

            if key == 'creation':
                creation = value

            elif key == 'oci':
                oci = value

            elif key == 'author_sc':
                author_sc = value

            elif key == 'citing':
                citing = value

            # TODO: change time format
            elif timespan == 'timespan':
                timespan = value

            elif key == 'cited':
                cited = value

            elif journal_sc == 'journal_sc':
                journal_sc = value

        # query to insert citation data into MySQL
        query = ("Insert IGNORE INTO opencitations.citations " " (oci, citing, cited, creation, timespan, journal_sc, author_sc) " " VALUES (%s,%s,%s,%s,%s,%s,%s)")
        data = (oci, citing, cited, creation, timespan, journal_sc, author_sc)

        openCitationsCursor.execute(query, data)
        openCitationsDatabase.commit()
#-------------------------------------------------------------