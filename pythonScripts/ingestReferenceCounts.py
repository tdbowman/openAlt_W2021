# author: Rihat Rahman
# Lines: 1 - 33
# scipt to insert reference counts and check if references need to be updated
#-------------------------------------------------------------

def ingestReferenceCounts (doi, openCitationsCursor, referenceCountsJson, openCitationsDatabase):

    count = referenceCountsJson[0]['count']

    if count == 0:
        return False

    query = ("SELECT count FROM reference_count WHERE doi = '" + doi + "'")

    openCitationsCursor.execute(query)

    previous_count = openCitationsCursor.fetchall()

    if previous_count == []:

        query = ("Insert IGNORE INTO reference_count " " (doi, count) " " VALUES (%s,%s)")
        data = (doi, count)

        openCitationsCursor.execute(query, data)

    else:
        if int(previous_count[0][0]) >= int(count):
            return False
        query = ("UPDATE reference_count SET count = '" + str(count) + "' WHERE doi = '" + doi + "'")
        openCitationsCursor.execute(query)
    
    openCitationsDatabase.commit()
#-------------------------------------------------------------