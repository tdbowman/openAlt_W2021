
'''
TODO:

    Write move statement at the bottom of this file
    Testing testing testing.
    More Try Except?

'''
import json
import logging
import sys
import os
logging.basicConfig(filename='./ingest.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  # Set the logging parameters
try:
    import mysql.connector
except:
    logging.info("Cannot determine how you intend to run the program")
import crossref
import datacite
import hypothesis
import newsfeed
import reddit
import redditLinks
import stackExchange
import twitter
import web
import wikipedia
import wordPress
import cambiaLens

# Change these to suit your system
dataDirectory = "C:/Users/mitch/Desktop/JSON"
mysql_username = "root"
mysql_password = ""

def main():

    restorePoint = ""  # Used as last filename we were ingesting
    files = []
    global dataDirectory
    connection = mysql.connector.connect(user=str(mysql_username), password=str(mysql_password), host='127.0.0.1', database='crossrefeventdata')
    cursor = connection.cursor()  # Allows us to have multiple seperate working environments through the same connection. Can create individual cursors for each (event) table? redditC = cnx.cursor()?

    # dataDirectory = "/home/fg7626/crossrefDataDumps"
    for (path, dirnames, filenames) in os.walk(dataDirectory):
        files.extend(os.path.join(path, name) for name in sorted(filenames))

    '''
    # Can possibly use some variant of this to pop off any files which are not json
    # But there should not be anything but .json in the folder so low priority
    i = 0
    while (i < len(files)-1):
        if not files[i].endswith('.json'):
            files.pop(i)
        i += 1
    print(files)
    '''

    '''
    # We can run a second copy of this to pop all files which after the restore point
    i = 0
    while (i < len(files)-1):
        if not files[i].endswith('.json'):
            files.pop(i)
        i += 1
    print(files)
    '''

    # For each file in the directory, open the file.
    #   For each open file, load the contents into memory and extract the events LIST
    #       For i in events, pull out key/value pairs and "INSERT IGNORE INTO crossRefEventData"
    for i in files:
        restorePoint = i  # This is the filename we should start at when rerunning it
        with open(i) as json_file:
            data = json.load(json_file)  # Dict
            events = data.get("message").get("events")  # LIST of dicts
            for uniqueEvent in events:  # each uniqueEvent is a dict
                for key, value in uniqueEvent.items():
                    # Try except incase something goes wrong for if elif statements
                    try:
                        if (key == "source_id" and value == "twitter"):
                            twitter.twitterIngest(uniqueEvent, cursor, connection)
                        elif (key == "source_id" and value == "cambia-lens"):
                            cambiaLens.cambiaLensIngest(uniqueEvent, cursor, connection)
                        elif (key == "source_id" and value == "hypothesis"):
                            hypothesis.hypothesisIngest(uniqueEvent, cursor, connection)
                        elif (key == "source_id" and value == "reddit-links"):
                            redditLinks.redditLinksIngest(uniqueEvent, cursor, connection)
                        elif (key == "source_id" and value == "newsfeed"):
                            newsfeed.newsfeedIngest(uniqueEvent, cursor, connection)
                        elif (key == "source_id" and value == "web"):
                            web.webIngest(uniqueEvent, cursor, connection)
                        elif (key == "source_id" and value == "crossref"):
                            crossref.crossrefIngest(uniqueEvent, cursor, connection)
                        elif (key == "source_id" and value == "datacite"):
                            datacite.dataciteIngest(uniqueEvent, cursor, connection)
                        elif (key == "source_id" and value == "wikipedia"):
                            wikipedia.wikipediaIngest(uniqueEvent, cursor, connection)
                        elif (key == "source_id" and value == "wordpressdotcom"):
                            wordPress.wordPressIngest(uniqueEvent, cursor, connection)
                        elif (key == "source_id" and value == "stackexchange"):
                            stackExchange.stackExchangeIngest(uniqueEvent, cursor, connection)
                        elif (key == "source_id" and value == "reddit"):
                            stackExchange.stackExchangeIngest(uniqueEvent, cursor, connection)
                    except Exception as e:
                        logging.info("Failed Ingest. Failed on file" + i)
                        logging.info("The error was " + str(e))
                        cursor.close()
                        connection.close()
                        sys.exit()
    '''
    TODO: 
    add line to move (mv) file out of the dumps directory
    Requires a folder structure like

        home 
        /   \  
    dumps   ingest

    Because the ../ingest/ tells it to move from dumps, up one director, then down into ingest
    The mv command works fine on windows, so we should be able to debug it before uploading to the server

    os.sys("mv " + files[i] + "../ingest/" + files[i])
    
    '''
    cursor.close()
    connection.close()

if __name__ == '__main__':
    main()