import dateutil.parser


def wordpressIngest(uniqueEvent, cursor, connection):

    # These are all temporary objects used to store the values of the fields in the JSON files.
    # Some fields may not always exist. We were getting errors when we didn't have some fields initialized so we decided to initialize all the fields.
    # The layout here is based upon the JSON file layout and is different from the crossrefeventdatamain database's table layout.

    t_license = None
    t_terms = None
    t_obj_id = None
    t_source_token = None
    t_occurred_at = None
    t_subj_id = None
    t_id = None
    t_evidence_record = None
    t_action = None
    t_subj_pid = None
    t_subj_title = None
    t_subj_type = None
    t_source_id = None
    t_obj_pid = None
    t_obj_url = None
    t_timestamp = None
    t_relation_type_id = None

    for key, value in uniqueEvent.items():
        if (key == "license"):
            t_license = value
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
        elif (key == "terms"):
            t_terms = value
        elif (key == "action"):
            t_action = value
        elif (key == 'subj'):
            subj_fields = uniqueEvent.get("subj")
            for key, value in subj_fields.items():
                if(key == 'pid'):
                    t_subj_pid = value
                elif(key == 'type'):
                    t_subj_type = value
                elif(key == 'title'):
                    t_subj_title = value
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
        elif (key == 'relation_type_id'):
            t_relation_type_id = value

    if (t_obj_id != None):

        # Insert t_obj_id from the event of the JSON file into the main table
        objectIDInsertionQuery = "INSERT IGNORE INTO main (objectID) VALUES(\'" + \
            t_obj_id + "\');"
        cursor.execute(objectIDInsertionQuery)
        connection.commit()

        # Fetch all records from the 4 columns in the main table from t_obj_id and is placed into a list of tuples.
        # (firstWordpressEvent, lastWordpressevent, totalEvents, totalWordpressEvents)
        listOfDictQuery = "SELECT firstWordpressEvent, lastWordpressEvent, totalEvents, totalWordpressEvents FROM Main WHERE objectID = \'" + t_obj_id + "\';"
        cursor.execute(listOfDictQuery)
        listOfTuples = cursor.fetchone()

        # Initialize objects to tuple values
        firstEvent = listOfTuples[0]
        lastEvent = listOfTuples[1]
        totalEvents = listOfTuples[2]
        totalWordpressEvents = listOfTuples[3]

        # If empty, intialize to 0
        if not totalEvents:
            totalEvents = 0
        if not totalWordpressEvents:
            totalWordpressEvents = 0

        # Convert t_timestamp(timestamp) into t_dateTime(datetime)
        t_dateTime = dateutil.parser.isoparse(t_timestamp)
        t_dateTime = str(t_dateTime)

        # If t_timestamp is less than firstEvent or if firstEvent is NULL, update firstWordpressEvent with t_dateTime in the same row in the main table.
        if ((t_timestamp < str(firstEvent)) or (firstEvent == None)):
            updateFirstEventQuery = "UPDATE main SET firstWordpressEvent = \'" + \
                t_dateTime + "\' WHERE objectID = \'" + t_obj_id + "\';"
            cursor.execute(updateFirstEventQuery)
            connection.commit()

        # If t_timestamp is greater than lastEvent or if lastEvent is NULL, update lastWordpressEvent with t_dateTime in the same row in the main table.
        if ((t_timestamp > str(lastEvent)) or (lastEvent == None)):
            updateLastEventQuery = "UPDATE main SET lastWordpressEvent = \'" + \
                t_dateTime + "\' WHERE objectID = \'" + t_obj_id + "\';"
            cursor.execute(updateLastEventQuery)
            connection.commit()

        # Increment event count
        totalEvents += 1
        totalWordpressEvents += 1

        # Update totalEvents and totalWordpressEvents in the main table
        updateTotalEventsQuery = "UPDATE main SET totalEvents = " + str(totalEvents) + \
            ", totalWordpressEvents = " + str(totalWordpressEvents) + \
            " WHERE objectID = \'" + t_obj_id + "\';"

        cursor.execute(updateTotalEventsQuery)
        connection.commit()

        # SQL which inserts into dataciteevent table
        add_event = ("INSERT IGNORE INTO WordPressEvent " "(license, termsOfUse, objectID, sourceToken, occurredAt, subjectID, eventID, evidenceRecord, eventAction, subjectPID, subjectTitle, subjectType, sourceID, objectPID, objectURL, timeObserved, relationType) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        # Values to insert into wordpressevent tabls
        data_event = (t_license, t_terms, t_obj_id, t_source_token, t_occurred_at, t_subj_id, t_id, t_evidence_record, t_action,
                      t_subj_pid, t_subj_title, t_subj_type, t_source_id, t_obj_pid, t_obj_url, t_timestamp, t_relation_type_id)

        cursor.execute(add_event, data_event)
        connection.commit()
