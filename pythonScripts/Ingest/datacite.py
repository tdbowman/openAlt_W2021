def dataciteIngest(uniqueEvent, cursor, connection):
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

    # SQL which inserts into dataciteevent table  - LEAVE OUT THE OBJECT ID
    add_event = ("INSERT IGNORE INTO DataCiteEvent " "(license, objectID, occurredAt, subjectID, eventID, termsOfUse, messageAction, sourceID, timeObserved, relationType) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)")
    # Values to insert into dataciteevent tabls  - LEAVE OUT THE OBJECT ID
    data_event = (t_license, t_obj_id, t_occurred_at, t_subj_id, t_id, t_terms, t_message_action, t_source_id, t_timestamp, t_relation_type_id)

    add_to_main =("INSERT IGNORE INTO main (objectID) VALUES (\'" + t_obj_id + "\');")

    cursor.execute(add_to_main)
    cursor.execute(add_event, data_event) # add information to dataciteevent table
    connection.commit()
