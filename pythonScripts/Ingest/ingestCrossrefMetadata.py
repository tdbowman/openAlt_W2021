# This file is a modified version of crossref.py

def crossrefMetadataIngest(data, cursor, connection):
    # Initialize all values with None
    t_DOI=None
    t_URL=None
    t_abstract=None
    t_created=None
    t_lang=None
    t_primaryAuthor=None
    t_primarySubject=None
    t_publisher=None
    t_ref_count=None
    t_refby_count=None
    t_rs_count=None
    t_score=None
    t_source=None
    t_title=None
    t_type=None
    t_id=None
    # Enter the objects with the values of the fields in the JSON file.
    for key, value in data.items():
        #print(value)
        if (key == "DOI"):
            t_DOI = value
            print(t_DOI)
            if (len(t_DOI) >= 100):
                return
        elif (key == "URL"):
            t_URL = value
        elif (key == "abstract"):
            t_abstract = value
        elif (key == "created"):
            t_created = value.get("date-time")
        elif (key == "language"):
            t_lang=value
        elif (key =="author"):
            t_primaryAuthor=str(value[0].get("family"))+", "+str(value[0].get("given"))
        elif (key == "subject"):
            t_primarySubject=str(value[0])
        elif (key == "publisher"):
            t_publisher = value
        elif (key == "reference-count"):
            t_ref_count = value
        elif (key == "is-referenced-by-count"):
            t_refby_count = value
        elif (key == "references-count"):
            t_rs_count = value
        elif (key == "score"):
            t_score = value
        elif (key == "source"):
            t_source = value
        elif (key == "title"):
            t_title = str(value[0])
        elif (key == "type"):
            t_type = value
        elif (key == "_id"):
            t_id = value
    # SQL query to insert data into tobles
    add_event = ("INSERT IGNORE INTO _metadata_ "
    "(DOI, URL, abstract, datetimeCreated, language, primaryAuthor, primarySubject, publisher, "
    "referenceCount, referencedByCount, referencesCount, score, source, title, type, _id) "
    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    # Values to insert into _metadata_ event table
    data_event = (t_DOI, t_URL, t_abstract, t_created, t_lang,
                    t_primaryAuthor, t_primarySubject, t_publisher, t_ref_count,
                    t_refby_count, t_rs_count, t_score, t_source,
                    t_title, t_type,str(t_id))

    # Execute query to add information to _metadata_ event table
    cursor.execute(add_event, data_event)
    connection.commit()
    print("data stored")
    return
