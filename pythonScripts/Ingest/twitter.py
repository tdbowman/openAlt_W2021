def twitterIngest(uniqueEvent, cursor):
    for key, value in uniqueEvent.items():
        # for key in uniqueEvent.keys():
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
            for key, value in subjField.items():  # value of subj is a dict:
                if (key == 'pid'):
                    t_pid = value  # pid
                elif (key == 'title'):
                    t_title = value  # title
                elif (key == 'issued'):
                    t_issued = value  # issued
                elif(key == 'author'):
                    authorField = subjField.get("author")
                # value of author is a dict, has url
                    for key, value in authorField.items():
                        if(key == 'url'):
                            t_url = value
                elif(key == 'original-tweet-url'):  # original-tweet-url
                    t_original_tweet_url = value
                elif(key == 'original-tweet-author'):  # original-tweet-author
                    t_original_tweet_author = value
                elif(key == 'alternative-id'):  # alternative-id
                    t_alternative_id = value
        elif (key == "source_id"):
            t_source_id = value
        elif (key == "obj"):
            obj_field = uniqueEvent.get("obj")
            for key, value in obj_field.items():  # Value of obj is a dict:
                if(key == 'pid'):
                    t_obj_pid = value  # pid
                elif(key == 'url'):
                    t_obj_url = value  # url
        elif (key == "timestamp"):
            t_timestamp = value
        elif (key == "updated_date"):
            t_updated_date = value
        elif (key == "relation_type_id"):
            t_relation_type_id = value
    # cursor.execute()
    # Execute some complex SQL statement here
    # INSERT INTO IN
