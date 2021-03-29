import os
import json
import flask
from flask import Flask
from flask import send_file
from flask_mysqldb import MySQL
from flask import request, jsonify, redirect, flash
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

# Import for password creation
import random
import string

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
from emailError import emailError
from emailAdmin import emailAdmin
from singleDOIEmailLogic import articleLandingEmail
from getCount import uploadDOIList, getStats
import dbQuery

from getPassword import getPassword, SECRET_KEY, SITE_KEY

from resultsForm import ResultForm
from flask_bootstrap import Bootstrap


# current directory
path = os.getcwd()

# parent directory
parent = os.path.dirname(path)
config_path = os.path.join(parent, "config", "openAltConfig.json")

# config file
f = open(config_path)
APP_CONFIG = json.load(f)


# get the users password from crossrefeventdata/web/passwd.txt
mysql_username = 'root'
mysql_password = getPassword()

# Instantiate an object of class Flask
app = flask.Flask(__name__)
app.secret_key = "OpenAlt"

# Database connection settings
app.config['MYSQL_USER'] = mysql_username
app.config['MYSQL_PASSWORD'] = mysql_password
# Or use the database.table which will allow us to join the databases - the one with author, and the one with events
app.config['MYSQL_DB'] = 'doidata'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Database initialization and cursor
mysql = MySQL(app)

# global variable to store admin password
glpass = ""

# test
logged = False

# for reCAPTCHA
app.config['SECRET_KEY'] = os.urandom(32)
app.config['RECAPTCHA_PUBLIC_KEY'] = SITE_KEY
app.config['RECAPTCHA_PUBLIC_KEY'] = SECRET_KEY


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

# Author:
# Name: Mohammad Tahmid
# Lines 57-69, 123
# ---------------------
# Date: 02/23/2021
# Description: Passes a connection for a opencitations database
# -----------------------------------------------------------
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
# -----------------------------------------------------------


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

    # OR request.environ['REMOTE_ADDR']
    print("IP ADDRESS:", request.remote_addr)

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

    citation_years_list = []
    citationYearInput = ''

    # Based on the current year, initialize the years_list list year range(5 years).
    # This is the default year range.
    currentYear = datetime.now().year
    for i in range(currentYear - 4, currentYear + 1):
        years_list.append(i)
        citation_years_list.append(i)

        # If a HTTPS POST Request is received...
        # Author: Mohammad Tahmid
        # Lines: 113-127
        # Description: Gets the DOI from the article landing page and downloads the information to the users computer

    # If a HTTPS POST Request is received...
    if request.method == "POST":

        if request.form.get('articleDLChoice') is not None:
            # File type user wants the information dowloaded as
            fileChoice = str(request.form.get("articleDLChoice"))

            # The DOI of the aritcle that the user was viewing and wants the information of
            fileDOI = str(request.form.get("articleDLDOI"))

            # The email the user entered is retreived and stored
            fileEmail = str(request.form.get("email_input"))

            try:
                valid = validate_email(fileEmail)
                valid = valid.email
                print(valid)

                flash("Your results will be emailed to you shortly. Thank You.", "valid")

                # Zipped up contents of the data from the database
                articleLandingEmail(mysql, fileDOI, fileChoice, valid)

                # return flask.render_template('searchComplete.html')

            except EmailNotValidError as e:
                print(e)
                flash(
                    "You have entered an invalid email address. Please try again.", "danger")
                # session.pop('_flashes', None)

            # Zipped up contents of the data from the database
            # zipEvents = articleLandingDownload(mysql, fileDOI, fileChoice, fileEmail)

            # The zipped up files are downloaded onto the user's desktop
            # return send_file(zipEvents, as_attachment=True)

        # Grab the year value from the year filter of the bar chart.
        if request.form.get('year') is not None:
            yearInput = request.form.get('year')
            yearInput = int(yearInput)
            years_list = []
            for i in range(yearInput - 2, yearInput + 3):
                years_list.append(i)


        if request.form.get('citationYear') is not None:
            citationYearInput = request.form.get('citationYear')
            citationYearInput = int(citationYearInput)
            citation_years_list = []
            for i in range(citationYearInput - 2, citationYearInput + 3):
                citation_years_list.append(i)

    # Go to articleDashboardLogic.py
    return articleDashboardLogic(mysql, mysql2, mysql3, years_list, yearInput, citation_years_list, citationYearInput)


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
    app.config["UPLOAD_FILES"] = "./web/uploadFiles"
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

            uploadDOIList(mysql, fileName)

        return flask.render_template('downloadDOI.html', results = getStats())

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

        try:
            if dbQuery.checkUser(emailVal, 'doi', mysql.connection.cursor()) is True:
                searchByDOI(mysql, filepath, dropdownValue, emailVal)
                return redirect('/searchComplete')
            else:
                return redirect('/limitReached')
        except Exception as e:
            print(e)
            emailError(emailVal, 'doi')
            return redirect('/searchError')

        # return flask.render_template('searchComplete.html')

    return flask.render_template('downloadDOI.html')


