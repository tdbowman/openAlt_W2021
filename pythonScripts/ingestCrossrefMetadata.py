# Author: Tabish Shaikh

from getCountry import extract_country
from getUniversity import extract_university

def crossrefMetadataIngest(data, cursor, connection, fk):
    # Initialize all values with None
    t_affiliation = None
    t_auth_orcid = None
    t_country = None
    t_family = None
    t_given = None
    t_name = None
    t_orcid = None
    t_sequence = None
    t_suffix = None
    t_uni = None
    t_fk = None
    # Enter the objects with the values of the fields in the JSON file.
    for key,value in data.items():
        if (key == "affiliation"):
            t_affiliation = str(value)
            if t_affiliation != "[]":
                t_country = extract_country(t_affiliation)
                t_uni = extract_university(t_affiliation)
        elif (key == "authenticated_orcid"):
            t_auth_orcid = str(value)
        elif (key == "family"):
            t_family = str(value)
        elif (key == "given"):
            t_given = str(value)
        elif (key == "ORCID"):
            t_orcid = str(value)
        elif (key == "sequence"):
            t_sequence = str(value)
        elif (key == "suffix"):
            t_suffix = str(value)
        t_name = str(t_family) + ", " + str(t_given)
        t_fk = fk
    # SQL query to insert data into tobles
    add_event = ("INSERT IGNORE INTO author "
    "(affiliation, country, university, authenticated_orcid, family, given, name, orcid, sequence, suffix, fk) "
    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    # Values to insert into _metadata_ event table
    data_event = (t_affiliation, t_country, t_uni, t_auth_orcid, t_family, t_given,
                    t_name, t_orcid, t_sequence, t_suffix, t_fk)

    # Execute query to add information to _metadata_ event table
    cursor.execute(add_event, data_event)
    connection.commit()
    return
