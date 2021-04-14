import dateutil.parser
import datetime
import pytz


def crossrefIngest(uniqueEvent, cursor, connection):

    # These are all temporary objects used to store the values of the fields in the JSON files.
    # Some fields may not always exist. We were getting errors when we didn't have some fields initialized so we decided to initialize all the fields.
    # The layout here is based upon the JSON file layout and is different from the crossrefeventdatamain database's table layout.

    t_license = None
    t_obj_id = None
    t_source_token = None
    t_occurred_at = None
    t_subj_id = None
    t_id = None
    t_terms = None
    t_message_action = None
    t_source_id = None
    t_timestamp = None
    t_relation_type_id = None

    # Initialize the temporary objects with the values of the fields in the JSON file.
    for key, value in uniqueEvent.items():
        if key == "license":
            t_license = value
        elif key == "obj_id":
            t_obj_id = value
        elif (key == "source_token"):
            t_source_token = value
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


    if(len(t_obj_id) < 100):
        # Insert t_obj_id from the event of the JSON file into the main table
        objectIDInsertionQuery = "INSERT IGNORE INTO main (objectID) VALUES(\'" + \
            t_obj_id + "\');"
        cursor.execute(objectIDInsertionQuery)
        connection.commit()

        # Fetch all records from the 4 columns in the main table from t_obj_id and is placed into a list of tuples.
        # (firstCrossrefEvent, lastCrossrefevent, totalEvents, totalCrossrefEvents)
        listOfDictQuery = "SELECT firstCrossrefEvent, lastCrossrefEvent, totalEvents, totalCrossrefEvents FROM main WHERE objectID = \'" + t_obj_id + "\';"
        cursor.execute(listOfDictQuery)
        row = cursor.fetchone()

        firstEvent = ""
        lastEvent = ""
        totalEvents = 0
        totalCrossrefEvents = 0

        if (type(row) == dict):
            # Initialize objects to dictionary key values
            firstEvent = row['firstCrossrefEvent']
            lastEvent = row['lastCrossrefEvent']
            if row['totalEvents'] is not None:
                totalEvents = row['totalEvents']
            if row['totalCrossrefEvents'] is not None:
                totalCrossrefEvents = row['totalCrossrefEvents']
        elif (type(row) == tuple):
            # Initialize objects to tuple values
            firstEvent = row[0]
            lastEvent = row[1]

            if row[2] is not None:
                totalEvents = row[2]
            if row[3] is not None:
                totalCrossrefEvents = row[3]

    # If we enter this except block, most likely the DOI was long gibberish and was unable to be entered into the main table which is VARCHAR(100)
    elif (len(t_obj_id) >= 100):
        return  # just return to main.py, this event will not be ingested

    # Convert t_timestamp(timestamp) into a localized time
    t_dateTime = dateutil.parser.isoparse(t_timestamp)
    t_dateTime = t_dateTime.astimezone(pytz.timezone("US/Michigan"))
    t_dateTime = t_dateTime.strftime("%Y-%m-%d %H:%M:%S")

    # If t_dateTime is less than firstEvent or if firstEvent is NULL, update firstCrossrefEvent with t_dateTime in the same row in the main table.
    if ((t_dateTime < str(firstEvent)) or (firstEvent == None)):
        updateFirstEventQuery = "UPDATE main SET firstCrossrefEvent = \'" + \
            t_dateTime + "\' WHERE objectID = \'" + t_obj_id + "\';"
        cursor.execute(updateFirstEventQuery)
        connection.commit()

    # If t_dateTime is greater than lastEvent or if lastEvent is NULL, update lastCrossrefEvent with t_dateTime in the same row in the main table.
    if ((t_dateTime > str(lastEvent)) or (lastEvent == None)):
        updateLastEventQuery = "UPDATE main SET lastCrossrefEvent = \'" + \
            t_dateTime + "\' WHERE objectID = \'" + t_obj_id + "\';"
        cursor.execute(updateLastEventQuery)
        connection.commit()

    # Increment event count
    totalEvents += 1
    totalCrossrefEvents += 1

    # Update totalEvents and totalCrossrefEvents in the main table
    updateTotalEventsQuery = "UPDATE main SET totalEvents = " + str(totalEvents) + \
        ", totalCrossrefEvents = " + str(totalCrossrefEvents) + \
        " WHERE objectID = \'" + t_obj_id + "\';"

    cursor.execute(updateTotalEventsQuery)
    connection.commit()

    # These statements are used to insert data into Crossref Event's Table
    # SQL which inserts into event table
    # This was a previous layout of columns in the Crossref event table before we remodeled the database
    add_event = ("INSERT IGNORE INTO crossrefevent " "(license, objectID, sourceToken, occurredAt, subjectID, eventID, crossrefTermsOfUse, messageAction, sourceID, timeObserved, relationType) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

    # Values to insert into Crossref event table
    data_event = (t_license, t_obj_id, t_source_token, t_occurred_at, t_subj_id,
                  t_id, t_terms, t_message_action, t_source_id, t_dateTime, t_relation_type_id)

    # Execute query to add information to Crossref event table
    cursor.execute(add_event, data_event)
    connection.commit()
