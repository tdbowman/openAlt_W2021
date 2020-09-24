''' TODO:
Instead of printing to a the console, we should print to an error log
    import logging - see: https://realpython.com/python-logging/#the-logging-module

Catch condition when "status failed" - occurs when there is server maintainence 

Implement sendFailureEmail function
    Might be able to put the entire log into the failure email that goes out
'''
import datetime
import time
import requests
import json
try:
    import schedule
except ImportError:
    print("You need to install the schedule module using \"pip install schedule\" before proceeding")
    exit

# False if you want to run it right now, or True if you want it to run on the regular schedule
runOnSchedule = True

# These variables build the query we send to crossref
email = "mitchfen@protonmail.com"
source = "" # An empty string will cause it to pull from all sources
rows = "10000" # number of Events to pull for today
fetchURL = "https://api.eventdata.crossref.org/v1/events?mailto="

def sendFailureEmail(message):
    # TODO: Send an email when the script fails. It needs to be restarted manually
    return

def beautifyJSON(response):
    try:
        todaysDate = datetime.datetime.today().strftime("%m-%d-%y--%I:%M")
        fileName = "/home/fg7626/crossrefDataDumps/" + todaysDate + ".json" # ex: 9-21-2020.json
        fileName = todaysDate + ".json" # ex: 9-21-2020.json
        print("Beginning JSON formatting")
        jsonResponse = response.json()
        print("Writing JSON data to file")
        with open(fileName, 'w') as f:
            json.dump(jsonResponse, f, indent=4)
    except:
        print ("Failure in beautifyJSON step")
        sendFailureEmail("Failed to beautify JSON")

def fetchData():
    try:
        query = fetchURL + email + source + "&rows=" + rows
        print ("Downloading Data")
        response = requests.get(query)
        # If the data was not grabbed successfully, then sleep 30s and retry.
        # We assume it was busy on the first pass - so the response is always checked.
        serverBusy = True
        while (serverBusy):
            if ((response.text == "Server is overloaded, please try later") or (response.status_code not in (200, 201))):
                print("Server is overloaded or down. Retrying in 30s...")
                time.sleep(30)
                response = requests.get(query)
            # TODO: Need to add a statement to catch the condition when "status failed" - server maintainence
            else:
                serverBusy = False # We have successfully gotten data
        # Now that we have the data we need to beautify it
        beautifyJSON(response)
    except:
        print ("Failure in fetchData step")
        sendFailureEmail("Failed to download the data")
    
# This loop causes the fetchData function to be called every hour.
# This allows us to get all the data for that day, while allowing some time for the server to be busy
# Line 58 can be copied and provided with a different time, should we choose to run the script multiple times per day
if (runOnSchedule == True):
    #schedule.every().day.at("00:30").do(fetchData)
    schedule.every().hour.do(fetchData)
    while True:
        schedule.run_pending()
        time.sleep(60)
# This executes when we don't want to run it on a schedule - for testing purposes
elif (runOnSchedule == False):
    fetchData()
else:
    print("Cannot determine how you intend to run the program")