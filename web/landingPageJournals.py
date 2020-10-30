import flask

def landingPageJournals(mysql):
    #global mysql
    cursor = mysql.connection.cursor()

    totalSumQuery="SELECT (SELECT COUNT( DISTINCT container_title) FROM dr_bowman_doi_data_tables._main_ ) AS sumCountJournal"

    cursor.execute(totalSumQuery)
    mysql.connection.commit()
    totalSumJournals = cursor.fetchone()

    print(totalSumJournals)

    cursor.close()
    return (totalSumJournals['sumCountJournal'])

