from datetime import datetime as dt
import time
import requests
import json
import logging
import sys
import os
import platform

try:
    import schedule
except ImportError:
    logging.info("You need to install the schedule module using \"pip install schedule\" before proceeding")
    exit

email = "YOUR_EMAIL_HERE"
source = "" # An empty string will cause it to pull from all sources
rows = "10000" # number of Events to pull for today
fetchURL = "https://api.eventdata.crossref.org/v1/events?mailto="
tempFileName = "tempFile.json" # file which it writes data to before formatting. Overwritten on each fetchData call
logging.basicConfig(filename='tapAPI.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S') # Set the logging parameters

# THESE MAY BE CHANGED
runOnSchedule = True # False if you want to run it right now, or True if you want it to run on the regular schedule
cursor = "" # Always the first cursor, but you can change it if starting the script from a later point

def main():

    # This loop causes the fetchData function to be called on a schedule
    # This allows us to get all the data for that day, while allowing some time for the server to be busy
    if (runOnSchedule == True):
        schedule.every(1).hours.do(fetchData)
        while (True):
            schedule.run_pending()
            time.sleep(1)
    elif (runOnSchedule == False):
        fetchData() # only fetch once, for troubleshooting
    else:
        logging.info("Cannot determine how you intend to run the program")

def sendFailureEmail(message):
    # TODO: Send an email when the script fails. It needs to be restarted manually
    return

def fetchData():
    try:
        query = "curl " + "\"" + fetchURL + email + source + "&rows=" + rows + "&cursor=" + cursor + "\"" + " > " + tempFileName
        logging.info(" - Downloading Data using query: \n" + query)
        os.system(query)
        # If the data was not grabbed successfully, then sleep 20s and retry.
        # We assume it was busy on the first pass - so the response is always checked.
        serverBusy = True
        while (serverBusy):
            file = open(tempFileName, "r")
            if (file.read(6) == "Server"):
                logging.info("Server overload, Retrying in 20s...")
                file.close()
                time.sleep(20)
                os.system(query)
            else:
                file.close() # Need to close the file now that we know the first word != Server
                serverBusy = False # We have successfully gotten data
        # Now that we have the data we need to beautify it
        logging.info(" - Successfully wrote data to tempFile.json ")
        beautifyJSON()
    except:
        logging.info(" - Failure in fetchData step")
        sendFailureEmail("Failed to download the data")

def beautifyJSON():
    try:
        global cursor # so that we modify the global version, not this functions copy
        todaysDate = dt.today().strftime("%m-%d-%y--%I-%M") # Semicolons are allowed in Linux, not in Windows Paths
        # This lets us save a file in the same directory as the script if we are debugging
        if (runOnSchedule == True):
            fileName = "/home/fg7626/crossrefDataDumps/" + todaysDate + ".json"
            #fileName = todaysDate + ".json" # Use this so it writes to the same directory as script when debugging
        else:
            fileName = todaysDate + ".json" # Use this so it writes to the same directory as script when debugging
        logging.info(" - Beginning JSON formatting")
        with open(tempFileName) as json_file:
            data = json.load(json_file)
            cursor = data.get("message").get("next-cursor")
        
        #Added 1/24/2021 for run command for OS type
        if (platform.system() == 'Linux'):
            os.system("cat " + tempFileName + " | python3 -mjson.tool > " + fileName)
        elif(platform.system() == 'Windows'):
            os.system("cat " + tempFileName + " | python -mjson.tool > " + fileName)

        logging.info(" - Cursor for this retrieval was " + str(cursor))
        if (cursor == "" or cursor == None):
            logging.info(" - Null cursor - done collecting data - check log for last cursor used")
            sys.exit("exit")
        logging.info(" - Writing JSON data to " + fileName)
        logging.info(" - Waiting for next scheduled run...")
    except:
        logging.info(" - Failure in beautifyJSON step - Was the server down?")
        sendFailureEmail("Failed to beautify JSON")

if __name__ == '__main__':
    main()