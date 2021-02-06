import cambiaLens
import wordpress
import wikipedia
import web
import twitter
import stackExchange
import redditLinks
import reddit
import newsfeed
import hypothesis
import datacite
import crossref
import f1000
import json
import logging
import sys
import os
import time

logging.basicConfig(filename='./ingest.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  # Set the logging parameters
try:
    import mysql.connector
except:
    logging.info("Cannot determine how you intend to run the program")

# Change these to suit your system
print("MySQL Credentials")
mysql_username = input("Username: ")
mysql_password = input("Password: ")


def main():

    connection = mysql.connector.connect(user=str(mysql_username), password=str(
        mysql_password), host='127.0.0.1', database='crossrefeventdatamain')

    # Returns dictionary values instead of tuples
    cursor = connection.cursor(dictionary=True)

    # Query that grabs ID of the last row(highest ID) of the database
    SQLMaxFindAI = "Select MAX(id) as id FROM paperbuzzeventdata.event_data_json;"
    cursor.execute(SQLMaxFindAI)
    maxAIResults = cursor.fetchone()
    maxAI = maxAIResults["id"]
    AI = 1

    # Loop through the whole paperbuzz database
    while(AI < maxAI):
        query = "select json from paperbuzzeventdata.event_data_json where id = " + \
            str(AI) + ";"
        cursor.execute(query)
        # Grabs the json column and puts it into a dictionary
        eventRow = cursor.fetchone()

        # Stores the "json" key within eventBytes
        # eventBytes turns into a byte class
        eventBytes = eventRow.get("json")

        # Converts eventBytes into a dictionary
        eventDict = json.loads(eventBytes.decode('utf-8'))

        # Go through keys and values of dictionary, searching for source_id and the value based on which online platform the event comes from
        for key, value in eventDict.items():
            try:
                # Speeds up the process of searching for the source_id.
                if(key != "source_id"):
                    pass
                else:
                    if (key == "source_id" and value == "cambia-lens"):
                        print('CambiaLens')
                        cambiaLens.cambiaLensIngest(
                            eventDict, cursor, connection)
                        break
                    elif (key == "source_id" and value == "crossref"):
                        print('Crossref')
                        crossref.crossrefIngest(
                            eventDict, cursor, connection)
                        break
                    elif (key == "source_id" and value == "datacite"):
                        print('Datacite')
                        datacite.dataciteIngest(
                            eventDict, cursor, connection)
                        break
                    elif (key == "source_id" and value == "f1000"):
                        print('F1000')
                        f1000.F1000Ingest(
                            eventDict, cursor, connection)
                        break
                    elif (key == "source_id" and value == "hypothesis"):
                        print('Hypothesis')
                        hypothesis.hypothesisIngest(
                            eventDict, cursor, connection)
                        break
                    elif (key == "source_id" and value == "newsfeed"):
                        print('Newsfeed')
                        newsfeed.newsfeedIngest(
                            eventDict, cursor, connection)
                        break
                    elif (key == "source_id" and value == "reddit"):
                        print('Reddit')
                        reddit.redditIngest(
                            eventDict, cursor, connection)
                        break
                    elif (key == "source_id" and value == "reddit-links"):
                        print('RedditLinks')
                        redditLinks.redditLinksIngest(
                            eventDict, cursor, connection)
                        break
                    elif (key == "source_id" and value == "stackexchange"):
                        print('Stackexchange')
                        stackExchange.stackExchangeIngest(
                            eventDict, cursor, connection)
                        break
                    elif (key == "source_id" and value == "twitter"):
                        print('Twitter')
                        twitter.twitterIngest(
                            eventDict, cursor, connection)
                        break
                    elif (key == "source_id" and value == "web"):
                        print('Web')
                        web.webIngest(eventDict, cursor, connection)
                        break
                    elif (key == "source_id" and value == "wikipedia"):
                        print('Wikipedia')
                        wikipedia.wikipediaIngest(
                            eventDict, cursor, connection)
                        break
                    elif (key == "source_id" and value == "wordpressdotcom"):
                        print('Wordpress')
                        wordpress.wordpressIngest(
                            eventDict, cursor, connection)
                        break
            except Exception as e:
                logging.info("Failed Ingest. Failed on file")
                logging.info("The error was " + str(e))
                cursor.close()
                connection.close()
                sys.exit()
        # print(type(eventDict))
        AI += 1
    cursor.close()
    connection.close()
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    start_time = time.time()
    main()
