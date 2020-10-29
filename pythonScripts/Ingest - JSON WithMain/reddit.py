def redditIngest(uniqueEvent, cursor, connection):
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
    t_evidence_record = None
    t_terms = None
    t_action = None
    t_subj_pid = None
    t_subj_type = None
    t_subj_title = None
    t_subj_issued = None
    t_source_id = None
    t_obj_pid = None
    t_obj_url = None
    t_timestamp = None
    t_relation_type_id = None
    t_updated_date = None

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
        elif (key == "evidence_record"):
            t_evidence_record = value
        elif key == "terms":
            t_terms = value
        elif (key == "action"):
            t_action = value
        elif (key == "subj"):
            subjField = uniqueEvent.get("subj")
            for key, value in subjField.items():
                if (key == 'pid'):
                    t_subj_pid = value
                elif (key == 'type'):
                    t_subj_type = value
                elif (key == 'title'):
                    t_subj_title = value
                elif (key == 'issued'):
                    t_subj_issued = value
        elif (key == "source_id"):
            t_source_id = value
        elif (key == "obj"):
            obj_field = uniqueEvent.get("obj")
            for key, value in obj_field.items():
                if(key == 'pid'):
                    t_obj_pid = value
                elif(key == 'url'):
                    t_obj_url = value
        elif (key == "timestamp"):
            t_timestamp = value
        elif (key == "relation_type_id"):
            t_relation_type_id = value
        elif (key == "updated_date"):
            t_updated_date = value

    # Fetch all records from the 6 columns in the database and is placed into a list of tuples
    listOfDictQuery = "SELECT increment, objectID, totalEvents, totalRedditEvents,firstRedditEvent, lastRedditEvent FROM Main;"
    cursor.execute(listOfDictQuery)
    listOfTuples = cursor.fetchall()

    # This is used for the situation that there may be a match in objectIDs(DOI) between the event in the JSON file and the main table.
    # If there isn't a match then we'll be using an insertion query rather than an update query for an event.
    # The insertion query will be used for the main table.
    updated = False

    # Fetch all records from the 3 columns in the database and is placed into a list of tuples
    timestampQuery = "SELECT eventID, timeObserved, objectID FROM Redditevent;"
    cursor.execute(timestampQuery)
    listOfEventIDAndTimestamps = cursor.fetchall()

    # Iterate through the list of records(which are within tuples)
    # From the main table (increment, objectID, totalEvents, totalRedditEvents,firstRedditEvent, lastRedditEvent)
    for lOfTuple in listOfTuples:

        # If there's an event with an objectID(DOI) within the JSON file that matches a objectID(DOI) within the Reddit Event Table, continue
        if t_obj_id == lOfTuple[1]:

            # DON'T CHANGE THE INCREMENT
            iOfRecord = lOfTuple[0]
            tEvents = lOfTuple[2]
            tRedditEvents = lOfTuple[3]

            # From the Reddit event table (eventID, timeObserved, objectID)
            # This list of tuples(listOfEventIDandTimestamps) is used to compare timestamps of records from the Reddit Event Table to determine the value of the column of firstRedditEvent and lastRedditEvent in the Main table
            for IDandTimestamps in listOfEventIDAndTimestamps:
                # This is used to find the same eventID in the Reddit event table as the firstRedditEvent(eventID) in the main table.
                # This is to make sure we're updating or modifying the firstRedditevent from the main table.
                if lOfTuple[4] == IDandTimestamps[0]:
                    if t_timestamp < str(IDandTimestamps[1]):
                        fRedditEvent = t_id
                    elif str(IDandTimestamps[1]) < t_timestamp:
                        fRedditEvent = IDandTimestamps[0]
                # This is to make sure we're updating or modifying the lastRedditevent from the main table with the same objectID.
                if t_obj_id == IDandTimestamps[2]:
                    if t_timestamp < str(IDandTimestamps[1]):
                        lRedditEvent = IDandTimestamps[0]
                    elif str(IDandTimestamps[1]) < t_timestamp:
                        lRedditEvent = t_id

            tEvents = tEvents + 1
            tRedditEvents = tRedditEvents + 1

            # Update query used to modify the record at a specific row(record) in the main table.
            updateQuery = "UPDATE Main SET totalEvents = %s, totalRedditEvents = %s, firstRedditEvent = %s, lastRedditEvent = %s WHERE increment = %s;"

            updateValues = (tEvents, tRedditEvents, fRedditEvent,
                            lRedditEvent, iOfRecord)

            # Execute query
            cursor.execute(updateQuery, updateValues)
            connection.commit()

            # An existing row in the main was indeed modified.
            updated = True
    # Inserting a new record in the main table
    if updated == False:
        # Initialize temporary values
        t_total_events = 0
        t_total_Reddit_events = 0
        t_first_Reddit_event = None
        t_last_Reddit_event = None

        t_first_Reddit_event = t_id
        t_total_events += t_total_events + 1
        t_total_Reddit_events += t_total_Reddit_events + 1
        t_last_Reddit_event = t_id

        # Inserting a row(record) query in the main table
        addToMainQuery = (
            "INSERT IGNORE INTO Main " "(objectID,totalEvents,totalRedditEvents,firstRedditEvent,lastRedditEvent) " "VALUES(%s,%s,%s,%s,%s);")

        mainData = (t_obj_id, t_total_events, t_total_Reddit_events,
                    t_first_Reddit_event, t_last_Reddit_event)

        # Execute query
        cursor.execute(addToMainQuery, mainData)
        connection.commit()

    # These statements are used to insert data into Reddit Event's Table
    # SQL which inserts into event table
    add_event = ("INSERT IGNORE INTO redditevent " "(license, termsOfUse, updatedReason, updated, updatedDate, objectID, objectPID, objectURL, sourceToken, occurredAt, subjectID, eventID, evidenceRecord, eventAction, sourceID, subjectPID, subjectType, subjectTitle, subjectIssuedDate, timeObserved, relationType) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

    # Values to insert into Newsfeed event table
    data_event = (t_license, t_terms, t_updated_reason, t_updated, t_updated_date, t_obj_id, t_obj_pid, t_obj_url, t_source_token, t_occurred_at,
                  t_subj_id, t_id, t_evidence_record, t_action, t_source_id, t_subj_pid, t_subj_type, t_subj_title, t_subj_issued, t_timestamp, t_relation_type_id)

    # Execute query to add information to Reddit event table
    cursor.execute(add_event, data_event)
    connection.commit()