@ app.route('/uploadAuthors', methods=["GET", "POST"])
def uploadAuthors():

    app.config["UPLOAD_FILES"] = "./web/uploadFiles"
    destination = app.config["UPLOAD_FILES"]

    if not os.path.isdir(destination):
        os.mkdir(destination)

    if request.method == "POST":
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
    if request.method == "POST":

        filepath = session.get('authorPath')

        dropdownValue = request.form.get('dropdownSearchBy')
        print("Download Type:", dropdownValue)

        emailVal = request.form.get('email_input')
        print("Recipient: ", emailVal)

        try:
            if dbQuery.checkUser(emailVal, 'author', mysql.connection.cursor()) is True:
                searchByAuthor(mysql, filepath, dropdownValue, emailVal)
                return redirect('/searchComplete')
            else:
                return redirect('/limitReached')
        except Exception as e:
            print(e)
            emailError(emailVal, 'author')
            return redirect('/searchError')

        return redirect('/searchComplete')
        # return flask.render_template('searchComplete.html')

    return flask.render_template('downloadAuthors.html')


@ app.route('/uploadUni', methods=["GET", "POST"])
def uploadUni():

    app.config["UPLOAD_FILES"] = "./web/uploadFiles"
    destination = app.config["UPLOAD_FILES"]

    if not os.path.isdir(destination):
        os.mkdir(destination)

    if request.method == "POST":
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
    if request.method == "POST":

        filepath = session.get('uniPath')

        dropdownValue = request.form.get('dropdownSearchBy')
        print("Download Type:", dropdownValue)

        emailVal = request.form.get('email_input')
        print("Recipient: ", emailVal)

        try:
            if dbQuery.checkUser(emailVal, 'uni', mysql.connection.cursor()) is True:
                searchByUni(mysql, filepath, dropdownValue, emailVal)
                return redirect('/searchComplete')
            else:
                return redirect('/limitReached')
        except Exception as e:
            print(e)
            emailError(emailVal, 'uni')
            return redirect('/searchError')

        return redirect('/searchComplete')
        # return flask.render_template('searchComplete.html')

    return flask.render_template('downloadUni.html')


@ app.route('/searchComplete', methods=["GET", "POST"])
def searchComplete():
    return flask.render_template('searchComplete.html')


@ app.route('/searchError', methods=["GET", "POST"])
def searchError():
    return flask.render_template('searchError.html')


@ app.route('/limitReached', methods=["GET", "POST"])
def limitReached():
    limit = APP_CONFIG['User-Result-Limit']['limit']
    interval = APP_CONFIG['User-Result-Limit']['dayInterval']
    print(flask.request.remote_addr)
    return flask.render_template('limitReached.html', limit=limit, interval=interval)


@ app.route('/captchaTest', methods=["GET", "POST"])
def captchaTest():
    form = ResultForm()
    if form.validate_on_submit():
        return flask.render_template('searchComplete.html')

    return flask.render_template('captchaTest.html', form=form)


@ app.route('/admin', methods=["GET", "POST"])
def admin():
    if request.method=="GET":
        global logged
        logged = False

        # Password creation
        source = string.ascii_letters + string.digits
        pw = ''.join((random.choice(source) for i in range(10)))

        emailAdmin(pw)
        global glpass
        glpass = pw
        return flask.render_template('adminLogin.html', pw = pw)
    elif request.method=="POST":
        if request.form['pw_input']==glpass:

            logged = True
            return redirect('/adminConfigUpdate')
        else:
            return redirect('/admin')
    else:
        return redirect('/admin')


