import flask

def landingPageStats(mysql):
    #global mysql
    cursor = mysql.connection.cursor()

    totalSumQuery=" SELECT( (SELECT COUNT(objectID) FROM crossrefeventdatamain.cambiaevent)+ (SELECT COUNT(objectID) FROM crossrefeventdatamain.crossrefevent) + (SELECT COUNT(objectID) FROM crossrefeventdatamain.dataciteevent) + (SELECT COUNT(objectID) FROM crossrefeventdatamain.hypothesisevent) + (SELECT COUNT(objectID) FROM crossrefeventdatamain.newsfeedevent) +(SELECT COUNT(objectID) FROM crossrefeventdatamain.redditevent) + (SELECT COUNT(objectID) FROM crossrefeventdatamain.redditlinksevent) +(SELECT COUNT(objectID) FROM crossrefeventdatamain.stackexchangeevent) + (SELECT COUNT(objectID) FROM crossrefeventdatamain.twitterevent) +(SELECT COUNT(objectID) FROM crossrefeventdatamain.webevent) + (SELECT COUNT(objectID) FROM crossrefeventdatamain.wikipediaevent) + (SELECT COUNT(objectID) FROM crossrefeventdatamain.wordpressevent) +(SELECT COUNT(objectID) FROM crossrefeventdatamain.f1000event))AS sumCount;"

    cursor.execute(totalSumQuery)
    mysql.connection.commit()
    totalSum = cursor.fetchone()

    print(totalSum)

    cursor.close()
    return (totalSum['sumCount'])



