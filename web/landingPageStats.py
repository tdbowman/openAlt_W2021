#import flask
import flask

#define function to retrieve the total number of events in the database
def landingPageStats(mysql):
    #global mysql
    cursor = mysql.connection.cursor()
    
    #string to query the database to sum up all events from all 13 sources listed below
    totalSumQuery= 'SELECT SUM(totalEvents) FROM crossrefeventdatamain.main;'

    #execute string's query using cursor
    cursor.execute(totalSumQuery)
    
    #commit
    mysql.connection.commit()

    #fetch result 
    totalSum = cursor.fetchone()

    #close cursor
    cursor.close()

    #return result fetched from the dictionary
    return (totalSum['sumCount'])



