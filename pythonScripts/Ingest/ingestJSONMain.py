import cambiaLens
import wordpress
import wikipedia
import web
import f1000
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
import time

logging.basicConfig(filename='./ingest.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  # Set the logging parameters
try:
    import mysql.connector
except:
    logging.info("Cannot determine how you intend to run the program")

# Change these to suit your system

dataDirectory = "./JSON"

# dataDirectory = "C:\\Users\\tasha\\Documents\\GitHub\\openAlt_W2021\\eventData"

print("MySQL Credentials")
mysql_username = input("Username: ")
mysql_password = input("Password: ")


def main():

    restorePoint = ""  # Used as last filename we were ingesting
    files = []
    global dataDirectory
    connection = mysql.connector.connect(user=str(mysql_username), password=str(
        mysql_password), host='127.0.0.1', database='crossrefeventdatamain')
    cursor = connection.cursor()  # Allows us to have multiple seperate working environments through the same connection. Can create individual cursors for each (event) table? redditC = cnx.cursor()?

    for (path, dirnames, filenames) in os.walk(dataDirectory):
        files.extend(os.path.join(path, name) for name in sorted(filenames))

    # For each file in the directory, open the file.
    #   For each opened file, load the contents into memory and extract the events LIST
    #       For i in events, pull out key/value pairs and "INSERT IGNORE INTO crossRefEventData"
    for i in files:
        restorePoint = i  # This is the filename we should start at when rerunning it
        with open(i) as json_file:
            data = json.load(json_file)  # Dict
            events = data.get("message").get("events")  # LIST of dicts
            for uniqueEvent in events:  # each uniqueEvent is a dict
                # Go through each event's key and value pairs
                for key, value in uniqueEvent.items():
                    # Try except incase something goes wrong for if elif statements
                    # The source_id is a distinct field that represents each online platform
                    # If the source_id is *insert online platform here*, then insert the values for each field of the event.
                    # Break statements are used to stop the loop from going through the rest of the event, all we needed was to find source_id. This helps speeds up the process.
                    try:
                        # Speeds up the process of searching for the source_id.
                        if(key != "source_id"):
                            pass
                        else:
                            if (key == "source_id" and value == "cambia-lens"):
                                print('cambia')
                                cambiaLens.cambiaLensIngest(
                                    uniqueEvent, cursor, connection)
                                break
                            elif (key == "source_id" and value == "crossref"):
                                print('crossref')
                                crossref.crossrefIngest(
                                    uniqueEvent, cursor, connection)
                                break
                            elif (key == "source_id" and value == "datacite"):
                                print('datacite')
                                datacite.dataciteIngest(
                                    uniqueEvent, cursor, connection)
                                break
                            elif (key == "source_id" and value == "f1000"):
                                print('F1000')
                                f1000.F1000Ingest(
                                    uniqueEvent, cursor, connection)
                                break
                            elif (key == "source_id" and value == "hypothesis"):
                                print('hypothesis')
                                hypothesis.hypothesisIngest(
                                    uniqueEvent, cursor, connection)
                                break
                            elif (key == "source_id" and value == "newsfeed"):
                                print('newsfeed')
                                newsfeed.newsfeedIngest(
                                    uniqueEvent, cursor, connection)
                                break
                            elif (key == "source_id" and value == "reddit"):
                                print('reddit')
                                reddit.redditIngest(
                                    uniqueEvent, cursor, connection)
                                break
                            elif (key == "source_id" and value == "reddit-links"):
                                print('redditlinks')
                                redditLinks.redditLinksIngest(
                                    uniqueEvent, cursor, connection)
                                break
                            elif (key == "source_id" and value == "stackexchange"):
                                print('stackexchange')
                                stackExchange.stackExchangeIngest(
                                    uniqueEvent, cursor, connection)
                                break
                            elif (key == "source_id" and value == "twitter"):
                                print('twitter')
                                twitter.twitterIngest(
                                    uniqueEvent, cursor, connection)
                                break
                            elif (key == "source_id" and value == "web"):
                                print('web')
                                web.webIngest(uniqueEvent, cursor, connection)
                                break
                            elif (key == "source_id" and value == "wikipedia"):
                                print('wikipedia')
                                wikipedia.wikipediaIngest(
                                    uniqueEvent, cursor, connection)
                                break
                            elif (key == "source_id" and value == "wordpressdotcom"):
                                print('wordpress.com')
                                wordpress.wordpressIngest(
                                    uniqueEvent, cursor, connection)
                                break
                    except Exception as e:
                        logging.info("Failed Ingest. Failed on file" + i)
                        logging.info("The error was " + str(e))
                        cursor.close()
                        connection.close()
                        sys.exit()
    cursor.close()
    connection.close()
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    start_time = time.time()
    main()
