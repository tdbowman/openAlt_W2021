# Tabish Shaikh's work

import zipfile
import zlib
import urllib.request
import json
import requests
import os

def downloadResultsAsJSON():
    # Download search results as json 
    # and save it in tempFile.json

    with urllib.request.urlopen("https://api.crossref.org/works?sample=10") as url:
        f = open('tempFile.json', 'w')
        tempfile = json.loads(url.read().decode())
        tempfile = json.dumps(tempfile, indent=4, separators=(". ", " = "))
        f.write(str(tempfile))
        f.close()

    # Zip downloaded json file

    zipfile.ZipFile('yourSearchInJSON.zip', mode = 'w', compression = zipfile.ZIP_DEFLATED).write('tempFile.json')

    # Delete the copy of the downloaded file that was not zipped

    if os.path.exists('tempFile.json'):
        os.remove('tempFile.json')

if __name__ == '__main__':
    downloadResultsAsJSON()
