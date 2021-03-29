# author: Rihat Rahman
# Lines: 1-54
# script to ingest references from MongoDB to MySQL
#-------------------------------------------------------------

def ingestReferences (doi, openCitationsCursor, referenceCollections, openCitationsDatabase):
    
    listOfReferences = referenceCollections.find()

    for citation in listOfReferences:

        creation = None
        oci = None
        author_sc = None
        citing = None
        timespan = None
        cited = None
        journal_sc = None

        for key, value in citation.items():

            if key == 'oci':
                oci = value[8:]

            elif key == 'citing':
                citing = value[8:]

            elif key == 'cited':
                cited = value[8:]

            elif key == 'creation':
                creation = value [8:]

            # TODO: change time format
            elif timespan == 'timespan':
                timespan = value[8:]

            elif journal_sc == 'journal_sc':
                journal_sc = value[8:]

            elif key == 'author_sc':
                author_sc = value[8:]


        query = ("Insert IGNORE INTO opencitations.ref " " (oci, citing, cited, creation, timespan, journal_sc, author_sc) " " VALUES (%s,%s,%s,%s,%s,%s,%s)")
        data = (oci, citing, cited, creation, timespan, journal_sc, author_sc)

        openCitationsCursor.execute(query, data)
        openCitationsDatabase.commit()
#-------------------------------------------------------------
