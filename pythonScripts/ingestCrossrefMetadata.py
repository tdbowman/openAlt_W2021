# Author: Tabish Shaikh
"""
MIT License

Copyright (c) 2020 tdbowman-CompSci-F2020

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
