# You must have curl installed to use this script!
# We may need to change the number of rows and the frequency of the schedule
import datetime
import os
import time

try:
    import schedule
except ImportError:
    print("You need to install the schedule module using \"pip install schedule\" before proceeding")
    exit

# Modifiable Variables
email = "mitchfen@protonmail.com"
source = "" # An empty string will cause it to pull from all sources
rows = "1" # number of Events to pull for today
fetchURL = "https://api.eventdata.crossref.org/v1/events?mailto="

def sendFailureEmail(message):
    # TODO: Send an email when the script fails. It needs to be restarted manually
    return

def beautifyJSON(tempFileName):
    try:
        # Using the Linux shell is my preffered method to beautify the JSON
        # This allows me to beaufity it in one line of code
        # https://docs.python.org/3/library/json.html
        todaysDate = datetime.datetime.today().strftime("%m-%d-%y")
        #fileName = "/home/fg7626/crossrefDataDumps/" + str(todaysDate) + ".json" # ex: 9-21-2020.json
        datedFile = todaysDate + ".json" # ex: 9-21-2020.json
        os.system("cat " + tempFileName + " | python -mjson.tool > " + datedFile)
    except:
        sendFailureEmail("Failed to beautify JSON today")

def fetchData():
    try:
        tempFileName = "tempFile.json"
        query = "curl " + "\"" + fetchURL + email + source + "&rows=" + rows + "\"" + " > " + tempFileName
        os.system(query)

        # If the data was not grabbed successfully, then sleep 20s and retry.
        # If it fails, the first word in all-events.json will be "Server" so we check that
        # We assume it was busy on the first pass - so the all-events.json is always checked.
        serverBusy = True
        while (serverBusy):
            file = open(tempFileName, "r")
            if (file.read(6) == "Server"):
                print("Server overload, Retrying in 20s...")
                file.close()
                time.sleep(20)
                os.system(query)
            else:
                file.close() # Need to close the file now that we know the first word != Server
                serverBusy = False # We have successfully gotten data
        # Now that we have the data we need to beautify it
        beautifyJSON(tempFileName)
    except:
        print ("Failure")
        sendFailureEmail("Failed to download the data today")
        
# This loop causes the fetchData function to be called once a day at 11:40 pm
# This allows us to get all the data for that day, while allowing some time for the server to be busy
schedule.every().day.at("11:40").do(fetchData)
while True:
    schedule.run_pending()
    time.sleep(60)