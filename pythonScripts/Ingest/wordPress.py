def wordPressIngest(uniqueEvent, cursor, connection):
    t_license = None
    t_terms = None
    t_obj_id = None
    t_source_token = None
    t_occurred_at = None
    t_subj_id = None
    t_id = None
    t_evidence_record = None
    t_action = None
    t_subj_pid = None
    t_subj_title = None
    t_subj_type = None
    t_source_id = None
    t_obj_pid = None
    t_obj_url = None
    t_timestamp = None
    t_relation_type_id = None
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
        elif (key == "action"):
            t_action = value
        elif (key == 'subj'):
            subj_fields = uniqueEvent.get("subj")
            for key, value in subj_fields.items():
                if(key == 'pid'):
                    t_subj_pid = value
                elif(key == 'type'):
                    t_subj_type = value
                elif(key == 'title'):
                    t_subj_title = value
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

        if (t_obj_id != None):
        # SQL which inserts into dataciteevent table
            add_event = ("INSERT IGNORE INTO WordPressEvent " "(license, termsOfUse, objectID, sourceToken, occurredAt, subjectID, eventID, evidenceRecord, eventAction, subjectPID, subjectTitle, subjectType, sourceID, objectPID, objectURL, timeObserved, relationType) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            # Values to insert into wordpressevent tabls
            data_event = (t_license, t_terms, t_obj_id, t_source_token, t_occurred_at, t_subj_id, t_id, t_evidence_record, t_action, t_subj_pid, t_subj_title, t_subj_type, t_source_id, t_obj_pid, t_obj_url, t_timestamp, t_relation_type_id)
            add_to_main = ("INSERT IGNORE INTO main(objectID) VALUES (\'" + t_obj_id + "\');")
            cursor.execute(add_to_main)
            cursor.execute(add_event, data_event)
            connection.commit()
