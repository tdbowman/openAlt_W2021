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

    # Fetch all records from the 6 columns in the database and is placed into a list of tuples
    listOfDictQuery = "SELECT increment, objectID, totalEvents, totalCambiaEvents,firstCambiaEvent, lastCambiaEvent FROM Main;"
    cursor.execute(listOfDictQuery)
    listOfTuples = cursor.fetchall()

    # This is used for the situation that there may be a match in objectIDs(DOI) between the event in the JSON file and the main table.
    # If there isn't a match then we'll be using an insertion query rather than an update query for an event.
    # The insertion query will be used for the main table.
    updated = False

    # Fetch all records from the 3 columns in the database and is placed into a list of tuples
    timestampQuery = "SELECT eventID, timeObserved, objectID FROM cambiaevent;"
    cursor.execute(timestampQuery)
    listOfEventIDAndTimestamps = cursor.fetchall()

    # Iterate through the list of records(which are within tuples)
    # From the main table (increment, objectID, totalEvents, totalCambiaEvents,firstCambiaEvent, lastCambiaEvent)
    for lOfTuple in listOfTuples:

        # If there's an event with an objectID(DOI) within the JSON file that matches a objectID(DOI) within the Cambia Event Table, continue
        if t_obj_id == lOfTuple[1]:

            # DON'T CHANGE THE INCREMENT
            iOfRecord = lOfTuple[0]
            tEvents = lOfTuple[2]
            tCambiaEvents = lOfTuple[3]

            # From the Cambia event table (eventID, timeObserved,objectID)
            # This list of tuples(listOfEventIDandTimestamps) is used to compare timestamps of records from the Cambia Event Table to determine the value of the column of firstCambiaEvent and lastCambiaEvent in the Main table
            for IDandTimestamps in listOfEventIDAndTimestamps:
                # This is used to find the same eventID in the Cambia event table as the firstCambiaEvent(eventID) in the main table.
                # This is to make sure we're updating or modifying the firstCambiaevent from the main table.
                if lOfTuple[4] == IDandTimestamps[0]:
                    if t_timestamp < str(IDandTimestamps[1]):
                        fCambiaEvent = t_id
                    elif str(IDandTimestamps[1]) < t_timestamp:
                        fCambiaEvent = IDandTimestamps[0]
                # This is to make sure we're updating or modifying the lastCambiaevent from the main table with the same objectID.
                if t_obj_id == IDandTimestamps[2]:
                    if t_timestamp < str(IDandTimestamps[1]):
                        lCambiaEvent = IDandTimestamps[0]
                    elif str(IDandTimestamps[1]) < t_timestamp:
                        lCambiaEvent = t_id

            tEvents = tEvents + 1
            tCambiaEvents = tCambiaEvents + 1

            # Update query used to modify the record at a specific row(record) in the main table.
            updateQuery = "UPDATE Main SET totalEvents = %s, totalCambiaEvents = %s, firstCambiaEvent = %s, lastCambiaEvent = %s WHERE increment = %s;"

            updateValues = (tEvents, tCambiaEvents, fCambiaEvent,
                            lCambiaEvent, iOfRecord)

            # Execute query.
            cursor.execute(updateQuery, updateValues)
            connection.commit()

            # An existing row in the main was indeed modified.
            updated = True

    # Inserting a new record in the main table.
    if updated == False:
        # Initialize temporary values
        t_total_events = 0
        t_total_Cambia_events = 0
        t_first_Cambia_event = None
        t_last_Cambia_event = None

        t_first_Cambia_event = t_id
        t_total_events += t_total_events + 1
        t_total_Cambia_events += t_total_Cambia_events + 1
        t_last_Cambia_event = t_id

        # Inserting a row(record) query in the main table
        addToMainQuery = (
            "INSERT IGNORE INTO Main " "(objectID,totalEvents,totalCambiaEvents,firstCambiaEvent,lastCambiaEvent) " "VALUES(%s,%s,%s,%s,%s);")

        mainData = (t_obj_id, t_total_events, t_total_Cambia_events,
                    t_first_Cambia_event, t_last_Cambia_event)

        # Execute query
        cursor.execute(addToMainQuery, mainData)
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
