
'''
TODO:

    High priority:
    -Create 11 more functions, one for each event type
    -Fill out all 11 functions with the proper values according to json
    -Figure out how to send SQL insert statements using cursor.
        -Write 12 complex insert statements, one for each function - be sure to use INSERT IGNORE to skip duplicates

    Lower priority:
    -Get

'''
import json
import logging
import sys
import os
import cambiaLens
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


try:
    import mysql.connector
except:
    logging.info("Cannot determine how you intend to run the program")

logging.basicConfig(filename='ingest.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  # Set the logging parameters
restorePoint = ""  # Used as last filename we were ingesting

cnx = mysql.connector.connect(
    user='root', password='RiyaFoxMcCloud64', host='127.0.0.1', database='crossRefEventData')
cursor = cnx.cursor()  # Allows us to have multiple seperate working environments through the same connection. Can create individual cursors for each (event) table? redditC = cnx.cursor()?
files = []
dataDirectory = "C:/Users/ujaya_000/Desktop/Senior Project LE/PythonScripts/JSON"


def main():

    global restorePoint
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
                            twitter.twitterIngest(uniqueEvent, cursor)
                        elif (key == "source_id" and value == "cambia-lens"):
                            cambiaLens.cambiaLensIngest(uniqueEvent, cursor)
                        if (key == "source_id" and value == "hypothesis"):
                            hypothesis.hypothesisIngest(uniqueEvent, cursor)
                        if (key == "source_id" and value == "reddit-links"):
                            redditLinks.redditLinksIngest(
                                uniqueEvent, cursor)
                        elif (key == "source_id" and value == "newsfeed"):
                            newsfeed.newsfeedIngest(uniqueEvent, cursor)
                        elif (key == "source_id" and value == "web"):
                            web.webIngest(uniqueEvent, cursor)
                        elif (key == "source_id" and value == "crossref"):
                            crossref.crossrefIngest(uniqueEvent, cursor)
                        elif (key == "source_id" and value == "datacite"):
                            datacite.dataciteIngest(uniqueEvent, cursor)
                        elif (key == "source_id" and value == "wordpressdotcom"):
                            wordPress.wordPressIngest(uniqueEvent, cursor)
                        elif (key == "source_id" and value == "stackexchange"):
                            stackExchange.stackExchangeIngest(
                                uniqueEvent, cursor)
                    except:
                        logging.info("Failed Ingest. Failed on file" + i)
                        cnx.close()
                        sys.exit()


cnx.close()  # Close the database, we're done

# cnx.commit() Must be used to commit the data after using insert, delete or update statements

# cursor.close() Will have to close each individual cursor if we decide to use multiple cursors

# cnx.close()


if __name__ == '__main__':
    main()
