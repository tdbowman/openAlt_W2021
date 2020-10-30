import dateutil.parser


def wikipediaIngest(uniqueEvent, cursor, connection):

    # These are all temporary objects used to store the values of the fields in the JSON files.
    # Some fields may not always exist. We were getting errors when we didn't have some fields initialized so we decided to initialize all the fields.
    # The layout here is based upon the JSON file layout and is different from the crossrefeventdatamain database's table layout.

    t_license = None
    t_terms = None
    t_updated_reason = None
    t_obj_id = None
    t_source_token = None
    t_occurred_at = None
    t_subj_id = None
    t_id = None
    t_evidence_record = None
    t_action = None
    t_subj_pid = None
    t_subj_url = None
    t_subj_title = None
    t_api_url = None
    t_source_id = None
    t_obj_pid = None
    t_obj_url = None
    t_timestamp = None
    t_updated_date = None
    t_relation_type_id = None

    for key, value in uniqueEvent.items():
        if key == "license":
            t_license = value
        elif (key == "terms"):
            t_terms = value
        elif (key == "updated_reason"):
            t_updated_reason = value
        elif (key == "obj_id"):
            t_obj_id = value
        elif (key == "source_token"):
            t_source_token = value
        elif (key == "occurred_at"):
            t_occurred_at = value
        elif (key == "subj_id"):
            t_subj_id = value
        elif (key == "id"):
            t_id = value
        elif (key == "evidence_record"):
            t_evidence_record = value
        elif (key == "action"):
            t_action = value
        elif (key == 'subj'):
            subj_fields = uniqueEvent.get("subj")
            for key, value in subj_fields.items():
                if(key == 'pid'):
                    t_subj_pid = value
                elif(key == 'url'):
                    t_subj_url = value
                elif(key == 'title'):
                    t_subj_title = value
                elif(key == 'api-url'):
                    t_api_url = value
        elif (key == 'source_id'):
            t_source_id = value
        elif (key == 'obj'):
            obj_fields = uniqueEvent.get('obj')
            for key, value in obj_fields.items():
                if(key == 'pid'):
                    t_obj_pid = value
                elif(key == 'url'):
                    t_obj_url = value
        elif (key == 'timestamp'):
            t_timestamp = value
        elif (key == "updated_date"):
            t_updated_date = value
        elif (key == 'relation_type_id'):
            t_relation_type_id = value

    try:
        # Insert t_obj_id from the event of the JSON file into the main table
        objectIDInsertionQuery = "INSERT IGNORE INTO main (objectID) VALUES(\'" + \
            t_obj_id + "\');"
        cursor.execute(objectIDInsertionQuery)
        connection.commit()

        # Fetch all records from the 4 columns in the main table from t_obj_id and is placed into a list of tuples.
        # (firstWikipediaEvent, lastWikipediaevent, totalEvents, totalWikipediaEvents)
        listOfDictQuery = "SELECT firstWikipediaEvent, lastWikipediaEvent, totalEvents, totalWikipediaEvents FROM Main WHERE objectID = \'" + t_obj_id + "\';"
        cursor.execute(listOfDictQuery)
        row = cursor.fetchone()

        if (type(row) == dict):
            # Initialize objects to dictionary key values
            firstEvent = row['firstWikipediaEvent']
            lastEvent = row['lastWikipediaEvent']
            totalEvents = row['totalEvents']
            totalWikipediaEvents = row['totalWikipediaEvents']
        elif (type(row) == tuple):
            # Initialize objects to tuple values
            firstEvent = row[0]
            lastEvent = row[1]
            totalEvents = row[2]
            totalWikipediaEvents = row[3]

    # If we enter this except block, most likely the DOI was long gibberish and was unable to be entered into the main table which is VARCHAR(100)
    except:
        return  # just return to main.py, this event will not be ingested

    # If empty, intialize to 0
    if not totalEvents:
        totalEvents = 0
    if not totalWikipediaEvents:
        totalWikipediaEvents = 0

    # Convert t_timestamp(timestamp) into t_dateTime(datetime)
    t_dateTime = dateutil.parser.isoparse(t_timestamp)
    t_dateTime = str(t_dateTime)

    # If t_timestamp is less than firstEvent or if firstEvent is NULL, update firstWikipediaEvent with t_dateTime in the same row in the main table.
    if ((t_timestamp < str(firstEvent)) or (firstEvent == None)):
        updateFirstEventQuery = "UPDATE main SET firstWikipediaEvent = \'" + \
            t_dateTime + "\' WHERE objectID = \'" + t_obj_id + "\';"
        cursor.execute(updateFirstEventQuery)
        connection.commit()

    # If t_timestamp is greater than lastEvent or if lastEvent is NULL, update lastWikipediaEvent with t_dateTime in the same row in the main table.
    if ((t_timestamp > str(lastEvent)) or (lastEvent == None)):
        updateLastEventQuery = "UPDATE main SET lastWikipediaEvent = \'" + \
            t_dateTime + "\' WHERE objectID = \'" + t_obj_id + "\';"
        cursor.execute(updateLastEventQuery)
        connection.commit()

    # Increment event count
    totalEvents += 1
    totalWikipediaEvents += 1

    # Update totalEvents and totalWikipediaEvents in the main table
    updateTotalEventsQuery = "UPDATE main SET totalEvents = " + str(totalEvents) + \
        ", totalWikipediaEvents = " + str(totalWikipediaEvents) + \
        " WHERE objectID = \'" + t_obj_id + "\';"

    cursor.execute(updateTotalEventsQuery)
    connection.commit()

    # SQL which inserts into event table
    add_event = (
        "INSERT IGNORE INTO WikipediaEvent " "(license, termsOfUse, updatedDate, updatedReason, objectID, sourceToken, occurredAt, subjectID, eventID, evidenceRecord, eventAction, subjectPID, subjectTitle, subjectURL, subjectAPIURL, sourceID, objectPID, objectURL, timeObserved, relationType) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    # Values to insert into wikipediaevent table  - LEAVE OUT THE OBJECT ID
    data_event = (t_license, t_terms, t_updated_date, t_updated_reason, t_obj_id, t_source_token, t_occurred_at, t_subj_id, t_id, t_evidence_record,
                  t_action, t_subj_pid, t_subj_title, t_subj_url, t_api_url, t_source_id, t_obj_pid, t_obj_url, t_timestamp, t_relation_type_id)

    # add information to wikipediaevent table
    cursor.execute(add_event, data_event)
    connection.commit()
