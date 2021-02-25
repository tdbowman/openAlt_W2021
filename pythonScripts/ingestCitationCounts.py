# author: Rihat Rahman
# Lines: 1 - 34
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