@ app.route('/adminConfigUpdate', methods=["GET", "POST"])
def adminConfigUpdate():
    global logged
    if logged == False:
        return redirect('/admin')
    elif request.method == "GET":
        return flask.render_template('adminConfigUpdate.html', confOA=APP_CONFIG)
    elif request.method == "POST":
        dict01 = request.form['key0.1']
        APP_CONFIG["Admin"]["email"] = dict01
        dict11 = request.form['key1.1']
        dict12 = request.form['key1.2']
        dict13 = request.form['key1.3']
        dict14 = request.form['key1.4']
        APP_CONFIG["DOI-Database"]["name"] = dict11
        APP_CONFIG["DOI-Database"]["username"] = dict12
        APP_CONFIG["DOI-Database"]["password"] = dict13
        APP_CONFIG["DOI-Database"]["address"] = dict14
        dict21 = request.form['key2.1']
        dict22 = request.form['key2.2']
        dict23 = request.form['key2.3']
        dict24 = request.form['key2.4']
        APP_CONFIG["Crossref-Event-Database"]["name"] = dict21
        APP_CONFIG["Crossref-Event-Database"]["username"] = dict22
        APP_CONFIG["Crossref-Event-Database"]["password"] = dict23
        APP_CONFIG["Crossref-Event-Database"]["address"] = dict24
        dict31 = request.form['key3.1']
        dict32 = request.form['key3.2']
        dict33 = request.form['key3.3']
        dict34 = request.form['key3.4']
        APP_CONFIG["OpenCitations"]["name"] = dict31
        APP_CONFIG["OpenCitations"]["username"] = dict32
        APP_CONFIG["OpenCitations"]["password"] = dict33
        APP_CONFIG["OpenCitations"]["address"] = dict34
        dict41 = request.form['key4.1']
        dict42 = request.form['key4.2']
        dict43 = request.form['key4.3']
        dict44 = request.form['key4.4']
        dict45 = request.form['key4.5']
        APP_CONFIG["MongoDB-SciELO-Database"]["name"] = dict41
        APP_CONFIG["MongoDB-SciELO-Database"]["collection"] = dict42
        APP_CONFIG["MongoDB-SciELO-Database"]["username"] = dict43
        APP_CONFIG["MongoDB-SciELO-Database"]["password"] = dict44
        APP_CONFIG["MongoDB-SciELO-Database"]["address"] = dict45
        dict51 = request.form['key5.1']
        dict52 = request.form['key5.2']
        APP_CONFIG["Crossref-Event-API"]["name"] = dict51
        APP_CONFIG["Crossref-Event-API"]["url"] = dict52
        dict61 = request.form['key6.1']
        dict62 = request.form['key6.2']
        dict63 = request.form['key6.3']
        dict64 = request.form['key6.4']
        APP_CONFIG["Crossref-Metadata-API"]["name"] = dict61
        APP_CONFIG["Crossref-Metadata-API"]["doi_url"] = dict62
        APP_CONFIG["Crossref-Metadata-API"]["author_url"] = dict63
        APP_CONFIG["Crossref-Metadata-API"]["uni_url"] = dict64
        dict71 = request.form['key7.1']
        dict72 = request.form['key7.2']
        APP_CONFIG["OpenCitations-Citation-API"]["name"] = dict71
        APP_CONFIG["OpenCitations-Citation-API"]["url"] = dict72
        dict81 = request.form['key8.1']
        dict82 = request.form['key8.2']
        APP_CONFIG["OpenCitations-Citation-Count-API"]["name"] = dict81
        APP_CONFIG["OpenCitations-Citation-Count-API"]["url"] = dict82
        dict91 = request.form['key9.1']
        dict92 = request.form['key9.2']
        APP_CONFIG["OpenCitations-Reference-API"]["name"] = dict91
        APP_CONFIG["OpenCitations-Reference-API"]["url"] = dict92
        dict101 = request.form['key10.1']
        dict102 = request.form['key10.2']
        APP_CONFIG["OpenCitations-Reference-Count-API"]["name"] = dict101
        APP_CONFIG["OpenCitations-Reference-Count-API"]["url"] = dict102
        dict111 = request.form['key11.1']
        dict112 = request.form['key11.2']
        APP_CONFIG["SciELO-Brazil-Data-API"]["name"] = dict111
        APP_CONFIG["SciELO-Brazil-Data-API"]["url"] = dict112
        dict121 = request.form['key12.1']
        dict122 = request.form['key12.2']
        APP_CONFIG["User-Result-Limit"]["limit"] = dict121
        APP_CONFIG["User-Result-Limit"]["dayInterval"] = dict122
        with open("../config/openAltConfig.json", "w") as f:
            json.dump(APP_CONFIG, f, indent=4)
        f.close()
        logged = False
        return flask.render_template('adminUpdateComplete.html')
    else:
        return redirect('/admin')


# If this is the main module or main program being run (app.py)......
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
