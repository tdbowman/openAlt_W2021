def cambiaLensIngest(uniqueEvent, cursor, connection):

    # Updated fields do not always exist. So I set them as empty sting in case
    t_license = None
    t_updated_reason = None
    t_updated = None
    t_obj_id = None
    t_source_token = None
    t_occurred_at = None
    t_subj_id = None
    t_id = None
    t_terms = None
    t_action = None
    t_work_subtype_id = None
    t_work_id = None
    t_title = None
    t_pid = None
    t_jurisdiction = None
    t_source_id = None
    t_timestamp = None
    t_updated_date = None
    t_relation_type_id = None

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
        elif key == ("terms"):
            t_terms = value
        elif (key == "action"):
            t_action = value
        elif (key == "subj"):
            # value of subj is a dict:
            subj_field = uniqueEvent.get('subj')
            for key, value in subj_field.items():
                if(key == 'work_subtype_id'):
                    t_work_subtype_id = value
                elif(key == 'work_type_id'):  # work_type_id
                    t_work_id = value
                elif(key == 'title'):  # title
                    t_title = value
                elif(key == 'pid'):  # pid
                    t_pid = value
                elif(key == 'jurisdiction'):  # jurisdiction
                    t_subj_jurisdiction = value
        elif (key == "source_id"):
            t_source_id = value
        elif (key == "timestamp"):
            t_timestamp = value
        elif (key == "updated_date"):
            t_updated_date = value
        elif (key == "relation_type_id"):
            t_relation_type_id = value

    # SQL which inserts into event table
    add_event = ("INSERT IGNORE INTO CambiaEvent " "(eventID, objectID, license, updatedReason, updated, sourceToken, occurredAt, subjectID, termsOfUse, eventAction, workSubtypeID, workTypeID, subjectTitle, subjectPID, jurisdiction, sourceID, timeObserved, updatedDate, relationType) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    # Values to insert into event table
    data_event = (t_id, t_obj_id, t_license, t_updated_reason, t_updated, t_source_token, t_occurred_at, t_subj_id, t_terms, t_action,
                  t_work_subtype_id, t_work_id, t_title, t_pid, t_jurisdiction, t_source_id, t_timestamp, t_updated_date, t_relation_type_id)

    cursor.execute(add_event, data_event)  # add information to cambia table
    connection.commit()
