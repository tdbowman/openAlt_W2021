# This file is a modified version of crossref.py

def crossrefMetadataIngest(data, cursor, connection):
    t_indexed=None
    t_rc=None
    t_publisher=None
    t_issue=None
    t_content_domain=None
    t_published=None
    t_abstract=None
    t_type=None
    t_created=None
    t_source=None
    t_irbc=None
    t_title=None
    t_prefix=None
    t_member=None
    t_event_name=None
    t_event_loc=None
    t_container_title=None
    t_deposited=None
    t_score=None
    t_issued_date=None
    t_ref_count=None
    t_URL=None
    # Initialize the temporary objects with the values of the fields in the JSON file.
    for key, value in data.items():
        if (key == "DOI"):
            t_DOI = value
            if (len(t_DOI) >= 100):
                return
        elif (key == "indexed"):
            t_indexed = value.get("date-time")
        elif (key == "reference-count"):
            t_rc = value
        elif (key == "publisher"):
            t_publisher = value
        elif (key == "issue"):
            t_issue = value
        elif (key == "content-domain"):
            t_content_domain = value.get("domain")
        elif (key == "abstract"):
            t_abstract = value
        elif (key == "type"):
            t_type = value
        elif (key == "created"):
            t_created = value.get("date-time")
        elif (key == "source"):
            t_source = value
        elif (key == "is-referenced-by-count"):
            t_irbc = value
        elif (key == "title"):
            t_title = str(value[0])
        elif (key == "prefix"):
            t_prefix = value
        elif (key == "member"):
            t_member = value
        elif (key == "event"):
            t_event_name = value.get("name")
            t_event_loc = value.get("location")
        elif (key == "container-title") or (key == "short-container-title"):
            t_container_title = str(value[0])
        elif (key == "deposited"):
            t_deposited = value.get("date-time")
        elif (key == "score"):
            t_score = value
        elif (key == "references-count"):
            t_ref_count = value
        elif (key == "URL"):
            t_URL = value

    add_event = ("INSERT INTO _metadata_" "(DOI, dateTime, referenceCount, publisher, issue, contentDomain, abstract, type, created, source, isReferencedByCount, title, prefix, member, eventName, eventLocation, containerTitle, deposited, score, referencesCount, URL) " "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

    # Values to insert into _metadata_ event table
    data_event = (str(t_DOI), str(t_indexed), int(t_rc), str(t_publisher), str(t_issue),
                  str(t_content_domain), str(t_abstract), str(t_type), str(t_created), str(t_source),
                  int(t_irbc), str(t_title), str(t_prefix), str(t_member), str(t_event_name), str(t_event_loc), str(t_container_title),
                  str(t_deposited), str(t_score), int(t_ref_count), str(t_URL))

    # Execute query to add information to _metadata_ event table
    cursor.execute(add_event, data_event)
    connection.commit()
    return
