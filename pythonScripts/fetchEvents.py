import mysql.connector
import os

db = mysql.connector.connect(host = "localhost", user = "root", passwd = "Dsus1209.", database = "dr_bowman_doi_data_tables")
db2 = mysql.connector.connect(host = "localhost", user = "root", passwd = "Dsus1209.", database = "crossrefeventdatamain")

mycursor = db.cursor()
mycursor2 = db2.cursor()

mycursor.execute("Select DOI FROM _main_")
records = mycursor.fetchall()

temp = (None, )
source = ""
cursor = ""

for i in range(500):
    if (records[i] != temp):
        print (records[i])
        temp = records[i]
        testString = temp[0]
        filename = "data\\test" + str(i) + ".json"
        query = "curl " + "\"" + "https://api.eventdata.crossref.org/v1/events?mailto=YOUR_EMAIL_HERE&rows=10&obj-id=" + testString + "\"" + " > " + filename
        os.system(query)
        mycursor2.execute("DELETE FROM crossrefeventdatamain.main WHERE objectID = 'https://doi.org/" + testString + "';")
        db2.commit()