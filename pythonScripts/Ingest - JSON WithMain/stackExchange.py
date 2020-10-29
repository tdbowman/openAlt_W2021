def stackExchangeIngest(uniqueEvent, cursor, connection):

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
    t_subj_pid = None
    t_subj_title = None
    t_subj_type = None
    t_source_id = None
    t_obj_pid = None
    t_obj_url = None
    t_timestamp = None
    t_relation_type_id = None
    t_author_id = None
    t_author_url = None
    t_author_name = None

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
        elif (key == 'subj'):
            subj_fields = uniqueEvent.get("subj")
            for key, value in subj_fields.items():
                if(key == 'pid'):
                    t_subj_pid = value
                elif(key == 'title'):
                    t_subj_title = value
                elif(key == 'issued'):
                    t_subj_issued = value
                elif(key == 'type'):
                    t_subj_type = value
                elif(key == 'author'):
                    authorField = subj_fields.get("author")
                # value of author is a dict, has url
                    for key, value in authorField.items():
                        if(key == 'url'):
                            t_author_url = value
                        elif(key == 'name'):
                            t_author_name = value
                        elif(key == 'id'):
                            t_author_id = value
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

    # Fetch all records from the 6 columns in the database and is placed into a list of tuples
    listOfDictQuery = "SELECT increment, objectID, totalEvents, totalstackExchangeEvents,firststackExchangeEvent, laststackExchangeEvent FROM Main;"
    cursor.execute(listOfDictQuery)
    listOfTuples = cursor.fetchall()

    # This is used for the situation that there may be a match in objectIDs(DOI) between the event in the JSON file and the main table.
    # If there isn't a match then we'll be using an insertion query rather than an update query for an event.
    # The insertion query will be used for the main table.
    updated = False

    # Fetch all records from the 3 columns in the database and is placed into a list of tuples
    timestampQuery = "SELECT eventID, timeObserved, objectID FROM stackExchangeevent;"
    cursor.execute(timestampQuery)
    listOfEventIDAndTimestamps = cursor.fetchall()

    # Iterate through the list of records(which are within tuples)
    # From the main table (increment, objectID, totalEvents, totalstackExchangeEvents,firststackExchangeEvent, laststackExchangeEvent)
    for lOfTuple in listOfTuples:

        # If there's an event with an objectID(DOI) within the JSON file that matches a objectID(DOI) within the stackExchange Event Table, continue
        if t_obj_id == lOfTuple[1]:

            # DON'T CHANGE THE INCREMENT
            iOfRecord = lOfTuple[0]
            tEvents = lOfTuple[2]
            tstackExchangeEvents = lOfTuple[3]

            # From the stackExchange event table (eventID, timeObserved, objectID)
            # This list of tuples(listOfEventIDandTimestamps) is used to compare timestamps of records from the stackExchange Event Table to determine the value of the column of firststackExchangeEvent and laststackExchangeEvent in the Main table
            for IDandTimestamps in listOfEventIDAndTimestamps:
                # This is used to find the same eventID in the stackExchange event table as the firststackExchangeEvent(eventID) in the main table.
                # This is to make sure we're updating or modifying the firststackExchangeevent from the main table.
                if lOfTuple[4] == IDandTimestamps[0]:
                    if t_timestamp < str(IDandTimestamps[1]):
                        fstackExchangeEvent = t_id
                    elif str(IDandTimestamps[1]) < t_timestamp:
                        fstackExchangeEvent = IDandTimestamps[0]
                # This is to make sure we're updating or modifying the laststackExchangeevent from the main table with the same objectID.
                if t_obj_id == IDandTimestamps[2]:
                    if t_timestamp < str(IDandTimestamps[1]):
                        lstackExchangeEvent = IDandTimestamps[0]
                    elif str(IDandTimestamps[1]) < t_timestamp:
                        lstackExchangeEvent = t_id

            tEvents = tEvents + 1
            tstackExchangeEvents = tstackExchangeEvents + 1

            # Update query used to modify the record at a specific row(record) in the main table.
            updateQuery = "UPDATE Main SET totalEvents = %s, totalstackExchangeEvents = %s, firststackExchangeEvent = %s, laststackExchangeEvent = %s WHERE increment = %s;"

            updateValues = (tEvents, tstackExchangeEvents, fstackExchangeEvent,
                            lstackExchangeEvent, iOfRecord)

            # Execute query
            cursor.execute(updateQuery, updateValues)
            connection.commit()

            # An existing row in the main was indeed modified.
            updated = True
    # Inserting a new record in the main table
    if updated == False:
        # Initialize temporary values
        t_total_events = 0
        t_total_stackExchange_events = 0
        t_first_stackExchange_event = None
        t_last_stackExchange_event = None

        t_first_stackExchange_event = t_id
        t_total_events += t_total_events + 1
        t_total_stackExchange_events += t_total_stackExchange_events + 1
        t_last_stackExchange_event = t_id

        # Inserting a row(record) query in the main table
        addToMainQuery = (
            "INSERT IGNORE INTO Main " "(objectID,totalEvents,totalstackExchangeEvents,firststackExchangeEvent,laststackExchangeEvent) " "VALUES(%s,%s,%s,%s,%s);")

        mainData = (t_obj_id, t_total_events, t_total_stackExchange_events,
                    t_first_stackExchange_event, t_last_stackExchange_event)

        # Execute query
        cursor.execute(addToMainQuery, mainData)
        connection.commit()

    # These statements are used to insert data into stackExchange Event's Table
    # SQL which inserts into event table
    add_event = ("INSERT IGNORE INTO stackExchangeevent " "(license, termsOfUse, objectID, sourceToken, occurredAt, subjectID, eventID, evidenceRecord,  subjectPID, subjectTitle, subjectIssuedDate, subjectType, subjectAuthorURL, subjectAuthorName, subjectAuthorID, sourceID, objectPID, objectURL, timeObserved, relationType) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

    # Values to insert into stackExchange event table
    data_event = (t_license, t_terms, t_obj_id, t_source_token, t_occurred_at, t_subj_id, t_id, t_evidence_record, t_subj_pid,
                  t_subj_title, t_subj_issued, t_subj_type, t_author_url, t_author_name, t_author_id, t_source_id, t_obj_pid, t_obj_url, t_timestamp, t_relation_type_id)

    # Execute query to add information to Stackexchange event table
    cursor.execute(add_event, data_event)
    connection.commit()
