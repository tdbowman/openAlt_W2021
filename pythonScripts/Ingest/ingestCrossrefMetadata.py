# Author: Tabish Shaikh

def crossrefMetadataIngest(data, cursor, connection, listofnames):
    # Initialize all values with None
    t_affiliation=None
    t_auth_orcid=None
    t_family=None
    t_given=None
    t_name=None
    t_orcid=None
    t_sequence=None
    t_suffix=None
    # Enter the objects with the values of the fields in the JSON file.
    for i in data:
        for key,value in i.items():
            if (key == "affiliation"):
                t_affiliation=str(value)
            elif (key == "authenticated_orcid"):
                t_auth_orcid=str(value)
            elif (key == "family"):
                t_family=str(value)
            elif (key == "given"):
                t_given=str(value)
            elif (key == "ORCID"):
                t_orcid=str(value)
            elif (key == "sequence"):
                t_sequence=str(value)
            elif (key == "suffix"):
                t_suffix=str(value)
            t_name=str(t_family)+", "+str(t_given)
            for col in listofnames:
                if col == t_name:
                    return
    # SQL query to insert data into tobles
    add_event = ("INSERT IGNORE INTO author "
    "(affiliation, authenticated_orcid, family, given, name, orcid, sequence, suffix) "
    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
    # Values to insert into _metadata_ event table
    data_event = (t_affiliation, t_auth_orcid, t_family, t_given,
                    t_name, t_orcid, t_sequence, t_suffix)

    # Execute query to add information to _metadata_ event table
    cursor.execute(add_event, data_event)
    connection.commit()
    return
