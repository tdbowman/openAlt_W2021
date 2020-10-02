def cambiaLensIngest(uniqueEvent, cursor):
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
                    t_jurisdiction = value
        elif (key == "source_id"):
            t_source_id = value
        elif (key == "timestamp"):
            t_timestamp = value
        elif (key == "updated_date"):
            t_updated_date = value
        elif (key == "relation_type_id"):
            t_relation_type_id = value
    # cursor.execute()
    # Execute some complex SQL statement here
    # INSERT INTO IN
