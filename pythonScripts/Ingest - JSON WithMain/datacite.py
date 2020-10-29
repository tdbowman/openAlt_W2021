def dataciteIngest(uniqueEvent, cursor, connection):

    # These are all temporary objects used to store the values of the fields in the JSON files.
    # Some fields may not always exist. We were getting errors when we didn't have some fields initialized so we decided to initialize all the fields.
    # The layout here is based upon the JSON file layout and is different from the crossrefeventdatamain database's table layout.

    t_license = None
    t_obj_id = None
    t_occurred_at = None
    t_subj_id = None
    t_id = None
    t_terms = None
    t_message_action = None
    t_source_id = None
    t_timestamp = None
    t_relation_type_id = None

    for key, value in uniqueEvent.items():
        if key == "license":
            t_license = value
        elif key == "obj_id":
            t_obj_id = value
        elif (key == "occurred_at"):
            t_occurred_at = value
        elif (key == "subj_id"):
            t_subj_id = value
        elif (key == "id"):
            t_id = value
        elif (key == "terms"):
            t_terms = value
        elif (key == "message_action"):
            t_message_action = value
        elif (key == "source_id"):
            t_source_id = value
        elif (key == "timestamp"):
            t_timestamp = value
        elif (key == "relation_type_id"):
            t_relation_type_id = value

    # Fetch all records from the 6 columns in the database and is placed into a list of tuples
    listOfDictQuery = "SELECT increment, objectID, totalEvents, totalDataciteEvents,firstDataciteEvent, lastDataciteEvent FROM Main;"
    cursor.execute(listOfDictQuery)
    listOfTuples = cursor.fetchall()

    # This is used for the situation that there may be a match in objectIDs(DOI) between the event in the JSON file and the main table.
    # If there isn't a match then we'll be using an insertion query rather than an update query for an event.
    # The insertion query will be used for the main table.
    updated = False

    # Fetch all records from the 3 columns in the database and is placed into a list of tuples
    timestampQuery = "SELECT eventID, timeObserved,objectID FROM Dataciteevent;"
    cursor.execute(timestampQuery)
    listOfEventIDAndTimestamps = cursor.fetchall()

    # Iterate through the list of records(which are within tuples)
    # From the main table (increment, objectID, totalEvents, totalDataciteEvents,firstDataciteEvent, lastDataciteEvent)
    for lOfTuple in listOfTuples:

        # If there's an event with an objectID(DOI) within the JSON file that matches a objectID(DOI) within the Datacite Event Table, continue
        if t_obj_id == lOfTuple[1]:

            # DON'T CHANGE THE INCREMENT
            iOfRecord = lOfTuple[0]
            tEvents = lOfTuple[2]
            tDataciteEvents = lOfTuple[3]

            # From the Datacite event table (eventID, timeObserved, objectID)
            # This list of tuples(listOfEventIDandTimestamps) is used to compare timestamps of records from the Datacite Event Table to determine the value of the column of firstDataciteEvent and lastDataciteEvent in the Main table
            for IDandTimestamps in listOfEventIDAndTimestamps:
                # This is used to find the same eventID in the Datacite event table as the firstDataciteEvent(eventID) in the main table.
                # This is to make sure we're updating or modifying the firstDataciteevent from the main table.
                if lOfTuple[4] == IDandTimestamps[0]:
                    if t_timestamp < str(IDandTimestamps[1]):
                        fDataciteEvent = t_id
                    elif str(IDandTimestamps[1]) < t_timestamp:
                        fDataciteEvent = IDandTimestamps[0]
                # This is to make sure we're updating or modifying the lastDataciteevent from the main table with the same objectID.
                if t_obj_id == IDandTimestamps[2]:
                    if t_timestamp < str(IDandTimestamps[1]):
                        lDataciteEvent = IDandTimestamps[0]
                    elif str(IDandTimestamps[1]) < t_timestamp:
                        lDataciteEvent = t_id

            tEvents = tEvents + 1
            tDataciteEvents = tDataciteEvents + 1

            # Update query used to modify the record at a specific row(record) in the main table.
            updateQuery = "UPDATE Main SET totalEvents = %s, totalDataciteEvents = %s, firstDataciteEvent = %s, lastDataciteEvent = %s WHERE increment = %s;"

            updateValues = (tEvents, tDataciteEvents, fDataciteEvent,
                            lDataciteEvent, iOfRecord)

            # Execute query
            cursor.execute(updateQuery, updateValues)
            connection.commit()

            # An existing row in the main was indeed modified.
            updated = True

    # Inserting a new record in the main table
    if updated == False:
        # Initialize temporary values
        t_total_events = 0
        t_total_Datacite_events = 0
        t_first_Datacite_event = None
        t_last_Datacite_event = None

        t_first_Datacite_event = t_id
        t_total_events += t_total_events + 1
        t_total_Datacite_events += t_total_Datacite_events + 1
        t_last_Datacite_event = t_id

        # Inserting a row(record) query in the main table
        addToMainQuery = (
            "INSERT IGNORE INTO Main " "(objectID,totalEvents,totalDataciteEvents,firstDataciteEvent,lastDataciteEvent) " "VALUES(%s,%s,%s,%s,%s);")

        mainData = (t_obj_id, t_total_events, t_total_Datacite_events,
                    t_first_Datacite_event, t_last_Datacite_event)

        # Execute query
        cursor.execute(addToMainQuery, mainData)
        connection.commit()

    # These statements are used to insert data into Crossref Event's Table
    # SQL which inserts into event table
    add_event = ("INSERT IGNORE INTO DataCiteEvent " "(license, objectID, occurredAt, subjectID, eventID, termsOfUse, messageAction, sourceID, timeObserved, relationType) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)")

    # Values to insert into Datacite event table
    data_event = (t_license, t_obj_id, t_occurred_at, t_subj_id, t_id, t_terms,
                  t_message_action, t_source_id, t_timestamp, t_relation_type_id)

    # Execute query to add information to Datacite event table
    cursor.execute(add_event, data_event)
    connection.commit()
