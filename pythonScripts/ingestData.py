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

try:
    import mysql.connector
except:
    logging.info("Cannot determine how you intend to run the program")

logging.basicConfig(filename='ingest.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S') # Set the logging parameters
restorePoint = "" # Used as last filename we were ingesting

cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='crossRefEventData')
cursor = cnx.cursor()
files = []
dataDirectory = "C:/Users/mitch/Desktop/JSON"

def main():
    
    global restorePoint
    #dataDirectory = "/home/fg7626/crossrefDataDumps"
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
        restorePoint = i # This is the filename we should start at when rerunning it
        with open(i) as json_file:
            data = json.load(json_file) # Dict
            events = data.get("message").get("events") # LIST of dicts
            for uniqueEvent in events: # each uniqueEvent is a dict
                for key, value in uniqueEvent.items():
                    if (key == "source_id" and value == "twitter"):
                        twitterIngest(uniqueEvent)
                    elif (key == "source_id" and value == ""):
                        twitterIngest(uniqueEvent)
                    elif (key == "source_id" and value == ""):
                        twitterIngest(uniqueEvent)
                    elif (key == "source_id" and value == ""):
                        twitterIngest(uniqueEvent)
                    elif (key == "source_id" and value == ""):
                        twitterIngest(uniqueEvent)
                    elif (key == "source_id" and value == ""):
                        twitterIngest(uniqueEvent)
                    elif (key == "source_id" and value == ""):
                        twitterIngest(uniqueEvent)
                    elif (key == "source_id" and value == ""):
                        twitterIngest(uniqueEvent)
                    elif (key == "source_id" and value == ""):
                        twitterIngest(uniqueEvent)
    cnx.close() # Close the database, we're done

def twitterIngest(uniqueEvent):
    for key, value in uniqueEvent.items():
    #for key in uniqueEvent.keys():
        if key == "license":
            t_license = value
            print(t_license)
        elif key == "terms":
            t_terms = value
            print(t_terms)
        elif (key == "updated_reason"):
            pass
        elif (key == "updated"):
            pass
        elif (key == "obj_id"):
            pass
        elif (key == "source_token"):
            pass
        elif (key == "occurred_at"):
            pass
        elif (key == "subj_id"):
            pass
        elif (key == "id"):
            pass
        elif (key == "evidence_record"):
            pass
        elif (key == "action"):
            pass
        elif (key == "subj"):
            # value of subj is a dict: 
            #   pid 
            #   title
            #   issued
            #   value of author is a dict, has url
            #   original-tweet-url
            #   original-tweet-author
            #   alternative-id
            pass
        elif (key == "source_id"):
            pass
        elif (key == "obj"):
            # Value of obj is a dict:
            #   pid
            #   url
            pass
        elif (key == "timestamp"):
            pass
        elif (key == "updated_date"):
            pass
        elif (key == "relation_type_id"):
            pass
    # Execute some complex SQL statement here
    # INSERT INTO IN

if __name__ == '__main__':
    main()