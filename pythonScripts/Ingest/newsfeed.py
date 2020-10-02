def newsfeedIngest(uniqueEvent, cursor):
    for key, value in uniqueEvent.items():
        if key == "license":
            t_license = value
        elif key == "terms":
            t_terms = value
        elif (key == "updated_reason"):
            t_updatedReason = value
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
        elif (key == "action"):
            t_action = value
        elif (key == "subj"):
            subjField = uniqueEvent.get("subj")
            for key, value in subjField.items():
                if (key == 'pid'):
                    t_pid = value
                elif (key == 'type'):
                    t_type = value
                elif (key == 'title'):
                    t_title = value
                elif(key == 'url'):
                    t_url = value
        elif(key == 'source_id'):
            t_source_id = value
        elif (key == "obj"):
            objField = uniqueEvent.get("obj")
            for key, value in objField.items():
                if (key == 'pid'):
                    t_pid = value
                if (key == 'url'):
                    t__obj_url = value
        elif (key == "timestamp"):
            t_timestamp = value
        elif(key == 'updated_date'):
            t_updated_date = value
        elif(key == 'relation_type_id'):
            t_relation_type_id = value
