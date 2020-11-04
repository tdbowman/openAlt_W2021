import flask

def landingPageStats(mysql):
    #global mysql
    cursor = mysql.connection.cursor()

    totalSumQuery=" SELECT( (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.cambiaevent)+ (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.crossrefevent) + (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.dataciteevent) + (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.hypothesisevent) + (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.newsfeedevent) +(SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.redditevent) + (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.redditlinksevent) +(SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.stackexchangeevent) + (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.twitterevent) +(SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.webevent) + (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.wikipediaevent) + (SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.wordpressevent) +(SELECT COUNT( DISTINCT eventID) FROM crossrefeventdatamain.f1000event))AS sumCount;"

    cursor.execute(totalSumQuery)
    mysql.connection.commit()
    totalSum = cursor.fetchone()

    print(totalSum)

    cursor.close()
    return (totalSum['sumCount'])



