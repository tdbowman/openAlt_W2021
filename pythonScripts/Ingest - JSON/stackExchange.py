def stackExchangeIngest(uniqueEvent, cursor, connection):
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

    # SQL which inserts into event table
    add_event = ("INSERT IGNORE INTO Stackexchangeevent " "(license, termsOfUse, objectID, sourceToken, occurredAt, subjectID, eventID, evidenceRecord,  subjectPID, subjectTitle, subjectIssuedDate, subjectType, subjectAuthorURL, subjectAuthorName, subjectAuthorID, sourceID, objectPID, objectURL, timeObserved, relationType) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    # Values to insert into event table
    data_event = (t_license, t_terms, t_obj_id, t_source_token, t_occurred_at, t_subj_id, t_id, t_evidence_record, t_subj_pid,
                  t_subj_title, t_subj_issued, t_subj_type, t_author_url, t_author_name, t_author_id, t_source_id, t_obj_pid, t_obj_url, t_timestamp, t_relation_type_id)

    cursor.execute(add_event, data_event)  # add information to reddit table
    # Helps check if rows are inserting. Helps me sleep at night. print(cursor.rowcount, "record inserted.")
    connection.commit()
