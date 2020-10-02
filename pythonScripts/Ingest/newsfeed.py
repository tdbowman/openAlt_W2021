def newsfeedIngest(uniqueEvent, cursor, connection):
    for key, value in uniqueEvent.items():
        if key == "license":
            t_license = value
        elif key == "terms":
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
        elif (key == "subj"):
            subjField = uniqueEvent.get("subj")
            for key, value in subjField.items():
                if (key == 'pid'):
                    t_pid = value
                elif (key == 'type'):
                    t_type = value
                elif (key == 'title'):
                    t_title = value
                elif(key == 'url'):
                    t_url = value
        elif(key == 'source_id'):
            t_source_id = value
        elif (key == "obj"):
            objField = uniqueEvent.get("obj")
            for key, value in objField.items():
                if (key == 'pid'):
                    t_pid = value
                if (key == 'url'):
                    t__obj_url = value
        elif (key == "timestamp"):
            t_timestamp = value
        elif(key == 'updated_date'):
            t_updated_date = value
        elif(key == 'relation_type_id'):
            t_relation_type_id = value
            
    # SQL which inserts into event table
    add_event = ("INSERT IGNORE INTO NewsfeedEvent " "(eventID, objectID, occurredAt, license, termsOfUse, updatedReason, updated, sourceToken, subjectID, evidenceRecord, eventAction, subjectPID, subjectType, subjectTitle, subjectURL, sourceID, objectPID, objectURL, timeObserved, updatedDate, relationType) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)")

    # Values to insert into event table
    data_event = (t_id, t_obj_id, t_occurred_at, t_license, t_terms, t_updatedReason, t_updated, t_source_token, t_subj_id, t_evidence_record, t_action, t_subj_id, t_type, t_title, t_url, t_source_id, t_obj_id, t__obj_url, t_timestamp, t_updated_date, t_relation_type_id)

    add_to_main =("INSERT IGNORE INTO main (objectID) VALUES (\'" + t_obj_id + "\');")

    cursor.execute(add_to_main)
    cursor.execute(add_event, data_event) # add information to hypothesis table
    connection.commit()   
