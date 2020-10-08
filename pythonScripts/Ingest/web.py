def webIngest(uniqueEvent, cursor, connection):
    # Updated fields do not always exist. So I set them as empty sting in case
    t_updated_reason = None
    t_updated_date = None
    t_updated = None
    for key, value in uniqueEvent.items():
        if (key == "terms"):
            t_terms = value
        elif (key == "updated_reason"):
            t_updatedReason = value
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
        elif (key == "action"):
            t_action = value
        elif (key == 'subj'):
            subj_fields = uniqueEvent.get("subj")
            for key, value in subj_fields.items():
                if(key == 'pid'):
                    t_subj_pid = value
                elif(key == 'url'):
                    t_subj_url = value
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

    # SQL which inserts into event table
    add_event = ("INSERT IGNORE INTO webEvent " "(eventID, objectID, occurredAt, termsOfUse, updatedReason, updated, sourceToken, subjectID, evidenceRecord, eventAction, subjectPID, subjectURL, sourceID, objectPID, objectURL, timeObserved, updatedDate, relationType) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    # Values to insert into event table
    data_event = (t_id, t_obj_id, t_occurred_at, t_terms, t_updatedReason, t_updated, t_source_token, t_subj_id, t_evidence_record,
                  t_action, t_subj_pid, t_subj_url, t_source_id, t_obj_pid, t_obj_url, t_timestamp, t_updated_date, t_relation_type_id)

    add_to_main = (
        "INSERT IGNORE INTO main (objectID) VALUES (\'" + t_obj_id + "\')")

    cursor.execute(add_to_main)
    cursor.execute(add_event, data_event)  # add information to reddit table
    # Helps check if rows are inserting. Helps me sleep at night. print(cursor.rowcount, "record inserted.")
    connection.commit()
