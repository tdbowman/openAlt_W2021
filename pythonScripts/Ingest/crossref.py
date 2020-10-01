def crossrefIngest(uniqueEvent, cursor):
    for key, value in uniqueEvent.items():
        if key == "license":
            t_license = value
            print(t_license)
        elif key == "obj_id":
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
        elif (key == "terms"):
            t_terms = value
            print(t_terms)
        elif (key == "message_action"):
            t_message_action = value
            print(t_message_action)
        elif (key == "source_id"):
            t_source_id = value
            print(t_source_id)
        elif (key == "timestamp"):
            t_timestamp = value
            print(t_timestamp)
        elif (key == "relation_type_id"):
            t_relation_type_id = value
            print(t_relation_type_id)