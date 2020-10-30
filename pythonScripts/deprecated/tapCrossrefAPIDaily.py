''' TODO:
Need to catch condition when "status failed" - occurs when there is server maintainence 

Implement sendFailureEmail function

Need to delete the log file if it gets too big!
'''
from datetime import datetime as dt
import time
import requests
import json
import logging
try:
    import schedule
except ImportError:
    logging.info("You need to install the schedule module using \"pip install schedule\" before proceeding")
    exit

# False if you want to run it right now, or True if you want it to run on the regular schedule
runOnSchedule = True
email = "mitchfen@protonmail.com"
source = "" # An empty string will cause it to pull from all sources
rows = "10000" # number of Events to pull for today
fetchURL = "https://api.eventdata.crossref.org/v1/events?mailto="

# Set the logging parameters - how we want the log to look, what file its in
logging.basicConfig(filename='tapCrossrefAPIDaily.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def main():
    # This loop causes the fetchData function to be called every hour.
    # This allows us to get all the data for that day, while allowing some time for the server to be busy
    # Line 58 can be copied and provided with a different time, should we choose to run the script multiple times per day
    if (runOnSchedule == True):
        schedule.every().hour.do(fetchData)
        #schedule.every().minute.do(fetchData) # Use this one for debugging
        while True:
            schedule.run_pending()
            time.sleep(1)
    # This executes when we don't want to run it on a schedule - for testing purposes
    elif (runOnSchedule == False):
        fetchData()
    else:
        logging.info("Cannot determine how you intend to run the program")

def sendFailureEmail(message):
    # TODO: Send an email when the script fails. It needs to be restarted manually
    return

def fetchData():
    try:
        query = fetchURL + email + source + "&rows=" + rows
        logging.info(" - Downloading Data")
        response = requests.get(query)
        # If the data was not grabbed successfully, then sleep 30s and retry.
        # We assume it was busy on the first pass - so the response is always checked.
        serverBusy = True
        while (serverBusy):
            if ((response.text == "Server is overloaded, please try later") or (response.status_code not in (200, 201))):
                logging.info(" - Server is overloaded or down. Retrying in 30s...")
                time.sleep(30)
                response = requests.get(query)
            # TODO: Need to add a statement to catch the condition when "status failed" - server maintainence
            else:
                serverBusy = False # We have successfully gotten data
        # Now that we have the data we need to beautify it
        beautifyJSON(response)
    except:
        logging.info(" - Failure in fetchData step")
        sendFailureEmail("Failed to download the data")

def beautifyJSON(response):
    try:
        todaysDate = dt.today().strftime("%m-%d-%y--%I-%M") # Semicolons are allowed in Linux, not in Windows Paths
        # This lets us save a file in the same directory as the script if we are debugging
        if (runOnSchedule == True):
            fileName = "/home/fg7626/crossrefDataDumps/" + todaysDate + ".json"
        else:
            fileName = todaysDate + ".json" # Use this so it writes to the same directory as script when debugging
        logging.info(" - Beginning JSON formatting")
        jsonResponse = response.json()
        logging.info(" - Writing JSON data to " + fileName)
        with open(fileName, 'w') as f:
            json.dump(jsonResponse, f, indent=4)
    except:
        logging.info(" - Failure in beautifyJSON step")
        sendFailureEmail("Failed to beautify JSON")

if __name__ == '__main__':
    main()