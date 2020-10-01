def redditIngest(uniqueEvent, cursor):
    for key, value in uniqueEvent.items():
        if key == "license":
            t_license = value
            print(t_license)
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
        elif (key == "evidence_record"):
            t_evidence_record = value
            print(t_evidence_record)
        elif key == "terms":
            t_terms = value
            print(t_terms)
        elif (key == "action"):
            t_action = value
            print(t_action)
        elif (key == "subj"):
            subjField = uniqueEvent.get("subj")
            for key, value in subjField.items():
                if (key == 'pid'):
                    t_pid = value
                    print(t_pid)
                elif (key == 'type'):
                    t_type = value
                    print(t_type)
                elif (key == 'title'):
                    t_type = value
                    print(t_type)
                elif (key == 'issued'):
                    t_issued = value
                    print(t_issued)
        elif (key == "source_id"):
            t_source_id = value
            print(t_source_id)
        elif (key == "obj"):
            obj_field = uniqueEvent.get("obj")
            for key, value in obj_field.items():
                if(key == 'pid'):
                    t_obj_pid = value
                    print(t_obj_pid)
                elif(key == 'url'):
                    t_obj_url = value
                    print(t_obj_url)
        elif (key == "timestamp"):
            t_timestamp = value
            print(t_timestamp)   
        elif (key == "relation_type_id"):
            t_relation_type_id = value
            print(t_relation_type_id)