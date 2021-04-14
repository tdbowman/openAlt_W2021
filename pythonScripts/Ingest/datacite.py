import dateutil.parser
import datetime
import pytz


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


    if(len(t_obj_id) < 100):
        # Insert t_obj_id from the event of the JSON file into the main table
        objectIDInsertionQuery = "INSERT IGNORE INTO main (objectID) VALUES(\'" + \
            t_obj_id + "\');"
        cursor.execute(objectIDInsertionQuery)
        connection.commit()

        # Fetch all records from the 4 columns in the main table from t_obj_id and is placed into a list of tuples.
        # (firstDataciteEvent, lastDataciteevent, totalEvents, totalDataciteEvents)
        listOfDictQuery = "SELECT firstDataciteEvent, lastDataciteEvent, totalEvents, totalDataciteEvents FROM main WHERE objectID = \'" + t_obj_id + "\';"
        cursor.execute(listOfDictQuery)
        row = cursor.fetchone()

        firstEvent = ""
        lastEvent = ""
        totalEvents = 0
        totalDataciteEvents = 0

        if (type(row) == dict):
            # Initialize objects to dictionary key values
            firstEvent = row['firstDataciteEvent']
            lastEvent = row['lastDataciteEvent']
            if row['totalEvents'] is not None:
                totalEvents = row['totalEvents']
            if row['totalDataciteEvents'] is not None:
                totalDataciteEvents = row['totalDataciteEvents']
        elif (type(row) == tuple):
            # Initialize objects to tuple values
            firstEvent = row[0]
            lastEvent = row[1]

            if row[2] is not None:
                totalEvents = row[2]
            if row[3] is not None:
                totalDataciteEvents = row[3]

    # If we enter this except block, most likely the DOI was long gibberish and was unable to be entered into the main table which is VARCHAR(100)
    elif (len(t_obj_id) >= 100):
        return  # just return to main.py, this event will not be ingested

    # Convert t_timestamp(timestamp) into a localized time
    t_dateTime = dateutil.parser.isoparse(t_timestamp)
    t_dateTime = t_dateTime.astimezone(pytz.timezone("US/Michigan"))
    t_dateTime = t_dateTime.strftime("%Y-%m-%d %H:%M:%S")

    # If t_dateTime is less than firstEvent or if firstEvent is NULL, update firstDataciteEvent with t_dateTime in the same row in the main table.
    if ((t_dateTime < str(firstEvent)) or (firstEvent == None)):
        updateFirstEventQuery = "UPDATE main SET firstDataciteEvent = \'" + \
            t_dateTime + "\' WHERE objectID = \'" + t_obj_id + "\';"
        cursor.execute(updateFirstEventQuery)
        connection.commit()

    # If t_dateTime is greater than lastEvent or if lastEvent is NULL, update lastDataciteEvent with t_dateTime in the same row in the main table.
    if ((t_dateTime > str(lastEvent)) or (lastEvent == None)):
        updateLastEventQuery = "UPDATE main SET lastDataciteEvent = \'" + \
            t_dateTime + "\' WHERE objectID = \'" + t_obj_id + "\';"
        cursor.execute(updateLastEventQuery)
        connection.commit()

    # Increment event count
    totalEvents += 1
    totalDataciteEvents += 1

    # Update totalEvents and totalDataciteEvents in the main table
    updateTotalEventsQuery = "UPDATE main SET totalEvents = " + str(totalEvents) + \
        ", totalDataciteEvents = " + str(totalDataciteEvents) + \
        " WHERE objectID = \'" + t_obj_id + "\';"

    cursor.execute(updateTotalEventsQuery)
    connection.commit()

    # These statements are used to insert data into Crossref Event's Table
    # SQL which inserts into event table
    # This was a previous layout of columns in the Datacite event table before we remodeled the database
    add_event = ("INSERT IGNORE INTO dataciteevent " "(license, objectID, occurredAt, subjectID, eventID, termsOfUse, messageAction, sourceID, timeObserved, relationType) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)")

    # Values to insert into Datacite event table
    data_event = (t_license, t_obj_id, t_occurred_at, t_subj_id, t_id, t_terms,
                  t_message_action, t_source_id, t_dateTime, t_relation_type_id)

    # Execute query to add information to Datacite event table
    cursor.execute(add_event, data_event)
    connection.commit()
