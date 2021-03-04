#import flask
import flask

#define function to retrieve the total number of journals in the database 
def landingPageJournals(mysql):
    #global mysql
    cursor = mysql.connection.cursor()

    #string to query the database to sum up all journals from _main_ table
    totalSumQuery="SELECT (SELECT COUNT( DISTINCT container_title) FROM doidata._main_ ) AS sumCountJournal"

    #execute string's query using cursor 
    cursor.execute(totalSumQuery)

    #commit
    mysql.connection.commit()
    
    #fetch result
    totalSumJournals = cursor.fetchone()

    #close cursor
    cursor.close()
    
    #return result fetched from dictionary
    return (totalSumJournals['sumCountJournal'])

