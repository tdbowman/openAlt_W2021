# Tabish Shaikh's work

import zipfile
import zlib
import csv
import os
import pandas

# Modified version of downloadResultsJSON.py
# Could be refactored

# directories
dir_file = str(os.path.dirname(os.path.realpath(__file__)))
dir_results = dir_file + '\\Results\\'

def downloadResultsAsCSV(csvDir,zipName,csvName):
    zipPath = dir_results + str(zipName)

    tempFile = pandas.read_csv(csvDir)
    tempFile.to_csv(csvName)

    # Zip newly created csv file

    zipfile.ZipFile(zipPath, mode = 'w', compression = zipfile.ZIP_DEFLATED).write(csvName)

    # Delete the copy of the files that were not zipped

    if os.path.exists(csvDir):
         os.remove(csvDir)

if __name__=='__main__':
    downloadResultsAsCSV('placeholder.csv','testName','testCSVName')
