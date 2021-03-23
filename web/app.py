# Author: Darpan (Lines 231-251, 273-280)

import os
import flask
from flask import Flask
from flask import send_file
from flask_mysqldb import MySQL
from flask import request, jsonify, redirect, flash
from datetime import datetime

# Import our functions for other pages
from searchLogic import searchLogic
from articleDashboardLogic import articleDashboardLogic
from journalDashboardLogic import journalDashboardLogic
from authorDashboardLogic import authorDashboardLogic
from landingPageStats import landingPageStats
from landingPageArticles import landingPageArticles
from landingPageJournals import landingPageJournals
from uploadDOI import searchByDOI, getZipEvents
from uploadAuthor import searchByAuthor, getZipAuthor
from uploadUni import searchByUni, getZipUni

from getPassword import getPassword

# get the users password from crossrefeventdata/web/passwd.txt
mysql_username = 'root'
mysql_password = getPassword()

# Instantiate an object of class Flask
app = flask.Flask(__name__)
# Database connection settings
app.config['MYSQL_USER'] = mysql_username
app.config['MYSQL_PASSWORD'] = mysql_password
# Or use the database.table which will allow us to join the databases - the one with author, and the one with events
app.config['MYSQL_DB'] = 'doidata'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Database initialization and cursor
mysql = MySQL(app)

# Instantiate a second object of class Flask
app2 = flask.Flask(__name__)
# Database connection settings
app2.config['MYSQL_USER'] = mysql_username
app2.config['MYSQL_PASSWORD'] = mysql_password

# Or use the database.table which will allow us to join the databases - the one with author, and the one with events
app2.config['MYSQL_DB'] = 'crossrefeventdatamain'
app2.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Database initialization and cursor
mysql2 = MySQL(app2)

#Author:
    #Name: Mohammad Tahmid
    #Lines 57-69, 123
    #---------------------
#Date: 02/23/2021
#Description: Passes a connection for a opencitations database
#-----------------------------------------------------------
# Instantiate a third object of class Flask
app3 = flask.Flask(__name__)
# Database connection settings
app3.config['MYSQL_USER'] = mysql_username
app3.config['MYSQL_PASSWORD'] = mysql_password

# Or use the database.table which will allow us to join the databases - the one with author, and the one with events
app3.config['MYSQL_DB'] = 'opencitations'
app3.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Database initialization and cursor
mysql3 = MySQL(app3)
#-----------------------------------------------------------


# Pass on vars between pages
session = {}


@app.route('/')
def index():
    # Go to landingPageStats.py
    totalSum = landingPageStats(mysql)

    # Go to landingPageArticles.py
    totalSumArticles = landingPageArticles(mysql)

    # Go to landingPageJournals.py
    totalSumJournals = landingPageJournals(mysql)

    return flask.render_template('index.html', totalSum=totalSum, totalSumArticles=totalSumArticles, totalSumJournals=totalSumJournals)


@app.route('/searchResultsPage', methods=["GET", "POST"])
def search():

    # If a HTTPS POST Request is received...
    if(request.method == "POST"):
        dropdownValue = request.form.get('dropdownSearchBy')
    else:
        dropdownValue = str(flask.request.args.get("dropdownSearchBy"))

    # Go to searchLogic.py
    return searchLogic(mysql, mysql2, dropdownValue)


@app.route('/articleDashboard', methods=["GET", "POST"])
def articleDashboard():

    # Initialize years_list and yearInput.
    years_list = []
    yearInput = ''

    # Based on the current year, initialize the years_list list year range(5 years).
    # This is the default year range.
    currentYear = datetime.now().year
    for i in range(currentYear - 4, currentYear + 1):
        years_list.append(i)

	# If a HTTPS POST Request is received...
	#Author: Mohammad Tahmid
	#Lines: 113-127
	#Description: Gets the DOI from the article landing page and downloads the information to the users computer

    # If a HTTPS POST Request is received...
    if request.method == "POST":

        if request.form.get('articleDLChoice') is not None:
		    #File type user wants the information dowloaded as
            fileChoice = str(request.form.get("articleDLChoice"))

		    #The DOI of the aritcle that the user was viewing and wants the information of
            #fileDOI = str(request.form.get("articleDLDOI"))

		    #Zipped up contents of the data from the database
            #zipEvents = articleLandingDownload(fileDOI, fileChoice, mysql)

		    #The zipped up files are downloaded onto the user's desktop
            #return send_file(zipEvents, as_attachment=True)

        # Grab the year value from the year filter of the bar chart.
        if request.form.get('year') is not None:
            yearInput = request.form.get('year')
            yearInput = int(yearInput)
            years_list = []
            for i in range(yearInput - 2, yearInput + 3):
                years_list.append(i)

    # Go to articleDashboardLogic.py
    return articleDashboardLogic(mysql, mysql2, mysql3, years_list, yearInput)


@ app.route('/journalDashboard', methods=["GET", "POST"])
def journalDashboard():

    # Get the current year so we can pass it to the graph X axis
    # The earliest year we consider is 1997
    years_list = []
    currentYear = datetime.now().year
    for i in range(1997, currentYear + 1):
        years_list.append(i)

    # Go to journalDashboardLogic.py
    return journalDashboardLogic(mysql, years_list)


@ app.route('/authorDashboard', methods=["GET", "POST"])
def authorDashboard():

    # Initialize years_list and yearInput.
    years_list = []
    yearInput = ''

    # Based on the current year, initialize the years_list list year range(5 years).
    # This is the default year range.
    currentYear = datetime.now().year
    for i in range(currentYear - 4, currentYear + 1):
        years_list.append(i)

    # If a HTTPS POST Request is received...
    if request.method == "POST":
        # Grab the year value from the year filter of the bar chart.
        if request.form.get('year') is not None:
            yearInput = request.form.get('year')
            yearInput = int(yearInput)
            years_list = []
            for i in range(yearInput - 2, yearInput + 3):
                years_list.append(i)

    # Go to authorDashboardLogic.py
    return authorDashboardLogic(mysql, mysql2, years_list, yearInput)


