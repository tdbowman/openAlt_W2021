def cambiaLensIngest(uniqueEvent, cursor):
    for key, value in uniqueEvent.items():
        if key == "license":
            t_license = value
            print(t_license)
        elif (key == "updated_reason"):
            t_updated_reason = value
            print(t_updated_reason)
        elif (key == "updated"):
            t_updated = value
            print(t_updated)
        elif (key == "obj_id"):
            t_obj_id = value
            print(t_obj_id)
        elif (key == "source_token"):
            t_source_token = value
            print(t_source_token)
        elif (key == "occurred_at"):
            t_occurred_at = value
            print(t_occurred_at)
        elif (key == "subj_id"):
            t_subj_id = value
            print(t_subj_id)
        elif (key == "id"):
            t_id = value
            print(t_id)
        elif key == ("terms"):
            t_terms = value
            print(t_terms)
        elif (key == "action"):
            t_action = value
            print(t_action)
        elif (key == "subj"):
            # value of subj is a dict:
            subj_field = uniqueEvent.get('subj')
            for key, value in subj_field.items():
                if(key == 'work_subtype_id'):
                    t_work_subtype_id = value
                    print(t_work_subtype_id)  # work_subtype_id
                elif(key == 'work_type_id'):  # work_type_id
                    t_work_id = value
                    print(t_work_id)
                elif(key == 'title'):  # title
                    t_title = value
                    print(t_title)
                elif(key == 'pid'):  # pid
                    t_pid = value
                    print(t_pid)
                elif(key == 'jurisdiction'):  # jurisdiction
                    t_jurisdiction = value
                    print(t_jurisdiction)
        elif (key == "source_id"):
            t_source_id = value
            print(t_source_id)
        elif (key == "timestamp"):
            t_timestamp = value
            print(t_timestamp)
        elif (key == "updated_date"):
            t_updated_date = value
            print(t_updated_date)
        elif (key == "relation_type_id"):
            t_relation_type_id = value
            print(t_relation_type_id)
    # cursor.execute()
    # Execute some complex SQL statement here
    # INSERT INTO IN
