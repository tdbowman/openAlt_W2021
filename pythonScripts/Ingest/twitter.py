
def twitterIngest(uniqueEvent, cursor):
    for key, value in uniqueEvent.items():
        # for key in uniqueEvent.keys():
        if key == "license":
            t_license = value
            print(t_license)
        elif key == "terms":
            t_terms = value
            print(t_terms)
        elif (key == "updated_reason"):
            t_updatedReason = value
            print(t_updatedReason)
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
        elif (key == "evidence_record"):
            t_evidence_record = value
            print(t_evidence_record)
        elif (key == "action"):
            t_action = value
            print(t_action)
        elif (key == "subj"):
            subjField = uniqueEvent.get("subj")
            for key, value in subjField.items():  # value of subj is a dict:
                if (key == 'pid'):
                    t_pid = value  # pid
                    print(t_pid)
                elif (key == 'title'):
                    t_title = value  # title
                    print(t_title)
                elif (key == 'issued'):
                    t_issued = value  # issued
                    print(t_issued)
                elif(key == 'author'):
                    authorField = subjField.get("author")
                # value of author is a dict, has url
                    for key, value in authorField.items():
                        if(key == 'url'):
                            t_url = value
                            print(t_url)
                elif(key == 'original-tweet-url'):  # original-tweet-url
                    t_original_tweet_url = value
                    print(t_original_tweet_url)
                elif(key == 'original-tweet-author'):  # original-tweet-author
                    t_original_tweet_author = value
                    print(t_original_tweet_author)
                elif(key == 'alternative-id'):  # alternative-id
                    t_alternative_id = value
                    print(t_alternative_id)
        elif (key == "source_id"):
            t_source_id = value
            print(t_source_id)
        elif (key == "obj"):
            obj_field = uniqueEvent.get("obj")
            for key, value in obj_field.items():  # Value of obj is a dict:
                if(key == 'pid'):
                    t_obj_pid = value  # pid
                    print(t_obj_pid)
                elif(key == 'url'):
                    t_obj_url = value  # url
                    print(t_obj_url)
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