@ app.route('/admin', methods=["GET", "POST"])
def adminlogin():
    return flask.render_template('admin.html')


@ app.route('/about', methods=["GET", "POST"])
def about():
    return flask.render_template('about.html')


@ app.route('/team', methods=["GET", "POST"])
def team():
    return flask.render_template('team.html')


@ app.route('/licenses', methods=["GET", "POST"])
def licenses():
    return flask.render_template('licenses.html')


@ app.route('/searchByOptions', methods=["GET", "POST"])
def searchByOptions():

    if request.method == "POST":
        select = request.form.get("uploadList")

        if select == "DOI":
            return redirect('/uploadDOI')
        elif select == "Author":
            return redirect('/uploadAuthors')
        elif select == "University":
            return redirect('/uploadUni')

    return flask.render_template('searchByOptions.html')


@ app.route('/uploadDOI', methods=["GET", "POST"])
def uploadDOI():

    # Directory of where to put the uploaded file
    app.config["UPLOAD_FILES"] = "../web/uploadFiles"
    target = app.config["UPLOAD_FILES"]

    # Allowed extensions of file
    ALLOWED_EXTENSIONS = {'csv'}

    destination = app.config["UPLOAD_FILES"]

    # Limit of the file size to 1 GB
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

    # If directory does not exist, create it
    if not os.path.isdir(target):
        os.mkdir(target)

    # If a HTTPS POST Request is received...
    if request.method == "POST":

        # If file is received...
        if request.files:

            # Retrieve the uploaded file
            uploadFiles = request.files["csv/json"]
            fileName = uploadFiles.filename

            # Check extension of file
            fileExtension = fileName.rsplit(
                '.', 1)[1].lower() in ALLOWED_EXTENSIONS

            # Check file submission
            if uploadFiles and fileExtension:
                # Save the file to the directory
                uploadFiles.save(os.path.join(target, fileName))

            session['doiPath'] = fileName

        return flask.render_template('downloadDOI.html')

    return flask.render_template('uploadDOI.html')


@ app.route('/downloadDOI', methods=["GET", "POST"])
def downloadDOI():
    if request.method == "POST":

        filepath = session.get('doiPath')
        # session['type'] = 'doi'

        dropdownValue = request.form.get('dropdownSearchBy')
        print("Download Type:", dropdownValue)

        emailVal = request.form.get('email_input')
        print("Recipient: ", emailVal)

        searchByDOI(mysql, filepath, dropdownValue, emailVal)

        return redirect('/searchComplete')
        # return flask.render_template('searchComplete.html')

    return flask.render_template('downloadDOI.html')


@ app.route('/uploadAuthors', methods=["GET", "POST"])
def uploadAuthors():

    app.config["UPLOAD_FILES"] = "../web/uploadFiles"
    destination = app.config["UPLOAD_FILES"]

    if not os.path.isdir(destination):
        os.mkdir(destination)

    if request.method=="POST":
        if request.files:
            uploadFiles = request.files["csv/json"]
            print(uploadFiles)

            fileName = uploadFiles.filename
            uploadFiles.save(os.path.join(destination, fileName))
            print("File saved.")

            session['authorPath'] = fileName

        return flask.render_template('downloadAuthors.html')

    return flask.render_template('uploadAuthors.html')





@ app.route('/downloadAuthors', methods=["GET", "POST"])
def downloadAuthors():
    if request.method=="POST":

        filepath = session.get('authorPath')

        dropdownValue = request.form.get('dropdownSearchBy')
        print("Download Type:",dropdownValue)

        emailVal = request.form.get('email_input')
        print("Recipient: ", emailVal)

        searchByAuthor(mysql, filepath, dropdownValue, emailVal)

        return redirect('/searchComplete')
        # return flask.render_template('searchComplete.html')

    return flask.render_template('downloadAuthors.html')


@ app.route('/uploadUni', methods=["GET", "POST"])
def uploadUni():

    app.config["UPLOAD_FILES"] = "../web/uploadFiles"
    destination = app.config["UPLOAD_FILES"]

    if not os.path.isdir(destination):
        os.mkdir(destination)

    if request.method=="POST":
        if request.files:
            uploadFiles = request.files["csv/json"]
            print(uploadFiles)

            fileName = uploadFiles.filename
            uploadFiles.save(os.path.join(destination, fileName))
            print("File saved.")

            session['uniPath'] = fileName

        return flask.render_template('downloadUni.html')

    return flask.render_template('uploadUni.html')


@ app.route('/downloadUni', methods=["GET", "POST"])
def downloadUni():
    if request.method=="POST":

        filepath = session.get('uniPath')

        dropdownValue = request.form.get('dropdownSearchBy')
        print("Download Type:",dropdownValue)

        emailVal = request.form.get('email_input')
        print("Recipient: ", emailVal)

        searchByUni(mysql, filepath, dropdownValue, emailVal)

        return redirect('/searchComplete')
        # return flask.render_template('searchComplete.html')



    return flask.render_template('downloadUni.html')

@ app.route('/searchComplete', methods=["GET", "POST"])
def searchComplete():
    # redirect('/searchComplete')

    # if session['type'] == 'doi':
    #     filepath = session.get('doiPath')
    #     searchByDOI(mysql, filepath)

    return flask.render_template('searchComplete.html')




# If this is the main module or main program being run (app.py)......
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
