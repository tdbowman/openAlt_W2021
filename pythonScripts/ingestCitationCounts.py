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
# Lines: 1 - 58
# scipt to insert citation counts and check if citations need to be updated
#-------------------------------------------------------------
def ingestCitationCounts(doi, openCitationsCursor, citationCountsJSON, openCitationsDatabase):


    count = citationCountsJSON[0]['count']

    if count == 0:
        return False

    query = ("SELECT count FROM citation_count WHERE doi = '" + doi + "'")

    openCitationsCursor.execute(query)

    previous_count = openCitationsCursor.fetchall()


    if previous_count == []:

        query = ("Insert IGNORE INTO citation_count " " (doi, count) " " VALUES (%s,%s)")
        data = (doi, count)

        openCitationsCursor.execute(query, data)

    else:
        if int(previous_count[0][0]) >= int(count):
            return False
        query = ("UPDATE citation_count SET count = '" + str(count) + "' WHERE doi = '" + doi + "'")
        openCitationsCursor.execute(query)

    openCitationsDatabase.commit()
#-------------------------------------------------------------