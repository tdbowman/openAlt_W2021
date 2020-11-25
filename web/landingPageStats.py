#import flask
import flask

#define function to retrieve the total number of events in the database
def landingPageStats(mysql):
    #global mysql
    cursor = mysql.connection.cursor()
    
    #string to query the database to sum up all events from all 13 sources listed below
    totalSumQuery=" SELECT( (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.cambiaevent)+ (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.crossrefevent) + (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.dataciteevent) + (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.hypothesisevent) + (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.newsfeedevent) +(SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.redditevent) + (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.redditlinksevent) +(SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.stackexchangeevent) + (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.twitterevent) +(SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.webevent) + (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.wikipediaevent) + (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.wordpressevent) +(SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.f1000event))AS sumCount;"

    #execute string's query using cursor
    cursor.execute(totalSumQuery)
    
    #commit
    mysql.connection.commit()

    #fetch result 
    totalSum = cursor.fetchone()

    #print in terminal for testing purposes
    print(totalSum)

    #close cursor
    cursor.close()

    #return result fetched from the dictionary
    return (totalSum['sumCount'])



