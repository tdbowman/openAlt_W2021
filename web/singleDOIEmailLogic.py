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
    #Lines 1-54
    #---------------------
#Date: 03/08/2021
#Description: Handles the fetching the data from the download feature of the bulk upload and then placing a zip file of the contents onto the users computer.

def articleLandingEmail(mysql, fileDOI, fileChoice, fileEmail):

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
    #zipEvents = ""

    #If the user selects to reeive their data in a CSV format from "fileChoice" then the code below is ran
    
    #Creation of a temporary file using tempfile module in python
    #This file is set so that it can be read and zipped up by function later
    #If the file was set to delete=True then the temp file would be deleted after it is written to
    temp = tempfile.NamedTemporaryFile(dir=filePath, suffix=".csv", delete=False, mode='w+t')

    #Writing the doi to be passed to the file
    #This info will be later passed to the download function since the download function needs to have a file to look at
    temp.write(fileDOI)
    print(temp.name)
    temp.close()

    #Get a zip file of the data found of the DOI in the databases
    uploadDOI.downloadDOI(mysql, temp.name, fileChoice, fileEmail)

    #Temporary file is finally deleted to save space on the hard drive
    os.remove(temp.name) 