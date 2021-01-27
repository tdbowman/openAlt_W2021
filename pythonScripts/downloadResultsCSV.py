# Tabish Shaikh 1/26/21
import zipfile
import time
import csv
import requests
import os
import sys

email = "tabishshaikh97@gmail.com"
source = ""
fetchurl = "https://api.eventdata.crossref.org/v1/events?mailto="
tempFileName = "tempfile.csv"

def downloadResults():
    query = "curl" + "\"" + fetchurl + email + source + "\"" + " > " + tempFileName
    os.system(query)
    serverBusy = True
    while (serverBusy):
       file = open(tempFileName, "r")
       if (file.read(6) == "Server"):
           file.close()
           time.sleep(20)
           os.system(query)
       else:
           file.close()
           serverBusy = False

def compressFile():
    ZipFile.write(tempFileName, "test.zip", compress_type=None)

if __name__ == '__main__':
    downloadResults()
