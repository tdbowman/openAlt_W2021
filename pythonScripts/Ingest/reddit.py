def redditIngest(uniqueEvent, cursor, connection):
    # Updated fields do not always exist. So I set them as empty sting in case
    t_updated_reason = None
    t_updated_date = None
    t_updated = None
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
    
    # SQL which inserts into event table
    add_event = ("INSERT IGNORE INTO redditevent " "(license, termsOfUse, updatedReason, updated, updatedDate, objectID, objectPID, objectURL, sourceToken, occurredAt, subjectID, eventID, evidenceRecord, eventAction, sourceID, subjectPID, subjectType, subjectTitle, subjectIssuedDate, timeObserved, relationType) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    # Values to insert into event table
    data_event = (t_license, t_terms, t_updated_reason, t_updated, t_updated_date, t_obj_id, t_obj_pid, t_obj_url, t_source_token, t_occurred_at, t_subj_id, t_id, t_evidence_record, t_action, t_source_id, t_subj_pid, t_subj_type, t_subj_title, t_subj_issued, t_timestamp, t_relation_type_id)

    add_to_main =("INSERT IGNORE INTO main (objectID) VALUES (\'" + t_obj_id + "\');")

    cursor.execute(add_to_main)
    cursor.execute(add_event, data_event) # add information to dataciteevent table
    connection.commit()