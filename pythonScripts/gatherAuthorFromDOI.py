import json
import argparse
import pandas as pd
import csv 
import os
import crossref
import platform


tempDir = "AuthorMetaData"
csvLineCount = 0
currentRows = 0

try: 

    filePath = os.path.abspath(__file__)
    directoryName = os.path.dirname(filePath)
    os.chdir(directoryName)

    if not os.path.isdir(tempDir):
        os.makedirs(tempDir)
    
    csvData = pd.read_csv("DOIValues.csv", header = None)
    csvLineCount = len(list(csvData.index))
except OSError:

    print("Cannot change directory to the location of this file")
except:

    print("Unspecified Error, Exiting")


if (platform.system() == 'Linux'):

     directoryName = directoryName + "/" + tempDir 

elif(platform.system() == 'Windows'):

    directoryName = directoryName + "\\" + tempDir

with open('DOIValues.csv', newline='') as csvFile:
        lineIn = csv.reader(csvFile)

        while currentRows < csvLineCount:
            
            csvRow = next(lineIn) 
            StringConvert = ""
            csvLineString = StringConvert.join(csvRow)

            try:
                from crossref.restful import Works
                works = Works()
                doiMetaData = works.doi(csvLineString)

                if (doiMetaData['author']):

                    authorList = doiMetaData['author']

                    '''
                    filePlace = directoryName + "\\" + csvLineString + "_MetaData.json"
                    with open(filePlace, "w+") as write_file:
                        #json_object = json.dump(authorList)
                        #write_file.write(json_object)
                        json.dump(authorList, write_file 
                    '''
            except ImportError:
                print("Installation of the Crossref API is needed")
            except:
                print("Unknown Error")

            currentRows += 1
            if currentRows > csvLineCount:
                currentRows = csvLineCount