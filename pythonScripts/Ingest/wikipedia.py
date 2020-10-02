def wikipediaIngest(uniqueEvent, cursor):
    for key, value in uniqueEvent.items():
        if (key == "license"):
            t_license = value
        elif (key == "terms"):
            t_terms = value
        elif (key == "updated_reason"):
            t_updatedReason = value
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
                    t_pid = value
                elif(key == 'url'):
                    t_url = value
                elif(key == 'title'):
                    t_title = value
                elif(key == 'api-url'):
                    t_api_url = value
        elif (key == 'source_id'):
            t_source_id = value
        elif (key == 'obj'):
            obj_fields = uniqueEvent.get('obj')
            for key, value in obj_fields.items():
                if(key == 'pid'):
                    t_pid = value
                elif(key == 'url'):
                    t_url = value
        elif (key == 'timestamp'):
            t_timestamp = value
        elif (key == "updated_date"):
            t_updated_date = value
        elif (key == 'relation_type_id'):
            t_relation_type_id = value
    # cursor.execute()
    # Execute some complex SQL statement here
    # INSERT INTO IN
