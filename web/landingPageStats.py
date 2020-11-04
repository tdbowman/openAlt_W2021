import flask

def landingPageStats(mysql):
    #global mysql
    cursor = mysql.connection.cursor()

    totalSumQuery=" SELECT( (SELECT COUNT( DISTINCT objectID) FROM crossrefeventdatamain.cambiaevent)+ (SELECT COUNT( DISTINCT objectID) FROM crossrefeventdatamain.crossrefevent) + (SELECT COUNT( DISTINCT objectID) FROM crossrefeventdatamain.dataciteevent) + (SELECT COUNT( DISTINCT objectID) FROM crossrefeventdatamain.hypothesisevent) + (SELECT COUNT( DISTINCT objectID) FROM crossrefeventdatamain.newsfeedevent) +(SELECT COUNT( DISTINCT objectID) FROM crossrefeventdatamain.redditevent) + (SELECT COUNT( DISTINCT objectID) FROM crossrefeventdatamain.redditlinksevent) +(SELECT COUNT( DISTINCT objectID) FROM crossrefeventdatamain.stackexchangeevent) + (SELECT COUNT( DISTINCT objectID) FROM crossrefeventdatamain.twitterevent) +(SELECT COUNT( DISTINCT objectID) FROM crossrefeventdatamain.webevent) + (SELECT COUNT( DISTINCT objectID) FROM crossrefeventdatamain.wikipediaevent) + (SELECT COUNT( DISTINCT objectID) FROM crossrefeventdatamain.wordpressevent) +(SELECT COUNT( DISTINCT objectID) FROM crossrefeventdatamain.f1000event))AS sumCount;"

    cursor.execute(totalSumQuery)
    mysql.connection.commit()
    totalSum = cursor.fetchone()

    print(totalSum)

    cursor.close()
    return (totalSum['sumCount'])



