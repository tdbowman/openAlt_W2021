import flask

def landingPageStats(mysql):
    #global mysql
    cursor = mysql.connection.cursor()

    totalSumQuery=" SELECT (SELECT COUNT(objectID) FROM crossrefeventdata.cambiaevent) + (SELECT COUNT(objectID) FROM crossrefeventdata.crossrefevent) + (SELECT COUNT(objectID) FROM crossrefeventdata.dataciteevent) + (SELECT COUNT(objectID) FROM crossrefeventdata.hypothesisevent) + (SELECT COUNT(objectID) FROM crossrefeventdata.newsfeedevent) + (SELECT COUNT(objectID) FROM crossrefeventdata.redditevent) + (SELECT COUNT(objectID) FROM crossrefeventdata.redditlinksevent) + (SELECT COUNT(objectID) FROM crossrefeventdata.stackexchangeevent) + (SELECT COUNT(objectID) FROM crossrefeventdata.twitterevent) + (SELECT COUNT(objectID) FROM crossrefeventdata.webevent) + (SELECT COUNT(objectID) FROM crossrefeventdata.wikipediaevent) + (SELECT COUNT(objectID) FROM crossrefeventdata.wordpressevent) AS sumCount"

    cursor.execute(totalSumQuery)
    mysql.connection.commit()
    totalSum = cursor.fetchone()

    print(totalSum)

    cursor.close()
    return (totalSum['sumCount'])



