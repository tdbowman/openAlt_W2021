def stackExchangeIngest(uniqueEvent, cursor, connection):
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
                    t_pid = value
                elif(key == 'title'):
                    t_title = value
                elif(key == 'issued'):
                    t_issued = value
                elif(key == 'type'):
                    t_type = value
                elif(key == 'author'):
                    authorField = subj_fields.get("author")
                # value of author is a dict, has url
                    for key, value in authorField.items():
                        if(key == 'url'):
                            t_url = value
                        elif(key == 'name'):
                            t_name = value
                        elif(key == 'id'):
                            t_id = value
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
        elif (key == 'relation_type_id'):
            t_relation_type_id = value
    # cursor.execute()
    # Execute some complex SQL statement here
    # INSERT INTO IN
