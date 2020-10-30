import cambiaLens
import wordPress
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
import json
import logging
import sys
import os
logging.basicConfig(filename='./ingest.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  # Set the logging parameters
try:
    import mysql.connector
except:
    logging.info("Cannot determine how you intend to run the program")

# Change these to suit your system
mysql_username = "root"
mysql_password = ""

connection = mysql.connector.connect(user=str(mysql_username), password=str(
    mysql_password), host='127.0.0.1', database='crossrefeventdata')

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
            if (key == "source_id" and value == "twitter"):
                twitter.twitterIngest(
                    eventDict, cursor, connection)
                break
            elif (key == "source_id" and value == "cambia-lens"):
                cambiaLens.cambiaLensIngest(
                    eventDict, cursor, connection)
                break
            elif (key == "source_id" and value == "hypothesis"):
                hypothesis.hypothesisIngest(
                    eventDict, cursor, connection)
                break
            elif (key == "source_id" and value == "reddit-links"):
                redditLinks.redditLinksIngest(
                    eventDict, cursor, connection)
                break
            elif (key == "source_id" and value == "newsfeed"):
                newsfeed.newsfeedIngest(
                    eventDict, cursor, connection)
                break
            elif (key == "source_id" and value == "web"):
                web.webIngest(eventDict, cursor, connection)
                break
            elif (key == "source_id" and value == "crossref"):
                crossref.crossrefIngest(
                    eventDict, cursor, connection)
                break
            elif (key == "source_id" and value == "datacite"):
                datacite.dataciteIngest(
                    eventDict, cursor, connection)
                break
            elif (key == "source_id" and value == "wikipedia"):
                wikipedia.wikipediaIngest(
                    eventDict, cursor, connection)
                break
            elif (key == "source_id" and value == "wordpressdotcom"):
                wordPress.wordPressIngest(
                    eventDict, cursor, connection)
                break
            elif (key == "source_id" and value == "stackexchange"):
                stackExchange.stackExchangeIngest(
                    eventDict, cursor, connection)
                break
            elif (key == "source_id" and value == "reddit"):
                reddit.redditIngest(
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
