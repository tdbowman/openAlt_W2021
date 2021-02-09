# Tabish Shaikh's work

import zipfile
import zlib
import csv
import os
import pandas

# directories
dir_file = str(os.path.dirname(os.path.realpath(__file__)))
dir_results = dir_file + '\\Results\\'

def downloadResultsAsCSV(csvDir,zipName,csvName):
    # Check for any zip file with the same name
    if os.path.exists(zipName):
        # If necessary, delete it to prevent any errors
        os.remove(zipName)
    # Folder where zip file will be stored
    zipPath = dir_results + str(zipName)
    # Convert file from DataFrame to csv
    tempFile = pandas.read_csv(csvDir)
    tempFile.to_csv(csvName)
    # Zip newly created csv file
    zipfile.ZipFile(zipPath, mode = 'w', compression = zipfile.ZIP_DEFLATED).write(csvName)

if __name__ == '__main__':
    # Filler top level code
    downloadResultsAsCSV('uploadDOI_Results.csv','uploadDOI_ResultsCSV.zip','uploadDOI_Results.csv')
