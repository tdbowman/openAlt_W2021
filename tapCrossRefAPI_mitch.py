# Mitch Fenner 9/17/20
# You must have curl installed to use this script!
import os
import time

def main():

    fetchURL = "https://api.eventdata.crossref.org/v1/events?mailto="
    email = None
    source = None
    query = None
    keepGoing = True

    while (keepGoing):
            
        # Get user email
        email = input("Enter your email: ")
        email = email + "&"

        # Get user desired sources
        source = input("Enter the source (leave blank for all): ")
        if (source != ""): source = "source=" + source + "&"

        # Get user desired rows
        rows = input("Enter the number of rows: ")
        rows = "rows=" + rows
            
        # Ensure the user provided an email and row value, if not, loop again
        if (email != "" and email != None and rows !="" and rows != None): 
            keepGoing = False
        
    # Call the fetch function now that we have valid user input
    fetchData(fetchURL, email, source, rows)


# Assemble the query for CrossRef, sleep and retry if the server is busy
def fetchData(fetchURL, email, source, rows):

    query = "curl " + "\"" + fetchURL + email + source + rows + "\"" + " > all-events.json" 
    print ("Executing query: " + query)
    os.system(query)
        
    # If the data was not grabbed successfully, then sleep 20s and retry.
    # If it fails, the first word in all-events.json will be "Server" so we check that
    # We assume it was busy on the first pass - so the all-events.json is always checked.
    serverBusy = True
    while (serverBusy):
        file = open("all-events.json", "r")
        if (file.read(6) == "Server"):
            print("Server overload, Retrying in 20s...")
            file.close()
            time.sleep(20)
            os.system(query)
        else:
            file.close() # Need to close the file now that we know the first word != Server
            serverBusy = False # We have successfully gotten data

if __name__ == '__main__':
    main()