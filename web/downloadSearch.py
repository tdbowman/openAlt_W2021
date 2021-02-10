# Tabish Shaikh's work

import zipfile
import zlib
import urllib.request
import json
import csv
import requests
import os
import pandas

# Modified version of downloadResultsJSON.py
# Could be refactored

def downloadResultsAsCSV():
    # Download search results as json
    # and save it in tempFile.json

    with urllib.request.urlopen("https://api.crossref.org/works?sample=10") as url:
        f = open('tempFile.json', 'w')
        tempfile = json.loads(url.read())
        tempfile = json.dumps(tempfile)
        f.write(str(tempfile))
        f.close()

        # Translate json file into a csv file

        tempfile = pandas.read_json('tempFile.json')
        tempfile = tempfile['message']
        tempfile = tempfile['items']
        tempfile = pandas.DataFrame(tempfile)
        tempfile.to_csv('tempFile.csv')

    # Zip newly created csv file

    zipfile.ZipFile('yourSearchInCSV.zip', mode = 'w', compression = zipfile.ZIP_DEFLATED).write('tempFile.csv')

    # Delete the copy of the files that were not zipped

    if os.path.exists('tempFile.json'):
        os.remove('tempFile.json')
    if os.path.exists('tempFile.csv'):
        os.remove('tempFile.csv')

if __name__=='__main__':
    downloadResultsAsCSV()