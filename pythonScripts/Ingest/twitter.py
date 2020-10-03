def twitterIngest(uniqueEvent, cursor, connection):
    t_subject_pid = None
    t_subject_title = None
    t_subject_issued = None
    t_author_url = None
    t_original_tweet_url = None
    t_original_tweet_author = None
    t_alternative_id = None
    for key, value in uniqueEvent.items():
        # for key in uniqueEvent.keys():
        if key == "license":
            t_license = value
        elif key == "terms":
            t_terms = value
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
        elif (key == "evidence_record"):
            t_evidence_record = value
        elif (key == "action"):
            t_action = value
        elif (key == "subj"):
            subjField = uniqueEvent.get("subj")
            for key, value in subjField.items():  # value of subj is a dict:
                if (key == 'pid'):
                    t_subject_pid = value
                elif (key == 'title'):
                    t_subject_title = value
                elif (key == 'issued'):
                    t_subject_issued = value
                elif(key == 'author'):
                    authorField = subjField.get("author")
                # value of author is a dict, has url
                    for key, value in authorField.items():
                        if(key == 'url'):
                            t_author_url = value
                elif(key == 'original-tweet-url'):
                    t_original_tweet_url = value
                elif(key == 'original-tweet-author'):
                    t_original_tweet_author = value
                elif(key == 'alternative-id'):
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

    # SQL which inserts into event table
    add_event = ("INSERT IGNORE INTO TwitterEvent " "(eventID, objectID, tweetAuthor, originalTweetAuthor, occurredAt, license, termsOfUse, updatedReason, updated, sourceToken, evidenceRecord, eventAction, subjectID, subjectPID, originalTweetURL, alternativeID, title, issued, sourceID, objectPID, objectURL, timeObserved, updatedDate, relationType)" "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

    # Values to insert into event table
    data_event = (t_id, t_obj_id, t_author_url, t_original_tweet_author, t_occurred_at, t_license, t_terms, t_updated_reason, t_updated, t_source_token, t_evidence_record, t_action, t_subj_id,
                  t_subject_pid, t_original_tweet_url, t_alternative_id, t_subject_title, t_subject_issued, t_source_id, t_obj_pid, t_obj_url, t_timestamp, t_updated_date, t_relation_type_id)

    add_to_main = (
        "INSERT IGNORE INTO main(objectID) VALUES (\'" + t_obj_id + "\');")

    cursor.execute(add_to_main)
    cursor.execute(add_event, data_event)  # add information to reddit table
    print(cursor.rowcount, "record inserted.")
    # Helps check if rows are inserting. Helps me sleep at night. print(cursor.rowcount, "record inserted.")
    connection.commit()
