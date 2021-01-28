import mysql.connector
import os
import platform
import csv

mysql_username = "root"
mysql_password = "Dsus1209."

# print("MySQL Credentials")
# mysql_username = input("Username: ")
# mysql_password = input("Password: ")

# connect to dr_bowman_doi_data_tables database
drBowmanDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "dr_bowman_doi_data_tables")

# connect to crossrefeventdatamain database
eventDatabase = mysql.connector.connect(host = "localhost", user = mysql_username, passwd = mysql_password, database = "crossrefeventdatamain")

drBowmanDatabaseCursor = drBowmanDatabase.cursor()
eventDatabaseCursor = eventDatabase.cursor()

drBowmanDatabaseCursor.execute("Select DOI FROM _main_")
articles = drBowmanDatabaseCursor.fetchall()

# To fetch event data for all articles, set numberOfArticlesToFetch = articles.length
numberOfArticlesToFetch = 500 

# create directory to store temporary JSON files
eventDataDirectory = 'eventData'

emptyDOI = (None, )


if platform.system() == "Windows":
    directory = "eventData\\events_"

elif platform.system() == "Darwin" | "Linux":
    "eventData/events_"

if not os.path.exists("eventData"):
    os.makedirs(eventDataDirectory)


with open("json_info.csv", "w", newline="") as jsonInfoFile:
    writer = csv.writer(jsonInfoFile)
    writer.writerow(["File Name", "DOI"])

    fileCounter = 1


    for i in range(numberOfArticlesToFetch):

        if (articles[i] != emptyDOI):

            article = articles[i]
            articleDOI = article[0]

            print(articleDOI)

            fileName = directory + str(fileCounter) + ".json"
            fileCounter += 1
            print(fileName)

            query = "curl " + "\"" + "https://api.eventdata.crossref.org/v1/events?mailto=YOUR_EMAIL_HERE&obj-id=" + articleDOI + "\"" + " > " + fileName
            os.system(query)

            writer.writerow([fileName[10:], articleDOI])

            eventDatabaseCursor.execute("DELETE FROM crossrefeventdatamain.main WHERE objectID = 'https://doi.org/" + articleDOI + "';")
            eventDatabase.commit()