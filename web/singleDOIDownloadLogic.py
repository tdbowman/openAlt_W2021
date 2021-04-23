"""
MIT License

Copyright (c) 2020 tdbowman-CompSci-F2020

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
import tempfile
import platform
import logging

import uploadDOI

#Author: 
    #Name: Mohammad Tahmid 
    #Lines 1-63
    #---------------------
#Date: 02/24/2021
#Description: Handles the fetching the data from the download feature of the bulk upload and then placing a zip file of the contents onto the users computer.
#UPDATE: This is during the beginning of version 2.0 of the project that was replaced later on in the development of this project. This placed data in directly into the MySQL database instead of filtering into MongoDB first

def articleLandingDownload(DOI, fileChoice, mysql):

    #The direcotry name to hold the temporary files that hold the DOI that will be used to search through the databases
    singleDOIDirectory = "SingleDOIs"

    #Creation of the temporyfiles directory in the folder if it does not exists. If it exists then nothing is done
    try:

        #The directory of the file is found and saved into a variable
        filePath = os.path.dirname(os.path.realpath(__file__))
        filePath = os.path.join(filePath, singleDOIDirectory)

        #Creation of the directory is done using the code below
        if not os.path.exists(filePath):
            os.makedirs(filePath)
    except:
        print("Directory for articleLanding page download not found")


    #Variable to hold the zipped file contents that will be returned
    zipEvents = ""

    #If the user selects to reeive their data in a CSV format from "fileChoice" then the code below is ran
    if fileChoice == "CSV":

        #Creation of a temporary file using tempfile module in python
        #This file is set so that it can be read and zipped up by function later
        #If the file was set to delete=True then the temp file would be deleted after it is written to
        temp = tempfile.NamedTemporaryFile(dir=filePath, suffix=".csv", delete=False, mode='w+t')

        #Writing the doi to be passed to the file
        #This info will be later passed to the download function since the download function needs to have a file to look at
        temp.write(DOI)
        temp.close()

        #Get a zip file of the data found of the DOI in the databases
        zipEvents = uploadDOI.downloadDOI(mysql, temp.name)

        #Temporary file is finally deleted to save space on the hard drive
        os.remove(temp.name)

    #TODO: This is to be implemented if/when the JSON upload and download on the bulk search is completed
    #If the user selects to reeive their data in a CSV format from "fileChoice" then the code below is ran
    elif fileChoice == "JSON":
        print("TODO: Implement JSON Data Fetch")

    #This zip file of the information is returned back to the control of the web interface and will be later downloaded to the user's computer
    return zipEvents 