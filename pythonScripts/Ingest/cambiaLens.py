import dateutil.parser


def cambiaLensIngest(uniqueEvent, cursor, connection):

    # These are all temporary objects used to store the values of the fields in the JSON files.
    # Some fields may not always exist. We were getting errors when we didn't have some fields initialized so we decided to initialize all the fields.
    # The layout here is based upon the JSON file layout and is different from the crossrefeventdatamain database's table layout.

    t_license = None
    t_updated_reason = None
    t_updated = None
    t_obj_id = None
    t_source_token = None
    t_occurred_at = None
    t_subj_id = None
    t_id = None
    t_terms = None
    t_action = None
    t_work_subtype_id = None
    t_work_id = None
    t_title = None
    t_pid = None
    t_jurisdiction = None
    t_source_id = None
    t_timestamp = None
    t_updated_date = None
    t_relation_type_id = None

    # Initialize the temporary objects with the values of the fields in the JSON file.
    for key, value in uniqueEvent.items():
        if key == "license":
            t_license = value
        elif (key == "updated_reason"):
            t_updated_reason = value
        elif (key == "updated"):
            t_updated = value
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
        elif key == ("terms"):
            t_terms = value
        elif (key == "action"):
            t_action = value
        elif (key == "subj"):
            # Value of subj is a dict so we must go inside it to retrieve the values
            subj_field = uniqueEvent.get('subj')
            for key, value in subj_field.items():
                if(key == 'work_subtype_id'):
                    t_work_subtype_id = value
                elif(key == 'work_type_id'):
                    t_work_id = value
                elif(key == 'title'):
                    t_title = value
                elif(key == 'pid'):
                    t_pid = value
                elif(key == 'jurisdiction'):
                    t_jurisdiction = value
        elif (key == "source_id"):
            t_source_id = value
        elif (key == "timestamp"):
            t_timestamp = value
        elif (key == "updated_date"):
            t_updated_date = value
        elif (key == "relation_type_id"):
            t_relation_type_id = value

    try:
        # Insert t_obj_id from the event of the JSON file into the main table
        objectIDInsertionQuery = "INSERT IGNORE INTO main (objectID) VALUES(\'" + \
            t_obj_id + "\');"
        cursor.execute(objectIDInsertionQuery)
        connection.commit()

        # Fetch all records from the 4 columns in the main table from t_obj_id and is placed into a list of tuples.
        # (firstCambiaEvent, lastCambiaevent, totalEvents, totalCambiaEvents)
        listOfDictQuery = "SELECT firstCambiaEvent, lastCambiaEvent, totalEvents, totalCambiaEvents FROM Main WHERE objectID = \'" + t_obj_id + "\';"
        cursor.execute(listOfDictQuery)
        row = cursor.fetchone()

        if (type(row) == dict):
            # Initialize objects to dictionary key values
            firstEvent = row['firstCambiaEvent']
            lastEvent = row['lastCambiaEvent']
            totalEvents = row['totalEvents']
            totalCambiaEvents = row['totalCambiaEvents']
        elif (type(row) == tuple):
            # Initialize objects to tuple values
            firstEvent = row[0]
            lastEvent = row[1]
            totalEvents = row[2]
            totalCambiaEvents = row[3]

    # If we enter this except block, most likely the DOI was long gibberish and was unable to be entered into the main table which is VARCHAR(100)
    except:
        return  # just return to main.py, this event will not be ingested

    # If empty, intialize to 0
    if not totalEvents:
        totalEvents = 0
    if not totalCambiaEvents:
        totalCambiaEvents = 0

    # Convert t_timestamp(timestamp) into t_dateTime(datetime)
    t_dateTime = dateutil.parser.isoparse(t_timestamp)
    t_dateTime = str(t_dateTime)

    # If t_timestamp is less than firstEvent or if firstEvent is NULL, update firstCambiaEvent with t_dateTime in the same row in the main table.
    if ((t_timestamp < str(firstEvent)) or (firstEvent == None)):
        updateFirstEventQuery = "UPDATE main SET firstCambiaEvent = \'" + \
            t_dateTime + "\' WHERE objectID = \'" + t_obj_id + "\';"
        cursor.execute(updateFirstEventQuery)
        connection.commit()

    # If t_timestamp is greater than lastEvent or if lastEvent is NULL, update lastCambiaEvent with t_dateTime in the same row in the main table.
    if ((t_timestamp > str(lastEvent)) or (lastEvent == None)):
        updateLastEventQuery = "UPDATE main SET lastCambiaEvent = \'" + \
            t_dateTime + "\' WHERE objectID = \'" + t_obj_id + "\';"
        cursor.execute(updateLastEventQuery)
        connection.commit()

    # Increment event count
    totalEvents += 1
    totalCambiaEvents += 1

    # Update totalEvents and totalCambiaEvents in the main table
    updateTotalEventsQuery = "UPDATE main SET totalEvents = " + str(totalEvents) + \
        ", totalCambiaEvents = " + str(totalCambiaEvents) + \
        " WHERE objectID = \'" + t_obj_id + "\';"

    cursor.execute(updateTotalEventsQuery)
    connection.commit()

    # These statements are used to insert data into Cambia Event's Table
    # SQL which inserts into event table
    add_event = ("INSERT IGNORE INTO CambiaEvent " "(sourceID, objectID, subjectID, eventID, occurredAt, timeObserved, relationType, sourceToken, license, termsOfUse, updatedReason, updated, eventAction, workSubtypeID, workTypeID, subjectTitle, subjectPID, jurisdiction, updatedDate) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);")

    # Values to insert into Cambia Event Table
    data_event = (t_source_id, t_obj_id, t_subj_id, t_id, t_occurred_at, t_timestamp, t_relation_type_id, t_source_token, t_license, t_terms, t_updated_reason, t_updated, t_action,
                  t_work_subtype_id, t_work_id, t_title, t_pid, t_jurisdiction,  t_updated_date)

    # Execute query to add information to Cambia event table
    cursor.execute(add_event, data_event)
    connection.commit()
